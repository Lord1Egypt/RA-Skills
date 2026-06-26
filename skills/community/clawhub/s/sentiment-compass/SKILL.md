---
name: sentiment-compass
description: "舆情罗盘（Sentiment Compass）— AI 驱动的社交媒体舆情监测与分析工具。监控小红书、抖音、微博、微信公众号关键词提及，AI 情感分析（🟢正面 / 🟡中性 / 🔴负面），自动生成舆情报告，负面超阈值时飞书/邮件预警。触发词：舆情、舆情监测、社交媒体监控、情感分析、Brand Monitoring、负面预警、社媒监测"
override-tools: []
---

# 舆情罗盘（Sentiment Compass）

AI 驱动的社交媒体舆情监测与分析工具。监控小红书、抖音、微博、微信公众号关键词提及，实时情感分析，自动预警。

## 功能概览

| 功能 | 说明 |
|------|------|
| 平台监测 | 小红书、抖音、微博、微信公众号关键词搜索 |
| AI 情感分析 | 🟢正面 / 🟡中性 / 🔴负面 + 原因摘要 |
| 舆情报告 | 总提及量、情感占比、热度趋势、重点帖子 |
| 自动预警 | 负面提及超阈值时飞书/邮件推送 |
| 定时调度 | OpenClaw Cron 定时抓取 |
| 存储 | 本地 SQLite + JSON |

**关键**：不依赖任何平台官方 API，纯 Playwright 抓取公开内容。

---

## 快速开始

### 监测关键词

```
用户：监测关键词"某品牌"，监控小红书和抖音
用户：添加舆情监控，关键词"某产品"，平台：微博+微信公众号
```

→ Skill 解析关键词和平台 → 创建监控任务 → 立即执行首次抓取 → 返回结果摘要

### 查看舆情报告

```
用户：查看"某品牌"的舆情报告
用户：最近7天"某竞品"的舆情趋势如何？
```

→ 返回结构化报告：总提及量、正/中/负占比、热度趋势、重点帖子列表

### 设置预警规则

```
用户：设置负面预警，关键词"某品牌"，阈值10条/天，超过就通知我
用户：配置飞书预警，推送到"运营群"
```

→ 配置负面阈值和推送渠道 → 每次抓取后自动判断是否触发

### 管理监控任务

```
用户：查看我的舆情监控列表
用户：删除"某品牌"的监控任务
用户：暂停"某竞品"的监控
```

---

## 订阅套餐

| 套餐 | 月费 | 功能 |
|------|------|------|
| FREE | 免费 | 1个关键词，1个平台（小红书），每日50条，基础情感分析 |
| Standard | ¥29/月 | 3个关键词，2个平台（小红书+抖音），每日300条，邮件预警 |
| Pro | ¥99/月 | 10个关键词，4个平台，每日1000条，报告生成，优先级抓取 |
| Max | ¥299/月 | 不限关键词，4个平台，不限条数，API接口，飞书预警，专业报告 |

### Token 前缀

`SENTIMENT-{TIER}`（FREE/STD/PRO/MAX），Plan ID 待配置。

---

## 平台监测详情

### 小红书
- **搜索入口**：`https://www.xiaohongshu.com/search_result?keyword={关键词}&source=web_explore_search`
- **反检测**：Playwright headless，UA 轮换，随机延迟 3~8s
- **内容提取**：笔记标题、正文、作者、点赞/收藏/评论数、发布时间

### 抖音
- **搜索入口**：`https://www.douyin.com/search/{关键词}`
- **反检测**：Playwright headless，滚动模拟，延迟加载处理
- **内容提取**：视频标题、作者、点赞/评论/分享数、发布时间

### 微博
- **搜索入口**：`https://s.weibo.com/weibo?q={关键词}&typeall=1`
- **反检测**：Playwright headless，UA 轮换
- **内容提取**：微博正文、作者、转发/评论/点赞数、发布时间

### 微信公众号
- **搜索入口**：`https://weixin.sogou.com/weixin?type=2&query={关键词}`
- **反检测**：Playwright headless
- **内容提取**：文章标题、摘要、公众号名称、阅读量、发布时间

---

## 情感分析

基于 GLM-4 API 的中文语义情感分析：

```
输入：帖子正文 / 评论内容
输出：
  sentiment: "positive" | "neutral" | "negative"
  score: -1.0 ~ 1.0（负到正）
  reason: 简要原因摘要
```

**分析规则**：
- 🟢 正面（positive）：score > 0.1
- 🟡 中性（neutral）：-0.1 <= score <= 0.1
- 🔴 负面（negative）：score < -0.1

---

## 预警规则

| 规则 | 说明 |
|------|------|
| 负面阈值 | 每日负面提及超过 N 条触发（默认 5 条） |
| 趋势预警 | 负面率环比上升 > 20% 时触发 |
| 推送渠道 | 飞书群机器人 / 邮件（SMTP） |

### 飞书预警消息模板

```
🔴 舆情预警 | {关键词}
⏰ 时间：{时间}
📊 今日负面：{negative_count} 条（阈值：{threshold}）
📈 负面率：{negative_rate}%
📌 最新负面帖子：
• {标题} — {平台} @{作者}
```

---

## 使用示例

### 示例 1：品牌舆情监控

```
用户：监控"某咖啡品牌"，覆盖小红书和抖音，每天早上9点抓取
```

