import argparse, json
from .nite import Tweet
from termcolor import colored

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nitter scraping tool")
    parser.add_argument("query", type=str, help="Keyword or hashtag to search for")
    parser.add_argument("--limit", type=int, default=10, help="Number of tweets to retrieve (default: 10)")
    parser.add_argument("--since", type=str, default=None, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--until", type=str, default=None, help="End date (YYYY-MM-DD)")
    parser.add_argument("--near", type=str, default=None, help="Location filter (e.g., Jakarta)")
    parser.add_argument("--lang", type=str, default=None, help="Language filter (e.g., en, id, es)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    print(f"\nSearching for {colored(args.query,'light_yellow')}...")

    tweets = Tweet.posts(
        query=args.query,
        limit=args.limit,
        since=args.since,
        until=args.until,
        near=args.near,
        lang=args.lang,
        verbose=args.verbose
    )

    tweets = json.loads(tweets)
    if tweets: print(f"{colored(len(tweets),'light_green')} tweets found!\n")
    for tweet in tweets:
        print("-"*60)
        print(f"\n{colored(tweet['user']['username'],'light_cyan')} at {colored(tweet['date'],'light_grey')} tweeted:")
        print(f"{colored(tweet['link'],'light_yellow')}")
        print(f"\n{tweet['text']}\n")
        print(f"hashtags: {colored(', '.join(tweet['hashtags']),'light_yellow')}") if tweet['hashtags'] else None
        print(f"{colored(tweet['stats']['likes'],'light_cyan')} likes, {colored(tweet['stats']['retweets'],'light_blue')} retweets, {colored(tweet['stats']['quotes'],'light_green')} quotes, {colored(tweet['stats']['comments'],'light_magenta')} comments\n")
        print("-"*60)