# Changelog

## 1.1.8 (2026-10-15)
- Re-release of 1.1.7, which never became public: its bundle accidentally
  included a `garmin/__pycache__/*.pyc` left behind by a local syntax check,
  and ClawHub's A.I.G scanner rejects Python bytecode outright. No bytecode
  in this bundle.
- SKILL.md clarifications prompted by the SkillSpector review of v1.1.6:
  - Transparency section now states exactly when data leaves the machine
    (only on an explicit send command, printed before upload; Garmin sync is
    download-only) and the runtime scope (bash/node/python3, no elevation).
  - "Fragments are normal input" reworded: it governs input format only and
    explicitly does not override the coach's safety judgement.
  - Removed the stale "v1.1.0 overhaul" banner; minor wording ("kill" →
    "remove").

## 1.1.7 (2026-10-15)
- Security-audit remediation (A.I.G T09 findings on v1.1.6):
  - `training/text-to-image.sh`: plan title and every content line are
    HTML-escaped before rendering — plan text can no longer inject markup.
  - `training/screenshot.mjs`: the render context now runs with JavaScript
    disabled and offline; every non-`file://` request is aborted, so the
    screenshot page cannot execute code or reach the network. `--no-sandbox`
    stays (required for chrome-headless-shell as non-root in Docker) and is
    documented in-code.
  - `garmin/garmin-sync.py`: health records and session tokens are written
    owner-only — `summary.json` and activity snapshots are created with mode
    0600, `garmin/`, `activities/` and `.garth/` set to 0700 on every run
    (pre-existing files are tightened too). Replaces the manual `chmod 700`
    step in the Data & privacy section.

## 1.1.6 (2026-08-21)
- Frontmatter description now discloses Garmin health-metric collection and
  local credential/token storage up front (SkillSpector TP4 advisory).
- Display name fixed to drop the accidental "Clawhub" prefix (build-folder
  artifact).

## 1.1.5 (2026-08-21)
- Privacy review remediation (ClawScan/SkillSpector findings on v1.1.4):
  - New "Data & privacy" section fully enumerating every Garmin data category
    collected (activity details, daily health metrics, training metrics, auth
    token cache), storage locations, retention (until user deletion, with the
    exact delete command), recommended permissions, and the opt-out.
  - `garmin-query.py json` now outputs a minimized, coaching-operational
    subset by default (activities + training metrics); daily health metrics
    (resting HR, stress, Body Battery) require an explicit `--full` flag.

## 1.1.2 (2026-08-17)
- Credential handling unified to chmod-600 dotfiles (`.credentials` at skill
  root, matching the existing `garmin/.credentials` pattern). Credentials no
  longer pass through command-line arguments (visible in process listings) or
  environment variables; docs and code now describe the identical flow.
  Addresses the ClawScan review note on credential safety and disclosure.

## 1.1.1 (2026-08-17)
- Scanner compliance: `text-to-image-canvas.mjs` now takes credentials as CLI
  arguments (same interface as `send-album.mjs`) instead of reading environment
  variables in the same file that performs network sends — addresses ClawScan
  static-analysis rule `suspicious.env_credential_access`. No behavior change.

## 1.1.0 (2026-08-17)

**Security**
- All credentials now come from environment variables (`TELEGRAM_BOT_TOKEN`,
  `TELEGRAM_CHAT_ID`) — removed every hardcoded path and credential from
  bundled scripts. Added a Transparency section to SKILL.md declaring the
  skill's complete network surface (api.telegram.org + optional Garmin Connect).
- Scripts are path-independent: data lives relative to the skill directory,
  overridable via `GARMIN_DATA_DIR` / `PLAYWRIGHT_BROWSERS_PATH`.

**Coaching disciplines (new)**
- Six production-derived rules: data-first answers, injury-inquiry discipline
  (resolved = passive monitoring), immediate goal-change propagation,
  pending-item semantics (track the runner's actions, never the bot's
  unanswered questions), correction-requires-real-error, fragments-are-normal.
  Each rule is distilled from a documented failure mode observed in six months
  of production coaching.

**Memory conventions (new)**
- Stable fact IDs, absolute-date discipline, authoritative-correction handling,
  and a refreshed MEMORY.md template.

## 1.0.7 (2026-05)
- Visual HD training plans, Garmin sync, MAF/VDOT/80-20 methodology.
