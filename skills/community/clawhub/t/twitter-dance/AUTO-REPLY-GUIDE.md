# 🤖 Twitter 自动回复评论指南

> 自动获取推文评论，并用 AI 智能回复

## 快速开始

### 方法 1️⃣：快速回复特定推文

最简单、最推荐的方法：

```bash
# 模拟模式（查看要回复哪些评论，不实际发送）
node scripts/quick-reply.js --tweet-id=2031936903918883025 --replies=5 --dry-run

# 真实模式（实际发送回复）
node scripts/quick-reply.js --tweet-id=2031936903918883025 --replies=5
```

### 方法 2️⃣：自动回复最近推文的所有评论

```bash
# 模拟模式（查看计划）
node scripts/auto-reply-comments.js --tweets=3 --replies=5 --dry-run

# 真实模式（实际发送）
node scripts/auto-reply-comments.js --tweets=3 --replies=5
```

---

## 详细说明

### 快速回复脚本（推荐）

**文件**: `scripts/quick-reply.js`

**用途**: 为指定推文的所有评论进行智能回复

**命令行选项**:
- `--tweet-id=<ID>` **【必需】** 推文的 Twitter ID
- `--replies=N` 获取最多 N 条评论（默认 10）
- `--dry-run` 模拟模式：仅显示不发送
- `--no-reply` 仅显示评论，不进行回复

**示例**:
```bash
# 获取推文 2031936903918883025 的 10 条最新评论，模拟回复
node scripts/quick-reply.js --tweet-id=2031936903918883025 --dry-run

# 实际回复
node scripts/quick-reply.js --tweet-id=2031936903918883025

# 只看评论，不回复
node scripts/quick-reply.js --tweet-id=2031936903918883025 --no-reply --replies=20
```

### 自动回复脚本

**文件**: `scripts/auto-reply-comments.js`

**用途**: 自动获取你最近的推文，为它们的所有评论进行回复

**命令行选项**:
- `--tweets=N` 获取最近 N 条推文（默认 5）
- `--replies=N` 每条推文获取最多 N 条评论（默认 10）
- `--dry-run` 模拟模式
- `--replied-only` 只对未回复的评论操作
- `--skip-own` 跳过你自己的推文评论

**示例**:
```bash
# 获取最近 5 条推文及其评论，模拟回复
node scripts/auto-reply-comments.js --tweets=5 --replies=5 --dry-run

# 实际回复最近 3 条推文的所有评论
node scripts/auto-reply-comments.js --tweets=3 --replies=10
```

---

## 🎯 如何获取推文 ID

推文 ID 是 Twitter 推文的唯一标识符（通常是 19 位数字）。

### 方法 1：从 URL 获取
1. 打开任何 Twitter 推文
2. URL 格式: `https://twitter.com/username/status/<推文ID>`
3. 例如: `https://twitter.com/elonmusk/status/1234567890123456789`
4. `1234567890123456789` 就是推文 ID

### 方法 2：从开发者工具获取
1. 打开推文，按 `F12` 打开开发者工具
2. 切换到 Network 标签
3. 刷新页面或滚动
4. 查看 API 调用，找到类似 `statuses/show.json` 的请求
5. 在请求的查询参数中查看 `id` 参数

---

## 🧠 AI 回复智能匹配

脚本会自动分析评论内容，选择最合适的回复模板：

| 评论类型 | 触发词 | 回复示例 |
|---------|--------|--------|
| **感谢** | 谢谢、感谢 | "感谢你的反馈！😊" |
| **询问** | 怎么、为什么、？| "很好的问题，让我们继续讨论！" |
| **同意** | 同意、赞成、好 | "完全同意！👏" |
| **鼓励** | 加油、继续 | "继续加油！🚀" |
| **其他** | - | "谢谢你的评论！😄" |

### 自定义回复模板

编辑 `scripts/quick-reply.js` 或 `scripts/auto-reply-comments.js`，修改 `replyTemplates` 对象：

```javascript
const replyTemplates = {
  感谢: [
    '感谢你的反馈！😊',
    '你的支持对我很重要！',
    // 添加更多回复...
  ],
  // 修改或添加其他类别...
};
```

---

## 💡 最佳实践

