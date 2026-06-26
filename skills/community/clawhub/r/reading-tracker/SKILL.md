---
name: reading-tracker
description: 个人阅读管理与笔记系统。用于记录读书进度、管理书摘与思考、生成阅读报告。支持渐进式阅读法：书摘记录→每周回顾→月度串联。触发词："开始读"、"记录书摘"、"阅读进度"、"读完"、"复习"、"本月读了什么"。
---

> **English**: Personal reading tracker with spaced repetition reviews, structured note-taking, and monthly reading calendar. Helps you remember what you read and build consistent habits. Designed for readers finishing 30–50 books/year.

# Reading Tracker - 个人阅读管理系统

帮助你建立可持续的阅读习惯，对抗"读完就忘"。

> **English**: Helps you build sustainable reading habits and combat "read and forget". Supports progressive reading: capture → weekly review → monthly synthesis.

## 核心工作流 / Core Workflow

### 1. 开始阅读 / Start Reading
用户说：开始读《书名》
→ 创建书籍笔记文件
→ 记录开始时间
→ 设置阅读目标

> **EN**: User says: "Start reading [Book Title]" → Create note file → Record start date → Set reading goal

### 2. 记录书摘 / Capture Quote
用户说：记录书摘 / 今天读到...
→ 提取书名、内容、思考
→ 检查是否包含进度信息
→ 如无进度，主动追问
→ 保存到对应书籍文件
→ 设置艾宾浩斯复习提醒

> **EN**: User shares a quote/thought → Extract book, content, reflection → Ask for progress if missing → Save to book file → Schedule spaced repetition reviews

### 3. 完成阅读 / Finish Reading
用户说：读完《书名》
→ 触发强制输出三问
→ 保存核心观点、认知改变、行动计划
→ 标记完成状态
→ 生成本书总结

> **EN**: User says "Finished [Book Title]" → Trigger 3 mandatory questions → Save key insight, mindset shift, action plan → Mark as complete

### 4. 复习提醒 / Review Reminders
通过 Cron 每周触发
→ 检查 schedule.json 中到期复习项
→ 推送个性化复习问题

> **EN**: Cron-triggered weekly → Check due reviews in schedule.json → Push personalized review questions

### 5. 生成报告 / Generate Reports
用户说：本月读了什么 / 年度总结
→ 统计阅读天数、连续记录、断档
→ 生成阅读日历
→ 提取跨书关联主题

> **EN**: Monthly/yearly reports with reading calendar, streak tracking, cross-book theme analysis

## 数据存储结构 / Data Structure

### 文件路径 / File Paths
```
workspace/reading/
├── books/
│   └── {book-title}-{YYYY-MM}.md    # Book notes
├── reviews/
│   ├── weekly-{YYYY}-W{WW}.md       # Weekly reviews
│   └── monthly-{YYYY}-{MM}.md       # Monthly synthesis
├── library.json                      # Book index
└── schedule.json                     # Review schedule
```

### 单本书笔记格式 / Book Note Template
```markdown
# 《书名》/ Book Title

## 元信息 / Metadata
- 作者/Author：{作者}
- 开始时间/Started：{YYYY-MM-DD}
- 完成时间/Finished：{YYYY-MM-DD}
- 总进度/Progress：{百分比}%
- 评分/Rating：{1-5}⭐

## 核心输出 / Key Outputs
- 一句话总结/One-sentence summary：
- 认知改变/Mindset shift：
- 行动计划/Action plan：

## 书摘与思考 / Quotes & Thoughts

### {YYYY-MM-DD} 第{X}章/Ch{X}（{进度}%）
> "{书摘内容/Quote}"

**我的想法/My thought**：{思考内容/Reflection}

## 复习记录 / Review Log
- [{日期}] {复习内容}
```

## 交互规则 / Interaction Rules

### 识别意图 / Intent Recognition

**开始阅读 / Start:**
- "开始读《原子习惯》" / "Start reading Atomic Habits"
- "我要读《深度工作》" / "I want to read Deep Work"

**记录书摘 / Capture:**
- "记录书摘..." / "Save this quote..."
- "第X章有句话..." / "Chapter X says..."

**完成阅读 / Finish:**
- "读完《书名》" / "Finished [Book Title]"
- "标记《书名》为已读" / "Mark [Book Title] as read"

**查看复习 / Review:**
- "今天复习什么" / "What to review today"
- "/复习" / "/review"

**生成报告 / Reports:**
- "本月读了什么" / "What did I read this month"
- "阅读报告" / "Reading report"

### 追问逻辑 / Follow-up Logic

**当用户记录书摘但未提供进度时 / When progress is missing:**
```
📝 记录成功 / Saved!

顺便问下，今天读到哪了？
（第X章 / 第X页 / 大概百分之多少？）

EN: What chapter/page are you on?
```

### 完成三问 / The 3 Questions

当用户标记读完时，必须回答：

1. **一句话总结**这本书的核心观点：
   > **EN**: One-sentence summary of the core idea:

2. **认知改变**：它改变了你什么想法？
   > **EN**: Mindset shift: What changed for you?

3. **行动计划**：你会采取什么具体行动？
   > **EN**: Action plan: What will you do differently?

## 报告格式 / Report Format

### 月报模板 / Monthly Report

```
📊 2025年3月阅读报告 / March 2025 Reading Report

┌─────────────────────────────────────┐
│  本月读完：2本 / Finished: 2 books    │
│  在读：1本 / Reading: 1 book          │
│  书摘记录：23条 / Quotes: 23          │
│  平均阅读速度：5天/本 / Avg: 5 days   │
└─────────────────────────────────────┘

📅 本月阅读日历 / Reading Calendar

Mo  Tu  We  Th  Fr  Sa  Su
                          ·
 ·  📖  ·  📖  📖  ·   ·
 ·  📖  ·   ·  📖  📖  ·
📖  ·  📖  ·   ·   ·   ·
 ·  📖

📖 = 有阅读记录 / Read   · = 无记录 / No record

📈 关键数字 / Key Stats
✅ 本月有记录：9天 / 15天（截至今日）
   Days with records: 9/15
⚡ 最长连续：3天（3/4 - 3/6）
   Longest streak: 3 days
😅 最长断档：4天（3/7 - 3/10）
   Longest gap: 4 days

📖 已读完 / Finished:
   1. 《原子习惯》⭐⭐⭐⭐⭐
      Atomic Habits
      核心收获：用系统设计替代意志力
      Key takeaway: Replace willpower with systems
```

## 复习算法 / Review Algorithm

基于艾宾浩斯遗忘曲线 / Spaced repetition based on Ebbinghaus:
- 第1次复习：1天后 / 1 day
- 第2次复习：3天后 / 3 days
- 第3次复习：7天后 / 7 days
- 第4次复习：30天后 / 30 days

## 使用脚本 / Scripts

- `scripts/reading_cli.py` - 核心 CLI 工具 / Core CLI
- `scripts/generate_report.py` - 报告生成 / Report generation
- `scripts/review_scheduler.py` - 复习计划 / Review scheduling

## Cron 配置 / Cron Setup

每周一上午 9:00 触发复习提醒：
```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * 1"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "检查今日阅读复习任务 / Check today's reading reviews"
  }
}
```
