---
name: southwest-seat-monitor
description: Southwest-specific seat monitor. Watch a specific Southwest segment's seat map (via the tokenized reservation seat flow) for a window/aisle/exit seat becoming available, and alert the agent when one opens. Use when the user asks to monitor Southwest seat availability, watch for a Southwest window seat, or track seat openings on a Southwest booking. Companion to the generic seat-monitor skill (read that first) and the travel-agent skill.
---

# Southwest Seat Monitor

Implementation layer for the generic `seat-monitor` pattern, specific to **Southwest Airlines**
(assigned seating, post-2025 model). Read-only. Never submits a seat change.

## Verified flow (proven working — do not re-derive)
The **only** route that loads a real seat map:

1. `https://www.southwest.com/loyalty/myaccount/` — signed-in account page.
   - Confirm signed in: page shows "My Account" / "You Have N Upcoming Trip!". If it shows a
     sign-in form instead → session is dead; alert, do not silently report "0 seats".
2. Find the trip's **`Details`** link → `/air/manage-reservation/view?searchToken=…`
   - This tokenized URL carries the reservation. There may be several trips; pick the right one
     (match by date/route — e.g. "Round trip - Oct 19 - 22 Las Vegas, NV to Orlando, FL").
3. On the reservation page, click **`Upgrade or modify seats`** →
   `/air/seat/select-seats?clk=TRIPDETAILS_UPGDSEAT_LINK&searchToken=…`
   - ⚠️ **Do NOT** use the footer link `Change or Upgrade Seats` → `/air/seat/?clk=GFOOTER-AIR-SEATS`.
     It has **no token** and renders an empty shell (`air-seat-index`, no seats). This is THE trap.
4. The seat page opens on the **outbound** segment. Switch to the target segment by clicking the
   button whose text contains e.g. `FLIGHT 2 of 2 MCO to LAS` (buttons read
   `FLIGHT <n> of <total>\n<ORIG>\nto\n<DEST>\n<duration>`).
5. Read the rendered seat buttons.

## Reading seat state (two equivalent sources)

### A. DOM (what the monitor uses — most robust)
Every seat is a `<button>` with an `aria-label` like:
```
Seat 4F $94. (Chargeable, Front cabin, Extra leg room, Window)
Seat 8E Selected for passenger number 2 JUAN MAZO. $38. (Chargeable, Preferred, Over wing, Middle)
Seat 1A $94. (Chargeable, Front cabin, Bulkhead seat, Extra leg room, Window) unavailable
```
- **Open vs occupied:** the button is `disabled` / `aria-disabled="true"` / class contains
  `disabled` when taken. Available seats are enabled.
- **Seat type:** the label names it — `Window` / `Middle` / `Aisle`.
- Class names seen: `seat__… occupied__…`, `seat__… preferred__…`, `seat__… extraLegRoom__…`,
  `seat__… standard__…`, `seat__… unavailable__…`.

### B. JSON (captured passively, same info)
- `GET /api/seat-management/v1/seatmaps/selections` (arrives only when entered via the tokenized
  flow; ~52–66 KB). Shape:
  ```
  data[0] = {
    flight_segment: { marketing_flight_number, origination_airport_code, destination_airport_code,
                      depart_at, flight_equipment_type_code },
    cabins[0]: {
      columns[7]: [ {type:"SEAT", column:"A", position:"WINDOW"}, … ]   ← the legend
      rows[33]:   [ { row_number, seats: [ { column, characteristics[], available: true|false,
                                             price:{…} } ] } ]
    },
    price_summary: { CHARGEABLE, PREFERRED, EXTRA_LEGROOM, EXIT_ROW, STANDARD, … },
    original_seats: [ { row, column, characteristics[], passenger_id, … } ]   ← the user's seat
  }
  ```
- Also `GET /api/seat-management/v1/reservations?search_token=…` and
  `GET /api/air-manage-reservation/v1/reservations?search_token=…`.

## Column legend (window location)
From `cabins[0].columns` (and the visible header):
```
A = WINDOW   B = MIDDLE   C = AISLE   |   D = AISLE   E = MIDDLE   F = WINDOW
```
→ **Window seat = column "A" or "F".** Always confirm from the map's own columns array; aircraft
type can vary (`73H`, `7S7`, …).

## Itinerary / seat lookup (account-level)
- `GET /api/loyalty-management/v2/loyalty-management/accounts/self/future-air-reservations-secure`
  → trips, segments (`segment_identifier` 1=outbound, 2=return), and
  `passengers[0].seats[]` = `{segment_reference, seat_number, characteristics[]}`.
- `GET /api/security/v4/security/userinfo` → session validity.
- ⚠️ **Never `page.goto()` these JSON endpoints directly** — direct endpoint hits get 403 (Akamai).
  Navigate the UI and capture passively.

## Anti-bot notes
- Use a **real headed Chrome** (`/usr/bin/google-chrome-stable`) with a **persistent profile**,
  driven over CDP, on a VNC/X display. Bundled Chromium is a weaker fingerprint.
- Save the login in the profile's password manager as a self-heal aid (caveat: OS keyring may be
  locked on a bare-X host; a login prompt stalls silently → must be caught by the health check).
- Randomize intervals; never fixed-cadence.

## Reference implementation
`~/.openclaw/state/southwest/monitor4.mjs` — v4, agent-alerting + session health:
- `--once` single check; default = loop with randomized 8–18 min (3–5 min within final 24h).
- Waking hours 07:00–23:00 PT; daily cap 60; auto-alert on session failure.
- Env-overridable: `SW_STATE`, `SW_CDP`, `SW_TARGET_LABEL`, `SW_TARGET_AIRPORT`,
  `SW_WINDOW_COLUMNS`, `SW_DAILY_CAP`, `SW_WAKE_START/END`, `SW_MIN_MIN/MAX_MIN`,
  `SW_TIGHT_MIN_MIN/MAX_MIN`, `SW_FLIGHT_DEP`, `SW_AGENT_SESSION`.
- Files: `monitor.log`, `alerted-windows.json`, `counter.json`, `health.json`, `monitor-out/latest-seats.json`.
- Alerts go to the **agent session** (`SW_AGENT_SESSION`), which relays to the human as needed.

## Failure modes & fixes
| Symptom | Cause | Fix |
|---|---|---|
| seat page shows no seats | used footer link (no token) | use `Details` → `Upgrade or modify seats` |
| no seat link found | SPA hadn't rendered | poll for the link (up to ~15–20 s), don't check once |
| 403 on trips/seat JSON | direct endpoint `goto()` | navigate the UI, capture passively |
| signed-in check fails | session expired | health alert → human re-login in the profile |
| wrong leg's seats | seat page defaults to outbound | click the `FLIGHT n of m <DEST>` segment button |

## Reboot persistence (TODO / optional)
The reference impl is a bare node process — survives session end, not reboot. To survive reboot,
wrap in a systemd user unit that also keeps Chrome (CDP 9222) alive with the southwest profile.
