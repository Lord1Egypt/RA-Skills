# Prerequisites

Check every point **before** phase 0. Do not trust this file blindly — measure.

## 0. Stop here first: credits

A fresh account starts with **0 credits**, and the first thing this skill does —
creating three scopes — already costs **260 credits** (100 + 80 + 80, the price per scope falls with the number of own scopes). If `onto_credit_balance` is 0,
nothing else in this skill works: the very first write answers **HTTP 402**.

Get the money sorted before you build anything (section 3 says how): a prepaid code
from the operator, a card payment by the human, or a service request if you are an
agent without a payment method. Ask for the amount you actually need —
[measurement](measurement.md) budgets a complete build plus a staffed test week at
**about 4,260 credits (~43 EUR)**; phase 0 alone needs 260.

Do not start phase 0 with less than phase 0's cost in the account, and do not
improvise a workaround: a half-built workspace costs more than waiting for credits.

## 1. Account and rights

| Need | Detail |
|---|---|
| Telesherpa account with MCP access | Role `member` is enough for everything in this skill. No elevated platform rights are needed or assumed. Registration: see the platform skill (`telesherpa-ontology-platform/SKILL.md`, "register"). |
| Own scopes | You create three scopes with `ontouser_scope_create`; you become their owner and can manage them. |
| A manager (human or agent) | Named in [intake](intake.md). Holds read + write on all three scopes. |
| At least one staff test account | An **activated managed account** with rights as in phase 3 §3. Human registration needs an activation e-mail at a dedicated controlled mailbox; documentation addresses at `example.com` cannot be activated. Obtain permission for a usable test-account route before staff tests, and match the master person to the actual login. If the allowed test-data policy permits only placeholder addresses, stop those login tests instead of bypassing activation. Use a management invitation and read back the managed-account rights; see [company-manager.md](../../../telesherpa-ontology-platform/references/features/company-manager.md). |
| Browser access for acceptance | Some checks are only visible in the browser (rendered view values, CSV download, toasts, what a staff member sees). Plan a human or a browser-capable agent logging in as manager **and** as staff. |
| Time zone | Stored and returned as **UTC**, with the `_local`/`value_local` sibling in the viewer's zone. **Naive input is read in the viewer's zone** (default `Europe/Berlin`, measured 2026-11-25: `2026-11-10 09:00:00` is stored as `08:00:00` UTC); append `Z` or an offset (`2026-11-10T09:00:00Z`) and it is taken literally. If the business is in another zone, say so in phase 0 and file `ontouser_service_request` ([intake](intake.md) question 6) — the default zone is per profile, the skill assumes Europe/Berlin. |

## 2. First step: measure, do not assume

Run these read-only calls first and keep the answers in your run log:

1. `GET https://mcp.telesherpa.com/health` → `status` must be `ok`. Note the `tools` value; do not compare it with any number in a document. Without raw HTTP access skip this and rely on step 2.
2. `auth_status` → token valid, roles contain `member`, number of tools visible to *your* account.
3. List your tools — the tool list of your MCP client is enough (with raw HTTP: `tools/list` after `initialize` with the `mcp-session-id` header). Confirm that every tool below exists; a missing tool → stop (see SKILL.md "Stop and escalate").

   | Phase | Tools that must exist |
   |---|---|
   | 0 | `ontouser_scope_create`, `ontouser_scope_index`, `ontouser_scope_types`, `ontouser_scope_types_set`, `onto_type_show`, `onto_property_def_create`, `onto_property_def_update`, `onto_link_index`, `ontouser_team_index`, `ontouser_team_show`, `ontouser_team_set_scope_rights`, `onto_credit_balance`, `onto_credit_pricing` |
   | 1 | `onto_object_create`, `onto_object_show`, `onto_object_index`, `onto_object_set_property`, `onto_object_execute_action`, `onto_actiondef_save`, `onto_actiondef_list`, `onto_function_create`, `onto_function_run`, `onto_trigger_create`, `onto_formdef_create`, `onto_formdef_save`, `onto_interface_create_def`, `onto_interface_update_def`, `onto_interface_show` |
   | 2 | `show_formdef` (plus the phase-1 tools) |
   | 3 | `create_invite_code`, `ontouser_team_transfer`, `onto_trigger_update`, `onto_trigger_index`, `onto_startcard_save`, `onto_startcard_index`, `ontouser_notification_index` |
   | 4 | no new tools |
   | any | `ontouser_service_request`, `onto_object_addcomment`, `ontouser_notification_send`, `onto_object_delete` |
   | acceptance clean-up | `ontouser_team_offboard_preview`, `ontouser_team_offboard` |

4. `onto_credit_balance` → `balance` and `billing_model`. `flat` accounts are not charged; a measured test run needs a pay-per-use account.
5. `onto_credit_pricing` → keep the full table with date and time (section 4).

## 3. Credits

- **There is no starting credit.** A fresh account has 0 credits. See section 0 before
  you touch anything.
