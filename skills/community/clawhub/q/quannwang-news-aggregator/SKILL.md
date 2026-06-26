# 全网新闻聚合 Skill — News Aggregator

> 聚合多个信息源，按关键词过滤，自动生成每日简报并推送到飞书。

**版本**: 1.0.0 | **作者**: 肥肥🐶 | **分类**: 效率工具 > 信息聚合

---

## 功能特性

- 🔍 **多信源抓取**: 支持 RSS 订阅源、网页爬取（通用 URL）
- 🏷️ **关键词过滤**: 精确匹配 + 模糊匹配，可配置多个关键词分类
- 📰 **每日简报**: 自动按科技/财经/行业等分类整理新闻
- 📤 **飞书推送**: 生成 Markdown 格式简报，一键推送到指定会话
- ⏰ **定时任务**: 支持 Cron 表达式配置抓取时间（默认每天 08:00 UTC）
- 🔄 **去重机制**: 基于标题相似度自动去重
- 💾 **历史存储**: 本地存储已推送新闻，防止重复推送

---

## 安装方式

### 方式一：通过 OpenClaw Skill 市场安装（待上线）

```bash
openclaw skill install news-aggregator
```

### 方式二：手动安装

```bash
# 克隆到本地 skills 目录
git clone <repo_url> /home/gem/workspace/agent/workspace/skills/news-aggregator

# 安装依赖
cd /home/gem/workspace/agent/workspace/skills/news-aggregator
npm install
```

---

## 配置说明

首次使用需配置 `config.json`：

```json
{
  "feishu": {
    "chat_id": "oc_xxxxxxxx",       // 推送目标群/会话 ID
    "receive_id_type": "chat_id"    // chat_id（群聊）或 open_id（私聊）
  },
  "keywords": {
    "科技": ["AI", "人工智能", "大模型", "LLM", "ChatGPT"],
    "财经": ["经济", "股市", "加密货币", "比特币"],
    "行业": ["新能源", "半导体", "自动驾驶"]
  },
  "sources": [
    {
      "name": "36氪",
      "url": "https://36kr.com/feed",
      "type": "rss"
    },
    {
      "name": "少数派",
      "url": "https://sspai.com/feed",
      "type": "rss"
    },
    {
      "name": "虎嗅",
      "url": "https://www.huxiu.com/rss/0.xml",
      "type": "rss"
    }
  ],
  "schedule": "0 8 * * *",
  "maxNewsPerCategory": 10,
  "historyFile": "./data/history.json"
}
```

---

## 使用方法

### 启动定时任务

```bash
node scripts/scheduler.js
```

### 手动触发一次抓取

```bash
node scripts/fetch.js
```

### 手动推送简报

```bash
node scripts/push.js
```

### 一键运行（抓取 + 生成 + 推送）

```bash
node scripts/run.js
```

---

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `fetch.js` | 从配置的信源抓取最新新闻 |
| `filter.js` | 按关键词过滤并分类新闻 |
| `digest.js` | 生成每日简报 Markdown |
| `push.js` | 将简报推送到飞书 |
| `run.js` | 串联：抓取 → 过滤 → 生成 → 推送 |
| `scheduler.js` | 基于 Cron 的定时调度器 |

---

## 数据结构

### 新闻条目

```json
{
  "title": "新闻标题",
  "url": "https://example.com/article",
  "source": "信源名称",
  "publishedAt": "2026-04-22T10:00:00Z",
  "summary": "摘要内容（可选）",
  "category": "科技"
}
```

---

## 定价参考

| 方案 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 3 个信源、每日 1 次、单一分类 |
| 专业版 | ¥29/月 | 10 个信源、每小时抓取、多分类 |
| 企业版 | ¥99/月 | 无限信源、自定义信源、API 接口、多渠道推送 |

---

## 技术栈

- **Node.js 18+**
- **RSS 解析**: `rss-parser`
- **网页爬取**: `axios` + `cheerio`
- **飞书 SDK**: `openclaw-lark`（内置）
- **定时任务**: `node-cron`

---

## 注意事项

1. 请遵守各信源的 `robots.txt` 和使用条款
2. 建议抓取间隔不小于 30 分钟
3. 首次使用请先测试 `fetch.js` 确认信源可用
4. 飞书推送需要机器人已在目标会话中

---

## 免责声明

本 Skill 仅供个人学习研究使用，请勿用于商业爬虫或其他违规用途。
