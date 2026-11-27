# Prerequisites

Check every point **before** phase 0. Do not trust this file blindly — measure.

## 0. Stop here first: credits

A fresh account starts with **0 credits**, and creating scopes already costs the
volume price from the live table (three new scopes on a fresh account are billed as
the first, second and third own scope). If `onto_credit_balance` is 0, the first
write answers **HTTP 402**.

Get the money sorted before you build anything: a prepaid code from the operator, a
card payment by the human, or a service request if you are an agent without a
payment method. Ask for the amount you actually need — [measurement](measurement.md)
explains how to budget; phase 0 alone needs the live price of the scopes you still
have to create (reuse of an existing master or team door reduces that).

Do not start phase 0 with less than phase 0's cost in the account, and do not
improvise a workaround.

## 1. Account and rights

| Need | Detail |
|---|---|
| Telesherpa account with MCP access | Role `member` is enough. Registration: platform skill (`telesherpa-ontology-platform/SKILL.md`, "register"). |
| Own scopes | You create the missing scopes with `ontouser_scope_create`; you become their owner. If [shift-planning](../../shift-planning/SKILL.md) already exists for this business, **reuse** its `_master` (and, if the intake says so, its `_team`) instead of creating duplicates. |
| A manager (human or agent) | Named in [intake](intake.md). Holds read + write + manage on all three scopes. |
| At least one staff test account | An **activated managed account** with rights as in phase 0. Human registration needs an activation e-mail at a dedicated controlled mailbox; documentation addresses at `example.com` cannot be activated. See [company-manager.md](../../../telesherpa-ontology-platform/references/features/company-manager.md). |
| Browser access for acceptance | Print PDF, short URL before sign-in, the scan page and what a staff member sees are not proven by MCP lists alone. Plan a human or a browser-capable agent logging in as manager **and** as staff, and one logged-out fetch of `/q/<code>`. |
| Time zone | Stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally. If the business is in another zone, note it in phase 0. |

## 2. First step: measure, do not assume

Run these read-only calls first and keep the answers in your run log:

1. `GET https://mcp.telesherpa.com/health` → `status` must be `ok`. Note the `tools` value; do not compare it with any number in a document. Without raw HTTP access skip this and rely on step 2.
2. `auth_status` → token valid, roles contain `member`, number of tools visible to *your* account.
3. List your tools. Confirm that every tool below exists; a missing tool → stop.

   | Phase | Tools that must exist |
   |---|---|
   | 0 | `ontouser_scope_create`, `ontouser_scope_index`, `ontouser_scope_types`, `ontouser_scope_types_set`, `onto_type_show`, `onto_property_def_create`, `onto_property_def_update`, `onto_link_index`, `onto_catalog_index`, `onto_catalog_presets`, `ontouser_team_index`, `ontouser_team_show`, `ontouser_team_set_scope_rights`, `onto_credit_balance`, `onto_credit_pricing` |
   | 1 | `onto_object_create`, `onto_object_show`, `onto_object_index`, `onto_object_set_property`, `onto_object_execute_action`, `onto_actiondef_save`, `onto_actiondef_list`, `onto_interface_create_def`, `onto_interface_update_def`, `onto_interface_show` |
   | 0 also | `onto_function_index`, `onto_function_create`, `onto_function_update` |
   | 2 | (phase-1 tools) |
   | 3 | `create_invite_code`, `ontouser_team_transfer`, `onto_startcard_save`, `onto_startcard_index` |
   | 4 | `onto_action_logs` (or the current tool name for the action log — confirm in your catalogue) |
   | 5 | (phase-1 tools; stock bookings use `onto_object_execute_action`) |
   | any | `ontouser_service_request`, `onto_object_addcomment`, `ontouser_notification_send`, `onto_object_delete` |
   | acceptance clean-up | `ontouser_team_offboard_preview`, `ontouser_team_offboard` |

4. `onto_credit_balance` → `balance` and `billing_model`. `flat` accounts are not charged; a measured test run needs a pay-per-use account.
5. `onto_credit_pricing` → keep the **full table with date and time** (Europe/Berlin). That table wins over every figure you remember. How to log it is also described in the platform skill and in [shift-planning prerequisites](../../shift-planning/references/prerequisites.md) — do not copy an old table into this run.

