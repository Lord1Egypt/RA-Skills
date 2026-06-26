# Twitter Dance - GraphQL API 集成指南

> 基于 apidance.pro 的官方 GraphQL API
> 
> 最后更新：2026-03-12

## 快速开始

### 1. 安装依赖

```bash
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
npm install
```

### 2. 配置环境变量

```bash
# .env 文件
APIDANCE_API_KEY=your-api-key
TWITTER_AUTH_TOKEN=your-auth-token
KIMI_API_KEY=sk-xxx  # 可选
VERBOSE=true
```

### 3. 测试 GraphQL API

```bash
# 发送简单推文
node scripts/test-tweet-graphql.js "Hello Twitter!"

# 使用自动生成的推文发推
node scripts/auto-tweet.js

# 仅查看草稿
node scripts/auto-tweet.js --draft-only
```

---

## API 端点

### CreateTweet - 创建/发布推文

**URL**
```
POST https://api.apidance.pro/graphql/CreateTweet
```

**请求头（Required）**
```
Authtoken: <your-twitter-auth-token>
apikey: <your-apidance-api-key>
User-Agent: Apidog/1.0.0 (https://apidog.com)
Content-Type: application/json
Accept: */*
Host: api.apidance.pro
Connection: keep-alive
```

**请求体格式**

```json
{
  "variables": {
    "tweet_text": "推文内容，最多 280 字",
    "dark_request": false,
    "reply": {
      "in_reply_to_tweet_id": null,
      "exclude_reply_user_ids": []
    },
    "media": {
      "media_entities": [],
      "possibly_sensitive": false
    },
    "semantic_annotation_ids": [],
    "includePromotedContent": false
  }
}
```

**参数说明**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `tweet_text` | string | ✅ | 推文内容（1-280 字） |
| `dark_request` | boolean | ✅ | 暗主题模式（通常为 false） |
| `reply.in_reply_to_tweet_id` | string\|null | ❌ | 被回复推文的 ID（可选，null 表示不回复） |
| `reply.exclude_reply_user_ids` | array | ✅ | 排除的用户 ID 列表（通常为空） |
| `media.media_entities` | array | ❌ | 媒体对象数组（可选） |
| `media.possibly_sensitive` | boolean | ✅ | 标记为敏感内容（通常为 false） |
| `semantic_annotation_ids` | array | ✅ | 语义注释 ID（通常为空） |
| `includePromotedContent` | boolean | ✅ | 包含推广内容（通常为 false） |

**成功响应示例**

```json
{
  "data": {
    "create_tweet": {
      "tweet_results": {
        "result": {
          "rest_id": "1768234567890123456",
          "core": {
            "user_results": {
              "result": {
                "id": "VXNlcjoxMjM0NTY3ODk=",
                "rest_id": "123456789",
                "legacy": {
                  "name": "Your Name",
                  "screen_name": "yourhandle",
                  "description": "Your bio"
                }
              }
            }
          },
          "legacy": {
            "created_at": "Wed Mar 12 10:05:00 +0000 2026",
            "text": "推文内容...",
            "favorite_count": 0,
            "retweet_count": 0
          }
        }
      }
    }
  }
}
```

**错误响应示例**

```json
{
  "errors": [
    {
      "message": "Invalid token",
      "code": 401,
      "details": "The provided authtoken is invalid or expired"
    }
  ]
}
```

---

## 使用示例

### JavaScript / Node.js

#### 方式 1：使用 TwitterDanceAPIClient

```javascript
const TwitterDanceAPIClient = require('./src/twitter-api-client');

const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN,
  verbose: true  // 显示详细日志
});

// 发送简单推文
const result = await client.tweet('Hello Twitter! 🚀');
console.log('推文 ID:', result.tweetId);
```

#### 方式 2：直接使用 graphqlRequest（低级 API）

```javascript
const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN
});

// 直接调用 GraphQL
const variables = {
  tweet_text: '我的推文内容',
  dark_request: false,
  reply: { in_reply_to_tweet_id: null, exclude_reply_user_ids: [] },
  media: { media_entities: [], possibly_sensitive: false },
  semantic_annotation_ids: [],
  includePromotedContent: false
};

const response = await client.graphqlRequest('/graphql/CreateTweet', variables);
```

#### 方式 3：回复推文

```javascript
const result = await client.tweet('这是一个回复', {
  inReplyToTweetId: '1768234567890123456'
});
```

