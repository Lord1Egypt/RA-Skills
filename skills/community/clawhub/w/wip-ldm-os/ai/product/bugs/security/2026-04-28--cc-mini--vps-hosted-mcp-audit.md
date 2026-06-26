# VPS hosted-mcp security audit and hardening plan (2026-04-28)

> **Live reading guide:** this is the master audit doc. Findings, threat model, storage map, gate, VPS read-only command checklist, remediation tracker, and revision log all live here. Fixes go on separate branches/PRs per the remediation tracker. This doc stays the source of truth for status.

**Filed:** 2026-04-28 PST
**Author:** cc-mini (Claude Code on the Mac mini), with findings input from Parker and a tightening review by another Claude session
**Severity:** High. Hosted-mcp is the privileged surface for remote control of the local Codex daemon. Pre-identified findings expose plaintext bearer tokens, plaintext payloads over the relay WebSocket, missing cross-origin protection on the WS upgrade, a silent JSON-fallback that masks DB outages in production, and a possible source-vs-deployed mismatch on the phone app.
**Status:** Pre-audit. Lanes A/B/C not yet executed. Pre-identified findings on tracker. Dogfood is paused until the gate (below) is met.

## Why this exists

Hosted-mcp is not "just a web app." It is a privileged remote-control relay into a local Codex daemon. The right standard for it is:

- Long-lived tokens never appear in URLs.
- The relay sees ciphertext only.
- Browser-origin abuse is blocked.
- Secrets are not recoverable from Postgres, JSON files, or logs.
- Deployed VPS code is proven to match reviewed source.

Parker's first read-only pass over `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/`, plus a follow-up review by another Claude session, surfaced the issues below. Together they justify a full audit and a documented gate before resuming dogfood.

Headline signals:

1. **Phone app does not use E2EE or short-lived tickets.** Source still wires plaintext `?token=ck-...` and plaintext `session.*` over WebSocket. Server has E2EE/ticket support but the deployed client does not consume it. Server still accepts the URL-token fallback. Live-URL fetch returned the homepage rather than the app, suggesting deployment routing may also be wrong.
2. **Bearer + device tokens stored as plaintext at rest.** Postgres holds tokens directly; JSON backups duplicate them.
3. **WebSocket upgrade does not validate Origin.** CSWSH opening for any user with a logged-in browser. Origin check is necessary but only protects the browser-origin path; a stolen `ck-...` used by a direct WS client is unaffected unless tickets are short-lived and defaults are rotated.
4. **CORS is `*` on bearer-token surfaces.**
5. **Hardcoded default `ck-...` keys in source.** If any of these were ever valid against production, they need rotation; if they are still accepted, they are a backdoor.
6. **Silent JSON fallback in production.** If Prisma is unavailable, the server silently falls back to JSON storage and continues to mint/validate auth tokens. That should fail closed in production.

## The gate

Seven conditions. All must be met before remote-control dogfood resumes. Each maps to one or more findings (see **Findings tracker**) and each has an explicit verification step (see **The gate, expanded with verification**).

1. **Deployed provenance proven.** We have on-disk hashes for the live `server.mjs` and the live static phone-app bundle, plus the live nginx route mapping, the PM2 env, and the git commit those artifacts were built from. The deployed tree matches the reviewed source. The live remote-control URL serves the codex-remote-control app, not the homepage.
2. **No long-lived bearer in browser WS.** Browser uses short-lived single-use WS tickets minted by `/ws-ticket` (or equivalent). The server's URL-token fallback path that accepts `?token=ck-...` on WS upgrade is removed in production, or guarded behind an explicit dev-only flag that is off by default.
3. **No plaintext `session.*` over relay; relay routes ciphertext only.** Browser sends ciphertext envelopes (E2EE). The server-side WS handler for remote-control payloads forwards opaque envelopes; it does not parse or log inner content.
4. **WebSocket Origin allowlist.** The WS upgrade handler validates `Origin` against an explicit env-driven allowlist before bearer/ticket check. Disallowed origins receive 403. (This blocks browser CSWSH only; it does not stop a stolen bearer used by a direct WS client. That path is closed by conditions 2 and 5.)
5. **Bearer hygiene and pre-fix log audit.** All hardcoded default `ck-...` constants are removed from source, all known defaults are rotated in production, and a pre-fix log audit confirms no `ck-` or `?token=` value remains in nginx or PM2 logs (any value found in logs is rotated immediately).
6. **Production data-store fails closed.** The silent Prisma -> JSON fallback path is removed or guarded behind an explicit dev-only flag. If Prisma is unavailable in production, the server refuses to mint or validate auth tokens.
7. **Basic rate limits on auth-mint and validate flows.** `/ws-ticket`, `/bootstrap`, pairing status, pairing completion, OAuth endpoints, and passkey endpoints have at least basic rate limits before real dogfood.

