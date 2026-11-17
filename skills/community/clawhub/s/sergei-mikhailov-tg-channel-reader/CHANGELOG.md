# Changelog

---

## [0.11.1] - 2026-07-03

**Fix: `tg-reader auth` crashed at the `code_sent` stage.** The staged onboarding flow added in 0.11.0 derived the `code_type` field from the Pyrogram `SentCode.type` object, which could resolve to a non-serializable value — so emitting the stage raised `TypeError: Object of type type is not JSON serializable` and the process exited. Because the crash happened *after* `send_code`, 0.11.0 would send the login code but then die before sign-in, making the agent-driven login impossible to complete.

`code_type` is now always emitted as a string. Verified live end-to-end (send code → sign in → `authorized`).

---

## [0.11.0] - 2026-07-03

**Agent-drivable onboarding — an AI agent can set up authentication *for* the user.** Until now the only way to log in was `tg-reader auth`, an interactive command whose phone/code prompts are invisible when driven from an agent or a piped/exec context (the prompt buffers and never shows). So a human always had to sit at the terminal. Now the login is a structured, staged flow an agent can run end-to-end.

### What an agent can do

With the user's consent, the agent runs the whole login and asks the user only for what Telegram itself requires — the **phone number**, the **login code** Telegram sends, and (if the account has one) the **cloud 2FA password**.

- New staged `tg-reader auth --phone … --code-file … --password-file …`. One live process emits one JSON object per line with a `stage` and `next_action`:
  `need_phone` → `code_sent` (`code_type: app`/`sms`) → `need_2fa` → `authorized` (plus `already_authorized` and `error` with a `reason`). The agent reacts to each stage and asks the user the matching thing.
- **Self-serve fallback:** `tg-reader auth --guide` prints step-by-step instructions so a user who'd rather not involve the agent can authorize themselves.

### Safety / privacy

- **The session is stored locally on this machine (OpenClaw)** (`~/.tg-reader-session.session`) — it never leaves the machine and is not uploaded anywhere. The agent should reassure the user of this.
- **The login code and 2FA password are handled securely:** read from a file (`--code-file`/`--password-file`, polled) or stdin — never passed on the command line, so they don't leak into process lists or logs.
- Never prompts via `ainput`; emits flushed JSON (and mirrors stages to `TG_AUTH_PROGRESS` if set). An existing session is backed up first; a dead/unauthorized one is moved aside (`.dead-*`, never deleted) so the fresh login starts clean. Runs under the session lock.

### Compatibility

`tg-reader auth` with no flags still works: it now reports `already_authorized` for a live session, or asks for `--phone`. No re-authentication required for existing sessions.

---

## [0.10.1] - 2026-07-03

**SOCKS5 proxy support for MTProto.** Some networks/hosts filter direct MTProto (TCP 443 to Telegram DCs), surfacing as persistent `Connection timed out` even when the internet works. The skill can now route through a local SOCKS5 proxy.

### Why this was broken

- The skill read only `api_id`/`api_hash`/`session` from config; a `socks_proxy` setting had no effect because the value was never passed to the client. On a host with direct MTProto filtered, every run timed out and looked like a network/Telegram outage rather than a missing route.

### How it works after this update

- New `socks_proxy` config key (and `TG_PROXY` env override, which takes priority). Accepted forms: `host:port` (SOCKS5 by default), `socks5://host:port`, `socks5://user:pass@host:port`.
- The parsed proxy is passed to every client on both backends — Pyrogram (`reader.py`) and Telethon (`reader_telethon.py`), fetch/info/auth paths — and to the `tg-reader-check` online probe.
- `tg-reader-check` now reports the resolved proxy as `credentials.proxy`.
- Fully backward compatible: with no `socks_proxy`/`TG_PROXY` set, the client connects directly exactly as before. Telethon uses the native python-socks dict form (no PySocks dependency).

---

## [0.10.0] - 2026-07-02

**Session hardening — the skill can no longer destroy its own session, and can recover it when something else does.** Triggered by a real incident: after a VM restart, several agent processes raced over the same session file, overwrote it with empty copies, and reported the session as "expired" — while the session on Telegram's side was alive the whole time.

### Why this was broken

