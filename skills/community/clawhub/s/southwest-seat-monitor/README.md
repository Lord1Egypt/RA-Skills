# southwest-seat-monitor

Watch a Southwest Airlines seat map for a better seat — built by [papiprompts](https://github.com/jdm0830).

## Why this exists

Southwest moved to **assigned seating**. Which means there's now a seat map worth watching, and
which means the good seats — windows especially — get taken early and then occasionally **free up**
when someone moves or cancels.

The problem: you're not going to refresh a seat map every 10 minutes for a week.

So this watches it for you. Point it at a segment, tell it what you want (a window, an aisle, an
exit row), and it pings you the moment one opens. **Read-only — the seat grab stays yours.**

## What it does

- Watches a specific segment's seat map for a target seat type becoming available.
- **Read-only.** It never submits a seat change; you do the swap yourself.
- Alerts on **state change**, not every poll — one ping per newly-open seat.
- **Session-health aware** — distinguishes "no seats available" from "not logged in", and alerts
  on the latter instead of silently reporting zero.

## How it works (the important bit)

Southwest's site is bot-defended, and there's a trap that costs hours if you don't know it:

**The correct seat-map entry is the tokenized reservation flow, not the footer link.**

```
✅  My Account → "Details"  →  /air/manage-reservation/view?searchToken=…
✅  then "Upgrade or modify seats"  →  /air/seat/select-seats?...&searchToken=…
❌  "Change or Upgrade Seats"  →  /air/seat/?clk=GFOOTER-AIR-SEATS   ← no token, empty shell
```

The footer link has **no reservation token**, so the seat app loads an empty shell and never
requests a map. That's the whole trick.

Then: the seat page opens on the **outbound** segment — you click the button for the segment you
want (`FLIGHT 2 of 2 MCO to LAS`) before reading seats.

**Reading seats:** each seat is a `<button>` whose `aria-label` says everything:
```
Seat 4F $94. (Chargeable, Front cabin, Extra leg room, Window)
Seat 1A $94. (…, Window) unavailable
```
→ **open/occupied** = the button's disabled state; **window/aisle/middle** = named in the label.
Equivalently, the seat-map JSON at `/api/seat-management/v1/seatmaps/selections` carries
`{column, characteristics[], available: true|false}`.

**Window location** comes from the map's own column legend: `A = WINDOW, F = WINDOW`.

## Design principles

- **Read-only.** Never submits a seat change.
- **Randomized intervals** (8–18 min) — fixed cadence is a bot tell. Tightens to 3–5 min inside the
  final 24h before departure.
- **Waking hours only**, with a daily call cap.
- **Auto-stop + alert** on 403/429/challenge, and on repeated session failures.
- **Alert the agent, not the human.** The agent is the filter; the human hears only about a real
  opening or a broken session.
- **One careful browser session**, never parallel contexts against one account — that's the
  fingerprint that trips airline bot-defenses.

## Requirements

- [patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) (or Playwright)
- A real headed Chrome with a **persistent, already-logged-in profile**, exposing a CDP port
- A Southwest account

## Layout

```
SKILL.md                 # the skill (read this first — full flow + pitfalls)
scripts/monitor.mjs      # reference implementation (--once, or loop with guardrails)
package.json
```

## Usage

```bash
node scripts/monitor.mjs --once      # single check, print result
node scripts/monitor.mjs             # loop: randomized intervals, waking hours, daily cap
```

Config via env (all optional): `SW_CDP`, `SW_TARGET_LABEL`, `SW_TARGET_AIRPORT`,
`SW_WINDOW_COLUMNS`, `SW_FLIGHT_DEP`, `SW_DAILY_CAP`, `SW_WAKE_START/END`, `SW_MIN_MIN/MAX_MIN`,
`SW_AGENT_SESSION`.

## Notes on sharing

- Bring your **own** logged-in profile. The skill never asks for or stores your Southwest password.
- Set your own segment (`SW_TARGET_LABEL` / `SW_TARGET_AIRPORT`) and target columns.
- Keep it read-only unless you deliberately want otherwise.

## Credits

Built by **papiprompts**.

## License

MIT — use it, fork it, improve it. A tip is appreciated but never expected.
