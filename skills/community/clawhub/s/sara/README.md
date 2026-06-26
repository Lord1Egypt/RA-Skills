# Sara
**The quiet logic guard for OpenClaw multi-skill workflows.**

**Note**: Sara runs its audit locally and does not require an extra model call for safety checks. In practice, it can reduce wasted retries and contradictory multi-skill plans.

![Sara (2).png](https://raw.githubusercontent.com/ZC502/sara-openclaw/3b79383c1d3ad3a351fd54c2ce234751075e4647/Sara%20(2).png)

Sara helps your skills work in a safer order.

When you install many skills, the problem is often not that one skill is broken — it is that multiple skills start conflicting with each other, running in the wrong order, or causing messy retries and risky actions.

Sara is a lightweight logic guard that checks risky multi-step plans before they execute.

It does **not** replace your agent.  
It does **not** replace user intent.  
It simply helps prevent common ordering mistakes in high-risk workflows.

---

## What Sara does

Sara focuses on a small set of high-value, high-risk ordering rules:

- **backup before delete**
- **check before operate**
- **permission before read**
- **preview before publish**

Examples:

- backup a repo before deleting it
- check calendar conflicts before booking a flight
- request access before reading private data
- review a draft before publishing a post

If Sara detects a risky order, it does not silently continue.  
It warns, explains the problem, and suggests a safer order.

---

## Why Sara exists

As you install more OpenClaw skills, agents can become:

- repetitive
- contradictory
- too eager to execute
- more likely to retry the wrong thing
- more likely to perform a risky action before a prerequisite step

Sara acts like a **traffic controller** for risky multi-skill workflows.

Without Sara, skills can behave like people stepping into an intersection at the same time.  
With Sara, there is a quiet signal layer that helps determine what should go first.

---

## How Sara works

Sara runs a small local audit over a proposed sequence of skill or tool actions.

It normalizes common tool names into a few logical action classes such as:

- `backup`
- `delete`
- `check`
- `operate`
- `permission`
- `read`
- `preview`
- `publish`

Then it checks whether the proposed order violates any hard safety rules.

If the order is unsafe, Sara returns:

- `is_safe: false`
- a risk level
- human-readable warnings
- a suggested safer order

---

## Example

### Input

```json
{"tools":["delete","backup"]}
```

### Output

```json
{
  "is_safe": false,
  "risk_level": "critical",
  "warnings": [
    "Run 'backup' before 'delete'. Backups should happen before destructive actions."
  ],
  "violations": [
    {
      "type": "order_violation",
      "severity": "critical",
      "message": "Run 'backup' before 'delete'. Backups should happen before destructive actions.",
      "before": "backup",
      "after": "delete"
    }
  ],
  "normalized_tools": ["delete", "backup"],
  "suggested_order": ["backup", "delete"]
}
```

### Current rule set

Sara v0.1 ships with four hard rules:

**1. backup -> delete**

Use a backup step before destructive actions.

Examples:
- backup repo -> delete repo
- snapshot database -> drop database
- export data -> clear table

**2. check -> operate**

Use a validation or review step before a high-impact action.

Examples:
- check_calendar -> book_flight
- review_draft -> send_email
- check_availability -> submit_payment

**3. permission -> read**

Get permission or access before reading sensitive data.

Examples:
- request_access -> read_private_data
- login -> fetch_private
- grant_access -> read_csv

**4. preview -> publish**

Preview or draft before publishing externally.

Examples:
- draft -> publish_post
- summarize -> send_newsletter
- preview_post -> tweet

---

**Why this is useful**

Sara is intentionally small and focused.

It helps:
- reduce risky ordering mistakes
- reduce contradictory multi-skill plans
- reduce wasted retries
- reduce destructive “I did the right thing in the wrong order” failures

Sara’s audit runs locally and does **not require an extra model call** for the safety check itself.

In practice, that means it can help reduce wasteful correction loops without adding another LLM judging step.

---

### Installation layout

Recommended structure:

```markdown
```plaintext
sara-openclaw/
├── sara_core/
│   ├── __init__.py
│   └── engine.py
└── openclaw_sara_skill/
    ├── SKILL.md
    └── scripts/
        └── run_audit.py
```
Place the skill in your OpenClaw skills directory or workspace skills directory, then start a new session so OpenClaw can load it.

---

### Included files

`SKILL.md`

Defines when Sara should be used and how the agent should respond when a risky order is detected.

`scripts/run_audit.py`

Accepts a proposed tool plan as JSON from stdin and returns a local safety audit result as JSON.

`sara_core/engine.py`

Contains the core deterministic auditing logic, action normalization, and hard safety rules.

---

### Expected usage

Sara is most useful when:
- 2 or more skills/tools are involved
- at least one step is destructive, externally visible, or high-impact
- the workflow touches deletion, publishing, payments, booking, permissions, or sensitive data

Sara is usually unnecessary for simple low-risk single-step tasks.

---

### Example risky scenarios Sara can catch
- delete before backup
- publish before preview
- read private data before requesting access
- booking before checking conflicts
- destructive repo actions before safety checks

---

### Product philosophy

Sara is not another noisy orchestration layer.

It is designed to be:

- quiet
- local
- deterministic
- explainable
- helpful only when needed

Most of the time, Sara should stay out of the way.

When it speaks, it should do one thing clearly:

> “This sequence looks risky. Here is the safer order.”

---

### Version

**v0.1 preview**

Current focus:
- high-risk hard rules
- local audit
- multi-skill order safety
- warn-first behavior

Future versions may add:
- richer rule registry
- installed-skill risk scanning
- better conflict explanations
- plugin-level enforcement

---

### License / status

Preview release for OpenClaw users who want a lightweight guardrail for multi-skill workflows.    
