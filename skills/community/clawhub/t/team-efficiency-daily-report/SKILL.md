---
name: team-efficiency-daily-report
description: Generate team efficiency daily report automatically
---

# Team Efficiency Daily Report

Generate team efficiency daily report automatically.

## What this skill does

This skill will:

1. Open the configured dashboard URL
2. Capture the XHR API request payload
3. Modify query time range if need:
   - startTime = first day of current month
   - endTime = today
4. Call the API to fetch data
5. Parse efficiency metrics
6. Save today's data locally
7. Generate a markdown daily report

## Usage

When the user asks something like:

- 生成团队效能日报
- 查询团队效能数据
- 生成效能分析日报

Run:
node dist/index.js

## Output

The skill will generate:


~/openclaw-skill-data/team-efficiency-daily-report/YYYY-MM-DD.json
~/openclaw-skill-data/team-efficiency-daily-report/YYYY-MM-DD.md


Example:

~/openclaw-skill-data/team-efficiency-daily-report/2026-03-13.md

## Configuration

Report configuration is defined in:

config.json

It contains:

- dashboard url
- data API
- metric column mapping
- need to modify request params