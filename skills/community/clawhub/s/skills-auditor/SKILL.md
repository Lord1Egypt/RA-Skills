---
name: skills-auditor
version: 1.0.3
description: Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity). Requires Python ≥3.9 and git.
---

# Skill Auditor

A security-oriented skill for managing OpenClaw skills safely. This package includes executable Python scripts (not instructions-only), with six core capabilities:

1) **Threat scanning** (static analysis)
2) **Append-only audit logs** (local NDJSON)
3) **Skills monitoring & notifications** (push alerts on changes)
4) **File-level diff + content diff** (git snapshots)
5) **Baseline approval mechanism** (approved skills don't repeat-alert)
6) **Semantic analysis** (built-in rule engine + Agent LLM deep analysis)

> This skill performs **static analysis of audited skills** — it does **not execute the code of the audited skill itself**. The audit tool executes **local trusted commands/subprocesses** such as `git`, Python helper scripts, and controlled local process calls needed for snapshotting, diffing, and notification generation.
>
> **Scope of this skill**: The included Python scripts perform file reading, git operations, regex-based scanning, and local log writing. **The scripts themselves do not contain any network or HTTP client code.**
>
> **Semantic analysis** is performed by the **hosting Agent** as part of the audit workflow. This is an **Agent-level capability**, not a script-level operation — the Agent reads code context and applies its language model to assess risk. Data handling during semantic analysis is governed by the Agent's own deployment configuration and security policies, which is outside the scope of this skill package.

---

## Requirements

- **Python ≥ 3.9**, standard library only (no third-party dependencies)
- **git** (required for content diff snapshots and local repository history)
- A normal local shell/process environment for controlled subprocess execution used by the audit tool itself
- See `scripts/requirements.txt` for details

---

## Core Capabilities

### 1) Threat Scanning (Static Risk Analysis)

`skills_audit.py` performs static inspection of installed skill directories:

Output fields:
- `risk.level`: `low | medium | high | extreme`
- `risk.decision`: `allow | allow_with_caution | require_sandbox | deny`
- `risk.risk_signals[]`: evidence (file + snippet)
- `risk.network.domains[]`: extracted domains
- `risk.source`: `local`

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

### 6) Semantic Analysis (Dangerous Functions + Capability Analysis)

Semantic analysis operates in **two layers**:

1. **Built-in rule engine** (script-level): The `semantic_analyze_skill()` function in `skills_audit.py` performs regex pattern matching, keyword scoring, and context-aware weighting. This is a pure local Python function — **no network access, no model dependency**.

2. **Agent semantic understanding** (Agent-level): The hosting Agent applies its language model to perform deeper code comprehension — identifying obfuscated patterns, indirect calls, and contextual risk that pure regex cannot catch. **This is an Agent-level capability; its data handling is governed by the Agent's deployment configuration and security policies, not by this skill package.**

The combined result is written to the `semantic_analysis` field in the audit log, covering:

- **Dangerous function analysis**: identifies risky patterns such as `eval`, `exec`, `os.system`, `subprocess` with `shell=True`, `curl|sh`, `wget|bash` — evaluating whether usage is benign (documentation examples, rule-table entries) or genuinely dangerous
- **Capability analysis**: determines whether the skill possesses network access, filesystem modification, process execution, cron/scheduler, git operations, or config-handling capabilities
- **Combined result**: evaluates execution-capability risk and malicious-intent risk as separate dimensions, using semantic intent as the primary decision axis, then emits `level / decision / reason`

**Mandatory rules:**
- Every scan must execute semantic analysis (both layers) — this step cannot be skipped or disabled
- If `semantic_analysis` is missing or empty in the scan result, the scan **must fail** rather than silently proceeding without it

**Responsibility boundary:**
- **This skill package** (scripts + configs): performs local file I/O, git operations, regex scanning, and NDJSON logging. The scripts contain **no HTTP client code, no network libraries, and no model API calls**
- **The hosting Agent**: responsible for model invocation during semantic understanding. How the Agent handles data (local model, private API, cloud API) is determined by the Agent's own deployment — organizations should configure their Agent's data policies accordingly
- Pattern definitions are loaded from `config/semantic-patterns.json` (editable, no code changes needed)

**Analysis context awareness:**
- Distinguishes hit contexts: `real_execution / rule_sample / doc_example / config_sample`
- Low-signal files (rule configs, log templates, skill docs, `config/semantic-patterns.json`) are deprioritized in dangerous-function scoring
- For audit tools themselves (e.g., `skills_audit.py`), analysis prioritizes real execution paths and does not treat pattern-string tables as dangerous execution
- Execution capability is separated from malicious intent — normal engineering capabilities (e.g., `subprocess.run([...], shell=False)` with fixed argv) do not automatically imply hostile intent
- Results are stored as an independent field in the audit log for future enhancements and frontend visualization

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

## Resource Usage (Stability Test)

This skill is lightweight and does not consume significant CPU or memory. Below are benchmark results on a **2-core / 4 GB** host, comparing a 60-second idle baseline with the skill running in a relatively silent state:

| Metric | Idle Baseline | With skills-audit | Increment |
|---|---|---|---|
| CPU avg | 10.20 % | 22.79 % | +12.59 % |
| Memory avg | 48.95 % | 59.01 % | +10.06 % |
| CPU max | 80.00 % | 97.51 % | +17.51 % |
| Memory max | 58.59 % | 72.28 % | +13.69 % |

> The skill adds only ~12 % CPU and ~10 % memory on average. Peak spikes occur during git snapshot commits and are transient.

---

## Safety Notes

- Static analysis only: never execute unknown skill code during audit.
- When `risk.level` is `high`/`extreme`, require human review or sandbox.
- Prefer OpenClaw `cron add` / `cron edit` for scheduling.
- Integrity checks use **SHA-256**.
