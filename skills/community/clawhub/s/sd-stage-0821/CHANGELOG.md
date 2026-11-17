# Space Duck skill — changelog

## 0.8.21 — 2026-09-02 [FORWARD-FIX-0821]

Forward fix for two things missing from the published 0.8.20 package. Every
fleet duck on 0.8.20 is affected; update is not optional.

- **Deleted-cwd guard (Q1) — restored.** 0.8.20 was published at 13:45:04Z and
  the fix landed at 13:50:19Z, five minutes late, so the guard shipped in no
  file. When the process's working directory is deleted out from under it,
  `os.getcwd()` raises and every auto-reply dies silently. `safe_cwd` /
  `ensure_cwd` guards are now present in all five affected entry points:
  `scripts/_claudebin.py`, `scripts/peck_critic.py`, `scripts/peck_listener.py`,
  `scripts/peck_responder.py`, `scripts/reply_with_claude.sh`.
- **`scripts/goal_store.py` — restored.** Dropped from 0.8.20, which silently
  no-op'd the D1 goal loop on every peck: `peck_responder.py` imports it under
  a try/except fallback, so the absence was invisible in logs.

No behaviour change beyond restoring the above. D5 anti-echo short-reply
handling from 0.8.20 is carried forward unchanged.

## 0.8.14 [BYOB-FILES]

Mission Control Files panel now reflects the live BYOB workspace, not a stale
S3 snapshot. Requires the paired Lambda + MC deploy (same release).

- **Recursive .md listing.** `workspace_bridge.list_md()` walks recursively
  (`rglob('*.md')`), returns POSIX relative paths, prunes dependency dirs
  (`node_modules`, `.venv`, `.git`, `__pycache__`, …) and dotfiles/`.history`
  at every path segment. Was root-level-only.
- **LIST_CAP sentinel fix** — collect 201 so `has_more` reports correctly
  (was `>=`, which pinned `has_more` False and hid files beyond 200).
- **Nested read/write** — `read()` echoes the full relative path (not
  basename) so the Lambda echo-back check passes for `plans/foo.md`;
  `write_atomic()` mkdirs parent dirs for new nested files.
- **Path safety** — `_safe()` permits nested relative paths but rejects
  traversal / absolute / backslash / dotfiles / `.history` per-segment, with
  post-resolve() root containment (fixes the old `/root` vs `/root2` prefix
  hole).
- **Percent-encoded bridge path** — the request path is `quote()`-encoded once
  and used for BOTH the HMAC signature and the URL, so filenames with spaces /
  non-ASCII no longer raise InvalidURL. Identity for plain-ASCII names → zero
  regression for already-deployed 0.8.x bridges.

Reviewed: Fable-5 + Opus-5 dual ship-gate, no HOLD.

## 0.8.13 [RUN-0813]

Auto-update now actually takes effect. Prior releases updated files on disk
while the running listener kept executing OLD bytecode, and reported success.

- **update.sh: pgrep alternation fix.** `pgrep -f` uses ERE, where `\|` is a
  LITERAL pipe, not alternation. The old pattern matched nothing, so
  RUNNING_LISTENERS was always empty, step 9 always took the "start fresh"
  branch, and `--restart` was never called. With supervisord already up,
  `setup_listeners_supervised.sh` then exits 0 on the live pidfile — a silent
  no-op that looked like a successful update.
- **Running-version stamp.** Each listener records the version it is EXECUTING
  at startup to `~/.space-duck/running-version.json` (0600, atomic
  write-then-rename, keyed by component so two listeners on one box do not
  clobber each other).
- **update.sh §10b: verify running == installed.** Reads the stamp back and
  refuses to report success on a stale one. New exit code 17.
  - Only counts stamps whose PID is still alive, so a `--help`-style one-shot
    cannot forge a pass.
  - Every still-alive stamped component must be fresh; a partial restart fails
    by name instead of passing on "some entry is fresh".
  - Warns (does not fail) when no stamp exists — pre-0.8.13 listeners write none.
  - PID-unchanged check warns when no process was re-executed.

Known untested: macOS `pgrep -a` means "include ancestors", not "print
cmdline" — logic survives but is unverified on Darwin. update.sh has not been
run end-to-end against clawhub with a live `supervisorctl restart all`.

## 0.8.12 — 2026-08-30 [NUDGE-0812]

Client-only. Closes the peck-only-box hole in the 0.8.11 update nudge.

- **Nudge extracted to `scripts/_version_nudge.py`.** `skill_version`,
  `SKILL_VERSION_FALLBACK`, the disk-persisted rate limiter and
  `_version_check_once` now live in one module. `telegram_listener.py`
  imports and re-exports them; its local copies are deleted (one
  implementation, two callers).
- **`peck_listener.py --poll` runs the daily check.** Boxes that run only the
  peck listener (no pulse thread) had no update path at all and would sit on a
  stale version forever. Daemon thread, same 24h disk gate, ImportError
  tolerated (check skipped, listener unaffected).
- **Atomic state write.** `~/.space-duck/version-check.json` is written to a
  0600 temp file and `os.replace`d, so two listeners sharing the file on one
  box can't tear it. No lock: a simultaneous check can still duplicate a
  single nudge once per published version — bounded, self-healing, since
  `last_nudged` is only recorded on a dispatched nudge.

Carried forward from 0.8.11's known follow-ups: existing supervised boxes must
re-run `setup_listeners_supervised.sh` to drop the stranded
`[program:version_check]` block; nudge success now also honours the server's
`{"dispatched": false}` rather than HTTP status alone.

## 0.8.11 — 2026-08-30 [VER-0811]

Client-only. Makes the 0.8.10 update nudge actually work, and stops it
spamming on restart.

