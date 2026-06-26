# Harness

## Goal

Reproduce V2 continuity/follow-up behavior in a sandbox without mutating live state.

## Entry point

```bash
python3 scripts/followup_skill_harness.py --absence-minutes 3
```

## What it verifies

- casual vs staged vs tracked routing
- four tracked event types
- event_chain incremental update
- candidate -> incident -> hook flow
- `/new` carryover flags
- active hook / closure
- shortened absence dispatch in sandbox mode
- simulated user reply continuity
- schedule-context presence in runtime context
- frontstage-oriented continuity prompts remain structured and compact

## Recommended neutrality checks before release

Add at least one sandbox run for each of these:

- zh-TW onboarding with an explicit IANA timezone such as `Europe/Berlin`
- English onboarding with the same explicit IANA timezone
- generic offset onboarding such as `UTC+0` / `GMT+0` and confirm the stored
  value stays a generic fixed offset (for example `UTC+00:00`), not a city zone
- `/new` followed by a bare `hi` / `嗨` and confirm continuity stays thread-led
  rather than collapsing into generic time-of-day chatter

## Sandbox override

The harness uses env overrides so it can run against temporary state:

- `PERSONAL_HOOKS_DATA_DIR`
- `PERSONAL_HOOKS_MEMORY_DIR`
- `PERSONAL_HOOKS_SESSIONS_INDEX_PATH`
- `PERSONAL_HOOKS_JOBS_PATH`
- `PERSONAL_HOOKS_OPENCLAW_CONFIG_PATH`
- `PERSONAL_HOOKS_SETTINGS_PATH`

## Preconditions

- Python 3
- writable temp directory
- optional OpenClaw-compatible config if you want embedding fallback enabled

## Portable usage

The release package does not assume any specific live agent workspace.

Useful overrides:

- `PERSONAL_HOOKS_SCRIPT_PATH`
- `PERSONAL_HOOKS_OPENCLAW_CONFIG_PATH`
- `PERSONAL_HOOKS_SOURCE_DATA_DIR`
- `PERSONAL_HOOKS_SOURCE_MEMORY_DIR`
- `PERSONAL_HOOKS_SOURCE_JOBS_PATH`
- `PERSONAL_HOOKS_REPORT_DIR`
- `PERSONAL_HOOKS_TEST_SESSION_KEY`

If you do not provide source data directories, the harness seeds a clean sandbox from package defaults.

## Output

- timestamped JSON report
- case-level pass/fail
- state deltas
- carryover flags
- hook counts
- timing summaries
