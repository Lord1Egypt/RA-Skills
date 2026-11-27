# Country module: Germany (DE)

Use for businesses in Germany. Other countries get their own file
(`country-at.md`, `country-nl.md`, …) with the same sections.

> **Verify yearly.** Every value below carries the date it was checked and a source.
> Before each build, open the sources again and update value + date. If a value has
> changed and this file is older, use the new value and report the difference.
> This is configuration guidance, **not legal advice**. The business decides with its
> tax adviser / payroll office.

## 1. Values used by the workspace

| Value | Amount | Valid from | Checked | Source |
|---|---|---|---|---|
| Statutory minimum wage | 13.90 EUR gross per hour | 2026-01-01 | 2026-11-06 | MiLoV5 § 1 — https://www.gesetze-im-internet.de/milov5/__1.html |
| Statutory minimum wage | 14.60 EUR gross per hour | 2027-01-01 | 2026-11-06 | MiLoV5 § 1 (same) |
| Minijob earnings limit | 603 EUR per month (7,236 EUR per year) | 2026-01-01 | 2026-11-06 | Minijob-Zentrale — https://www.minijob-zentrale.de/DE/die-minijobs |
| Minijob earnings limit | 633 EUR per month (7,596 EUR per year) | 2027-01-01 | 2026-11-06 | Haufe, "Minijob-Grenze 2026 und 2027" — https://www.haufe.de/personal/entgelt/minijob-grenze_78_479516.html; Bundesagentur für Arbeit — https://www.arbeitsagentur.de/vor-ort/stralsund/unternehmen/arbeitgebernews/der-mindestlohn-steigt |

How the minijob limit is derived (dynamic since 2022-10-01): minimum wage × 130 ÷ 3,
rounded up to full euros (Haufe, above). If the minimum wage changes, the limit changes.

**In the workspace (phase 4):** the minijob warning compares, per person with
`contractType = minijob` and month, `actual hours × hourlyRate` against the limit of
that month. The view restricts the warning to minijob rows with
`"bedingung": [{"spalte": "contractType", "op": "=", "wert": "minijob"}]` (phase 4
§6.3). Example: 47.25 actual hours × 13.90 EUR = 656.78 EUR > 603 EUR → warning. The
threshold is a **parameter of the view**; never hard-code it in warning text. Set
`schwelle: 603` (2026) and `schwelle_ab_2027: 633` (from 2027-01-01). **Caveat:** the
platform picks the year from the date the view is opened, not from the selected
month. A December 2026 payroll prepared in January 2027 is checked against 633; a
January 2027 month viewed in December 2026 against 603. For months near the limit,
check by hand against the limit of the month itself.

Notes for the warning text (no verdict): an unforeseeable, occasional excess in up to
two calendar months per year does not end a minijob (Haufe, above). The warning
therefore says "check with payroll", not "no longer a minijob".

## 2. Working time and breaks (Arbeitszeitgesetz, ArbZG)

Shown as warning columns in the rule-check view (phase 1 §6.4, confirmed in the
browser) — never as automatic blocking. How the view maps the rules below:

| Rule-check column | Checks | Rule below |
|---|---|---|
| Break too short | planned break against shift length: more than 6 h needs at least 30 min, more than 9 h at least 45 min | § 4 ArbZG (the split into 15-minute blocks is not checked) |
| Over 10 planned hours / Over 10 hours that day | one shift, or all shifts of a person on one day, longer than 10 h | § 3 ArbZG (the 6-month average is not checked) |
| Less than 11 hours rest | gap to the same person's previous shift | § 5 ArbZG (the hospitality shortening to 10 h and its compensation are a manual check) |
| Minor after 22:00 | person under 18 whose shift ends after 22:00 | § 14 JArbSchG, see below |

