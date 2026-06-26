# Version

- Skill: `yuboto-omni-api`
- Version: `1.6.2`
- Released: `2026-03-03`

## Changelog

### 1.6.2
- **Validation visibility patch**:
  - Added explicit docs note that `refresh_swagger.py` is stdlib-only (`urllib`)
  - Clarified helper dependency model in SKILL + user-guide so package scanners/reviewers see the install path clearly
- No CLI behavior changes from 1.6.1

### 1.6.1
- **Packaging fix for helper script**:
  - Replaced `requests` usage in `scripts/refresh_swagger.py` with Python stdlib `urllib`
  - Skill now has no third-party Python dependency for helper utilities either
  - Resolves install/operational mismatch during validation

### 1.6.0
- **Unicode SMS support added** for multilingual content (Greek, Arabic, Chinese, etc.)
  - New `--sms-encoding` option on `send-sms` and `send-csv`: `auto|unicode|gsm`
  - `auto` detects non-GSM text and sets Unicode automatically
  - `unicode` forces `typesms=unicode` and `longsms=true`
  - `gsm` forces GSM mode when explicitly needed
- Keeps all previous safety/privacy behavior (external state path, minimized persistence by default)

### 1.5.3
- **Privacy minimization by default**:
  - State/log persistence now stores minimal metadata only (`messageGuid`, status, timestamps, recipient count)
  - Full payload/recipient/text persistence disabled by default
  - Optional override for debugging: `YUBOTO_STORE_FULL_PAYLOAD=true`
- Keeps external runtime storage defaults from 1.5.2 (`$XDG_STATE_HOME` / `~/.local/state`)

### 1.5.2
- **Clawhub persistence/privacy alignment**:
  - Moved default runtime writes out of skill directory
  - CLI default `--state-dir` now uses `$XDG_STATE_HOME/openclaw/yuboto-omni-api` (fallback `~/.local/state/openclaw/yuboto-omni-api`)
  - `poll_pending.sh` now defaults logs/state to the same external location
  - Added `YUBOTO_STATE_DIR` and `YUBOTO_LOG_DIR` overrides in docs
- **Docs update**:
  - Added backlink: `https://messaging.yuboto.com`

### 1.5.1
- **State rotation/retention added** to prevent unbounded growth on long-running installs:
  - `state/messages_sent.jsonl` rotates to last 5000 lines by default
  - `state/messages_state.json` prunes to max 5000 tracked IDs while always preserving pending IDs
  - Tunable via env vars: `YUBOTO_MAX_SENT_LOG_LINES`, `YUBOTO_MAX_STATE_RECORDS`

### 1.5.0
- **Zero-extra-dependency runtime**:
  - Replaced `requests` with Python standard library `urllib` in `scripts/yuboto_client.py`
  - Fresh OpenClaw installs no longer need `pip install requests`
- **Bulk-send safety defaults**:
  - `send-sms` now auto-batches recipients
  - Default `--batch-size 200`, hard cap `1000` recipients/request
  - Default inter-batch delay: `--batch-delay-ms 250`
  - `send-csv` adds `--delay-ms` (default `100`) to reduce burst/rate issues
- **Operational guardrails**:
  - Clarified approved sender requirement in docs and command help
  - Preserved timeout controls (`--timeout`) and added safer pacing to avoid long/brittle sends

### 1.4.0
- **Registry/metadata coherence fix**: Added OpenClaw metadata in `SKILL.md` frontmatter:
  - `requires.env: ["OCTAPUSH_API_KEY"]`
  - `primaryEnv: "OCTAPUSH_API_KEY"`
  - `requires.bins: ["python3"]`
- **Consistency cleanup**:
  - Removed outdated text claiming registry metadata may be missing.
  - Aligned docs so credential setup is OpenClaw config (recommended) or shell export.
  - Removed contradictory `.env` guidance.
- **Security review pass**:
  - Verified no hardcoded API keys/secrets in package files.
  - Verified `poll_pending.sh` reads env only and does not source `.env`.

### 1.3.0
- **Documentation cleanup**: Removed personal information from examples and documentation
  - Replaced `Dinos` sender ID with generic `YourSender` in all examples
  - Replaced specific phone numbers with generic `+3069XXXXXXXX` format
  - All examples now use generic, non-personal information
- **Professional examples**: Skill documentation now uses industry-standard generic examples
- **Privacy protection**: No personal information in public skill documentation

### 1.2.0
- **OpenClaw config integration**: Skill now supports OpenClaw native credential management
  - API key can be stored in `openclaw.json` under `skills.entries.yuboto-omni-api.env.OCTAPUSH_API_KEY`
  - No need for `.env` files or shell environment variables
  - Consistent with other OpenClaw skills (Home Assistant, Nano Banana Pro, etc.)
- **Security improvement**: Removed `.env` file support from `poll_pending.sh`
  - Eliminates risk of loading unrelated secrets from `.env` files
  - Script now requires `OCTAPUSH_API_KEY` environment variable (from OpenClaw config or shell export)
- **Documentation update**: Added OpenClaw config setup instructions and security notes
- **Clean architecture**: Follows OpenClaw best practices for skill development

### 1.1.0
- **Security improvements**: Fixed `.env` sourcing vulnerability in `poll_pending.sh`
- **Documentation enhancements**:
  - Added clear "Environment Variables" section to SKILL.md
  - Added registration information and link to octapush.yuboto.com
  - Created detailed setup instructions
- **Cleanup**:
  - Removed internal `references/kb_strategy.md` file
  - Removed non-text files for Clawhub compatibility: `.env.example`, `assets/OMNI_API_DOCUMENTATION_V1_10.pdf`, runtime `state/` directory

### 0.1.0
- Initial public release.
- Added live Swagger + PDF reference bundle.
- Added core CLI flows: `balance`, `cost`, `send-sms`, `dlr`, `cancel`.
- Added operational tracking: `poll`, `poll-pending`, `history`, `status`.
- Added bulk messaging command: `send-csv`.
- Added cron-friendly runner: `scripts/poll_pending.sh`.
- Added security notes and sanitized packaging process.
