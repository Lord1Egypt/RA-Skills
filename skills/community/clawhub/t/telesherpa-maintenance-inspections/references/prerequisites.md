# Prerequisites

Complete this file before the intake is closed and before phase 0. Measure what
the account can actually do; do not copy a previous run.

## 0. Stop here first: credits

Call `onto_credit_balance` and `onto_credit_pricing` on the account that will
build the workspace. Quote `billing_model`, the balance and the date (Europe/Berlin).
If the model is pay-per-use, agree a budget and a top-up contact before you create
scopes. If the balance cannot cover phase 0, stop and ask. Do not start and hope.

## 1. Account and rights

The building account has role `member` and can manage the scopes it creates.
Confirm with `auth_status`. The tool list you use is the list that call returns
for *this* account, not a number remembered from this skill.

You need, at least, tools to: list and create scopes, set types on a scope, show
a type, create property definitions, create and show objects and links, create
and show views, start cards, forms, actions, functions and triggers, and execute an action. If a
required tool is missing, stop and file `ontouser_service_request`.

## 2. First step: measure, do not assume

| Call | What you quote |
|---|---|
| `auth_status` | role, and that the tools named in the phases are present |
| `onto_credit_balance` | billing model, balance |
| `onto_credit_pricing` | date, and the keys you will actually use (`create_scope`, `create_object`, `create_link`, `action`, `delete_*`, …) |
| `ontouser_scope_index` | existing scopes; whether `_master` / `_team` can be reused |
| `onto_type_show` on each type in phase 0 | the type exists and is readable |
| `onto_link_index` | `concerns` accepts `serviceOrder` with `car`, `device`, `tool`, `machine`, `building` |
| `onto_catalog_index` | only if you plan to apply a preset; quote the content first |

Time zone of the business: Europe/Berlin, or stop and file a service request
(intake 5).

## 3. Credits

Write down: the budget, who tops up, and the stop rule (cap reached, or a phase
at more than twice its estimate). Read the balance again before each phase.
Deleting an object or a link costs the live `delete_*` price; budget clean-up
separately. Never delete by name or prefix.

## 4. Price list

Do not copy a price table into the run log from memory or from this skill. Save
the live `onto_credit_pricing` result with date and time (Europe/Berlin). Quote
key and number when you explain spend. How to read the table is in the platform
skill: [tool-traps.md](../../../telesherpa-ontology-platform/references/features/tool-traps.md).

## 5. Object types: catalogue, preset, or missing

Required types for this skill:

| Type | Where it is used |
|---|---|
| `organisation`, `building`, `person` | master: business, site, people |
| `car`, `device`, `tool`, `machine` | master: assets (use the types the intake actually needs) |
| `serviceOrder` | maintenance: duties, protocols and defects |

Read each type with `onto_type_show` before you activate it. A member does not
create types. If a required type is missing, stop and file
`ontouser_service_request` using a short template: the type name, why this
skill needs it, the scope you wanted to activate it in, and the `onto_type_show`
/ catalogue result. Do not substitute a neighbouring type (for example do not
store a device as a `tool` because `device` was missing).

Activate types with `ontouser_scope_types_set`. That call **replaces** the list
on the scope; include every type the scope must keep. A preset may be applied
only on an empty scope, and only after `onto_catalog_index` has shown its
content. Types on a scope are not access control.

## 6. Checklist

- [ ] `auth_status` quoted
- [ ] live price list and balance quoted, budget agreed
- [ ] time zone Europe/Berlin, or a service request filed
- [ ] every required type readable
- [ ] `concerns` confirmed for the asset types in use
- [ ] reuse of existing `_master` / `_team` decided
- [ ] intake A, B, D and E answered in writing