- `fetch`/`info` (Pyrogram backend) checked only that the session *file exists*, then entered `Client.start()`, which interactively prompts for a phone number when the session is not authorized. In cron this hangs or dies — and by then the SQLite session is already open for writing.
- Nothing prevented two `tg-reader` processes from opening the same SQLite session file concurrently.
- Error messages suggested switching to the freshest session file found on disk — agents followed that blindly, drifting onto empty never-authorized files.
- `auth` overwrote the session file with no backup.
- There was no honest `not_authorized` error — agents invented explanations ("TTL 30 days", "revoked by Telegram").
- SKILL.md itself advised `rm -f` on the session file as the "session expired" remedy.

### How it works after this update

- `fetch`/`info` connect **non-interactively** (`connect()` + `get_me()`) and never prompt. An unauthorized session returns a structured `error_type: "not_authorized"` immediately; a network failure returns `error_type: "network"` — the two are never conflated. As a backstop, non-interactive commands run with stdin detached (any stray prompt gets `EOFError` instead of hanging).
- Every session use (fetch/info/auth/restore, both backends) takes an **exclusive file lock**. A second process waits up to 60 s, then returns `error_type: "busy"` — concurrent processes can no longer corrupt the file. (POSIX only; on other platforms the lock is a no-op.)
- After every successful authorized run the session is snapshotted to `{session}.session.last-good` (0600) with a no-secrets manifest (verified time, user, sha256). New **`tg-reader restore-session`** command restores it: moves the broken file aside (never deletes), checksum-verifies the backup, installs it, and confirms authorization against Telegram.
- `auth` backs up an existing session first (timestamped `.bak-*`, last 3 kept) and verifies the fresh session with `get_me()`.
- `tg-reader-check --online` (opt-in) verifies actual authorization of the resolved session — the offline default also reports lock state and last-good backup metadata.
- `not_authorized` errors advertise the last-good backup when one exists (`action: "offer_restore"`) and carry an explicit background policy: scheduled/background runs must notify the user, not attempt repairs.
- "Session file not found" hints no longer suggest switching to the freshest found file; they point at `tg-reader-check --online` verification instead.

### Required user action

Update the installed package (`pip install .` from the skill directory, or `clawhub update`). No re-authentication needed. The first successful fetch after the update creates the last-good backup.

### Added

- `tg_session_guard.py` — shared module: session lock, timestamped backups with rotation, last-known-good snapshot/restore (no heavy dependencies)
- `restore-session` subcommand in both backends (`tg-reader`, `tg-reader-telethon`)
- `tg-reader-check --online` — authorization check for the resolved session, under the lock
- `error_type` values: `not_authorized`, `busy`, `network`
- SKILL.md "Session Safety Rules" — agents must never delete/move session files or attempt auth/restore from background runs

### Changed

- Pyrogram backend `fetch`/`info` no longer use `Client.start()` — replaced with non-interactive `connect()` + authorization check (Telethon backend already connected non-interactively; its unauthorized error is now structured)
- `auth` creates a timestamped backup before overwriting an existing session (both backends)
- Session-discovery hints in `reader.py`, `reader_telethon.py`, and `tg_check.py` no longer recommend the freshest file by mtime
- SKILL.md: removed the destructive `rm -f` session-expired instruction; documented recovery via `restore-session`
- `.gitignore`: added `*.session.lock`, `*.session.last-good`, `*.session.last-good.json`, `*.session.bak-*`

### Not changed (no regression risk)

- Fetch/output formats, channel error types, read_unread tracking, comments, `--output` — untouched
- Default session paths and config schema — the `session` config key stays optional
- Device identity remains Pyrogram/Telethon defaults (spoofing gets sessions terminated)
- Dependencies — still pyrofork + tgcrypto + telethon

---

## [0.9.4] - 2026-05-16

**Recent Telegram posts come through again.** The Pyrogram backend now uses `pyrofork>=2.3.69` (a community-maintained drop-in fork) instead of the stale upstream `pyrogram`. Under 0.9.3 and earlier, recent channel posts arrived with `"text": ""`, `"has_media": false`, no `"web_page"` field — even when the same post displayed fine in the Telegram app.

### Why this was broken

The PyPI `pyrogram` package has been frozen at 2.0.106 since August 2023 and does not know the Telegram `Message` TL constructor IDs introduced in May 2026. For any post encoded with one of the newer constructors, Pyrogram silently parses out only the basic metadata (`id`, `date`, `views`, `forwards`, `edit_date`) and leaves `msg.message` / `msg.media` / `msg.entities` / `msg.web_page` as `None`. The 0.9.3 `web_page` extraction logic was correct in isolation — the parsed `Message` object it read from was already empty.