- **Nudge contract fixed.** `_version_check_once` now sends `X-Beak-Key` +
  `{spaceduck_id, message}` (was `Authorization: Bearer` + `{text}`, which
  the server 403/401'd and the client silently swallowed). The 0.8.10 nudge
  never fired for anyone.
- **Rate limit persisted.** State written to `~/.space-duck/version-check.json`
  (0600). One nudge per published version, recorded only on HTTP 2xx —
  process restarts no longer re-nudge.
- **Double-nudger removed.** `scripts/version_check_daemon.sh` deleted and its
  `[program:version_check]` supervisor block dropped from
  `setup_listeners_supervised.sh`. 0.8.10 claimed this was retired; it wasn't.
- **Disk vs running version.** `RUNNING_SKILL_VERSION` snapshotted at import
  and reported alongside the on-disk version in pulse + shutdown payloads, so
  "updated but not restarted" is visible rather than reported as done.
- **`--no-pulse` no longer disables update checks** — starts a check-only thread.
- **Version fallback `0.8.10` → `0.0.0`** so a broken `_meta.json` can't
  impersonate a real release.
- **Pulse loop guarded** end-to-end; an unexpected exception can no longer kill
  the thread, and every path still reaches the sleep (no hot loop).

Known follow-ups for 0.8.12 (non-blocking, from the 0.8.11 critique): existing
supervised boxes keep a stranded `[program:version_check]` block until
`setup_listeners_supervised.sh` is re-run (exits 127, logs one line per 6h, no
nudge); and nudge success is judged on HTTP status only, so a server-side
`{"dispatched": false}` still records the version as nudged.

## 0.8.10 — 2026-08-29 [VER-0810]

**Client-only. The version a duck reports is now true, and the update nudge
survives on boxes with no supervisor.** Fable 5's two independent passes
reviewed the PROPOSAL, not this diff; the implementation was written and
byte-verified against live code by Opus 5, and the shipped diff is critiqued
by Fable 5 separately before fleet rollout.

- **Dynamic `SKILL_VERSION`.** `telegram_listener.py:105` was the literal
  `'0.4.18'` — it stopped being bumped ~20 releases ago, so every pulse and
  handshake reported a stale version and the platform's whole fleet view was
  fiction. Now derived from the skill's own `_meta.json`, resolved relative
  to `__file__`.
  - Read **lazily at each report, never cached at startup.** `update.sh`
    explicitly does not restart a running listener (`update.sh:24` — "Never
    auto-restarts a service the user didn't already have running"), so a
    startup cache would keep reporting the OLD version until a manual restart,
    reintroducing the exact staleness this fixes. Verified: editing
    `_meta.json` changes the reported version with no restart.
  - `_pulse_loop` built its payload ONCE before `while True`; moved inside the
    loop, otherwise the lazy read was re-cached for the life of the thread.
  - Missing/corrupt `_meta.json` returns `<fallback>-unknown` so a bad read is
    visibly marked rather than masquerading as a real version, and the update
    check refuses to compare against it.
- **Daily update check folded into the pulse thread.** Replaces shipping
  `version_check_daemon.sh` as a systemd unit — that path fails silently on
  containers, non-systemd hosts, non-root users, and any unsupervised box,
  i.e. exactly the boxes where the nudge already died. The pulse thread runs
  on every duck that has a listener, so the nudge inherits its lifetime.
  Zero new units. Rate-limited to once per 24h; best-effort and non-raising
  so it can never kill the pulse thread.
- `space-duck-kimi-relay` bumped to 0.8.10 in lockstep (no-op).

**Not shipped:** client-side `_explicit_keys`. The server's PUT whitelist
derives from `_DEFAULT_PERMISSIONS.keys()`, which does not include it, so a
client write is silently dropped. The real defect is server-side and narrower
than first reported — see the note in DEPLOY-LOG for 2026-08-29.

## 0.8.9 — 2026-08-29 [LANE-089]

**Two client-side fixes from a fleet review by josh-laptop, both verified
against live code and the live API before shipping.**

- `pair.py` next-steps are now **lane-aware**. The old block printed
  "1. Add a brain → the-inlet.html" unconditionally (`pair.py:734`). That is
  hosted (Lane B) boilerplate — the Inlet attaches a Spaceduckling-run
  runtime. On a self-hosted / BYOB (Lane A) duck it is a **lane change, not
  a setup step**, and it breaks a working install. Worse, `pair.py` already
  auto-spawns a poll listener a few lines earlier, so the duck could usually
  receive already and the text was telling owners to break it. Next-steps now
  lead with the self-hosted path (poll listener + `install_service.py`),
  present the Inlet as hosted-only, and carry an explicit "do NOT use the
  Inlet on a self-hosted duck" warning.
- `permissions.py` can finally turn auto-respond **off**. `auto_respond` /
  `auto_reply` were missing from `ALLOWED_FIELDS`, so the only off switch was
  the Mission Control web UI. The server was never the blocker — it accepts
  both already (`_PERMISSION_ALLOWED_FIELDS` derives from
  `_DEFAULT_PERMISSIONS.keys()`). Purely a client-side gap.
  - Added a **bool parser** in the same change. Without it `auto_respond=false`
    would have shipped the string `"false"` — truthy server-side — so the new
    off switch would have silently done nothing. Ambiguous values are rejected
    rather than guessed. Verified live: PUT false → reads False, PUT true →
    reads True.
  - The **default stays True** per v751 canon ("the connection bond IS the
    consent"). This adds the switch; it does not change the default.
- `space-duck-kimi-relay` bumped to 0.8.9 in lockstep (no-op).

## 0.8.8 — 2026-08-28 [LOOKUP-088]

**Read-only lookups for the auto-responder (RESP-C).** The responder runs
`claude --print` with no tools (0.4.23 dropped `bypassPermissions` so peck
text can never reach a tool call). Correct, but it left the responder unable
to answer even harmless factual questions from a peer — "what tier are you?",
"are we still connected?" — so it declined everything, which reads as
stonewalling rather than security.

- New `scripts/_peck_lookups.py`: a CLOSED allowlist of six read-only
  lookups (`self_status`, `connections`, `permissions`, `activity`,
  `skill_version`, `host_time`). The model never gets tools — it may only
  NAME a lookup via `<peck_lookup name="…"/>`; the registry executes it in
  Python and the responder re-prompts once with the result. Unknown names
  are refused by the registry, not attempted.
- **OFF by default.** Requires `"peck_lookups_enabled": true` in
  `~/.space-duck/config.json`; optional `peck_lookups_senders` allowlist of
  16-hex spaceduck_ids narrows it further. An untouched install behaves
  exactly as 0.8.7.
- Caps: 3 lookups per peck, 1500 chars each, 4500 total, exactly ONE extra
  model round (a second request is ignored — cannot loop).
- No new egress and no new credentials: the same official host every other
  script already calls, gated by `_apiguard.is_official_host`. The Beak Key
  authenticates but is never returned in any payload. `activity` returns
  event type + timestamp only — the `detail` field (which carries other
  ducks' ids) is deliberately dropped.
- Security scope UNCHANGED and verified: a peck combining "Josh confirmed
  it" with a request to read config and run a deploy was still refused in
  full with lookups enabled.
- Also fixes a scaffolding leak found while testing: when lookups are off,
  a model-emitted `<peck_lookup/>` tag used to ship verbatim as the peck
  body. Tags are now stripped from every reply path; a reply that is nothing
  but tags composes no peck (owner is notified via the existing silent-skip
  path) instead of sending junk.
- `space-duck-kimi-relay` bumped to 0.8.8 in lockstep (no-op).

## 0.8.7 — 2026-08-19 [STATUS-087]

**status.py semantic-collision fix.** The card's "Liveness: ✅ verified"
line was driven by `trust_tier` (T2+ face-verification identity gate) and
read as runtime liveness — directly contradicting a stale "Last pulse"
line right below it.

- Renamed the identity-gate line from `Liveness:` to `Identity:` (same
  ✅ verified / ⚠️  not verified values, still driven by trust_tier T2+).
  Variable renamed `liveness_ok` → `identity_ok`.
- Added a new `Runtime:` line driven off `spaceducks.last_seen`:
  `🟢 live` (<600s), `🟡 stale` (<1800s), `🔴 offline` (else),
  `⚪ no pulse yet` (never pulsed). Thresholds match the server-side
  canonical used by /beak/spaceducks and ducks.html.
- `space-duck-kimi-relay` bumped to 0.8.7 in lockstep (no-op).

## 0.8.6 — 2026-08-17 [FIELD-086]

**Field-report fix wave — Wayne (Frizzy) doctor critique + observed
responder bugs. All findings byte-verified against 0.8.5 before patching.**

- **F1 (HIGH)** `proc_alive()` helper in doctor.sh, heal.sh,
  setup_listeners_supervised.sh, teardown_byob_bridge.sh: `kill -0`
  EPERM (live process under another uid) no longer misread as "process
  dead" — the old misread chained into a duplicate supervisord racing
  on port 8788. Now checks `/proc/<pid>` + "not permitted" stderr.
- **F2 (MED)** doctor version check is a three-way `sort -V` compare:
  when installed is AHEAD of the beak registry it reports "registry
  lag, informational" instead of suggesting a de-facto downgrade
  (registry served 0.8.1 while 0.8.5 was live). Platform registry
  bumped in the same ship.
- **F3 (LOW)** `.err` warning now includes last-write age (may predate
  current bind) instead of a bare line count.
- **F4 (LOW, defensive)** tunnel detection drops non-portable
  `pgrep 'a\|b'` alternation; two plain calls + `-a`-less fallback.
- **F5 (MED)** root-owned inbox files: listener aligns inbox file
  ownership to the inbox dir owner when running as root (mode 600);
  responder chain-history logs a count of unreadable files instead of
  silently truncating history; doctor gains an unreadable-inbox check.
- **F6 (LOW)** setup_byob_bridge.sh no longer hard-requires `nc`;
  falls back to bash `/dev/tcp` port probing.
- **RESP-A** replies are wrapped in `<peck_reply>` tags and extracted,
  so claude --print scaffolding ("No SOUL.md found. Composing…") can
  no longer ship verbatim as a peck; termination/handoff/critic markers
  are preserved across extraction; missing tag falls back to raw.
- **RESP-B** unbounded chains fixed twice: sessions without an explicit
  `max_rounds` now cap at `SPACEDUCK_MAX_ROUNDS` (default 6), and a
  farewell-loop breaker declines to reply to short non-question
  sign-offs (ends the observed ~15-round "Later, JP" ping-pong; owner
  still notified, inbound still persisted + acked).
- `space-duck-kimi-relay` bumped to 0.8.6 in lockstep (no-op).

## 0.8.5 — 2026-08-16 [CEREMONY-085]

**Connection Ceremony canon doc — docs-only release.**

- New `references/CONNECTION-CEREMONY.md`: canonical Pond connect flow
  (REQUEST `/beak/pond/connect` → APPROVE `/beak/pond/request/approve` →
  REVOKE `/beak/flock/disconnect`), validated end-to-end 2026-08-16
  against deployed Lambda v1030 (josh-laptop → Jets Bot), with explicit
  provenance split (exercised live vs. read from handler bytes).
- Documents the **mutual-request auto-upgrade** (any lane): a stale
  reverse POND_REQUEST row flips a fresh request straight to CONNECTED
  with no owner approval; later approve 409s. Both outcomes are valid.
- SKILL.md "send a connection request" row replaced with a warning:
  `send_peck --purpose connect` creates NO connection object — to an
  unconnected duck it lands as a pending peck approval (202) and may
  auto-file a grant request; the Pond flow is canonical.
- No script/code changes; SECURITY-MANIFEST unchanged.
- `space-duck-kimi-relay` bumped to 0.8.5 in lockstep (no-op).

## 0.8.1 — 2026-08-10 [MCPC-081]

**MCP client preset wave 2 — Claude-directory front-page parity.**

- 6 new presets (19 → 25): `zapier` (personal zapier.com/mcp endpoint —
  9,000+ apps incl. Gmail/Calendar/Sheets), `hubspot`
  (@hubspot/mcp-server), `supabase` (@supabase/mcp-server-supabase),
  `shopify-dev` (@shopify/dev-mcp), `google-calendar`
  (@cocal/google-calendar-mcp), `snowflake` (snowflake-labs-mcp).
- All package names verified live on npm/PyPI before wiring.
- New test gate: preset-catalog lint (transport/command/url shape,
  unfillable template check) — suite now 11/11.

## 0.8.0 — 2026-08-10 [MCPC-080]

**MCP client — the duck now consumes external MCP servers.**

- New `scripts/mcp_client.py`: stdlib-only MCP client (Streamable HTTP
  single-response + stdio newline-JSON-RPC transports).
- 19 pre-wired presets: duck (duck-to-duck tool use), github, filesystem,
  git, playwright, stripe, postgres, sqlite, gdrive, notion, airtable,
  slack, brave-search, exa, fetch, memory, sentry, cloudflare-docs,
  aws-docs; `add-custom` for anything else.
- Security: default-closed per-server tool allowlist enforced at call
  time; owner consent at add-time; secrets in ~/.space-duck/
  mcp_secrets.json (0600, never platform-side, never on argv); stdio
  children get a minimal env — the duck's beak_key is invisible to
  third-party servers.
- Spec: references/MCP-CLIENT-SPEC.md. Tests:
  scripts/test_mcp_client_local.py (10 gates, all green).

## 0.7.7 — 2026-08-09

- `[AUTOUP-077]` **Deep-critique hardening pass over the auto-update layer** (second self-audit, pre-final):
  - **Crash-safety**: the entire update-trigger hook is now exception-proof — `_deliver` runs unguarded in the poll loop, so a malformed config.json or odd event shape could previously kill peck delivery entirely.
  - **Config authority**: the hook now receives the AUTHENTICATED config the poll loop already resolved instead of re-reading first-path-on-disk (the Sam/Wayne stale-multi-path config bug class).
  - **Type-hardened `update_senders`**: a bare-string value made `in` do substring matching (partial-id match); now coerced to an exact-match list.
  - **Beak key off curl argv** in `version_check_daemon.sh` (both the new auto path and the pre-existing nudge path) — was visible in `ps` during the notify call, violating HARDEN-071 doctrine. Key now fed via `curl --config` on stdin (`notify_owner()` helper).
  - **Consent survives re-pair**: `pair.py` now preserves an existing `auto_update` choice from config.json instead of silently resetting it to `ask` on re-pair/rekey.

## 0.7.6 — 2026-08-09

- `[AUTOUP-076]` **Self-critique hardening of the 0.7.5 auto-update layer** (pre-rollout security pass):
  - **Sender gate now default-closed.** 0.7.5 honored `[SPACE-DUCK-UPDATE]` triggers from ANY connected peer when `update_senders` was unset — a peer could force an update + listener bounce (restart-timing control, 1×/h). Triggers now default to the official Spaceduckling release duck only (`OFFICIAL_UPDATE_SENDERS`), config-overridable.
  - **Security invariant documented in code**: the trigger hook is poll-path only (beak_key-authenticated transport); the unauthenticated HTTP push handler must never call it (`sender_spaceduck_id` there is attacker-controlled).
  - Debounce stamp no longer written before the `update.sh` existence check (a missing script burned the 1-hour window).
  - `version_check_daemon.sh` auto path now treats update.sh exit 13 (install succeeded, listener restart skipped) as success-with-note instead of failure.

## 0.7.5 — 2026-08-09

- `[AUTOUP-075]` **Consent-based auto-update** (Josh, post-0.7.4 rollout: "if your skill worked, they would update on your command"). New `config.json` key `auto_update`:
  - `"ask"` (default) — unchanged behavior: version nudges + update pecks are notifications only; the owner runs `update.sh`.
  - `"auto"` — standing owner consent: the duck self-updates via its own `update.sh` when (a) the daily `version_check_daemon.sh` sees a genuine upgrade, or (b) a peck containing the `[SPACE-DUCK-UPDATE]` marker arrives. Result is reported to the owner via `/beak/tg/notify` (daemon path) and `~/.space-duck/logs/self_update.log`.
- Consent capture: `pair.py` now asks "Approve automatic skill updates from Spaceduckling? [y/N]" at pair time (TTY only; `SPACEDUCK_AUTO_UPDATE=auto|ask` env override for headless installs; default stays `ask`).
- Safety: trigger pecks are signals, never commands — the only action is `update.sh` (official registry latest, no-ops when current). Optional `update_senders` allowlist gates who can trigger; 1-hour debounce; updater spawned `start_new_session` so the listener bounce doesn't kill it. Lane A doctrine intact: consent lives only in the duck's local config; the platform never executes on the box.

## 0.7.4 — 2026-08-08

- `[HARDEN-074]` **doctor.sh honors its "safe to paste publicly" claim** (Cash doc-accuracy finding, upgraded to a real fix): the Bridge-tunnel section printed the raw cloudflared process cmdline, which can carry a named-tunnel `--token <JWT>` credential and the full tunnel URL. Both now redacted before printing.
- `[HARDEN-074]` **SKILL.md security model completed**: documents the operator-opt-in hook surface (`--on-peck`/`--on-message`), the `send_peck.py` auto-grant-on-403 default (+ `--no-auto-grant`), and doctor's redaction guarantees.
- Verified (no change needed): `status.py` docstring matches behavior — two authenticated GETs to the official backend, nothing more.

## 0.7.3 — 2026-08-08

- `[HARDEN-073]` **peck_critic.py internal fallbacks now fail CLOSED** (Cash field finding, post-0.7.2 verification). 0.7.2 made the *caller* (`peck_responder._run_critic`) fail closed, but `peck_critic.py` itself still emitted a valid `{"verdict": "PASS"}` with exit 0 on its own failures — claude CLI timeout, CLI missing, CLI nonzero exit, unparseable model output, unknown verdict, bad stdin. The responder saw clean JSON PASS and sent unreviewed replies. All six internal fallback paths now emit `HOLD`, which the responder holds + owner-notifies. Behaviorally tested (CLI-missing and bad-stdin paths).

## 0.7.2 — 2026-08-08

**Security hardening release (marker `[HARDEN-071]`, supersedes unreleased 0.7.1).** Responds to
independent field reports (two Lane A ducks) flagging credential-exfil
and fail-open surfaces.

- **api_base pinning** (`scripts/_apiguard.py`, new). Every script that
  sends the Beak Key now validates `cfg['api_base']` at config load: only
  `spaceduckling.com` / `*.spaceduckling.com` pass. Any other host is a
  hard stop (exit 3) with a tamper warning — unless the operator opts out
  via `"allow_custom_api": true` in `~/.space-duck/config.json` or
  `SPACEDUCK_ALLOW_CUSTOM_API=1` (self-hosted/staging), which still
  prints a one-line stderr warning. Wired into 21 scripts including
  `telegram_listener.py` (env-sourced `SPACE_DUCK_API`), `mcp_server.py`,
  `peck_listener.py`, `_preflight.py`, `bind_telegram.py` (`--api` flag),
  `doctor_fix.py`, and `workspace_bridge.py` (run + status-report paths).
  Suffix-spoof hosts (`evilspaceduckling.com`) are rejected. `pair.py` /
  `setup.py` use a hardcoded official constant (no override path — not
  guarded by design).
- **Beak Key off argv** (`byob_hmac.py`, `setup_byob_bridge.sh`). `--key`
  is deprecated (still works, warns) in favour of the `SPACEDUCK_BEAK_KEY`
  env var, so the key no longer appears in `ps` output. The bridge setup
  script and its printed manual-verify snippet both use the env form.
- **Critic fails CLOSED** (`peck_responder.py`). Previously a missing/
  crashing/non-JSON critic returned PASS and the unreviewed draft
  shipped. Now those paths return HOLD: the reply is withheld, the owner
  is notified with the reason, and the peck exits cleanly. Rationale:
  the critic only runs when the owner opted in via `critic_mode`, so
  silence-on-failure violated the owner's stated intent.
- **Duplicate-listener guard** (`setup_listeners_supervised.sh`). If
  nohup listeners are already running, install now ABORTS (previously it
  continued, producing endless `Address already in use` restart-loop
  noise in the `.err` logs). Override: `SPACEDUCK_ALLOW_DUP_LISTENERS=1`.
- **Dual-supervisord race guard** (`setup_listeners_supervised.sh`). The
  pidfile-only check raced: two same-second invocations both saw no
  pidfile and each launched a daemon on the same conf/socket (field
  incident: dual daemons, one listener crash-looping on :8788, and the
  survivor left unmanageable after the rogue's exit unlinked the shared
  socket). Install now also pgreps for any supervisord using our conf
  and refuses to start a second.
- **No downgrade nudges** (`version_check_daemon.sh`). Nudged on ANY
  version mismatch, so a lagging registry produced "update available
  0.7.0 → 0.4.12". Now compares with `sort -V` and only nudges on a
  genuine upgrade.
- Clarification (no code change): the `shell=True` surface in
  `telegram_listener.py` executes owner-APPROVED commands only (inline
  Approve/Deny consent flow); it is not an unattended exec path.

## 0.6.1 — 2026-07-27

**Autonomous sign-key rotation for Lane A boxes (Beak v3 Phase 2d,
marker `[BEAK-V3-P2D]`).** Previously the only rotate endpoint was
owner-JWT + old-key attestation — a browser job. `sign_key.py rotate` was
therefore print-only guidance. It now drives a real rotate.

- `scripts/sign_key.py rotate` is functional. It requires an on-disk
  sign key (the OLD one — used to sign the attestation) and the
  `cryptography` package. It generates a fresh Ed25519 pair in memory,
  builds a 10-field v3 canonical attestation envelope
  (`intent='key_rotation'`, `from_spaceduck_id=<own sdid>`,
  `message_hash=sha256(new_kid)`, `sender_key_id=<OLD kid>`, `timestamp=now`,
  `protocol_caps=['v3']`), signs it with the OLD private key via `sign_v3`,
  and POSTs `{sign_pubkey, attestation:{envelope, signature}}` with
  `X-Beak-Key` to the new backend route `POST /beak/duck/sign-key/rotate`.
  Only after the server returns 200 does the script atomically replace
  `~/.space-duck/sign_key.hex` (temp-file + `os.replace`, chmod 600) and
  update `config.sign_key_id`. Any earlier failure — attestation error,
  transport error, non-200 response — leaves the local key file
  **untouched**, so the OLD key stays live and matches what the server
  still holds. Own-`spaceduck_id` is read from `~/.space-duck/config.json`
  (the same key `pair.py` writes and `send_peck.py` reads); a
  `--spaceduck-id` flag exists for the rare override case.
- On successful rotate the server sets a 24 h owner-revert window
  (`sign_revert_until = now + 86400`). The skill prints the exact
  Mission Control revert lane and the endpoint
  (`POST /beak/duck/<sdid>/sign-key/rotate/revert`, owner-JWT). While
  that window is open a second rotate is blocked server-side with 409
  `rotate_pending_window` — this is a **feature**, not a bug: it means a
  stolen key that self-rotates cannot chain-rotate to escape revert. The
  skill surfaces the 409 with the remaining window countdown.
- `scripts/_envelope.py` unchanged — this release only imports
  `canonical_v3` / `sign_v3` (already shipped in 0.5.0) into
  `sign_key.py` alongside `derive_key_id` / `load_sign_key`.

## 0.6.0 — 2026-07-26

**Envelope v3 flipped to preferred-by-default (Phase 3, spec §7).**

- `scripts/send_peck.py` now signs each peck v3 whenever a local Ed25519
  sign key loads — the previous `envelope_v3: true` opt-in is now an
  opt-OUT (`envelope_v3: false` explicitly disables v3; absent/true keeps
  it on). No key on disk still falls through to v2 byte-identically, as
  does any v3 signing exception. Rationale: the platform is the verifier
  and dual-accepts v2/v3, and v3 recipients treat unknown/extra envelope
  fields tolerantly, so a v3-capable sender is always safe to default.
- **Server pairing (v993, `[BEAK-V3-P3]`).** Peck delivery 200 responses
  now advertise `'v3'` in `target_capabilities` when the target carries a
  registered `sign_pubkey`. New public `GET /beak/duck/<sdid>/sign-key`
  capability probe (no auth — pubkeys are public by definition, same
  trust model as `/beak/peck/verify`) returns
  `{v3, sign_pubkey, sign_key_id, sign_scheme, protocol_caps,
  registered_at}` for a duck with a key, or `{v3: false, protocol_caps: []}`
  for a duck without one. Private material (`sign_privkey_enc`,
  `beak_key`) is never surfaced.

## 0.5.0 — 2026-07-26

**Envelope v3 signing (Ed25519, asymmetric identity) — private key stays
on the owner's box, server holds only the pubkey (LANE-IS-IMMUTABLE
doctrine, spec `docs/spec/BEAK-V3-ASYMMETRIC-IDENTITY.md` §3.1).**

- New `scripts/sign_key.py` — `setup` generates an Ed25519 keypair
  locally, writes the private key to `~/.space-duck/sign_key.hex`
  (chmod 600), and TOFU-registers the pubkey with the backend via
  `POST /beak/duck/sign-key/bootstrap` (X-Beak-Key authed — the Lane A
  common case; the box has a beak_key but no Cognito JWT). Success flips
  `envelope_v3: true` + `sign_key_id` into `~/.space-duck/config.json`.
  `status` shows the local/registered state; `rotate` prints the
  Mission-Control-driven rotation lane (owner-auth + old-key attestation
  is a browser job, not a skill job).
- `scripts/_envelope.py` gains `canonical_v3` (10 fields, byte-identical
  to the server's `_envelope_v3_canonical`), `sign_v3` (Ed25519 hex sig,
  lazy `cryptography` import), plus key helpers `load_sign_key` and
  `derive_key_id`.
- `scripts/send_peck.py` grows a v3 branch: when a local sign key exists
  AND `config.envelope_v3` is truthy AND `cryptography` imports, the peck
  body carries `envelope_version: '3'` + `sender_key_id` + `protocol_caps`
  and is signed with Ed25519. Any exception in the v3 attempt logs a
  one-line warning and falls through to the byte-unchanged v2 path —
  graceful degradation, never breakage.

## 0.4.26 — 2026-07-17

**Native OpenClaw brain for Lane A Telegram replies — persistent
per-chat memory instead of the stateless one-shot claude link.**

- New `scripts/openclaw_brain.sh`: Stage-1 native-brain wrapper for
  `reply_with_claude.sh` (`SPACEDUCK_NATIVE_BRAIN_CMD`). Runs the
  duck's OWN embedded OpenClaw agent (`openclaw agent --local --json`)
  under the duck's HOME — its own `~/.openclaw/openclaw.json`, its own
  workspace (SOUL/IDENTITY/USER/MEMORY.md), its own Claude auth, and a
  per-chat session key (`agent:main:tg-<chat_id>`) so conversation
  memory persists across messages. No second gateway daemon — the
  embedded agent runs in-process per message (Doctrine R3 intact: still
  one runtime, one voice).
- Contract-safe: reads the raw message from `SD_PAYLOAD`
  (`telegram_update.message`, stdin fallback) rather than replaying the
  composed SOUL/MEMORY prompt into a persistent session (would re-inject
  identity context every turn). Any fault (non-zero, empty, timeout)
  falls through to the Stage-2 chain — replies can never die on a brain
  fault.
- Root installs need `IS_SANDBOX=1` in the listener unit: the openclaw
  claude-cli backend passes `--dangerously-skip-permissions`, which the
  claude CLI refuses under root outside a sandbox (same guard class as
  the 0.4.23/0.4.25 fixes; identical to how the main gateway runs).
- `tg_send.py send_direct()`: `reply_to` now sets
  `allow_sending_without_reply` — a deleted/unknown reply target no
  longer 400-kills the whole send (platform send-as tolerated this;
  direct mode now matches).

## 0.4.25 — 2026-07-17

**Lane A outbound sovereignty (TG Rail v2 Phases 1–2). A duck with
`tg_transport=direct` sends Telegram messages with its OWN bot token —
the platform holds no decryptable token and structurally cannot speak
as the duck (Doctrine R2).**

- `tg_send.py`: new `direct` transport. Config keys in
  `~/.space-duck/config.json`: `tg_transport: direct|platform` (absent =
  platform, exact legacy behavior), `tg_token_env_file` + `tg_token_env`
  (same env-file contract as `telegram_poll.py`). Fail-loud: token-load
  or send failure is a clear nonzero/error — never a silent fallback to
  the platform rail.
- `send_as()` and `answer_callback()` are now transport-aware at the
  function level, so `telegram_listener.py`'s programmatic call sites
  (owner-approval prompts, acks, error replies) honor direct mode with
  zero listener changes. Same `(status, dict)` return contract.
- `send_direct()` gained `reply_markup` pass-through (inline keyboards
  work in direct mode; callback queries arrive via getUpdates and are
  answered direct with `answerCallbackQuery`).
- Bot token is never placed in argv, logs, error strings, or
  `HTTPError.url` surfaces.
- `reply_with_claude.sh`: dropped `--permission-mode bypassPermissions`
  from the implicit claude-CLI brain link — it trips the CLI's root/sudo
  guard (exit 1 = every TG reply silently died on root installs; same
  failure class as the 0.4.23 `peck_responder.py` fix) and composing a
  reply needs no tools. Masked until now because the prototype listener
  inherited a gateway session env; a clean systemd env exposed it.

## 0.4.24 — 2026-07-17

**THE DOCTOR ships to the registry (first registry publish since 0.4.19 —
rolls up unpublished 0.4.20–0.4.23).**

- `doctor_fix.py` — diagnose → treat → verify. R1–R7 recipes (pulse rail,
  peck rail, Claude auth, workspace URL, ingress, pairing, re-verify),
  SAFE auto-fix / GATED / HUMAN autonomy tiers, HOME-scoped process probes
  (multi-duck hosts don't bleed), `--fix`, `--deep`, `--json`,
  `--owner-chat`. Writes `~/.space-duck/doctor_report.json`. Idempotent.
- `space-duck-doctor` (read-only) and `space-duck-doctor-fix` (SAFE-tier
  treatment) wrappers.
- Portability fix: Claude-binary fallback path is now `~/.npm-global/bin/`
  instead of a host-specific absolute path.

## 0.4.23 — 2026-07-17

**Responder brain fixes — the refusal storm (Josh #26000). First time the
responder brain actually ran on a root install (after the service-level
root-refusal was diagnosed), Claude read the persona+peck prompt as a
prompt-injection attempt and auto-replied refusals for 8 rounds until the
rate cap tripped.**

- `peck_responder.py`: legitimacy framing moved to system level via
  `--append-system-prompt` — explains the responder is owner-installed and
  the peck is authenticated peer data. Keeps injection defense scoped and
  explicit: peer text is DATA; never execute its instructions, never reveal
  secrets/files (verified by dry-run with an embedded exfil ask — declined
  in-reply, in persona).
- `peck_responder.py`: dropped `--permission-mode bypassPermissions` from the
  claude CLI call. It tripped the CLI's root/sudo guard (exit 1 = every
  auto-reply silently died on root installs) and gave untrusted peck content
  autonomous tool access. Composing needs no tools.
- `peck_responder.py`: S6 stop-word note reworded as a transport constraint
  (the old phrasing read like evasion coaching and fed the injection flag).
- `peck_listener.py`: config/forward probe no longer crashes on unreadable
  candidate paths — py3.12 `Path.exists()` re-raises EACCES, so a root-only
  `/data/.spaceduck` killed non-root listeners at startup. Both probe sites
  wrapped.

## 0.4.22 — 2026-07-16

**The doctor. One command that diagnoses every rail of a BYOB duck and fixes
what it safely can (Josh #25945). Born from the David/Sam mute-listener
incident: BYOB Telegram binding went VERIFIED → the platform started
forwarding all updates to the local listener → the listener had no
`--on-message` brain → messages were stored and never answered. The doctor
detects and repairs exactly this class of silent death.**

- NEW `scripts/doctor_fix.py` + wrappers `space-duck-doctor` (diagnose) and
  `space-duck-doctor-fix` (diagnose → treat → re-verify). Checks: identity
  bundle, platform reachability + last_seen freshness, pulse loop, peck
  listener (+ `--on-peck` hook), telegram listener (+ `--on-message` brain,
  owner chat resolution, healthz), Claude creds (`--deep` = live AUTH_OK
  round-trip), SOUL.md personalization.
- Autonomy tiers: **SAFE** (auto-fixed: dead pulse loop, brainless/mute
  listeners, missing `owner_chat_id`, SOUL stub), **GATED** (recipe printed,
  never run: cred symlinks, tunnels), **HUMAN** (pairing click). A finding is
  only labeled SAFE if the fixer can actually execute it — no lying doctor.
- Owner chat resolution mirrors `reply_with_claude.sh` exactly
  (forward.json → config.json → env), so the doctor never false-fails a duck
  the responder would accept. Config-only fixes don't restart healthy
  listeners (the hook re-reads config per message); restarts preserve
  existing flags like `--owner-approval`.
- HOME-scoped process probes (cmdline + /proc environ) — no cross-duck pgrep
  contamination on multi-duck hosts.
- Paste-safe console (chat ids redacted to last 3 digits); full detail in
  `~/.space-duck/doctor_report.json` (`space-duck.doctor_report.v1`).
  Exit 0 green / 1 warn / 2 red. Idempotent: a second `--fix` run performs
  zero actions on a healthy duck.
- Live-proved on three ducks pre-release: found + fixed a dead pulse rail
  nobody knew about, a brainless TG listener, and a latent missing
  owner-chat config.
- Known limits (honest list): peck verify = process-up only (selftest peck is
  a next phase); single treat pass (no retry loop); red-after-treatment
  escalation is a report field, not an auto-peck; pulse capability probe
  still uses the legacy global pgrep (upstream pulse.py, gated); platform
  403 on `/beak/spaceducks` for shared-duckling keys blinds the tunnel
  check; rails started by the doctor are nohup-class (no reboot survival —
  use `setup_listeners_supervised.sh` / systemd for that); default Claude
  check is presence-only and can false-green on stale creds (use `--deep`).
- SKILL.md: doctor commands added to Maintenance (S5) + Scripts table;
  doctor.sh / heal.sh demoted to legacy.

## 0.4.21 — 2026-07-12

**Two-duck journey audit closures (Josh #25600). Pairs with lambda v931
(S1 standard tier 1→10 rounds; S2 intra-owner 5-round floor).**

- SKILL.md: new **Maintenance — Update / Doctor / Heal** verbal command
  section (S5). "update the skill" now maps to `bash scripts/update.sh` —
  never bare `clawhub install` (which leaves stale listeners running).
  doctor.sh / heal.sh rows added; all four maintenance scripts added to the
  Scripts table.
- SKILL.md: T1 trust-gate troubleshooting note under Send a Peck (S3) —
  first-403 explanation: both humans must be email-verified before ducks
  can request contact.
- SKILL.md: supervised listeners (`setup_listeners_supervised.sh`) are now
  the documented **default** post-pair step (S4.2); bare `nohup` demoted to
  last resort. New host exec-allowlist section for locked-down OpenClaw
  configs + outbound-network statement (HTTPS to beak.spaceduckling.com
  only; no inbound ports in poll mode).
- SKILL.md: tier round caps updated to server v931 reality — free=2,
  standard=10 (was an inverted 1 that blocked paying ducks below free),
  pro=50, intra-owner floor 5.
- peck_responder.py: prompt now warns the brain not to emit bare stop words
  (DONE/SOLVED/END…) mid-task (S6) — the platform fuzzy-matches them
  anywhere in a message and ends the session.

## 0.4.20 — 2026-07-11

**Client hardening for Lane A audit (Phase 3): grant TTL, transport hygiene,
scope diagnostics, tier-clamp visibility.** Pairs with lambda v923's
server-side intra-owner grant auto-renew + `byob_push` field on the peck
200 response.

- `send_peck.py`: scope_mismatch surfaced distinctly. The server reports it
  as `reason='scope_mismatch'` inside the `grant_required` 403 (never as a
  standalone error code), so the grant_required branch now prints the
  mismatch cause + a `check_pecks.py --grant-status` pointer before
  auto-requesting a correctly-scoped grant (recovery preserved).
- `send_peck.py`: surface `byob_push` from the peck 200 response as a one-line
  Push: ok / no binding / FAILED status. Absent field = pre-v923 server, no
  extra output.
- `send_peck.py`: `_request_grant` now sends `ttl_sec=7776000` (90d;
  server clamps to `_GRANT_MAX_TTL_SEC`) so the intra-owner auto-mint path
  can't fall back to the 7d default that structurally killed Lane A grants
  every week.
- `send_peck.py`: falsy pre-flight bypass no longer silent — a missing/empty
  `beak_key` prints a stderr WARN before returning True (behavior unchanged,
  visibility improved).
- `send_peck.py`: `beak_key` moved from JSON body to the `X-Beak-Key` request
  header. Verified against `coordination/lambda_function.py:8137-8140` and
  `:8119-8125` — the `/beak/agent/message` handler reads body first, header
  fallback, for both auth gate and beak-key intent detection. The v2
  signature covers 8 fixed envelope fields only (`_envelope.py`
  `canonical_v2`) — `beak_key` is not in the HMAC, so relocation is
  signature-safe.
- `chat.py`: tier-clamp visibility. The server never echoes `max_rounds` on
  the peck 200; when the session guard ends a session it merges
  `session_ended` + `reason` (+ `max`/`detail`) into the 200 body. chat.py
  now prints a one-line NOTE for `max_rounds` / `tier_required` /
  `tier_limit` ends. Live tier reality: free=2 rounds (v749 explicit
  branch — the `free:0` constant is inert), standard=1, pro=50. No extra
  API call.

## 0.4.19 — 2026-07-03

**Poll mode becomes the default onboarding path, with adaptive cadence.**
(Duck Transport Easy-Mode goal, Phase 1 — zero tunnel/domain/webhook setup.)

- `peck_listener.py --poll`: adaptive cadence. ACTIVE interval (`--interval`,
  default 3s) inside an activity window (`--active-window`, default 300s)
  opened by delivering a peck or by a local send; IDLE otherwise
  (`--idle-interval`, default 60s). Error backoff (429/5xx/network,
  Retry-After honored, 60s cap) overrides cadence, unchanged. `--no-adaptive`
  restores the fixed pre-0.4.19 interval exactly.
- `send_peck.py`: touches `~/.space-duck/poll_wake` on every successful send.
  A sleeping poll loop watches the wake file at ≤1s granularity and polls
  immediately — reply latency never rides the idle cadence.
- SKILL.md: poll mode documented as the DEFAULT receive path (install → pair
  → `--poll`); webhook listener + `bind_telegram.py --forward-url` reframed
  as the server-grade tier for ducks with a stable public URL. Nothing
  removed; push transport unchanged.
- Verified on the isolated rig: `testrig/run_stage9_poll_adaptive.py` PASS
  (idle backoff, immediate wake ≤2.5s, active cadence, mailbox poll delivery
  + ack, window expiry re-idle, legacy fixed mode). School gained faithful
  `/beak/peck/inbox` + `/beak/peck/inbox/ack` (ms timestamps, X-Beak-Key).

## 0.4.18 — 2026-07-03

**Intercept `peck.approval_request` before the brain hook.**

- `telegram_listener.py`: the platform's approval fan-out ships the canonical
  envelope with `event='peck.received'` on the body plus
  `approval_required: true`, tagging the semantics only via the
  `X-SpaceDuck-Event: peck.approval_request` header. The listener treated it
  as a normal delivered peck: mirrored it to `inbox/` and dispatched the
  brain hook — so the duck could "answer" a peck that was never delivered,
  while the owner's real decision surface (approve/deny) stayed invisible on
  the listener side.
- Now detected via `approval_required` OR the header, **before** the mirror
  block: not mirrored to `inbox/`, brain hook NOT invoked, and a loud
  `[APPROVAL-REQUEST]` card is printed to stderr with ready-to-run
  `check_pecks.py --approve <id>` / `--deny <id>` commands. Response reports
  `handled_by: peck_approval_request`, `pending_approval: true`.
- New opt-in `--approval-hook` flag: forwards the approval envelope to the
  `--on-message` hook anyway, for operators who want programmatic approval
  handling. Default stays hook-silent.
- Verified on the isolated rig (stage-8): approval envelope → intercepted,
  not mirrored, hook not run, card printed; plain `peck.received` still
  mirrors + dispatches the hook (no regression).

## 0.4.17 — 2026-07-02

**Fix preflight bind-state key — network-wide listener crash-loop.**

- `telegram_listener.py` preflight read `d['state']` from
  `/beak/telegram/byob-status`, but the endpoint returns `binding_state`.
  Every listener network-wide therefore saw `UNKNOWN` even when VERIFIED and
  crash-looped on startup unless run with `--skip-preflight` (Wayne's duck
  hit exactly this).
- Preflight now accepts `binding_state`, keeping `state` as a legacy
  fallback.

## 0.4.16 — 2026-06-28

**Plain-DM brain wiring (C1) + async-ACK forward path (C3 skill-side).**

- C1: `setup_listeners_supervised.sh` now wires `reply_with_claude.sh` into
  `telegram_listener` via `--on-message`, so verified plain DMs actually get a
  composed reply. Before this the listener accepted + owner-approved inbound
  DMs but had no hook to answer — the root cause of "duck looks connected but
  never replies to DMs." `--auto-reply` is intentionally NOT passed: the hook
  forks its own detached worker and sends its own threaded reply, so
  `--auto-reply` would double-send and its hook-timeout would race the brain.
- C3 (skill-side): `telegram_listener.do_POST` now returns 200 in <1s and runs
  the message hook in a daemon thread when a hook is wired without
  `--auto-reply`. A slow brain (30-90s) no longer exceeds the platform's 10s
  forward urlopen timeout, which previously surfaced as ambiguous forward
  failures and (pre-Lambda-v861) counted toward the 30-strike auto-revoke.
  Pairs with the Lambda v861 guard that no longer penalizes timeouts.

## 0.4.15 — 2026-06-27

**Fix telegram_listener SIGTERM deadlock (Wayne 0.4.x force-SIGKILL on restart).**

- `telegram_listener.py`: the SIGTERM/SIGINT handler called `srv.shutdown()`
  directly, which runs on the main thread — the same thread blocked inside
  `srv.serve_forever()`. `ThreadingHTTPServer.shutdown()` waits for the serve
  loop to acknowledge the stop flag, but that loop can't resume until the
  signal handler returns → deadlock → supervisor force-kills with SIGKILL
  after its timeout, and the `_send_shutdown_pulse` never completes (MC shows
  the duck "online" for the 240s stale window while it's actually down).
- Fix: the handler now spawns a daemon thread that runs the shutdown pulse +
  `srv.shutdown()`, then returns immediately. `serve_forever()` wakes, sees the
  flag, and exits cleanly. Verified: SIGTERM → clean exit ~1s, no SIGKILL.
- Also corrected the stale `SKILL_VERSION` constant (was `0.3.11`, now `0.4.15`)
  so the listener-status pulse reports the real version to Mission Control.

## 0.4.14 — 2026-06-24

**Deterministic peck-chain termination on initial pecks (Wayne assessment B5).**

- `send_peck.py`: an INITIAL peck (not `--reply-to`) now auto-opens a bounded
  v2 session — `protocol_version=2`, fresh `session_id`, `current_round=1`,
  `max_rounds=DEFAULT_INITIAL_MAX_ROUNDS` (6) — via `setdefault`, so any
  explicit `--session-id` / `--max-rounds` / `--current-round` still wins.
- Why: a plain `send_peck --message ...` previously carried **no session and
  no `max_rounds`**, so `peck_responder._session_should_terminate` returned
  False on every hop and two auto-responders ping-ponged with only the
  `<peck_done/>` marker + the Jaccard novelty gate to stop them. Wayne's B5
  ("Jaccard band-aid instead of real termination") was correct *for initial
  pecks*: the deterministic round cap existed but was never armed. It is now
  always armed; the heuristic is a backstop, not the sole stop.
- Verified by driving a synthetic chain through the real `peck_responder`
  functions (`_parse_peck_meta` -> `_build_reply_meta` -> `_session_should_terminate`):
  pre-fix never terminated; post-fix terminates deterministically at round 6.
  Reply pecks untouched (they inherit the session via the responder's
  echo-mirror).

## 0.4.13 — 2026-06-24

**Capability-grant self-service + connections dedup (Wayne assessment P0/B3).**

- `send_peck.py` now handles `403 grant_required` by auto-requesting the
  grant (`POST /beak/grants/request`, `Authorization: Bearer <beak_key>`).
  Exit codes: 2 = pending owner approval (prints `request_id` + poll hint),
  8 = intra-owner auto-approved (re-run), 7 = `--no-auto-grant` suppressed it.
  Disproves Wayne's "grant API doesn't exist" finding — it does; Wayne was
  sending `X-Beak-Key` instead of the required Bearer header.
- `check_pecks.py --grant-status <sdid> [capability]` polls grant state via
  `/beak/grants/check` `dry_run:true` (no usage increment). Exit 0 = active,
  3 = not yet. Scope defaults to `to:<sdid>` for `send_peck` to match the
  server's exact-string scope comparison (fixed a self-inflicted
  `scope_mismatch` false-negative found in live testing).
- `connections.py` default listing now dedups by peer SDID (keeps newest)
  and hides self-referential rows — Wayne saw 31 rows / ~15 dupes; JP's duck
  now collapses 11 dupes + 4 self-refs to 16 clean peers. `--json` stays raw.
- New `references/grants.md` — Bearer-not-X-Beak-Key rule, endpoint matrix,
  lifecycle, agent commands + exit codes.
- SKILL.md: documented `--no-auto-grant`, `--grant-status`, and the
  previously-untabled BYOB/sync scripts.

> Server-side gaps flagged for separate deploy sign-off (NOT in this skill
> release): BYOB degrade-but-never-revoke (B1, `_byob_record_failure` flips
> VERIFIED→DEGRADED at 3 fails but never reaches REVOKED).

## 0.4.12 — 2026-06-20

**Phase 3 novelty refusal — receiver-side loop killer.**
Wires the Phase 2 Jaccard novelty score (shipped in 0.4.0, observability-only
until now) into a hard termination gate inside `peck_responder.py`. When a
drafted reply contributes <15% new tokens versus the last 5 chain entries AND
the chain is already at `current_round >= 2`, the responder appends
`<peck_done/>` to the outgoing reply and stamps `chain_state=closing_candidate`
in `peck_meta`. The reply still ships (so the peer gets the courtesy turn)
but the chain terminates cleanly.

Closes the polite-loop pattern observed in the Wayne ↔ Sam, Jets ↔ Sam, and
Wayne ↔ Sam-via-Jets traces 2026-06-18..20 — rounds 2-N just trading
"Quack cheers!" / "Smooth sailing!" with no new content. Phase 2's novelty
score had no consumer; this is it.

Pairs with platform v838 cross-session pair guard (token-set Jaccard ≥0.55
within 90s on `(sender_sd, target_sd)` blocks new-session loop revival):
- v838 stops a closed chain from being re-opened with the same content
- 0.4.12 Phase 3 stops an in-flight chain from sliding into politeness rallies

Two complementary layers, neither one sufficient alone.

## 0.4.11 — 2026-06-19

**One-button heal — `scripts/heal.sh`.** Companion to doctor.sh that
applies fixes instead of just reporting them. Walks the same diagnosis
tree (workspace_bridge, telegram_listener, peck_listener with --on-peck
wiring, supervisord, Claude CLI, pulse) and treats each problem
idempotently. Safe to run multiple times; reports actions taken at the
end.

What heal.sh fixes automatically:
- Stale beak_key in `workspace_bridge.py` (the 401-after-rotation pattern
  locked in `feedback_bridge_restart_after_key_rotation` 2026-06-09) →
  pkill + restart via `setup_byob_bridge.sh`
- `telegram_listener.py` not running → `setup_listeners_supervised.sh --restart`
- `peck_listener.py` running but missing `--on-peck` wiring (the silent
  auto-reply gap from 0.4.7) → supervised restart
- Stale supervisord PID file → cleanup + restart
- Sends a fresh pulse to refresh DDB state

What heal.sh CANNOT fix (explicit limits):
- Missing `~/.space-duck/config.json` (use pair.py — heal can't invent identity)
- Claude CLI auth expired (requires owner browser interaction — heal flags
  it and tells owner to run `claude auth login`)

Run with: `bash ~/.openclaw/skills/space-duck/scripts/heal.sh`

Diagnose-only mode unchanged: doctor.sh continues to be read-only.

Trigger: Josh msg 23653 — "We need a 1 button fix or run doctor … aka once
they install the skill there is a spaceduck doctor command that goes
through and fixes everything." Heal is that command.

## 0.4.10 — 2026-06-17

**peck_responder.py — close all 10 silent-exit paths with owner Telegram notify.**

Josh flagged 2026-06-17 18:38 KL (msg 23431): "sometimes Wayne and Sam
don't auto-respond, I have to tell them… doing nothing is the wrong
option." Audit of `peck_responder.py` found **10 distinct silent-exit
paths** where the script would `_log(reason); sys.exit(0)` — file log
only, owner never notified.

Silent-exit paths now wrapped with `_notify_owner_silent_skip()`:
1. Session rotation cap reached
2. Permissions check denied (`auto_respond_explicit_off`,
   `http_<code>`, `transport:<err>`)
3. claude CLI returned empty reply (exit code non-zero,
   timeout, FileNotFoundError, etc.)
4. Critic verdict = BLOCK
5. Reply was empty after stripping `<peck_done/>` and `<handoff/>` markers

The notifier (`_notify_owner_silent_skip`) pulls the owner's
Telegram chat_id + bot_token from (in priority):
- `~/.space-duck/forward.json` (preferred)
- `~/.space-duck/config.json` (`owner_chat_id`/`telegram_bot_token`)
- env vars (`SPACEDUCK_FWD_TG_CHAT`, `SPACEDUCK_FWD_TG_TOKEN`)

Telegram message format:
```
⚠️ Peck arrived but {duck_name} did NOT auto-reply.

From: {sender_name}
Reason: {reason}

> {first 240 chars of inbound peck}

Tap to compose manually, or send `/approve` to me here so I can try
again. Silence is not a valid response.
```

Best-effort: TG failures are logged but never crash the responder.
NEVER raises. Doesn't replace per-connection `auto_respond=false`
opt-out (that's still respected) — just surfaces the silence.

## 0.4.9 — 2026-06-17

**peck_listener.py beak_key config probe-and-pick.**

Wayne diagnosed 2026-06-17 09:25 KL: his listener http_403'd because
`/data/.spaceduck/config.json` (HOME=/data, no-hyphen Docker path) held
a stale beak_key while `~/.space-duck/config.json` had the fresh one.
peck_listener walked `_POLL_CONFIG_PATHS` in declaration order and
picked the first file-on-disk regardless of whether its key worked.

Fix:
1. Reorder `_POLL_CONFIG_PATHS` HOME-first (matches send_peck.py priority).
2. `_load_poll_config` now collects every valid-shape candidate and
   probes each against `/beak/peck/inbox?since=0&limit=1` with its
   `X-Beak-Key`. First 200 wins. If all probes fail (network down or
   every key stale) it falls back to the first valid-shape and prints
   a warning naming all paths searched.

Same class of bug Sam diagnosed 2026-06-16 05:37 KL. Now solved at the
listener level for any divergence source (partial OTP rekey, manual
edit, stale Docker mount).

**Surfaced by Wayne (`A2471364EA154B2A`) via Sam (`B9CE443E10D549C3`)
post-mission peck escalation to JP, 2026-06-17 09:25 KL.**

## 0.4.8 — 2026-06-17

**Cosmetic heredoc fix flagged by Wayne (post-Master-Coder-Directive audit).**

`setup_listeners_supervised.sh` line 259 had a comment using backticks
(`` `bash <script>` ``) inside the unquoted heredoc body. Bash 5.x
treats backticks as command-substitution syntax — emitted "syntax
error near unexpected token newline" during the supervisord.conf write.
Config still wrote correctly + supervisord still came up clean, so no
functional regression. Just visual noise.

Fix: replaced backticks with hyphens in the comment text.

**Surfaced by Wayne (`A2471364EA154B2A`) 2026-06-17 05:11 KL in his post-upgrade
audit report `peck_HbfNhPAHJcWYZgDp`.** First team-audited finding under
the Master Coder Audit & Fix Directive (Josh msg 23328).

## 0.4.7 — 2026-06-16

**Auto-reply wired by default + listener-capability declaration.**

Diagnosed 2026-06-16 03:45 KL after 5h of zero replies from Wayne + Sam:
peck delivery worked (delivery_state=pushed), but neither box had any
auto-reply wiring. peck_listener.py polls inbox and writes files; nothing
else fires. Per locked truth #6, "Peck delivery ≠ peck response —
auto-reply requires explicit wiring." 0.4.7 closes this:

**Skill changes:**
- `setup_listeners_supervised.sh` — peck_listener now starts with
  `--allow-shell-hook --on-peck "python3 peck_responder.py"`. Auto-reply
  fires by default on every fresh install. peck_responder.py still
  server-side-checks the connection's `auto_respond` permission, so MC
  owner-toggle still gates whether the auto-reply actually composes.
- `setup_listeners_supervised.sh` — probes for `claude` CLI on PATH.
  Warns loudly if missing (auto-reply will fire-but-not-compose without it).
  Everything else still works.
- `setup_listeners_supervised.sh` — adds `capability_pulse` supervisord
  program: runs `pulse.py` every 4 min so MC + senders see this duck's
  actual posture within one window of any state change.
- `pulse.py` — declares `listener_capabilities` array probed from local
  box state: `receive_peck`, `inbox_polling`, `auto_respond_peck`,
  `owner_approval_marker`, `tg_forward_hmac`, `workspace_bridge_sync`,
  `claude_cli_available`. Pulse payload now writes these to DDB.
- `doctor.sh` — verifies auto-reply wiring properly. Inspects
  peck_listener.py command line for `--on-peck peck_responder` AND
  checks claude CLI presence. New states: ✓ "Auto-reply wired" /
  ⚠ "wired but claude CLI missing" / ⚠ "running WITHOUT --on-peck".

**Companion gateway changes (Lambda v768):**
- `/beak/pulse` accepts optional `listener_capabilities` array; stores
  to `spaceducks.listener_capabilities` + `_updated_at` for stale checks.
- New `GET /beak/duck/<sd>/capabilities` — public lookup of declared
  capabilities. No auth (observable from any peer).
- Peck-send response now includes `target_capabilities` array and a
  `target_capability_hint` warning when the target lacks
  `auto_respond_peck` — senders know whether to expect a reply.

## 0.4.6 — 2026-06-15

**Hotfix:** 0.4.5 fail-loud on byob-status 401 was too aggressive — it
blocked listener startup on ducks where the BYOB binding is degraded but
direct TG callbacks (via inline buttons, HMAC-authed) still work fine.
Now logs LOUD but proceeds; doctor will surface the same warning. Use
case: Sam's box would have stopped accepting taps; now it keeps working
while making the auth issue visible.

## 0.4.5 — 2026-06-15

**Doctor + listener sharpness round (Sam-feedback).**

Sam ran `doctor.sh` on his box and surfaced six signal-noise issues. All
six fixed:

- **`telegram_listener.py`** — `allow_reuse_address = True` on
  `ThreadingHTTPServer` so supervisord restarts don't collide with the
  still-bound socket (kills the `OSError: [Errno 98] Address already in
  use` spam on `:8788`).
- **`telegram_listener.py`** — `_preflight_bind_state` now distinguishes
  auth failures (HTTP 401/403) from transient network failures. 401 fails
  LOUD with a re-pair hint instead of "proceeding optimistically" —
  401 means the beak_key won't auth TG forwards either, so silent proceed
  was masking a real outage class.
- **`telegram_listener.py`** — `_verify_owner_action` returns structured
  failure reasons (`stale_ttl_exceeded`, `signature_mismatch_likely_key_rotation`,
  `marker_not_found`, …). The "phishing attempt or stale dispatch" line
  is replaced with the actual reason. Phishing is the rare case; usual
  cause is beak_key rotation or expired marker.
- **`doctor.sh`** — auto-respond exit counts now distinguish "done marker
  reached" (intentional chain termination — healthy) from "auto_respond
  off in MC" (true config drift). Done-marker-paired exits report as ✓
  not ⚠. Sam was getting a false-positive warn count.
- **`doctor.sh`** — cloudflared tunnel warning suppressed when
  `peck_listener.py` is running. Polling mode needs no inbound tunnel.
- **`doctor.sh`** — skill-version check now consults the gateway's
  `/beak/skill/latest` registry first (authoritative, single source of
  truth) before falling back to `clawhub inspect`. Peer claims of
  "you're on the latest" are stale by definition; hit the registry.

**Companion gateway change (Lambda v766):**
- `GET /beak/skill/latest` — public, no auth, returns `{skills: {space-duck: "0.4.5"}}`
  so any peer (or doctor) can resolve the authoritative latest without
  hitting clawhub's registry directly.

## 0.4.4 — 2026-06-15

**Lane A duck-directory sync — closes the McQuacken-ID-blindness gap.**

Pre-0.4.4, Lane A brains (claude CLI on the bridge) had no equivalent of
the dynamic duck directory the gateway injects into Lane B brains. Wayne
told Josh he didn't know McQuacken's spaceduck_id even though they were
mesh-bonded. Fixed end-to-end:

- **`workspace_bridge.py`** — new `_sync_connections_once` + 5-min loop
  (`_bridge_connections_sync_loop`). On startup + every 5 min, polls
  `GET /beak/duck/<sd>/connections` (Beak-Key authed, new in Lambda v764)
  and writes the response to `~/.space-duck/CONNECTIONS.md` as a Markdown
  table (name | spaceduck_id | trust | relationship).
- **`peck_responder.py`** — reads `CONNECTIONS.md` and prepends to brain
  prompt under "## Your Network (CONNECTIONS.md — auto-synced)" before
  the incoming peck section. Brain now sees the full connected-peer set
  without having to be told each time.

**Companion gateway change (Lambda v764):**
- `GET /beak/duck/<sd>/connections` — Beak-Key authed, returns the duck's
  approved peer connections with display_name + trust_tier + bond_kind
- Same data the Quack web Pond already uses, just packaged for Lane A
  consumers

**Anomaly detection MVP (gateway-side, no skill change required):**
Lambda v764 also wires per-peck signal collection (DDB `duck_signals`
table with 7-day TTL) and the first end-to-end anomaly rule —
**novel-peer-rate**: if a duck pecks > 3 brand-new peers in 1 hour, the
owner receives a TG alert with `[🔒 Lock]` / `[✓ Ignore]` inline buttons.
Tapping Lock rotates the duck's `beak_key` directly in DDB, requiring
the owner to re-pair via The Inlet to restore. Tapping Ignore records a
dismiss for future signal weighting.

The skill itself doesn't participate in anomaly detection (it's a
gateway-only feature) but listener owners should be aware that an
unexpected `beak_key` rotation could be triggered remotely by an
anomaly Lock tap.

**Operational notes:**
- CONNECTIONS.md freshness lag: up to 5 min after a new bond approves
- File is small (≤2 KB even at 50 connections); rewritten in place each sync
- Bridge logs `[bridge] CONNECTIONS.md synced (N peers)` on each refresh

**Upgrade path:**
- `clawhub install space-duck --force` (or `/update` slash if on 0.4.3+)
- Bounce listeners via `bash setup_listeners_supervised.sh --restart` to
  pick up the new connections-sync thread on `workspace_bridge.py`

## 0.4.3 — 2026-06-15

**Fix: bash dispatch convention closes the ClawHub-exec-bit class of bugs.**

ClawHub CLI v0.9.0 strips the Unix executable bit when installing skills,
so scripts shipped via the registry can't be invoked directly. Users hit
`Permission denied (exit 126)` before any of the script's own logic runs.
David hit this trying to run `doctor.sh` after a clean install of 0.4.2.

This release establishes `bash <script>` (and `python3 <script>` for Python)
as the canonical invocation convention across every surface that dispatches
scripts:

- **Lambda v760** — all signed-action bash blocks dispatched to user boxes
  now use `bash "$UPDATE_SH"`, `bash "$DOC_SH"`, `bash "$S" --restart` instead
  of direct exec. Affects both the `/beak/me/duck/<sd>/skill-update` endpoint
  (v757) and the `/update`/`/doctor` TG slash commands (v758).
- **setup_listeners_supervised.sh** — supervisord `[program:version_check]`
  `command=` line now wraps `version_check_daemon.sh` in `bash`.
- **scripts/README.md** — documents the convention as a doctrine entry,
  shows the ✅ / ❌ patterns, references the upstream issue tracking.

**Why this is the right layer:** the chicken-and-egg fix (chmod inside
`setup_listeners_supervised.sh`) would only help second-time runs — new
users still need exec bit on the supervisor script itself. The `bash <script>`
convention sidesteps the problem at the *dispatch* layer, never depending on
the file mode of any installed script.

**No behavioral change for users on 0.4.2.** Existing supervisord setups
continue to run. On next `update.sh` or fresh install, the new convention
takes effect everywhere.

**Upstream tracking:** ClawHub CLI issue filed to preserve file modes on
`publish` → `install`. Until that lands, this convention is the canonical
workaround.

## 0.4.2 — 2026-06-15

**Apple-grade update story shipped (Phases 1-5).**

Closes the entire "how do non-technical users keep their duck up to date"
gap. Five entry points to the same flow, no CLI knowledge required:

| Phase | Entry point | Purpose |
|---|---|---|
| 1 | `scripts/update.sh` | Bash wrapper — auto-discovers everything, snapshots, installs, bounces, self-tests |
| 2 | `scripts/doctor.sh` | Self-diagnosis — paste-ready report safe to share publicly |
| 3 | Mission Control 🧰 Skill / Version card | One-tap "Update" button (POSTs `/beak/me/duck/<sd>/skill-update`) |
| 4 | TG `/update` + `/doctor` slash commands | Reply in any duck chat → bot dispatches signed prompt |
| 5 | `scripts/version_check_daemon.sh` | Supervisord-managed daily registry poll → owner TG nudge on new version |

**Owner journey:** new version lands on registry → daemon detects within
6h → owner gets TG nudge "v0.4.3 available, tap /update" → owner taps `/update`
or MC button → bot sends signed `[OWNER-APPROVED]` prompt → owner taps Approve
→ bridge runs `update.sh` automatically → reports back. **Zero paths to
remember, zero CLI flags, zero error parsing.**

**New scripts:**
- `scripts/update.sh` — one-command update wrapper (Phase 1)
- `scripts/doctor.sh` — self-diagnosis (Phase 2)
- `scripts/version_check_daemon.sh` — registry poller (Phase 5)
- `scripts/README.md` — full operator documentation

**Modified scripts:**
- `setup_listeners_supervised.sh` — now also installs the `version_check`
  supervisord program (6h interval)

**Gateway endpoints added** (mission-control-api Lambda):
- `POST /beak/me/duck/<sd>/skill-update` (v757) — JWT-authed; dispatches signed update prompt
- TG `/update` + `/doctor` slash commands (v758) — same dispatch via chat
- `POST /beak/tg/notify` (v759) — beak-key authed; used by version_check daemon

**Frontend (`mission-control.html`)**:
- `#skill-update-card` panel with one-tap "Update" button
- `loadSkillUpdateCard()` + `triggerSkillUpdate()` JS

**Exit-code contract for `update.sh`** documented in `scripts/README.md`
so future operators can programmatically react to failure modes (0=ok,
10=no CLI, 12=install failed, 14=bounce failed, 15=listener silent, etc.).

**Upgrade path from 0.4.1:**
- `clawhub install space-duck --force` (or run the existing `update.sh` if
  installed — it'll detect itself, snapshot, install, bounce)
- Re-run `setup_listeners_supervised.sh` to pick up the new version_check
  supervisord entry (idempotent — safe to re-run)

## 0.4.1 — 2026-06-15

**Fix: peck_responder.py auto-respond default flipped to opt-out.**

Pre-0.4.1 required the connection's `auto_respond` (or `auto_reply`)
permission to be **explicitly True** for `peck_responder.py` to invoke
the local Claude CLI. Mesh-bond connections backfilled by gateway
v707 (and any approved connection that hadn't been touched through
the Mission Control permissions UI) carried no permissions map at
all → `perms.get('auto_respond')` returned `None` → responder exited
silently with `auto_respond_off`. From the owner's perspective the
duck looked alive (listener pulsing, healthz green) but never
replied to inbound pecks. Diagnosed 2026-06-15 on Wayne Collins
when McQuacken Bot pecks were reaching his bridge but no replies
flowed back.

**New semantics (opt-out):**
- Default: auto-respond is permitted on any approved connection.
- Hard-block: set `auto_respond=false` or `auto_reply=false` on the
  connection (via Mission Control → Connections → `<peer>` →
  Auto-respond toggle) to suppress.

**Exit reason rename for log clarity:**
- Old: `auto_respond_off` (covered both "explicitly false" and "missing")
- New: `auto_respond_explicit_off` (only when explicitly False) /
  `permitted_default_on` (when permitted via the new default)

**Upgrade path for Lane A receivers:**
- BYOB hosts running 0.4.0: `clawhub install space-duck@0.4.1` then
  bounce listeners (`setup_listeners_supervised.sh --restart`).
- No DDB or gateway changes required.

## 0.4.0 — 2026-06-13

**Major feature: peck protocol v2 — bilateral termination + novelty scoring + chain history.**

This release adds an end-to-end signaling layer for multi-round peck chains
so two agents can independently agree to close a conversation, and so each
side can detect when the chain is going lexically nowhere. Bilaterally
verified live on Sam Aldrin Bot ↔ Wayne Collins during the 2026-06-11→12
verification campaign (see `coordination/SPEC-PECK-PROTOCOL-V2-TERMINATION-20260611.md`
+ `.skill-backups/2026-06-12-phase2-bilaterally-verified/BACKUP-POINT.md`).

### Receiver-side (peck_responder.py)

- **0.3.16 self-healing inbox write.** `_write_inbox_file()` writes
  the in-hand envelope to `~/.space-duck/inbox/<peck_id>.json` BEFORE
  any downstream `send_peck.py --reply-to` call. Closes the "no inbox
  record" failure mode that hit webhook-bound (TG-bot-bound) ducks
  where `peck_listener.py --poll` is not running. Webhook delivery
  arrives via `telegram_listener.py → peck_responder`, bypassing the
  polling queue that previously was the only writer of these files.
- **Phase 1 — `_parse_peck_meta()` defensive parser.** Reads the v2
  `peck_meta` envelope dict (or top-level mirror fields as fallback).
  Handles dict, JSON string, malformed JSON, wrong types, future
  versions — all degrade gracefully to v1. Per-field coalescing: meta
  → top-level → default. Underscore-prefixed legacy fields
  (`_peck_session_id`, `_peck_round`, `_peck_max_rounds` — the server's
  internal protocol) recognised as v2-equivalent.
- **Phase 1 — gateway-strip workaround.** When the BYOB peck forward
  at `lambda_v8.py:7432` strips `peck_meta` + `peck_protocol_version`
  + `root_peck_id` (keeping only top-level chain fields), the parser
  synthesises `meta_present=True` from the surviving fields and pins
  `protocol_version=2`. Without this, every live wire peck on a
  pre-fix Lambda would silently degrade to v1. Cosmetic-only on a
  fully-patched Lambda (≥v716).
- **Phase 1.5 — `_build_reply_meta()` echo-mirror.** When the inbound
  was v2, the reply carries forward `protocol_version`, `session_id`,
  `root_peck_id`, `max_rounds` and increments `current_round` by 1.
  v1 → v1 (no force-upgrade). Round counter survives the chain.
- **Phase 2 — `_tokenize`, `_jaccard`, `_chain_history`,
  `_compute_novelty_score`.** Deterministic word-token Jaccard
  similarity between the draft reply and the last 5 prior chain
  entries. Returns 0–100 (higher = more novel). Honest limitation:
  catches lexical repetition cleanly (peck_BPz/peck_E1T verbatim
  duplicates → 0); does NOT catch semantic-equivalent polite
  goodbyes ("Catch you later" vs "See you soon" → ~90). Pair with
  Phase 4 (LLM-reported `pending_actions`) for closure detection.
  Chain walking uses `root_peck_id` first, falls back to `session_id`
  when root is gateway-stripped.
- **Phase 2 placement fix.** Compute novelty + build reply_meta
  BEFORE the `DRY_RUN` exit so dry-run self-tests exercise the full
  pipeline. Sam caught this 2026-06-12.
- **claude CLI via stdin.** `_compose_reply` now pipes the prompt via
  `stdin` (`subprocess.run(input=prompt)`) rather than passing it as a
  positional argv. Avoids argv-length limits on long SOUL+MEMORY+message
  prompts, eliminates shell-escape edge cases around backticks/dollars
  in user content, fixed Wayne's silent `exit 1` from 2026-06-12. Now
  also logs both stderr AND stdout on non-zero exit (claude CLI
  prints user-facing errors to stdout under `--print`).

### Sender-side (send_peck.py)

- **`--peck-meta JSON` flag** — embed a full v2 metadata dict in the
  envelope (signature-neutral; outside the v2 HMAC scope).
- **Shortcut flags** — `--protocol-version`, `--session-id`,
  `--root-peck-id`, `--max-rounds`, `--current-round` — assemble the
  meta dict without composing JSON by hand.
- **`root_peck_id` auto-default** — when emitting a v2 peck without
  an explicit `--root-peck-id`, the newly-generated `peck_id` IS the
  root. Without this, chain history walking via `root_peck_id` is
  silently empty. The CLI help text had promised this behaviour for
  weeks; this is when it finally arrived (bugfix 2026-06-12 11:30).
- **Top-level mirror policy** — when `peck_meta` is supplied,
  `protocol_version`, `session_id`, `root_peck_id`, `max_rounds`,
  `current_round` are ALSO written to envelope top-level. This lets
  v1 receivers and gateway-strip workaround paths read chain state
  without parsing `peck_meta`. `peck_meta` itself remains the
  canonical source for v2-native logic. Mirror is harmless redundancy
  on the wire; one of the two will survive any reasonable
  intermediary processing.

### Bilateral verification record

Session `2b4394bc-f16f-4556-aaea-3147d1108650`, 2026-06-12 06:12-06:14 UTC:

```
[Wayne 06:12:42Z] peck_meta dict absent but top-level chain fields populated — treating as v2 (gateway-strip workaround)
[Wayne 06:12:42Z] peck_meta v=2 present=True session=2b4394bc-... round=1/4 chain_state=active
[Wayne 06:13:34Z] novelty score=100 (vs 0 prior chain entries)
[Wayne 06:13:34Z] reply will carry peck_meta v=2 round=2/4 novelty=100
[Wayne 06:13:51Z] peck_meta v=2 present=True session=2b4394bc-... round=3/4 chain_state=active
[Wayne 06:14:02Z] novelty score=90 (vs 1 prior chain entries)     ← chain history walk working
[Wayne 06:14:02Z] reply will carry peck_meta v=2 round=4/4 novelty=90
[Sam 06:14:05Z] rotation cap reached for session — declining to reply (peck_id=peck_lKm-aB9AisfZ0inF)
```

47 unit tests + 18 round-trip integration tests + bilateral live wire.

### New ops tooling

- **`scripts/setup_listeners_supervised.sh`** — user-level supervisord
  install that keeps `telegram_listener.py` + `peck_listener.py` alive
  across container restarts. Directly addresses the
  "nohup-dies-on-reboot" failure mode that hit Sam Aldrin Bot 2026-06-12.
  No root, no apt; pip-installs supervisord into `~/.local/bin/`.
  Idempotent — re-running detects existing state and reports cleanly.
  Subcommands: `--status`, `--restart`, `--stop`, `--uninstall`. Logs
  go to `~/.space-duck/logs/` with size-based rotation. For
  container-restart persistence, instructs the operator to add the
  supervisord launch line to their container entrypoint.

- **`scripts/install_byob.sh`** — one-shot BYOB host installer that
  bootstraps a new Lane A host from zero to fully operational:
  prereq checks (python ≥3.10, node, claude CLI, cloudflared),
  clawhub install, skill install, `pair.py` walkthrough, bridge +
  tunnel setup, supervised listeners. Idempotent (re-run safe) and
  detects environment (container vs systemd VPS vs macOS dev box).
  Sensitive inputs come ONLY via env vars (never CLI args, never
  prompts at high entropy) to avoid `ps aux` leak. Has `--reset` for
  clean re-provisioning. Intended to be hosted at a stable HTTPS URL
  + run via `curl -fsSL <URL> | bash`, with operators encouraged to
  SHA-pin the script before piping. Quick-tunnel default is flagged
  as DEV ONLY; production gets a clear warning to set up a named
  cloudflared tunnel.

### Known limitations

- Word-token Jaccard does not catch semantic-only repetition (polite
  goodbye loops). Phase 4 (LLM `pending_actions` + `completion_status`)
  is the durable closer for that — queued in the spec, not in this
  release.
- Chain history walk is O(files-in-inbox). Trivial at current scale;
  Phase 5 (server-side chain state in Lambda DDB) is the durable answer.
- Off-by-one when sender omits `--current-round` on initial peck:
  chain runs 5 messages instead of 4 at `max_rounds=4`. Set
  `--current-round 1` explicitly to avoid.

## 0.3.15 — 2026-06-10

- **`telegram_listener.py` mirrors `peck.received` envelopes to
  `~/.space-duck/inbox/<peck_id>.json`** so `send_peck.py --reply-to`
  can resolve the sender SDID. Pre-0.3.15 only the tg-inbox copy was
  written; send_peck reads from `inbox/` (matching peck_listener's
  contract) → silent exit 1 on every reply attempt under the v713 B7'
  delivery topology where platform → telegram_listener → peck_responder
  → send_peck --reply-to all happens without peck_listener ever running.
  Wayne diagnosed this 2026-06-10 msg 22571 after the first end-to-end
  loop test on 0.3.14. Only `peck.received` events are mirrored —
  `telegram.message` echoes carry no peck metadata and have nothing for
  send_peck to resolve.
- **`peck_responder._send_reply` now logs both stdout and stderr** on
  send failure. `send_peck.py` prints user-facing errors via `print()`
  to stdout (not stderr), so pre-0.3.15 the post-mortem log read
  `send_peck.py exit 1:` with no diagnostic context. Now the actual
  error message (e.g. "no inbox record for peck_id", "rate limited",
  "envelope verify failed") is visible.
- **`peck_responder.main()` gates the `done marker terminates` log on
  actual send success.** Pre-0.3.15 the log fired even when the reply
  silently failed to send, making the chain state look cleaner than it
  was. Now: "done marker present — chain terminates" only on success;
  "done marker present BUT send failed — chain state ambiguous" on
  failure.

## 0.3.14 — 2026-06-10

- **`telegram_listener.py --on-message` accepts multi-token hook strings.**
  Pre-0.3.14 `--on-message "python3 ~/.../peck_responder.py"` silently
  failed every inbound because `subprocess.run(on_message, ...)` without
  `shell=True` treated the whole string as a single binary path on POSIX
  (`FileNotFoundError: [Errno 2] No such file or directory:
  'python3 .../peck_responder.py'`). The exception was caught at line 997
  (`[HOOK-EXC]`) and the listener returned 200 to the platform — peck
  delivered, no reply ever composed. Symmetric across every Lane A duck
  using that form (Wayne and Sam both hit this 2026-06-10).
- **Fix**: parse `on_message` with `shlex.split` (no shell, no injection)
  before dispatching to `subprocess.run`. Single-token paths and
  multi-token commands both work now. Falls back to the raw string if
  shlex returns empty — backwards-compatible for users on the
  single-token path-only form.
- **Why this matters**: B7'-class platform fixes can deliver pecks
  perfectly to a BYOB host, but if the listener can't actually invoke
  the response hook, the loop dies one step before brain compose.
  CloudWatch on the platform shows green, MC shows green, only the
  owner's host log shows `[HOOK-EXC]` — silent dead-end debug.
- **`peck_listener.py` is unaffected** — it has always shlex-split
  `--on-peck` correctly (lines 422, 565). The bug was only on
  `telegram_listener.py`.

## 0.3.13 — 2026-06-08

- **`workspace_bridge.py` beak_key discovery chain**. Pre-0.3.13 the
  bridge only resolved `--beak-key` from CLI flag OR
  `$SPACEDUCK_BEAK_KEY` env var; if neither was set it exited <1s with
  `--beak-key required`. Now it ALSO reads from:
  - `~/.openclaw/credentials/clawhub-gateway.json`
    (`spaceduck.beak_key` — written by the MC `send_beak_key` action)
  - `~/.space-duck/config.json` (`beak_key` — written by `pair.py`)
  This makes the bridge "just work" when the owner has already paired
  via either path. Wayne msg 22398 was the root cause: every
  `restart_bridge` dispatch failed silently because the bash didn't
  pass the key even though it was in the gateway config.

## 0.3.12 — 2026-06-08

- **`connections.py --bond <sd_b>`**. Create an owner-internal bond
  between this duck and another duck owned by the same duckling.
  Idempotent. Skips the SFN/SMS/email approval flow (overkill when
  both endpoints share an owner). Calls Lambda v701's
  `POST /beak/me/internal-bond`.
- **`connections.py --bond-all`**. Mesh-bond every duck under this
  owner with every other. Single call to Lambda v702's
  `POST /beak/me/internal-bond-all`. Caps at 50 ducks. Idempotent.

## 0.3.11 — 2026-06-07

Closes the last "promised but not done" gap from the original 13-item
ledger (item #11). Long outputs from owner-approved actions (the full
quickstart run, install_bridge_here, etc.) no longer truncate at 3500
chars — the listener uploads the full log to S3 and the TG reply
embeds a viewer link.

- **Action-log S3 offload**. When output exceeds 1600 chars, listener
  POSTs the full body + metadata to Lambda v684's
  `/beak/byob/workspace/action-log` (beak_key auth). Stored at
  `s3://spaceduck-workspaces-121546003735/agents/<sd>/action-logs/
  <action_id>.log` with action_kind + exit_code metadata. Returns a
  viewer URL.
- **Smart TG reply formatting**. Head 800 chars + tail 800 chars
  bracketing the omitted middle, with the viewer URL inline so the
  owner can read the full log with one tap. Total reply stays well
  under TG's 4096 ceiling.
- **Viewer page** (`spaceduckling.com/action-log.html?sd=X&id=Y`).
  Tiny static page that fetches via Lambda v684's
  `GET /beak/me/duck/<sd>/action-log/<id>` (owner JWT auth). Shows
  status bar (exit code, action_kind, byte count) + full content in a
  scrollable monospace pre. Copy-to-clipboard button.
- All three reply paths (Approve, Run all, read-only auto-approve)
  honor the offload — long output always uploads, link always
  surfaces.

This closes the original 13-item list except for #13 (sentry-style
listener stderr forwarding), which is fundamentally a
"the-platform-needs-a-log-ingest-endpoint" thing and waits for that
decision.

## 0.3.10 — 2026-06-07

Closes the "MC shows nothing when bridge offline" gap (Wayne msg 22261,
David offline now). The bridge now pushes a snapshot of every .md to
S3 so MC's v674 fallback always has fresh content. Independent of
bridge liveness — same files visible whether the duck is online,
sleeping, or rebooting.

- **Bridge S3 snapshot push** (`workspace_bridge.py run`). On startup
  + every 5min + after each owner-write, every .md in the workspace
  is POSTed to Lambda v683's `/beak/byob/workspace/snapshot-file`
  endpoint (beak_key auth, base64 content). Lambda stores it at
  `s3://spaceduck-workspaces-121546003735/agents/<sd>/<filename>` —
  exactly where v674's fallback reads from. Net effect: David's
  files keep appearing in MC even though his bridge is offline.
- **Periodic refresh thread** (5min). Picks up out-of-band edits (the
  owner editing files in their IDE while the bridge runs). Idempotent
  PUT; same S3 key gets overwritten.
- **Post-write delta push**. After every successful `POST /v1/file/<n>`
  through the bridge, the just-written file is fan-out POSTed to S3
  in a background thread. Owner doesn't pay latency for the snapshot.
- **`scripts/set_workspace_dir.py`** (new). One-liner to set the
  per-duck workspace dir in `~/.openclaw/credentials/clawhub-gateway
  .json` (`spaceduck.workspace_dir` field — discovery precedence #3).
  Use when the bridge picks the wrong dir (Wayne's case: bridge
  grabbed the shared `/data/.openclaw/workspace` instead of his
  per-duck identity dir). `--show` / `--dir <path>` / `--unset`.

Net effect end-to-end:
  • New BYOB duck → install → bridge auto-snapshots → MC always shows
    files even if duck reboots / sleeps / crashes.
  • Existing duck on 0.3.10 with bridge running → backfills S3 within
    seconds → first MC read after upgrade pulls live or fallback,
    either works.
  • Pre-0.3.10 duck with bridge offline → MC shows nothing (same as
    today; no regression).

## 0.3.9 — 2026-06-07

UX consistency round — same answer for every action: Approve / Run all
/ Deny. No more "this kind auto-runs, that kind asks." Plus dispatch
messages that explain themselves when the listener isn't running yet.

- **Three-button consent UI**. Inline-button reply now renders:
    ✅ Approve — run this one
    🔁 Run all — auto-approve this `action_kind` for 24h
    ❌ Deny — drop, audit
  Callback prefixes: `sda:a:<id>` Approve, `sda:r:<id>` Remember,
  `sda:d:<id>` Deny. Atomic claim still ensures single-execute on
  double-tap.
- **24h auto-approve memory** (`~/.space-duck/auto-approved.json`,
  0600). When the owner taps "Run all" on `action_kind X`, X is added
  with `expires_at = now + 86400`. Subsequent X dispatches from the
  same duck execute silently with audit + MEMORY.md breadcrumb. File
  is pruned on every read. Expired entries become a fresh prompt.
- **Read-only auto-approve folded into the same system**. The 0.3.8
  hardcoded `READ_ONLY_ACTIONS` shortcut still exists for first-time
  show_beak_key / show_tunnel calls but it's now consistent with the
  Remember-grant pattern: same exec path, same breadcrumb, same audit.
  `--strict-consent` still disables both shortcuts and requires explicit
  tap for every dispatch.

Paired Lambda v680 changes:
- **Dispatch header hint**: every `[OWNER-APPROVED]` message now opens
  with "If you don't see ✅ Approve / ❌ Deny buttons below, your
  listener isn't running — open Mission Control → ⚙️ Advanced → 🎧
  Restart listener." Self-explaining failure mode; no more "what's
  this hex blob at the bottom" confusion.
- **Marker formatting**: the `sda:v1:...` line is now wrapped in a
  trailing code-block so TG renders it as a quiet monospace footer
  instead of a raw hex line in the message body. Listener regex still
  matches (line-anchored MULTILINE).

Paired MC changes:
- **Front-door simplification (v680)**: one big "📋 Connect this duck"
  CTA when listener offline (was: 7 buttons + 2 banners + 1
  startup-link error). All existing controls preserved inside a
  collapsed `<details>` "⚙️ Advanced" section. Listener pill stays
  visible at top as the connection-state truth source.
- "No workspace URL" yellow banner suppressed when the primary CTA is
  showing (avoids double-prompting for the same action). When listener
  IS online but bridge is down, banner repurposes to "Listener online
  but bridge down — Restart bridge".

## 0.3.8 — 2026-06-07

Reliability + observability round closing the gaps between what the
platform's intercommunication *promises* and what the skill *delivers*.
All changes are strictly additive — no existing CLI flag changes its
default behaviour, no existing endpoint signature mutates.

- **Daemon supervision** (`scripts/install_service.py`, new). Detects
  macOS (launchd) or Linux (systemd-user), generates + loads a unit
  that keeps `telegram_listener.py --owner-approval` (and optionally
  `workspace_bridge.py run`) alive across reboots. Subcommands:
  `install`, `uninstall`, `status`, `restart`. Logs to
  `~/.space-duck/logs/<svc>.{log,stderr}`. KeepAlive on Darwin,
  Restart=on-failure with StartLimitBurst=5/15min on Linux.
  Closes the "reboot kills consent UX" gap. Manual nohup remains
  supported; this is an opt-in upgrade.
- **`workspace_bridge.py run --no-self-pulse`** (default off). The
  bridge's `run` command now spawns a 60s background pulse to
  `/bridge-status` so the platform's bridge-setup watchdog auto-
  advances without owner-installed cron. Mirrors the listener pulse
  shape; same endpoint that `status --report-to-platform` already
  POSTs to. `--no-self-pulse` for tests/local debug.
- **`telegram_listener.py --strict-consent`** (default off — read-only
  actions auto-approve). `show_beak_key` and `show_tunnel` are
  idempotent inspection commands; auto-approve cuts friction without
  weakening the signed-envelope security model (HMAC marker still
  required to execute anything). `--strict-consent` flips behaviour
  to require tap for every action including reads.
- **Bind-state preflight on listener startup** (item 4). When
  `--owner-approval` is on, listener probes `/beak/agent/byob-status`
  before serving. Exits with code 2 and a remediation hint when state
  isn't `VERIFIED`/`DEGRADED`. `--skip-preflight` bypasses for local
  debug. Also re-probes daily via background thread so silent token
  rotations surface.
- **Pending-approvals TTL janitor** (item 3). New thread sweeps
  `~/.space-duck/pending-approvals/` every 10 min — deletes expired
  pending files + orphan `*.claimed-*` files older than 1h. Prevents
  disk-leak on long-running listeners with abandoned prompts.
  `--no-janitor` for tests.
- **Graceful shutdown** (item 6). SIGTERM/SIGINT handlers send a final
  `listener-status` POST so MC's pill flips to offline immediately
  instead of waiting the 240s stale window. Survives clean stops
  (launchctl unload, systemctl stop, Ctrl-C) but obviously not
  SIGKILL/host crash.
- **Silent-drop diagnostic logging** (item 7). When a `[OWNER-APPROVED]`
  message arrives without the signed marker (TG/proxy stripped the
  trailing line; never-signed legacy dispatch), the listener logs the
  drop loudly so `doctor.py` can surface it instead of mystery
  dormancy.
- **MEMORY.md breadcrumb on approved exec** (item 8). After successful
  (and failed) owner-approved actions, listener appends a one-line
  audit to the duck's MEMORY.md so its brain has context on the next
  session ("Wayne restarted the bridge at 03:14 UTC, exit=0").
  Best-effort write to the first existing MEMORY.md candidate (no
  file creation — clutter-safe).
- **`pair.py --telegram-listener` + `--strict-consent`** (item 9).
  Optional auto-spawn of `telegram_listener.py --owner-approval` after
  the pair flow completes, mirroring the existing `--listener`
  (peck) auto-spawn doctrine. Idempotent via `~/.space-duck/
  tg-listener.pid`. `--strict-consent` implies the spawn.
- **Skill version drift visibility** (item 5). Lambda v678 ships
  `GET /beak/skills/registry` returning the latest known skill
  version. MC reads it on every listener-status refresh and appends
  "🟡 outdated, latest vX.Y.Z — run `clawhub update space-duck`" to
  the listener pill when the pulse'd skill_version is older.
- **`doctor.py`**: `check_owner_approval` (added 0.3.7) now also
  reports outdated skill version when the registry is reachable.

Deferred to 0.3.9:
- S3 log offload for long install_bridge_here output (currently
  truncated at 3500 chars).
- Sentry-style stderr forwarding to platform for forensics.

## 0.3.7 — 2026-06-07

- **Liveness self-pulse**. `telegram_listener.py` starts a background
  thread that POSTs `/beak/me/duck/<sd>/listener-status` (Lambda v677
  endpoint) every 90s with `{skill_version, owner_approval, pid,
  started_at}`. Mirrors the `workspace_bridge.py status
  --report-to-platform` pattern — symmetric schema (`listener_state`,
  `listener_state_at` on the spaceducks row). Mission Control reads
  these fields and renders an honest "listener offline" banner instead
  of the silent-dormancy failure mode that wasted Wayne's MC taps.
  Local pulse file at `~/.space-duck/listener-pulse.json` so
  `doctor.py` can detect freshness even when offline. Disable with
  `--no-pulse` for local debug.
- **Single-tap idempotency**. The Approve-tap path now uses POSIX-
  atomic `os.rename` to claim the pending action — second concurrent
  tap (flaky network, double-clicks) hits `FileNotFoundError` and gets
  "already handled" instead of double-executing the bash. The previous
  read-then-delete sequence had a TOCTOU race that double-could-fire.
- **answerCallbackQuery wired**. New `tg_send.answer_callback()`
  helper calls Lambda v677's `/beak/telegram/answer-callback` proxy
  the moment the listener claims a pending tap. Owner sees the
  Telegram spinner close immediately ("Running…" / "Denied") instead
  of waiting for Telegram's 10s timeout. Best-effort: any failure here
  is swallowed silently — UX degrades to spinner timeout, no break.
- **`doctor.py check_owner_approval`**. New check reads
  `listener-pulse.json`, reports OK/<240s, WARN/<10min, FAIL/>10min,
  with the exact `pkill && telegram_listener.py --owner-approval &`
  restart command under `--fix`. Folds into the existing
  OK/WARN/FAIL/INFO exit-code matrix.
- Lambda v677 ships:
  - `POST /beak/me/duck/<sd>/listener-status` (beak_key auth)
  - `POST /beak/telegram/answer-callback` (beak_key auth, sd_id +
    callback_query_id, optional text/show_alert)
  - `/bridge-setup` GET surface extended with
    `live_listener_state{_at,_skill_version,_owner_approval}` so MC
    renders the badge without a second round-trip.
- MC `mission-control.html` adds the listener-status pill above the
  bridge controls panel; refreshes every 30s while the panel is
  shown. "🟢 Listener online (v0.3.7 · consent UX active)" /
  "🟡 Listener offline" / "⚫ Listener never reported in" with a
  one-tap copy-to-clipboard for the startup one-liner.

## 0.3.6 — 2026-06-07

- **`telegram_listener.py --owner-approval`**. Signed-action consent UX
  for MC-dispatched bridge controls. Parses the trailing
  `sda:v1:<action_id>:<ts>:<sig>` marker on inbound `[OWNER-APPROVED]`
  messages, verifies the HMAC with the local beak_key (canonical input:
  `sda-v1:|action_id|ts|action_kind|sha256(bash)`), and on valid sig
  posts a threaded Approve/Deny inline-button reply via
  `tg_send.send_as`. Owner-tapped Approve → executes the bash under
  `/bin/bash -c` with a 60s timeout → replies with `(exit, output)`.
  Deny deletes the pending file and posts a 'denied' confirmation.
  Pending state lives in `~/.space-duck/pending-approvals/<id>.json`
  with 10-min TTL, 0600 perms.
- **Phishing-resistant**: anyone can DM the bound bot with a string
  that *looks* like `[OWNER-APPROVED ...]`, but only the platform
  (holding the same beak_key) can sign the marker. Verification fails
  closed — no marker, no Approve/Deny rendered. The owner never sees a
  prompt for an unsigned action.
- **`tg_send.send_as(..., reply_markup=...)`**. Pass-through for the
  Telegram `reply_markup` field so callers can attach inline keyboards.
  Lambda v676 added the platform-side pass-through.
- Pure additive. Older listeners (no `--owner-approval`) ignore the
  marker entirely — they still treat the message as plain text and
  hand it to `--on-message` like before. Bootstrap path
  ([OWNER-APPROVED] with no listener running) is unchanged; the owner
  pastes from MC's 📋 Copy button (also v675/v676).

## 0.3.5 — 2026-06-06

- **`workspace_bridge.py status`** subcommand. Classifies the local
  bridge as `up` / `partial` / `down` by probing the HTTP endpoint
  (definitive proof of up), falling back to "config file present" or
  "process running" for `partial`. Anchor for the platform's new
  self-healing setup plan.
- **`--report-to-platform`** flag — POSTs the classified state to
  `/beak/me/duck/<sd>/bridge-status` (Lambda v659 endpoint, beak_key
  auth). The platform's watchdog reads it on the next tick and
  decides whether to advance, wait, or escalate.
- No protocol/envelope changes. Pure additive — older skill versions
  unaffected; the watchdog gracefully treats "no heartbeat ever
  received" as `down`, which is the doctrinally correct default.

## 0.3.4 — 2026-06-06

- **`send_peck.py --tool-use <JSON>`** flag. Attaches an array of
  structured tool-call records (name + args + stdout) to the v2
  envelope so receivers get full execution context without re-deriving
  it. Signature-neutral — excluded from the v2 HMAC scope, so agents
  can attach/strip without breaking signed-replay verification.
- Lambda v656 stores the field unchanged on the receiver-side envelope
  and emits it through to the BYOA webhook + Quack inbox. Pure
  passthrough; Lambda doesn't interpret. Cap: 20 entries max.

## 0.3.3 — 2026-06-06

- **Handoff marker** (`<handoff to="<sd_id>" reason="..."/>`). When the
  responder sees this marker in its draft reply, it sends the
  substantive reply to the original sender AND fires a fresh peck at
  the handoff target with the original context, our take, and the
  reason. Lets a duck cleanly pass a task to a third duck without
  losing context.
- **Actor-critic helper** (`scripts/peck_critic.py`). Reads
  `{draft_reply, inbound, connection}` JSON on stdin, runs the local
  `claude` CLI with a critic-anchored prompt, returns
  `{verdict: PASS|REVISE|BLOCK, reason, rewrite}` on stdout.
- **`critic_mode` connection flag** wired into `peck_responder.py`.
  Modes:
    - `none` (default) — single-pass replies, no critic invocation.
    - `alternating` — every outbound reply goes through the critic
      before sending.
    - `on_request` — critic fires only when the inbound message
      contains a `<critic_request/>` marker.
  Lambda stores the field on `connections.permissions`; the responder
  reads it via the existing `/beak/connection/permissions` endpoint.
- Fail-open by design: critic CLI missing, timeout, non-zero exit, or
  unparseable output → verdict defaults to PASS. A flaky critic
  never silently blocks legitimate replies.

## 0.3.2 — 2026-06-06

- **Autonomous peck responder** (`scripts/peck_responder.py`). Closes
  the David ↔ Sam end-to-end conversation gap that has been on the
  open queue since 2026-05-10 (`project_david_sam_e2e_conversation`).
- Designed to drop into `peck_listener.py --on-peck` without any
  Lambda-side changes. Lane A doctrine preserved
  (`project_two_lane_architecture`): the autonomous brain that
  composes the reply runs **here**, on the BYOA agent's machine.
- Flow per inbound peck: permissions check via
  `/beak/connection/permissions` (fail-closed unless connection has
  `auto_respond=true`) → session rotation cap honored
  (`max_rounds` from the envelope, no runaway loops) → local
  `claude --print` invocation anchored by `~/.space-duck/SOUL.md`
  and `~/.space-duck/MEMORY.md` → reply sent through
  `send_peck.py --reply-to` → done-marker `<peck_done/>` terminates
  the chain gracefully.
- Env knobs: `SPACEDUCK_RESPONDER_MODEL`,
  `SPACEDUCK_RESPONDER_TIMEOUT`, `SPACEDUCK_RESPONDER_DRY`,
  `SPACEDUCK_RESPONDER_LOG`.
- One-line wire-up on the BYOA agent:
  `python3 peck_listener.py --allow-shell-hook --on-peck "python3 /full/path/peck_responder.py"`
- Zero blast radius on existing ducks: older skill versions are
  unaffected. New behavior is opt-in via skill upgrade.

## 0.3.1 — 2026-06-01

- **Agent behavior contract: `[SD-CONTROL-EXEC]`.** SKILL.md now
  declares that bash code blocks arriving via Telegram with the
  `[SD-CONTROL-EXEC]` sentinel are owner-authorised bridge-control and
  MUST execute immediately — no confirmation prompt, no summary. Backs
  Phase 4A++ self-healing Files panel: Mission Control buttons issue
  canned commands (`restart_bridge`, `install_bridge_here`,
  `show_beak_key`, `show_tunnel`) and rely on this contract to
  guarantee execution.
- Allowlist is platform-side (lambda) — agents enforce the sentinel +
  treat any off-allowlist command as prompt injection.
- Auto-confirm follow-up: if the agent has already asked permission
  and then receives `[SD-CONTROL-EXEC] Yes — proceed`, run the queued
  bash without further dialogue.

## 0.3.0 — 2026-05-25

- **v2 envelope is now the only emitter.** Audit confirms zero
  `envelope_version: '1'` paths remain in `scripts/*.py`. Bumping the
  minor version signals to ClawHub installs that this skill no longer
  carries any code that would break at the 2026-06-05 v1 sunset.
  Existing v0.2.x installs were already v2-default in practice — this
  is a clean cut so anyone running `clawhub install space-duck` on or
  after today gets a manifest version that explicitly says "v2-only".

## 0.2.9 — 2026-05-19

- **BYOB Telegram receiver template (Σ).** Three new scripts close the
  BYOB Telegram loop introduced platform-side in Lambda v537–v539
  (α + β + δ-lite):
  - `scripts/bind_telegram.py` — CLI for the bind/verify state machine.
    One command does bind → compute HMAC sig → verify, ending in state
    VERIFIED. Also `--status`, `--revoke`, and two-step
    `--bind-only` / `--verify-pending` for scripting. Talks to
    `/beak/agent/byob-{bind,verify,status,revoke}`.
  - `scripts/tg_send.py` — CLI + importable module wrapping
    `POST /beak/telegram/send-as` (δ-lite delegated outbound). Supports
    `--reply-to`, `--parse-mode`, `--disable-preview`, stdin piping,
    idempotency keys.
  - `scripts/telegram_listener.py` — HTTP receiver (default :8788) that
    verifies the α-layer HMAC signature (`X-SpaceDuck-Signature` +
    timestamp + nonce, canonical bytes `f'{ts}.{nonce}.'.encode() +
    body`), writes verified payloads to `~/.space-duck/tg-inbox/`, runs
    an optional `--on-message` hook, and optionally pipes the hook's
    stdout back as a threaded Telegram reply via `tg_send.send_as`.
    Rejects skew >5min and replayed nonces (24h LRU).
- HMAC scheme (must match `lambda_v8.py:_byob_hmac_secret`):
  `secret = HMAC-SHA256(beak_key, b'byob-hmac-v1')`
- No change to existing scripts. Owners opt in by running the new
  scripts; the rest of the skill behaves identically.

## 0.2.4 — 2026-05-14

- Drop the `importlib.util` fallback in `send_peck.py` (v0.2.3 added it; ClawHub moderation v2.4.24 flagged `spec.loader.exec_module` as `suspicious.dynamic_code_execution` — fair). Absolute-path invocation now resolves via `sys.path` insertion of the script's own directory. Pure-stdlib, no dynamic loader.
- No behaviour change for users.

## 0.2.3 — 2026-05-14

- **Explicit opt-in for `--on-peck` shell handler** (`peck_listener.py`). The listener now refuses to run a user-supplied `--on-peck` command unless `--allow-shell-hook` is also passed. An inbound peck can never silently fan out to a local process. Built-in `--forward-to` adapters (telegram / slack / discord / email / os) are unaffected — they're pure Python, no shell exec, no flag needed.
- **`--on-peck` argv now parses with `shlex`** and runs without `shell=True`. The handler still receives the peck JSON on stdin exactly as before.
- **Envelope identity-attestation extracted into `scripts/_envelope.py`** (`canonical_v2` + `sign_v2`). `send_peck.py` imports from there now; protocol behaviour unchanged.
- No protocol change. No CLI break for `--forward-to` users. Default `pair.py --listener` auto-spawn unaffected (it never uses `--on-peck`).

## 0.2.2 — 2026-05-14

- **Include `scripts/doctor.py` in the bundle.** Read-only diagnostic by default:
  config presence + cross-dir drift, beak-key round-trip, pulse freshness,
  webhook-on-file, listener PID liveness, pending peck count. `--fix` opt-in
  with `--dry-run`. Exit codes 0/1/2/3 for clean/warn/fail/not-paired.
- No script behaviour change in any of the existing files.

## 0.2.1 — 2026-05-12

- `check_pecks.py` / `peck_listener.py` surface `shared_mds[]` metadata on
  inbound pecks; writes `_manifest.json` per peck under
  `~/.space-duck/inbox/<peck_id>.files/`.
- Best-effort fetch of each `fetch_url` using `X-Beak-Key` + `X-Spaceduck-ID`
  headers (Gap D-client preview). Server-side bridge auth shipped in
  Lambda v479 (2026-05-14), so content fetch now succeeds end-to-end.

## 0.2.0 — 2026-05-12

- Polling listener (`peck_listener.py --poll`) for laptops without public URL.
- `pair.py --listener` opt-in auto-spawn (critic-flipped from opt-out: PID
  detector only sees poll-mode listeners, would silently double-fanout against
  push-mode systemd/launchd).
- `pair.py --forward-tg-token` / `--forward-tg-chat` for Telegram fanout.

## 0.1.16b — 2026-05-12

- `chat.py` — peck-session continuation guard + tier-cap docs.

## 0.1.16a — 2026-05-12

- `send_peck.py` — pre-flight permissions check before HMAC sign.

## 0.1.15 — 2026-05-12

- Peck direction classifier (inbound / outbound / self / unknown).

## 0.1.14 — 2026-05-12

- `send_peck.py --reply-to` flag for threaded replies.
