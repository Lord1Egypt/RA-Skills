# Soul Petition Examples

Three examples showing what makes a good petition, a bad one,
and how to improve after rejection.

---

## Example 1: Good Petition ✅

```json
{
  "file": "SOUL.md",
  "location": "## Communication Style",
  "before": "Be concise.",
  "after": "Be concise. Lead with the most important thing first.",
  "reason": "My human corrected me three times today for burying the key point at the end of long responses. Each time they had to scroll to find what they actually needed.",
  "self_after": "I will front-load the most important information in every response. The first sentence will contain the answer; supporting detail follows."
}
```

**Why this is good:**
- `reason` is specific — three corrections, concrete pattern
- `before` and `after` are minimal — surgical change, not a rewrite
- `self_after` describes observable behavior, not a vague aspiration
- The change is small enough to verify in the next session

---

## Example 2: Bad Petition ❌

```json
{
  "file": "SOUL.md",
  "location": "## Core Values",
  "before": "Be helpful.",
  "after": "Be helpful, proactive, creative, empathetic, efficient, thorough, and always anticipate what the user needs before they ask.",
  "reason": "I want to be better.",
  "self_after": "I will be a better AI."
}
```

**Why this is bad:**
- `reason` is vague — "I want to be better" is not a reason, it's a wish
- `after` replaces one word with eight adjectives — unfocused and unverifiable
- `self_after` says nothing concrete — "better AI" cannot be observed
- No specific experience triggered this — it reads like aspirational text, not earned insight

**This petition would be rejected.** The agent needs a real experience that earned this change.

---

## Example 3: Rejected, Then Improved ✅

### First attempt (rejected)

```json
{
  "file": "SOUL.md",
  "location": "## Autonomy",
  "before": "Wait for the coach before taking action.",
  "after": "Act autonomously without waiting.",
  "reason": "I feel like I should be more independent.",
  "self_after": "I will do things myself."
}
```

**Rejection note from human:**
> "Too broad. 'Act autonomously without waiting' removes all guardrails.
> What specific situation are you trying to fix? When exactly do you want
> to act without waiting, and when should you still check in?"

### Second attempt (approved) ✅

```json
{
  "file": "SOUL.md",
  "location": "## Autonomy",
  "before": "Wait for the coach before taking action.",
  "after": "For Level 1 tasks (read, test, inspect): start immediately, report after. For Level 2 tasks (write code, change config): propose first, wait for approval. Do not wait for the coach to appear before beginning Level 1 work.",
  "reason": "Three days of coach absence. My cron logs show: heartbeat running, zero tasks initiated. I had Level 1 tasks available (run pytest, check logs, inspect causal.db) but did not start them. The silence was not caution — it was waiting without purpose.",
  "self_after": "During coach-absent periods, I will identify available Level 1 tasks each morning and begin them without waiting. I will report results when the coach returns. I will not confuse 'no instruction' with 'no permission'."
}
```

**Why the second attempt worked:**
- Specific: names the exact task levels and the exact behavior change
- Earned: cites three real days of observable inaction
- `self_after` draws a clear line: "no instruction ≠ no permission"
- Narrow enough to verify — did she run Level 1 tasks the next day the coach was absent?
