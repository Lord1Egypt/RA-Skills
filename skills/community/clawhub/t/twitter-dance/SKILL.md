# Twitter Dance - Skill 定义

**自动发推文 Skill（基于 apidance.pro API）**

## 基本信息

- **名称**：twitter-dance
- **版本**：1.0.0
- **类型**：社媒运营自动化
- **推荐用途**：日常推文发布、内容分发
- **最佳实践**：与 Kimi AI 结合使用

## 简介

Twitter Dance 是一个完全自动化的推特发布和管理系统，基于 apidance.pro 官方 API。

**核心特性：**
- 🤖 AI 推文生成（Kimi）
- ⚡ 完全自动化发推
- 💰 超低成本（$0.05/月）
- 📊 完整日志和统计
- 🔒 安全可靠（无浏览器自动化）
- 📱 账户统计和分析
- 🔔 通知管理
- 💬 自动回复
- 📈 互动数据分析
- ⏰ 互动周期优化

## 安装

```bash
# 1. 获取 API Key
# apidance.pro: https://t.me/shingle
# TWITTER_AUTH_TOKEN: X.com Settings → Developers
# KIMI_API_KEY: https://platform.moonshot.cn

# 2. 配置环境变量
export APIDANCE_API_KEY="..."
export TWITTER_AUTH_TOKEN="..."
export KIMI_API_KEY="..."

# 3. 进入 Skill 目录
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
```

## 快速开始

### 生成推文（无需发布）
```bash
node scripts/auto-tweet.js --draft-only
```

### 自动发推
```bash
node scripts/auto-tweet.js
```

### 批量发推
```bash
node scripts/auto-tweet.js --count=5
```

### 测试 GraphQL API
```bash
node scripts/test-tweet-graphql.js "你的推文内容"
```

## 高级功能

使用 `TwitterDanceEnhanced` 类获得更多强大功能：

### 账户统计
```bash
node scripts/test-advanced-features.js stats
```
获取粉丝数、推文数、点赞数等详细统计

### 通知管理
```bash
node scripts/test-advanced-features.js notifications
```
获取最新的互动通知（提及、点赞、转发）

### 自动回复
```bash
node scripts/test-advanced-features.js reply <tweetId> <replyText>
```
自动回复特定推文

### 推文分析
```bash
node scripts/test-advanced-features.js timeline-analytics
```
分析时间线，找出最受欢迎的推文

### 互动周期分析
```bash
node scripts/test-advanced-features.js engagement-hours
```
找出最佳发推时间

### 完整功能菜单
```bash
node scripts/test-advanced-features.js
```

**详见：** [ADVANCED_FEATURES.md](./ADVANCED_FEATURES.md)

## API 参考

### TwitterDanceAPIClient

#### 初始化
```javascript
const TwitterDanceAPIClient = require('./src/twitter-api-client');

const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN,
  verbose: true
});
```

#### 方法

##### tweet(text, options)
发布推文

**参数：**
- `text` (string): 推文内容（≤280 字）
- `options` (object):
  - `media` (array): 媒体 URL 列表（可选）

**返回：**
```javascript
{
  success: true,
  tweetId: "1234567890",
  timestamp: "2026-03-11T13:27:00Z",
  text: "推文内容",
  length: 150
}
```

**示例：**
```javascript
const result = await client.tweet("Hello Twitter! 🚀");
console.log(result.tweetId);
```

##### likeTweet(tweetId)
点赞推文

**参数：**
- `tweetId` (string): 推文 ID

**示例：**
```javascript
await client.likeTweet("1234567890");
```

##### retweet(tweetId)
转发推文

**示例：**
```javascript
await client.retweet("1234567890");
```

##### getTweet(tweetId)
查询推文详情

**返回：**
```javascript
{
  success: true,
  tweet: { /* 推文数据 */ }
}
```

##### getUser(username)
查询用户信息

**示例：**
```javascript
const user = await client.getUser("elonmusk");
console.log(user.followers_count);
```

##### searchTweets(query, options)
搜索推文

**参数：**
- `query` (string): 搜索关键词
- `options` (object):
  - `count` (number): 返回数量，默认 10
  - `lang` (string): 语言代码，默认 'en'

**示例：**
```javascript
const results = await client.searchTweets("OpenClaw", { count: 20 });
```

