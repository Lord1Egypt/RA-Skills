# Phase 0 — scopes, rights, object types, properties

**Goal:** three scopes with the right types activated, the rights of the manager
account written down and set, property definitions in the maintenance scope, and
a smoke test that proves the **definitions** are in place. No business data yet
(that is phase 1).

**Input:** answered [intake](intake.md) (questions 1, 5, 7, 15, 16) and the
checks from [prerequisites](prerequisites.md).

**Budget (pay-per-use):** the live volume price of every **new** scope, plus reads
and any definition writes the live table prices. If you reuse an existing
`_master` or `_team` from shift-planning, do not create them again and do not
bill them twice. Log what is booked.

Placeholders: `<company>` (slug from intake 15), `<master_scope_id>`,
`<maintenance_scope_id>`, `<team_scope_id>` (numbers returned by
`ontouser_scope_create` or by `ontouser_scope_index` when reusing). Never publish
those numbers.

---

## 1. Definitions

### 1.1 Scopes

| Scope name | Purpose | Holds | Who works here |
|---|---|---|---|
| `<company>_master` | master data | business, sites, people (**basic** fields), assets | managers write |
| `<company>_maintenance` | inspection work | `serviceOrder` rows (duties, protocols and defects), property definitions, manager views, function and triggers, `result_scope_id` of the actions | managers |
| `<company>_team` | team door | start cards, team counterparts of the lists, both forms and the report-defect asset view | managers (daily UI) |

Rules:
- Names: `a-z0-9_`, max 30 characters. Check the longest one (`<company>_maintenance`).
- The scope is the lock. Never rely on a view filter to hide data.
- **Reuse.** If shift-planning already created `_master` and `_team` for this
  business, add only `_maintenance`, keep the existing people and sites, and record
  that decision in the run log. A second master with a copy of the persons is a
  defect.
- Write all three names and returned ids into your run log (not into the public skill).
- **Links cross scopes.** `concerns` / `ofAsset` runs from a `serviceOrder` in
  maintenance to an asset in master.

### 1.2 Rights matrix

Read / Write / Manage per account. `–` = no grant at all.

This skill describes the **manager path** that was measured.

| Account | `<company>_master` | `<company>_maintenance` | `<company>_team` |
|---|---|---|---|
| Manager / owner (builds the workspace) | R W M | R W M | R W M |

Notes:
- Inspection, protocol and defect objects are stored in the maintenance scope.
  The team door holds views, start cards and the forms; writes go through the
  scope bridge (`result_scope_id` = maintenance).
- Do not grant extra rights "so a view works".

### 1.3 Types to activate

On `_master`: `organisation`, `building`, `person`, and the asset types the
intake actually uses — typically `car`, `device`, `tool`, `machine`.
On `_maintenance`: `serviceOrder`.
On `_team`: no extra master types required; views, start cards and the forms live
here.

Activation: `ontouser_scope_types_set` **replaces** the list. Include every type
the scope must keep. A preset may be applied only on an empty scope, and only
after `onto_catalog_index` has shown its content. Quote `ontouser_scope_types`
before and after.

### 1.4 Properties and option values

Create these property definitions with `onto_property_def_create`, `scope_id` =
`<maintenance_scope_id>`, type `serviceOrder`. Customer fields belong in the
customer scope. Read each definition back; the `scope_id` in the read-back must
be the maintenance scope.

| Key | Value type | Purpose |
|---|---|---|
| `dueDate` | date | next due date (source of truth) |
| `intervalDays` | int | calendar interval |
| `intervalKm` | int | optional kilometre interval |
| `lastDone` | date | date the inspection was last recorded |
| `kind` | options | inspection kind (English values) |
| `orderKind` | options | `scheduledInspection` \| `defect` \| `contractMaintenance` \| `inspectionProtocol` |
| `result` | options | `pass` \| `defect` |
| `inspectionNote` | string | optional note written to the duty by `apply_inspection` |

`kind` option values (create all the intake uses; labels in the intake language,
see [country-de.md](country-de.md) when the label language is German):

- `occupationalSafetyCheck`
- `periodicVehicleInspection`
- `electricalTest`
- `fireExtinguisher`
- `ladder`
- `oilChange`
- `contractMaintenance`

Platform fields already on `serviceOrder` that this skill uses, not redefined:
`orderStatus` (`open` / `inProgress` / `done`), `description`, `task`,
`assignedTo`, `priority`, `startedAt`, `completedAt`.

### 1.5 Link types

Confirm in `onto_link_index` before you depend on them:

| Link | Direction | Linkvalue | Use |
|---|---|---|---|
| `concerns` | serviceOrder → asset (`car`, `device`, `tool`, `machine`, `building`) | `ofAsset` (set on the edge) | duty or defect to its asset |
| `concerns` | protocol → duty (both `serviceOrder`) | `ofOrder` (set on the edge) | protocol created by `record_inspection` |
| `bestehtAus` | organisation → building | — | site tree, same as shift-planning |

Invent none. If `concerns` does not allow a pair you need, stop and file a
service request.

## 2. Recipe

1. Read `ontouser_scope_index`. Reuse `_master` / `_team` if the intake says so.
2. Create the missing scope or scopes. Read the index again. Lower-case the ids.
3. Set manager rights on all three (read, write, manage).
4. Read `ontouser_scope_types` on each scope. Activate the types in section 1.3
   with `ontouser_scope_types_set` (full list). Read back.
5. Create the property definitions in section 1.4, one at a time. Read each back.
6. Confirm `concerns` in `onto_link_index`.
7. Smoke test: `onto_type_show` on `serviceOrder` in the maintenance scope quotes
   every key in section 1.4.

## 3. Checks via MCP

- `ontouser_scope_index` lists three names with the agreed suffixes; you are
  manager of all three.
- `ontouser_scope_types` on master and maintenance shows the types in 1.3 as
  active.
- `onto_type_show` on `serviceOrder` in the maintenance scope quotes `dueDate`
  (date), `intervalDays`, `kind`, `orderKind`, `result`, `lastDone`,
  `inspectionNote`.
- Each property definition's `scope_id` is `<maintenance_scope_id>`.

## 4. Checks in the browser

As the manager, open the three scopes from the app and confirm their names.
There is no business data yet.

## 5. Phase gate

Quote the three scope names, the active types per scope, and the
`serviceOrder` fields from `onto_type_show`. If any line is missing, phase 0 is
not closed.

## 6. Typical errors

- `ontouser_scope_types_set` dropped types that were already on the scope
  because the new list was incomplete.
- Property definitions created without `scope_id`, so they are not the
  customer fields this skill uses.
- Option values translated into the label language (the value must stay
  English; the label may change).
- A second `_master` created instead of reusing the shift-planning master.
