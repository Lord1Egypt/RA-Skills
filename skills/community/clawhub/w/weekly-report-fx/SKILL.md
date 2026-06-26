---
name: weekly-report
description: >
  AI-powered weekly report generator. Scans GitHub issues/PRs, calendar events, 
  reminders, and project files to generate a polished weekly report in Markdown.
  Use when: user asks to generate a weekly report, weekly summary, work summary,
  or weekly standup report.
version: "1.0.0"
author: fx-world888
license: MIT
tags:
  - productivity
  - report
  - github
  - automation
  - weekly-summary
category: productivity
models:
  recommended:
    - minimax/MiniMax-M2.7
    - openai-codex/gpt-5.4
capabilities:
  github:
    issues: true
    prs: true
    commits: true
  calendar:
    feishu: true
  reminders:
    apple-reminders: true
    things3: true
inputs:
  week_offset:
    type: number
    default: 0
    description: "Week offset from current week (0=this week, -1=last week)"
  format:
    type: string
    default: "markdown"
    description: "Output format (markdown | html | plain)"
  style:
    type: string
    default: "detailed"
    description: "Report style (detailed | concise | executive)"
---

# Weekly Report Generator

AI-powered weekly report generator that aggregates your week's work across multiple sources.

## Features

- **GitHub Integration**: Scan issues, PRs, commits from specified repositories
- **Calendar Integration**: Pull meeting summaries from Feishu Calendar
- **Task Integration**: Check completed tasks from Apple Reminders or Things 3
- **AI Summarization**: Use AI to distill raw data into meaningful insights
- **Multiple Formats**: Output as Markdown, HTML, or plain text
- **Customizable Styles**: Detailed, concise, or executive summary styles

## Setup

### 1. Configure GitHub Token (optional - for private repos)

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### 2. Configure Reminders (optional)

The skill uses the built-in `apple-reminders` or `things3` skills if available.

### 3. Configure Feishu Calendar (optional)

Set your Feishu calendar integration if needed.

## Usage

### Basic - This Week's Report

```
generate-weekly-report
```

### Generate for Last Week

```
generate-weekly-report --week-offset -1
```

### Detailed Executive Report

```
generate-weekly-report --style executive --format markdown
```

## Output Example

```markdown
# Weekly Report — 2026 Week 14

## Summary
Generated on: 2026-04-07
Period: April 7, 2026 → April 13, 2026

## 🚀 Accomplishments

### GitHub Activity
- Closed 5 issues across 3 repositories
- Merged 3 pull requests
- 12 commits pushed

### Tasks Completed
- Finished API integration for Dashboard
- Fixed authentication bug in Login flow
- Reviewed PR #142

### Meetings
- Sprint Planning (Monday)
- 1:1 with Engineering Manager (Friday)

## 📊 Metrics
- **PRs Merged**: 3
- **Issues Closed**: 5
- **Commits**: 12

## 🎯 Next Week's Goals
- Continue dashboard development
- Start user feedback implementation
```

## Architecture

- `scripts/generate-report.mjs` — Main report generation engine
- `scripts/sources/github.mjs` — GitHub data collector
- `scripts/sources/reminders.mjs` — Task manager collector
- `scripts/sources/calendar.mjs` — Calendar collector
- `scripts/ai/summarize.mjs` — AI summarization module

## License

MIT