## Threat model

### Actors

- **U1: Honest user with phone + browser.** Parker, today. Loads the remote-control app, holds a ck or ticket, drives the daemon.
- **U2: Honest local daemon.** Codex daemon on Parker's machine, listening on a local socket / port, responding to remote-control over the relay.
- **OP: VPS operator.** Today this is Parker. In future could be additional ops or contractors. Has shell on `wip-vps`.
- **A1: Web-origin attacker.** Runs a malicious page that a logged-in user visits. Browser-bound.
- **A2: Token-leak attacker.** Has a stolen `ck-...` long-lived bearer (from URL leak, log scrape, referer, or backup file).
- **A3: VPS-read attacker.** Has read access to VPS filesystem or Postgres backups (compromised account, leaked dump, backup misroute).
- **A4: WS-protocol attacker.** Speaks WS directly with a stolen bearer; not constrained by browser CORS/Origin.

### Surfaces

- **S1: Phone app.** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/codex-remote-control/index.html` and any related JS. Browser-side. The `?token=<ck>` WS open at line 139.
- **S2: Hosted-mcp server.** `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs`. Node, PM2-managed. OAuth, passkeys, agent auth, wallet, WS upgrade, E2EE handlers, bootstrap and ws-ticket endpoints.
- **S3: nginx.** TLS termination, routing, static assets. Serves the codex-remote-control app and proxies to Node.
- **S4: Postgres (Prisma).** `prisma/schema.prisma`. ApiKey, Device, passkey, wallet tables. Currently plaintext `key` and `token` columns.
- **S5: JSON backups on disk.** Server writes API key and passkey backups via `saveApiKey()` and similar paths around `server.mjs:102`. Filesystem perms and retention unknown. Server also silently falls back to JSON read/write when Prisma is unavailable per `server.mjs:60`.
- **S6: Relay WebSocket.** The wire between phone and daemon, terminated at the VPS hosted-mcp.
- **S7: Daemon endpoint.** Local socket / port on user machine, accepts commands relayed from S6.
- **S8: Codex config / credentials on user machine.** What persists locally.

### Trust boundaries

- Browser <-> nginx: TLS, public.
- nginx <-> Node: loopback, trusted.
- Node <-> Postgres: loopback, env-credentialed, trusted.
- Node <-> filesystem (JSON): trusted, but JSON state must not be a hidden production storage path.
- VPS <-> daemon (over WS through relay): wire is hostile; relay must be ciphertext-only for remote-control payloads.
- Daemon <-> local user: trusted.

### Attacker-goal matrix

| Attacker | Goal | Pre-mitigation path | Mitigation owner |
|----------|------|---------------------|------------------|
| A1 | Hijack WS session from a malicious page | Open WS from malicious origin using user's stored bearer | Origin allowlist (gate 4 / F-003); short-lived tickets bound to origin (gate 2 / F-001) |
| A2 | Reuse stolen ck against any auth surface | Use ck against `/bootstrap`, `/ws-ticket`, or WS query string | Default-key removal + rotation (gate 5 / F-002); pre-fix log audit (gate 5 / F-007); short ticket TTL (gate 2 / F-001); rate limits (gate 7 / F-008); token hashing at rest (P1, F-004) |
| A3 | Read tokens at rest | Read Postgres dump or JSON backup | Hashing at rest (P1, F-004); JSON backup hardening (P1, F-005b); fail-closed primary store so secondary path is not a silent prod copy (gate 6 / F-005a); backup encryption + retention (P2) |
| A4 | Bypass browser checks via direct WS client | Open WS directly with stolen bearer | Origin check is browser-only and does NOT stop A4 (explicit dependency note for F-003); A4 is closed by gate 2 (no long-lived bearer) + gate 5 (rotation + log audit) + ticket TTL + rate limits |
| OP-compromise | Read all data | Inherent to operator role | Out of scope for this gate; mitigated long-term by separation of duties, audit logging, minimum-role Postgres user, encrypted backups |

## Storage map

What is stored, where, and in what shape. This is the data-audit deliverable.

| What | Where | Shape today | Shape required |
|------|-------|-------------|----------------|
| ApiKey.key | Postgres `ApiKey.key` (per `prisma/schema.prisma:33`) | plaintext | keyed-hash + `lastFour` + `displayName` |
| ApiKey JSON backup | disk per `server.mjs:102` | plaintext, duplicate | eliminate or encrypt-at-rest with strict perms + short retention |
| Silent JSON fallback (read+write) when Prisma unavailable | per `server.mjs:60` | active in production | removed or guarded by `LDM_DEV_MODE=1`; in production, fail closed |
| Device.token | Postgres `Device.token` | plaintext | keyed-hash + per-device metadata |
| Default `ck-...` constants | source `server.mjs:72` | plaintext, in repo | removed from source; all defaults rotated; `/bootstrap` and WS reject any historically-known default |
| Bearer in WS URL (server-side accept) | `server.mjs:2396` accepts `?token=ck-...` as fallback on WS upgrade | accepted in production | removed in production, or guarded by an explicit dev-only flag |
| Bearer in WS URL (client-side send) | `index.html:139` opens WS with `?token=<ck>` | always sent | replaced by short-lived ticket fetch; if ticket goes via query, single-use, short TTL, redacted in logs; preferred: `Sec-WebSocket-Protocol` subprotocol |
| Session payloads on relay | WS frames per `index.html:139` | plaintext `session.*` JSON | ciphertext envelopes only (E2EE) |
| Passkey credentials | Postgres + JSON backup (verify in Lane A) | TBD | hashed where applicable; metadata-only backups |
| OAuth tokens | Postgres (verify schema) | TBD | hashed; explicit TTL |
| Wallet records | Postgres | TBD | confirm no PAN / no card material; Stripe customer id only |
| 1Password SA token | local `~/.openclaw/secrets/op-sa-token` | not on VPS | out of scope here |

The "Shape today" column gets concrete `file:line` evidence as Lane A executes. Where rows say "verify", that is a Lane A or Lane B action.

## The gate, expanded with verification

| # | Condition | Verification method | Findings |
|---|-----------|---------------------|----------|
| 1 | Deployed provenance proven | `sha256sum` of live `/var/www/wip.computer/app/mcp-server/server.mjs` vs repo at known commit; `sha256sum` of every file under deployed `app/codex-remote-control/`; `pm2 env` captured + diffed against expected; `nginx -T` excerpt for the relevant `location` blocks captured; live URL fetch returns the codex-remote-control HTML (assert on a known string from the file) | F-009 |
| 2 | No long-lived bearer in browser WS | DevTools network panel: WS open URL contains a ticket (or no token at all if subprotocol-borne), not `ck-`; nginx access log shows ticket-shaped values only for the WS path; `/ws-ticket` is the mint path; server-side: rejecting `?token=ck-...` returns 401 in production builds | F-001 |
| 3 | No plaintext `session.*` over relay; relay routes ciphertext only | Server logs a non-sensitive marker on the E2EE decrypt path; marker hits on every payload; relay path code review confirms no `JSON.parse` of inner content; static-grep confirms no `session.` strings handled outside E2EE wrapper | F-001 |
| 4 | WS Origin allowlist | Test from disallowed origin: WS upgrade rejected with 403 before bearer/ticket check; test from allowed origin: success; allowlist is env-driven, not hardcoded; nginx pass-through of `Origin` header confirmed | F-003 |
| 5 | Bearer hygiene + log audit | `grep -RIn 'ck-' src/hosted-mcp/` returns no default-key constants; previously-known defaults rejected by `/bootstrap` and WS upgrade; log audit confirms no `ck-` or `?token=` in `/var/log/nginx/{access,error}.log`, in `pm2 logs mcp-server`, in any rotated logs; any value found in logs is rotated immediately | F-002, F-007 |
| 6 | Production data-store fails closed | Manually break Prisma connection in a staging instance; confirm `/bootstrap`, `/ws-ticket`, OAuth, passkey paths return 5xx and refuse to mint or validate; confirm no JSON write occurs; in `LDM_DEV_MODE=1` the JSON path is allowed and clearly logged; production builds reject the dev flag | F-005a |
| 7 | Basic rate limits on auth-mint and validate flows | Hit `/ws-ticket`, `/bootstrap`, pairing status, pairing completion, OAuth, passkey at >N/sec from one IP/UA; observe 429s; rate limits are env-tunable; structured log entries record limited requests | F-008 |

## Audit lanes

Three lanes. Lane A first. Lane B is read-only on the VPS and requires Parker's approval. Lane C cuts across A and B.

### Lane A: Repo audit (executed by cc-mini, docs-only)

Scope: `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/` and adjacent `src/bridge/`, `src/hooks/`, and any installer config that touches deploy.

Step by step:

1. **Map the auth surface.** Enumerate all routes in `server.mjs`. For each: which auth method (cookie, bearer, ticket, passkey assertion), what it gates, where the credential comes from, where it is stored. Output: route table.
2. **Map the WS surface.**
   1. WS upgrade handler at `server.mjs:2389`. Document what it checks (token, ticket, origin, headers) and the order of checks. Note the URL-token fallback at `server.mjs:2396`.
   2. E2EE/ticket handlers at `server.mjs:2283`. Document ticket TTL, ticket-to-session binding, decrypt path.
   3. Phone app client at `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/codex-remote-control/index.html`. Document what it does at line 139 and below: how it gets the credential, how it opens WS, what it sends.
3. **Map the data surface.**
   1. `prisma/schema.prisma`. List every table, every column whose name contains `key|token|secret|credential|passkey|cookie|password`.
   2. Find every `writeFileSync` / `appendFileSync` / `fs.promises.writeFile` in `server.mjs` and adjacent files; flag any that include token / key material. Specifically: the silent JSON fallback path at `server.mjs:60`.
   3. Find every `console.log` / logger call that may include token / key material.
4. **Map the deploy surface.**
   1. `nginx` config in repo (if any).
   2. PM2 ecosystem file (if any).
   3. `.env.example` and any docs that imply what env vars exist.
   4. Install spec / `agent.txt` / installer paths that touch the VPS.
5. **Static-grep checks (recorded as evidence).**
   ```bash
   cd repos/ldm-os/wip-ldm-os-private/src/hosted-mcp
   grep -RIn 'ck-[A-Za-z0-9_-]\{6,\}' .
   grep -RIn 'Access-Control-Allow-Origin' .
   grep -RIn 'origin\b' . | grep -iE 'header|req|upgrade'
   grep -RIn 'writeFileSync\|appendFileSync\|fs\.promises\.writeFile' .
   grep -RIn 'JSON\.parse' . | grep -iE 'frame|payload|session|message'
   grep -RIn 'sessionStorage\|localStorage' app/ demo/
   grep -RIn 'token=' app/ demo/
   grep -RIn 'prisma' . | grep -iE 'catch|fallback'
   ```
6. **Cross-check source vs deployed.** Note any place where the server speaks E2EE / ticket but the client does not, or vice versa. F-001 is the headline example. F-009 captures the deployed-side proof.
7. **Output.** Update **Findings tracker**, **Storage map**, and **Threat model** with concrete `file:line` evidence. Add new findings as they appear. Open questions go to **Open questions** with an OQ-N id.

### Lane B: VPS read-only audit (Parker-run, or with Parker's explicit approval)

Read-only. No changes. No `--fix`, no `restart`, no `reload`, no edits. If shell access is granted to cc-mini, the same constraint applies. Run B0 and B7 first; they are the highest-value steps for the gate.

#### B0. Deployed provenance capture (gate 1 / F-009)

Run before any other live testing. Captures the on-disk artifacts the server is actually running today.

```bash
# Server file hash + stat
sudo sha256sum /var/www/wip.computer/app/mcp-server/server.mjs
sudo stat /var/www/wip.computer/app/mcp-server/server.mjs

