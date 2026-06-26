# Twitter Dance - 5 分钟快速开始

**自动发推文 Skill（基于 apidance.pro API）**

## 1️⃣ 获取 API Keys

### 第一步：获取 apidance.pro API Key
- 访问：https://t.me/shingle（Telegram）
- 或微信：debuggod
- 购买 API Key（10k 请求 = $8）
- 配置环境变量：
  ```bash
  export APIDANCE_API_KEY="your-api-key-here"
  ```

### 第二步：获取 Twitter AuthToken（可选，发推需要）
- 访问 X.com（Twitter）
- 打开浏览器开发者工具（F12）
- 找到任何 API 请求的 Header → `Authorization: Bearer xxxx`
- 或访问 Settings → Developers → API Keys
- 配置环境变量：
  ```bash
  export TWITTER_AUTH_TOKEN="your-auth-token"
  ```

### 第三步：配置 Kimi API（可选，提高推文质量）
```bash
export KIMI_API_KEY="sk-JM5Ji1efm1IH0iUYAmm3Mn0pWDutMtaHlq5VMKO0taZ4OYW9"
```

## 2️⃣ 快速使用

### 仅生成推文（无需 AuthToken）
```bash
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
node scripts/auto-tweet.js --draft-only
```

### 自动发推
```bash
node scripts/auto-tweet.js
```

### 发 5 条推文
```bash
node scripts/auto-tweet.js --count=5
```

## 3️⃣ 完整工作流

```bash
# 1. 检查 API 配置
echo $APIDANCE_API_KEY
echo $TWITTER_AUTH_TOKEN
echo $KIMI_API_KEY

# 2. 先生成草稿预览（安全）
node scripts/auto-tweet.js --draft-only

# 3. 如果内容满意，发推
node scripts/auto-tweet.js

# 4. 查看日志
cat logs/results-2026-03-11.jsonl
```

## 🎯 功能特性

✅ **AI 推文生成**
- 使用 Kimi API 生成高质量推文
- 本地模板作为备选方案
- 自动话题轮换（每天不同主题）

✅ **批量发推**
- 一次发多条推文
- 自动间隔（避免速率限制）
- 完整日志记录

✅ **成本控制**
- apidance.pro：$8/10k 请求
- Kimi API：可选，按需付费
- 推荐用量：每天 1-5 条推文 = ~$0.01-0.05/天

## 📚 核心 API

### 发推文
```javascript
const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN
});

const result = await client.tweet("推文内容");
// 返回：{ success: true, tweetId: "...", timestamp: "..." }
```

### 生成推文
```javascript
const generator = new TweetGenerator({
  kimiApiKey: process.env.KIMI_API_KEY
});

const tweet = await generator.generate();
// 返回：{ text, source, topic, length, keywords }
```

### 其他操作
```javascript
// 点赞
await client.likeTweet(tweetId);

// 转发
await client.retweet(tweetId);

// 查询推文
await client.getTweet(tweetId);

// 搜索推文
await client.searchTweets("关键词");

// 获取 Timeline
await client.getTimeline({ count: 20 });

// 检查 API 配额
await client.checkQuota();
```

## 🔧 配置文件

### .env（推荐）
```
APIDANCE_API_KEY=your-key-here
TWITTER_AUTH_TOKEN=your-token-here
KIMI_API_KEY=sk-xxx
```

### 环境变量
```bash
export APIDANCE_API_KEY="..."
export TWITTER_AUTH_TOKEN="..."
export KIMI_API_KEY="..."
```

## 📊 日志和结果

发推后，日志保存在 `logs/` 目录：

```
logs/
├── tweets-2026-03-11.jsonl         # 生成的推文草稿
└── results-2026-03-11.jsonl        # 发推结果
```

### 查看结果
```bash
tail -f logs/results-*.jsonl | jq .
```

## ❌ 常见问题

### Q: 缺少 APIDANCE_API_KEY
**A:** 在 https://t.me/shingle 购买 API Key

### Q: 缺少 TWITTER_AUTH_TOKEN
**A:** 仅生成推文时不需要。发推时必须有。[获取步骤](#第二步获取-twitter-authtoken可选发推需要)

### Q: 推文太长（>280 字）
**A:** Kimi 会自动截断。本地模板已验证都 <280 字。

### Q: API 超配额了
**A:** 检查配额：`node -e "const c=require('./src/twitter-api-client'); const cli=new c({apiKey:process.env.APIDANCE_API_KEY}); cli.checkQuota().then(console.log);"`

### Q: 需要自定义推文主题
**A:** 修改 `src/tweet-generator.js` 中的 `topics` 数组

## 📈 成本分析（月度）

假设每天 1 条推文：
- apidance.pro：30 条 × ($8/10k) = ~$0.02/月
- Kimi API：30 次调用 × (~$0.001) = ~$0.03/月
- **总计：~$0.05/月**

## 🚀 下一步

1. ✅ 配置 API Keys
2. ✅ 测试 `--draft-only` 模式
3. ✅ 配置定时任务（Cron）
4. ✅ 监控推文效果

## 📖 详细文档

- [SKILL.md](./SKILL.md) - 完整 API 参考
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - 架构设计（待完成）
- [apidance.pro 文档](https://doc.apidance.pro) - 官方文档

---

**现在就开始使用 Twitter Dance 吧！** 🎭✨
