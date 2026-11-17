---
name: simplisafe-api
description: Query and control a SimpliSafe alarm system from the shell with curl — read system state, sensors, locks, events and settings, and arm/disarm or lock/unlock. Use when the user asks about their SimpliSafe alarm, house sensors, door locks, or whether the system is armed. Requires a one-time browser login to mint a refresh token.
---

# SimpliSafe from the shell

SimpliSafe's API is reachable **server-side** — no browser bridge, no extension,
no signed-in tab. Auth is a bearer token minted from a long-lived OAuth refresh
token, so everything here is plain `curl` + `jq`.

Requires `curl` and `jq`.

## One-time setup

SimpliSafe issues no API keys. The credential is an OAuth refresh token, minted
by a browser login you do **once**:

```bash
node ~/git/simplisafe-mcp/scripts/bootstrap-auth.mjs           # prints an authorize URL
# sign in, then copy the com.simplisafe.mobile://... URL the browser fails to open
node ~/git/simplisafe-mcp/scripts/bootstrap-auth.mjs "<that URL>"
```

That writes `SIMPLISAFE_REFRESH_TOKEN` to `~/git/simplisafe-mcp/.env` (mode 0600).
SimpliSafe does **not** rotate refresh tokens, so this survives indefinitely —
until you sign out of all devices in the SimpliSafe app, which revokes it.

To capture the code from the browser: open DevTools → Network → tick **Preserve
log** *before* signing in, then find the failed navigation to
`com.simplisafe.mobile://…?code=…` and copy its link address. The code is
single-use and expires in ~2 minutes.

## Core pattern

```bash
source ~/git/simplisafe-mcp/skills/simplisafe-api/references/ss-helpers.sh

ss_api GET /api/authCheck | jq            # who am I
SID=$(ss_sid)                             # the single active system id
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" | jq
```

`ss_api <METHOD> <PATH> [JSON_BODY]` attaches auth, prints the body on stdout,
and on a non-2xx prints to **stderr** and returns 1 — so a failure never looks
like an empty result. Access tokens are cached in `$TMPDIR` (0600) and re-minted
only when stale; the helpers never write to the repo's `.env`.

## Resolve first

Almost every path needs a **system id (`sid`)**, and getting one takes two calls
(`authCheck` → `userId`, then the subscriptions route). `ss_sid` does both, and
**fails loudly if the account has more than one system** rather than guessing —
pass the sid explicitly in that case.

Note two routing traps:

- The system version that decides `ss3/` routing is at
  `location.system.version`, **not** the top-level `systemVersion` (a different
  number entirely).
- **Events and doorlock control are NOT under the `ss3/` prefix.** Everything
  else is.

## Reads

```bash
# Is it armed? -> OFF | HOME | AWAY | HOME_COUNT | AWAY_COUNT | ALARM
ss_api GET "/users/$(ss_api GET /api/authCheck | jq -r .userId)/subscriptions?activeOnly=true" \
  | jq -r '.subscriptions[0].location.system.alarmState'

# Anything wrong with a sensor?
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq '[.sensors[] | select(.flags.offline or .flags.lowBattery) | {name, type, flags}]'

# Recent activity
ss_api GET "/subscriptions/$SID/events?numEvents=10" \
  | jq -r '.events[] | "\(.eventTimestamp|todate)  \(.info)"'
```

More recipes, including lock state and base-station health:
[references/recipes.md](references/recipes.md).

## Writes — read this before running one

These commands act on a **physical security system**. Disarming leaves a house
unmonitored; arming can trip a siren and a monitoring-center dispatch; unlocking
opens a real door. Confirm intent with the user before running any of them, and
never run one speculatively.

```bash
ss_api POST "/ss3/subscriptions/$SID/state/away"      # or /home, /off — no body
ss_api POST "/doorlock/$SID/<serial>/state" '{"state":"lock"}'   # or "unlock"
```

**A 2xx is not proof it worked.** Re-read and check one field:

