# Views from building blocks

A view is described, not written: you say which objects, which columns, which
condition — the server builds the query. Two rules follow from that:

- Views are built **only from the blocks below**; free-form queries are not available to
  customer accounts.
- Every block carries the scope filter, so a view can only ever show what its reader may
  see.

Minimal shape:

```json
{
  "elements": ["filter", "table"],
  "table": {
    "from": "objects",
    "type": "shift",
    "columns": [
      {"key": "tag",  "prop": "shiftStart", "format": "wochentag_datum", "label": "Day"},
      {"key": "zeit", "prop": "shiftStart", "bis": "shiftEnd", "format": "zeitspanne", "label": "Time"}
    ],
    "sort": {"key": "tag", "dir": "asc"}
  }
}
```

`type` is the object type name, `prop` a field key, `format` the display format
(`text`, `datum`, `zeit`, `wochentag_datum`, `wochentag_datum_zeit`, `zeitspanne`,
`kalenderwoche`, `jahr`, `zahl`, `waehrung`, `monat`, `warnung`).

## A warning column — amount over a threshold

`warnung` computes one row instead of reading a field: hours times hourly rate. It needs
two columns that are already in the list.

```json
{"key": "minijob", "format": "warnung", "wert": "ist", "stundenlohn": "lohn",
 "schwelle": 603, "schwelle_ab_2027": 633, "text": "over the limit: {betrag} EUR"}
```

| Key | Meaning |
|---|---|
| `wert` | column key holding the hours |
| `stundenlohn` | column key holding the hourly rate |
| `schwelle` | limit, default 603 |
| `schwelle_ab_2027` | limit from 2027 on (the year comes from the server, no upkeep) |
| `text` | cell text, placeholders `{betrag}`, `{stunden}`, `{grenze}` |

The cell stays empty when one of the two values is missing — no invented number.

### Only for some rows

Without a second condition the warning fires for every row that crosses the limit, so a
part-time contract would be flagged like a marginal one. Add `bedingung` — a list of
conditions on **column keys**, joined with AND:

```json
{"key": "minijob", "format": "warnung", "wert": "ist", "stundenlohn": "lohn",
 "bedingung": [{"spalte": "vertrag", "op": "=", "wert": "minijob"}],
 "schwelle": 603, "text": "over the limit: {betrag} EUR"}
```

`op` is one of `=`, `!=`, `>`, `<`, `>=`, `<=`; numbers are compared as numbers, the rest
as text. A named column must appear **before** the warning column — otherwise the
definition is refused. If a named column is missing from a row, the condition does not
hold and the cell stays empty. Without `bedingung` the column behaves as before.

## Whose rows? — the person binding

A view that lives in one scope but shows data from another (a team door) must bind the
rows to the signed-in person. One block does that:

```json
"person": {"link": "worksShift", "richtung": "rueckwaerts", "prop": "email", "type": "person"}
```

The server builds the comparison against the e-mail of the signed-in person — you do not
write `{current_user_email}` yourself. Without a person binding, a view with
`data_scope_id` is refused.

## Time window, filters, sorting

```json
"zeitraum": {"key": "tag", "von": "{period_start}", "bis": "{period_end}"},
"param": "woche",
"span": 7,
"filter": ["station", "status"],
"sort": {"key": "tag", "dir": "asc"}
```

`param`/`span` create the period switch in the header (`?woche=YYYY-MM-DD`); the
`zeitraum` uses the resulting placeholders. `filter` lists column keys — the value comes
from the filter bar, never from the definition.

Without a date in the URL the window starts at the beginning of the week. A daily view
wants another start:

```json
"param": "tag", "span": 1, "basis": "heute"
```

`basis`: `woche` (default, Monday of the current week), `heute` (today), `monat` (first
of the month).

## Empty and filled fields

A condition can ask whether a field has no value at all — no value needed:

```json
"ohne_link": {"link": "worksShift", "richtung": "rueckwaerts"},
"wo": [{"prop": "shiftStatus", "op": "leer"}]
```

`op`: `leer` (no value) and `nicht_leer` (has a value) work in `wo` and in counters;
all other operators take a `wert`.

## Status — active, deleted, both

By default a list shows living objects only. A recycle-bin view asks for the others:

```json
"table": {"from": "objects", "type": "shift", "status": "deleted", "columns": [...]}
```

