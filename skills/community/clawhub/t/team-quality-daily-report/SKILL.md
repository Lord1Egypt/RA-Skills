---
name: team-quality-daily-report
description: Generate team quality daily report automatically
---

# Team Quality Daily Report

Generate team quality daily report automatically.

## What this skill does

This skill will:

1. Open the configured dashboard URL
2. Capture the XHR API request payload
3. Modify query time range:
   - startTime = first day of current month
   - endTime = today
4. Call the API to fetch data
5. Parse quality metrics
6. Save today's data locally
7. Compare with yesterday's data
8. Generate a markdown daily report

## Usage

When the user asks something like:

- 生成团队质量日报
- 查询团队质量数据
- 生成质量分析日报

Run:
node dist/index.js

## Output

The skill will generate:


~/openclaw-skill-data/team-quality-daily-report/YYYY-MM-DD.json
~/openclaw-skill-data/team-quality-daily-report/YYYY-MM-DD.md


Example:

~/openclaw-skill-data/team-quality-daily-report/2026-03-13.md

## Configuration

Report configuration is defined in:

config.json

It contains:

- dashboard url
- data API
- metric column mapping