# Static phone-app bundle hash + listing
sudo find /var/www/wip.computer/app/mcp-server/ \
  -path '*codex-remote-control*' -type f \
  -exec sha256sum {} \;
sudo ls -la /var/www/wip.computer/app/mcp-server/app/codex-remote-control/ 2>/dev/null
sudo ls -la /var/www/wip.computer/app/mcp-server/demo/ | head -20

# nginx route mapping for the surface
sudo nginx -T 2>/dev/null | awk '
  /server_name|listen|location|proxy_pass|add_header/ {print NR": "$0}
' > /tmp/nginx-audit-routes.txt
wc -l /tmp/nginx-audit-routes.txt

# PM2 env for the app
pm2 list
pm2 env <id_from_pm2_list>     # capture, redact secret values, save snapshot

# git commit currently deployed (if a marker file or env var exists)
sudo grep -RInE 'commit|version|sha' /var/www/wip.computer/app/mcp-server/.deployed-* 2>/dev/null
sudo cat /var/www/wip.computer/app/mcp-server/package.json 2>/dev/null | head -30
```

What we want answered:

- The `sha256sum` of the live `server.mjs` matches a specific commit in `wip-ldm-os-private` history. If it does not, F-009 is open until reproducible build provenance lands.
- The deployed `app/codex-remote-control/index.html` matches the in-repo source line for line, or the difference is documented.
- The nginx route for remote-control points to the expected app directory, not to a default fallback that returns the homepage.
- The PM2 env declares only the env vars we expect, and the `LDM_DEV_MODE` style flag (if used by F-005a) is **not** set in production.

#### B7. Pre-fix log audit (gate 5 / F-007)

Run before any other live testing. If `ck-` or `?token=` strings exist in any log, treat them as already-leaked and rotate.

```bash
sudo grep -E '\?token=|\&token=|key=|ck-[A-Za-z0-9]' /var/log/nginx/access.log | head -40
sudo grep -E '\?token=|\&token=|key=|ck-[A-Za-z0-9]' /var/log/nginx/error.log | head -40
sudo zgrep -E '\?token=|\&token=|key=|ck-[A-Za-z0-9]' /var/log/nginx/*.gz 2>/dev/null | head -40
pm2 logs mcp-server --lines 1000 --nostream | grep -iE 'token|key|ck-'
sudo journalctl -u nginx --since '7 days ago' | grep -iE '\?token=|ck-' | head -40
```

What we want answered:

- Any matches at all means the value is leaked. Rotate the matching `ck` immediately.
- If matches are present, log redaction is its own follow-up under F-007 implementation: nginx `log_format` should mask `token=...` query parameters; PM2 logs should not echo bearer values.
- Confirm zero matches over a recent window after rotation and redaction.

#### B1. Service inventory

```bash
sudo systemctl list-units --type=service --state=running | grep -iE 'pm2|nginx|postgres'
pm2 list
pm2 show mcp-server
```

#### B2. nginx (full)

```bash
sudo nginx -T 2>/dev/null > /tmp/nginx-audit.txt
grep -nE 'server_name|listen|location|proxy_pass|ssl_protocols|ssl_ciphers|add_header' /tmp/nginx-audit.txt
# Specifically capture: locations for /demo, /agent, /app/codex-remote-control, /ws, /bootstrap, /ws-ticket
sudo ls -la /etc/nginx/sites-enabled/
```

What we want answered:

- Which path serves the codex-remote-control app today? Is it the same source tree as the repo? (B0 cross-references this.)
- Are there `add_header` rules for HSTS, CSP, Referrer-Policy, X-Frame-Options, Permissions-Policy?
- Is the WS upgrade proxied through nginx? If so, does nginx pass `Origin` through unchanged? (Required for F-003 to be enforceable in Node; otherwise the allowlist must live in nginx.)

#### B3. Filesystem on `/var/www/wip.computer/app/mcp-server/`

```bash
ls -la /var/www/wip.computer/app/mcp-server/
ls -la /var/www/wip.computer/app/mcp-server/demo/
ls -la /var/www/wip.computer/app/mcp-server/app/ 2>/dev/null
stat /var/www/wip.computer/app/mcp-server/server.mjs
stat /var/www/wip.computer/app/mcp-server/.env 2>/dev/null
find /var/www/wip.computer/app/mcp-server -maxdepth 4 -name '*.json' -ls
find /var/www/wip.computer/app/mcp-server -maxdepth 4 -name '*backup*' -ls
find /var/www/wip.computer/app/mcp-server -maxdepth 4 -name '*api-key*' -ls
```

What we want answered:

- Owner and mode of `server.mjs`, `.env`, and any `*.json` backup files. Secrets should be mode `600`, owned by app user only; shared-read at most `640`.
- Whether the deployed `app/codex-remote-control/index.html` matches the source in repo; diff it.
- Whether any backup file mode is world-readable.

#### B4. Postgres

```bash
sudo -u postgres psql -c '\du'                          # roles
sudo -u postgres psql -l                                # databases
sudo -u postgres psql -d <db_name> -c '\dt'             # tables
sudo -u postgres psql -d <db_name> -c '\d "ApiKey"'     # column types
sudo -u postgres psql -d <db_name> -c '\d "Device"'
sudo -u postgres psql -d <db_name> -c "SELECT count(*) FROM \"ApiKey\";"
sudo -u postgres psql -d <db_name> -c "SELECT count(*) FROM \"Device\";"
sudo netstat -tlnp 2>/dev/null | grep 5432              # confirm bound to 127.0.0.1 only
sudo ss -tlnp | grep 5432
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep -v '^#' | grep -v '^$'
```

What we want answered:

- Postgres is bound only to loopback.
- App connects with a least-privilege role, not `postgres` superuser.
- `ApiKey.key` and `Device.token` column types and presence of any hash columns.

#### B5. Backups

```bash
ls -la /var/backups/ 2>/dev/null
ls -la /root/backups/ 2>/dev/null
ls -la /var/www/wip.computer/app/mcp-server/backups/ 2>/dev/null
crontab -l
sudo cat /etc/cron.d/* 2>/dev/null
which rclone restic borg duplicity 2>/dev/null
```

What we want answered:

- Are backups encrypted at rest?
- Where do they go (local only, S3, external)?
- Retention policy? Are old backups pruned?
- Are they accessible to non-root users?

#### B6. Firewall and SSH

```bash
sudo ufw status verbose
sudo iptables -L -n -v
sudo cat /etc/ssh/sshd_config | grep -iE '^PermitRootLogin|^PasswordAuthentication|^AllowUsers|^Port|^PubkeyAuthentication'
last -n 30 -F
sudo tail -n 200 /var/log/auth.log
```

#### B8. TLS

```bash
sudo certbot certificates
echo | openssl s_client -connect wip.computer:443 -servername wip.computer 2>/dev/null \
  | openssl x509 -noout -dates -subject -issuer
nmap --script ssl-enum-ciphers -p 443 wip.computer    # if nmap installed
```

#### B9. Process / fd inventory

```bash
ps -ef | grep -iE 'node|pm2|nginx|postgres'
sudo lsof -p $(pgrep -f 'mcp-server' | head -1) | head -80
```

What we want answered:

- The app process is running as a non-root user.
- It does not have a stray open fd to anything unexpected (foreign IP, world-writable file).

### Lane C: Data audit

Consumes Lane A and Lane B output. Steps:

1. **Postgres data inventory.** Use Lane B B4. List every column whose name implies sensitive data. For each: type, length, presence of hash, presence of related metadata column.
2. **JSON backup inventory.** Use Lane B B3/B5. List every backup file. For each: owner, mode, contents shape (header lines only, never paste full content into this doc), retention.
3. **Log inventory.** Use Lane B B7. Confirm zero token leak in logs over a recent window. Establish ongoing redaction policy.
4. **Browser storage inventory.** Open the live demo and codex-remote-control URLs in DevTools. Enumerate `localStorage`, `sessionStorage`, IndexedDB, cookies. For each: shape, sensitivity, expiry.
5. **Daemon storage inventory.** On user machine, list daemon config dir, daemon storage, log files. Document any token persistence.
6. **Codex config inventory.** Confirm where Codex stores its credentials, who owns them, mode.
7. **Cross-reference.** Update **Storage map** with shapes and severities.

## Findings tracker

### P0 gate-blockers (must land before resuming dogfood)

| ID | Title | Evidence | Gate | Status |
|----|-------|----------|------|--------|
| F-001 | Phone app does not use E2EE / short-lived tickets; server still accepts URL-token fallback | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/codex-remote-control/index.html:139` opens WS with `?token=<ck>` and sends plaintext `session.*`. Server has E2EE/ticket support at `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2283` but client does not consume it; server still accepts URL-token fallback at `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2396` | 2, 3 | open |
| F-002 | Hardcoded default `ck-...` bearer keys in source | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:72` | 5 | open |
| F-003 | WebSocket upgrade does not validate Origin (CSWSH risk; browser-only defense) | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2389` authenticates token/ticket but does not check `Origin`. Note: this is a browser-only defense; A4 (direct WS client with stolen ck) is not closed by this finding alone and requires F-001 + F-002 to also land | 4 | open |
| F-005a | Production data-store does not fail closed; silent Prisma -> JSON fallback | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:60` silently falls back to JSON read/write when Prisma is unavailable; production code path can mint and validate auth tokens without the canonical store being healthy | 6 | open |
| F-007 | Pre-fix log audit + ongoing log redaction | `?token=ck-...` URLs at `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:2396` and `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/app/codex-remote-control/index.html:139` may have caused historical log leakage in nginx access logs and PM2 logs | 5 | open |
| F-008 | Auth-adjacent endpoints lack rate limits | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs` mints/validates control authority via `/ws-ticket`, `/bootstrap`, pairing status, pairing completion, OAuth, passkey paths without basic rate limits | 7 | open |
| F-009 | Deployed provenance is not proven | A live-URL fetch returned the public homepage rather than the codex-remote-control app, suggesting source and deployed assets may diverge. We do not currently capture hashes / git commit / PM2 env / nginx route as part of deploy | 1 | open |

### P1 cleanup (before broader users, not gate)

| ID | Title | Evidence | Status |
|----|-------|----------|--------|
| F-004 | API keys and device tokens stored as plaintext at rest in Postgres | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/prisma/schema.prisma:33` | open |
| F-005b | JSON backup files duplicate plaintext token material | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:102` (apply same shape to passkey backups) | open |
| F-006 | CORS is `*` on bearer-token surfaces | `repos/ldm-os/wip-ldm-os-private/src/hosted-mcp/server.mjs:263` | open |

### P2 hygiene (alongside or after P1)

Slots, to be filled in during Lane A and Lane B:

- **F-P2.1** Security headers on nginx: HSTS, CSP, Referrer-Policy, X-Frame-Options, Permissions-Policy. Verify in Lane B B2.
- **F-P2.3** Structured audit logging for token use, ticket mint, passkey assertion, agent-auth grant.
- **F-P2.4** Backup retention policy, encryption-at-rest for backups, off-VPS copy policy.
- **F-P2.5** Postgres role hardening: confirm app user is least-privilege, not superuser; verify `pg_hba.conf`.

(F-P2.2 was promoted to P0 / F-008. F-P2.6 was promoted to P0 / F-007.)

## Remediation tracker

Each fix lives on its own branch. Do not stage fixes on `cc-mini/vps-security-hardening-plan` or `cc-mini/vps-audit-tighten-from-review`. Update **Status** as PRs land.

| Finding | Topic | Proposed branch | Status | PR |
|---------|-------|-----------------|--------|----|
| F-002 + F-005a | Remove default `ck` keys + production fail-closed (Prisma unavailable refuses auth) | `cc-mini/vps-fail-closed-defaults` | not started | |
| F-007 | Pre-fix log audit + redaction policy (nginx `log_format`, PM2 redaction); post-rotation re-scan | `cc-mini/vps-log-audit-redaction` | not started | |
| F-003 | WebSocket Origin allowlist (env-driven) | `cc-mini/ws-origin-allowlist` | not started | |
| F-008 | Basic rate limits on auth-mint/validate flows | `cc-mini/auth-rate-limiting` | not started | |
| F-001 | Phone app E2EE + short-lived ticket wiring; remove URL-token fallback in production | `cc-mini/remote-control-e2ee-ticket-wiring` | not started | |
| F-009 | Deployed provenance: hash + git commit + PM2 env + nginx route capture, deploy script writes provenance file | `cc-mini/vps-deployed-provenance` | not started | |
| F-004 | API key + device token hashing migration (Postgres + Prisma migration) | `cc-mini/api-key-token-hashing` | not started | |
| F-005b | JSON backup file hardening (eliminate or encrypt + perms + retention) | `cc-mini/json-backup-hardening` | not started | |
| F-006 | CORS scoping | `cc-mini/cors-scoped-origin` | not started | |
| F-P2.1 | nginx security headers | `cc-mini/nginx-security-headers` | not started | |
| F-P2.3 | Structured audit logging | `cc-mini/auth-audit-logging` | not started | |
| F-P2.4 | Backup retention + encryption | `cc-mini/backup-policy` | not started | |
| F-P2.5 | Postgres role hardening | `cc-mini/postgres-role-hardening` | not started | |

### Sequencing

The order matches the gate's intent: stop the bleeding first, then close the perimeter, then rewire the client, then prove deployment. Dogfood resumes only after the gate is fully green.

1. **Stop the bleeding (gate 5 + 6).**
   - F-007 first: log audit. Find any leaked `ck-...` and rotate before any further live testing.
   - F-002: remove default `ck-...` constants from source; rotate production keys.
   - F-005a: production fail-closed; silent JSON fallback removed or guarded behind dev-only flag.
   - These three can land together on `cc-mini/vps-fail-closed-defaults` (F-002 + F-005a) and `cc-mini/vps-log-audit-redaction` (F-007).
2. **Close the perimeter (gate 4 + 7).**
   - F-003: WS Origin allowlist.
   - F-008: rate limits on auth-mint/validate flows.
3. **Rewire the client and the WS surface (gate 2 + 3).**
   - F-001: phone app uses E2EE + short-lived tickets; server URL-token fallback removed in production.
4. **Prove deployment (gate 1).**
   - F-009: capture and verify hashes, git commit, PM2 env, nginx route. Deploy script writes a provenance file (or build artifact) so future deploys are auditable.
5. **Resume dogfood under the new gate.** Each verification step in **The gate, expanded with verification** must produce concrete evidence captured in this doc before resume.
6. **P1 work** (F-004, F-005b, F-006) against the now-stable surface.
7. **P2 hygiene** in parallel as time allows.

## Open questions

- **OQ-1.** Which exact path does `wip.computer` serve for remote-control today, and where does the codex-remote-control app live in the deployed asset tree? Lane A read of repo + Lane B B0/B2/B3 of nginx and filesystem will answer.
- **OQ-2.** Have any of the hardcoded `ck-...` defaults at `server.mjs:72` ever been valid against production, or are they purely dev fixtures? Influences urgency of rotation logging and the "previously-known defaults rejected" verification.
- **OQ-3.** Does the daemon also accept the same `ck`-style bearer? Same hashing and rotation policy needs to apply there. Lane A read of `src/bridge/` and daemon code answers.
- **OQ-4.** Is Postgres exposed beyond loopback? Lane B B4 answers.
- **OQ-5.** Where do JSON backups go on the VPS, what is their retention, and are they ever copied off-VPS? Lane B B3/B5 answers.
- **OQ-6.** Does nginx pass `Origin` through to the Node WS upgrade unchanged? Lane B B2 answers. If nginx strips or rewrites it, the Origin allowlist has to live in nginx, not Node.
- **OQ-7.** What is the ticket transport in gate 2? Query string with single-use short-TTL value, `Sec-WebSocket-Protocol` subprotocol, or POST + cookie? Each has tradeoffs around logging and CSRF; pick before F-001 implementation.
- **OQ-8.** Does any current OAuth or passkey path persist tokens in `localStorage` or `sessionStorage` in the demo or remote-control app? Lane C step 4 answers.
- **OQ-9.** What is the env signal for "production" that F-005a's fail-closed and F-001's URL-token-fallback-removal should key off? Candidates: `NODE_ENV=production`, an LDM-specific flag like `LDM_HOSTED_MCP_MODE=production`, or absence of `LDM_DEV_MODE=1`. Pick before F-002 + F-005a implementation so the same flag is consistent.
- **OQ-10.** What is the rate-limit transport for F-008? In-process LRU per IP, an `express-rate-limit` style middleware, or nginx-side `limit_req`? Pick before F-008 implementation; nginx-side is more durable across PM2 restarts but harder to scope per-route.

## References

- OWASP WebSocket Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html>
- OWASP Cryptographic Storage Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html>
- OWASP REST Security Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>
- OWASP CSWSH (Cross-Site WebSocket Hijacking): <https://owasp.org/www-community/attacks/Cross_Site_WebSocket_Hijacking>
- IETF RFC 6455 (The WebSocket Protocol), section 10.2 Origin Considerations: <https://datatracker.ietf.org/doc/html/rfc6455#section-10.2>
- OWASP ASVS, V2 Authentication, V3 Session Management: <https://owasp.org/www-project-application-security-verification-standard/>

## Process notes

- **Doc ownership.** This doc stays the source of truth for the audit. Findings move from `open` to `in-progress` to `landed` (with PR link) to `verified`. Do not delete findings; superseded findings become `superseded` with a pointer to the new id.
- **Worktree discipline.** This doc lives on `cc-mini/vps-security-hardening-plan` (initial) and `cc-mini/vps-audit-tighten-from-review` (this revision). Code fixes live on their own branches per the remediation tracker. Do not stage fixes on either docs branch.
- **Commit hygiene.** Co-authored commits per repo convention (Parker, Lēsa, Claude Code). No squash merge.
- **VPS access.** Lane B is read-only and Parker-approved. No `--fix`, no restart, no edit during the audit.
- **Splitting the doc.** If a finding's implementation plan grows beyond a small section, move it to its own file at `ai/product/bugs/security/2026-04-28--cc-mini--<finding-slug>.md` and link from this doc. The master audit stays here.

## Revision log

- **2026-04-28 PST (initial filing).** PR #720, merge commit `da20a88`. Six conditions (gate), six findings (F-001 through F-006). Severity High. Dogfood paused.
- **2026-04-28 PST (review tightening).** Integrating review feedback from another Claude session.
  - Promoted **deployed provenance** to gate condition 1 (was "correct app served"); split into its own finding **F-009** with concrete capture steps in Lane B B0.
  - Expanded **F-001** evidence to include the server-side URL-token fallback at `server.mjs:2396`. F-001 implementation now also requires removing or guarding that fallback in production.
  - Split **F-005**:
    - **F-005a** (P0, gate 6): production data-store fails closed; silent Prisma -> JSON fallback at `server.mjs:60` removed or guarded behind a dev-only flag.
    - **F-005b** (P1): JSON backup file hardening (perms, retention, encryption).
  - Added explicit **F-003 dependency note**: Origin allowlist is browser-only; A4 (direct WS client with stolen ck) is closed by gate 2 (no long-lived bearer) + gate 5 (rotation + log audit), not by F-003 alone.
  - Promoted log work to **F-007** (P0, gate 5): pre-fix log audit + ongoing redaction policy. Lane B B7 moved up alongside B0 as the first read-only steps.
  - Promoted rate limits to **F-008** (P0, gate 7): basic rate limits on auth-mint/validate flows before real dogfood.
  - Resequenced **fix order** to: stop the bleeding (F-007, F-002, F-005a) -> close the perimeter (F-003, F-008) -> rewire the client (F-001) -> prove deployment (F-009) -> resume dogfood -> P1 -> P2.
  - Added **OQ-9** (env signal for production) and **OQ-10** (rate-limit transport).
