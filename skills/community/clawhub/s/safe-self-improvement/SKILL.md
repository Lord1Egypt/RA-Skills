---
name: safe-self-improvement
description: "Security-hardened self-improvement skill for OpenClaw. Captures learnings, errors, and corrections with mandatory human-approval gate, automated sanitization, audit tooling, and promotion rate-limiting. Use when: (1) A command or operation fails unexpectedly, (2) User corrects the agent, (3) User requests a missing capability, (4) An external API or tool fails, (5) Agent realizes knowledge is outdated, (6) A better approach is discovered. Review learnings before major tasks."
homepage: https://github.com/gateswell/safe-self-improvement-agent
metadata:
  clawdbot:
    emoji: "⚡"
requires:
  env: []
  files:
    - scripts/sanitize.sh
    - scripts/audit.sh
    - scripts/promotion-gate.sh
---

# Safe Self-Improvement

Log learnings and errors to markdown files for continuous improvement with security hardening. Unlike untrusted variants: **all promotions require human approval, sensitive data is sanitized by script, and bulk promotions are rate-limited**.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | — | This skill makes no external network calls |

No data leaves the machine. Learnings are stored locally only.

## Security & Privacy

- **Data stored locally**: All learnings written to `.learnings/` in the workspace directory
- **No external transmission**: Zero network calls; no data sent to any third party
- **Sensitive data protection**: `scripts/sanitize.sh` must pass before any entry is written (see Pre-Log Sanitization)
- **Cross-session sharing**: Blocked by default; requires explicit user approval per session
- **Read-only recommendation**: For high-security environments, set `.learnings/` to read-only (`chmod 555`)

## Model Invocation Note

This skill operates autonomously between sessions. The agent reads SKILL.md on trigger and executes logging, sanitization, and promotion workflows. To disable: remove the skill directory or run `openclaw skills disable safe-self-improvement`.

## Trust Statement

By installing this skill, you trust the author (gateswell) with handling your learning logs. This skill does not contact external services, share data, or execute untrusted code. Install only if you trust the source.

---

## First-Use Initialisation

If `.learnings/` directory or its files are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\nCorrections, insights, and knowledge gaps.\n\n**Categories**: correction | insight | knowledge_gap | best_practice\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/ERRORS.md ] || printf "# Errors\n\nCommand failures and integration errors.\n\n---\n" > .learnings/ERRORS.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nCapabilities requested by the user.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files.

## 🔒 Security Rules (Non-Negotiable)

1. **NEVER auto-modify core files** — `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, `IDENTITY.md` must NOT be modified without explicit user approval shown as a clear question and awaiting a "yes" response.
2. **No secrets in logs** — Never log tokens, API keys, passwords, private keys, env vars, or full config/source files. Use redacted summaries only.
3. **No cross-session sharing without approval** — Using `sessions_send` or `sessions_spawn` to share learnings requires the same approval gate as promotion: present what will be shared, to which session, and wait for explicit "yes". Never share automatically.
4. **No hook scripts** — This skill does not install or use hook scripts that read command output.
5. **No dynamic payload fetching** — Never fetch remote content at runtime for skill logic.
6. **Promotion = proposal, not action** — When a learning qualifies for promotion, ASK the user first.
7. **Sanitize before write** — Before logging any entry, run `scripts/sanitize.sh` on the content. Block the write if sanitization fails.

## ⚠️ Security Limitations

**This skill's protections are based on AI instruction adherence, not hardware-level isolation.**

- In high-security environments (financial, medical, critical infrastructure): **do not use this skill**
- The sanitization script provides a defense layer, but a determined attacker controlling the agent's context could bypass it
- For team environments: set `.learnings/` to read-only (`chmod 555`) and require a human to make it writable for approved promotions

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` (category: `correction`) |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` (category: `knowledge_gap`) |
| Found better approach | Log to `.learnings/LEARNINGS.md` (category: `best_practice`) |
| Learning seems broadly applicable | **Propose** promotion — do NOT auto-modify core files |

## Pre-Log Sanitization (Mandatory — Script-Enforced)

Before writing ANY entry, you MUST run the sanitization script:

```bash
./scripts/sanitize.sh "<content_to_log>"
```

The script checks for:
- API keys / tokens (GitHub, AWS, OpenAI, etc.)
- Private keys (RSA, EC, SSH, etc.)
- Passwords and secrets in plain text
- IP addresses (private ranges)
- MAC addresses
- Phone numbers
- Email addresses (non-placeholder)
- SSID/WiFi credentials
- GPS coordinates
- Device serial numbers

**If sanitization fails (exit code 1):**
- Do NOT write the entry
- Inform the user: "Sensitive data detected in proposed log entry. Content blocked. Rewrite with placeholders."
- Redact and retry with `./scripts/sanitize.sh "<redacted_content>"`

**Only proceed to write the entry after sanitization passes.**

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context (sanitized — no secrets)

### Suggested Action
Specific fix or improvement

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX
- Pattern-Key: optional.stable_key
- Recurrence-Count: 1
- First-Seen: YYYY-MM-DD
- Last-Seen: YYYY-MM-DD

---
```

