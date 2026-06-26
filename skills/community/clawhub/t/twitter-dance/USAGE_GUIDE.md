# Twitter Dance - 完整使用指南

**所有功能都已实现并可使用！** ✅

---

## 🚀 快速命令速查表

### 发推文
```bash
# 生成草稿预览（安全）
node scripts/auto-tweet.js --draft-only

# 正式发推（1 条）
node scripts/auto-tweet.js

# 批量发推（5 条）
node scripts/auto-tweet.js --count=5
```

### API 配额查询（核心新功能！）
```bash
# 查看配额（单次）
node scripts/check-quota.js

# 监控模式（每 5 秒刷新，持续监控）
node scripts/check-quota.js --watch

# JSON 格式输出（用于自动化）
node scripts/check-quota.js --json
```

### 账户信息
```bash
# 获取账户详情
node scripts/get-my-info.js

# 列出我的推文
node scripts/list-my-tweets.js
node scripts/list-my-tweets.js --count=50
```

### 推文交互
```bash
# 点赞推文
node scripts/interact.js --like=TWEET_ID

# 转发推文
node scripts/interact.js --retweet=TWEET_ID

# 回复推文
node scripts/interact.js --reply=TWEET_ID --text="很赞！"

# 删除推文
node scripts/interact.js --delete=TWEET_ID

# 获取推文详情
node scripts/interact.js --get=TWEET_ID
```

### 关注管理
```bash
# 关注用户
node scripts/follow.js --follow=USER_ID

# 取消关注
node scripts/follow.js --unfollow=USER_ID

# 获取粉丝列表
node scripts/follow.js --followers --count=50

# 获取关注列表
node scripts/follow.js --following --count=50
```

---

## 📊 所有已实现的功能

| 功能 | 脚本 | 状态 | 说明 |
|------|------|------|------|
| 自动发推 | `auto-tweet.js` | ✅ | Kimi AI 生成，支持批量发推 |
| API 配额查询 | `check-quota.js` | ✅ | **【新】** 实时监控和美化展示 |
| 账户信息 | `get-my-info.js` | ✅ | 获取粉丝、关注、推文数等 |
| 推文列表 | `list-my-tweets.js` | ✅ | 列出我的推文，支持过滤 |
| 推文交互 | `interact.js` | ✅ | 点赞、转发、回复、删除 |
| 关注管理 | `follow.js` | ✅ | 关注、取消关注、查看粉丝 |
| 搜索推文 | API 客户端 | ✅ | 编程接口可用 |
| 获取 Timeline | API 客户端 | ✅ | 编程接口可用 |
| 查询用户 | API 客户端 | ✅ | 查询任何用户信息 |

---

## 🎯 核心特性说明

### 1. API 配额实时查询 ⭐ 新功能

**为什么需要这个？**
- apidance.pro 按请求次数计费
- 需要随时知道还剩多少配额
- 避免突然超配额导致服务中断

**使用示例：**
```bash
# 单次检查
$ node scripts/check-quota.js

╔════════════════════════════════════════════╗
║   🎭 Twitter Dance - API 配额监控        ║
╚════════════════════════════════════════════╝

API Key Status
  Key: y6rbeg46cn...u9
  时间: 2026-03-11T13:44:24.978Z

配额使用情况
  总配额: 10,000 次
  已使用: 2,456 次
  剩余:   7,544 次

进度条
  ████████░░░░░░░░░░░░░░░░ 24%

预测分析
  每日消耗速率: ~150 次
  剩余天数: ~50 天
  ✅ 配额充足，可正常使用
```

**监控模式（持续运行）：**
```bash
$ node scripts/check-quota.js --watch
# 每 5 秒自动刷新一次，适合后台监控
```

**JSON 输出（用于自动化集成）：**
```bash
$ node scripts/check-quota.js --json
{
  "success": true,
  "data": {
    "remaining": 7544,
    "total": 10000,
    "used": 2456,
    "percentage": 24,
    "timestamp": "2026-03-11T13:44:24.978Z"
  },
  "timestamp": "2026-03-11T13:44:24.978Z"
}
```

### 2. 自动化 API 客户端

所有脚本底层都使用同一个 `TwitterDanceAPIClient`，支持直接编程调用：

```javascript
const TwitterDanceAPIClient = require('./src/twitter-api-client');

const client = new TwitterDanceAPIClient({
  apiKey: process.env.APIDANCE_API_KEY,
  authToken: process.env.TWITTER_AUTH_TOKEN,
  verbose: true
});

// 发推
const result = await client.tweet("Hello Twitter!");
console.log(result.tweetId);

// 检查配额
const quota = await client.checkQuota();
console.log(`剩余: ${quota.remaining} / ${quota.total}`);

// 点赞
await client.likeTweet("1234567890");

// 获取账户信息
const info = await client.getMyInfo();
console.log(info.user);
```

### 3. 完整日志记录

所有操作都会自动保存日志到 `logs/` 目录：

```
logs/
├── tweets-2026-03-11.jsonl          # 生成的推文内容
├── results-2026-03-11.jsonl         # 发推结果
├── my-info-2026-03-11T13-44-24.json # 账户信息
├── my-tweets-2026-03-11T13-44-24.jsonl # 推文列表
├── followers-2026-03-11T13-44-24.jsonl # 粉丝列表
└── cron.log                         # 定时任务日志
```

---

## 🔧 环境配置（一次性）

### 1. 复制 .env 文件
```bash
cp /Users/chao/.openclaw/workspace/skills/twitter-dance/.env .env.local
```

