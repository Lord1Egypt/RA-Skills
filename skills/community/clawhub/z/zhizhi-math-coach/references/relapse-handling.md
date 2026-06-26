# Relapse Handling

## Purpose

When an error type or cause was previously marked `补齐理解`, `待巩固`, or `已掌握`, treat a similar new mistake as a history-aware event.

Do not overwrite the old status without comparing evidence. Decide whether this is:

- `复发`: the same concept or cause failed again.
- `迁移失败`: familiar form works, changed wording or mixed context fails.
- `间隔遗忘`: the child understood before, but spacing was too long.
- `偶发失误`: isolated slip without repeated evidence.

## Decision Rules

- Same wording plus same wrong method: mark `复发`, likely `理解未稳固`.
- New wording plus same underlying model: mark `迁移失败`.
- Long gap after prior success: mark `复发`, likely `间隔遗忘`.
- One wrong item but nearby same-type items correct: mark `观察中` or `偶发失误`.
- Repeated mistakes across two or more items in one batch: mark `复发` with high confidence.

If evidence is unclear, use `复发待确认` and generate 2 to 3 diagnostic verification questions.

## Required Diagnosis Additions

For relapse-like cases, include:

- `历史状态`: previous status and date.
- `复发判断`: `复发` / `迁移失败` / `间隔遗忘` / `偶发失误` / `复发待确认`.
- `历史对比`: what is the same and what changed.
- `处理策略`: reteach, spaced review, mixed practice, or diagnostic verification.

## Response Strategy

- `理解未稳固`: return to concrete explanation and ask the child to explain the rule aloud.
- `迁移失败`: use paired contrast problems with similar numbers but changed wording.
- `间隔遗忘`: use spaced review: today, two days later, one week later.
- `偶发失误`: add a checking prompt, not a full reteach.
- `复发待确认`: give a mini diagnostic set before changing the status.
