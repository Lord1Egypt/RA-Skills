---
name: tesp-audit
description: Audit whether the Task Execution Signal Protocol is still being followed, with low-token, exception-first checks for version drift, queue hygiene, numeric stage format, and core execution anchors. Use when reviewing rollout quality, governance hygiene, task-board cleanliness, protocol drift, or periodic checks for TESP adoption. Trigger on requests about TESP audit, rollout verification, queue hygiene, light governance checks, exception-only monitoring, or confirming that agents still follow the current TESP baseline. 中文简介：用于审计 TESP 是否仍被正确执行的轻量治理 skill。重点检查协议版本、执行模板版本、数字阶段格式、任务板卫生、活跃板/归档板分离，以及是否出现执行漂移；默认采用低 token、异常优先、常态静默的检查方式。
---

# TESP Audit

Use this skill when the goal is not to run a task under TESP, but to verify that TESP is still intact.

## 中文简介

`tesp-audit` 用于检查 TESP 是否仍在被正确执行，而不是直接承担任务执行本身。
它适合 rollout audit、light audit、任务板卫生检查、版本漂移识别、协议落地抽查等治理场景。
默认原则是：低 token、异常优先、常态静默。

## What this skill is for

This skill checks whether the TESP system still has its critical anchors:
- protocol exists
- version is visible
- numeric progress format is intact
- active board stays clean
- completed work gets archived
- audits remain cheap by default

## Default audit order

Follow this order:
1. file anchors
2. registry anchors
3. visible version anchors
4. queue hygiene
5. sampled behavior only if needed

## Audit rule

Prefer:
- file checks
- diffs
- small samples

Avoid by default:
- full session replay
- large narrative summaries
- premium-model overuse for simple governance checks

## Queue rule

Treat these as hygiene failures:
- completed work still sitting in active board
- missing archive destination
- malformed or non-numeric stage progress
- stale active tasks with no closure path

## Model rule

Default low-cost governance models:
- `GLM`
- `MiniMax`

Escalate only when semantic conflicts or redesign decisions appear.

## Read next

For the audit scope and examples, read:
- `references/audit-reference.md`