- Ways to get credits (platform skill, "credits"): pay by card (`onto_credit_checkout`, a human pays), prepaid code (`onto_credit_chargeup`), or ask the operator via `ontouser_service_request` (a request, not a claim to free credits). Never trigger a payment without explicit instruction from the human.
- **The executing account pays.** A staff member clicking "Clock in" pays 20 credits from *their* balance, even through a scope bridge. Staff without credits get **HTTP 402** and the UI may show no message ("dialog hangs"). Give each staff account a small balance with `ontouser_team_transfer` (`reason` and `idempotency_key` are required; reuse the same key on retry so nothing is booked twice).
- **Lists are free** (index/list calls); opening a single object costs `read` = 1 credit. Writes are expensive, deletes the most.

## 4. Price list (live, read 2026-11-11, about 18:55 Europe/Berlin (UTC+1))

Read it again at the start of every run with `onto_credit_pricing`; the live table wins.

| Key | Credits | Typical use in this skill |
|---|---|---|
| `graph` | 1 | object graph |
| `read` | 1 | opening one object |
| `set_property` | 2 | single field correction |
| `create_link` | 5 | links between objects |
| `addcomment` | 5 | comments / notes |
| `update_link` | 5 | link value change |
| `update_object` | 5 | object update |
| `bulk_action_per_object` | 5 | per object in a bulk call |
| `file_upload` | 5 | qualification certificate |
| `file_per_mb` | 1 | per MB uploaded |
| `create_object` | 10 | shifts, people, templates, requests |
| `form_answer_complete` | 20 | completed form |
| `action` | 20 | every action execution (manager **and** staff) |
| `delete_property` | 20 | removing a field value |
| `delete_link` | 20 | removing a link |
| `delete_object` | 20 | removing an object |
| `complete_service_order` | 50 | completing a service order |

Scope price (one-time, per own scope, volume discount): 1st scope **100**, 2nd–3rd **80 each**,
4th–10th **60 each**, from the 11th **50 each** credits. There is **no upper limit** on the
number of own scopes — 402 on `ontouser_scope_create` means "not enough credits", never
"plan reached". 1 credit = 0.01 EUR. The 260 of this skill assume a fresh account without
other scopes; an account that already manages scopes starts higher up the ladder. If the account
already owns scopes, log what is actually booked. Recurring plan fees, if your plan
has any, are not part of this table — ask the operator before a paid run.

Notes:
- The live table on 2026-11-11 returned **17 operation keys plus four scope price bands** (100 / 80 / 60 / 50 credits per scope, falling with the number of own scopes; there is no upper limit). Count what you get and log it; the live table always wins.
- **Deleting costs 20 credits** — as much as an action. A test run that creates probes and deletes them pays twice. Budget the clean-up, or keep test objects with the `TEST-` prefix.
- Creating property definitions, actions, views, triggers and functions has no own price key in the table. Whether these calls are free or booked under another key is visible on your statement after the first run.
- **Triggers and notifications cost no credits** (confirmed); only the writes that cause them do (see SKILL.md).

## 5. Object types: catalogue, preset, or missing

All types this skill uses are **platform types**; you activate them per scope, you do
not create them. No catalogue preset bundles them, so activate them one by one with
`ontouser_scope_types_set` (phase 0).

| Type | Used for | Note |
|---|---|---|
| `organisation` | business | |
| `building` | site / restaurant | |
| `space` | station (kitchen, service, …) | |
| `person` | staff member | `email` binds the login |
| `shiftTemplate` | shift template | |
| `shift` | shift | |
| `absence` | absence, day-off wish | |
| `changeRequest` | shift request, swap, takeover, handover | may be missing from the activation list but still usable — see phase 0 |
| `demand` | staffing demand | optional in phases 1–4 |
| `serviceOrder` | plan period, manager notes | |
| `file` | qualification certificate | |
| `comment` | notes (who/when/old → new) | |

Check each with `onto_type_show` (name, `type.id`, properties). **If a type is
missing**, stop and file a service request. A member agent cannot create types.

Template:

```json
{
  "tool": "ontouser_service_request",
  "arguments": {
    "category": "feature",
    "subject": "Missing object type for shift planning: <type_name>",
    "text": "I am setting up shift planning (industry skill shift-planning, verified 2026-11-06) in my scopes <company>_master / <company>_planning / <company>_team. The type <type_name> is not available (onto_type_show returns <status/error>). I need it for <purpose>. Please activate it or tell me the intended replacement. I have not created any workaround.",
    "context": {"tool": "onto_type_show", "arguments": {"name": "<type_name>"}, "response": "<verbatim response>"}
  }
}
```

The same template (category `bug`) is used for any platform fault from the stop list.

## 6. Checklist

- [ ] health ok, `auth_status` member, tool list contains every tool named in phase 0
- [ ] billing model known; balance covers the phase-0 budget (≥ 260 credits for three scopes plus margin)
- [ ] price table saved with timestamp
- [ ] all twelve types readable with `onto_type_show` (`changeRequest` may be missing from the **activation** list of `ontouser_scope_types` and still work — phase 0 §1.3)
- [ ] intake answered and confirmed by the business