#### 方式 4：发送带媒体的推文

```javascript
const result = await client.tweet('查看这张图片！', {
  media: [
    { media_id: '1869610428579606520' },
    { media_id: '1869610428579606521' }
  ]
});
```

#### 方式 5：标记为敏感内容

```javascript
const result = await client.tweet('18+ 内容...', {
  possiblySensitive: true
});
```

---

### cURL 示例

#### 基本推文

```bash
curl --location --request POST 'https://api.apidance.pro/graphql/CreateTweet' \
  --header 'Authtoken: your-auth-token' \
  --header 'apikey: your-api-key' \
  --header 'User-Agent: Apidog/1.0.0 (https://apidog.com)' \
  --header 'Content-Type: application/json' \
  --header 'Accept: */*' \
  --header 'Host: api.apidance.pro' \
  --header 'Connection: keep-alive' \
  --data-raw '{
    "variables": {
      "tweet_text": "Hello Twitter! 🚀",
      "dark_request": false,
      "reply": {
        "in_reply_to_tweet_id": null,
        "exclude_reply_user_ids": []
      },
      "media": {
        "media_entities": [],
        "possibly_sensitive": false
      },
      "semantic_annotation_ids": [],
      "includePromotedContent": false
    }
  }'
```

#### 回复推文

```bash
curl --location --request POST 'https://api.apidance.pro/graphql/CreateTweet' \
  --header 'Authtoken: your-auth-token' \
  --header 'apikey: your-api-key' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "variables": {
      "tweet_text": "这是一个回复",
      "dark_request": false,
      "reply": {
        "in_reply_to_tweet_id": "1768234567890123456",
        "exclude_reply_user_ids": []
      },
      "media": {
        "media_entities": [],
        "possibly_sensitive": false
      },
      "semantic_annotation_ids": [],
      "includePromotedContent": false
    }
  }'
```

#### 带媒体的推文

```bash
curl --location --request POST 'https://api.apidance.pro/graphql/CreateTweet' \
  --header 'Authtoken: your-auth-token' \
  --header 'apikey: your-api-key' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "variables": {
      "tweet_text": "查看这张图片！",
      "dark_request": false,
      "reply": {
        "in_reply_to_tweet_id": null,
        "exclude_reply_user_ids": []
      },
      "media": {
        "media_entities": [
          { "media_id": "1869610428579606520", "tagged_users": [] },
          { "media_id": "1869610428579606521", "tagged_users": [] }
        ],
        "possibly_sensitive": false
      },
      "semantic_annotation_ids": [],
      "includePromotedContent": false
    }
  }'
```

---

## 媒体上传

### 获取媒体 ID

在上传媒体到推文前，需要先上传文件获取 `media_id`。

**步骤：**
1. 上传图片/视频文件到 Twitter
2. 获取返回的 `media_id`
3. 在 `media.media_entities` 中使用该 ID

**apidance.pro 上传 API**（如果支持）

```bash
POST /v1.1/media/upload

参数：
- media: <binary file data>
- media_type: image/jpeg | image/png | video/mp4 等
```

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `Invalid token` | AuthToken 过期或无效 | 从 X.com/settings 重新获取 |
| `Invalid API key` | API Key 错误 | 检查 APIDANCE_API_KEY 环境变量 |
| `Tweet text too long` | 推文超过 280 字 | 缩短推文内容 |
| `Rate limit exceeded` | 请求过于频繁 | 等待或购买更高配额 |
| `Invalid media_id` | 媒体 ID 不存在 | 确保先上传媒体并获取有效 ID |

### 错误响应结构

```json
{
  "errors": [
    {
      "message": "Error message",
      "code": 400,
      "details": "Detailed explanation"
    }
  ]
}
```

### 在代码中处理错误

```javascript
try {
  const result = await client.tweet('推文内容');
  console.log('✅ 成功！推文 ID:', result.tweetId);
} catch (err) {
  console.error('❌ 发推失败:', err.message);
  
  // 根据错误类型采取行动
  if (err.message.includes('token')) {
    console.error('→ 需要更新 AuthToken');
  } else if (err.message.includes('too long')) {
    console.error('→ 推文过长，需要缩短');
  }
}
```

---

## 性能优化

### 1. 批量发推

