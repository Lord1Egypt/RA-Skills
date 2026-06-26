---
name: registry-sync
description: Keep the Feishu registry sheet in sync whenever a new local skill, workflow, or template is created or significantly updated. Use when a new skill is added under workspace/skills, when a new workflow becomes part of the regular operating system, when a new template is created under research/, or when the user asks to update, register, sync, or maintain the Skill/Workflow registry table. Also use after successfully creating a new reusable workflow so it does not get forgotten.
---

# Registry Sync

Maintain the Feishu registry spreadsheet as the source of truth for local skills, workflows, and templates.

## Registry target
Primary registry sheet:
- Spreadsheet: `加十的 Skill 与工作流清单`
- URL: `https://bytedance.larkoffice.com/sheets/Bf6qsMV9fhqrD6tPE6TcQhF7nEe`

Known tabs:
- `总览`
- `Skills`
- `Workflows`
- `Templates`
- `Content`

## Core rule

When a new reusable capability is created, do not stop at file creation. Also update the registry sheet.

## What counts as a registry item

### Skills
Register items under `/Users/shiyi/.openclaw/workspace/skills/*/SKILL.md`

### Workflows
Register persistent operating flows such as:
- Feishu doc workflow
- Feishu sheet workflow
-公众号灵感池
- content pipeline
- any recurring multi-step operational flow the user is expected to reuse

### Templates
Register reusable process templates under `/Users/shiyi/.openclaw/workspace/research/` such as:
- install/wiring
- debug
- delivery/handoff
- api selection
- scheduled briefing

## Minimum metadata to capture

For each new item, capture at least:
- 名称
- 作用
- 适用场景
- 典型触发
- 默认位置/资源位置
- 当前状态
- 优先级
- 备注

## Sync procedure

1. Determine the category:
   - Skill
   - Workflow
   - Template
   - Content-related flow

2. Read the local source of truth:
   - SKILL.md for skills
   - workflow doc / Feishu doc / known runtime artifact for workflows
   - research template file for templates

3. Summarize the item in practical language.

4. Update the proper tab in the registry sheet.

5. If the item changes the high-level landscape, also update `总览`.

## Preferred write strategy

Prefer structured table writes over ad-hoc manual browser typing.

If a new tab is required and `feishu_sheet` API cannot create worksheet tabs, use the `feishu-sheet-tabs` skill approach:
- create tabs via browser runtime methods
- populate them with `feishu_sheet`

## When to trigger automatically

Trigger this skill after:
- creating a new local skill
- creating a new reusable template
- creating a new recurring workflow the user will reuse

Do not wait for the user to remind you.

## Fallback

If Feishu Sheets is temporarily unavailable, append the pending registry change to a local backlog file and tell the user it is queued.

Backlog file:
- `/Users/shiyi/.openclaw/workspace/research/registry-sync-backlog.md`

## Backlog format

- 日期
- 类别
- 名称
- 应写入哪个分页
- 待补充的字段

## Output style

Keep the confirmation brief:
- what was registered
- which tab was updated
- whether the write was direct or queued
