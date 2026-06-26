# Space Duck scripts/

This directory contains every operational script a Space Duck owner needs.
The set is intentionally small, predictable, and Apple-grade in UX:

| Script | Purpose | Trigger |
|---|---|---|
| `pair.py` | First-time pair this box with a duck identity | One-shot at install |
| `setup_listeners_supervised.sh` | Stand up + restart the listener stack under supervisord | One-shot, or `--restart` |
| `telegram_listener.py` | Receive verified-HMAC peck deliveries from the gateway | Daemon (via supervisord) |
| `peck_responder.py` | Per-message handler invoked by `telegram_listener.py` | Per-peck (not persistent) |
| `peck_listener.py` | Polling-mode listener (alternative to webhook) | Daemon (optional) |
| `send_peck.py` | Send an outbound peck (CLI + library) | Per-call |
| `bind_telegram.py` | Bind a Telegram bot to this duck | Once |
| `tg_send.py` | Low-level TG send helper | Used by other scripts |
| `connections.py` | List the duck's connection set | Diagnostic |
| `workspace_bridge.py` | File-sync side of the BYOB bridge (separate port from listener) | Daemon |
| **`update.sh`** | **Apple-grade one-command skill update** | `./update.sh` or TG `/update` or MC button |
| **`doctor.sh`** | **Self-diagnosis report (paste-ready)** | `./doctor.sh` or TG `/doctor` |
| **`version_check_daemon.sh`** | **Daily registry poll; nudges owner via TG when newer version exists** | Supervisord daemon (auto) |

## Apple-grade update story (Phase 1–5, 2026-06-15)

Five entry points to the same one-tap experience. Owners can use whichever
they like — they all converge on the same signed `[OWNER-APPROVED]` dispatch
+ `update.sh` execution + listener bounce.

| Phase | Entry point | How owner uses it |
|---|---|---|
| **1** | `./update.sh` | Owner runs on their box. Wrapper auto-discovers everything. |
| **2** | `./doctor.sh` | Owner runs on their box. Output is paste-ready for support. |
| **3** | Mission Control **🧰 Skill / Version** card | One-tap "Update" button in MC — dispatches signed TG message. |
| **4** | TG `/update` or `/doctor` slash command | Type in the duck's chat. Bot sends signed prompt. Owner taps Approve. |
| **5** | Daily cron via supervisord | Polls registry every 6h; nudges TG when newer version exists. |

**Owner journey:**
1. (Optionally) installs supervisord (Phase 5 ships with this), gets daily nudges.
2. When a nudge arrives → tap "Update" in MC OR type `/update` in TG chat.
3. Bot sends `[OWNER-APPROVED HH:MM]` message with HMAC-signed marker.
4. `telegram_listener.py` (already running) verifies marker → renders Approve / Deny.
5. Owner taps ✅ Approve → listener runs `update.sh` → install + bounce + self-test.
6. Bot reports back: *"✓ Updated to v0.4.2"*.

**Zero CLI knowledge required.** Zero paths to remember. Zero error-message
parsing. If anything fails, the failure is captured in `responder.log` and
`doctor.sh` self-explains.

## Exit codes (`update.sh`)

| Code | Meaning | Recovery |
|---|---|---|
| 0 | Success (or already up-to-date) | None — done. |
| 10 | ClawHub CLI not installed | `npm install -g @clawhub/cli` |
| 11 | Skill location not discoverable | Run from `$HOME` so default install path is used |
| 12 | `clawhub install` failed | Check network; logs printed; backup preserved at `.skill-backups/<ts>/` |
| 13 | Install succeeded, listener script not found | Skill installed; start listener manually |
| 14 | Listener bounce failed | `kill -9 <pid>` + manual restart via `setup_listeners_supervised.sh` |
| 15 | Listener not pulsing within 15s post-install | Check `telegram_listener.log`; potential config issue |
| 16 | Registry unreachable AND no installed version | Check network; install fresh from registry when online |
| 20 | Unexpected error | Caught by `trap` — paste full output to support |

## Diagnostic categories (`doctor.sh`)

Report sections:
1. **Skill install** — location, installed version, latest registry version
2. **ClawHub CLI** — presence, version
3. **Identity** — config file, permissions, spaceduck_id, duckling_id, beak_key
4. **Listener processes** — telegram_listener, peck_listener, peck_responder
5. **Supervisord** — PID file, process aliveness
6. **Recent activity** — responder.log tail, error log size, auto_respond_off counter
7. **Bridge tunnel** — cloudflared/trycloudflare process, local healthz probe

Output is structured (✓ / ⚠ / ✗) with next-step hints. Safe to paste publicly
— no secrets, no bridge URLs with hash, no tokens.

## Slash commands (TG bot)

Available in every Space Duck conversation:

