# Rules & Functions — automation on the platform

The platform has an **automation layer**: rules (called „Trigger" in the system) react to
changes on objects, functions are named calculations/effect bundles that rules can call.
Both are **ontology objects**, not a separate schema.

> **Rules and functions can also be CREATED via MCP.** Reading, running
> **and writing** go via MCP (`onto_trigger_create/_update/_delete`,
> `onto_function_create/_update/_delete`). Earlier versions of this reference said „creation only
> via HTTP/admin" — that is outdated.

## The building blocks

| Object type | ID | Definition stored as | Purpose |
|---|---|---|---|
| `trigger` | 25 | property `triggerdef` | rule: „if X happens, do Y" |
| `function` | 26 | property `functiondef` | named calculation + effects |

As with `actiondef` and `formdef` there is **no separate schema entry** for them — deliberately.
The automation reads exactly this property; the GUI writes nothing else.

**Every object write produces an event** (kind of change, affected object, field,
old and new value, trigger source). The worker drains this buffer.

## Flow

```
Objekt wird geschrieben
    → der Server legt ein Ereignis an
        → der Abarbeiter laeuft (kurzer Takt) und zieht passende Regeln
            → lädt aktive trigger-Objekte, die passen (event + object_type + Feld)
                → prüft condition (deklarativ, KEIN SQL)
                    → führt effects aus: set_property | create_object | create_link | run_function
                        → Effekt erzeugt Event → nächste Runde (max_depth 3)
```

Two operating modes — **two timers, not one**:

| Operating mode | Trigger source | Worker | Interval |
|---|---|---|---|
| `on_change` (insert/update/delete) | object change | own worker | short |
| `schedule` (time-driven) | time schedule | own worker | longer |

Each path has **its own** worker — one does **not** cover the other. If only
the time-driven one runs, one never sees event-driven rules fire.

Status and backlog are queryable (open / total / error / ok / skip). The status endpoint
is not reachable from outside.

## Structure of a rule (`triggerdef`)

```json
{
  "on": "update",
  "object_types": ["radioTower"],
  "scopes": [<SCOPE_ID>],
  "enabled": true,
  "condition": {
    "changed": ["status"],
    "props": [ { "key": "status", "op": "eq", "value": "defect" } ]
  },
  "effects": [
    { "type": "set_property", "key": "priority", "value": "high" },
    { "type": "run_function", "function": "wartung_faellig" }
  ]
}
```

**Allowed `on` values:** `insert`, `update`, `delete`, `schedule`, `link_removed`.
`link_removed` fires when a link of one of the listed `link_types` is removed — with
`remove: "pair"` as well as with `replace_link`; `to_removed: true` addresses the person
who was released.

**Allowed `effects[].type`:** `set_property`, `create_object`, `create_link`, **`run_function`**,
**`notify`**, `run_import_source`, `http_call`.
`webhook` is **deliberately not allowed** — it would remain silently ineffective.
The validator rejects it on save with a plain-text message.
Details for `notify` and `link_removed`: `notifications-and-link-events.md`.

**`condition.changed`** — fire only if one of these fields has changed.
For an operation that writes several fields (e.g. form submit), this is the
most effective brake against multiple firing.

**`condition.props[]`** — value comparison against the **current object state** (not against the
event). Operators: `eq`, `neq`, `in`, `gt`, `gte`, `lt`, `lte`, `empty`, `notempty`, `matches`.
Fail-closed: an unknown operator counts as **not satisfied** (not as „always true").

## Creating a rule/function via MCP (today's way)

```
onto_function_index    → does the function already exist? (name or udid)
onto_trigger_index     → which rules run in the scope? (`q` filters by name, for this call only)
onto_dispatch_status   → did they run? backlog, errors, last events
```

**A rule does not fire instantly.** Events are picked up every 60 s, time-based rules every
5 minutes; a busy queue takes longer. So after creating a rule and making a change, look at
`onto_dispatch_status` instead of repeating the action or assuming it failed.

**Create a function** — `onto_function_create`:

```json
{"name":"onto_function_create","arguments":{
  "name":"wartung_faellig",
  "scope_id":<SCOPE_ID>,
  "body":{
    "inputs":[{"key":"kmStand","type":"int","required":true}],
    "body":{"if":[{"\u003e":[{"field":["kmStand"]},10000]},"faellig","ok"]},
    "effects":[],
    "timeout_ms":2000
  }
}}
```

**Create a rule** — `onto_trigger_create`:

```json
{"name":"onto_trigger_create","arguments":{
  "name":"meine_regel",
  "scope_id":<SCOPE_ID>,
  "body":{
    "on":"insert",
    "object_types":["inspection"],
    "condition":{"props":[{"key":"zustand","op":"eq","value":"kritisch"}]},
    "effects":[{"type":"create_object","object_type":"changeRequest","name":"Eskalation: {object_name}",
                "props":{"proposedKey":"zustand","text":"Automatisch erzeugt"},
                "links":[{"linktype":"proposesChange","to":"{object_udid}"}]}]
  }
}}
```

Return: `{udid, key, scope_id}` (the `udid` is the identifier for `_update`/`_delete`).

- **`object_types` is mandatory and must not be empty** — the server validation rejects an
  empty list with „without an object type the rule never takes effect" (400), and every type named
  must be present and active.
- **`scopes` is filled from `scope_id` at creation** — the caller does not need to pass it.
  The list is the permission for execution, see Security.
- `scope_id` is mandatory; you need **`can_manage_scope`** there (403 otherwise). The
  public scope only through the operator.
- `key` is sanitised to `[a-zA-Z0-9_]` and must be unique (409 otherwise).
- `_delete` is a **soft delete** (`status=deleted`) — reversible.
- **`_create` and `_update` are schema writes**: they change what the platform
  does automatically. Write permission (`can_write`) is deliberately **not** enough.

Placeholders in values: `{object_udid}`, `{object_name}`, `{value_new}`, `{value_old}`.

## Structure of a function (`functiondef`)

```json
{
  "inputs": [
    { "key": "objekt", "type": "object",   "required": true },
    { "key": "schwelle", "type": "int",    "required": false }
  ],
  "body": { "cat": ["Wartung fällig: ", { "field": "name" }] },
  "effects": [ { "type": "set_property", "key": "note", "value": "faellig" } ],
  "timeout_ms": 2000
}
```

- **`inputs[].type`:** `object`, `string`, `int`, `float`, `bool`, `datetime`, `list`.
- **`body`** is an **AST for the expression parser** — there is no second
  interpreter. Validation runs on save; an unknown operator is an
  **error at creation time**, not only at execution.
- **`timeout_ms`:** 100–30000, otherwise an error.
- **Convention:** the input key `objekt` carries the target UDID
  (see `onto_function_run`: `inputs` = `{key: wert}`).

### Operator catalogue (whitelist)

Anything outside this list is rejected on save.

- **Selection/data:** `var`, `source`, `field` (alias for `var`)
- **Graph navigation:** `link`, `linklist` — access linked objects via links
- **Aggregation over lists:** `count_of`, `sum_of`, `max_of`, `min_of`
- **Logic:** `and`, `or`, `!`, `if` (2–3 arguments)
- **Comparison:** `==`, `!=`, `===`, `!==`, `<`, `<=`, `>`, `>=`, `in`, `notin`,
  `empty`, `notempty`, `matches`
- **Arithmetic:** `+`, `-`, `*`, `/`, `%`, `min`, `max`, `abs`, `round`
- **Text:** `cat`, `lower`, `upper`, `len`, `trim`
- **Form-specific:** `sum_over`, `count_over`

The AST **always** has the form `{"operator":[argumente]}` — thus `{"-":[a,b]}` for a minus b,
not `{"op":...}`.

`link`/`linklist` take a **configuration object**, not an expression:
```json
{ "link": { "type": "performs", "dir": "in", "prop": "kmReading" } }
```
A typo in the link type is caught on save if the caller passes the valid link types
(e.g. from the link definitions) — otherwise silently an empty value.

## Security (fail-closed, all verified)

- **Visibility per row** via scope management — no admin bypass.
- **The target scope must be managed** (`can_manage_scope=1`); the public scope only through the
  operator.
  The check happens server-side per scope, fail-closed.
- The target scope is **the permission**: it determines which objects the rule may act on.
  If it is drawn too wide, the rule applies everywhere in that area. Keep it narrow.
- **`max_depth` (default 3)** against infinite loops (effect produces event produces effect).
- **Dedupe 60 s** against repeat firing — the comparison is `(Trigger, Objekt, Feld, **Wert**)`,
  via a fingerprint. The **value** must be compared as well: otherwise genuine
  value changes are discarded.
- **Role whitelist per definition** (default `member`).
- **Automation costs NO credits.** Only a person or an agent triggering something pays the price
  of that write; a rule that fires afterwards is free.

### An effect type outside the whitelist is rejected on save
No silent no-op. Conversely: a `run_function` reference to a non-existent function
is likewise rejected on save, so that a rule does not fire and do nothing.

## Access paths — the important difference

| Path | Read | Write |
|---|---|---|
| **MCP** | `onto_trigger_index`, `onto_function_index`, `onto_function_run` | `onto_trigger_create/_update/_delete`, `onto_function_create/_update/_delete` |
| **HTTP (web/admin)** | in the web interface under Automation („Automatik") | the same functionality as the MCP tools |

Both paths end in **the same** functionality — MCP is the wrapper around it. An agent therefore
**no longer** needs the web interface. The six write tools are visible for the `member` role
(no admin needed); the real lock is `can_manage_scope` per target scope.

**The tool names end in `_create`/`_update`/`_delete`, NOT `_save`.** A client that looks for
`_save` finds nothing and falsely reports „tool missing".

Running works via MCP: `onto_function_run` with `function` (UDID **or** name) and `inputs`.

## Example: a rule with `create_object` and a link

`onto_trigger_index` lists the existing rules, `onto_function_run` (or a run through the
worker) shows what happened. Pattern for `create_object` with a link:

```json
{"on":"insert","object_types":["inspection"],"scopes":[<SCOPE_ID>],
 "condition":{"props":[{"key":"zustand","op":"eq","value":"kritisch"}]},
 "effects":[{"type":"create_object","object_type":"changeRequest",
             "name":"Eskalation: kritischer Zustand {object_name}",
             "props":{"proposedKey":"zustand","status":"proposed",
                      "text":"Automatisch vom Trigger erzeugt: Standort-Check {object_name} wurde im strukturierten Feld 'zustand' als 'kritisch' eingestuft."},
             "links":[{"linktype":"proposesChange","to":"{object_udid}"}]}]}
```

## Pitfalls

1. **A rule never fires inside the call.** Writing an object only queues the event; the effect
   follows within minutes. If „my rule does nothing", wait one interval before anything else —
   and do not write the object a second time.
2. **Form answers produce events** (trigger source „Formular"). Always test through the real path
   and check that the event arrived — a hand-built event only proves your own assumption.
3. **Multiple firing per operation (the „4x bug").** One submit writes N fields → N events.
   `condition.props` is checked against the CURRENT object state, not against the event — so
   each of the N events sees the finished object. The dedupe does not apply (different `key_name`
   = different hashes). **Remedy:** set `condition.changed` — then a gate in the
   worker applies and the same submission produces only one effect instead of four.
4. **The scope is the permission, not the home.** A rule only acts on objects whose
   scope is in the rule's permission list. If an object is moved to another scope,
   the rule no longer applies there.
5. **Dedupe window 60 s.** Two genuine changes of the same field to the same value
   within 60 s → only one execution. For an expected second run, change to a
   **different value**.
6. **`set_property` in effects uses `props` (object), NOT `key`/`value`.** A body with
   key/value is not recognised as wrong by the validation, but does nothing.
7. **`create_link` needs `linkvalue`** — if it is missing, the **whole effect** fails, not just
   the link. For `create_object.links` both key names are valid (`type` and `linktype`);
   every skipped link is noted in the action log.