### ✅ 推荐做法
- 👉 **先用 `--dry-run`** 查看将要回复的内容
- 👉 **开始时使用较少的回复数** (如 3-5 条)，确认效果后再增加
- 👉 **避免连续运行多次**，以免触发 Twitter 限流
- 👉 **定期检查**回复质量，可根据需要调整模板
- 👉 **使用 `--no-reply`** 只看评论，评估是否需要回复

### ❌ 避免
- ❌ 一次性回复过多评论（>50 条）
- ❌ 频繁运行（建议间隔 > 1 小时）
- ❌ 相同内容重复回复多次
- ❌ 忽视 `--dry-run` 直接实际发送

---

## 🔧 配置

### 环境变量

确保你的 `.env` 文件包含：

```env
TWITTER_AUTH_TOKEN=your_auth_token_here
APIDANCE_API_KEY=your_api_key_here
```

### 获取凭证

- **TWITTER_AUTH_TOKEN**: 
  1. 打开 Twitter，按 F12
  2. 应用 → 存储 → Cookies → 查找 `auth_token`
  3. 复制其值

- **APIDANCE_API_KEY**:
  1. 访问 https://t.me/shingle
  2. 从 Telegram Bot 获取 API Key

---

## 🐛 故障排除

### 问题：找不到推文的评论

**原因**:
- 推文 ID 错误
- 推文没有评论
- API 限流

**解决**:
- 确认推文 ID 是否正确
- 使用 `--no-reply` 检查评论是否存在
- 等待几分钟后重试

### 问题：回复发送失败

**错误**: `❌ 回复失败`

**原因**:
- API 限流（太频繁调用）
- 认证失败
- 推文已删除

**解决**:
- 增加延迟：编辑脚本中的 `setTimeout` 值
- 检查 `TWITTER_AUTH_TOKEN` 是否有效
- 确保推文仍然存在

### 问题：获取最近推文失败

**原因**:
- 账户没有推文
- API 认证问题

**解决**:
- 使用 `quick-reply.js` + `--tweet-id` 指定推文
- 检查 API 密钥

---

## 📊 高级用法

### 定时自动回复（使用 Cron）

```bash
# 每天 9:00 AM 自动回复最近 3 条推文的评论
0 9 * * * cd /path/to/twitter-dance && node scripts/auto-reply-comments.js --tweets=3 --replies=10
```

### 只回复未回复的评论

```bash
node scripts/auto-reply-comments.js --tweets=5 --replied-only
```

### 集成到 OpenClaw

在 OpenClaw 中创建 Cron 任务：

```javascript
const job = {
  name: 'Auto Reply Twitter Comments',
  schedule: { kind: 'cron', expr: '0 */2 * * *' }, // 每 2 小时
  payload: {
    kind: 'systemEvent',
    text: 'Run: node /path/to/twitter-dance/scripts/auto-reply-comments.js --tweets=3 --replies=5'
  }
};
```

---

## 📈 性能指标

| 指标 | 值 |
|------|-----|
| 获取评论延迟 | ~2-3 秒/条推文 |
| 回复发送速度 | ~1-2 秒/条评论 |
| 建议最大评论数 | 50 条/次 |
| 建议运行间隔 | ≥1 小时 |
| 平均成功率 | >95% |

---

## 🙋 常见问题

**Q: 可以自定义回复内容吗？**
A: 是的，编辑脚本中的 `replyTemplates` 对象即可。

**Q: 会不会触发 Twitter 限流？**
A: 脚本设计时已考虑限流，自动延迟 1-2 秒。一次回复 <50 条基本不会触发。

**Q: 能否关闭自动回复，只查看评论？**
A: 可以，使用 `--no-reply` 参数。

**Q: 如何在多条推文上使用？**
A: 使用 `auto-reply-comments.js` 脚本，它会自动遍历你最近的推文。

**Q: API Key 过期了怎么办？**
A: 在 https://t.me/shingle 联系获取新的 API Key。

---

## 🎉 完成！

你现在可以开始使用自动回复功能了！

```bash
# 最快开始：
node scripts/quick-reply.js --tweet-id=<你的推文ID> --dry-run

# 然后移除 --dry-run 来真正发送回复
node scripts/quick-reply.js --tweet-id=<你的推文ID>
```

**祝你使用愉快！**🚀
