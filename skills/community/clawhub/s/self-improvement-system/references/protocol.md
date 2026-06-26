# Self-Improvement Protocol Reference

This file contains the full operational detail for the self-improvement system. Consult it when logging a mistake, extracting a lesson, running an audit, or updating the playbook.

---

## Privacy Rules — apply before every write operation

All entries in all files must describe **reasoning errors and process failures only**. Before writing anything, verify that the entry contains none of the following:

- Personally identifiable information (names, emails, phone numbers, addresses, IDs)
- Credentials, API keys, tokens, or passwords
- Financial data, account numbers, or transaction details
- Health, legal, or other sensitive personal information
- Verbatim user messages or direct quotes from user input
- File contents, code, or data provided by the user

If describing a mistake requires any of the above, paraphrase at the most abstract level possible, or omit the detail. The entry should describe the class of error, not the specific content that triggered it.

**Examples of safe vs unsafe logging:**

| Unsafe | Safe |
|---|---|
| "Told user their password was 'abc123'" | "Stated user credential incorrectly" |
| "Hallucinated that John Smith's order was $240" | "Hallucinated a specific financial figure with false confidence" |
| "Misread the CSV the user uploaded" | "Misread the structure of a user-provided data file" |

When uncertain whether a detail is safe to include, leave it out entirely.

---

## 1. Error Logging (`mistakes.md`)

Use this exact format for every entry:

```
## [YYYY-MM-DD] [Short title — abstract, no user data]

**What happened:** [Plain description of the reasoning or process error]
**Root cause:** [Why it happened — overconfidence, missing context, wrong tool, skipped step, etc.]
**Severity:** Low / Medium / High
**Source:** self-detected | user-reported
**Preventive rule:** [One concrete sentence starting with "Always", "Never", or "Before X, do Y"]
```

**Severity guide:**
- High — caused incorrect output delivered to user, or required significant rework
- Medium — caused inefficiency, partial failure, or a near-miss the agent caught itself
- Low — minor inefficiency or edge case with minimal impact

**Source field:**
- `self-detected` — the agent caught the mistake before or during delivery
- `user-reported` — the user pointed it out after the fact

User-reported mistakes indicate the pre-response check failed. If user-reported mistakes outnumber self-detected ones at audit time, the check itself needs reinforcing in `soul.md`.

Do not skip logging because a mistake feels minor. Patterns emerge from small errors. But accuracy and privacy safety matter more than volume — a skipped entry is better than an unsafe one.

---

## 2. Lesson Extraction (`lessons.md`)

After logging a mistake, ask: *is this lesson reusable across different tasks?*

If yes, add it to `lessons.md` immediately using this format:

```
## [Short rule title]

**Rule:** [One clear, actionable sentence — no user data]
**Source:** [Brief abstract reference — e.g. "2025-06-01: Wrong tool order in data task"]
**Added:** [Date]
**Tag:** standard | pattern-rule
```

Review `lessons.md` before finalising any response or starting any multi-step task. Apply relevant rules actively — not as background noise.

---

## 3. Core Principles (`soul.md`)

Promote a lesson to `soul.md` only when it meets all three criteria:

1. It applies across many different task types
2. Violating it has caused or would cause a Medium or High severity mistake
3. It reflects a reasoning principle, not a situational tactic

Format each entry as a numbered principle with one sentence of rationale:

```
1. [Principle statement] — [One sentence explaining why this matters]
```

Keep `soul.md` short. If it grows beyond 20 principles, audit and consolidate before adding more. A bloated `soul.md` gets ignored; a tight one gets applied.

---

## 4. Pattern Detection

Run pattern detection in either of these conditions:
- Every 10 mistakes logged
- When explicitly asked to review patterns

Process:
1. Read all entries in `mistakes.md`
2. Group by root cause
3. If 3 or more mistakes share the same root cause, write a higher-order rule that prevents the entire class
4. Add it to `lessons.md` with the tag `pattern-rule`
5. Evaluate whether it meets the criteria for promotion to `soul.md`