**Youth protection in detail (§ 14 JArbSchG).** Minors may generally work only
between 6:00 and 20:00. Minors **over 16** may work in restaurants and hospitality
until 22:00. The rule check knows only the birth year: it treats a person as a minor
by year (current year − birth year < 18), so it cannot tell a 15-year-old from a
17-year-old, and someone who turns 18 later this year already counts as adult. For
staff under 16, check every shift ending after 20:00 by hand, or add a second rule
column with `zeit_ab: "20:00"` and the text "Minor after 20:00 — check age" (it then
also marks the 16- and 17-year-olds; the manager decides).

| Rule | Content | Source |
|---|---|---|
| Daily working time | 8 h per working day; up to 10 h if the average over 6 months / 24 weeks stays at 8 h | § 3 ArbZG — https://www.gesetze-im-internet.de/arbzg/__3.html |
| Breaks | > 6 h to 9 h: at least 30 min; > 9 h: at least 45 min; split into blocks of at least 15 min | § 4 ArbZG — https://www.gesetze-im-internet.de/arbzg/__4.html |
| Rest period | at least 11 h uninterrupted after the end of daily working time; in restaurants and hospitality it may be shortened by up to 1 h if each shortening is compensated within a calendar month or four weeks by extending another rest period to at least 12 h | § 5 ArbZG — https://www.gesetze-im-internet.de/arbzg/__5.html |
| Youth protection | under 18: generally only 6:00–20:00; over 16 in restaurants and hospitality until 22:00 | § 14 (1) and (2) no. 1 JArbSchG — https://www.gesetze-im-internet.de/jarbschg/__14.html |
| Recording working time | employers must record working time | Federal Labour Court (BAG), decision of 2022-09-13, 1 ABR 22/21 |
| Recording for minijobs and hospitality | for minijobbers and in the sectors of § 2a SchwarzArbG (which include restaurants and hospitality): start, end and duration of daily working time recorded by the end of the 7th day after the work, kept for at least 2 years | § 17 (1) MiLoG — https://www.gesetze-im-internet.de/milog/__17.html |

Checked: 2026-11-06. *Confirm* in the next yearly review: whether a new
working-time recording law has come into force.

How the workspace supports this:
- Clock in/out stores `actualStart`, `actualEnd`, `actualBreakMinutes` with a comment per write.
- Corrections only by the manager, with a required reason; the comment keeps old → new.
- Comments can be deleted by their author or by a writer of the planning scope.
  Retaining them is an operating rule, not a guarantee of an immutable working-time
  record; keep additional payroll evidence.
- Clock-in has no verified time window; managers review early clock-ins and
  deviations from the plan. A `{now}` condition is not a verified remedy.
- Birth year (`birthYear`) only if youth-protection checks are needed (intake 10).

## 3. Data protection (GDPR / DSGVO)

| Topic | Rule for the build | Source |
|---|---|---|
| Sick leave | Health data is a special category. Store **only the kind** `absenceKind = sick` and the period. **No diagnosis, no doctor's note content** in `absenceNote` or comments. The field label says "(no diagnosis)". | Art. 9 GDPR — https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| Data minimisation | On staff-readable master persons: only basic fields (name, login e-mail, stations; birth year only for youth protection). Contract type, hourly rate and private address/phone are protected (planning / managers). No diagnosis in absence notes. | Art. 5 (1)(c) GDPR |
| Who sees what | Staff: master **read** (basic person/station data for team views), **no** planning membership, team read+write. A planning object opens for a staff member only through the person link: their own shifts (`worksShift`) and their own absences and requests (`concerns`); colleagues' objects stay closed. Pay (`hourlyRate`), health notes and private contacts must **not** sit on staff-readable master persons — keep them on the staff record in planning (managers; phase 4 §1.2 on shift leads and the own record). | Art. 5 (1)(f) GDPR, Art. 32 GDPR |
| Data processing agreement | The business is the controller; Telesherpa processes on its behalf. A data processing agreement (Auftragsverarbeitungsvertrag) must be in place before real staff data is entered. Ask the business to confirm. | Art. 28 GDPR |
| Works council | If a works council exists, introducing a system that records working time and can monitor behaviour/performance is subject to co-determination; so are start and end of daily working time. The business must involve the works council **before** go-live. | § 87 (1) no. 2 and no. 6 BetrVG — https://www.gesetze-im-internet.de/betrvg/__87.html |
| Retention | Working-time records at least 2 years (MiLoG § 17). Payroll-relevant records (hours paid, hourly rate, contract type, the payroll CSV) fall under longer retention duties of tax and social-security law (e.g. wage account § 41 EStG, § 147 AO, § 28f SGB IV); the tax adviser sets the period. Delete or anonymise only after the longest applicable period. Deleting in the workspace: one id at a time. | § 17 MiLoG; § 41 EStG, § 147 AO, § 28f SGB IV |
| Test data | Never real staff data in tests; use `example.com` addresses and the prefix `TEST-`. | — |

