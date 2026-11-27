# Object model — conservation and surveyor case file

## 1. Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, sites, people (basic fields), objects under study | managers write |
| `<company>_cases` | case work | `serviceOrder` rows (cases and survey protocols), property definitions, manager views, function and triggers, `result_scope_id` of the action | managers |
| `<company>_team` | team door | start cards, team counterparts of the lists, the survey form | managers (daily UI) |

Rules:

- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_cases`).
- The scope is the lock. Never rely on a view filter to hide data.
- **Reuse.** If shift-planning already created `_master` and `_team` for this
  business, add only `_cases` and keep the existing people and sites.
- **Links cross scopes.** `concerns` / `ofAsset` runs from a `serviceOrder` in
  cases to an object in master.
- Placeholders such as `<cases_scope_id>` stay in the run log, not in public text.

## 2. Types to activate

On `_master`: `organisation`, `building`, `person`, and `device` when the intake
uses movable objects.
On `_cases`: `serviceOrder`.
On `_team`: no extra master types; views, start cards and the form live here.

Read each type with `onto_type_show` before you activate it. A member does not
create types. If a required type is missing, stop and file
`ontouser_service_request`. Activate with `ontouser_scope_types_set` (that call
**replaces** the list; include every type the scope must keep).

`device` is the catalogue asset type used for movable works and objects.
`building` is used when the case concerns a site or structure. Confirm the types
the intake named; if the business needs a dedicated catalogue type, file a
service request and wait.

## 3. Properties on the object (master)

Create these in the master scope only for fields the intake actually uses,
on `device` and/or `building`.

| Key | Value type | Purpose |
|---|---|---|
| `title` | string | object or work title |
| `objectRef` | string | inventory, work or file number the studio already uses |
| `objectNote` | string | short identifying note (maker, date, material) as given |

Platform name and description fields already on the type may be used; do not
redefine them.

## 4. Properties on `serviceOrder` (cases scope)

| Key | Value type | Purpose |
|---|---|---|
| `dueDate` | date | next deadline or follow-up date (source of truth for the lists) |
| `intervalDays` | int | optional follow-up interval, when the business uses one |
| `lastDone` | date | date the last survey was recorded |
| `caseKind` | options | `conservation` / `survey` |
| `clientName` | string | client or commissioning party as given at intake |
| `orderKind` | options | `caseFile` / `surveyProtocol` |
| `result` | options | `pass` / `defect` |
| `inspectionNote` | string | findings written back to the case by `apply_survey` |

Platform fields already on `serviceOrder` that this skill uses, not redefined:
`orderStatus` (`open` / `inProgress` / `done`), `description`, `task`,
`assignedTo`, `priority`, `startedAt`, `completedAt`.

A member of staff is assigned with `assignedTo`. The client name is stored as
text on the case so this skill does not invent a second link to `organisation`
or `person`. Client rows in master remain the address book the business already
keeps.

One open `caseFile` per object per matter. Further surveys of the same matter
are protocols on that same open case. A new matter on the same object is a new
case.

When a case is finished, the manager sets `orderStatus=done` on that case in
the form the intake agreed. The record-survey function does not close the case.

## 5. Link types

Confirm in `onto_link_index` before you depend on them. Invent none.

| Link | Direction | Linkvalue | Use |
|---|---|---|---|
| `concerns` | case → object (`device` or `building`) | `ofAsset` (set on the edge) | case to the object under study |
| `concerns` | protocol → case (both `serviceOrder`) | `ofOrder` (set on the edge) | survey protocol to its case |
| `bestehtAus` | organisation → building | — | site tree, same as shift-planning |

`ofAsset` to `building` is part of the measured inspection path. If the intake
uses `device` and `concerns` does not allow that pair, stop and file a service
request. Do not invent a linkvalue.

Treatment notes and later visits are further `surveyProtocol` rows on the same
case (findings and photos on each protocol). They are not a second object type.