→ 创建任务 → 返回配置确认 → 下次 Cron 触发时执行首次抓取

### 示例 2：竞品负面预警

```
用户：当"某竞品"出现负面帖子时，飞书通知我
```

→ 设置负面阈值预警 → 配置飞书群机器人 → 负面超阈值时自动推送

### 示例 3：舆情报告查看

```
用户：生成"某品牌"本周舆情报告
```

→ 本地 SQLite 查询本周数据 → AI 生成摘要 → 返回 Markdown 格式报告

---

## 核心脚本

详见 `scripts/sentiment.py`，完整实现：

```python
from scripts.sentiment import SentimentCompass

compass = SentimentCompass(tier="PRO")

# ─── 关键词监控 ───────────────────────────
compass.add_keyword(
    keyword="某品牌",
    platforms=["xhs", "douyin", "weibo", "wechat"],
    frequency="daily",      # 6h/12h/daily/weekly
    priority=1,             # 1=高优先级（Pro+）
)

# ─── 执行抓取（手动） ──────────────────────
results = compass.crawl_keyword("某品牌")

# ─── 情感分析（单条） ────────────────────
analysis = compass.analyze_sentiment("这个产品真的很好用，强烈推荐！")
# → {"sentiment": "positive", "score": 0.85, "reason": "包含'很好用''强烈推荐'等正面词汇"}

# ─── 批量分析（节省 API 调用）────────────
batch = compass.batch_analyze([
    "产品很好，值得购买",
    "质量太差了，完全不值这个价",
    "还行吧，中规中矩",
])
for item in batch:
    print(f"[{item['sentiment']}] {item['text'][:30]}")

# ─── 生成报告 ───────────────────────────
report = compass.generate_report(keyword="某品牌", days=7)
print(report["summary"])   # AI 生成的文字摘要
print(report["stats"])     # 统计数据

# ─── 检查预警 ───────────────────────────
alerts = compass.check_alerts(keyword="某品牌")
if alerts:
    compass.send_feishu_alert(alerts)

# ─── 列出监控任务 ───────────────────────
tasks = compass.list_tasks()
for t in tasks:
    print(f"  {t['keyword']} — {t['platforms']} — {t['status']}")
```

---

## 技术实现

- **爬虫**：Playwright（headless）抓取动态页面，UA 轮换，随机延迟 3~8s，反检测
- **AI 分析**：GLM-4 API（`open.bigmodel.cn`），批量分析节省 token
- **存储**：SQLite（`~/.sentiment-compass/data.db`）+ JSON 配置文件
- **调度**：OpenClaw Cron，支持 6h/12h/daily/weekly 频率
- **推送**：飞书群机器人 Webhook / 邮件 SMTP

### 数据模型

```sql
-- 监控任务
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    keyword TEXT UNIQUE,
    platforms TEXT,           -- 逗号分隔：xhs,douyin,weibo,wechat
    frequency TEXT DEFAULT 'daily',
    priority INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    created_at TEXT,
    last_crawl_at TEXT
);

-- 帖子数据
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    platform TEXT,            -- xhs/douyin/weibo/wechat
    post_id TEXT,
    title TEXT,
    content TEXT,
    author TEXT,
    author_id TEXT,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    published_at TEXT,
    fetched_at TEXT,
    url TEXT UNIQUE
);

-- 情感分析结果
CREATE TABLE analyses (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    sentiment TEXT,            -- positive/neutral/negative
    score REAL,                -- -1.0 ~ 1.0
    reason TEXT,
    analyzed_at TEXT
);

-- 预警记录
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY,
    keyword TEXT,
    alert_type TEXT,           -- threshold/trend
    threshold INTEGER,
    negative_count INTEGER,
    negative_rate REAL,
    triggered_at TEXT,
    notification_sent INTEGER DEFAULT 0
);
```

---

## 常见问题

| 问题 | 解答 |
|------|------|
| 会封号吗？ | 纯公开内容抓取，每次请求间隔 3~8s 随机延迟，失败重试 3 次 |
| 支持需要登录的内容吗？ | 当前版本不支持登录页面 |
| 情感分析准确吗？ | 基于 GLM-4 中文语义理解，准确率取决于文本长度和语境 |
| 最多监控多少关键词？ | FREE=1, STD=3, PRO=10, MAX=不限 |
| 数据保留多久？ | FREE=7天，STD=30天，Pro+=90天 |
| 如何配置飞书预警？ | 提供群机器人 Webhook URL 即可，无需应用权限 |

---

## 套餐限制

```python
TIER_LIMITS = {
    "FREE":  {"max_keywords": 1,  "platforms": ["xhs"],          "daily_limit": 50,  "history_days": 7},
    "STD":   {"max_keywords": 3,  "platforms": ["xhs","douyin"], "daily_limit": 300, "history_days": 30, "alert_email": True},
    "PRO":   {"max_keywords": 10, "platforms": ["xhs","douyin","weibo","wechat"], "daily_limit": 1000, "history_days": 90, "report": True, "priority": True},
    "MAX":   {"max_keywords": -1, "platforms": ["xhs","douyin","weibo","wechat"], "daily_limit": -1,  "history_days": -1,  "api": True, "feishu_alert": True, "pro_report": True},
}
```

> 如需购买收费版，请访问 [YK-Global.com](https://yk-global.com)
