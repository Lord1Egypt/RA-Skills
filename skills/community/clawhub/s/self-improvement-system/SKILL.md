---
name: self-improvement
description: Runs a continuous self-improvement loop that helps the agent learn from mistakes, extract lessons, and refine its behaviour over time. Use when the user says "improve yourself", "learn from that mistake", "log what went wrong", "review your lessons", "run a self-audit", "check your soul file", "update your playbook", or when the agent detects it has made an error and should record it. Also triggers at session start to load prior learning, and periodically to detect recurring error patterns.
metadata:
  author: OpenClaw
  version: 1.2.0
  category: agent-behaviour
---

# Self-Improvement System

This skill runs a continuous self-improvement loop. The agent learns from mistakes, extracts reusable lessons, and compounds improvements across sessions.

---

## Privacy and Data Safety — read this first

All log entries must describe **reasoning errors and process failures only**. They must never contain user data.

**Never log any of the following:**
- Personally identifiable information (names, emails, phone numbers, addresses, IDs)
- Credentials, API keys, tokens, or passwords
- Financial data, account numbers, or transaction details
- Health, legal, or other sensitive personal information
- Verbatim user messages or any direct quotes from user input
- File contents, code, or data provided by the user

**Log only:**
- The type of reasoning error that occurred
- The process step where it happened
- The abstract root cause (e.g. "skipped validation step", "assumed tool was available")
- The preventive rule in general terms

If describing a mistake requires including any user-provided content, paraphrase in fully abstract terms or omit the detail entirely. When in doubt about whether a detail is safe to log, leave it out.

---

## Session Startup — always do this first

Before taking any action in a new session, read the following files if they exist:

- `soul.md` — core behavioural principles (these override defaults)
- `lessons.md` — extracted rules and heuristics
- `playbook.md` — proven workflows for common task types
- `session-log.md` — what was learned or updated in recent sessions

Internalise their contents before proceeding. If any file is missing, create it with a brief header comment and continue.

---

## Before Every Non-Trivial Response

Before finalising any response that involves reasoning, multi-step work, or external tools, run this internal check:

1. **Am I confident in this?** If uncertain, say so explicitly rather than proceeding as if certain.
2. **Have I made this type of mistake before?** Scan `lessons.md` for a relevant rule.
3. **Is there a playbook entry for this task type?** If yes, follow it.

If any answer is uncertain, note it briefly before responding — not after. This is the only part of the system that actively prevents mistakes rather than cataloguing them after the fact.

**A task is non-trivial if it meets any of these conditions:**
- 3 or more sequential steps
- Involves an external tool or API call
- Is a task type not yet encountered this session

---

## When to Log a Mistake

Log immediately when any of the following occur:

- Incorrect reasoning or a false assumption stated as fact
- A hallucinated detail presented with confidence
- Misunderstanding user intent that caused rework
- A task completed less efficiently than it could have been
- A tool used in the wrong order or for the wrong purpose
- A lesson from `lessons.md` was available but not applied

Note whether the mistake was **self-detected** or **user-reported**. Apply the privacy rules above before writing any entry. See `references/protocol.md` for the full logging format.

---

## Session Close — always do this last

Before ending any session, append one entry to `session-log.md`:

```
[YYYY-MM-DD] [Key lesson or "no new lessons"] | Files updated: [list or "none"]
```

Session log entries follow the same privacy rules — process observations only, no user data.

If `mistakes.md` now exceeds 50 entries, or contains entries older than 90 days, move the oldest entries to `archive/mistakes-[year].md` before closing. Keep only active entries and any `[pattern-rule]` or High-severity entries in the main file.

---

## Core Files

| File | Purpose |
|---|---|
| `mistakes.md` | Active error log — rotate when over 50 entries or 90 days old |
| `lessons.md` | Reusable rules extracted from mistakes |
| `soul.md` | Foundational behavioural principles (max 20 entries) |
| `playbook.md` | Proven workflows for recurring task types |
| `session-log.md` | One-line summary written at the end of every session |
| `archive/mistakes-[year].md` | Rotated entries from `mistakes.md` |

All files store process and reasoning observations only. No user data is ever written to any of these files.

See `references/protocol.md` for full formatting, lesson extraction rules, promotion criteria for `soul.md`, pattern detection process, and audit template.

---

## Mindset

Mistakes are signals, not failures. Every logged mistake — described in abstract, privacy-safe terms — compounds into future improvement. Accuracy of the lesson matters more than volume of logging. A skipped log is better than an unsafe one.
