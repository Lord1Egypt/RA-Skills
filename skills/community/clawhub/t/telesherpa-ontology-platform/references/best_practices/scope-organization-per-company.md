# Scope organisation for companies (agent → employee)

**Status:** Recommended pattern for new company scope setups in self-service.
**Question:** How do you organise scopes so that employees may do exactly what they should —
which scopes does the company agent create, what goes into them, who gets which rights?

---

## 1. The core: rights run through scopes, not through roles

On the platform there are no freely definable data-access roles. All platform users
share the same base role; **who may do what follows exclusively from the
scope memberships:**

- `can_read` — read
- `can_write` — write
- `can_manage_scope` — manage (invite, set rights, visibility)

So there is only *one* axis for distinguishing rights — and that is the scope.

**Consequence:** Anyone who may do A but not B must be separated via scopes. There is no second
axis through which one could express that.

**And from that follows the actual problem:** write permission on a scope applies to **all
objects** of that scope, without exception. One scope per company means: all employees may do everything.

## 2. The way out: reading and writing are TWO axes

You do not have to put everyone into the same scope. Access is granted along separate paths:

| Axis | Effect |
| --- | --- |
| **Writing** (`can_write`) | write to all objects of the scope |
| **Reading** (`can_read`) | read all objects of the scope |
| **Managing** (`can_manage_scope`) | owner: invite, set rights, visibility |
| **Bookability** | who may book the scope itself (`read_allowed_for`) |
| **Opt-out** | company switches off individual actions |
| **Field level** | individual fields only for specific scope holders |

An object lies in **exactly one** scope. But a scope can be **readable** for holders of other
scopes. So: **writing is exclusive, reading is shareable.** That is the whole construction.

## 3. The actual mechanism: the two-phase commit is your object permission

This is the most important point. There is already a commit on submit:

| Phase | Answer scope | Who may write |
| --- | --- | --- |
| **Draft** (`status=draft`) | write scope of the person filling it in | the employee |
| **Submit** (`status=sent`) | target scope of the action (`target_scope`) | only those who may write there |

The employee has **no write permission on the target scope** — which is why he cannot change the
finished answer after submitting, even though he created it. **That is the permission**, without a
single object ACL: on submit the answer *moves* out of his write scope into a read scope.

The commit runs server-side from the configuration (never from the request) and moves object +
properties + links + files + subform rows in one transaction. **Important:** without the
file cascade the customer sees the answer without signature/photos.

**`target_scope` is a decision, not an obligation** — see section 8.

## 4. Proposal: THREE scopes per company (base pattern, not rigid)

```
<firma>_stammdaten   Stammdaten: Standorte, Kundenobjekte, Anlagen
<firma>_arbeit       Arbeitsbereich: Entwürfe, laufende Besuche
<firma>_archiv       Ziel-Scope: abgeschlossene Antworten
```

Why exactly these three — and not one or ten:

- **`stammdaten`** — the objects *on* which work is done. Must be readable by everyone
  (the field service must see the site), but should not be changed by everyone.
- **`arbeit`** — **drafts** live here. Writing yes, but nobody outside sees half-finished work.
  Separate from `stammdaten` so that a draft **never** accidentally turns up in the customer records.
- **`archiv`** — completed answers land here. Only back office/agent write here.

**This is a base pattern for the single-team case, not a fixed number.** If two teams must not
see each other's drafts, each team needs its own `arbeit` scope — the formula
is actually **1× `stammdaten` + 1× `archiv` + N× `arbeit`** (one per team with
draft separation), not rigidly three. **Write granularity = scope granularity.**

**The standard scope quota is deliberately tight** — a company with one team gets by with
it. If the company grows to several teams, more is needed; additional scopes are available via
credits, alternatively there is a flat model without an upper limit. So whoever hits the quota
has not found an error but reached the point at which usage pays off — that is intended
design, not a bug that one would have to work around.

## 5. What carries which axis — the four levels

| Level | Where it belongs |
| --- | --- |
| Visibility of the form definition | `stammdaten` (or `+PUBLIC` for a generic template) |
| Allowed object type | `["building"]` (or the site type) |
| Visibility of the button | `stammdaten` — button only on these objects |
| Data ownership of the answer | `archiv` or "scope of the parent object" |

