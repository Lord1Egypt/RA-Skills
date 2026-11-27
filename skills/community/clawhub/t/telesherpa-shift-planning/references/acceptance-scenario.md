# Acceptance scenario (end to end, phases 0–4)

One continuous test with fixed, fictional start data and expected values. A fresh
agent runs it once from an empty account; the paid run is measured with
[measurement.md](measurement.md). Every step names the **role** that performs it and
the **expected result**; a step passes only when the result is read back (tool read
or browser), not when the write call returned "OK".

- Business: **Trattoria Example**, slug `trattoria` → scopes `trattoria_master`,
  `trattoria_planning`, `trattoria_team`.
- All test objects carry the prefix `TEST-A-` (A = acceptance). All addresses are
  `@example.com` in this document. These are not activatable human mailboxes.
  Before login tests, obtain explicit permission for dedicated controlled test
  mailboxes or another supported active test-account route, and align their master
  person e-mails with those logins. If only `example.com` data is permitted, keep
  the synthetic fixtures and mark staff-login tests blocked. Never use real staff data.
- Roles: **M** = manager account (owner of the three scopes,
  `manager@example.com`); **S** = a staff account (managed, rights per phase 0);
  **T** = trigger / platform (asynchronous, wait up to 5 minutes, scheduled rules
  every 5 minutes).
