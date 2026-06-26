# TESP Protocol Reference

## Identity
- Full name: `Task Execution Signal Protocol`
- Abbreviation: `TESP`
- Current baseline version: `v1.0.2`

## Purpose
TESP exists to ensure that any task beyond the instant-response window remains visible, staged, and governable.

The goal is not just to do the work, but to make execution observable:
- status visible
- stage visible
- blockers visible
- outputs visible
- no need for the human to chase updates

## Layer Structure
TESP has 3 fixed layers:
1. Layer 1 — acknowledgement
2. Layer 2 — progress broadcast
3. Layer 3 — task board

## Layer 1 rule
Required format:

```text
✅ 已接收 | TESP v1.0.2 | 预计 X 分钟可完成
场景：[1-3句话概括问题总结或者前置场景]
目标：[1-3句话概括任务方向或者目标]
```

Rules:
- version must be visible
- `场景` must restate the underlying situation, not just the title
- `目标` must make the direction explicit
- send fast, ideally within 30 seconds for non-instant work

## Layer 2 rule
Cadence:
- ≤1 hour → every 15 minutes
- 1–6 hours → every 1 hour
- >6 hours → split into subtasks first

Progress format uses numeric stage notation only:
- `1/1`
- `2/5`
- `4/5`

Never use alphabetic stage notation like `A2/C3`.

Subtasks should generally stay under 6 hours.

## Layer 3 rule
Active work lives in:
- `/Users/weweclaw/.openclaw/workspace/TASK_QUEUE.md`

Completed work lives in:
- `/Users/weweclaw/.openclaw/workspace/TASK_ARCHIVE.md`

Rule:
- active board keeps only in-progress / blocked / waiting-for-confirmation work
- completed work should be removed from active view and archived promptly

## Cross-agent rule
When handing off:
1. update task board
2. write shared handoff
3. transfer execution

## Version rule
TESP must be versioned in two places:
1. protocol document version
2. visible execution version in Layer 1

Audits should check both.

## Token rule
TESP governance should default to cheap signals first:
1. file checks
2. diff checks
3. sampled verification
4. only then deeper reasoning if drift appears

Preferred low-cost models for routine governance:
- `GLM`
- `MiniMax`

## Existing audit hook
A light audit cron already exists in the source workspace:
- name: `tesp:light-audit`
- cadence: daily at 06:30 Asia/Shanghai
- model: `GLM`
- style: exception-first, normally silent, always writes a local report
