---
name: weekend-scout
description: >
  Scout outdoor events, festivals, and fairs happening next weekend in the
  user's city and nearby cities. Build home-city picks and road-trip options,
  format the digest, and send it to Telegram. Use for actual scout runs and
  reruns of the same workflow. Do not use for codebase maintenance or skill edits.
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python"]}}}
---

## Weekend Scout

ALWAYS use defined `python -m weekend_scout` CLI commands to interface with any skill data files. NEVER manually edit cache files, initialize via file editing, or write database entries directly.
If this run was started by OpenClaw cron, return the final formatted summary for cron delivery instead of choosing an outbound destination yourself.

> **Normal run rule:** Treat this skill plus the bundled references as the authoritative run
> contract. During a normal scout run, do **not** inspect `weekend_scout` package source files or
> call `--help` to infer schemas, payload shapes, or behavior.
>
> Required `python -m weekend_scout ...` commands must succeed before the run continues. If an
> authoritative CLI command exits non-zero, returns a top-level `error`, or returns a
> required-success payload indicating failure, stop the run and tell the user the skill contract
> drifted.
>
> Do **not** fabricate missing logs, synthesize helper outputs, or continue after such a failure.
> If a bundled reference documents a negative-but-valid outcome, handle it exactly as written
> instead of treating it as drift.
>
> Note: `weekend_scout` is a Python package. `python -m weekend_scout` works from any directory.
> Do **not** prefix commands with `cd <path> &&`. Do not patch behavior ad hoc during execution.
>
> **Reference loading rule:** Do **not** preload all references. Read only the reference needed
> for the current branch and current step. After reading a reference, execute that step before
> opening another reference unless you are blocked. Do **not** open later-stage references during
> Step 1 or Step 2 just because they will be needed later.

### Reset Mode

- If the user invoked `weekend-scout --reset`, do **not** run `init-skill`.
- First ask for confirmation that this will delete the Weekend Scout config and cache for the active installation.
- Only after the user explicitly confirms, run:

```bash
python -m weekend_scout reset --yes
```

- Then report the CLI result and stop. Do **not** continue to Step 1 or any discovery steps in reset mode.

### Step 1: Initialize

```bash
python -m weekend_scout init-skill [--city CITY] [--radius KM]
```

- If `needs_setup` is `true`, do **not** guess or infer a city, do **not** continue to Step 2, and return:

```text
Weekend Scout needs one-time setup. Run it again with your city and radius, for example: /weekend-scout Warsaw, 150
```
- If `warnings` contains `coordinates_not_set`, read `references/onboarding.md` and follow the
  auto-fix path exactly.
- If either setup condition is true, do **not** open any other reference until setup completes and
  `init-skill` is rerun successfully.
- If neither setup condition is true, do **not** open `references/onboarding.md` during Step 1.
- Do **not** open `references/search-workflow.md` before setup is complete.
- Do **not** open `references/platform-transport.md` before `init-skill`. `init-skill` itself is not a
  file-backed payload call.
- Otherwise extract and keep:

```text
saturday, sunday, home_city
max_city_options, max_trip_options
max_searches, max_fetches
tier1
cities.tier2_count, cities.tier3_count
cached.count, cached.covered_cities, cached.city_counts
run_id
cache_dir
workflow
```

- Reuse `cache_dir` from `init-skill` for every later file-backed payload in onboarding, discovery, and delivery. Do
  **not** rebuild the transport path manually.

- Treat `workflow` as dynamic run data only:
  - `workflow.audit_command`
  - `workflow.coverage`
  - `workflow.phase_a`
  - `workflow.phase_c`
  - `workflow.phase_d`
- In compact `init-skill`, tier2 and tier3 are not preloaded; request them later on demand.
- Do not recompute localized broad or targeted queries when `workflow.phase_a` or `workflow.phase_c.tier1` already provide them.

### Step 2: Search

- If this run was started from an interactive OpenClaw invocation channel, send this message once before discovery starts: `Searching for next weekend's events now. This can take a minute or two.`
- Do **not** send that message for OpenClaw cron runs.
- Do **not** send that message for `weekend-scout --cached-only`.
- Do **not** repeat that message during later phases, later city batches, or reruns within the same run.
- Before discovery work, read `references/search-workflow.md`.
- The discovery reference is the sole authority for Step 2 phase lifecycle, helper command order, and authoritative command shapes.
- Do **not** open scoring or delivery references during Step 2.
- Read `references/platform-transport.md` only immediately before the first file-backed Step 2 call
  documented in the discovery reference.
- If the user invoked `weekend-scout --cached-only`, follow the cached-only path from that reference, then continue with the normal Step 3 and Step 5/6 flow.
- `--cached-only` is a skill invocation argument. Do **not** append it to
  `python -m weekend_scout init` or `python -m weekend_scout init-skill`.
- Otherwise follow the full Step 2 contract from that reference exactly. The normal-run failure
  rule applies to every required Step 2 CLI call, so do **not** repair failed Step 2 state
  manually.

### Step 3: Score And Step 4: Build Trips

- Before scoring or trip building, read `references/scoring-and-trips.md`.
- Do **not** open the delivery reference until Step 5.
- Follow that reference exactly for the score rubric, selection caps, trip construction, and `score_summary`.

### Step 5: Format/Send And Step 6: Mark Served/Report

- If the user invoked `weekend-scout --research-only`, report the `score_summary`
  output to the user and stop. Do **not** read `references/delivery-and-audit.md`
  or proceed to Step 6.
- Before formatting or sending, read `references/delivery-and-audit.md`.
- Read `references/platform-transport.md` only immediately before the first file-backed Step 5/6 call
  (`format-message`).
- Follow that reference exactly for `format-message`, `send`, `run_complete`, `audit-run`, and the final user report.
- Use `workflow.audit_command` as the run-scoped audit command for this execution.
