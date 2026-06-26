# Twitter Dance - 高级功能指南

> 全面的 Twitter 账户管理和自动化工具
>
> 包括：账户统计、通知、自动回复、数据分析、互动周期

## 快速开始

### 1. 账户统计

获取你的 Twitter 账户详细统计信息：

```bash
node scripts/test-advanced-features.js stats
```

**输出示例：**
```
📱 账户信息
姓名: 滴滴老司机
账户: @getrich_BTCCC
简介: Your bio here
位置: Location

📊 统计数据
粉丝: 417
关注: 733
推文: 382
点赞: 156
媒体: 30
列表: 7
```

**API 用法：**
```javascript
const stats = await client.getAccountStats();

// 返回：
// {
//   success: true,
//   account: { name, handle, bio, location, verified },
//   stats: { followers, following, tweets, likes, mediaCount, listedCount },
//   profile: { profileImage, createdAt, isProtected }
// }
```

---

### 2. 获取通知

获取最新的互动通知（提及、点赞、转发、回复）：

```bash
node scripts/test-advanced-features.js notifications
```

**输出示例：**
```
🔔 通知摘要
提及: 5
回复: 3
点赞: 12
转发: 2
关注: 0

📝 最新互动:
1. @username - 5❤️ 2🔄
   "你好啊！很喜欢你的..."
```

**API 用法：**
```javascript
const notifications = await client.getNotifications({ count: 20 });

// 返回：
// {
//   success: true,
//   notifications: [{
//     type: 'interaction',
//     author: '用户名',
//     handle: 'username',
//     text: '推文内容',
//     likes: 5,
//     retweets: 2,
//     timestamp: '2026-03-12...',
//     tweetId: '123456'
//   }],
//   summary: { mentions, replies, likes, retweets, follows }
// }
```

---

### 3. 自动回复

自动回复特定的推文：

```bash
node scripts/test-advanced-features.js reply 2031936903918883025 "感谢你的评论！"
```

**API 用法：**
```javascript
const result = await client.autoReply(
  tweetId,           // 被回复推文的 ID
  '回复内容',         // 回复文本
  { 
    prependMention: true  // 自动 @ 提及原作者
  }
);

// 返回：
// {
//   success: true,
//   replyId: '新推文 ID',
//   originalTweetId: '原推文 ID',
//   text: '回复内容',
//   timestamp: '2026-03-12...'
// }
```

**批量回复：**
```javascript
const tweetIds = ['123', '456', '789'];

for (const tweetId of tweetIds) {
  await client.autoReply(tweetId, '感谢评论！');
  // 避免速率限制
  await new Promise(r => setTimeout(r, 2000));
}
```

---

### 4. 推文指标

获取单条推文的详细互动数据：

```bash
node scripts/test-advanced-features.js metrics 2031936903918883025
```

**输出示例：**
```
📈 推文指标
❤️  点赞: 156
🔄 转发: 42
💬 回复: 8
💭 引用: 2
👀 浏览: 2,345
📊 总互动: 208
```

**API 用法：**
```javascript
const metrics = await client.getTweetMetrics(tweetId);

// 返回：
// {
//   success: true,
//   tweetId: '...',
//   metrics: {
//     likes: 156,
//     retweets: 42,
//     replies: 8,
//     quotes: 2,
//     views: 2345
//   },
//   engagement: {
//     totalEngagement: 208,
//     engagementRate: 0.089
//   }
// }
```

---

### 5. 时间线分析

分析你的推文历史数据：

```bash
node scripts/test-advanced-features.js timeline-analytics
```

**输出示例：**
```
📊 时间线统计
总推文: 100
总点赞: 5,234
总转发: 1,123
总回复: 456
平均点赞/条: 52
平均转发/条: 11

⭐ 最受欢迎的推文
"AI 的发展速度已经超出想象..."
互动数: 234
发布时间: 2026-03-12T03:34:44Z
```

**API 用法：**
```javascript
const analytics = await client.getTimelineAnalytics({ count: 100 });

// 返回：
// {
//   success: true,
//   totalTweets: 100,
//   totalLikes: 5234,
//   totalRetweets: 1123,
//   totalReplies: 456,
//   averageLikes: 52,
//   averageRetweets: 11,
//   topTweet: {...},
//   tweets: [{id, text, likes, retweets, replies, engagement}]
// }
```

