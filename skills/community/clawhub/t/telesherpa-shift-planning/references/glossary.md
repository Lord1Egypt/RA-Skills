# Glossary

One term, one meaning, in every file. Column "Key" is the identifier you type
(verbatim). Country-specific display labels are kept in the country module; the label
language of a real customer comes from intake 19.

## Key concepts

### Door / team door
The **team scope** is the staff's door into the workspace. Staff hold **read + write**
there, **read (no write)** on master, and **no membership** on the planning scope. The
view "My shifts" takes **shifts** as its base set and binds them to the signed-in
master person with `person: {link: worksShift, richtung: rueckwaerts, prop: email,
type: person}`. No e-mail placeholder is needed in that block. Request/absence views
bind via `concerns`; open shifts use `passt` to match qualifications. The views list
what the person link reaches; they do not filter a readable planning scope. Every
view a staff member opens and every button they press lives in the team scope; the
button writes back through a scope bridge.

### Person link (own objects)
The only way a staff member reaches a planning object: the object hangs on their
master person — a shift through `worksShift` (person → shift), an absence or a
request through `concerns`. Then its detail page opens and actions on it can run,
although the staff member has no right on planning. Every other planning object
(a colleague's shift, absence or request) stays closed and answers as if it did not
exist. The link opens the **whole object**, not a redacted copy (fields and
comments) — so nothing that the person must not read belongs on it. A request is
open to **everyone it is linked to**: the requester and the named partner
(`takingOver`). Exception: open shifts matching the person's qualifications are
listed through `passt` and can be requested without a person link (detail page and
comments for staff — confirm).

### Signed-in person
The master `person` whose `email` equals the login e-mail of the calling account
(compared in lower case; keep both identical). Guards, the `person` block,
`{user_person}` and `passt` all resolve the caller this way. A login without such a
person reaches nothing.

### Scope bridge
An action that runs from the team door but stores its result in the planning scope:
`"action": {"result_scope_id": <planning_scope_id>, "props": {...}}`. It opens for one
call, one target object and exactly the listed property keys, then closes. It is not a
right. Example: "Clock in" sets `actualStart` and `clockStatus` on the staff member's
own shift in planning, although the staff member has **no membership** on planning
(neither read nor write). The row is reachable through the person link.
Reference: [scope-bridges.md](../../../telesherpa-ontology-platform/references/features/scope-bridges.md). Recipes: [phase2.md](phase2.md), [phase4.md](phase4.md).

### Management gate
`"require_scope_write": <planning_scope_id>` on an action. Only accounts with write on
planning see and run the button. Every manager action carries it (publish, staff a
shift, approve, correct actual time, restore, delete for good). Example: "Correct actual
time (manager)" is invisible for staff. For views the counterpart is
`view_config.access.require`.

### Guard
A read-only pre-check on an action, evaluated before anything is written:
`"guards": [{"type": "linked_to_user", "linktype": "worksShift", "message": "Only your own shift"}]`.
It passes only if the signed-in person (see above) is linked to the target object via
`worksShift`. Example: a staff member who manipulates the URL to clock in on a
colleague's shift gets the guard message and nothing is written. The action's
`condition` is evaluated before the guard.

Forms take the same shape in their definition: `"guards": [{"type": "linked_to_user",
"linktype": "concerns"}]` refuses saving an answer whose person concerned is not the
signed-in person (phase 2 §3.1).

Which staff actions carry it:

| Staff action | Guard | Why |
|---|---|---|
| Clock in / Clock out (phase 4) | yes, `worksShift` | writes onto the shift itself |
| Request swap / takeover / handover (phase 2) | yes, `worksShift` | only the person on the shift may give it away |
| Request shift (phase 2) | no | the open shift has no person yet; the action only creates a request, binds the requester to the signed-in person, and a manager decides |
| Request absence (phase 2, form) | yes, on the form: `concerns` | only the person concerned may submit; the manager still sees requester and person concerned |

### First publication
The moment a shift is published for the first time (shifts are published one by one;
there is no bulk publish). This is the **only** event that messages everybody
concerned: every person staffed on the shift. Marker: `firstNoticeStatus = sent` on the
shift, so it never fires twice ([phase3.md](phase3.md) §6). Every later change
(cancelled, re-staffed, swapped, request decided, assignment removed) notifies only the
people affected.

### Affected people
The persons linked to the changed object (via `worksShift`, or as requester/partner of a
change request, or the person of an absence) — and the manager where the rule says so.
Nobody else.

### E2 / basic vs protected
**Basic data for all, protected data for managers only.** Staff can read master, so
shared master `person` objects may hold only basic fields (name, login e-mail,
stations). Pay, health-related notes and private contacts belong on the manager-only
**staff record** in the planning scope ([phase4.md](phase4.md) §1.2). Hiding a column in a view is not enough if the field
sits on a staff-readable object. The staff record hangs on its person, so assume that
person can open it (own data only; colleagues' records stay closed).

## Terms

German display labels belong in [country-de.md](country-de.md) §6.

| English term | Key | Note |
|---|---|---|
| master data scope | `<company>_master` | managers write; staff read (basic only; see E2) |
| planning scope | `<company>_planning` | managers only; staff: no membership |
| team scope (door) | `<company>_team` | staff read/write |
| business | `organisation` |  |
| site | `building` |  |
| station | `space` (object), `station` (option on shift/template) | create scope-specific English option values (phase 0); platform defaults stay German |
| staff member | `person` | `email` binds the login |
| contract type | `contractType` | `minijob`, `partTime`, `fullTime`, `fixedTerm`, `casual` — on the staff record (phase 4) |
| hourly rate | `hourlyRate` | protected — on the staff record in planning, not on the staff-readable master person |
| shift template | `shiftTemplate` |  |
| shift | `shift` |  |
| shift status | `shiftStatus` | scope-own English values `open`, `planned`, `published`, `swapped`, `cancelled` |
| shift kind | `shiftKind` | `early`, `late`, `split`, `night` |
| planned hours | `plannedHours` | computed |
| break (planned) | `breakMinutes` |  |
| plan period | `serviceOrder` with `task = planPeriod` |  |
| manager note | `serviceOrder` with `task = planNote`, linked `concerns` / `followUpOf` |  |
| staffing (assignment) | link `worksShift` person → shift |  |
| qualified for | link `concerns`, linkvalue `qualifiedFor` |  |
| absence | `absence` | `absenceKind`: `vacation`, `sick`, `dayOffWish`, `training`, `availability` |
| day-off wish | `absenceKind = dayOffWish` | an absence, not a request kind |
| change request | `changeRequest` |  |
| request kind | `requestKind` | `swap`, `takeover`, `handover`, `shiftRequest` |
| demand | `demand` | optional |
| clock in / out | actions on shift, bridge + guard |  |
| actual start / end | `actualStart`, `actualEnd` |  |
| actual break | `actualBreakMinutes` |  |
| actual hours | `actualHours` | computed |
| clock status | `clockStatus` | `clockedIn`, `clockedOut`, `corrected` |
| actual time changed by / at | `actualChangedBy`, `actualChangedAt` |  |
| correction note | `comment` effect on the action | who, when, old → new, reason |
| change log | comments + `actualChangedBy`/`At` + object history | operating rule: do not edit/delete; comments are technically deletable |
| staff record | manager-only record in planning, linked `concerns` / `staffRecordOf` → person | contract type, hourly rate, private contact (phase 4) |
| first-publication marker | `firstNoticeStatus` | `open`, `sent` |
| payroll-prep view / export | `sp_payroll_prep` in planning + CSV | eight-field CSV in phase 4 order; wage column before warning |
| minijob warning | computed column `miniJobWarning` | threshold from the country module (DE: [country-de.md](country-de.md)) |
| link removed (event) | `link_removed` | notification when an assignment disappears |
| start card | start card (scope + view), e.g. "My shifts" → `sp_my_shifts` | team front page; no roles |
| favourite | personal favourite | per user |
| blocks view | `elements: ["blocks"]` | several tables/cards on one page |
| view gate | `view_config.access.require` | `"write"`, `"manage"`, scope id |
| managed account | account managed by one of your scopes | staff accounts |
## View blocks

[view-blocks.md](../../../telesherpa-ontology-platform/references/features/view-blocks.md)
is the platform reference. Use its keywords verbatim, with this skill's English
column keys and link values. `person` binds own/involved rows; `passt` compares
station targets with qualifications; `ohne_link` keeps only rows without a given link
(unstaffed shifts); `regeln`/`personenregeln` add review warnings and `nur_treffer`
keeps only rows with a warning; `counters` shows numbers above the table;
`status: deleted` builds trash; `basis` sets where the period starts (`woche`,
`heute`, `monat`). The seven views of phases 1 and 3 are confirmed in the browser.

| Block keyword | Meaning |
|---|---|
| `param`, `span`, `basis` | period switch in the header: URL parameter name, length in days, start (`woche` = Monday of this week, default; `heute` = today; `monat` = first of the month) |
| `zeitraum` | which column key the period applies to (`von` / `bis` with `{period_start}` / `{period_end}`) |
| `status` | `active` (default), `deleted`, `any` |
| `wo` | fixed row conditions (`prop`, `op`, `wert`); `op` `leer` / `nicht_leer` need no `wert` |
| `person` | bind rows to the signed-in person over a link |
| `ohne_link` | rows that have **no** link of this type |
| `passt` | rows whose link target equals a target of the signed-in person (another meaning of the same link) |
| `regeln` | one warning column per row condition (`feld`, `op`, `wert`, `text`); `art: pause` = break check by shift length |
| `personenregeln` | warnings across the person's shifts: `u18`, `tagessumme` (daily total), `ruhezeit` (rest time) |
| `nur_treffer` | `true` = show only rows with at least one warning |
| `counters` / `zaehler` | numbers above the table; each item `type`, `label`, optional `filter` (`feld`, `op`, `wert`), `ohne_link`, `scopes` |
| `agg` | aggregate over a link column: `sum`, `count` |
| `ziel` | conditions on the link target before aggregating (`wo` inside) |
| `stellen` | decimal places of a `zahl` column |
| `stundenlohn`, `schwelle`, `betrag` | `warnung` column: rate column, limit, and `{betrag}` = computed amount in the warning text |
| `schwelle_ab_2027` | `warnung` column: limit from 2027; the year comes from the current date, not the selected month |
| `bedingung` | `warnung` column: warn only if other columns match (`spalte` = column key, `op`, `wert`; several = AND) |
| `{monat_start}`, `{monat_ende}` | bounds of the month chosen with `?monat=YYYY-MM` (payroll view) |
| `subform`, `objekt`, `via` | detail-page panel: object type of the panel and the link (`link`, `richtung`, `linkvalue`) that reaches it |
| `dateien` | detail-page panel listing attached files |

## Action effects and checks

| Keyword | Meaning |
|---|---|
| `replace_link` | moves a link: `on` = object whose link changes, `linktype`, `side: object1` = replace the person side (from-end) with `to` |
| `precheck` | read-only check before the action runs, e.g. `person_time_overlap` (absence vs. shifts) |
| `comment` | effect that writes a comment on the object (change log) |
| `{current_user_email}` | in actions: login e-mail of the caller |
| `{'current_user_email'}` | in view `wo` conditions: the same value, quoted form (only phase 3 §7.1) |
| `{user_person}`, `{user_email}` | in actions: the signed-in person / its e-mail (person binding of a bridge action; `{user_email}` counts as binding) |
| `{object_name}` | in triggers and functions: name of the triggering object; **not** available in action names |