```javascript
// 批量发推时，添加延迟以避免速率限制
const tweets = ['推文1', '推文2', '推文3'];

for (let i = 0; i < tweets.length; i++) {
  await client.tweet(tweets[i]);
  
  // 推文间隔 3 秒
  if (i < tweets.length - 1) {
    await new Promise(r => setTimeout(r, 3000));
  }
}
```

### 2. 连接复用

```javascript
// 多次使用同一个 client 实例
const client = new TwitterDanceAPIClient({...});

// ✅ 好：复用同一实例
for (let i = 0; i < 10; i++) {
  await client.tweet(`推文 ${i + 1}`);
}

// ❌ 差：每次创建新实例
for (let i = 0; i < 10; i++) {
  const c = new TwitterDanceAPIClient({...});
  await c.tweet(`推文 ${i + 1}`);
}
```

### 3. 并行请求

```javascript
// 并行发送多个推文（注意速率限制）
const tweets = ['推文1', '推文2', '推文3'];
const promises = tweets.map(text => client.tweet(text));
const results = await Promise.allSettled(promises);
```

---

## 配额管理

### 检查 API 配额

```javascript
const quota = await client.checkQuota();
console.log('剩余配额:', quota.remaining);
```

### 配额成本

| 操作 | 成本 |
|------|------|
| 发推 | 1 个配额 |
| 回复 | 1 个配额 |
| 带媒体推文 | 1 个配额 |
| 点赞 | 0.5 个配额 |
| 转发 | 0.5 个配额 |

### 月度成本估算

- 每天 1 条推文：~$0.24/月
- 每天 10 条推文：~$2.4/月
- 每天 30 条推文：~$7.2/月

---

## 集成示例

### 与 Cron 任务集成

```bash
# 每天 09:00 自动发推
0 9 * * * cd /path/to/twitter-dance && node scripts/auto-tweet.js >> logs/cron.log 2>&1
```

### 与 OpenClaw 集成

```javascript
// 在 OpenClaw Skill 中使用
const TwitterDanceAPIClient = require('./src/twitter-api-client');

// skill.js
async function tweet(content) {
  const client = new TwitterDanceAPIClient({
    apiKey: process.env.APIDANCE_API_KEY,
    authToken: process.env.TWITTER_AUTH_TOKEN
  });
  
  return await client.tweet(content);
}

module.exports = { tweet };
```

---

## 故障排除

### 问题：推文发布后找不到

**原因**：可能被 Twitter 自动审核隐藏或删除

**解决方案**：
1. 检查账户是否有违规
2. 查看推文是否包含不当内容
3. 查看 Twitter 通知了解更多信息

### 问题：速率限制错误

**原因**：发推过于频繁

**解决方案**：
1. 增加推文间隔（至少 3 秒）
2. 使用配额更高的 API Key
3. 分散发推时间

### 问题：媒体上传失败

**原因**：media_id 无效或过期

**解决方案**：
1. 确保先上传媒体获取有效 ID
2. 检查媒体格式是否支持
3. 检查文件大小是否超限

---

## 最佳实践

✅ **推荐做法**
- 使用环境变量存储敏感信息
- 添加适当的错误处理和重试逻辑
- 遵守 API 速率限制（3 秒/条推文）
- 定期监控 API 配额
- 在发推前进行内容审查
- 使用日志记录所有操作

❌ **避免做法**
- 硬编码 API Key 和 Token
- 一次发超过 50 条推文
- 忽视错误响应
- 在高并发情况下发推
- 重复发送相同内容
- 不检查推文长度

---

## 参考资源

- [apidance.pro 官方文档](https://doc.apidance.pro)
- [Twitter API v2 文档](https://developer.twitter.com/en/docs/twitter-api)
- [GraphQL 简介](https://graphql.org/)

---

## 更新日志

### v2.0.0（2026-03-12）
- ✅ 新增 `graphqlRequest()` 方法（低级 GraphQL API）
- ✅ 完善 `tweet()` 方法，支持回复和媒体
- ✅ 添加详细的请求头格式
- ✅ 改进错误处理和响应解析
- ✅ 新增测试脚本 `test-tweet-graphql.js`

### v1.0.0（2026-03-11）
- ✅ 初始发布
- ✅ 基本 tweet() 功能
- ✅ auto-tweet.js 脚本

---

**需要帮助？**
- 📧 Issue: https://github.com/your-repo/issues
- 💬 讨论: https://discord.com/invite/clawd
- 📖 文档: https://docs.openclaw.ai