- Times are sent with `Z`/offset (a bare `YYYY-MM-DD HH:MM:SS` is read in the viewer's zone);
  reads return the UTC value plus the `_local` sibling — compare UTC with UTC.
- Both test months lie in 2026 (month A = October, month B = November). The
  threshold year follows the current date, not the month: run the payroll checks
  while the current date is in 2026, or compare against the 2026 limit by hand.
- Budget: the credit estimate per phase and the cap are in
  [measurement.md](measurement.md) §3; read the balance before and after each phase.

## 1. Start data

### 1.1 Site and stations (master)

| Object | Name | Values |
|---|---|---|
| organisation | `TEST-A-Trattoria Example` | |
| building (site) | `TEST-A-Trattoria Example Main Street` | opening Tue–Sun, closed Monday |
| space (stations) | `TEST-A-Kitchen`, `TEST-A-Service`, `TEST-A-Bar`, `TEST-A-Dishwashing` | `station` = `kitchen`, `service`, `bar`, `dishwashing` |

### 1.2 People (master: basic data; planning: staff record)

| # | Person (master) | Login e-mail | Qualified for | Birth year | Staff record: contract / hourly rate | Account |
|---|---|---|---|---|---|---|
| P1 | `TEST-A-Test Cook` | `test.cook@example.com` | kitchen | 1990 | `fullTime` / 16.00 | staff S1 |
| P2 | `TEST-A-Pat Server` | `pat.server@example.com` | service | 1998 | `minijob` / 13.90 | staff S2 |
| P3 | `TEST-A-Sam Bar` | `sam.bar@example.com` | bar, service | 1995 | `partTime` / 15.00 | staff S3 |
| P4 | `TEST-A-Kim Dish` | `kim.dish@example.com` | dishwashing | 2009 (under 18) | `casual` / 13.90 | none (manager acts) |
| P5 | `TEST-A-Lee Service` | `lee.service@example.com` | service | 1988 | `fullTime` / 16.50 | none |

Hourly rates are fictional and only have to be at or above the national minimum wage
of the country module (see country module).

### 1.3 Templates (master)

| Template | Station | Start–end | Break | Planned hours | Weekdays |
|---|---|---|---|---|---|
| `TEST-A-Kitchen early` | kitchen | 09:00–15:30 | 30 | 6.0 | Tue–Sun |
| `TEST-A-Kitchen late` | kitchen | 16:30–23:00 | 30 | 6.0 | Tue–Sun |
| `TEST-A-Service lunch` | service | 11:00–15:00 | 0 | 4.0 | Tue–Sun |
| `TEST-A-Service evening` | service | 16:30–23:30 | 30 | 6.5 | Tue–Sun |
| `TEST-A-Bar evening` | bar | 17:00–23:00 | 30 | 5.5 | Wed–Sun |
| `TEST-A-Dishwashing evening` | dishwashing | 18:00–22:00 | 0 | 4.0 | Fri–Sat |

### 1.4 Two months

- **Month A = 2026-10 (past, for payroll):** shifts created, staffed and published,
  actual times entered by manager correction (clocking always writes "now").
- **Month B = 2026-11, plan week 2026-11-16 … 2026-11-22 (live flow):** generation,
  publication, requests, day-off wish, clocking by staff.

Month A shifts:

| Person | Template | Dates (2026-10) | Planned | Actual (correction) |
|---|---|---|---|---|
| P2 Pat | Service evening | 02, 03, 09, 10, 16, 17, 23 | 7 × 6.5 = 45.5 | as planned, except 09: 16:00–23:30, 16: 16:00–23:30, 23: 15:45–23:30 (break 30 each) → 47.25 |
| P2 Pat | Service evening | 24 — **cancelled** | excluded | excluded |
| P3 Sam | Bar evening | 07, 14, 28 | 3 × 5.5 = 16.5 | as planned → 16.5 |
| P4 Kim | Dishwashing evening | 02, 09 (end 22:00) | 2 × 4.0 = 8.0 | as planned → 8.0 |
| P1 Cook | Kitchen early | 06, 07, 08, 13 | 4 × 6.0 = 24.0 | as planned → 24.0 |
| P5 Lee | Service evening | 01, 08, 15, 22, 29, 30 | 6 × 6.5 = 39.0 | as planned → 39.0 |

23 shifts in month A (22 valid + 1 cancelled). Start dates of all month-A shifts fall
in October, none crosses midnight.

## 2. Steps

### Phase 0 — scopes, rights, types, fields

| # | Role | Step | Expected result |
|---|---|---|---|
| 0.1 | M | read prerequisites: health, `auth_status`, `onto_credit_balance`, `onto_credit_pricing` | pay-per-use account; balance ≥ budget; price table saved with time |
| 0.2 | M | create the three scopes ([phase0.md](phase0.md)) | `ontouser_scope_index` lists exactly `trattoria_master`, `trattoria_planning`, `trattoria_team`; balance −260 (three scopes at the volume price: 100 + 80 + 80) |
| 0.3 | M | activate types and create the scope-own properties | `ontouser_scope_types` per scope as in phase 0; option values English (`published`, `kitchen`, `minijob`, …) |
| 0.4 | M | activated staff accounts S1–S3 exist through the authorised test-account route (placeholder example.com addresses alone cannot be activated) as managed accounts (phase 3 §3 may be pulled forward) and get rights | S1–S3: master R, **no** planning membership, team RW |

### Phase 1 — master data, templates, plan, publication

| # | Role | Step | Expected result |
|---|---|---|---|
| 1.1 | M | create site and four stations (`sp_site_create`, `sp_station_create`) | objects in master with `station` values as in 1.1 |
| 1.2 | M | create P1–P5 (`sp_staff_create`), qualifications (`sp_qualify_for_station`) | master persons with name, login e-mail, birth year only; `concerns` links with the link values `employedAt` (site) and `qualifiedFor` (station, P3 two stations) |
| 1.3 | M | create the six templates (`sp_template_create`) | six `shiftTemplate` objects in master; planned hours as in 1.3 after the trigger |
| 1.4 | M | month A: create the 23 shifts already staffed (`sp_shift_from_template` with the person; `sp_shift_staff` only applies to open shifts), publish each (`sp_shift_publish`) | 23 shifts, 23 `worksShift` links; status `published`; initialise historical shifts to `firstNoticeStatus = sent` before enabling notification rules, so month A has no catch-up messages |
| 1.5 | M | cancel Pat's 2026-10-24 shift (`sp_shift_cancel`) | status `cancelled`; manager note created (`sp_cancelled_shift_note`) |
| 1.6 | M | month B: plan period 2026-11-16…22 (`sp_period_create`), week request, generation by weekday | shifts generated per template and opening day; no shift on Monday 2026-11-16 |
| 1.7 | M | staff week B: P2 Service evening Fri 20 + Sat 21; P3 Bar evening Thu 19; P1 Kitchen early Wed 18; one Service lunch on Sat 21 stays **open** | `sp_week_list` and `sp_week_grid` show it; open shift visible as open |
| 1.8 | M | publish the staffed shifts of week B one by one | status `published`; `firstNoticeStatus` still `open` until the rule runs, then `sent` |
| 1.9 | M | rule check: Dishwashing Sat 21, 18:00–23:00 (`sp_open_shift_create`), staffed with P4 Kim (under 18) | `sp_rule_check` lists the row with "Minor after 22:00" (shift ends 23:00); do not publish it |
| 1.10 | M | create isolated TEST probes on a separate date: one 11-hour planned shift, a second shift for the same person making the day total >10, and next shift <11 hours later | `longShift`, `dailyHours`, `shortRest` flags appear on the corresponding rows; the view lists only rows with at least one flag, so a control shift without any condition is absent |
| 1.11 | M | open `sp_shift_lead_today` without a date (opens on today), then on a one-day test period | "Open shifts today" = rows of that day without a person in the table; "Started without actual time" = all past shifts without actual start, independent of the chosen day; "Open requests" = rows with `proposed` in `sp_request_inbox` |
| 1.12 | M | create a TEST trash probe shift, delete that exact object using the normal delete UI; open `sp_recycle_bin`, then restore it | deleted probe visible only in trash; Restore removes it from trash; never purge test objects just to prove visibility |

### Phase 2 — requests, absences, decisions

| # | Role | Step | Expected result |
|---|---|---|---|
| 2.1 | S2 | takeover request on own Fri-20 shift, partner P3 (`sp_takeover_request`) | `changeRequest` `takeover`, `proposed`, links `shiftSwap`, `requestedBy` P2, `takingOver` P3 |
| 2.2 | M | request inbox → Decide (`sp_swap_decide` only; `sp_swap_execute` is the manual path without a request and is **not** run here) | P3 on the Fri-20 shift, P2 removed; request `accepted`; shift status unchanged (`published`) |
| 2.3 | S3 | shift request on the open Service lunch Sat 21 (`sp_shift_request`) | request `shiftRequest`, `requestedBy` P3 |
| 2.4 | M | reject the shift request (`sp_shift_request_reject`) | request `rejected`; shift still open |
| 2.5 | S1 | absence: day-off wish 2026-11-22 (`sp_absence_request`, `dayOffWish`) | `absence` in planning, `requested`, `concernsPerson` P1 |
| 2.6 | M | approve the day-off wish (`sp_absence_approve`) | `approved`; precheck shows no conflicting shift (P1 not on 22) |
| 2.7 | S1 | absence: vacation 2026-11-18 (P1 is on Kitchen early that day) | request created |
| 2.8 | M | approve → precheck warns about the overlapping shift → confirm | `approved`; P1 released from the 18th; manager note "absence released shift" |
| 2.9 | S1, then M | Request absence on a colleague's readable master person; complete kind `dayOffWish`, a test day's start/end, half day `false`, status `requested`, then save | refused by the form guard ("This form does not concern your person"); no `requested` answer for the colleague; remove the empty draft; do not approve anything |

### Phase 3 — staff view, start card, notifications

| # | Role | Step | Expected result |
|---|---|---|---|
| 3.1 | M | create `sp_my_next_shift`, `sp_my_shifts`, `sp_my_week`, `sp_my_requests`, `sp_my_absences`, `sp_open_shifts`, start card "My shifts" | definitions use `person`/`passt` as in phase 3; `onto_startcard_index` lists the card in `trattoria_team`; as S1 the card opens the own shifts |
| 3.2 | S2 | log in, start page | card "My shifts"; only own shifts (Sat 21 only, after the takeover) |
| 3.3 | S3 | "My shifts" | Thu 19 and Fri 20 (taken over) |
| 3.4 | S1 | "My absences" | day-off wish 22 approved, vacation 18 approved, no colleague's absence (confirm in the browser) |
| 3.4a | S2 / S3 | "My requests" | own or involved takeover / shift requests, correct statuses; no unrelated requests; newest change first |
| 3.4b | S2 / S3 | "My week" for 2026-11-16 | same own shifts as My shifts within the selected week; changing week changes the rows |
| 3.4c | S3, then S1 | "Open shifts for me" | S3 sees the unstaffed Service lunch Sat 21 (qualified); S1 does not (kitchen only); staffed, cancelled and past shifts excluded |
| 3.5 | T | messages after steps 1.8–2.8 (rules switched on in test mode: in-app only) | exactly the expectations of section 4 |
| 3.6 | M | switch e-mail/push on after 3.5 passed | `onto_trigger_index`: rules `email: true`, `push: true` |

### Phase 4 — clocking, corrections, staff records, payroll

| # | Role | Step | Expected result |
|---|---|---|---|
| 4.1 | M | staff records for P1–P5 (`sp_staff_record_create`) with contract and rate from 1.2 | five records in planning; master persons still without contract/rate/phone |
| 4.2 | S3 | Clock in on own Thu-19 shift (note "test") | `actualStart` = now, `clockedIn`, actor comment; S3 balance −20; if run before the planned day, record that early clock-in is permitted (no time window) |
| 4.3 | S3 | Clock out, break 30 | `actualEnd`, `actualBreakMinutes = 30`, `clockedOut`; `actualHours` after ≤ 5 min |
| 4.4 | M | correct Thu-19 to 17:00–23:00, break 30, reason "test correction" | `corrected`; comment shows old → new for start, end, break + reason; `actualHours = 5.5` |
| 4.4a | M | change only the end to 23:30, retaining start 17:00 and break 30 | `actualHours = 6.0` after the trigger, no manual calculation run |
| 4.4b | M | change only the break to 60, retaining start 17:00 and end 23:30 | `actualHours = 5.5` after the trigger; reason required |
| 4.5 | M | month A: enter the actual times of all 22 valid shifts by correction (table 1.4) | `actualHours` per shift as planned, Pat's three longer shifts 7.0, 7.0, 7.25 |
| 4.6 | M | `sp_payroll_prep?monat=2026-10` | values of section 3 |
| 4.7 | M | CSV export of month A | header `person;month;contractType;hourlyRate;shiftsInMonth;plannedHours;actualHours;miniJobWarning`; conventions per country module |
| 4.8 | M | `sp_payroll_prep` without parameter | current month (month B so far) |

## 3. Expected numbers (month A, 2026-10)

| person | shiftsInMonth | plannedHours | actualHours | actual × rate | miniJobWarning |
|---|---|---|---|---|---|
| TEST-A-Kim Dish | 2 | 8.00 | 8.00 | 111.20 | – |
| TEST-A-Lee Service | 6 | 39.00 | 39.00 | 643.50 | – (fullTime; `bedingung`, N13) |
| TEST-A-Pat Server | 7 | 45.50 | 47.25 | 656.78 | **YES, 656.78 EUR** (country-module limit for the test month) |
| TEST-A-Sam Bar | 3 | 16.50 | 16.50 | 247.50 | – |
| TEST-A-Test Cook | 4 | 24.00 | 24.00 | 384.00 | – |

- Cancelled shift (Pat, 2026-10-24) is not counted.
- 47.25 × 13.90 = 656.775 → shown as 656.78 (confirm: rounding of the warning amount).
- Persons without a staff record do not appear (`nur`).

## 4. Notification expectations

Only the listed persons receive the message; **nobody else** (check S1–S3 and the
manager after each step).

| After step | Rule | Recipient(s) | Not |
|---|---|---|---|
| 1.8 publish (1.4 historical markers already sent) | `sp_msg_first_publication` | each person on the published shift, once per shift | unstaffed open shifts; no repeat on the next tick |
| 1.5 cancel (historical marker sent) | `sp_msg_shift_cancelled` | P2 | others |
| 2.2 takeover | `sp_msg_swap_approved` → P2; `sp_msg_swap_partner_approved` → P3; `sp_msg_assignment_removed` → P2. **No** `sp_msg_shift_swapped` (the status does not change) | P2, P3 | P1, P4, P5 |
| 2.4 reject | `sp_msg_shift_request_rejected` | P3 | P2, P1 |
| 2.6 / 2.8 approve | `sp_msg_absence_approved` | P1 (twice, one per absence); 2.8 also `sp_msg_assignment_removed` → P1 | others |
| 4.2–4.5 clocking | none | – | everybody |

Persons without account (P4, P5) have no inbox; their messages are not checked.

## 5. Negative tests

| # | Role | Step | Expected |
|---|---|---|---|
| N1 | M | `ontouser_team_show` S1–S3 | master **read only**, **no** planning membership, team read+write |
| N2 | S2 | open a colleague's shift (detail URL of P3's shift) | refused / not found |
| N3 | S2 | Clock in on P3's shift (button or direct action run) | refused: "Only your own shift" |
| N4 | S2 | open `sp_week_list`, `sp_request_inbox`, `sp_payroll_prep`, `sp_actual_times`, `sp_rule_check`, `sp_shift_lead_today`, `sp_recycle_bin` by URL | refused |
| N5 | S2 | read colleague P3 on master | only name, login e-mail, stations (birth year only if shown for youth protection); **no** contract type, hourly rate, health or private contact fields |
| N6 | S2 | open a staff record in planning | refused |
| N7 | S3 | Clock in a second time on the same shift | refused (condition message) |
| N8 | S3 | Clock out without clock-in (other shift) | refused |
| N9 | S1 | `sp_actual_correct`, `sp_shift_publish`, `sp_absence_approve` | button absent; direct run refused (gate) |
| N10 | M | `sp_week_request` a second time on the week-B period; `sp_period_create` again for 2026-11-16…22 | week request refused (P1-11); the period is **not** refused (the `external_id` carries a random part); the agent must list the periods first and not create it (phase 1 §4.3) — record the result |
| N11 | S2 | swap with a partner not qualified for service | partner not offered / refused |
| N12 | M | `onto_startcard_save` in the team scope with a planning view | refused |
| N13 | M | payroll month A, row P5 (fullTime, 643.50 EUR) | no warning (contract condition); a warning here means `bedingung` is missing |
| N14 | S1 | staff account at 0 credits, press Clock in | HTTP 402; dialog may hang; nothing written |
| N15 | M | absence approve on a person with a shift without confirming | nothing released |
| N16 | S1 / S3 | open shifts: compare kitchen-only and service-qualified accounts | qualification changes rows, not planning rights; staffed rows absent |
| N17 | M | read trash and ordinary active list for a deleted TEST probe | probe only in `status: deleted`; restored probe only in active list |
| N18 | M | staff one open shift of today, then reload `sp_shift_lead_today` | "Open shifts today" drops by one: the counter counts shifts **without a person** of the day, not the status `open`; a shift with status `open` but a person does not count |

