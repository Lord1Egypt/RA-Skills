---
name: update-advisor
description: >
  OpenClaw update check and upgrade assistant. Triggers on phrases like
  "check for updates", "any new version", "is openclaw updated", "run the update",
  "confirm update", "upgrade openclaw".
  Two modes: (1) Check mode — analyze changelog, risk assessment, recommendation;
  (2) Execute mode — perform update with explicit, pre-update recovery watchdog protection (macOS launchd or Linux systemd).
metadata:
  openclaw:
    requires:
      bins: ["openclaw", "python3", "npm"]
---

# update-advisor

Helps you safely check for and apply OpenClaw updates, with changelog analysis, risk rating, and a Gateway-independent recovery watchdog path for Execute mode (macOS launchd or Linux systemd).

## Requirements and security disclosure

- `openclaw` — the CLI being updated
- `npm` — fallback for `npm view openclaw version` when OpenClaw update metadata is unavailable
- `python3` — used by the changelog parsing scripts and arming helper
- Execute recovery arming requires macOS `launchctl` + `plutil`, or Linux `systemd-run` + `systemctl --user`

Security boundaries:
- Check mode is read/report only. It runs local version/changelog/doctor checks and does not modify OpenClaw state.
- The only routine network lookup is `npm view openclaw version` when OpenClaw's own update metadata is unavailable.
- MEMORY.md is optional read-only context. Use already-loaded session context when available; read `MEMORY.md` only after the user explicitly asks for personalized relevance analysis or consents to that read. Never write to `MEMORY.md` during Check mode.
- Execute mode has persistent side effects (`openclaw update` and a temporary user-level launchd/systemd recovery job). Start it only after explicit user confirmation and after the dry-run/ownership/watchdog gates pass.
- The watchdog writes temporary state/log files under the selected state directory and must be cleaned up after recovery. It does not read secrets or send data to third-party endpoints.

## Implementation architecture

This skill has two distinct implementation layers:

- **Check mode** is implemented by bundled shell/Python scripts (`scripts/check-update.sh`, `parse_changelog.py`, `assemble_result.py`). These are the only files the agent executes directly. They run locally, make no network calls beyond `npm view openclaw version`, and produce structured JSON output.

- **Execute mode (v2, preferred)** uses an external, mock-tested watchdog script (`scripts/recovery-watchdog.sh`) launched before `openclaw update`, so recovery does not depend on Gateway/cron/session survival. The arming helper supports macOS launchd and Linux systemd user units; unsupported OS/backend combinations must stop before update. The launchd plist template is inert documentation; the helper renders per-run jobs.

- **Optional MEMORY.md access** in Check mode is read-only and scoped to annotating changelog relevance against the user's known configuration (channels, installed Skills, cron jobs). Prefer already-loaded session context. Read `MEMORY.md` only when the user explicitly asks for personalized relevance analysis or consents to that read. Check mode never writes to `MEMORY.md`; any logging happens only after Execute mode and only at the user's explicit request.

All actions that have persistent side effects (`openclaw update`, watchdog launch/job registration) require explicit user confirmation via the trigger detection flow before the agent proceeds.

## Resolving the skill directory

This skill's scripts live in the `scripts/` subdirectory next to this SKILL.md file.

To locate the workspace root at runtime, run:
```bash
openclaw config get workspace 2>/dev/null || echo "$HOME/.openclaw/workspace"
```

The full script path is then: `<workspace>/skills/update-advisor/scripts/check-update.sh`

Store the workspace root in a variable when preparing watchdog/log paths or optional post-recovery reporting commands.

---

## Trigger Detection

- Contains "check", "any new", "updated?", "检查更新", "有没有新版本", "更新了吗" → **Check mode** (analyze only, do not update)
- Contains "execute update", "confirm update", "upgrade", "升级", "确认更新", "执行更新" → **Execute mode** (perform update)
- If the immediately preceding turn was a **Check mode report** (Step 4 output), treat affirmative replies ("yes", "go ahead", "do it", "yeah", "sure", "ok", "好", "可以") as Execute mode triggers.

When in doubt, default to **Check mode** — never run the update without explicit user confirmation.

---

## Check Mode

### Step 1: Run the check script

```bash
bash <workspace>/skills/update-advisor/scripts/check-update.sh
```

Store the JSON output as `CHECK_RESULT`.

### Step 2: Parse result

**If `has_update = false` or `same_version = true` or `already_latest = true`**:
> Already on the latest version (`{current_version}`). If `doctor_ok` is false, surface the doctor issues. Done.

