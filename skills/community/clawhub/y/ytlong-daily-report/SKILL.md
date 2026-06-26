---
name: daily-report-generator
description: Automatically generate daily/weekly work reports from git commits, calendar events, and task lists. Use when you need to quickly create professional work reports without manual effort.
tags: [productivity, automation, report, git, calendar]
---

# Daily Report Generator

Automatically generates professional daily/weekly work reports by analyzing:
- Git commits from the day/week
- Calendar events
- Task completions

## Features

- **Multi-source aggregation**: Pulls data from git, calendar, and task managers
- **Smart summarization**: Groups related activities automatically
- **Multiple formats**: Markdown, HTML, plain text
- **Language support**: Chinese and English output

## Usage

### Generate Today's Report

```bash
node index.js today
```

### Generate Weekly Report

```bash
node index.js week
```

### Generate Custom Date Range

```bash
node index.js range --from 2024-01-01 --to 2024-01-07
```

### Specify Output Format

```bash
node index.js today --format html
node index.js week --format markdown
```

## Configuration

Create a `.reportrc.json` in your project root:

```json
{
  "git": {
    "enabled": true,
    "repos": ["./", "../other-project"]
  },
  "calendar": {
    "enabled": true,
    "sources": ["google", "apple"]
  },
  "tasks": {
    "enabled": true,
    "sources": ["apple-reminders"]
  },
  "output": {
    "language": "zh-CN",
    "format": "markdown",
    "includeStats": true
  }
}
```

## Output Example

```markdown
# 工作日报 - 2024年1月15日

## 完成的任务
- ✅ 完成用户认证模块开发
- ✅ 修复登录页面样式问题
- ✅ 代码审查：PR #123

## Git 提交
- feat: 添加双因素认证 (abc123)
- fix: 修复移动端显示问题 (def456)
- docs: 更新 API 文档 (ghi789)

## 会议
- 10:00 产品需求评审会
- 14:00 技术方案讨论

## 明日计划
- 继续开发支付模块
- 参加团队周会
```

## Requirements

- Node.js 18+
- Git (for commit analysis)
- Optional: Calendar access (Google/Apple)

## Installation

```bash
npm install
```

## License

MIT
