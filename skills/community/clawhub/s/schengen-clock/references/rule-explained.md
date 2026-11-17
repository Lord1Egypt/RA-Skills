# The Schengen 90/180 Rule — Mechanics, Traps, and Border Tactics

## The rule in one sentence

A non-EU short-stay visitor may be present in the Schengen area **at most 90
days inside any 180-day window**, where the window rolls every single day and
both the entry day and the exit day count as presence days.

## Why the rolling window breaks brains

Most people model allowance as "90 days per visit" or "180 days per year."
Both models are wrong:

- **"90 per visit"** — false. Enter Jan 1, stay 90 days, exit Mar 31. Re-enter
  Apr 10: the window ending Apr 10 looks back to Oct 12 of the previous year,
  which contains your entire 90-day stay. Allowance: **0 days**. Entry refused.
- **"Per calendar year"** — false. Presence on Feb 28 (year A) and presence on
  Jan 10 (year B) can share a rolling window. Calendar boundaries mean nothing.

The only correct mental model: **every day you want to be present, look back
180 days and count.** That is what `status`, `maxstay`, and `plan` do — day by
day, window by window, no approximations.

## Worked example (the registry from the SKILL.md demo)

| Stay | Dates | Days |
|---|---|---|
| FR | 2026-03-05 → 2026-03-18 | 14 |
| IT | 2026-05-10 → 2026-06-02 | 24 |
| ES | 2026-07-01 → 2026-08-30 | 61 |

Query: status on 2026-10-01. Window = 2026-04-05 … 2026-10-01.

- FR stay: entirely before Apr 5 → 0 days count.
- IT stay: fully inside → 24 days.
- ES stay: fully inside → 61 days.
- Total: **85 used, 5 remaining.**

The FR days "came back" — but only because the window slid past them. On
2026-09-01, the FR stay still partially counted. Nothing resets on a fixed
date; days expire on their own 180-day anniversary.

Max-stay if entering 2026-10-12: 5 days (exit by 2026-10-16). Anyone planning
"October in Europe" with this history would discover at check-in that the
airline's math says no.

## The four classic traps (what `traps` scans for)

1. **Back-to-back long stays.** ~60 days in, brief exit, ~40+ days back in.
   The second stay is capped by the still-warm first stay. Detection: gap ≤ 10
   days with lengths ≥ 60 + ≥ 40.
2. **Thin margin (<5 days).** A planned stay peaking at 85–90/90 has no slack
   for a delayed flight, illness, or a miscounted stamp. Detection: worst-window
   usage of planned (future) stays.
3. **Overstay already in history.** Any window where recorded presence > 90.
   Border authorities see this on next entry; penalties escalate. Detection:
   audit at every historical exit date.
4. **De-facto residence pattern.** 150+ presence days per rolling window,
   year-round. Border officers can refuse entry for "insufficient ties to home
   country" even when the letter of the 90/180 rule is satisfied.

## Counting details that matter

| Question | Answer |
|---|---|
| Does the entry day count? | Yes — day 1 of presence |
| Does the exit day count? | Yes — presence includes the exit day |
| I entered at 23:50 — half day? | No. Calendar day counts in full |
| Time in UK/Ireland/Cyprus? | Not Schengen — does not count (and doesn't pause your clock) |
| Time in San Marino/Vatican/Monaco? | No controls — counts as Schengen presence |
| Croatia? | Schengen since 2023-01-01 — counts |
| Romania/Bulgaria? | Air/sea borders March 2024, land March 2025 — counts |
| A cancelled flight kept me one extra day? | Ask the border police for a stamped extension note *before* day 91; airlines do not decide this |

## Overstay consequences, by severity

- **1–5 days, first offense, provable transit error** — usually a warning or
  fine at exit, but recorded in the entry/exit system (EES).
- **Larger/repeated** — fines (country-dependent, tens to hundreds of euros per
  day), removal, and an entry ban: typically 1 year, up to 3–5 for egregious
  cases, more with aggravating factors (work, deception).
- **Any overstay** — future visa applications must disclose it; EES records
  persist and are visible to all member states.

The EES (Entry/Exit System) digitized this: stamps are being replaced by
biometric logs that compute your 90/180 status automatically at every border.
The era of "the officer didn't count carefully" is over — which is exactly why
you should count carefully.

## Border interview tactics

When asked "how long are you staying?":

1. Answer with an exact date, not a vibe: "Until November 20th, 39 days."
2. Have the return ticket and the first hotel visible on your phone.
3. If you've had multiple stays, offer the math unprompted — the `letter`
   command prints a one-pager with the rolling-window calculation. Officers
   handle dozens of confused tourists daily; a person who knows their window
   arithmetic ends the conversation fast.
4. Never argue the rule with the officer. If their number differs from yours,
   ask politely for a supervisor — after complying.

## Who this tool is for (and not for)

**For:** visa-exempt passport holders (US, UK, Ukraine, Georgia, Armenia,
Serbia, North Macedonia, Bosnia, Moldova, Albania, Kosovo, Japan, Korea,
Australia, Canada, Brazil, Mexico, Malaysia, …) making multiple Europe trips,
digital nomads "tourist-visa hopping," snowbirds, and anyone who once lost a
weekend of their life to 90/180 arithmetic on a napkin.

**Not for:** D-visa / national long-stay holders (time on a single country's
long-stay visa generally doesn't consume 90/180 — but cross-country rules are
national), residence permit holders, working-holiday schemes, or asylum
procedures. Those regimes interact with 90/180 in ways this tool does not model.

## Final honesty

This is arithmetic, not legal advice. Consulates and border authorities apply
the rule to your specific passport, visas, and record. When the math and the
authorities disagree, the authorities are the fact on the ground.