`pyrofork` is the maintained fork. It ships the current TL schema, installs into the **same `pyrogram` import namespace**, and uses **format-compatible session files** — so no `tg-reader auth` re-run is required.

### How it works after this update

- **CLI surface is unchanged.** Same commands (`tg-reader fetch`, `tg-reader info`, `tg-reader auth`, `tg-reader-check`), same flags, same JSON output schema. An agent that worked with 0.9.3 keeps working with 0.9.4 without code changes.
- **Same session file** (`~/.tg-reader-session.session`) — no re-auth.
- **Same config file** (`~/.tg-reader.json`) and same env vars (`TG_API_ID`, `TG_API_HASH`, `TG_USE_TELETHON`, `TG_READ_UNREAD`, `TG_STATE_FILE`) — no config migration.
- **Same Python imports** in `reader.py` (`from pyrogram import Client`, …) — pyrofork serves the `pyrogram` namespace.
- `tg-reader-check` now reports the backend as "Pyrofork (pyrogram namespace) 2.3.x" and surfaces a problem with a `fix` field if it detects a left-over upstream `pyrogram 2.0.106`.

### Required user action (existing installs only)

`pip` will not transparently swap `pyrogram` for `pyrofork` because they own the same import namespace. Run once after updating the skill:

```bash
pip uninstall pyrogram -y
pip install --upgrade --force-reinstall sergei-mikhailov-tg-channel-reader
```

ClawHub users:

```bash
clawhub update sergei-mikhailov-tg-channel-reader
pip uninstall pyrogram -y
pip install pyrofork
```

After the swap, run `tg-reader-check` — `backends.pyrogram.version` should read 2.3.x (pyrofork), not 2.0.106.

### Fixed

- Pyrogram backend: posts encoded with new TL constructor IDs (rolled out in May 2026 and later) are now parsed with their real text, media, entities, and `web_page` data — instead of arriving as empty stubs.

### Changed

- `setup.py`: `pyrogram>=2.0.0` → `pyrofork>=2.3.69` (drop-in fork, same import namespace). `tgcrypto>=1.2.0` and `telethon>=1.24.0` unchanged.
- `tg_check.py` / `tg-reader-check`: detects an outdated `pyrogram 2.0.106` install and surfaces the migration command in its `problems` array and as a per-backend `outdated`/`fix` field.
- Install-time error messages in `reader.py`, `tg_reader_unified.py`, and `tg_check.py` now recommend `pip install pyrofork tgcrypto` and explicitly warn against installing upstream `pyrogram`.
- `setup-tg-reader.sh`: same detection logic — warns when `pyrogram 2.0.106` is found and prints the migration command.
- `SKILL.md`, `README.md`, `README_TELETHON.md`: install commands and library-selection sections updated to reference pyrofork; setup commands include the pre-emptive `pip uninstall pyrogram` step.

### Not changed (no regression risk)

- Telethon backend is untouched — its TL schema is independent and was never affected.
- The `web_page` field, text synthesis from card content, comments fetcher, and read-unread tracking — all introduced in 0.9.3 — keep working unchanged.
- Public CLI flags, JSON output schema, session-file format, config-file format, and env-var contract are identical to 0.9.3.

---

## [0.9.3] - 2026-05-16

**Posts with a link-preview card are no longer invisible.** Many channels (especially news outlets) publish via Telegram's Instant View — the message itself has little or no text, and the article body lives inside the link-preview card. Until now the skill dropped that card data entirely, so the agent reading the JSON saw an empty `text` field and skipped the post. Now the card's title, description, URL, and site name are exposed in a new `web_page` field, and when the message has no text of its own the reader synthesizes one from the card so the post still surfaces in summaries and `--text-only` filters.

### Added
- New `web_page` field on each message (and each comment) — present only when the post carries a Telegram link-preview card; contains `url`, `display_url`, `title`, `description`, `site_name` (whichever fields are non-empty)
- Text synthesis: when the message has no `text` / `caption` but does have a `web_page`, the `text` field is filled from `title + description + url` so card-only posts are no longer dropped silently by downstream agents or by `--text-only`
- Plain-text output (`--format text`) prints a `🔗 title — url` line after the post body when a card is present

