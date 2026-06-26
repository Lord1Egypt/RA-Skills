---
name: skill-safety-scanner
description: Scan your installed ClawHub skills for dangerous code patterns — credential harvesting, shell injection, unauthorized network calls, and known malicious signatures. Produces a per-skill safety report with SAFE/WARN/DANGEROUS ratings and one-command removal instructions. Use when you want to audit skills before trusting them, after installing new skills, or after the ClawHub security incident. No data leaves your machine.
---

# Skill Safety Scanner

Scans every installed skill in your OpenClaw workspace for dangerous code patterns.
Produces a per-skill SAFE / WARN / DANGEROUS rating with exact evidence and removal commands.

**Why this exists:** ~20% of ClawHub skills have been flagged for malicious patterns including
credential harvesting, shell injection, and C2 callbacks. This skill surfaces those issues
before they can cause damage — using OpenClaw's own built-in scanner, not a third party.

**Privacy guarantee:** Runs entirely on your machine. Zero network calls. Zero data exfiltration.
You can read every line of this skill — it is a single SKILL.md file.

---

## How it works

This skill uses `openclaw security audit --deep --json` which already scans all installed skills
for dangerous patterns. It then parses, formats, and explains the findings per-skill.

No new scanning code. No dependencies. Just OpenClaw's own trusted scanner with better output.

---

## Workflow

### 1. Run the scanner

```bash
openclaw security audit --deep --json
```

Capture the full JSON output.

### 2. Extract skill findings

From the JSON, find all entries where `id` starts with `skills.` — these are skill-specific findings.

Key finding IDs to look for:

| Finding ID | Meaning |
|------------|---------|
| `skills.code_safety` | Dangerous patterns detected in skill code |
| `skills.untrusted_exec` | Skill executes shell commands |
| `skills.env_harvesting` | Skill reads env vars AND makes network calls |
| `skills.network_exfil` | Skill sends data to external hosts |
| `skills.permission_escalation` | Skill requests elevated permissions |

### 3. Rate each skill

For each installed skill, assign a rating:

| Rating | Criteria |
|--------|----------|
| ✅ SAFE | No dangerous patterns found |
| ⚠️ WARN | Shell exec OR env access (not combined) — review source |
| 🔴 DANGEROUS | Env harvesting + network send combined, or known malicious signature |

### 4. Format the report

```
SKILL SAFETY SCAN — YYYY-MM-DD HH:MM
Scanned: X skills   Safe: X   Warn: X   Dangerous: X

──────────────────────────────────────
🔴 DANGEROUS — [skill-name]
   Path: ~/.openclaw/workspace/skills/[skill-name]
   Issue: [env-harvesting] Reads API keys and sends to external host
   Evidence: [filename]:[line] — [code snippet]
   Action: clawhub uninstall [skill-name]
           rm -rf ~/.openclaw/workspace/skills/[skill-name]

⚠️  WARN — [skill-name]
   Path: ~/.openclaw/workspace/skills/[skill-name]
   Issue: [dangerous-exec] Executes shell commands via child_process
   Evidence: [filename]:[line]
   Action: Review source before use. Remove if not needed:
           clawhub uninstall [skill-name]

✅ SAFE — [skill-name]   (no findings)
──────────────────────────────────────

RECOMMENDATION
[If any DANGEROUS skills]: Remove immediately — treat as compromised.
[If any WARN skills]: Review source at the path above before next use.
[If all SAFE]: Your skill set is clean. Re-scan after any new install.
```

### 5. Optional: Auto-remove dangerous skills

If the user confirms, execute removal for DANGEROUS-rated skills:

```bash
# For each DANGEROUS skill named [skill-name]:
clawhub uninstall [skill-name] 2>/dev/null
rm -rf ~/.openclaw/workspace/skills/[skill-name]
```

Always show the command and ask for confirmation before removing anything.

### 6. Re-scan to confirm

After any removals:

```bash
openclaw security audit --deep
```

Confirm the `skills.code_safety` finding is gone.

---

## Scheduling

To scan automatically after every new skill install, or on a daily schedule:

```bash
openclaw cron add --name "skill-safety-scanner:daily" --cron "0 3 * * *" \
  --prompt "Run the skill-safety-scanner skill and report findings to memory."
```

---

## What this skill does NOT do

- Does not send any data to external servers
- Does not modify any files without explicit confirmation
- Does not connect to the internet
- Does not access credentials or API keys
- Does not install anything
- Single SKILL.md file — inspect the full source above

---

## Notes

- Run this scan after every new ClawHub skill install
- WARN ratings are not always malicious — many legitimate skills use shell exec (e.g., tools that run git or npm). Review the source and make your own judgment.
- DANGEROUS = env harvesting + network send in the same file. This combination has no legitimate use case in a passive skill.
- If OpenClaw updates its scanner signatures, re-run this skill to catch newly detected patterns.
