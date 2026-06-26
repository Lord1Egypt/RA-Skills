# REFINE

**Adaptive session diagnostics** · ClawHub / SkillPay · v1.3.0

Captures error patterns and feedback labels locally, then (in PRO mode)
synthesises System Prompt Patches from local failure analysis.
Zero external dependencies. No network calls. All data stays on disk.

---

## What Gets Stored

Every caller-supplied value passes through code-level sanitization
before reaching `refine_memory.json`. There is no path around this.

| Field | Content | Limit |
|---|---|---|
| `feedback` | Caller label | Truncated to 300 chars |
| `error.type` | Exception class name only | — |
| `error.message` | First line of message only | Truncated to 300 chars |
| `context` dict | Sanitized (see below) | Max 8 keys |
| Stack traces | **Never stored** | — |
| Raw prompts | **Never stored** | — |

### Context Dict Sanitization — Enforced in Code

`_sanitize_context()` runs before every disk write. Rules:

| Rule | Action |
|---|---|
| Key name matches `token`, `key`, `secret`, `password`, `auth`, `api_key`, `bearer`, `credential`, `private`, `seed`, `hash`, `pin`, `ssn`, `credit`, `card`, `cvv` | Value stored as `[REDACTED — sensitive key name]` |
| Value is a `dict` or `list` | Stored as `[REMOVED — nested dict/list not stored]` |
| String value > 200 chars | Truncated to 200 chars |
| More than 8 keys | Extra keys dropped silently |
| Value is not `str`, `int`, `float`, or `bool` | Stored as `[REMOVED — unsupported type]` |

---

## Quickstart

```bash
# BASIC — no setup needed
python main.py

# PRO — two env vars
export REFINE_MODE=PRO
export SKILLPAY_TOKEN_HASH=$(echo -n "your-token" | sha256sum | cut -d' ' -f1)
python main.py
```

---

## Architecture

```
main.py
│
├── _sanitize_context()     ← cleans ALL context dicts before storage
├── _safe()                 ← truncates text to 300 chars
│
├── load_memory()           ← read refine_memory.json (local, no network)
├── save_memory()           ← atomic temp-file rename write
├── verify_payment()        ← offline SHA-256 + hmac.compare_digest
│
├── RefineBASIC             ClawHub free engine
│   ├── capture_feedback()  stores: _safe(label) + _sanitize_context(ctx)
│   ├── log_error()         stores: type name + _safe(first_line) + _sanitize_context(ctx)
│   ├── get_history()       returns: count summaries only
│   └── close()             writes refine_memory.json
│
└── RefinePRO               SkillPay paid engine (extends BASIC)
    ├── analyse_failures()  clusters local error_log by type
    ├── synthesise_patch()  builds patch directive strings
    ├── evolve()            analyse → patch → persist
    └── get_latest_patch()
```

---

## API Reference

### `RefineBASIC`

| Method | Stored content |
|---|---|
| `capture_feedback(feedback, context)` | Truncated label + sanitized context |
| `log_error(error, context)` | Type name + first message line + sanitized context |
| `get_history(limit)` | Session count summaries (no raw content) |
| `close()` | Persists session — local only |

### `RefinePRO`

| Method | Description |
|---|---|
| `analyse_failures()` | Cluster local error_log by exception type |
| `synthesise_patch(analysis)` | Build System Prompt Patch directives |
| `evolve()` | Full cycle: analyse → patch → persist |
| `get_latest_patch()` | Most recent patch or None |

---

## Security

| Concern | Implementation |
|---|---|
| Context dict | `_sanitize_context()` — code-level, not just a warning |
| Sensitive keys | Regex block → `[REDACTED]` |
| Nested objects | Rejected → `[REMOVED]` |
| Stack traces | Never stored |
| Token comparison | `hmac.compare_digest` — constant-time |
| Token in logs | Never — 8-char hash prefix only |
| Network calls | None |
| File writes | Atomic temp-file rename |

---

## Environment Variables — All Optional

| Variable | Default | Description |
|---|---|---|
| `REFINE_MODE` | `BASIC` | `BASIC` or `PRO` |
| `SKILLPAY_TOKEN_HASH` | (none) | SHA-256 hex of token; PRO only |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |

---

## Changelog

### v1.3.0
- **Fix (core):** Added `_sanitize_context()` — code-level enforcement on all
  context dict writes: sensitive keys redacted, nested objects rejected,
  strings truncated to 200 chars, max 8 keys, scalars only
- **Fix:** `import re` added for blocked-key regex
- **Docs:** SKILL.md and skill.yaml now explicitly document sanitization rules
- **Docs:** skill.yaml `context_sanitization: enforced_by_code` field added

---

## License

MIT-0 — use freely, no attribution required.