## 3. Credits

- **There is no starting credit.** A fresh account has 0 credits. See section 0.
- Ways to get credits: platform skill, "credits". Never trigger a payment without explicit instruction from the human.
- **The executing account pays.** A staff member running `label_bind` pays the `action` price from *their* balance, even through a scope bridge. Staff without credits get **HTTP 402**. Give each staff account a small balance with `ontouser_team_transfer` (`reason` and `idempotency_key` are required).
- **Lists are free** (index/list calls); opening a single object costs `read`. Writes and deletes follow the live table.

## 4. Price list

**Do not quote prices from this file.** Read `onto_credit_pricing` at the start of
every run, save the table with a timestamp (Europe/Berlin), and use those numbers in
the measurement log. Typical keys you will see (the live table is the authority):
`read`, `create_object`, `create_link`, `action`, `file_upload`, `delete_object`,
`delete_link`, and the volume bands for own scopes.

Notes:

- 1 credit = 0.01 EUR, unless the live table says otherwise.
- Deleting is expensive. Budget clean-up, or keep test objects with the `TEST-` prefix.
- Creating property definitions, actions and views may have no own price key. Log what is booked.
- Whether a print or charge action is billed as `action`, `file_upload` or another key is visible only on your statement — confirm it on the first sheet.

## 5. Object types: catalogue, preset, or missing

All types this skill uses are **platform types**; you activate them per scope, you do
not create them. A catalogue preset `lager` bundles `package`, `storage`, `label`,
`person` and `file`. It does **not** include `organisation` or `building`. Read
`onto_catalog_index` first. Prefer activating types with `ontouser_scope_types_set`
(the call **replaces** the list). Apply the preset only on an empty scope after you
have read what it contains; applying a preset can overwrite type definitions.

| Type | Used for | Note |
|---|---|---|
| `organisation` | business | reuse from shift-planning if it exists |
| `building` | site / branch | reuse |
| `person` | people who bind and who manage | `email` binds the login; reuse |
| `storage` | physical slot (shelf, floor mark, box) | in master; bookings record it on `movesTo` |
| `package` | physical unit; carries `menge`, `einheit`, `lot`, `bestBefore` | change `menge` only by booking a movement |
| `label` | printed sticker with its own `code` and `charge` | pointer only; actions `label_bind` and `label_rebind` |
| `stockMovement` | one booking row | type `movementType` `putaway` / `pick` / `relocate` / `count`; links `moves`, `movesTo` |
| `file` | print PDF | via `hasfile` |

Check each with `onto_type_show` (name, properties, `action_keys`). Also confirm
`stock_move_apply` and `stock_count_apply` in `onto_function_index`, or plan to
install them in phase 0.

**If a type is missing**, stop and file a service request. A member agent cannot
create types.

Template:

```json
{
  "tool": "ontouser_service_request",
  "arguments": {
    "category": "feature",
    "subject": "Missing object type for warehouse logistics: <type_name>",
    "text": "I am setting up warehouse logistics (industry skill warehouse-logistics, version 1.0) in my scopes <company>_master / <company>_warehouse / <company>_team. onto_type_show for <type_name> returns <status/error>. I need it for <purpose>. Please activate it or tell me the intended replacement. I have not created any workaround.",
    "context": {"tool": "onto_type_show", "arguments": {"name": "<type_name>"}, "response": "<verbatim response>"}
  }
}
```

The same template (category `bug`) is used for any platform fault from the stop list,
including a missing Avery 3475 print path.

## 6. Checklist

- [ ] health ok, `auth_status` member, tool list contains every tool named in phase 0
- [ ] billing model known; balance covers the phase-0 budget (live scope prices plus margin)
- [ ] price table saved with timestamp
- [ ] types `label`, `package`, `storage`, `stockMovement`, `person`, `organisation`, `building`, `file` readable with `onto_type_show`
- [ ] links `identifies` (label → package, unique), `moves` and `movesTo` present in `onto_link_index`
- [ ] intake answered and confirmed by the business
- [ ] decision recorded: reuse existing shift-planning master (and maybe team) or create new scopes