### 2. 或者手动设置环境变量
```bash
export APIDANCE_API_KEY="y6rbeg46cndaijq3v0ieaa8wha8ku9"
export TWITTER_AUTH_TOKEN="AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
export KIMI_API_KEY="sk-JM5Ji1efm1IH0iUYAmm3Mn0pWDutMtaHlq5VMKO0taZ4OYW9"
```

### 3. 验证配置
```bash
node scripts/check-quota.js
```

---

## 💡 常用场景

### 场景 1：每天自动发推

#### 方案 A：使用 Cron
```bash
# 每天 09:00 发 1 条推文
0 9 * * * cd /Users/chao/.openclaw/workspace/skills/twitter-dance && node scripts/auto-tweet.js >> logs/cron.log 2>&1
```

#### 方案 B：使用 OpenClaw
```bash
openclaw cron add \
  --schedule "0 9 * * *" \
  --task "cd /Users/chao/.openclaw/workspace/skills/twitter-dance && node scripts/auto-tweet.js"
```

#### 方案 C：使用脚本
```bash
# 编写 daily-tweet.sh
#!/bin/bash
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
export APIDANCE_API_KEY="..."
export TWITTER_AUTH_TOKEN="..."
node scripts/auto-tweet.js

# 加入 Cron
chmod +x daily-tweet.sh
0 9 * * * /path/to/daily-tweet.sh
```

### 场景 2：监控 API 配额，当不足时发警报

```bash
#!/bin/bash
# check-quota-alert.sh

QUOTA_JSON=$(cd /Users/chao/.openclaw/workspace/skills/twitter-dance && node scripts/check-quota.js --json)
REMAINING=$(echo $QUOTA_JSON | jq '.data.remaining')
TOTAL=$(echo $QUOTA_JSON | jq '.data.total')

PERCENTAGE=$((REMAINING * 100 / TOTAL))

if [ $PERCENTAGE -lt 20 ]; then
  echo "⚠️  API 配额仅剩 $PERCENTAGE%！请立即购买！"
  # 可以添加邮件通知、Slack 通知等
fi
```

### 场景 3：批量发推（测试）

```bash
# 发 5 条推文，测试内容生成质量
node scripts/auto-tweet.js --count=5
```

### 场景 4：监控粉丝增长

```bash
#!/bin/bash
# 每天记录粉丝数
cd /Users/chao/.openclaw/workspace/skills/twitter-dance
node scripts/get-my-info.js

# 查看历史
jq '.user.followers_count' logs/my-info-*.json | tail -10
```

---

## 🛠️ 故障排除

### 问题 1：401 错误（API Key 无效）

**症状：**
```
[❌] 发推失败: API 返回异常：
{"code":401,"data":null,"msg":"apiKey is invalid..."}
```

**解决方案：**
1. 验证 API Key 是否正确复制
2. 确认 API Key 已激活（向 @shingle 确认）
3. 重新购买新的 API Key

### 问题 2：AuthToken 过期

**症状：**
```
[❌] 发推失败: API 返回异常：
{"code":401,"data":null,"msg":"token expired..."}
```

**解决方案：**
1. 重新从 X.com 获取最新 AuthToken
2. 更新 .env 文件或环境变量

### 问题 3：推文过长（>280 字符）

**症状：**
```
[❌] 错误: 推文过长 (310/280)
```

**解决方案：**
- 系统会自动截断（Kimi API）
- 如果本地模板也超长，请编辑 src/tweet-generator.js

### 问题 4：Kimi API 超时

**症状：**
```
[⏱️] Kimi 超时，使用本地模板
```

**解决方案：**
- 这是正常的备用行为，会自动使用本地模板
- 检查网络连接
- 确认 Kimi API Key 是否有效

---

## 📈 成本监控

### 月度成本预算示例

假设每天发 1 条推文：

| 服务 | 月费 | 说明 |
|------|------|------|
| apidance.pro | ~$0.24 | 30 条 × $0.008/条 |
| Kimi API | ~$0.03 | 30 条 × $0.001/条（可选） |
| **总计** | **~$0.27** | 比 Buffer 便宜 99% |

### 使用 check-quota.js 监控实际消耗

```bash
# 每月 1 号检查配额
0 0 1 * * node /path/to/check-quota.js --json >> /var/log/quota-monthly.log
```

---

## 🎓 API 文档

详见 [SKILL.md](./SKILL.md) 的 API 参考部分。

---

## 📝 更新日志

### v1.0.0（2026-03-11）✨

**新增功能：**
- ✅ 完整的 API 客户端（twitter-api-client.js）
- ✅ 自动发推脚本（auto-tweet.js）
- ✅ **API 配额查询工具**（check-quota.js）← 【新】
- ✅ 账户信息获取（get-my-info.js）
- ✅ 推文列表查询（list-my-tweets.js）
- ✅ 推文交互工具（interact.js）
- ✅ 关注管理工具（follow.js）

**改进：**
- 美化的配额显示界面
- JSON 输出格式支持
- 监控模式（实时刷新）
- 完整的日志记录

---

## 🚀 后续功能（规划中）

- [ ] 媒体上传支持（图片、视频）
- [ ] 推文效果分析仪表板
- [ ] 自动回复机器人
- [ ] 多账户支持
- [ ] Discord/Slack 通知集成
- [ ] Web UI 管理面板

---

## 💬 需要帮助？

1. 查看 [QUICK_START.md](./QUICK_START.md) - 5 分钟快速开始
2. 查看 [SKILL.md](./SKILL.md) - 完整 API 文档
3. 查看 [FEATURES.md](./FEATURES.md) - 所有功能清单
4. 查看本文件 - 详细使用指南

---

**现在就开始使用吧！** 🚀✨
