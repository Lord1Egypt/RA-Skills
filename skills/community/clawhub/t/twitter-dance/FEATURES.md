# Twitter Dance - 完整功能清单

**自动发推文 Skill（基于 apidance.pro API）**

## 🎯 核心功能

### 1. 推文发布 ✅

#### 自动发推
```bash
# 发 1 条推文（默认）
node scripts/auto-tweet.js

# 发 5 条推文
node scripts/auto-tweet.js --count=5

# 仅生成草稿（不发推）
node scripts/auto-tweet.js --draft-only
```

**特性：**
- 使用 Kimi API 生成高质量推文
- 本地模板自动回退（Kimi 失败时）
- 自动话题轮换（每天不同话题）
- 完整日志记录（logs/目录）
- 自动间隔（避免 API 限制）

---

### 2. API 配额管理 ✅

#### 检查 API 配额
```bash
# 单次检查
node scripts/check-quota.js

# 监控模式（每 5 秒刷新一次）
node scripts/check-quota.js --watch

# JSON 输出格式
node scripts/check-quota.js --json
```

**显示信息：**
- 总配额数
- 已使用次数
- 剩余次数
- 使用百分比（进度条）
- 预测剩余天数
- 实时警告

---

### 3. 账户管理 ✅

#### 获取我的账户信息
```bash
node scripts/get-my-info.js
```

**显示内容：**
- 用户名、昵称、ID
- 粉丝数、关注数、推文数
- 账户简介
- 自动保存到文件

#### 获取我的推文列表
```bash
# 最近 20 条推文
node scripts/list-my-tweets.js

# 最近 50 条推文
node scripts/list-my-tweets.js --count=50

# 排除转发
node scripts/list-my-tweets.js --no-rt

# 排除回复
node scripts/list-my-tweets.js --no-replies
```

**显示内容：**
- 推文内容、ID、时间戳
- 点赞数、转发数、回复数
- 自动保存为 JSONL 文件

---

### 4. 推文交互 ✅

#### 点赞推文
```bash
node scripts/interact.js --like=1234567890
```

#### 转发推文
```bash
node scripts/interact.js --retweet=1234567890
```

#### 回复推文
```bash
node scripts/interact.js --reply=1234567890 --text="很赞！"
```

#### 获取推文详情
```bash
node scripts/interact.js --get=1234567890
```

#### 删除我的推文
```bash
node scripts/interact.js --delete=1234567890
```

---

### 5. 关注管理 ✅

#### 关注用户
```bash
node scripts/follow.js --follow=123456789
```

#### 取消关注
```bash
node scripts/follow.js --unfollow=123456789
```

#### 获取粉丝列表
```bash
# 获取最近 20 个粉丝
node scripts/follow.js --followers

# 获取最近 100 个粉丝
node scripts/follow.js --followers --count=100
```

#### 获取关注列表
```bash
# 获取最近 20 个关注
node scripts/follow.js --following

# 获取最近 100 个关注
node scripts/follow.js --following --count=100
```

---

### 6. 搜索和发现 ✅

#### 搜索推文（API 客户端可用）
```javascript
const client = new TwitterDanceAPIClient();
const results = await client.searchTweets("Bitcoin", { 
  count: 20,
  lang: 'en'
});
```

#### 获取 Timeline（API 客户端可用）
```javascript
const timeline = await client.getTimeline({
  count: 20,
  excludeReplies: false,
  includeRetweets: true
});
```

#### 查询用户信息（API 客户端可用）
```javascript
const user = await client.getUser("elonmusk");
```

---

## 🛠️ 配置指南

### 环境变量（.env）

```bash
# 必需
APIDANCE_API_KEY=your-api-key-here
TWITTER_AUTH_TOKEN=your-auth-token

# 可选但推荐
KIMI_API_KEY=sk-xxx

# 调试选项
VERBOSE=true
LOG_DIR=logs
```

### 如何获取 API Key

#### apidance.pro API Key
1. 访问 https://t.me/shingle（Telegram）
2. 或微信联系 debuggod
3. 购买 API Key（$8 per 10k requests）

#### Twitter AuthToken
1. 访问 https://x.com
2. 打开浏览器开发者工具（F12）
3. 找任何 API 请求的 `Authorization` Header
4. 复制 Bearer 后面的那一长串

#### Kimi API Key
1. 访问 https://platform.moonshot.cn
2. 获取 API Key
3. 按需付费（约 $0.001 per request）

---

## 📊 成本分析

### 按使用量计算（每月）

| 项目 | 用量 | 单价 | 总价 |
|------|------|------|------|
| apidance API | 30 条推文 | $0.008/条 | $0.24 |
| Kimi API | 30 次生成 | ~$0.001/次 | $0.03 |
| **总计** | - | - | **~$0.27/月** |

### 与竞品对比

