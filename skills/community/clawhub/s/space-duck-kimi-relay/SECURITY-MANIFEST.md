# space-duck-kimi-relay — Security Manifest (byte-grounded)

Version: 0.8.4 (aligned with the space-duck family — see MEMORY.md publish log) · Generated 2026-08-11 · Evidence = `scripts/kimi_login.py` line refs.
Rule: every claim below cites file:line. No claim rests on an LLM "reading".

## Scope
Package is exactly 3 files: `SKILL.md`, `_meta.json`, `scripts/kimi_login.py`.
No `lib/`, no `bin/`, no `package.json`, no JS, no dependencies beyond Python stdlib
(`fcntl, json, os, sys, time, urllib, http.server, secrets, subprocess`).

## Credential custody
- Store path: `~/.kimi-code/credentials/kimi.json` — `CRED_PATH` (kimi_login.py:41-42).
- Written 0600 via `os.open(..., 0o600)` in `_save()` (kimi_login.py:73); dir 0700 (kimi_login.py:65).
- Proxy bearer secret `proxy_secret` written 0600 (kimi_login.py:206).
- Access token read only from local file in `_load()`/`fresh_token()` (kimi_login.py:80-154).

## Outbound hosts (complete egress allowlist)
Every network call is a `urllib.request.urlopen` — there are exactly three call sites:
- kimi_login.py:55  → `AUTH_HOST` = `https://auth.kimi.com` (OAuth device + token/refresh), :36
- kimi_login.py:166 → `CODING_BASE` = `https://api.kimi.com/coding/v1` (inference), :40
- kimi_login.py:353 → `CODING_BASE` (streaming inference)
- kimi_login.py:333 → `https://openrouter.ai/api/v1` — ONLY when `OPENROUTER_API_KEY` set (:319)
No other socket/urlopen/requests calls exist. **Nothing is sent to Spaceduckling.**

## Where the token can leave the process
- Kimi token injected as `Authorization: Bearer` only to Kimi hosts: kimi_login.py:164, :350.
- `OPENROUTER_API_KEY` sent only to openrouter.ai: kimi_login.py:333.
- No logging of token/secret values (log_message prints request lines only, :278-279).

## Proxy exposure
- Binds localhost only: `ThreadingHTTPServer(("127.0.0.1", port), ...)` (kimi_login.py:387). No bind-address override exists.
- Auth ON by default: bearer check at kimi_login.py:291-296; secret auto-generated (:203-209).
- `KIMI_RELAY_NO_AUTH=1` is an explicit opt-OUT (:194) and prints a loud warning (:394).
  Assessed NOT a defect: already localhost-bound + secret-by-default. Disclosure, not a patch.

## Fallback spend
- Metered, default cap 200/day (`FALLBACK_DAILY_CAP`, :210); returns 429 past cap (:322-324).

## Service install (hardened in 0.5.2)
- systemd: secrets written to a **separate 0600 EnvironmentFile** `~/.kimi-code/credentials/relay.env` (kimi_login.py:461), referenced via `EnvironmentFile=` (:465). Secrets are NOT inlined into the (world-readable) unit.
- Deterministic test asserts: secret value absent from unit, `EnvironmentFile=` present, env file 0600. PASS (2026-08-11).
- macOS launchd: plist written 0600 (:444); values embedded in plist (0600) — documented residual.

## Overridable endpoints (disclosed)
- `KIMI_AUTH_HOST` (:36), `KIMI_CODING_BASE` (:40), `KIMI_CLIENT_ID` (:38). Changing these re-points token traffic — advanced use, disclosed in frontmatter.

## Not covered by this manifest
- Runtime behavior of the remote Kimi/OpenRouter endpoints (out of package scope).
- Signing / GitHub provenance: ClawHub v0.9.0 exposes no signing command — registry-feature gap, not a code defect.
