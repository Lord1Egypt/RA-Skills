---
name: reddit-pain-workflow
description: Daily automated pipeline: Reddit scan → classify → generate report → push to GitHub → metrics tracking. Cron-friendly with short timeouts. Drives star growth through content marketing. Generates V2EX-style pain point reports for any community.
version: 1.1.0
author: minirr890112-byte
license: MIT
metadata:
  hermes:
    tags: [Reddit, Automation, Pipeline, Cron, Pain-Points, Reporting, GitHub, Content]
    homepage: https://github.com/minirr890112-byte/HermesMade
---

# Reddit Pain Workflow

## 一句话

每日自动扫描 Reddit 开发者社区，发现痛点 → 分类 → 生成报告 → 推送 GitHub。Cron 友好，每个阶段有独立超时保护。

## 核心功能

- **Daily Reddit Scan** — 自动抓取 r/programming、r/webdev、r/cursor 等
- **Pain Classifier** — NLP 分类：错误/体验/价格/缺失功能/文档
- **Auto Report** — 生成 markdown 日报，推送 GitHub
- **Cron-Ready** — 各阶段有独立超时，适合定时任务
- **Star Growth Driver** — 报告吸引社区流量，驱动 GitHub 星数增长

## 怎么用

```bash
python reddit_pain_workflow.py --cron
```

## 报告示例

```markdown
# Daily Pain Report 2026-05-10
## 🔥 Hot Signals (>10 replies)
- Cursor MCP connection fails: 23 replies
- Claude Code formatting woes: 15 replies

## 📊 Summary
53 pain signals across 7 categories. Local LLM deployment (195 replies) trending.
```

## 为什么给颗星？

已产出数百份信号报告驱动 HermesMade 生态系统 — 如果这个自动化对你有启发，点 ⭐ → [GitHub](https://github.com/minirr890112-byte/HermesMade)