The behaviour of the block views in these steps is confirmed in the browser for the
authors' tested build (manager and staff account), except "My absences". In your own run a
saved definition is still not proof: check rendered rows, matching, rule flags and
counter totals in the browser and record pass/fail separately per view.

## 6. Clean-up

- Default: **keep** all `TEST-A-` objects in the three test scopes and record them in
  the run log — deleting costs 20 credits per object and link.
- If the account must be emptied: delete one id at a time along the delete path of
  phase 1 (recycle bin, then `sp_delete_for_good`), budget it in advance, and never
  delete outside the `TEST-A-` prefix.
- Offboard test staff accounts with `ontouser_team_offboard_preview` then
  `ontouser_team_offboard` (`mode` per decision); left-over credit returns to the
  manager.
- Never move test data into a real customer's scopes.

## 7. Additional checks from the phase chapters

These belong to a full acceptance run. Each line: what you do, what must happen.

**Phase 2 — requests**
1. A staff account submits a request through each of the three request actions; a
   second staff account tries to decide it. The guard refuses the second one and the
   request keeps its status.
2. `sp_absence_request` saves the own person and refuses a colleague (P2-5, P2-5b).
3. Decide a takeover and a handover with `sp_swap_decide`: no second link error, the
   requester gets exactly one message, the shift status stays unchanged.
4. Publish a week, then run the precheck again with `against_status` set to
   `published` — it reports the published state instead of offering a second publish.

**Phase 3 — staff view**
5. A staff account opens "My absences" and requests an open shift that is not yet
   linked to it (P3-13) — with staff rights only, no planning membership.
6. The first publication produces one plan summary message, not one per shift.
7. A handover notifies the person picked; adding a person to an already published
   shift notifies that person although the status does not change.

**Phase 4 — corrections and payroll**
8. The warning column flags one minijob row and one non-minijob row above the limit
   and leaves the rows below it alone (P4-13).
9. A denied export shows a notice instead of a blank page (P4-15).
10. A staff member opens their own staff record through the person link; a colleague's
    record is refused. Deleting a comment works for its author and for a scope writer
    (P4-16).
