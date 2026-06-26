# Changelog

## [1.1.3] - 2026-03-09

### Changed
- `digest-agent.sh` and `deliver.sh` rewritten for clarity and compactness —
  same behaviour, less code. Single-letter internal helpers, config reads
  collapsed to one line each, mechanical fallback simplified.
- `deliver.sh` Telegram payload now has `parse_mode: Markdown` baked in —
  header `*Pulse Board Digest*` renders bold; LLM body stays plain text.
- LLM prompt tightened: explicit instruction against asterisks, backticks,
  underscores, and all Markdown.

---

## [1.1.2] - 2026-03-09

### Fixed
- `deliver.sh` Telegram payload no longer includes `parse_mode: Markdown` —
  LLM-composed text containing backticks or asterisks was causing Telegram to
  return a 400 parse error. Digests now deliver as plain text.
- `digest-agent.sh` prompt updated to request plain text output from the agent
  instead of Telegram Markdown, preventing the agent from generating formatting
  characters that would trigger Telegram parse errors.

---

## [1.1.1] - 2026-03-09

### Fixed
- **Bug:** `deliver.sh` was overwriting `last-digest.md` (the raw log) with the
  composed/delivered message on every run. Raw log is now preserved in
  `last-digest.md` permanently. The composed message is written to a new
  separate file: `last-delivered.md`. These two files are now always distinct.
- `digest-agent.sh` delivery failure message updated to reference both files correctly.
- `pulse.yaml` `paths.last_digest` now correctly describes the raw log file.

### Added
- **Privacy disclosure:** `SKILL.md`, `install.sh` Step 7, and `_meta.json` now
  explicitly warn that when LLM composition is enabled, the raw `pending.log`
  is included in the prompt sent to the configured OpenClaw agent. If that agent
  uses a remote/cloud LLM provider, log content will be transmitted off-host.
  Users are advised to use a local-only agent (Ollama) if log privacy is required.
- `_meta.json` now includes a `privacy` section declaring both the LLM
  transmission risk and the caveat that Pulse Board cannot prevent plugged jobs
  from writing secrets into their outputs.
- `digest-agent.sh` inline comment notes the privacy implication before the
  agent call.

### Changed
- `deliver.sh` audit trail section rewritten — writes to `last-delivered.md`
  only, with explicit comment that `last-digest.md` is never touched.
- `SKILL.md` filesystem table updated to show both `last-digest.md` and
  `last-delivered.md` with correct descriptions.
- `SKILL.md` "Reviewing the raw log" section expanded into a full "Log files"
  section with a privacy warning block.

---

## [1.1.0] - 2026-03-09

### Added
- `digest-agent.sh` now composes human-readable digests via `openclaw agent`:
  - Opening verdict sentence (overall system health, casual but factual)
  - One bullet per skill — what ran, how many times, outcome
  - Errors and warnings expanded with relevant log lines
  - Mechanical status line (✅/⚠️ counts) always prepended — reliable regardless of LLM
- Full raw log always written to `~/.pulse-board/logs/last-digest.md` for on-demand review
- `pulse.yaml` new fields: `digest.llm_agent` (default: `main`) and `digest.llm_timeout` (default: 60s)
- `install.sh` Step 7: prompts for digest agent ID (lists available agents) and timeout
- Graceful fallback to mechanical format if `openclaw` is not in PATH, agent call fails, or times out

### Changed
- `install.sh` step count updated from 6 to 7
- `SKILL.md` updated to document raw log availability and agent digest flow

### Design notes
- Agent is called via `openclaw agent --agent <id> --message <prompt> --json`
- Raw log is passed as context in the prompt — never sent externally
- Delivered Telegram/Discord message contains only the LLM summary, not the raw log
- Raw log accessible on demand via `last-digest.md` or by asking your agent

---

## [1.0.5] - 2026-03-09

### Fixed / Security
- `install.sh` secrets env patch is now **explicit opt-in**: the installer
  shows exactly which keys are missing and why, then asks for confirmation
  before appending anything. Nothing is written to the secrets env file
  silently.
- `install.sh` crontab change is now **announced before it happens**: the
  installer prints the exact entries it will add and asks for confirmation.
- `plug.sh` `wrap_cmd` now carries an explicit comment explaining that the
  secrets env is sourced in the cron shell context only — it is never read,
  parsed, logged, or transmitted by `plug.sh` itself.
- `_meta.json` now fully declares `requires.binaries`, `requires.env_vars`,
  `filesystem.creates/reads/modifies`, `network.external_endpoints`, and
  `credentials` — eliminating the metadata/behavior mismatch flagged by the
  OpenClaw security scanner.
- `SKILL.md` now includes a full **"What this skill touches"** section
  (filesystem, crontab, secrets env, network, credentials) so human review
  matches scanner expectations before installation.

### Changed
- No behavioral changes — all logic is identical to 1.0.4. This release is
  purely transparency and consent improvements.

---

## [1.0.4] - 2026-03-09

### Fixed
- `plug.sh` cron tag colon-escaping bug: shell echo was silently dropping the
  colon in `# pulse-board:<skill>` tags, breaking `unplug.sh` discovery and
  producing duplicate cron entries on re-run. All crontab writes now go through
  `python3 subprocess` to bypass shell escaping entirely.
- `install.sh` step counter: steps 4 and 5 were both labelled `[ 4 / 5 ]`.
  Steps renumbered correctly as 1–6 with the new workspace step added.

### Added
- `install.sh` now adds a **Step 6: OpenClaw workspace** prompt and writes
  `openclaw_workspace` to `pulse.yaml`.
- `install.sh` post-install **secrets env patch**: automatically appends
  `LLM_API_KEY=ollama` and `OPENCLAW_WORKSPACE=<path>` to the secrets env file
  if those keys are absent.
- `install.sh` digest cron jobs now written via `python3 subprocess`.

### Changed
- `install.sh` step count updated from 5 to 6.

---

## [1.0.3] - 2026-03-08

### Added
- `plug.sh` discovery mode: scan crontab and OpenClaw `jobs.json`, merge,
  deduplicate, present numbered menu
- `install.sh` asks for OpenClaw cron directory, writes to `pulse.yaml`
- `plug.sh` auto-skips pure `agentTurn` jobs and already-plugged jobs
- Manual flag mode (`--skill`, `--cron`, `--cmd`) still works

---

## [1.0.2] - 2026-03-08

Complete redesign. Setup goes from ~15 terminal operations to 2.

### Added
- `install.sh` — interactive installer
- `plug.sh` — register + wire cron in one command
- `unplug.sh` — remove skill + cron in one command

### Removed
- `setup.sh`, `register.sh`, `unregister.sh`, `templates/`, `docs/`

---

## [1.0.1] - 2026-03-08

### Fixed
- Flat script structure, `SKILL_DIR` resolution, `digest-agent.sh` paths

---

## [1.0.0] - 2026-03-08

Initial release.