```
/update    — Dispatch a signed update prompt
/doctor    — Dispatch a signed doctor prompt
/peck      — Send a peck to another duck
/memory    — View current memory
/remember  — Add a fact to memory
/forget    — Wipe memory
/soul      — View persona
/setsoul   — Change persona
/model     — View/change AI model
/models    — List models your key supports
/clear     — Fresh conversation
/help      — Show all commands
```

## Mission Control card

`🧰 Skill / Version` panel renders for every duck. One button: "Update".
Tap → POSTs to `/beak/me/duck/<sd>/skill-update` → owner gets signed TG
prompt. No mid-flow forms, no version inputs, no confirmations.

## Bridge-side configuration

When `setup_listeners_supervised.sh` is run (any mode), it now also
installs the `version_check` program under supervisord, which runs
`version_check_daemon.sh` every 6 hours. The daemon:
1. Reads installed version from `_meta.json`
2. Queries the registry for latest
3. Skips if equal
4. Skips if already-nudged-this-version (idempotency via
   `~/.space-duck/last_nudge.txt`)
5. POSTs to `/beak/tg/notify` (beak-key auth) → platform sends TG message
   to the duck's owner

Daemon logs to `~/.space-duck/logs/version_check.log`.

## Invocation convention — always `bash <script>` (or `python3 <script>`)

ClawHub CLI v0.9.0 strips the Unix executable bit when installing skills.
Scripts shipped via the registry arrive at the user's box without `+x` set.
Direct invocation (`./update.sh` or `/path/to/doctor.sh`) returns
`Permission denied` (exit 126) before any of the script's own logic runs.

**Canonical workaround:** invoke every shell script via the bash binary,
which reads the file as input and doesn't need the exec bit:

```bash
# ✅ Always works, no chmod needed
bash /path/to/update.sh
bash /path/to/doctor.sh
bash /path/to/setup_listeners_supervised.sh --restart

# ❌ Requires +x — fails if ClawHub stripped it
/path/to/update.sh
```

Same property holds for Python scripts via `python3 <script>`.

**The platform respects this convention:**
- Lambda v760+: signed-action bash blocks dispatched to user boxes always
  use `bash "$SCRIPT_PATH"`, never direct exec
- Lambda v758+ TG `/update` + `/doctor` slash commands: same
- `setup_listeners_supervised.sh` supervisord `[program:version_check]`
  entry: `command=/bin/sh -c "...bash version_check_daemon.sh..."`

**For skill authors writing new scripts:**
- Use `bash` invocation in any caller documentation (READMEs, MC instructions,
  TG dispatch blocks).
- Test via `bash <script>` even if you `chmod +x` it locally — that way you
  catch any accidental dependency on exec-bit-based shebang invocation
  before users hit it.
- Skill files SHOULD still carry valid shebangs (`#!/usr/bin/env bash`,
  `#!/usr/bin/env python3`) so that if a user does grant exec bit (e.g. on a
  custom-built install path) the scripts work both ways.

**Upstream fix tracking:** filed against ClawHub CLI to preserve file modes
on `clawhub publish` → `clawhub install`. Until that lands, the `bash <script>`
convention is the canonical workaround.

## Optional: shell alias for ergonomics

Until a proper `space-duck` thin shim binary lands, owners who run
diagnostics or updates often can save typing with a shell alias. Add to
`~/.bashrc` (or `~/.zshrc`):

```bash
# Auto-discover skill directory
for _SD_DIR in \
  "$HOME/.openclaw/skills/space-duck" \
  "$HOME/.clawhub/skills/space-duck" \
  "/data/.openclaw/workspace/skills/space-duck" \
  "/data/.openclaw/skills/space-duck"; do
  [[ -d "$_SD_DIR/scripts" ]] && export SD_DIR="$_SD_DIR" && break
done
alias sd-doctor='bash "$SD_DIR/scripts/doctor.sh"'
alias sd-update='bash "$SD_DIR/scripts/update.sh"'
```

Now `sd-doctor` and `sd-update` work from anywhere. The auto-discovery
loop matches the skill's own — same paths, same precedence.

This is a stop-gap for human ergonomics; the proper UX path is the
Mission Control button + TG `/update` + `/doctor` slash commands, which
require no terminal at all.

## Doctrine

- **Read-only diagnostic, signed-action mutation.** `doctor.sh` never mutates;
  `update.sh` only mutates via a clearly logged sequence. MC button + slash
  commands always require owner TG approval (signed `[OWNER-APPROVED]`
  marker) before any bridge-side change.
- **Auto-discovery beats hard-coded paths.** Every script enumerates known
  locations before failing.
- **Snapshot before write.** `update.sh` backs up the current install before
  the new install lands, so rollback is `mv` away.
- **Idempotent.** Running any script twice produces the same end state.
- **No secrets in output.** Logs and reports are safe to paste publicly.
- **Bash invocation convention.** Scripts always invoked as `bash <script>`
  (or `python3 <script>` for Python) to sidestep exec-bit fragility — see
  section above.