`status`: `active` (default), `deleted`, `any`.

## Not yet taken

Rows that carry **no** link of a given type — open shifts nobody is assigned to:

```json
"ohne_link": {"link": "worksShift", "richtung": "rueckwaerts"}
```

Add `"linkvalue"` when only one meaning of the link must be missing. The same key works
inside a counter — that is how "open shifts nobody is assigned to" is counted:

```json
{"type": "shift", "label": "open", "ohne_link": {"link": "worksShift", "richtung": "rueckwaerts"}}
```

## Fits me — matching my own links

The row hangs on the same target as the signed-in person, just through another meaning
of the same link:

```json
"passt": {"link": "concerns", "mein_value": "einsetzbar fuer",
          "objekt_value": "Station", "type": "space"}
```

Read as: *person —concerns/"einsetzbar fuer"→ station* and *shift —concerns/"Station"→
station*, and both point at the same object. That is how "open shifts I am qualified
for" is expressed without a second query.

## Rule columns — one check per row

Each rule becomes a column that shows its text when the condition holds, and stays empty
otherwise:

```json
"regeln": [
  {"key": "long",  "feld": "plannedHours", "op": ">", "wert": 10, "text": "over 10 h"},
  {"key": "break", "feld": "breakMinutes", "op": "<", "wert": 30, "text": "break too short"}
]
```

`op` is one of `=`, `!=`, `>`, `<`, `>=`, `<=`; `wert` must be a number.

One rule needs no field: the statutory break depends on the shift length.

```json
{"key": "pause", "art": "pause", "text": "break too short"}
```

It reports shifts over 6 h with less than 30 min break and shifts over 9 h with less
than 45 min — the length comes from `shiftStart` and `shiftEnd`, the break from
`breakMinutes`.

## Rule columns across rows — per person

These look at the other shifts of the same person:

```json
"personenregeln": [
  {"key": "u18",  "art": "u18", "datum": "shiftStart", "zeit_ab": "22:00", "text": "minor after 22:00"},
  {"key": "day",  "art": "tagessumme", "wert": 10, "datum": "shiftStart", "text": "over 10 h that day"},
  {"key": "rest", "art": "ruhezeit",   "wert": 11, "datum": "shiftStart", "text": "less than 11 h rest"}
]
```

- `u18` — the person on the shift is younger than 18 (optionally only when the shift
  **ends** after `zeit_ab`; `zeit_feld` changes which time is compared, default
  `shiftEnd`).
- `tagessumme` — the person's planned hours on that day exceed `wert`.
- `ruhezeit` — the gap to the person's previous shift is below `wert` hours.

The person is resolved through the shift's `worksShift` link.

### Only the rows that trip a rule

By default every row keeps its rule columns, most of them empty. To see only the
offenders:

```json
"nur_treffer": true
```

## Counters

```json
"counters": {
  "from": "objects",
  "zaehler": [
    {"type": "shift", "label": "all"},
    {"type": "shift", "label": "open", "filter": [{"feld": "shiftStatus", "op": "=", "wert": "offen"}]},
    {"type": "shift", "label": "started, no actual time", "filter": [{"feld": "actualStart", "op": "leer"}]}
  ]
}
```

Each counter needs `type`, `label` and — if it filters a value — a `wert`;
`leer`/`nicht_leer` need none. A filter without a value is refused. `"from": "objects"`
is required, otherwise the counter block is ignored.

A counter takes the same window as the table. Say so explicitly if it counts one day:

```json
{"type": "shift", "label": "open today", "filter": [
  {"feld": "shiftStatus", "op": "=",  "wert": "offen"},
  {"feld": "shiftStart",  "op": ">=", "wert": "{period_start}"},
  {"feld": "shiftStart",  "op": "<=", "wert": "{period_end_dt}"}
]}
```

`"scopes": [80]` narrows one counter to a scope — needed when the original counts a
single scope while the reader may see several.

The header is rendered from `items`; the counter block writes it for you. If a counter
never shows up, that list is missing.

## Pitfalls

- A column `key` is used once per view — including rule columns. A duplicate is refused.
- `prop` must be a field key of the object type; unknown names are refused, not ignored.
- Formats change the display only; sorting and filtering use the raw value.
- One list shows one object type. Two kinds of objects in one list means two lists.