---

### 6. 互动周期分析

找出最佳发推时间：

```bash
node scripts/test-advanced-features.js engagement-hours
```

**输出示例：**
```
⏰ 按小时的互动情况

🏆 最佳发推时间 (UTC):

1. 09:00     - 平均互动: 45.2 ████████████
2. 14:00     - 平均互动: 38.5 ██████████
3. 08:00     - 平均互动: 35.1 █████████
4. 20:00     - 平均互动: 32.4 ████████
5. 18:00     - 平均互动: 28.9 ███████

💡 建议: 在 09:00 UTC 发推，获得最高互动
```

**API 用法：**
```javascript
const analysis = await client.getEngagementByHour();

// 返回：
// {
//   success: true,
//   hourlyStats: [
//     {hour: 0, tweets: 5, totalEngagement: 123, avgEngagement: 24.6},
//     {hour: 1, tweets: 3, totalEngagement: 98, avgEngagement: 32.7},
//     ...
//   ],
//   bestHour: 9,
//   bestHourEngagement: 45.2
// }
```

---

### 7. 批量操作

#### 批量点赞

```bash
node scripts/test-advanced-features.js bulk-like 123 456 789
```

**API 用法：**
```javascript
const tweetIds = ['123', '456', '789'];
const result = await client.bulkLikeTweets(tweetIds);

// 返回：
// {
//   success: true,
//   liked: 3,
//   failed: 0,
//   errors: []
// }
```

#### 批量转发

```javascript
const tweetIds = ['123', '456', '789'];
const result = await client.bulkRetweet(tweetIds);

// 返回：同上结构
```

---

### 8. 对话线程

获取推文的完整回复链：

```bash
node scripts/test-advanced-features.js conversation 2031936903918883025
```

**API 用法：**
```javascript
const thread = await client.getConversationThread(tweetId);

// 返回：
// {
//   success: true,
//   rootTweet: {...},
//   replies: {
//     success: true,
//     replies: [...]
//   },
//   timestamp: '2026-03-12...'
// }
```

---

## 完整代码示例

### 监控账户和自动回复

```javascript
const TwitterDanceEnhanced = require('./src/twitter-api-enhanced');

async function monitorAndRespond() {
  const client = new TwitterDanceEnhanced({
    apiKey: process.env.APIDANCE_API_KEY,
    authToken: process.env.TWITTER_AUTH_TOKEN
  });

  // 1. 获取账户统计
  const stats = await client.getAccountStats();
  console.log(`粉丝: ${stats.stats.followers}`);

  // 2. 获取最新通知
  const notifications = await client.getNotifications({ count: 10 });
  
  // 3. 自动回复提及
  for (const notif of notifications.notifications) {
    if (notif.type === 'interaction') {
      await client.autoReply(
        notif.tweetId,
        `感谢 @${notif.handle} 的评论！`
      );
    }
  }

  // 4. 分析最佳发推时间
  const bestTime = await client.getEngagementByHour();
  console.log(`最佳发推时间: ${bestTime.bestHour}:00 UTC`);
}

monitorAndRespond().catch(console.error);
```

### 数据分析仪表板

```javascript
async function generateReport() {
  const client = new TwitterDanceEnhanced({...});

  // 账户概览
  const stats = await client.getAccountStats();
  const analytics = await client.getTimelineAnalytics({ count: 200 });
  const engagement = await client.getEngagementByHour();

  const report = {
    account: stats.account.name,
    followers: stats.stats.followers,
    totalTweets: analytics.totalTweets,
    avgEngagement: Math.round(analytics.totalLikes / analytics.totalTweets),
    bestTweet: analytics.topTweet,
    bestTime: `${engagement.bestHour}:00 UTC`,
    recommendations: generateRecommendations(analytics, engagement)
  };

  console.log(JSON.stringify(report, null, 2));
}
```

### 定时发推和自动互动

```javascript
const schedule = require('node-schedule');

async function setupAutomation() {
  const client = new TwitterDanceEnhanced({...});

  // 每天 09:00 UTC 发推
  schedule.scheduleJob('0 9 * * *', async () => {
    await client.tweet('早上好！今天也要加油💪 #DailyTweet');
  });

  // 每小时检查一次通知并回复
  schedule.scheduleJob('0 * * * *', async () => {
    const notif = await client.getNotifications({ count: 5 });
    for (const n of notif.notifications) {
      await client.autoReply(n.tweetId, '感谢支持！');
    }
  });
}

setupAutomation();
```

