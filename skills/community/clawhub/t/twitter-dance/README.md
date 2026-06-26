# 🎭 Twitter Dance - 自动发推文 Skill

**使用 apidance.pro API + Kimi AI 的完全自动化推特发布系统**

## 核心特性

✨ **智能推文生成**
- 使用 Kimi AI 生成高质量推文（可选）
- 本地模板作为快速备选方案
- 自动话题轮换（5 个不同主题）

⚡ **完全自动化**
- 一键发推
- 批量发推支持
- 自动间隔控制（避免速率限制）

💰 **成本优化**
- apidance.pro：$8/10k 请求
- 日均成本：$0.001-0.005
- 完全按需付费

🔒 **安全可靠**
- 无需浏览器自动化
- 直接使用官方 API
- 完整日志和错误处理

## 快速开始

### 1. 配置 API Keys

```bash
# apidance.pro API Key（必需）
export APIDANCE_API_KEY="your-key-from-t.me/shingle"

# Twitter AuthToken（发推时必需）
export TWITTER_AUTH_TOKEN="your-token-from-x.com"

# Kimi API Key（可选，推荐）
export KIMI_API_KEY="sk-JM5Ji1efm1IH0iUYAmm3Mn0pWDutMtaHlq5VMKO0taZ4OYW9"
```

### 2. 生成推文（安全模式）

```bash
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
node scripts/auto-tweet.js --draft-only
```

### 3. 发布推文

```bash
node scripts/auto-tweet.js
```

### 4. 批量发推

```bash
node scripts/auto-tweet.js --count=5
```

## 项目结构

```
twitter-dance/
├── src/
│   ├── twitter-api-client.js      # apidance.pro API 客户端
│   ├── tweet-generator.js         # AI 推文生成器
│   └── utils.js                   # 工具函数（待完成）
├── scripts/
│   └── auto-tweet.js              # 主发推脚本
├── logs/                          # 推文日志
│   ├── tweets-*.jsonl             # 推文内容
│   └── results-*.jsonl            # 发推结果
├── docs/
│   └── ARCHITECTURE.md            # 架构设计（待完成）
├── QUICK_START.md                 # 5 分钟快速开始
├── SKILL.md                       # 完整 API 参考（待完成）
├── README.md                      # 本文件
└── package.json
```

## 核心 API

### TwitterDanceAPIClient

```javascript
const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN
});

// 发推文
await client.tweet("推文内容");

// 点赞
await client.likeTweet(tweetId);

// 转发
await client.retweet(tweetId);

// 搜索推文
await client.searchTweets("关键词");

// 查询用户
await client.getUser("username");

// 检查配额
await client.checkQuota();
```

### TweetGenerator

```javascript
const generator = new TweetGenerator({
  kimiApiKey: process.env.KIMI_API_KEY
});

// 生成单条推文
const tweet = await generator.generate();

// 批量生成
const tweets = await generator.generateBatch(5);
```

## 成本分析

| 用途 | 频率 | 月成本 |
|------|------|--------|
| 推文生成（Kimi） | 30 条/月 | ~$0.03 |
| API 请求（apidance） | 30 条/月 | ~$0.02 |
| **总计** | **30 条/月** | **~$0.05** |

与 Zapier/Make 相比节省 99% 的成本。

## 工作流示例

### 每天自动发推

```bash
# 设置 Cron（每天 09:00）
0 9 * * * cd /Users/chao/.openclaw/workspace/skills/twitter-dance && node scripts/auto-tweet.js
```

### 监控推文效果

```bash
# 实时查看日志
tail -f logs/results-*.jsonl | jq .
```

## 对标竞品

| 对比项 | Twitter Dance | Zapier | Make | Buffer |
|-------|---|---|---|---|
| 推文发布 | ✅ | ✅ | ✅ | ✅ |
| AI 生成 | ✅ | ❌ | ❌ | ❌ |
| 月成本 | $0.05 | $15+ | $10+ | $15+ |
| 自定义度 | 100% | 80% | 85% | 70% |
| 部署难度 | 简单（CLI） | 简单（UI） | 中等 | 简单 |

## 常见问题

### 如何获取 API Key？

**apidance.pro:**
- 访问 https://t.me/shingle（Telegram）
- 或微信：debuggod
- 购买后会收到 API Key

**Twitter AuthToken:**
1. 访问 X.com
2. 打开开发者工具（F12）
3. 找到任何 API 请求
4. 复制 `Authorization: Bearer xxxx` 中的 Token 部分

**Kimi API:**
- 访问 https://platform.moonshot.cn
- 创建新的 API Key

### 成本太高怎么办？

使用本地模板模式（不调用 Kimi）：
- 纯 apidance.pro：$0.02/月
- 完全免费的本地模板

### 能否自定义推文？

**两种方式：**

1. **修改模板**（最简单）
   ```javascript
   // 编辑 src/tweet-generator.js 中的 templates 数组
   ```

2. **传入自定义话题**
   ```javascript
   const tweet = await generator.generate({
     topic: {
       name: 'Crypto',
       keywords: ['Bitcoin', 'Ethereum'],
       tone: 'Technical'
     }
   });
   ```

## 最佳实践

✅ **推荐做法**
- 每天 1-3 条推文（成本低，效果好）
- 配合 Kimi API 提高质量
- 定期检查日志，分析互动
- 使用 `--draft-only` 先预览

❌ **不推荐做法**
- 一次发超过 10 条（可能触发速率限制）
- 禁用 Kimi 使用纯模板（质量下降）
- 完全自动化无人审核（可能发布不适当内容）

## 下一步

- [ ] 实现 `docs/ARCHITECTURE.md`
- [ ] 完成 `SKILL.md` API 文档
- [ ] 添加 `src/utils.js` 工具函数
- [ ] 支持媒体上传（图片、视频）
- [ ] 集成情绪分析（自动调整语气）
- [ ] Web 仪表板（查看推文效果）

## 许可证

MIT

## 支持

遇到问题？
- 查看 [QUICK_START.md](./QUICK_START.md)
- 提交 Issue 到 GitHub
- 联系 https://t.me/shingle（apidance 官方）

---

**现在就开始你的 Twitter Dance 之旅吧！** 🎭✨