| 工具 | 月费 | 特性 |
|------|------|------|
| Buffer | $15+ | Twitter + Facebook + LinkedIn |
| Zapier | $15+ | 自动化工作流 |
| Make | $10+ | 更强大的自动化 |
| **Twitter Dance** | **$0.27** | **专门为 Twitter 优化** |

**节省对比：** 比 Buffer 便宜 **99%** ✨

---

## 🚀 快速开始（5分钟）

### 第 1 步：配置 API Keys
```bash
export APIDANCE_API_KEY="your-api-key"
export TWITTER_AUTH_TOKEN="your-auth-token"
export KIMI_API_KEY="sk-xxx"
```

### 第 2 步：生成推文草稿（预览）
```bash
node scripts/auto-tweet.js --draft-only
```

### 第 3 步：检查 API 配额
```bash
node scripts/check-quota.js
```

### 第 4 步：正式发推
```bash
node scripts/auto-tweet.js
```

### 第 5 步：获取账户信息（验证）
```bash
node scripts/get-my-info.js
```

---

## 📅 定时任务（Cron）

### 每天自动发推（09:00）

#### 使用 Cron
```bash
0 9 * * * cd /path/to/twitter-dance && node scripts/auto-tweet.js >> logs/cron.log 2>&1
```

#### 使用 OpenClaw
```bash
openclaw cron add \
  --schedule "0 9 * * *" \
  --task "cd /Users/chao/.openclaw/workspace/skills/twitter-dance && node scripts/auto-tweet.js"
```

---

## 📁 文件结构

```
twitter-dance/
├── src/
│   ├── twitter-api-client.js      # API 客户端（核心）
│   └── tweet-generator.js          # 推文生成器
├── scripts/
│   ├── auto-tweet.js               # 自动发推（主脚本）
│   ├── check-quota.js              # 检查配额
│   ├── get-my-info.js              # 获取账户信息
│   ├── list-my-tweets.js           # 列出推文
│   ├── interact.js                 # 推文交互
│   └── follow.js                   # 关注管理
├── .env                            # 环境变量（勿提交）
├── .env.example                    # 示例配置
├── package.json                    # 依赖配置
├── QUICK_START.md                  # 快速开始
├── SKILL.md                        # API 文档
├── FEATURES.md                     # 本文件
└── logs/                           # 日志输出目录
```

---

## 🔧 API 客户端直接使用

### 初始化
```javascript
const TwitterDanceAPIClient = require('./src/twitter-api-client');

const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN,
  verbose: true
});
```

### 可用方法

#### 推文操作
- `tweet(text, options)` - 发推文
- `replyTweet(tweetId, text)` - 回复推文
- `deleteTweet(tweetId)` - 删除推文
- `getTweet(tweetId)` - 获取推文详情
- `getMyTweets(options)` - 获取我的推文列表

#### 交互操作
- `likeTweet(tweetId)` - 点赞
- `retweet(tweetId)` - 转发
- `getReplies(tweetId, options)` - 获取回复

#### 用户操作
- `getUser(username)` - 查询用户信息
- `getMyInfo()` - 获取我的账户信息
- `followUser(userId)` - 关注用户
- `unfollowUser(userId)` - 取消关注
- `getFollowers(options)` - 获取粉丝列表
- `getFollowing(options)` - 获取关注列表

#### 搜索和发现
- `searchTweets(query, options)` - 搜索推文
- `getTimeline(options)` - 获取 Timeline

#### 配额管理
- `checkQuota()` - 检查 API 配额

---

## ❓ 常见问题

### Q: 推文生成超过 280 字符怎么办？
**A:** 系统会自动截断。Kimi API 也会确保输出 ≤280 字。

### Q: 没有 Kimi API Key 可以使用吗？
**A:** 完全可以。系统会自动回退到本地模板生成推文（质量略低但仍可用）。

### Q: API Key 配额用完了怎么办？
**A:** 
1. 使用 `check-quota.js` 查看剩余配额
2. 在 https://t.me/shingle 购买更多

### Q: AuthToken 过期了怎么办？
**A:** 重新从 X.com 获取（步骤见上文）

### Q: 支持图片上传吗？
**A:** 暂未实现（v1.1 版本）。后续版本将支持。

### Q: 可以定时发推吗？
**A:** 完全支持！使用 Cron 或 OpenClaw 的定时功能。

---

## 🔒 安全建议

✅ **推荐做法**
- 不要提交 `.env` 文件到 Git
- 定期更新 AuthToken
- 监控 API 配额
- 使用 `--draft-only` 预览推文

❌ **不推荐**
- 一次发超过 20 条推文
- 完全无审核的自动化
- 共享 API Key

---

## 📞 支持和反馈

- **apidance.pro 支持:** https://t.me/shingle
- **GitHub Issues:** (待补充)
- **文档:** QUICK_START.md | SKILL.md | README.md

---

## 📄 许可证

MIT

---

**最后更新：2026-03-11**