---

## 方法参考

### TwitterDanceEnhanced 类

#### 账户和统计

| 方法 | 参数 | 返回 |
|------|------|------|
| `getAccountStats()` | - | 账户统计数据 |
| `getTimelineAnalytics(options)` | `{count}` | 时间线分析 |
| `getEngagementByHour()` | - | 按小时的互动数据 |

#### 通知和互动

| 方法 | 参数 | 返回 |
|------|------|------|
| `getNotifications(options)` | `{count}` | 通知列表 |
| `getTweetMetrics(tweetId)` | `tweetId` | 推文指标 |
| `autoReply(tweetId, text, options)` | `{tweetId, text, options}` | 回复结果 |

#### 批量操作

| 方法 | 参数 | 返回 |
|------|------|------|
| `bulkLikeTweets(tweetIds)` | `[tweetIds]` | 操作结果 |
| `bulkRetweet(tweetIds)` | `[tweetIds]` | 操作结果 |

#### 分析

| 方法 | 参数 | 返回 |
|------|------|------|
| `getConversationThread(tweetId)` | `tweetId` | 对话线程 |

---

## 场景应用

### 场景 1：社媒运营

```javascript
// 每天分析最佳发推时间，自动发推
const engagement = await client.getEngagementByHour();
const bestHour = engagement.bestHour;

schedule.scheduleJob(`0 ${bestHour} * * *`, async () => {
  // 发推
  await client.tweet('日常推文内容...');
});
```

### 场景 2：社区管理

```javascript
// 定期检查通知并自动回复
schedule.scheduleJob('0 * * * *', async () => {
  const notifications = await client.getNotifications();
  for (const n of notifications.notifications) {
    if (isRelevant(n.text)) {
      await client.autoReply(n.tweetId, 'Thank you for your comment!');
    }
  }
});
```

### 场景 3：数据分析

```javascript
// 生成月度报告
const stats = await client.getTimelineAnalytics({ count: 500 });
const bestTweets = stats.tweets
  .sort((a, b) => b.engagement - a.engagement)
  .slice(0, 10);

console.table(bestTweets);
```

---

## 最佳实践

✅ **推荐做法**

- 在批量操作时添加延迟（避免速率限制）
- 使用 schedule 定时发推而不是频繁手动发推
- 定期分析互动周期，优化发推时间
- 监控通知并及时回复
- 每周查看时间线分析，评估内容效果

❌ **避免做法**

- 一次性回复超过 50 条推文
- 在短时间内批量点赞数百条推文
- 忽视 API 错误和网络异常
- 发送垃圾回复或自动回复
- 不检查推文内容就批量操作

---

## 故障排除

### 问题：通知获取返回空结果

**原因：** home_timeline 可能没有足够的新推文

**解决方案：**
```javascript
const notifications = await client.getNotifications({ count: 100 });
```

### 问题：自动回复失败

**原因：** Token 过期或推文不存在

**解决方案：**
```javascript
try {
  await client.autoReply(tweetId, '回复内容');
} catch (err) {
  if (err.message.includes('Could not authenticate')) {
    console.error('Token 已过期，请更新');
  }
}
```

### 问题：时间线分析数据不完整

**原因：** 只获取了部分推文

**解决方案：**
```javascript
const analytics = await client.getTimelineAnalytics({ count: 300 });
```

---

## 更新日志

### v2.1.0（2026-03-12）

- ✅ 新增 `TwitterDanceEnhanced` 类
- ✅ 添加账户统计功能
- ✅ 添加通知管理
- ✅ 添加自动回复
- ✅ 添加数据分析
- ✅ 添加互动周期分析
- ✅ 添加批量操作
- ✅ 完整的测试脚本和文档

---

## 相关文档

- [GRAPHQL_API_GUIDE.md](./GRAPHQL_API_GUIDE.md) - GraphQL API 参考
- [QUICK_START.md](./QUICK_START.md) - 快速开始
- [USAGE_GUIDE.md](./USAGE_GUIDE.md) - 使用指南

---

**需要帮助？** 查看完整示例：`scripts/test-advanced-features.js`