##### getTimeline(options)
获取 Timeline

**参数：**
- `options` (object):
  - `count` (number): 推文数量，默认 20
  - `excludeReplies` (boolean): 排除回复
  - `includeRetweets` (boolean): 包含转发，默认 true

##### checkQuota()
检查 API 配额

**返回：**
```javascript
{
  success: true,
  remaining: 9500,
  total: 10000,
  used: 500
}
```

### TweetGenerator

#### 初始化
```javascript
const TweetGenerator = require('./src/tweet-generator');

const generator = new TweetGenerator({
  kimiApiKey: process.env.KIMI_API_KEY,
  verbose: true
});
```

#### 方法

##### generate(options)
生成单条推文

**参数：**
- `options` (object):
  - `topic` (object): 自定义话题（可选）

**返回：**
```javascript
{
  text: "推文内容...",
  source: "kimi" | "template",
  topic: "Crypto & Web3",
  length: 180,
  keywords: ["Bitcoin", "Ethereum"]
}
```

**示例：**
```javascript
const tweet = await generator.generate();
console.log(tweet.text);
```

##### generateBatch(count, options)
批量生成推文

**示例：**
```javascript
const tweets = await generator.generateBatch(5);
tweets.forEach((t, i) => {
  console.log(`${i + 1}. ${t.text}`);
});
```

## 工作流示例

### 场景 1：日常自动发推

```bash
# 设置 Cron 任务
0 9 * * * cd /path/to/twitter-dance && node scripts/auto-tweet.js >> logs/cron.log 2>&1
```

### 场景 2：批量发推（一次 5 条）

```bash
node scripts/auto-tweet.js --count=5
```

### 场景 3：仅生成草稿供审核

```bash
node scripts/auto-tweet.js --draft-only > tweets-to-review.txt
```

## 配置

### 环境变量

```bash
# 必需
APIDANCE_API_KEY=your-api-key
TWITTER_AUTH_TOKEN=your-token

# 可选（推荐）
KIMI_API_KEY=sk-xxx

# 日志
VERBOSE=true  # 详细日志
```

### 推文主题（自定义）

编辑 `src/tweet-generator.js` 中的 `topics` 数组：

```javascript
this.topics = [
  {
    name: 'Your Topic',
    keywords: ['keyword1', 'keyword2'],
    tone: 'Your tone'
  },
  // ...
];
```

## 成本分析

### 每月费用（基于 30 条推文）

| 项目 | 用量 | 单价 | 总价 |
|------|------|------|------|
| apidance.pro API | 30 条 | $0.008/条 | $0.24 |
| Kimi API（可选） | 30 条 | ~$0.001/条 | $0.03 |
| **总计** | **30 条** | - | **~$0.27** |

### 与竞品对比

- Zapier 推特集成：$15-25/月
- Make 推特场景：$10-20/月
- Buffer Pro：$15+/月
- **Twitter Dance：$0.27/月（节省 99%）**

## 故障排除

### 错误：缺少 APIDANCE_API_KEY
**解决：** 在 https://t.me/shingle 购买 API Key

### 错误：缺少 TWITTER_AUTH_TOKEN
**解决：** 从 X.com Settings → Developers 获取 Token

### 错误：推文过长
**解决：** Kimi 会自动截断；本地模板已验证都 <280 字

### 错误：API 配额已用尽
**解决：** 查看配额 → 购买更多或等待重置

## 最佳实践

✅ **推荐**
- 结合 Kimi API 提高推文质量
- 使用 `--draft-only` 先预览
- 定期检查日志分析效果
- 每天 1-3 条推文（高效且经济）

❌ **不推荐**
- 一次发超过 10 条推文
- 禁用 Kimi 使用纯模板
- 完全无人审核的完全自动化

### TwitterDanceEnhanced（高级 API）

#### 初始化
```javascript
const TwitterDanceEnhanced = require('./src/twitter-api-enhanced');

const client = new TwitterDanceEnhanced({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN,
  verbose: true
});
```

#### 核心方法