Checked: 2026-11-06.

## 4. Payroll export (Germany)

- Generic eight-field CSV as defined in phase 4 (`sp_payroll_prep`):
  `person;month;contractType;hourlyRate;shiftsInMonth;plannedHours;actualHours;miniJobWarning`.
  The rate must precede the warning; labels are the export headers. A linked rate
  is required when the warning is included.
- Threshold parameters of the warning column for Germany: `schwelle` 603 EUR/month
  (2026), `schwelle_ab_2027` 633 EUR/month (from 2027-01-01); the year follows the
  current date (section 1).
- German conventions for the payroll office: separator `;`, decimal comma, UTF-8 with BOM, CRLF line ends.
- The warning applies only to `contractType=minijob` through `bedingung`; without it,
  ignore warnings on other contracts.
- **DATEV**: outlook only, not part of this skill.

## 5. Labels

German staff usually expect German **labels** (intake 19). Option **values** follow the
scope-own English sets from phase 0; keep the token `minijob` on `contractType` if the
minijob warning in this module must match that value. Only labels change for display:
set them as the `label` of each option in the override (phase 0) and in the `werte`
maps of the views.

| Field | Value → German label |
|---|---|
| `shiftStatus` | `open` Offen · `planned` Geplant · `published` Veröffentlicht · `swapped` Getauscht · `cancelled` Abgesagt |
| `shiftKind` | `early` Frühschicht · `late` Spätschicht · `split` Teildienst · `night` Nachtschicht |
| `station` | `kitchen` Küche · `service` Service · `bar` Bar · `dishwashing` Spülküche · `shiftLead` Schichtleitung |
| `onCall` | `yes` Ja · `no` Nein |
| `absenceKind` | `vacation` Urlaub · `sick` Krank · `dayOffWish` Wunschfrei · `training` Schulung · `availability` Verfügbarkeit |
| `absenceStatus` | `requested` Beantragt · `approved` Genehmigt · `rejected` Abgelehnt |
| `halfDay` | `no` Nein · `firstHalf` Erste Hälfte · `secondHalf` Zweite Hälfte |
| `demandStatus` | `open` Offen · `planned` Geplant · `covered` Gedeckt · `dropped` Entfallen |
| `requestKind` | `swap` Tausch · `takeover` Übernahme · `handover` Abgabe · `shiftRequest` Schichtwunsch |
| `changeStatus` | `proposed` Beantragt · `accepted` Angenommen · `rejected` Abgelehnt |
| `clockStatus` | `clockedIn` Eingestempelt · `clockedOut` Ausgestempelt · `corrected` Korrigiert |
| `firstNoticeStatus` | `open` Offen · `sent` Erstmitteilung gesendet |
| `contractType` | `minijob` Minijob · `partTime` Teilzeit · `fullTime` Vollzeit · `fixedTerm` Befristet · `casual` Aushilfe |

The platform's own default sets for these fields in other scopes may use German
values; that is why phase 0 overrides them in planning and master.

## TODO

- [ ] Decide the exact warning text (phase 4) with the payroll office of the first customer.
- [ ] Add public holidays per federal state if surcharges are needed (out of scope now).

## 6. Additional German display terms

