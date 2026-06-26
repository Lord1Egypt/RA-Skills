# Phase 2: 数据分析参考

从 x_profile_analyzer.py 输出的 JSON 中提取关键统计：

```python
import json

with open('/tmp/x-profile-raw-{handle}.json') as f:
    d = json.load(f)

p = d['profile']
ts = d['tweet_stats']
tweets = d['tweets']
followings = d['followings']

# 基本信息
print(f"{p['name']} (@{p['username']})")
print(f"Followers: {p['followers_count']} | Following: {p['following_count']}")
print(f"Tweets: {ts['total_fetched']} fetched | avg {ts['avg_likes']}❤️ | {ts['tweets_per_day']}/day")

# 按 likes 排序
tweets_sorted = sorted(tweets, key=lambda t: t['likes'], reverse=True)

# 推文长度分布
long = len([t for t in tweets if len(t['text']) > 2000])
mid = len([t for t in tweets if 500 < len(t['text']) <= 2000])
short = len([t for t in tweets if len(t['text']) <= 500])

# 类型分布
originals = len([t for t in tweets if not t['is_retweet'] and not t['is_reply']])
replies = len([t for t in tweets if t['is_reply']])
retweets = len([t for t in tweets if t['is_retweet']])
quotes = len([t for t in tweets if t['is_quote']])

# 含链接/媒体
with_links = len([t for t in tweets if t.get('urls')])
with_media = len([t for t in tweets if t.get('has_media')])
```

## 动态分类建议流程

1. 先打印所有推文的前 100 字 + likes 数，快速浏览主题
2. 根据关键词和内容相似性，提出 3-6 个分类
3. 每个分类起一个中文名 + 英文 slug（用作文件名）
4. 将推文 ID 分配到各分类
5. 一条推文只进一个分类（选最匹配的）

注意：分类要反映此博主的独特性，不要套用通用模板。例如：
- @karpathy → "nanochat 与模型训练" 是他独有的
- @Saboo_Shubham_ → "OpenClaw Agent 运营实战" 是他独有的
- 通用的"行业洞察"类别可以保留，但要有具体内容支撑