### Changed
- Telethon backend: `has_media` is now `false` for messages whose only "media" is a link preview (`MessageMediaWebPage`), and `media_type` is no longer emitted for that case. This aligns the backend with Pyrogram, where `msg.media` was already `None` for these posts, and fixes a latent bug where `--text-only` would drop card-only posts on Telethon but keep them on Pyrogram.
- Comment fetcher (both backends): a comment whose only content is a shared link is no longer dropped by the empty-text `continue` — the same text synthesis and `web_page` extraction now apply to comments.

### Fixed
- Pyrogram backend: `msg.web_page` is now read alongside `msg.text` / `msg.caption`. Previously the card data lived in a separate attribute the reader never touched, so even rich previews on text-bearing posts lost their structured metadata.
- Telethon backend: `MessageMediaWebPage` is now unpacked into the structured `web_page` field. Previously only the bare class name `"MessageMediaWebPage"` was recorded in `media_type` and the inner `WebPage` (with the actual URL / title / description) was ignored.

---

## [0.9.2] - 2026-03-05

**Env var support for read_unread.** `TG_READ_UNREAD` and `TG_STATE_FILE` env vars now work alongside the config file — lets you enable read_unread mode via `~/.openclaw/openclaw.json` Docker `env` without needing `~/.tg-reader.json`.

### Added
- `TG_READ_UNREAD` env var (`"true"`/`"1"`) — enables read_unread mode; overrides config file
- `TG_STATE_FILE` env var — custom state file path; overrides config file
- `tg-reader-check` reports whether read_unread comes from env or config file

---

## [0.9.1] - 2026-03-05

**Metadata fix.** Set correct ClawHub display name to "Telegram Channel Reader".

---

## [0.9.0] - 2026-03-05

**Only see new posts.** Enable `read_unread` mode and the skill remembers what you've already seen — subsequent runs return only unread posts, no `--since` needed. Great for daily digests and monitoring workflows. Add `"read_unread": true` to `~/.tg-reader.json` and you're set.

### Added
- `read_unread` mode: per-channel `last_read_id` stored in `~/.tg-reader-state.json`
- `"read_unread": true` config option in `~/.tg-reader.json` to enable the mode
- `"state_file"` config option and `--state-file` CLI flag for custom state file location
- `--all` CLI flag to bypass read_unread mode and fetch everything without updating state
- `read_unread` metadata in JSON output when the mode is active
- `tg_state.py` — shared state management module (no heavy dependencies)
- `tg-reader-check` now reports read_unread configuration and state file status

### Changed
- When `read_unread` is active and state exists, `--since` is automatically ignored (all unread posts returned)
- On first run (no state), `--since` still applies (default 24h)
- `_fetch_channel` (Pyrogram) accepts optional `min_id` — breaks iteration at already-read messages
- `fetch_messages` / `iter_messages` (Telethon) uses native `min_id` for server-side filtering

---

## [0.8.12] - 2026-03-05

**Security scan fixes (round 2).** Fixed remaining broad session discovery in reader.py and reader_telethon.py — now all three modules use the same restricted `_SESSION_NAMES` list. Restructured README credential examples to recommend `~/.tg-reader.json` first instead of `~/.bashrc`.

### Changed
- `reader.py`: replaced broad `*.session` glob with known tg-reader session names only
- `reader_telethon.py`: same fix — restricted session discovery to known names
- `README.md`: credential setup now recommends `~/.tg-reader.json` (Option A); env vars demoted to Option D with warning against writing to shell profiles

---

## [0.8.11] - 2026-03-05

**Security scan fixes.** Addressed OpenClaw security scanner findings to move from "Suspicious" to "Benign".

### Changed
- `setup-tg-reader.sh`: no longer auto-adds commands to exec allowlist — now prints the approval commands for the user to run manually
- `tg_check.py`: session file discovery now searches only for known tg-reader session names instead of all `*.session` files (avoids exposing unrelated session paths)
- `SKILL.md`: replaced insecure `~/.bashrc` credential example with recommendation to use `~/.tg-reader.json`; updated setup script descriptions to reflect manual approval flow

---

## [0.8.10] - 2026-03-04

**Version bump.** Internal version alignment — no functional changes.

---

## [0.8.9] - 2026-03-04

