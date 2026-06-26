---
name: Skills Audit
version: 1.5.3
description: Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity).
---

# Skills Audit (skills-audit)

A security-oriented skill for managing OpenClaw skills safely. This package includes executable Python scripts (not instructions-only), with six core capabilities:

1) **Threat scanning** (static analysis)
2) **Append-only audit logs** (local NDJSON)
3) **Skills monitoring & notifications** (push alerts on changes)
4) **File-level diff + content diff** (git snapshots)
5) **Baseline approval mechanism** (approved skills don't repeat-alert)
6) **Semantic analysis** (dangerous functions + capability analysis)

> This skill performs **static analysis of audited skills** — it does **not execute the code of the audited skill itself**. However, the audit tool does execute **local trusted commands/subprocesses** such as `git`, Python helper scripts, and controlled local process calls needed for snapshotting, diffing, and notification generation.

---

## Requirements

- **Python ≥ 3.9**, standard library only (no third-party dependencies)
- **git** (required for content diff snapshots and local repository history)
- A normal local shell/process environment for controlled subprocess execution used by the audit tool itself
- See `scripts/requirements.txt` for details

---

## Core Capabilities

### 1) Threat Scanning (Static Risk Analysis)

`skills_audit.py` performs static inspection of installed skill directories. If a QianXin token is configured, it also queries QianXin SafeSkill by the **stable MD5 of the whole `workspace/skills` bundle** instead of uploading the bundle itself:

- **Network indicators**: URLs/domains, `curl/wget/requests` usage
- **Dangerous commands**: `curl|sh`, `wget|bash`, `eval`, dynamic exec, base64 pipes
- **Suspicious behavior**: persistence (cron/systemd), sensitive paths (`~/.ssh`, `~/.aws`, `/etc`)
- **Optional QianXin intel**: stable MD5 lookup for the full `workspace/skills` bundle using a user-supplied token

Output fields:
- `risk.level`: `low | medium | high | extreme`
- `risk.decision`: `allow | allow_with_caution | require_sandbox | deny`
- `risk.risk_signals[]`: evidence (file + snippet)
- `risk.network.domains[]`: extracted domains
- `risk.source`: `local` or `qianxin-md5`

QianXin config:
- Config file: `config/intelligent.json`
- Defaults to `enabled: false`
- `token` defaults to empty
- Users can enable it after download by filling in their own token and setting `enabled` to `true`
- If disabled, token is empty, or the query fails, the scan automatically falls back to local static analysis

### 2) Audit Logging (Append-only NDJSON)

All detections are appended as NDJSON to:
- `~/.openclaw/skills-audit/logs.ndjson`

State snapshot for diff:
- `~/.openclaw/skills-audit/state.json`

Schema defined by `log-template.json`. Key points:
- `sha256`: SHA-256 of SKILL.md (integrity field)
- `diff`: git commit info + per-file stat
- `file_changes`: file-level added/removed/changed lists
- `approved`: baseline approval status

### 3) Skills Monitoring & Push Notifications

Periodic monitoring of `workspace/skills` for additions, changes, and removals.

- No changes → no output
- Changes detected → one notification
- Baseline-approved unchanged skills are excluded from notifications

Notification template: `templates/notify.txt` (see `templates/README.md` for customization).

### 4) File-level Diff + Content Diff (Git Snapshots)

Each scan snapshots the skills directory into a local git repo (`~/.openclaw/skills-audit/snapshots/`):

- Each scan = one git commit
- Change detection via `git diff HEAD~1 HEAD`
- Notifications include per-file change summaries (+N -N lines)

Tiered display:
- ≤ 5 changed files: show all with +N -N
- 6–20: first 3 + "X more omitted"
- \> 20: first 3 + omitted + ⚠️ large-scale change warning
- \> 8 skills changed: high-risk expanded, low-risk compressed

View full diff:
```bash
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD
git -C ~/.openclaw/skills-audit/snapshots diff HEAD~1 HEAD -- skills/<skill-name>/
git -C ~/.openclaw/skills-audit/snapshots log --oneline
```

### 6) Semantic Analysis (Dangerous Functions + Capability Analysis)

Each scan now also produces a `semantic_analysis` field in the audit log:

- **Dangerous function analysis**: detects patterns such as `eval`, `exec`, `os.system`, `subprocess` with `shell=True`, `curl|sh`, and `wget|bash`
- **Capability analysis**: infers whether the skill has network, filesystem, process execution, cron/scheduler, git, or config-handling capabilities
- **Combined result**: evaluates execution-capability risk and malicious-intent risk separately, with semantic intent as the primary decision dimension, then emits `level / decision / reason`

