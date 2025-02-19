# 🐦 Nite Scraping Tool  

Nite is a powerful Python library for scraping tweets from [Nitter](https://github.com/zedeus/nitter), a privacy-friendly Twitter frontend. This tool allows you to extract tweets without requiring API keys or authentication, making it ideal for researchers, analysts, and developers.

## ✨ Features  

- 🔍 **Search tweets** by keyword or hashtag  
- 📅 **Filter by date range** (`since` and `until`)  
- 📍 **Search by location**  
- 🌍 **Filter by language**  
- 📊 **Retrieve tweet stats** (likes, retweets, comments, quotes)  
- 🏎 **Fast & lightweight** — no need for official Twitter API access  
- 🎨 **Customizable output**  

## 📦 Installation  

Before using Nite, ensure you have Python 3.7+ installed.  

1. **Install Nite via pip:**  
   ```bash
   pip install git+https://github.com/xrce/nite.git
   ```
2. **(Optional) Install `termcolor` for colored output:**  
   ```bash
   pip install termcolor
   ```

## 🚀 Usage  

### **Basic Example**  
The script below retrieves tweets based on a search query.  

```python
from nite import Tweet

query = "Python"
tweets = Tweet.posts(query=query, limit=5)

print(tweets)
```

### Advanced Usage

```python
import json
from nite import Tweet

query = "Python"
tweets = Tweet.posts(
    query=query,
    limit=1000,
    since="2024-01-01",
    until="2025-02-02",
    lang="en",
    near="San Francisco"
)

for tweet in json.loads(tweets):
    print("-"*60)
    print(f"\n{tweet['user']['username']} at {tweet['date']} tweeted:")
    print(f"{tweet['link']}")
    print(f"\n{tweet['text']}\n")
    print(f"hashtags: {', '.join(tweet['hashtags'])}") if tweet['hashtags'] else None
    print(f"{tweet['stats']['likes']} likes, {tweet['stats']['retweets']} retweets, {tweet['stats']['quotes']} quotes, {tweet['stats']['comments']} comments\n")
    print("-"*60)
```

### **Command-Line Tool**  
You can use Nite via a Python script for flexible tweet scraping.  

```bash
python -m nite "python" --limit 5 --since 2024-01-01 --until 2024-02-01 --lang en
```

### **Parameters**  
| Argument | Description | Example |
|----------|-------------|---------|
| `query` | Keyword or hashtag to search for | `"python"` |
| `--limit` | Number of tweets to retrieve (default: 10) | `--limit 5` |
| `--since` | Start date (YYYY-MM-DD) | `--since 2024-01-01` |
| `--until` | End date (YYYY-MM-DD) | `--until 2024-02-01` |
| `--near` | Location filter (city, country) | `--near "New York"` |
| `--lang` | Language filter (e.g., en, id, es) | `--lang en` |
| `--verbose` | Enable verbose output | `--verbose` |

## 🎨 Output

### JSON Structure
Here’s an example of a returned json data:  

```json
[
    {
        "user": {
            "username": "elonmusk",
            "name": "Elon Musk"
        },
        "text": "This is a sample tweet from #Tesla and #SpaceX",
        "hashtags": ["Tesla", "SpaceX"],
        "link": "https://twitter.com/elonmusk/status/123456789",
        "date": "2024-02-15T14:32:10Z",
        "stats": {
            "likes": 1000,
            "retweets": 500,
            "quotes": 50,
            "comments": 200
        },
        "media": {
            "images": [
                "https://pbs.twimg.com/media/sampleimage1.jpg",
                "https://pbs.twimg.com/media/sampleimage2.jpg"
            ],
            "videos": [
                "https://pbs.twimg.com/media/samplevideo1.mp4"
            ],
            "gifs": [
                "https://pbs.twimg.com/media/samplegif1.gif"
            ]
        },
        "retweet": false,
        "pinned": false,
        "replying": ["user1", "user2"],
        "quoted": {
            "text": "This is a quoted tweet",
            "link": "https://twitter.com/otheruser/status/987654321",
            "user": "otheruser"
        }
    }
]
```

### Sample Output  
Here’s an example of a formatted tweet output:  

```
--------------------------------------------------
@user123 at 2024-02-10 tweeted:

"Python is amazing! #coding #opensource"

hashtags: coding, opensource
120 likes, 45 retweets, 10 quotes, 15 comments
https://nitter.net/user123/status/1234567890
--------------------------------------------------
```

## 🔥 Why Use Nite Instead of the Twitter API?

| Feature | Nite | Twitter API |
|---------|------|------------|
| API Key Required | ❌ No | ✅ Yes |
| Rate Limits | 🚀 High | ⏳ Strict |
| Fetch Without Login | ✅ Yes | ❌ No |
| Advanced Search Filters | ✅ Yes | ⚠️ Limited |
| Free to Use | ✅ Yes | ❌ No (Limited free tier) | 

## ⚠️ Disclaimer  
This tool is meant for educational and research purposes only. Scraping and using Twitter data must comply with legal and ethical guidelines.  