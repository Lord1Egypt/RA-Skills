# [Skill Name] Evolution Rules

Domain-specific self-improvement rules for [skill-name]. Log learnings and errors to `.learnings/`; promote proven patterns to the targets below. **Evolution is driven by user feedback.**

## Quick Reference

| Situation | Action |
|-----------|--------|
| {LEARNING_TRIGGER_1} | Log to `.learnings/LEARNINGS.md` with category `correction` or `style_mismatch` |
| {LEARNING_TRIGGER_2} | Log to `.learnings/LEARNINGS.md` |
| {ERROR_TRIGGER_1} | Log to `.learnings/ERRORS.md` |
| {ERROR_TRIGGER_2} | Log to `.learnings/ERRORS.md` |
| User wants missing capability | Log to `.learnings/FEATURE_REQUESTS.md` |
| Pattern proven across 3+ instances | Promote to {PROMOTION_TARGET_1} |
| Safety/correctness rule | Promote to {PROMOTION_TARGET_2} |

## Review → Apply → Report Loop

**Before task**: Load relevant entries from `.learnings/LEARNINGS.md` (and ERRORS.md if applicable). Filter by area, tags, or keywords.

**During task**: Apply learnings when relevant. Optionally annotate: "本次参考了 [LRN-xxx]: ..." (or equivalent in target language).

**After task**: Tell user which learnings were used, what evolution result, what improvement. Decide per-use mention vs end-of-task summary based on context.

## Detection Triggers

### Learning Triggers (→ LEARNINGS.md)

- {LEARNING_TRIGGER_1}
- {LEARNING_TRIGGER_2}
- {LEARNING_TRIGGER_3}
- User provides correction or preference
- Better approach discovered for recurring task

### Error Triggers (→ ERRORS.md)

- {ERROR_TRIGGER_1}
- {ERROR_TRIGGER_2}
- {ERROR_TRIGGER_3}
- Operation fails unexpectedly
- Unexpected output or behavior

## Domain Activation Conditions (for hooks)

When to remind the agent to check learnings:

- {ACTIVATION_CONDITION_1}
- {ACTIVATION_CONDITION_2}

## Promotion Decision Tree

```
Is the learning skill-specific?
├── Yes → Keep in .learnings/
└── No → Is it style/behavior-related?
    ├── Yes → Promote to {PROMOTION_TARGET_1}
    └── No → Is it safety/correctness-related?
        ├── Yes → Promote to {PROMOTION_TARGET_2}
        └── No → Promote to {PROMOTION_TARGET_1}
```

## Experience Invalidation & Update

When user corrects again after a learning was applied:

- Add `Contradicted-By: LRN-YYYYMMDD-XXX` to the original entry
- Mark `Status: superseded` or `Last-Valid: YYYY-MM-DD` if the learning is no longer valid
- Increment `Recurrence-Count` if the pattern recurs but the fix is different

## Area Tags

| Area | Scope |
|------|-------|
| {AREA_1} | {AREA_1_SCOPE} |
| {AREA_2} | {AREA_2_SCOPE} |
| {AREA_3} | {AREA_3_SCOPE} |

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | Blocks core functionality, safety risk |
| `high` | Significant impact, affects common workflows |
| `medium` | Moderate impact, workaround exists |
| `low` | Minor inconvenience, edge case |

## Promotion Targets

- **{PROMOTION_TARGET_1}**: Evolution rules, style preferences, best practices
- **{PROMOTION_TARGET_2}**: Safety guidelines, correctness rules (if applicable)

## Placeholders to Replace

- `[skill-name]`, `[Skill Name]`: Domain name
- `{LEARNING_TRIGGER_1}`, `{LEARNING_TRIGGER_2}`, `{LEARNING_TRIGGER_3}`: User feedback phrases from domain config
- `{ERROR_TRIGGER_1}`, `{ERROR_TRIGGER_2}`, `{ERROR_TRIGGER_3}`: Failure modes from domain config
- `{ACTIVATION_CONDITION_1}`, `{ACTIVATION_CONDITION_2}`: Domain-specific activation (e.g., "User says 改得不通顺", "Optimization reported无效")
- `{PROMOTION_TARGET_1}`, `{PROMOTION_TARGET_2}`: e.g., `[skill-name]-专属进化规则.md`, `[skill-name]-最佳实践.md`
- `{AREA_1}`, `{AREA_2}`, `{AREA_3}`: Domain areas
- `{AREA_1_SCOPE}`, etc.: Brief scope description for each area
