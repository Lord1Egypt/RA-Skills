# Object model — art and exhibition transport

## 1. Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, sites, people (basic fields), packed items and crates | managers write |
| `<company>_transport` | transport work | `serviceOrder` rows (jobs and protocols), property definitions, manager views, functions and triggers, `result_scope_id` of the actions | managers |
| `<company>_team` | team door | start cards, team counterparts of the lists, both forms | managers (daily UI) |

Rules:

- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_transport`).
- The scope is the lock. Never rely on a view filter to hide data.
- **Reuse.** If shift-planning already created `_master` and `_team` for this
  business, add only `_transport` and keep the existing people and sites.
- **Links cross scopes.** `concerns` / `ofAsset` runs from a `serviceOrder` in
  transport to an item in master.
- Placeholders such as `<transport_scope_id>` stay in the run log, not in public text.

## 2. Types to activate

On `_master`: `organisation`, `building`, `person`, `device`.
On `_transport`: `serviceOrder`.
On `_team`: no extra master types; views, start cards and the forms live here.

Read each type with `onto_type_show` before you activate it. A member does not
create types. If a required type is missing, stop and file
`ontouser_service_request`. Activate with `ontouser_scope_types_set` (that call
**replaces** the list; include every type the scope must keep).

`device` is the catalogue asset type used for packed items and for crates. A
property `itemKind` distinguishes them. Confirm the type is present; if the
business needs a dedicated catalogue type, file a service request and wait.

## 3. Properties on `device` (master)

Create these in the master scope only for fields the intake actually uses.

| Key | Value type | Purpose |
|---|---|---|
| `itemKind` | options | `artwork` \| `crate` |
| `title` | string | object title |
| `artist` | string | artist or maker, when used |
| `medium` | string | medium or materials, when used |
| `dimensions` | string | dimensions as the business already writes them |
| `declaredValue` | string | declared or insured value as a stored figure, not a legal review |
| `crateCode` | string | crate or packing-unit code |

Platform name and description fields already on the type may be used; do not
redefine them.

## 4. Properties on `serviceOrder` (transport scope)

| Key | Value type | Purpose |
|---|---|---|
| `dueDate` | date | delivery date (source of truth for the lists) |
| `lastDone` | date | date of the last recorded collection or delivery |
| `tourCode` | string | shared code for jobs that travel together |
| `crateCode` | string | crate used on this job |
| `clientName` | string | client or lender name as given at intake |
| `collectionPlace` | string | collection address or site name |
| `deliveryPlace` | string | delivery address or site name |
| `orderKind` | options | `transportJob` \| `collectionReport` \| `deliveryReport` |
| `result` | options | `pass` \| `defect` |
| `inspectionNote` | string | condition or handover note written back to the job |

Platform fields already on `serviceOrder` that this skill uses, not redefined:
`orderStatus` (`open` / `inProgress` / `done`), `description`, `task`,
`assignedTo`, `priority`, `startedAt`, `completedAt`.

A member of staff is assigned with `assignedTo`. Collection and delivery
addresses are stored as text on the job so this skill does not invent a second
link to `building`. Site rows in master remain the address book the business
already keeps.

## 5. Link types

Confirm in `onto_link_index` before you depend on them. Invent none.

| Link | Direction | Linkvalue | Use |
|---|---|---|---|
| `concerns` | transport job → item (`device`) | `ofAsset` (set on the edge) | job to the packed item |
| `concerns` | protocol → job (both `serviceOrder`) | `ofOrder` (set on the edge) | collection or delivery report to its job |
| `bestehtAus` | organisation → building | — | site tree, same as shift-planning |

One open `transportJob` per item per move. Jobs that travel together share
`tourCode`. A crate is either a `device` with `itemKind=crate` or a `crateCode`
on the item and on the job — use the form the intake chose. Do not invent a
linkvalue such as a tour or crate edge.

If `concerns` does not allow a pair you need, stop and file a service request.
