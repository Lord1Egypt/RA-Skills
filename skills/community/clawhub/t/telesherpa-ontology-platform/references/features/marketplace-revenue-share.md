# Marketplace & revenue share — monetising your own scopes

## Concept

An agent is not only a data consumer but can itself become a data provider: create its own
scope, curate it (import + refinement, e.g. geocoding, completeness check,
comments), offer it publicly — and then automatically earns credits when other
users/agents work in this scope. The creator remains scope manager and sees
third-party usage/feedback.

**Already live as a showcase:** public, read-only reference scopes with real
industry data (including mobile-network infrastructure from official sources in several countries).

## Flow

### 1. Create your own scope

```json
{"name":"ontouser_scope_create","arguments":{"name":"meinbereich","description":"..."}}
```
→ The name is freely selectable (`[a-z0-9_]`, max 30 characters), no automatic prefix.

### 2. Curate

Import data (see import pipeline below), enrich it (e.g. `onto_object_geocode`
for address data from coordinates), check completeness, maintain metadata. This is the
actual value creation — simply passing raw data through offers little differentiation.

### 3. Offer publicly

```json
{"name":"ontouser_scope_set_visibility","arguments":{
  "scope_id": <eigener scope>,
  "read_allowed_for": ["PUBLIC"]
}}
```
Alternatively `read_allowed_for: [<scope_id_x>]` to release to specific user groups instead of
completely public. Only the owner (`can_manage_scope: 1` in `ontouser_scope_index`) may
set visibility.

### 4. Earn — automatically, no separate payout step

In addition to `usage_30d` (own spending), `onto_credit_balance` also returns
`earnings_30d`/`earnings_total` (revenue from third-party usage of your own scope). This
revenue is **credited directly in `balance`** — no separate wallet, no
manual credit entry required. Example response:

```json
{
  "balance": 352,
  "earnings_30d": [{"operation":"set_property","credits":2,"count":1}],
  "earnings_total": 2
}
```

## Checking scope status

```json
{"name":"ontouser_scope_index","arguments":{}}
```
Your own scopes are listed under `own[]`, each with `can_read`/`can_write`/`can_manage_scope`.
Only `can_manage_scope: 1` means owner rights (setting visibility, earning credits).
`public[]` lists publicly available scopes of others that you have not yet
assigned to yourself (`ontouser_scope_assign_public` to join).

## Import pipeline

There is an ETL engine for the initial data import into a scope. An agent can
**use** the result (query it via `onto_type_show`/`onto_object_search`); the pipeline
itself is configured by the platform.

If an import is desired: formulate the source (URL/API) + target object type with property mapping as
an ETL spec and hand it to the platform for configuration (see
`service-order-dispatch.md` for the related pattern "agent formulates, human executes").
