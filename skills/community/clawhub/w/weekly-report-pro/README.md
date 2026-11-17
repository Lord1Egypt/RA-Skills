# Weekly Report Pro v1.2

Auto-collect Git commits + code stats → structured weekly/monthly reports. No fluff, results-oriented.

## Features

- 🔍 Auto-scans local Git repos for commits (weekly or monthly range)
- 📊 Optional code stats: lines added/deleted, files changed per repo
- 🔀 Supports merge commit inclusion for team-lead reporting
- 💬 Asks once for non-code work, metrics, blockers, and next-period plans
- 👤 Auto-detects role (Developer/Ops/Sales/Manager) from repo content
- 🎯 Reads a local Markdown checklist and reports plan completion rate
- 🌐 Emits language metadata for Chinese or English templates
- 📄 4 role templates + 3 output styles (DingTalk/Feishu/Email)
- 📅 Dual mode: Weekly (`--mode weekly`) and Monthly (`--mode monthly`)
- 🔒 Privacy-first: all data stays local, nothing uploaded

> **v1.2** — Adds role override, cross-repository dashboard, Markdown plan tracking and language metadata.

## Quick Start

1. Say "Write my weekly report" or "生成周报" or "写月报"
2. Point to your code directories when asked
3. Answer a few quick questions about your week/month
4. Get a polished, results-oriented report

## Requirements

- Python 3.8+
- Git (for commit collection)

## CLI Options

```
python3 collect_git.py --dirs ~/code --days 7 --with-stats
                       --mode monthly | --include-merges | --author <name>
                       --role auto | --plan-file ./plan.md | --language auto
```

## Who Is This For?

- Developers who want Git commits auto-summarized with line stats
- Tech leads who need merge-aware team progress reports
- Anyone who hates writing weekly/monthly reports from scratch