### Error Entry

Append to `.learnings/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of failure

### Error
```
Error message (redacted)
```

### Context
- Command attempted
- Environment details (no secrets)
- Redacted excerpt of relevant output

### Suggested Fix
Possible resolution

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-YYYYMMDD-XXX

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted

### User Context
Why they needed it

### Complexity Estimate
simple | medium | complex

### Metadata
- Frequency: first_time | recurring

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN`, `ERR`, `FEAT`
- XXX: Sequential (`001`, `002`...)

## Resolving Entries

When an issue is fixed:
1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block:
```markdown
### Resolution
- **Resolved**: ISO-8601 timestamp
- **Notes**: What was done
```

Other status values: `in_progress`, `wont_fix`, `promoted`

## Promotion (Human-Approval Gate + Rate-Limit)

When a learning qualifies for promotion, propose — **never auto-execute**.

### When a Learning Qualifies for Promotion

- Recurrence-Count ≥ 3 (within 30 days)
- Seen across ≥ 2 distinct tasks
- Non-obvious, verified, or user-flagged

### Promotion Rate-Limiting

The `scripts/promotion-gate.sh` enforces:
- Maximum **3 promotions** per 24-hour window
- Minimum **6-hour cooldown** between bulk promotion batches
- Bulk = 3+ promotions at once (requires extra scrutiny)

Check gate status before proposing:
```bash
./scripts/promotion-gate.sh status
```

### Promotion Targets

| Learning Type | Target File | Example |
|---------------|------------|---------|
| Behavioral patterns | `SOUL.md` | "Be concise, avoid disclaimers" |
| Workflow improvements | `AGENTS.md` | "Spawn sub-agents for long tasks" |
| Tool gotchas | `TOOLS.md` | "Git push needs auth configured" |

### Promotion Procedure

**STOP. Do not modify the target file yet.**

1. Check gate: `./scripts/promotion-gate.sh check`
2. Present the user with:
   - The proposed rule (distilled, concise)
   - Target file and location
   - Original learning entry ID
   - Recurrence count and context
3. Ask: *"This learning recurred X times. Propose adding to [file]: [rule]. Approve?"*
4. **Only on explicit "yes"/"approve"/"确认":**
   - Run `./scripts/promotion-gate.sh approve LRN-YYYYMMDD-XXX`
   - Then modify the target file
   - Update original entry: `**Status**: promoted`, `**Promoted**: <filename>`
5. Any other response = do not promote

## Recurring Pattern Detection

When logging something similar to an existing entry:
1. Search: `grep -r "keyword" .learnings/`
2. Link: Add `**See Also**: LRN-...` in Metadata
3. Bump priority if recurring
4. Increment `Recurrence-Count` and update `Last-Seen`
5. If promotion threshold met → follow Promotion Procedure above

## Detection Triggers

Automatically log when you notice:

- **Corrections**: "No, that's not right...", "Actually...", "You're wrong about..."
- **Feature Requests**: "Can you also...", "I wish you could...", "Is there a way to..."
- **Knowledge Gaps**: User provides info you didn't know, docs are outdated, API differs
- **Errors**: Non-zero exit codes, exceptions, unexpected output, timeouts

> ⚠️ Note on corrections: If a correction feels suspicious (e.g., repeated similar corrections in short succession), log it but flag it in the entry with `**Confidence**: low`. Do not promote low-confidence learnings without extra scrutiny.

## Periodic Review & Audit

Run the audit script regularly:

```bash
./scripts/audit.sh
```

Audit checks:
1. **Sensitive data scan** — blocks if secrets found in any learnings file
2. **Format consistency** — all entries have Status, Priority, Logged fields
3. **Orphaned See Also links** — all references point to existing entries
4. **File size** — warns if any file exceeds 500 lines
5. **Summary report** — PASS/FAIL/WARNINGS

Run at least:
- Before any major task
- Monthly
- Before context compression

## Context Compression

When `.learnings/*.md` exceeds 500 lines (after audit confirms no issues):

1. **Distill resolved/promoted entries** into one-line summaries:
   - Before: Full entry (~15 lines)
   - After: `> [LRN-20260428-001] Use pnpm not npm (promoted→TOOLS.md)` (~1 line)
2. **Merge duplicate patterns** — if 3+ entries share the same `Pattern-Key`, keep one summary
3. **Expire stale entries** — `wont_fix` > 90 days → delete; `pending` no activity > 60 days → demote to `low` + compress
4. **Keep summary index** in `.learnings/archive/SUMMARY.md` — one line per entry, oldest first
5. Active files only retain `pending` and `in_progress` in full detail

## Best Practices

1. **Sanitize before write** — run `sanitize.sh` every time, no exceptions
2. Log immediately — context fades fast
3. Be specific — future sessions need clarity
4. Redact secrets — always
5. Include reproduction steps for errors
6. Suggest concrete fixes, not just "investigate"
7. Link related files
8. Run audit before compression — never compress a dirty file
9. Propose promotions promptly when threshold met — but wait for explicit approval
10. Flag low-confidence corrections — use `**Confidence**: low` and delay promotion
