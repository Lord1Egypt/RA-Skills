# PTO Planning — Reference

## 1. Holiday tables & shift rules used

- **US federal (5 U.S.C. 6103):** fixed-date holidays falling on Saturday are
  observed Friday; on Sunday, observed Monday (the script applies this —
  e.g., July 4, 2026 = Saturday → observed Fri July 3). Thanksgiving = 4th
  Thu of Nov; MLK/Presidents/Memorial/Labor/Columbus = weekday rules.
- **UK bank holidays:** weekend dates substitute to the next Monday (incl.
  Christmas/Boxing Day shuffle). The script's `bank()` implements this.
- **DE:** fixed + Easter offsets (Karfreitag −2, Ostermontag +1,
  Himmelfahrt +39, Pfingstmontag +50). Regional holidays (Heilige Drei
  Könige, Fronleichnam, Reformationstag…) omitted — add locally.
- **FR:** the 11 national days; Vendredi Saint kept informational
  (Alsace-Moselle only).
- **Easter:** Anonymous Gregorian algorithm — exact for all years 1583+.

## 2. Efficiency doctrine

```
efficiency = consecutive_days_off / pto_days_spent
```

- 4.0 = canonical single-day bridge (holiday adjacent to weekend)
- 5.0 = jackpot: one PTO day stitched between a holiday and a weekend-holiday
  pair (UK Jan pattern above) — happens a few times a decade per country
- 2.5–3.0 = two-day brackets; 1.8 = full-week arc (9 days for 5)
- < 2.0 = usually not worth it unless you wanted the time anyway

The greedy planner picks 4.0s first, then fills with 3.0+/2.5s under a
per-quarter cap of 45% of total budget (skipped for budgets < 6, where
balancing is meaningless).

## 3. Why people lose PTO (and how this plan prevents it)

- **Unused forfeiture:** US workers left a record ~770 million days on the
  table in recent USTravel Association reporting; ~all of it preventable by
  a January plan. Typical carryover caps: 40–80 hours.
- **Reactive burning:** single midweek days (eff 1.0) instead of bridges
  (4.0) — same budget, a quarter of the recovery value.
- **Blackout collisions:** retail Nov–Dec, accounting Jan/Apr/Jul/Oct
  quarter-close, tax season at CPA firms, SaaS quarter-end for sales. Book
  the bridges in January before the freeze is announced.

## 4. Negotiating the plan with a manager

1. Bring the whole-year plan, not requests — framing as "here's my year"
   reads as responsibility, not absence.
2. Bridges cluster around company holidays — teams expect thin staffing;
  you're taking the cheapest days on the calendar.
3. Offer overlap protection: identify your backup for each bridge
  (the standup-mobi skill's coverage protocol fits here).
4. Re-confirm Q4 bridges in September — November freezes eat unbooked days.

## 5. Country notes

- **US:** "unlimited PTO" cultures take *less* time; treat a self-imposed
  budget (15–20) as real and book it. Some states (CA) forbid use-it-or-lose
  it — caps are accrual pauses, not forfeits.
- **UK:** 28 statutory days incl. bank holidays for full-time — the script's
  bridge list shows why Jan and Easter punch above their weight.
- **DE:** 20 statutory + regional; Betriebsferien (plant shutdowns) in Aug
  and late Dec concentrate everyone's vacation — book summer by March.
- **FR:** August shutdown culture; the *good* windows for solo quiet time
  are May's bridge cluster (pont de l'Ascension) — the script surfaces them.

## 6. ICS format notes

Events are all-day (`VALUE:DATE`), DTEND is exclusive per RFC 5545. PTO
events are opaque blocks; the "OFF run" events are TRANSPARENT (visible but
non-blocking). Import to Google Calendar / Outlook / Apple via file import.
