---
name: weekly-report-flow
description: Generate and submit weekly reports from Aliyun DevOps workitems via EMOP API. Use when asked to run the weekly report flow, backfill missing weeks, or explain/automate the DevOps→summary→EMOP submission process.
---

# Weekly Report Flow (DevOps → Summary → EMOP)

## When to use
- User asks to generate/submit weekly reports.
- User asks to backfill missing weeks.
- User asks to automate the DevOps→summary→EMOP flow.

## Required inputs
- **DEVOPS_TOKEN** in environment (never write to disk)
- **EMOP token** in environment (never write to disk)
- **Assignee** default: 姚江峰
- **Types**: 需求/任务/缺陷

## Workflow
1) **Pull DevOps workitems**
   - Use browser session if direct API returns 403.
   - Endpoint: `/projex/api/workitem/workitem/list?_input_charset=utf-8`
   - Header: `x-yunxiao-token: $DEVOPS_TOKEN`
   - Page size 200, iterate all pages.
   - Filter in client by assignee/nickName and type.

2) **Classify**
   - Include **current sprint** workitems.
   - Include **last-week created** items not in current sprint.
   - Last week: Mon 00:00 → Sun 23:59 (Asia/Shanghai).

3) **Summarize**
   - 200–300 Chinese characters, department-formal, not流水账.
   - Output Markdown and also HTML ordered list `<ol><li>...</li></ol>`.

4) **Submit to EMOP**
   - POST `https://emop.oureman.com/api/weekly/report`
   - Headers: `token: $EMOP_TOKEN`, `Content-Type: application/json; charset=utf-8`
   - Body fields:
     - `date`: single day (last Friday, yyyy-MM-dd)
     - `reportDate`: ISO UTC `yyyy-MM-ddTHH:mm:ss.000Z`
     - `content`: `<ol><li>...</li></ol>`
   - Ensure UTF-8 bytes to avoid乱码.

## Backfill mode
- For each missing week (by Friday date), pull DevOps items for that week and generate summary.
- Submit one report per week.

## References
- See `references/urls.md` for project URLs and IDs.
- See `references/cli.md` for local script entrypoints.