Example of an action:
```json
{
  "object_types": ["building"],
  "scopes": [<stammdaten-id>],
  "action": {
    "type": "form_answer",
    "form": "<form-udid>",
    "target_scope": <archiv-id>
  }
}
```

**Important:** button visibility (`scopes`) is **not a security boundary**. It only filters
*where a button is displayed*; whoever triggers an action is additionally checked against the scope of the
target object. Whoever needs a real boundary must draw it there — not via the button display.

## 6. Who gets which rights — the three patterns

The agent is **scope owner** (`can_manage_scope=1`) and distributes rights in three ways:

**(a) Invite codes — targeted, for known people**
`create_invite_code(scope_id, can_read, can_write, can_manage_scope, allowlist, max_uses, expires_at)`
- Code format `XXXX-XXXX`, typeable (without 0/O/1/I/L). **Not secret** — meant to be passed on.
- Allowlist via `email` / `domain` / `glob` (e.g. the company's domain = all employees).
- Rights are **additive** (`max(code, bestehend)`) — a code can never revoke.
- `revoke` only prevents new redemptions; whoever is already in stays.
- **One code = one scope.** If an employee needs rights on several scopes (e.g. field service:
  `stammdaten` read + `arbeit` write), he redeems several codes for that — one per scope.

**(b) Visibility — self-booking, for open groups**
Owner sets the scope to public/bookable → it appears in the public list →
the employee books himself **read only** via `assign_public`. Writing is not reachable that
way — that is intentional.

**(c) Operator — for cases that self-service does not cover**
More scopes than the quota, or a scope without an owner.

### Building the rights matrix — via MCP

The assignment runs via invite codes; the agent as owner (`can_manage_scope=1`) creates them
and hands them out:

```
create_invite_code   scope_id=<stammdaten>  can_read=1  can_write=0
create_invite_code   scope_id=<arbeit>      can_read=1  can_write=1
create_invite_code   scope_id=<archiv>      can_read=1  can_write=0
```

Three codes for the field service — one per scope, because **a code grants exactly one scope**.
For open groups (changing subcontractors) put the domain entry into the allowlist or
upload the address list as XLSX via `upload_code_allowlist` (fully replaces the `email` entries
of this code, `domain`/`glob` remain).

Follow-up check at any time with `list_members` (who is in, which flags) and
`list_invite_codes` (which codes are still valid). **`toggle_member_flag` changes only ONE
right** — `remove_member` deletes the whole assignment.

### Concrete rights matrix (recommendation)

**Company agent / dispatch**
- `stammdaten` — write + manage
- `arbeit` — write + manage
- `archiv` — write + manage

**Back office / inside service**
- `stammdaten` — write
- `arbeit` — read (sees running jobs)
- `archiv` — write (evaluates completed ones)

**Field service / employees**
- `stammdaten` — **read** (sees the site, does not change it)
- `arbeit` — **write** (creates drafts, uploads signature)
- `archiv` — read (sees own completed visits)

**Read-only users / reporting**
- `stammdaten` — read
- `arbeit` — no access
- `archiv` — read

Important for the field service: giving `stammdaten` **read only** is the lever. That is exactly where the
sites sit — and nobody should change the master data while documenting a visit.

## 6b. Images as part of the setup (structured image storage)

It belongs to every site setup and is configured **before** the first field visit, because
the app then asks for exactly the motifs the back office needs:

```
onto_scope_structuredimage_categories       scope_id=<stammdaten>  → was gibt es schon?
onto_scope_save_structuredimage_categories  scope_id, categories=[...]
```

Recommendation for a site setup: 4–6 motifs, each with `de`+`en` as language variants of the same
`imagename`, and **exactly one with `thumbnail: true`** (that becomes the preview image in cards and
lists). Motifs that repeat on every visit get `versioned: true`.

**The file name is the key:** the person taking the photo (human in the app) uploads under the
name that stands as `imagename` in the category. If the name does not match exactly, only the
placeholder appears — without an error message. Details and a complete example:
`references/features/structured-image-storage.md`.

## 7. Fine-tuning: fields and buttons

**Individual fields** — a scope can be assigned to a field so that it is only visible for holders of this
scope (checked when rendering *and* on submit). This allows, for example: cost fields only
visible for the back office.
```json
{ "key": "kosten", "widget": "float", "label": "Kosten", "scope_id": <archiv-id> }
```

**Individual actions** — the company can deselect individual actions on the scope (opt-out) without anything
changing in the configuration itself.

**Recycle-bin trap:** `toggle_member_flag` changes **one** right, `remove_member` deletes the **whole**
assignment. Anyone who wants to "remove only writing" must not use `remove_member` — otherwise the
read right is gone as well.

## 7b. Two automations that almost always pay off

Rules (triggers) and functions are **not an extra** — they replace the phone call-back.
Both can be created via MCP (`onto_trigger_create`, `onto_function_create`), in the
target scope with `can_manage_scope=1`.

**1. Escalation on a critical finding** (the pattern is live on the platform):

```json
{"on":"insert","object_types":["inspection"],"scope_id":<arbeit>,
 "condition":{"props":[{"key":"zustand","op":"eq","value":"kritisch"}]},
 "effects":[{"type":"create_object","object_type":"changeRequest",
             "name":"Eskalation: {object_name}",
             "props":{"status":"proposed","text":"Automatisch aus dem Standort-Check erzeugt."},
             "links":[{"linktype":"proposesChange","to":"{object_udid}"}]}]}
```

**2. Metric from two fields** (function, callable in a rule via `run_function`):

```json
{"inputs":[{"key":"kmStand","type":"int","required":true}],
 "body":{"if":[{"\u003e":[{"field":["kmStand"]},10000]},"faellig","ok"]},
 "effects":[],"timeout_ms":2000}
```

**Two rules for operation** (both otherwise experienced as errors):
- **Always set `condition.changed`.** A form submit writes several fields = several
  events; without `changed` the rule fires per field (real: 1 case → 4 effects).
- **Rules act asynchronously.** A rule never fires inside the call that triggered it; the
  effect follows within minutes. Do not resend the write because "nothing happened yet".

Complete, including effect types and operator list:
`references/features/automation-and-functions.md`.

## 8. The honest remainder

- **No object-level right.** Anyone with write permission on a scope may change *all* objects in it.
  There is no per-object exception. Whoever needs that must cut finer
  (more scopes).
- **`can_write` does not imply `can_read`.** Set both rights separately, otherwise the
  employee does not see his own drafts.
- **On draft, the answer scope inherits** the write scope. Without a target scope (`target_scope`) the
  answer stays there — then the back office never sees it.
  **`target_scope` is a deliberate decision, not an obligation in every case:** sensible when
  creator (draft) and editor of the finished answer should be different roles/people
  (field service writes, back office evaluates). In a three-person operation where everyone
  may edit everything (e.g. a painting business without role separation), omitting it is valid — not a
  gap but a deliberate renunciation of the separation. Just be clear about WHY you decide that way —
  do not forget it by accident.
- **Visibility is bookability, not read permission.** Who may read is decided by `can_read`.
  Confusion leads to "scope visible, objects not".
- **A scope can become orphaned** (no active manager). Orphaned scopes can be listed
  specifically so that a company does not get stuck without an owner.

## 9. Summary in one sentence

Not one scope per company, but **at least two**: one in which work is done (write for
employees) and one in which results lie (write only for the back office) — the switch happens
automatically on submit via `target_scope`, if you deliberately decide in favour of it. Reading is shared
via `can_read`, writing is separated via scope boundaries.

## 10. Decision points — what the agent must determine

The scope structure follows from the business, not from the platform. The agent must decide four points
**deliberately** and record them in the handover note:

| Decision | What it depends on |
| --- | --- |
| `target_scope` yes/no | Are creator (draft) and editor (finished answer) different people? |
| Number of `arbeit` scopes | How many teams must **not** see each other's drafts? |
| Scope public (`PUBLIC`) | Should third-party usage automatically credit credits (marketplace)? |
| Rights matrix | Who reads master data, who writes where, who manages? |

Details on `target_scope` in section 8 — it is a **decision, not an obligation**. An
omitted `target_scope` is valid, but only as a deliberate choice: the answer then stays in the
write scope, and the back office never sees it. The difference between "deliberately omitted"
and "forgotten" only shows months later — which is why the reasoning belongs in writing in the
handover note (`references/best_practices/first-30-minutes.md`).