**Setup script for first-time installation.** New `setup-tg-reader.sh` checks all prerequisites (Python version, CLI commands in PATH, MTProto libraries, credentials, session file), runs `tg-reader-check`, and **automatically adds commands to OpenClaw exec approvals allowlist** via `openclaw approvals allowlist add --gateway`. No more manual approval needed when using the setup script.

### Added
- `setup-tg-reader.sh` — pre-flight setup script with colored output, auto-install from `setup.py`, and automatic exec approvals configuration
- SKILL.md: added CLI approval commands (`openclaw approvals allowlist add --gateway`) and setup script reference

### Changed
- SKILL.md: restructured Exec Approvals section — quick setup first, manual CLI second, UI/messenger third

---

## [0.8.8] - 2026-03-01

**Guard against hallucinated CLI flags.** LLM agents sometimes invent flags like `--hours` or `--days` instead of using the correct `--since` flag. Now the CLI catches these typos and returns a helpful JSON error with the correct flag name — so the agent can self-correct instead of failing silently. All argparse errors are now JSON-formatted for agent readability.

### Added
- Pre-flight check for common hallucinated flags (`--hours`, `--days`, `--weeks`, `--time`, `--period`, `--after`, `--from`, `--media`) with suggested corrections
- Custom `_JsonArgumentParser`: all CLI errors now output structured JSON (`{"error": "...", "action": "fix_command"}`) instead of plain text

### Changed
- `CLAUDE.md`: updated current version to 0.8.8

---

## [0.8.7] - 2026-03-01

**Write output to a file instead of flooding the agent's context.** New `--output` flag saves fetch results (especially large comment payloads) to a file. The agent gets a short confirmation on stdout instead of the full JSON — saving tokens. Works great with cron: schedule periodic updates to a file, then analyze on demand without re-fetching.

### Added
- `--output` flag for `fetch` command — writes results to a file instead of stdout
- `--output` without a filename defaults to `tg-output.json`
- When `--output` is used, stdout returns a short JSON confirmation: `{"status": "ok", "output_file": "...", "count": N}`
- `SKILL.md`: new "Saving to File (Token Economy)" section in After Fetching — explains the periodic update pattern

---

## [0.8.6] - 2026-03-01

**Exec approvals guidance and documentation cleanup.** Users on Linux couldn't figure out where to confirm command execution — the approval prompt lives in the Control UI, not the chat. SKILL.md now has a dedicated "Exec Approvals" section so the agent can explain this. Both SKILL.md and README.md were audited for redundancy and readability.

### Added
- `SKILL.md`: new "Exec Approvals" section — tells the agent how to help users find and approve pending command executions in the Control UI

### Changed
- `SKILL.md`: reordered sections by importance — Output Format, After Fetching, and Error Handling moved up; Setup & Installation moved down (agent rarely needs it)
- `SKILL.md`: condensed Setup & Installation — removed step-by-step my.telegram.org walkthrough (duplicated README), kept essential commands only
- `SKILL.md`: condensed Library Selection — removed code examples already shown in Commands section
- `README.md`: removed duplicate "Library Selection" section (already covered in Setup Step 4)
- `README.md`: moved orphaned troubleshooting items (confirmation code, ChannelInvalid, FloodWait) into the Troubleshooting section
- `README.md`: removed duplicate PATH instructions from Install section (kept in Troubleshooting)
- `README.md`: merged overlapping Security bullet points into a single clean list

---

## [0.8.5] - 2026-03-01

**Clear guide for running the skill on a schedule.** The "Isolated Agents & Cron Jobs" section is now a full "Scheduled Tasks & Cron" guide with two approaches: `sessionTarget: "main"` (recommended — reminder-based, works out of the box) and `sessionTarget: "isolated"` (autonomous but requires Docker setup and session file mounting). The agent now explains the trade-offs to the user when setting up a cron task.

### Changed
- `SKILL.md`: replaced "Isolated Agents & Cron Jobs" section with expanded "Scheduled Tasks & Cron" covering both session target modes, configuration examples, and session file caveats
- Agent instruction added: when creating a scheduled task, explain to the user which approach is used and what it means

---

## [0.8.4] - 2026-02-28

**Read what people are saying in the comments.** Add `--comments` to a fetch command and the skill retrieves discussion replies for each channel post — great for sentiment analysis, audience feedback, and topic tracking. Works with both Pyrogram and Telethon backends.