**If `changelog_not_found = true` or `changelog_empty = true`**:
> Mention that the CHANGELOG could not be located (or was empty), but the version comparison still works. Continue to Step 3.

**If `has_update = true`**, continue to Step 3.

### Step 3: Changelog analysis

Read fields from `CHECK_RESULT` and analyze along these dimensions.

Key fields available: `current_version`, `latest_version`, `has_update`, `flagged_items`, `flagged_count`, `changelog_delta`, `doctor_ok`, `doctor_exit_code`, `doctor_issues`, `update_meta`, `latest_not_local`, `changelog_not_found`, `changelog_empty`, `rollback_dry_run_cmd`, `rollback_execute_cmd`.


**A. Risk rating** (based on `flagged_items` + `changelog_delta`)

Check each `flagged_items` entry against the user's active configuration. Prefer already-loaded session context; read `MEMORY.md` only if the user explicitly asked for personalized relevance analysis or consents to that read:
- `config` / `schema` changes → check if it affects any configured integrations
- `security` / `harden` → usually good; mark green
- `deprecated` / `removed` → check if the user is using that feature
- `behavior change` → assess scope of impact

Risk level output:
- 🔴 High: breaking change or directly affects an actively used feature
- 🟡 Medium: config migration suggested, core function unaffected
- 🟢 Low: bug fixes and security hardening only

**B. Relevance to user's environment**

If personalized context is available or the user consented to reading `MEMORY.md`, use the user's active configuration — channels, installed Skills, cron jobs, running services, active integrations — and annotate each relevant changelog entry with **"relevant to your setup"** plus a brief explanation.

If no configuration context is available (fresh install, empty MEMORY.md), skip the relevance annotation and note: *"Personalized relevance analysis requires prior session context in MEMORY.md."*

**C. New feature opportunities**

Scan the delta text for new features (look for `### Changes`, `### New`, `### Added` headings, or any changelog block lines describing new behavior) and classify:
- ✅ Recommend enabling (low config cost, immediately useful)
- 👀 Worth watching (valuable but needs testing)
- ⏭️ Skip (not relevant to this setup)

**Special case: `latest_not_local = true`**