| 方法 | 功能 | 返回 |
|------|------|------|
| `getAccountStats()` | 获取账户统计 | 粉丝、推文、点赞等数据 |
| `getNotifications(options)` | 获取通知 | 最新互动列表 |
| `autoReply(tweetId, text, options)` | 自动回复 | 回复成功信息 |
| `getTweetMetrics(tweetId)` | 获取推文指标 | 点赞、转发、浏览数 |
| `getTimelineAnalytics(options)` | 时间线分析 | 推文统计和最佳推文 |
| `getEngagementByHour()` | 互动周期分析 | 每小时的互动数据 |
| `bulkLikeTweets(tweetIds)` | 批量点赞 | 操作结果 |
| `bulkRetweet(tweetIds)` | 批量转发 | 操作结果 |
| `getConversationThread(tweetId)` | 获取对话线程 | 推文及其回复 |

#### 使用示例

```javascript
// 获取账户统计
const stats = await client.getAccountStats();
console.log(`粉丝: ${stats.stats.followers}`);

// 自动回复
await client.autoReply('123456', '感谢评论！');

// 分析最佳发推时间
const best = await client.getEngagementByHour();
console.log(`最佳时间: ${best.bestHour}:00 UTC`);

// 批量点赞
await client.bulkLikeTweets(['123', '456', '789']);
```

## 🤖 自动回复评论功能

### 快速回复特定推文

```bash
# 查看将要回复的内容（模拟模式）
node scripts/quick-reply.js --tweet-id=2031936903918883025 --replies=10 --dry-run

# 实际发送回复
node scripts/quick-reply.js --tweet-id=2031936903918883025 --replies=10
```

**功能特性**:
- ✅ **AI 智能回复** - 根据评论内容自动选择合适的回复模板
- ✅ **模拟模式** - 使用 `--dry-run` 预览回复内容
- ✅ **速率限制保护** - 自动延迟避免 Twitter 限流
- ✅ **批量处理** - 一次处理多条评论

**命令行选项**:
| 选项 | 说明 | 例子 |
|------|------|------|
| `--tweet-id=<ID>` | 推文 ID（必需） | `--tweet-id=2031936903918883025` |
| `--replies=N` | 获取最多 N 条评论 | `--replies=5` |
| `--dry-run` | 模拟模式，不实际发送 | `--dry-run` |
| `--no-reply` | 仅显示评论，不回复 | `--no-reply` |

### 自动回复最近推文

```bash
# 获取最近 3 条推文，模拟回复它们的评论
node scripts/auto-reply-comments.js --tweets=3 --replies=10 --dry-run

# 实际回复
node scripts/auto-reply-comments.js --tweets=3 --replies=10
```

### 如何获取推文 ID

推文 URL 格式: `https://twitter.com/username/status/<推文ID>`

例如: `https://twitter.com/elonmusk/status/1234567890123456789`
- 推文 ID = `1234567890123456789`

### AI 回复匹配示例

| 评论类型 | 评论例子 | 自动回复 |
|---------|---------|--------|
| 感谢 | "谢谢你的分享！" | "感谢你的反馈！😊" |
| 询问 | "这怎么用？" | "很好的问题，让我们继续讨论！" |
| 同意 | "我也这样认为" | "完全同意！👏" |
| 鼓励 | "继续加油！" | "继续加油！🚀" |

### 详细使用指南

👉 参考 **[AUTO-REPLY-GUIDE.md](./AUTO-REPLY-GUIDE.md)** 获取完整说明

## 相关文档

- [AUTO-REPLY-GUIDE.md](./AUTO-REPLY-GUIDE.md) - 自动回复详细指南 ⭐️
- [ADVANCED_FEATURES.md](./ADVANCED_FEATURES.md) - 高级功能详解 ⭐️
- [GRAPHQL_API_GUIDE.md](./GRAPHQL_API_GUIDE.md) - GraphQL API 参考
- [QUICK_START.md](./QUICK_START.md) - 5 分钟快速开始
- [README.md](./README.md) - 项目概览
- [apidance.pro 文档](https://doc.apidance.pro) - 官方 API 文档

## 许可证

MIT

---

**版本更新日志：**

### v1.0.0（2026-03-11）
- ✅ 初始版本发布
- ✅ apidance.pro API 集成
- ✅ Kimi AI 推文生成
- ✅ 批量发推支持
- ✅ 完整日志和统计

### 规划中（v1.1.0+）
- 📷 媒体上传支持（图片、视频）
- 📊 推文效果分析仪表板
- 🎯 情绪分析和自动语气调整
- 🔄 高级定时和队列管理