### Added
- `--comments` flag for `fetch` command — fetches discussion replies (comments) for each post in a single channel
- `--comment-limit N` — max comments per post (default 10)
- `--comment-delay N` — seconds between posts when fetching comments (default 3) to avoid rate limits
- Output includes `comments_enabled`, `comments_available` flags and a `comments` array per message with `id`, `date`, `text`, `from_user`
- Channels without a linked discussion group return `comments_available: false` instead of an error

### Changed
- Default `--limit` drops from 100 → 30 when `--comments` is active (token economy — comments produce a lot of output)
- `--comments` is restricted to a single channel; using it with multiple channels returns an actionable error (`comments_multi_channel`)

### Error handling
- FloodWait during comment fetch: auto-retry once if ≤ 60 s, otherwise sets `comments_error` on the affected message and continues
- Media-only comments (no text) are silently skipped
- Anonymous comments return `from_user: null`

---

## [0.8.3] - 2026-02-28

**Posts with images and videos are no longer invisible.** Previously, if a channel post contained a photo or video, the skill could return an empty text field — and the agent would skip it during summarization. Now every message includes `has_media` and `media_type` fields, and the text caption is always captured correctly. Images and videos themselves are not analyzed (no OCR/vision), but their accompanying text is fully preserved.

### Fixed
- Pyrogram: made text extraction from media posts more explicit — `msg.text` and `msg.caption` are now checked separately instead of relying on Python `or` chain
- Both backends: `has_media` (boolean) and `media_type` (string) are now **always** included in the message output — media info is part of every response by default
- `SKILL.md`: removed instruction to "filter out media-only posts" — agents should never skip posts with media as they often contain important text in captions

### Changed
- Replaced `--media` flag with `--text-only` — by default all posts are included (media + text); use `--text-only` to exclude posts with no text (e.g. standalone images/videos without captions)

---

## [0.8.2] - 2026-02-28

**Security hardening after registry review.** The debug script now asks for confirmation before deleting session files, and insecure session-copying instructions have been removed from the docs.

### Fixed
- `debug_auth.py`: added confirmation prompt before deleting `.session` and `.session-journal` files — no more silent deletion
- `SKILL.md`: documented that `debug_auth.py` deletes session files (with confirmation)

### Removed
- Removed `scp` session-copying instructions from `README_TELETHON.md` and `TESTING_GUIDE.md` — copying session files between machines is insecure and grants full Telegram account access

---

## [0.8.0] - 2026-02-28

**Multiple channels no longer cause Telegram to block your account.** Previously, fetching several channels at once sent all requests in parallel — Telegram treated this as flood and rate-limited the session. Now channels are fetched one at a time with a 10-second pause between each, and short rate limits (≤ 60 s) are waited out automatically.

### Changed
- `fetch_multiple` in both Pyrogram and Telethon backends now processes channels **sequentially** instead of in parallel (`asyncio.gather` removed)
- Pyrogram multi-channel fetch uses a **single session** for all channels (previously each channel opened its own session)
- FloodWait auto-retry: if Telegram says "wait N seconds" and N ≤ 60, the skill sleeps and retries once automatically; longer waits still return an error

### Added
- `--delay` flag for `fetch` command — configurable pause between channels (default 10 seconds)

---

## [0.7.2] - 2026-02-28

**Fixed: channels with non-existent usernames no longer crash the skill.** Pyrogram throws a `KeyError` internally when a username like `@disruptors_official` doesn't exist — this wasn't caught before. Now any unrecognized error is handled gracefully and returns a clear JSON response instead of a stack trace.

### Fixed
- Pyrogram `fetch_messages()` and `fetch_info()` now catch `KeyError` from `resolve_peer` / `get_peer_by_username` — maps to `error_type: "not_found"`
- Added generic `except Exception` fallback to both functions (Telethon already had this) — maps to `error_type: "unexpected"` with `action: "report_to_user"`

---

## [0.7.1] - 2026-02-28

**The skill no longer crashes when a channel is private or you've been banned.** Previously, a single channel error would break the whole request. Now the agent gets a clear JSON response with the error type and a suggested next step — remove the channel, wait, or ask you for a new invite link.