```bash
sleep 3
ss_api GET "/users/$(ss_api GET /api/authCheck | jq -r .userId)/subscriptions?activeOnly=true" \
  | jq -r '.subscriptions[0].location.system.alarmState'
```

Four things that make naive verification lie:

- Arming reports `AWAY_COUNT` / `HOME_COUNT` while the exit delay runs, settling
  to `AWAY` / `HOME`. That is success in progress, not failure.
- Do **not** diff whole objects — `alarmStateTimestamp`, `stateUpdated` and
  `lastUpdated` advance on their own, so any call would look successful.
- **Re-read locks with `forceUpdate=true`.** The cached payload lags by minutes
  and has been seen reporting a *jammed* lock as cleanly `unlocked`.
- **A lock takes ~5 s to report**, so a 3-second check calls a successful unlock
  a failure. Poll, don't sleep once.

**Arming also LOCKS your doors.** Each lock's `setting` has `home`/`away` flags
that auto-lock on arm, and `homeToOff`/`awayToOff` controlling whether disarming
unlocks them. With `homeToOff: 0` (common), arm-then-disarm leaves the doors
locked — so it is *not* a safe way to test arming. Check with:

```bash
ss_api GET "/ss3/subscriptions/$SID/sensors?forceUpdate=false" \
  | jq -r '.sensors[] | select(.type==16) | "\(.name)\t\(.setting)"'
```

A lock reporting `lockJamState: 1` will not respond to commands at all: the POST
still returns `200`, and nothing moves. That is a hardware fault, not a bad
request.

## PINs are cleartext

`/ss3/subscriptions/$SID/settings/normal` returns `settings.pins` — the master,
duress and named-user **alarm codes, in cleartext**, in the same payload as the
harmless settings. Project `.settings.normal` unless the user explicitly wants
the codes:

```bash
ss_api GET "/ss3/subscriptions/$SID/settings/normal?forceUpdate=false" | jq '.settings.normal'
```

## In context groups

When the MCP server (`simplisafe-mcp`) is hosted behind mcp-host with context
groups on, its tools belong to the **home** group (`_meta.mint.domain: home`).

- **Canonical read:** `simplisafe_get_events` answers *what's new* at home. With
  `view: "brief"` it returns one line per event — `<sensor>: <event> — <ISO
  time> — <event type>`, cut to ≤ 120 chars as a whole (title first) — as the
  untrusted-data envelope's `data` array (event text is SimpliSafe's, sensor
  names are whoever set the system up), with `-- none` for an empty log and
  `-- more` when the page came back full. A title starting with `-- ` or `\`
  is escaped with one leading `\`, so a sensor name never reads as a note. There is no whats-due or whats-on read: nothing here is scheduled.
- **No subject:** `sid` is optional on a one-system account. A system's only
  label is its location, so the server does not publish one in its schema. On
  an account with several systems, the group read without a `sid` returns the
  server's "`sid` is required" error rather than guessing.
- **Writes:** `simplisafe_set_alarm_state` (arm/disarm) and
  `simplisafe_set_lock_state` are `turn-on-off` hints. They are never canonical,
  and they still ask for confirmation. The rest are `lookup`.
- **A compound ask** looks like "anything new at home, and is the pool heater
  on?" — the group asks this server for its brief events beside the other home
  members.
- Not browser-bridged: the server talks to SimpliSafe's API directly, so the
  group never answers "needs your browser open" for it.

## Notes

- `forceUpdate=true` makes the base station re-poll its devices — slower and
  harder on the hardware. Leave it `false` unless freshness matters.
- Lock state encoding is counter-intuitive: `lockState` **1 = locked, 2 =
  unlocked**, and `lockJamState` overrides both.
- Device type ids `21`, `23` and `24` appear on real systems but aren't in any
  public enum — handle unknown types gracefully.
- Avoid tight polling; the API rate-limits.

Full verified endpoint reference: `~/git/simplisafe-mcp/docs/SIMPLISAFE-API.md`.