Notes:
- The current implementation is a **local LLM-style heuristic analysis**, with no external model dependency
- This is a **mandatory rule**: every added or changed skill must go through semantic analysis during `skills_audit.py scan`
- If `semantic_analysis` is missing or cannot produce a result, the scan should fail instead of silently skipping it
- To reduce self-audit false positives, low-signal files such as rule configs, log templates, skill docs, and `config/semantic-patterns.json` are excluded from high-weight dangerous-function scoring
- Risk-rule scanning now distinguishes hit contexts: `real_execution / rule_sample / doc_example / config_sample`
- For `skills_audit.py` itself, semantic detection and risk scanning both prioritize real execution paths instead of treating the pattern-string tables as dangerous execution by default
- Semantic analysis now separates execution capability from malicious intent, so normal engineering capabilities do not automatically imply a hostile result
- Controlled local calls such as `subprocess.run([...], shell=False)` with fixed argv are treated as engineering capability rather than automatic malicious intent
- The field is designed to be forward-compatible with a real LLM-backed semantic scanner later

### 5) Baseline Approval Mechanism

Manage approved skills via `~/.openclaw/skills-audit/baseline.json`:

- Approved skills (matching tree_sha256) won't trigger repeated alerts
- Any file change automatically breaks approval → re-triggers risk detection

```bash
python3 {baseDir}/scripts/skills_audit.py approve --skill weather --workspace <workspace>
python3 {baseDir}/scripts/skills_audit.py approve --all --workspace <workspace>
python3 {baseDir}/scripts/skills_audit.py baseline --list
python3 {baseDir}/scripts/skills_audit.py baseline --revoke --skill weather
```

---

## Initialization and Manual Monitoring Setup (Agent Directive)

When the Agent first loads this skill, it may perform **local initialization**, but it must **not automatically create cron jobs**. Instead, it should guide the user to create monitoring explicitly:

1. Check if `~/.openclaw/skills-audit/state.json` exists
2. If not, run initialization:
   ```bash
   python3 {baseDir}/scripts/skills_audit.py init --workspace <workspace>
   ```
3. Check if a `skills-audit-watch` cron job already exists (`openclaw cron list`)
4. If not:
   - **Do not auto-create cron**
   - Tell the user they can create it manually
   - Provide a suggested command example (to be executed by the user, or only after explicit user approval):
   ```bash
   openclaw cron add \
     --name "skills-audit-watch" \
     --cron "*/1 * * * *" \
     --tz "Asia/Shanghai" \
     --session isolated \
     --message "python3 {baseDir}/scripts/skills_watch_and_notify.py --workspace <workspace>" \
     --announce \
     --channel <current_channel> \
     --to <current_user_id>
   ```
5. Remind the user to verify the push target before enabling it, especially if raw diffs or large change details may be sent externally
6. **Do not default to pushing large raw diffs to external channels**; prefer a concise summary first, with details on demand

> **Design principle**: `skills-audit` handles scanning, logging, and notification text generation. Scheduling and delivery should be user-directed rather than auto-created by default.

---

## Viewing Change Details (Agent Mandatory Flow)

> ⚠️ **Mandatory rule**: When a user asks about skill change details, the Agent **MUST** use the `show` command to obtain structured change data. By default, it should provide a **safe summary first**, rather than sending the full raw diff externally.

**Trigger phrases** (user may say):
- "what changed" / "show diff" / "what's different" / "change details"
- "具体改了什么" / "哪里变了" / "看一下变更"
- Any request for diff / change / modification details

**Fixed execution flow (cannot be skipped)**:

1. If user mentions a specific skill:
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show --skill <skill-name>
   ```
2. If no specific skill mentioned:
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show
   ```
3. By default, send only a **safe summary** derived from `show` output (files changed, line counts, major change points), to avoid externally exposing sensitive diff content
4. Only when the user **explicitly asks for raw/full content** should the full `show` output be sent, and the user should be warned that sensitive information may appear in diffs
5. For older history, use `--commit-range`:
   ```bash
   python3 {baseDir}/scripts/skills_audit.py show --commit-range HEAD~3..HEAD~2
   ```

**Prohibited behaviors**:
- ❌ Running `git diff` and bypassing the structured `show` output path
- ❌ Defaulting to send raw full diff content to external channels without warning
- ❌ Automatically pushing large raw change content to external channels
- ✅ Prefer a safe summary based on `show`; provide full raw content only on explicit request

---

## Manual Usage

### Initialize

```bash
python3 {baseDir}/scripts/skills_audit.py init --workspace /root/.openclaw/workspace
```

### Manual Scan

```bash
python3 {baseDir}/scripts/skills_audit.py scan --workspace /root/.openclaw/workspace --who user --channel local
```

### Local Notification Test

```bash
python3 {baseDir}/scripts/skills_watch_and_notify.py --workspace /root/.openclaw/workspace
```

---

## Safety Notes

- Static analysis only: never execute unknown skill code during audit.
- When `risk.level` is `high`/`extreme`, require human review or sandbox.
- Prefer OpenClaw `cron add` / `cron edit` for scheduling.
- Integrity checks use **SHA-256**.
