# Output Format Templates

> ⚠️ The following templates are **format references**, not fixed formats.
> Adjust flexibly based on actual project conditions. The key is **options + descriptions**.

---

## Principles

**Output format for each question:**
```
Question (trunk + branches)
    +
Option A (command) → Description (consequences/differences/risks/costs/...)
Option B (command) → Description
Option C (command) → Description
    ↓
User selects through dialogue
```

---

## Intra-Stage Output Templates

### Method 1: Table Format (suitable for comparing multiple options)

```
**Core Question: XXX?**

**Option A: XXX**
- Command: Choose this option
- Consequences: What happens after choosing
- Differences: How this differs from others
- Risks: Potential issues
- Costs/Time: Financial or time investment

**Option B: XXX**
- Command: ...
- Consequences: ...
- Differences: ...
- Risks: ...
- Costs/Time: ...

Which do you want to choose?
```

### Method 2: Concise Format (suitable when questions are clear)

```
**Core Question: XXX?**

- **A**: XXX (consequences: ...)
- **B**: XXX (consequences: ...)
- **C**: XXX (consequences: ...)

Which do you want to choose?
```

### Method 3: Q&A Format (suitable when follow-up guidance is needed)

```
**Core Question: XXX?**

What you've mentioned so far: ... (known information)
I need to understand: ...

**Option A: XXX**
- Consequences: ...
- Differences: ...

**Option B: XXX**
- Consequences: ...
- Differences: ...

Which do you want to choose? Or do you have other ideas?
```

---

## Follow-up Question Output Template

```
**Follow-up Question: (based on your selection of XXX, a follow-up)**

You said you want to do XXX. Can you be more specific about what scenario?

- **A1**: XXX (consequences: ...)
- **A2**: XXX (consequences: ...)
- **Other**: Please describe...
```

---

## Summary Stage Output Templates

### Compilation Format

```
## 📋 Project Plan

### Stage 1: Discovery
**Selection:** ...
**Key Decision:** ...

### Stage 2: Analysis
**Selection:** ...
**Key Decision:** ...

...

### Complete Plan

**Goal:** ...

**MVP Scope:**
- ✅ Do first: ...
- ❌ Defer: ...

**Technical Approach:** ...

**Time Estimate:** ...

**Risks & Contingencies:** ...

---

**Next Steps:**
1. ...
2. ...
3. ...

Once you confirm the plan is accurate, I will proceed to the execution stage.
```

---

## Dialogue Confirmation Templates

### Selection Confirmation

```
You selected 【Option A: XXX】.
- Consequences: ...
- Differences: ...

Confirm this selection?
- Confirm → Proceed to next question
- Reselect → Please choose again
- Need more info → Let me supplement...
```

### Stage Completion

```
✅ 【Stage X: Stage Name】 Complete
Selected: ...
Key Decision: ...

→ Proceed to 【Stage Y: Stage Name】?
```

### Planning Completion

```
📋 Planning Complete!

Please confirm the following key decisions:
1. ...
2. ...
3. ...

After confirmation, I will proceed to the execution stage. Let me know if anything needs adjustment.
```

---

## Format Adjustment Guide

| Scenario | Recommended Format |
|----------|---------------------|
| Large differences between options, need careful comparison | Table format |
| Simple and clear question | Concise format |
| Need to guide user thinking | Q&A format |
| Follow-up questions | Compact format |
| Stage summary | Structured compilation |
| Planning complete | Complete version + action checklist |

---

_Preamble + Execution flow: See `SKILL.md`_
_Dynamic question generation: See `references/dynamic-questions.md`_
