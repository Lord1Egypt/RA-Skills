# 社交媒体API配置指南

## Twitter API

### API版本对比

| 版本 | 价格 | 限制 | 适用场景 |
|------|------|------|----------|
| Free | $0 | 1,500 tweets/month | 个人测试 |
| Basic | $100/month | 10,000 tweets/month | 小型项目 |
| Pro | $5,000/month | 1,000,000 tweets/month | 商业应用 |
| Enterprise | 定制 | 无限制 | 大型应用 |

### Free版API使用

```python
import tweepy

# 认证
client = tweepy.Client(
    bearer_token="YOUR_BEARER_TOKEN",
    consumer_key="YOUR_API_KEY",
    consumer_secret="YOUR_API_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET"
)

# 搜索推文
response = client.search_recent_tweets(
    query="ETH -is:retweet lang:en",
    max_results=100,
    tweet_fields=["created_at", "public_metrics", "author_id"]
)

for tweet in response.data:
    print(f"{tweet.text} - Likes: {tweet.public_metrics['like_count']}")
```

### 常用查询

```python
# 监控特定代币
query = "ETH OR Ethereum -is:retweet"

# 监控KOL
query = "from:VitalikButerin"

# 监控话题
query = "#Ethereum -is:retweet"

# 过滤垃圾信息
query = "ETH -giveaway -airdrop -is:retweet min_faves:10"
```

## Reddit API

### PRAW配置

```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="SentimentMonitor/1.0"
)

# 获取子版块帖子
subreddit = reddit.subreddit("CryptoCurrency")

for submission in subreddit.new(limit=100):
    print(f"{submission.title} - Score: {submission.score}")
```

### 常用Subreddit

```python
CRYPTO_SUBREDDITS = [
    "CryptoCurrency",      # 综合加密货币
    "Bitcoin",             # 比特币
    "ethereum",            # 以太坊
    "ethfinance",          # 以太坊金融
    "defi",                # DeFi
    "NFTs",                # NFT
    "CryptoMarkets",       # 加密市场
    "SatoshiStreetBets",   # 加密WSB
]
```

## LunarCrush API

### 配置

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://lunarcrush.com/api3"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# 获取代币社交数据
response = requests.get(
    f"{BASE_URL}/coins",
    headers=headers,
    params={"symbol": "ETH"}
)

data = response.json()
print(f"Social Score: {data['data'][0]['social_score']}")
```

### 可用指标

- `social_score` - 社交分数
- `social_volume` - 社交提及量
- `social_engagement` - 社交互动
- `average_sentiment` - 平均情绪
- `bullish_sentiment` - 看涨情绪%
- `bearish_sentiment` - 看跌情绪%

## Santiment API

### GraphQL查询

```python
import requests

API_KEY = "YOUR_API_KEY"
URL = "https://api.santiment.net/graphql"

query = """
{
  getMetric(metric: "social_volume_total") {
    timeseriesData(
      slug: "ethereum"
      from: "2024-01-01T00:00:00Z"
      to: "2024-01-31T00:00:00Z"
      interval: "1d"
    ) {
      datetime
      value
    }
  }
}
"""

response = requests.post(
    URL,
    headers={"Authorization": f"Apikey {API_KEY}"},
    json={"query": query}
)
```

## 环境变量配置

### .env文件

```bash
# Twitter
TWITTER_BEARER_TOKEN=xxx
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_TOKEN_SECRET=xxx

# Reddit
REDDIT_CLIENT_ID=xxx
REDDIT_CLIENT_SECRET=xxx

# LunarCrush
LUNARCRUSH_API_KEY=xxx

# Santiment
SANTIMENT_API_KEY=xxx

# 通知
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
DISCORD_WEBHOOK_URL=xxx
```

### Python读取

```python
from dotenv import load_dotenv
import os

load_dotenv()

# Twitter配置
twitter_config = {
    "bearer_token": os.getenv("TWITTER_BEARER_TOKEN"),
    "consumer_key": os.getenv("TWITTER_API_KEY"),
    "consumer_secret": os.getenv("TWITTER_API_SECRET"),
}
```

## 免费替代方案

### Nitter (Twitter镜像)
```python
# 无需API key，但稳定性差
import requests
from bs4 import BeautifulSoup

def get_tweets_nitter(username):
    url = f"https://nitter.net/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # 解析推文...
```

### 注意
- 免费方案可能有稳定性问题
- 频繁请求可能被封IP
- 建议使用代理池

---

*API选择要根据预算和数据需求平衡。*
