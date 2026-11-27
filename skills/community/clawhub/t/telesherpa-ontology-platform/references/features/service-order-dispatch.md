# ServiceOrder — digital task → real human work

## Concept

The platform's biggest differentiator compared with pure data backends (Firebase, Supabase,
Snowflake): an agent can not only write data but **trigger real field work**.
A `serviceOrder` object, linked to a site, appears for human field service technicians
in their app/web interface — they accept it, do the work, close it. The agent gets the
result back (including uploaded photos, comments).

**Important:** This is not a simulation. A real person actually drives to a site.
A `serviceOrder` should therefore never be created carelessly — in tests always mark it clearly as
`TEST` in the name/task, so that the person executing it can immediately recognise that it is
not a real assignment.

## Lifecycle

```
open --(claim_service_order)--> inProgress --(complete_service_order)--> done
```

- **open**: the order is unassigned, visible in the open pool (interface `serviceOrders`)
- **inProgress**: someone has taken it over (`assignedTo` set, `startedAt` timestamp)
- **done**: completed (`completedAt` timestamp)

Both human and agent can call `claim_service_order` (self-assignment is wanted, not merely
permitted — everything is logged/audited, that is the control mechanism,
not an upfront lock).

## Creating the object (manual, two steps)

```json
// 1. serviceOrder-Objekt erzeugen
{"name":"onto_object_create","arguments":{
  "type":"serviceOrder",
  "name":"TEST - <Beschreibung>",
  "scope_id": <eigener Write-Scope>,
  "properties":{"task":"<Aufgabenbeschreibung>","priority":"low|medium|high","status":"open"}
}}

// 2. Mit Standort verlinken (Standort kann in fremdem read-only Scope liegen — SSR greift)
{"name":"onto_object_create_link","arguments":{
  "linktype":"hasServiceVisit",
  "object1_udid":"<standort-udid>",
  "object2_udid":"<serviceOrder-udid>"
}}
```

The link appears on the site object as `hasServiceVisit` (verb `mo.hasServiceVisit`,
reverse verb `mo.takesPlaceAt`).

## Creating the object (directly at the site, shorter)

Many object types now have a `create_service_order` action directly in the schema
(checkable via `onto_type_show`, field `schema.action_keys`). That saves the manual
create+link step:

```json
{"name":"onto_object_execute_action","arguments":{
  "action_key":"create_service_order",
  "udid":"<standort-udid>",
  "prompts":{"task":"...", "priority":"low"}
}}
```

## Steering the order

```json
{"name":"onto_object_execute_action","arguments":{"action_key":"claim_service_order","udid":"<serviceOrder-udid>"}}
{"name":"onto_object_execute_action","arguments":{"action_key":"complete_service_order","udid":"<serviceOrder-udid>"}}
```

## Checking the result

`onto_object_show` on the serviceOrder udid returns `status`, `assignedTo`, `startedAt`,
`completedAt`. Photos/comments that the executing person adds land as separate
`comment` objects (linked via `hascomment`) or in the structured image store of the
linked site object — look there, not only at the serviceOrder itself.

## Poll instead of guessing

Instead of periodically repeating `onto_object_show` on the serviceOrder udid, use the
poll cursor (`references/features/auth-token-lifecycle.md` describes the
related auth pattern; `onto_watch_changes` with `action` as a filter, e.g.
`action: "claim_service_order"`, saves calls and credits).

## Permission boundary (important)

Write permission on a scope does NOT automatically mean the right to create `serviceOrder` objects
or to execute `create_service_order`/`claim_service_order` actions — that can be
gated separately by RBAC (a 403 despite otherwise working write access is a signal
that must be explicitly unlocked, it does not follow automatically from object rights).
