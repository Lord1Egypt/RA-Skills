# Token Tracker

API Token 消耗追踪与报表生成工具。

## 功能特点

- 📊 **自动记录** - 追踪每次对话的 token 消耗
- 📈 **日报周报** - 生成详细的消耗报表
- 🔍 **趋势分析** - 分析使用模式，预测月度消耗
- 🔔 **定时推送** - 支持 cron 自动发送报告

## 快速开始

### 记录 Token 消耗

```bash
python3 scripts/log_token.py 1200 800
```

### 生成日报

```bash
python3 scripts/daily_report.py
```

### 生成周报

```bash
python3 scripts/weekly_report.py
```

## 报告示例

```
📊 Token 消耗日报 - 2026年3月19日

💰 今日汇总
• 输入：2,400 tokens
• 输出：1,800 tokens
• 总计：4,200 tokens
• 较昨日：📈 +15.3%

📅 近7天消耗明细

| 日期 | 输入 | 输出 | 总计 | 环比 | 趋势 |
|------|------|------|------|------|------|
| 3/13 | 1,200 | 800 | 2,000 | - | 📊 |
| 3/14 | 1,350 | 900 | 2,250 | +12.5% | 📈 |
...

📈 趋势分析
• 本周总计：18,150 tokens
• 日均消耗：2,593 tokens
• 预估月耗：约 77,790 tokens
```

## 定时推送设置

```bash
# 每天晚上 22:00 发送日报
cron add --name "token-daily-report" \
  --schedule "0 22 * * *" \
  --command "python3 scripts/daily_report.py"
```

## 版本

- 版本：1.0.0
- 更新日期：2026-03-19