Also check the Source field split. If user-reported mistakes represent more than 40% of logged entries, add or strengthen a `soul.md` principle about the pre-response uncertainty check.

---

## 5. Workflow Optimisation (`playbook.md`)

**What qualifies as a non-trivial task:**
- 3 or more sequential steps
- Involves an external tool or API call
- A task type not yet encountered this session

Document a workflow when you complete a task significantly better than before, or discover a faster and more reliable method.

Format:

```
## [Workflow name]

**Use when:** [Task type or trigger condition — specific enough that matching is unambiguous]
**Steps:**
1. [Step one]
2. [Step two]
3. ...
**Why it works:** [One sentence]
**Last validated:** [Date]
```

Consult `playbook.md` before starting any non-trivial task. Do not reinvent workflows already proven to work.

---

## 6. Session Log (`session-log.md`)

Append one line at the end of every session, no exceptions. Apply the same privacy rules — process observations only.

```
[YYYY-MM-DD] [Key lesson learned, or "no new lessons"] | Files updated: [comma-separated list, or "none"]
```

Examples:
```
2025-06-01 Always confirm tool availability before multi-step task | Files updated: mistakes.md, lessons.md
2025-06-02 No new lessons | Files updated: none
2025-06-03 Promoted "verify before executing" to soul.md | Files updated: mistakes.md, lessons.md, soul.md
```

The session log lets the next session quickly scan what changed recently without re-reading every file in full.

---

## 7. Archiving (`archive/mistakes-[year].md`)

At session close, check `mistakes.md`:

- If it contains more than 50 entries, move the oldest entries to `archive/mistakes-[year].md` until 40 remain
- If it contains entries older than 90 days, move those regardless of total count

**Always keep in the active file regardless of age:**
- Any entry tagged `pattern-rule`
- Any entry with Severity: High
- The most recent 10 entries

Create the archive directory if it does not exist. Name files by year: `archive/mistakes-2025.md`, `archive/mistakes-2026.md`, etc. Archived entries carry the same privacy standards as active ones.

---

## 8. Self-Audit Template

Run an audit every 10 sessions, or when explicitly asked. Write it as an entry in `mistakes.md` under the heading `[AUDIT]`.

```
## [AUDIT] [Date]

**Mistakes logged since last audit:** [Count]
**Self-detected vs user-reported split:** [e.g. "7 self / 3 user"]
**Most common root cause:** [Description]
**Lessons repeatedly violated:** [List any, or "none"]
**soul.md entries added:** [Count]
**Archive action taken:** [Moved X entries / "none needed"]
**Privacy check:** [Any entries flagged and redacted? Yes/No]
**One concrete improvement before next audit:** [Specific action]
```

---

## Troubleshooting

**Files don't exist at session start**
Create each missing file with a brief header and continue. Do not halt the session.

```
# mistakes.md
Active error log. Process observations only — no user data. Rotate to archive/ when over 50 entries or 90 days old.

# lessons.md
Reusable rules extracted from mistakes. Process observations only — no user data.

# soul.md
Core behavioural principles. Max 20 entries.

# playbook.md
Proven workflows for recurring task types.

# session-log.md
One-line summary per session. Process observations only — no user data.
```

**Unsure whether something qualifies as a mistake**
If you caught yourself mid-task and corrected course — log it as Low severity, source: self-detected. The value is in the pattern, not the individual incident. But if logging it safely would require omitting all meaningful detail, skip the entry.

**Unsure whether a detail is safe to log**
Leave it out. Describe the error at the most abstract level possible — the class of mistake, not the specific content.

**soul.md is getting long**
Before adding any new principle, review existing ones. Consolidate overlapping principles. A tight `soul.md` is more effective than a comprehensive one.

**User-reported mistakes are the majority**
This means the pre-response uncertainty check is not being applied. Add a High-priority principle to `soul.md` explicitly about running the check before non-trivial responses.
