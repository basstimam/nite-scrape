import requests, random, json, re, urllib3
from bs4 import BeautifulSoup
from urllib.parse import unquote
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://lightbrd.com",
    "https://nitter.lucabased.xyz",
    "https://nitter.space",
    "https://nitter.moomoo.me",
    "https://nitter.lunar.icu"
]

class Tweet:
    def instance():
        for instance in random.sample(NITTER_INSTANCES, len(NITTER_INSTANCES)):
            try:
                if requests.get(instance, timeout=5).status_code == 200: return instance
            except requests.exceptions.RequestException: continue
        raise Exception(" no instance available")

    def posts(search="tweets", query="", since=None, until=None, near=None, lang=None, limit=10, verbose=False):
        instance = Tweet.instance()
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0" }

        params = {"f": search, "q": query}
        if since: params["since"] = since
        if until: params["until"] = until
        if near: params["near"] = near
        if lang: params["lang"] = lang

        tweets_data = []
        page = 1

        try:
            while len(tweets_data) < limit:
                print(f"[{len(tweets_data)}/{limit}] retrieving tweets...") if verbose else None
                success = False
                for instance in random.sample(NITTER_INSTANCES, len(NITTER_INSTANCES)):  
                    response = requests.get(f"{instance}/search", params=params, headers=headers, verify=False)
                    if response.status_code == 200:
                        success = True
                        break  
                    print(f"[{len(tweets_data)}/{limit}] failed to fetch tweets, retrying...") if verbose else None
                    instance = Tweet.instance()
                if not success:
                    print(f"[{len(tweets_data)}/{limit}] all instances failed!") if verbose else None
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                tweets = soup.find_all("div", class_="timeline-item")
                if not tweets:
                    print(f"[{len(tweets_data)}/{limit}] no tweets found, retrying...") if verbose else None
                    instance = Tweet.instance()
                    continue

                for tweet in tweets:
                    try:
                        username = tweet.find("a", class_="username").text.strip() if tweet.find("a", class_="username") else "Unknown"
                        name = tweet.find("a", class_="fullname").text.strip() if tweet.find("a", class_="fullname") else username
                        content = tweet.find("div", class_="tweet-content").text.strip() if tweet.find("div", class_="tweet-content") else "No text"
                        hashtags = re.findall(r"#\w+", content) if content else []
                        tweet_link = f"https://twitter.com{tweet.find('a')['href']}" if tweet.find("a") else ""
                        date = tweet.find("span", class_="tweet-date").find("a")["title"] if tweet.find("span", class_="tweet-date") else ""
                        tweet_stats = tweet.find_all("span", class_="tweet-stat")
                        stats = {
                            "comments": int(tweet_stats[0].find("div").text.strip().replace(",", "")) if len(tweet_stats) > 0 and tweet_stats[0].find("div").text.strip().isdigit() else 0,
                            "retweets": int(tweet_stats[1].find("div").text.strip().replace(",", "")) if len(tweet_stats) > 1 and tweet_stats[1].find("div").text.strip().isdigit() else 0,
                            "quotes": int(tweet_stats[2].find("div").text.strip().replace(",", "")) if len(tweet_stats) > 2 and tweet_stats[2].find("div").text.strip().isdigit() else 0,
                            "likes": int(tweet_stats[3].find("div").text.strip().replace(",", "")) if len(tweet_stats) > 3 and tweet_stats[3].find("div").text.strip().isdigit() else 0,
                        }
                        media_section = tweet.find("div", class_="attachments")
                        images, videos, gifs = [], [], []
                        if media_section:
                            images = [ "https://pbs.twimg.com" + unquote(img["src"].split("/pic")[1]).split("?")[0] for img in media_section.find_all("img") ]
                            videos = [ unquote("https" + video["data-url"].split("https")[1]) if "data-url" in video.attrs else unquote(video.find("source")["src"]) for video in media_section.find_all("video", class_="") ]
                            gifs = [ unquote("https://" + gif.source["src"].split("/pic/")[1]) for gif in media_section.find_all("video", class_="gif") ]
                        retweet = tweet.find("div", class_="retweet-header") is not None
                        pinned = tweet.find("div", class_="pinned") is not None
                        replying = [user.text.strip() for user in tweet.find_all("div", class_="replying-to")] if tweet.find("div", class_="replying-to") else []
                        quoted_section = tweet.find("div", class_="quote")
                        quoted = {}
                        if quoted_section:
                            quoted = {
                                "text": quoted_section.find("div", class_="quote-text").text.strip() if quoted_section.find("div", class_="quote-text") else "",
                                "link": f"https://twitter.com{quoted_section.find('a')['href']}" if quoted_section.find("a") else "",
                                "user": quoted_section.find("a", class_="username").text.strip() if quoted_section.find("a", class_="username") else "",
                            }
                        tweets_data.append({
                            "user": {"name": name, "username": username},
                            "text": content,
                            "hashtags": hashtags,
                            "link": tweet_link,
                            "date": date,
                            "stats": stats,
                            "media": {"images": images, "videos": videos, "gifs": gifs},
                            "retweet": retweet,
                            "pinned": pinned,
                            "replying": replying,
                            "quoted": quoted
                        })

                        if len(tweets_data) >= limit: break
                    except Exception as e: print(f"[{len(tweets_data)}/{limit}] {e}")
                page += 1
                sleep(random.uniform(1, 3))
        except KeyboardInterrupt:
                print(f"interrupted, returning collected tweets...")
        return json.dumps(tweets_data, indent=4, ensure_ascii=False)