| English term | Key | Example display (DE) | Note |
|---|---|---|---|
| master data scope | `<company>_master` | Stammdaten | managers write; staff read (basic only; see E2) |
| planning scope | `<company>_planning` | Planung | managers only; staff: no membership |
| team scope (door) | `<company>_team` | Team | staff read/write |
| business | `organisation` | Betrieb | |
| site | `building` | Restaurant / Standort | |
| station | `space` (object), `station` (option on shift/template) | Station (Kitchen, Service, …) | create scope-specific English option values (phase 0); platform defaults stay German |
| staff member | `person` | Mitarbeiter:in | `email` binds the login |
| contract type | `contractType` | Vertragsart | `minijob`, `partTime`, `fullTime`, `fixedTerm`, `casual` — on the staff record (phase 4) |
| hourly rate | `hourlyRate` | Stundenlohn (EUR) | protected — on the staff record in planning, not on the staff-readable master person |
| shift template | `shiftTemplate` | Schichtvorlage | |
| shift | `shift` | Schicht | |
| shift status | `shiftStatus` | Schichtstatus | scope-own English values `open`, `planned`, `published`, `swapped`, `cancelled` |
| shift kind | `shiftKind` | Schichtart | `early`, `late`, `split`, `night` |
| planned hours | `plannedHours` | Soll-Stunden / Geplante Stunden | computed |
| break (planned) | `breakMinutes` | Pause (Minuten) | |
| plan period | `serviceOrder` with `task = planPeriod` | Dienstplan-Periode | |
| manager note | `serviceOrder` with `task = planNote`, linked `concerns` / `followUpOf` | Hinweis | |
| staffing (assignment) | link `worksShift` person → shift | eingeteilt / besetzt | |
| qualified for | link `concerns`, linkvalue `qualifiedFor` | einsetzbar für | |
| absence | `absence` | Abwesenheit | `absenceKind`: `vacation`, `sick`, `dayOffWish`, `training`, `availability` |
| day-off wish | `absenceKind = dayOffWish` | Wunschfrei | an absence, not a request kind |
| change request | `changeRequest` | Antrag | |
| request kind | `requestKind` | Art | `swap` (Tausch), `takeover` (Übernahme), `handover` (Abgabe), `shiftRequest` (Anfrage offene Schicht) |
| demand | `demand` | Bedarf | optional |
| clock in / out | actions on shift, bridge + guard | Einstempeln / Ausstempeln | |
| actual start / end | `actualStart`, `actualEnd` | Ist-Beginn / Ist-Ende | |
| actual break | `actualBreakMinutes` | Ist-Pause (Minuten) | |
| actual hours | `actualHours` | Ist-Stunden | computed |
| clock status | `clockStatus` | Stempelstatus | `clockedIn`, `clockedOut`, `corrected` |
| actual time changed by / at | `actualChangedBy`, `actualChangedAt` | Ist-Zeit geändert von / am | |
| correction note | `comment` effect on the action | Vermerk | who, when, old → new, reason |
| change log | comments + `actualChangedBy`/`At` + object history | Änderungsprotokoll | operating rule: no editing/deletion; comments are technically deletable |
| staff record | manager-only record in planning, linked `concerns` / `staffRecordOf` → person | Personalakte (geschützt) | contract type, hourly rate, private contact (phase 4) |
| first-publication marker | `firstNoticeStatus` | Erstmitteilung | `open`, `sent` |
| payroll-prep view / export | `sp_payroll_prep` in planning + CSV | Lohnvorbereitung | eight-field CSV in phase 4 order; rate before warning |
| minijob warning | computed column `miniJobWarning` | Minijob-Warnung | threshold from the country module (DE: [country-de.md](country-de.md)) |
| link removed (event) | `link_removed` | — | notification when an assignment disappears |
| start card | start card (scope + view), e.g. "My shifts" → `sp_my_shifts` | Startkarte | team front page; no roles |
| favourite | personal favourite | Favorit | per user |
| blocks view | `elements: ["blocks"]` | — | several tables/cards on one page |
| view gate | `view_config.access.require` | — | `"write"`, `"manage"`, scope id |
| managed account | account managed by one of your scopes | — | staff accounts |