The local CHANGELOG does not yet contain the new version (it's only available after installation). In this case:
1. Explain: "The new version's changelog is only available after installation."
2. Show `update_status` output as the available install info.
3. If the full changelog was fetched in this session via another method (e.g. `npm view openclaw`, GitHub raw), use that analysis directly.
4. Suggest: "Run the check again after updating to get the full changelog analysis."

### Step 4: Output decision report

```
## OpenClaw Update Report
**Current**: x.x.x → **Latest**: x.x.x
**Risk**: 🟢 / 🟡 / 🔴

### High-risk items (if any)
- ...

### Relevant to your setup
- ...

### New feature suggestions
- ...

### Doctor status
✅ OK / ⚠️ Issues or fix suggestions: ...

**Manual rollback candidate** (if needed): first preview with `openclaw update --dry-run --tag x.x.x`; only execute a rollback after a separate explicit confirmation.

---
Ready to update? (Reply "confirm update" or "execute update")
```

---

## Execute Mode

When the user explicitly says "execute update" / "confirm update" / "upgrade":

### ⚠️ Required explicit confirmation for recovery side effects

Before any persistent action, tell the user this mode can launch a temporary watchdog process/job and may run bounded `openclaw gateway install` attempts if Gateway stays unhealthy. Proceed only after explicit confirmation.

### Step 0: Installation ownership check (critical — prevents duplicate installs)

```bash
OC_PATH=$(which openclaw)
OC_REAL=$(python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$OC_PATH" 2>/dev/null || echo "$OC_PATH")
UPDATE_ROOT=$(openclaw update status --json 2>/dev/null | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("update",{}).get("root","") or "")
except Exception:
    print("")')
STAT_TARGET="${UPDATE_ROOT:-$OC_REAL}"
OC_OWNER=$(stat -f '%Su' "$STAT_TARGET" 2>/dev/null || stat -c '%U' "$STAT_TARGET" 2>/dev/null || echo "unknown")
CURRENT_USER=$(whoami)
echo "path: $OC_PATH | realpath: $OC_REAL | update_root: $UPDATE_ROOT | owner: $OC_OWNER | current user: $CURRENT_USER"
```

| Scenario | Criteria | Action |
|----------|----------|--------|
| **Different user owns the install** | `owner ≠ current user` | ❌ **Stop.** Tell the user running update would create a duplicate copy; ask the owner to remove old install first. |
| **Owner unknown** | `owner = unknown` | ❌ **Stop.** Ask the user to run ownership check locally and paste results. |
| **Current user owns the install** | `owner = current user` | ✅ Proceed |

### Step 0b: Confirm target version and dry-run

```bash
openclaw update status --json
openclaw update --dry-run --json
```

If dry-run fails, target is unclear, or downgrade risk exists without separate explicit confirmation, stop.

### Step 1: Arm recovery watchdog BEFORE update (Gateway-independent)

Primary requirement: a Gateway-independent parent must be armed and verified **before** `openclaw update`. The bundled helper auto-selects a backend: macOS uses launchd (`launchctl print` verification), Linux uses a systemd user unit (`systemctl --user show` verification). If no supported backend is available, stop and do not update.

```bash
SKILL_DIR="<path-to-update-advisor-skill>"
WATCHDOG_STATE_DIR="${TMPDIR:-/tmp}/update-advisor-watchdog"
mkdir -p "$WATCHDOG_STATE_DIR"
WATCHDOG_STATE_FILE="$WATCHDOG_STATE_DIR/pre-update.$(date +%Y%m%dT%H%M%S).state"

OPENCLAW_BIN="$OC_REAL" "$SKILL_DIR/scripts/arm-recovery-watchdog.sh" arm --state-file "$WATCHDOG_STATE_FILE"
```

Required gate:
- If `OC_REAL` is empty or not executable, **stop**. Do not run `openclaw update`.
- If arming exits non-zero, prints no `armed=1`, or does not print a state file path, **stop**. Do not run `openclaw update`.
- Keep `WATCHDOG_STATE_FILE`; it is needed for post-update cleanup.
- The helper writes the resolved `OPENCLAW_BIN` into the external job environment so launchd/systemd does not depend on the chat/session PATH.
- The watchdog runtime is bounded (`MAX_RUNTIME_SECONDS` / `--max-runtime-seconds`).
- Recovery attempts are bounded (`RECOVERY_RETRIES` / `--recovery-retries`).
- Logs are written under the state directory for postmortem and cleanup.

The inert template `scripts/recovery-watchdog-launchd.template.plist` documents the macOS LaunchAgent shape; prefer the helper over hand-editing templates. On Linux, the helper uses `systemd-run --user` directly and does not require a template file.

### Step 2: Run the update only after the watchdog gate passes

```bash
openclaw update
```

Session disconnection is expected. Do not treat the lost chat session itself as failure.

### Step 3: Watchdog behavior (independent path)

`recovery-watchdog.sh` waits a grace period, probes `openclaw gateway status`, and only when unhealthy runs bounded `openclaw gateway install` attempts. It exits success when Gateway is healthy and non-zero on timeout/retry exhaustion.

### Step 4: Post-update cleanup and optional reporting

After Gateway is healthy again, clean up the temporary LaunchAgent or systemd user unit plus state/log files:

```bash
"$SKILL_DIR/scripts/arm-recovery-watchdog.sh" cleanup --state-file "$WATCHDOG_STATE_FILE"
```

Then optionally report:

```bash
openclaw --version
openclaw gateway status
openclaw doctor
```

Cron/isolated-session reporting may summarize those outputs, but reporting is optional and must not be the only recovery mechanism.

---

## Notes

- **Step 1 (arm watchdog) must happen before Step 2 (run update)** — session disconnects immediately after
- Linux Execute recovery requires a working systemd user manager (`systemd-run --user` + `systemctl --user`). If unavailable, stop before update and explain that protected Linux recovery is unsupported on that host.
- `openclaw gateway restart` is handled internally; never call it separately
- Session disconnection after update is normal behavior, not a failure
- If the version is unchanged, say rollback is not needed. If a rollback may be needed after a partial upgrade, provide a dry-run command first and require separate confirmation before executing it.
- Skills updates (`clawhub update --all`) are out of scope; handle separately if needed
- **Never use the `edit` tool to patch `openclaw.json` directly** — always use `python3 -c` with the `json` module or `jq` to avoid injecting control characters that break JSON parsing
- **⚠️ exec environment risk**: When `openclaw update` is invoked via `exec`, the child process may share the Gateway's process group. Gateway termination can abort the restart handoff. Any optional cron verification job can only run after the Gateway/scheduler comes back; if no verification report arrives, tell the user to run `openclaw gateway status` locally, then `openclaw gateway install` if not installed or `openclaw gateway start` if installed but stopped, and then re-check.