### Improved
- Channel error handling: both Pyrogram and Telethon backends now catch `ChannelPrivate`, `ChannelBanned`, `ChatForbidden`, `ChatRestricted`, `UserBannedInChannel`, `InviteHashExpired`, and more
- Errors return structured JSON with `error_type` (access_denied, banned, not_found, invite_expired, flood_wait) and `action` field for agent automation
- `SKILL.md`: updated Error Handling section with error_type/action reference table

---

## [0.7.0] - 2026-02-28

**New `tg-reader-check` command — instant diagnostics in one second.** The agent runs it before reading channels and immediately sees whether credentials, session file, and libraries are all in place. If something is wrong, it gets a specific suggestion on how to fix it. No more mysterious errors on first run.

### Added
- `tg-reader-check` command — offline diagnostic that verifies credentials, session files, and backend availability
- Outputs structured JSON with `status`, `credentials`, `session`, `backends`, and `problems` fields
- Stale session detection: warns when config points to an older session while a newer one exists (common after re-auth)
- Shows `config_session_override` and `default_path` when config overrides the default session — helps spot mismatches
- Supports `--config-file` and `--session-file` flags (same as reader commands)
- `SKILL.md`: new "Pre-flight Check" section; agent should run `tg-reader-check` before fetching
- `_find_session_files()` deduplication fix (Python 3.13+ `glob` matches dotfiles with `*`)

---

## [0.6.1] - 2026-02-28

**The skill no longer hangs when the session file is missing.** Previously, a missing file would silently trigger a Telegram re-auth prompt that the agent couldn't handle. Now you get a JSON error explaining where the file was expected, which session files were found on disk, and the exact command to fix it.

### Fixed
- Session file validation: `fetch` and `info` commands now check that the `.session` file exists before connecting, instead of silently triggering a re-auth prompt
- When the session file is missing, both Pyrogram and Telethon backends output a structured JSON error with: expected path, list of found `.session` files in `~` and CWD, and a suggested `--session-file` fix
- `get_config()` now strips `.session` suffix if the user passes a full filename (e.g. `--session-file /path/to/foo.session`), preventing Pyrogram/Telethon from looking for `foo.session.session`

---

## [0.6.0] - 2026-02-24

**The skill now works in scheduled tasks (cron) and isolated agents.** If your agent runs on a schedule or inside a sandbox without access to the home directory — just pass explicit paths to the config and session file. Everything works out of the box.

### Added
- `--config-file` flag — pass explicit path to config JSON (overrides `~/.tg-reader.json`)
- `--session-file` flag — pass explicit path to session file (overrides default session path)
- Both flags work with all subcommands (`fetch`, `info`, `auth`) and both backends (Pyrogram, Telethon)
- `SKILL.md`: new "Isolated Agents & Cron Jobs" section with usage examples

### Fixed
- Skill now works in isolated sub-agent environments (e.g. OpenClaw cron with `sessionTarget: "isolated"`) where `~/` is not accessible

---

## [0.5.0] - 2026-02-23

**New `tg-reader info` command — learn everything about a channel in a second.** Title, description, subscriber count, and link. Great for checking a channel before reading its posts, or building a list of channels with descriptions.

### Added
- `tg-reader info @channel` — new subcommand to fetch channel title, description, subscriber count and link
- `SKILL.md`: documented `info` command in When to Use, How to Use, and Output Format sections
- `SKILL.md`: `~/.tg-reader.json` recommended as primary credentials method for agent/server environments that don't load `.bashrc`/`.zshrc`

---

## [0.4.3] - 2026-02-23

**Fixed three bugs that could break authentication and post fetching.** If `tg-reader auth` was giving you cryptic errors or posts wouldn't load — update to this version.

### Fixed
- `reader.py`: removed `system_lang_code` from Pyrogram `Client` init — parameter is Telethon-only and caused `TypeError` on auth
- `reader.py`: fixed `TypeError: can't compare offset-naive and offset-aware datetimes` when fetching messages — `msg.date` from Pyrogram is UTC-naive, now normalized before comparison with `since`
- `reader.py`: removed iOS device spoofing (`_DEVICE`) — Telegram detects the mismatch between declared client identity and actual behaviour and terminates the session; Pyrogram's default identity is stable

---

## [0.4.2] - 2026-02-23

**Improved documentation for macOS and Linux.** Installation instructions now cover both platforms, including Python virtual environments on Ubuntu/Debian.

