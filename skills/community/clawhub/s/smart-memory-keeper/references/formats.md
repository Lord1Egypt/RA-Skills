# Formats — tasks.md / Journal / MEMORY.md / 3-Part Memory

## tasks.md format

```markdown
# Task State

## In Progress
- [ ] {task name}
  - Status: {one sentence — what step you're on}
  - Next: {specific action; a fresh AI reading this should be able to start without asking}
  - Updated: {YYYY-MM-DD HH:MM}

## Completed (archive)
- [x] {task name} (done: {YYYY-MM-DD})
```

### Quality bar for "Next"

**Too vague (fail):**
```
Next: continue development
Next: fix the bug
Next: test it
```

**Actionable (pass):**
```
Next: run bash run.sh, verify server.py upload fields match expected schema
Next: open scripts/main.py line 390, add show_name check before _upload_results call
Next: update SKILL.md confirmation step with agent_name instructions, republish ClaWHub 1.0.9
```

> Rule: "Next" must include what + where + expected outcome. A context-free AI should be able to start immediately.

---

## Daily Journal template

```markdown
# YYYY-MM-DD

## Today's Work
<!-- Group by topic, not chronological. Skip empty sections. -->

### {topic, e.g. "BenchClaw client", "README rewrite"}
- {what was done and the result}

## Validated Approaches
<!-- Approved directions and working methods — record these too, not just mistakes -->
- **{method/direction}**: {why it works, when to apply}

## Key Decisions
<!-- Only decisions with context and reasoning — skip routine operations -->
- **{decision}**: {why this was chosen}

## Watch List
<!-- Unresolved risks, potential regressions, things to monitor -->
- {risk} → {how to handle or observe}

## Lessons Learned
- {what to do differently next time}
```

> **Writing principles:**
> - Signal over completeness — skip empty sections entirely
> - Group by topic, not time order
> - Watch List is the most important section — unrecorded risks become forgotten risks

### When to write journal entries

| Trigger | What to record |
|---------|----------------|
| User makes a key decision | Decision + reasoning (→ Key Decisions) |
| Problem solved | Problem + solution (→ relevant topic) |
| Unresolved risk found | Risk + plan (→ Watch List) |
| User approves an approach | Method + context (→ Validated Approaches) |
| AI's approach not rejected | Default approval signal — consider recording |
| User says "remember this" | Full content (→ most relevant section) |
| Important config changed | Before/after + reason (→ Key Decisions) |

---

## 3-Part Memory format (Lessons Learned & Validated Approaches)

```
- **Rule**: {do / don't do X}
  **Why**: {reasoning at the time — knowing why enables edge case judgment}
  **When**: {what situation triggers this, effective YYYY-MM-DD}
```

**Example (lesson learned):**
```
- **Rule**: always run git ls-files and show user before pushing
  **Why**: 2026-03-25 pushed personal data to public repo without review, had to delete and recreate
  **When**: before any git push or ClaWHub publish
```

**Example (validated approach):**
```
- **Rule**: don't expose scoring formulas or internal details in public README
  **Why**: user's explicit requirement; competitors could exploit the information
  **When**: writing or editing any BenchClaw public-facing docs, confirmed 2026-04-02
```

> Knowing *why* enables edge case judgment. Rules without reasons get applied blindly.

---

## MEMORY.md Project Index entry format

```markdown
### {project name}
- **Purpose**: {one-sentence description}
- **Local path**: `{absolute path}`
- **Git URL**: {URL or "local only"}
- **Version**: {semver}
- **Last updated**: {YYYY-MM-DD}
- **Notes**: {critical info needed before next operation}
```

Update immediately after: project added/removed, version released, Git remote/path changed.

---

## 3-File Rule — Where does information go?

| Question | File | Example |
|----------|------|---------|
| "What am I working on right now?" | `tasks.md` | "BenchClaw v1.0 — waiting for test results" |
| "What projects exist and where are they?" | `MEMORY.md` | "benchclaw-client: ~/.openclaw/workspace/skills/benchclaw-client, v1.0.0" |
| "What happened today / this week?" | `memory/YYYY-MM-DD.md` | "Rewrote README, pushed to GitHub, fixed unicode warning" |

**Simple rule:**
- tasks.md = **sticky note on your desk** ("don't forget, next step is X")
- MEMORY.md = **filing cabinet** ("where is the BenchClaw repo again?")
- Daily journal = **notebook** ("what did I actually do today?")

> When in doubt: progress or next action → tasks.md. Reference info → MEMORY.md. Record of what happened → journal.
