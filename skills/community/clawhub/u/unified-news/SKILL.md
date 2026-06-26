---
name: unified-news
description: 统一新闻获取与推送服务。整合 Web3/Crypto、AI科技、宏观经济热点以及金融市场新闻。支持分类获取、定时推送、去重过滤、自动格式化输出。当用户要求获取新闻、热点推送、资讯简报、定期新闻推送、或提到"新闻"、"资讯"、"热点"时使用此 Skill。
---

# Unified News Skill

整合 6551 API（热点新闻）和 RSS（财经新闻）的统一新闻服务。

## 数据源

| 源 | 类型 | 说明 |
|----|------|------|
| 6551 API | REST | Web3、AI、Macro 热点新闻 |
| RSS Feeds | Web | 财经/科技新闻（WSJ、CNBC、Yahoo） |

## 工作流程

### 1. 获取新闻分类

```bash
curl -s -X GET "https://ai.6551.io/open/free_categories"
```

### 2. 获取热点新闻

```bash
# Web3/Crypto 热点
curl -s -X GET "https://ai.6551.io/open/free_hot?category=crypto"

# AI/科技 热点
curl -s -X GET "https://ai.6551.io/open/free_hot?category=ai"

# 宏观经济 热点
curl -s -X GET "https://ai.6551.io/open/free_hot?category=macro"
```

### 3. 去重过滤

检查本地文件 `memory/news-sent.md` 读取今天已发送的新闻 ID，按 ID 或标题过滤已推送内容。

### 4. 格式化输出

整理新闻格式：
- 标题 + 来源
- 摘要（中英双语）
- 热度评分
- 相关代币/股票（如有）

### 5. 发送消息

使用 message 工具发送到飞书：
```json
{
  "action": "send",
  "channel": "feishu",
  "message": "格式化后的新闻内容"
}
```

### 6. 更新记录

将已发送的新闻 ID 追加到 `memory/news-sent.md`

## 定时推送配置

创建 cron 任务每4小时推送：

```bash
openclaw cron create \
  --name "新闻热点推送" \
  --every "4h" \
  --message "获取并推送新闻热点。请执行：1. 调用 unified-news skill 获取 Web3、AI、Macro 新闻；2. 检查 memory/news-sent.md 避免重复；3. 过滤已发送热点；4. 格式化发送到当前对话；5. 更新发送记录；6. 回复 NO_REPLY" \
  --channel feishu \
  --account <your-bot-id> \
  --to <target-user-id> \
  --session isolated \
  --announce
```

## 输出格式

```markdown
📰 今日新闻热点 — 2026年3月20日

🔥 Web3/Crypto
1. [标题] - 来源 | 热度: 85
   摘要...
   相关: BTC, ETH

🤖 AI/科技
1. [标题] - 来源 | 热度: 90
   摘要...

📈 宏观经济
1. [标题] - 来源 | 热度: 80
   摘要...

---
已发送新闻数: X
```