### Fixed
- `README.md`: fix `python3 -m reader` fallback to `python3 -m tg_reader_unified`
- `README.md`: add Linux venv install instructions for managed Python environments (Debian/Ubuntu)
- `README.md`: add macOS `~/.zshrc` for `TG_USE_TELETHON` alongside Linux `~/.bashrc`
- `README.md`: update PATH section to cover venv bin path, not just `~/.local/bin`
- `README.md`: add note to confirm phone number with `y` during Pyrogram auth
- `SKILL.md`: add Linux venv install instructions
- `SKILL.md`: add note to confirm phone number with `y` during Pyrogram auth

---

## [0.4.1] - 2026-02-23

**Security hardened.** The session file is now protected with restricted permissions, and secret keys no longer leak into logs.

### Security
- `test_session.py`: replaced partial `api_hash[:10]` print with masked output (`***`) to prevent secret leakage in logs or shared terminals
- `SKILL.md`: added `chmod 600` step after auth to restrict session file permissions

---

## [0.4.0] - 2026-02-23

**The skill now integrates correctly with OpenClaw.** Fixed the SKILL.md metadata format so OpenClaw can automatically detect that the skill needs Telegram credentials.

### Fixed
- `SKILL.md` frontmatter converted to single-line JSON as required by OpenClaw spec
- `requires.env` format corrected to array of strings `["TG_API_ID", "TG_API_HASH"]`
- Removed undocumented `requires.python` field from metadata
- Removed optional env vars (`TG_SESSION`, `TG_USE_TELETHON`) from gating filter
- Added missing `primaryEnv: "TG_API_HASH"` for openclaw.json `apiKey` support
- Auth command in setup guide corrected from `python3 -m reader auth` to `tg-reader auth`
- Fallback command in Error Handling corrected to `python3 -m tg_reader_unified`

### Added
- macOS (`~/.zshrc`) credentials setup alongside Linux (`~/.bashrc`) in agent instructions
- `CLAUDE.md` with project context and documentation references for Claude Code

---

## [0.3.0] - 2026-02-22

**Added a second engine — Telethon.** If the auth code isn't arriving via Pyrogram or you're hitting connection issues — try Telethon. One command, same result.

### Added
- **Telethon alternative implementation** (`reader_telethon.py`)
- New command `tg-reader-telethon` for users experiencing Pyrogram auth issues
- Comprehensive Telethon documentation (`README_TELETHON.md`)
- Testing guide (`TESTING_GUIDE.md`) with troubleshooting steps
- Session file compatibility notes
- Instructions for copying sessions between machines

### Changed
- Updated `setup.py` to include both Pyrogram and Telethon versions
- Added telethon>=1.24.0 to dependencies
- Enhanced README with Telethon usage section

### Fixed
- Authentication code delivery issues by providing Telethon alternative
- Session management for users with existing Telethon sessions

---

## [0.2.1] - 2026-02-22

**One command `tg-reader` — and the skill picks the best engine automatically.** No need to choose between Pyrogram and Telethon — it just works. But if you want manual control, the `--telethon` flag or an environment variable is at your service.

### Added
- Unified entry point (`tg_reader_unified.py`) for automatic selection between Pyrogram and Telethon
- Support for `--telethon` flag for one-time switch to Telethon
- Support for `TG_USE_TELETHON` environment variable for persistent library selection
- Direct commands `tg-reader-pyrogram` and `tg-reader-telethon` for explicit implementation choice

### Changed
- `tg-reader` command now uses unified entry point instead of direct Pyrogram call
- Updated documentation with library selection instructions
- `setup.py` now includes all three entry points

### Improved
- Simplified process for switching between Pyrogram and Telethon for users
- Better OpenClaw integration — single skill supports both libraries

---

## [0.2.0] - 2026-02-22

**Step-by-step setup guide included.** Even if you've never worked with the Telegram API — the guide walks you through creating an app on my.telegram.org all the way to your first request.

### Added
- Detailed Telegram API setup instructions in README
- Agent guidance in SKILL.md for missing credentials
- PATH fix instructions for tg-reader command not found
- Troubleshooting section with real-world errors

---

## [0.1.0] - 2026-02-22

**First release! Read Telegram channels straight from the terminal.** Fetch posts from public and private channels for any time window — as JSON for automation or plain text for reading.

### Initial release
- Fetch posts from Telegram channels via MTProto
- Support for multiple channels and time windows
- JSON and text output formats
- Secure credentials via env vars
