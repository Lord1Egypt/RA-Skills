# Scan flows: checkpoint, admission, shelf (QR)

**What you take away:** how a printed QR code becomes a transaction that the ontology itself
decides — with the binding rule for when execution happens immediately and when the user
must confirm, and with the evidence in the action log.

## Structure

1. The **object carries the state as a property** (e.g. `checked_at` on the checkpoint).
2. The code at the location or on the item contains the object's **UDID**.
3. The client sends the scan to the server; the server looks up the matching actiondefs, checks their
   condition and responds with candidates.
4. Execution happens **immediately or by button** — the server decides (see the rule below).
5. The **evidence** is created in the action log `onto_action_logs`, one row per execution with
   `action` (action key), object, account and `scope_id`.

The bundled interface serves the route `GET /ontouser/scan` (role `member`) — camera, sound,
feedback, result list and buttons, with a cache-buster on its own files. The **contract is
the server**, not the page — the same calls work from any interface.

## Server contract (HTTP, role `member`)

| Call | Purpose |
|---|---|
| `POST /onto/object/match_actions` — `{"udid": "<hex32>", "partner": "<hex32>"}` | Which actions match this scan? **Information only**, no change, no credit |
| `POST /onto/object/execute_action` | Executes a candidate (cost: `action`) |
| `POST /onto/object/counter` — `{}` | Counters from all visible actiondefs (read-only) |

`match_actions` returns per candidate: `key`, `label`, `auf_udid` (object on which execution
happens), `prompt` (field that receives the UDID of the other object), `partner`, `offene` (required
prompts without a default), `message`, `replace`, `remove`, `ein_code`, `blockiert`, `ausfuehrung`,
`bestaetigen`.

- **Two codes:** send `partner` along (package + shelf slot). Both scan orders are checked —
  which one was scanned first does not matter.
- **One code:** actions **without** a link are offered (acknowledge checkpoint) —
  recognisable by `ein_code: true`.
- `blockiert: true` means: the condition (`condition`) is violated, `message` explains it. Blocked
  candidates are delivered, not withheld — the user should see why not.
- The client must show `offene` as a form **before** it executes.

## Execution rule (server, binding)

1. exactly **one** possible `auto` action that does not detach a link → runs **immediately**
2. exactly **one** candidate in total → runs, **unless** it detaches a link (`remove`)
3. otherwise (several paths **or** a detaching action) → **buttons**, `bestaetigen: true`
4. `blockiert` and `remove` **never** run automatically

Mnemonic: *An action that detaches a link or violates its precondition never runs
automatically.* There are no exceptions, not even with `scan.ausfuehrung: "auto"`.

## Fields on the actiondef

`object_types`, `scopes`, `roles` as usual, plus for the scan:

- `condition`: `{ "props": [{"key","op","value"}], "message": "…" }` — **always evaluated
  server-side**. A condition that only the interface checks is not a condition.
- `prompts[]`: additionally `default_value`; `object_types: ["storage"]` turns a text field into an
  **object selection** (the client fills in the UDID).
- `action.links[]`: `{ "type", "from", "to", "replace", "remove", "require", "text" }` —
  `require: "absent"` / `"present"` checks the link, `text` is the plain-text message on
  violation, `replace: "source"` replaces an existing link (package from shelf A to B).
- `counter`: `{ "label": "Controls today", "query": "…" }` — a counter is evaluated server-side and
  only ever counts what the caller may see. If a counter fails, it is simply absent from the response;
  the scan continues.
- `scan`: `{ "ausfuehrung": "auto" | "bestaetigen" }` — default `auto`, `bestaetigen` forces buttons.
- `feedback`: `{ "scan" | "success" | "error": {"sound","color","mode","haptic","ms"}, "silent":
  bool, "dedupe_ms": int }` — three-stage feedback. The client separates the stages in time
  (default 320 ms, overridable via `abstand_ms`), otherwise sound and colour overlap.
  `dedupe_ms` swallows the same scan within the window.

## Object model (proven example)

| Purpose | Type | Field set |
|---|---|---|
| Checkpoint | `checkpoint` | `checkpoint_props`: `code`, `title`, `section`, `tour`, `interval_min`, `checked_at`, `checked_by` |
| Admission | `ticket` | `ticket_props`: `description`, `event`, `admitted`, `admitted_at`, `left_at` |
| Package / storage slot | `package`, `storage` | `package_props` (`place`), `storage_props` (`description`) |

- Address fields come from the existing set `address` (`street`, `postalCode`, `city`, `latitude`,
  `longitude` with geocode/reverse layout) — do not rebuild them.
- Admission in two actions: **admit** (`admitted = ja`, `admitted_at = {now}`, link
  `concerns → {user_person}` with `replace: "source"`) and **leave** (`admitted = ""`,
  `left_at = {now}`, the same link with `remove: true`). The state `admitted` is the
  truth, the link only shows the holder.
- **Object types are part of the platform schema** and are created by the platform operator. A
  customer agent starts from the types that exist (catalogue/presets) and builds actions, views
  and reports on top of them; new types are a service request.
  Field names in English, labels as **i18n keys without the `mo.` prefix**. Without an export of the
  language files the interface shows the raw key (`mo.Checkpoint`). Check beforehand which
  keys already exist (`onto_i18n_matrix`) — `mo.Area` means "Areal", not "Bereich".

## Use case: event admission control (type `ticket`)

At the entrance the printed ticket is scanned. **One code is enough** — there is no counterpart object,
because the guest has nothing to show except the ticket.

| Part | Configuration (proven) |
|---|---|
| Action | `qr_admit`, label "Einlass: Ticket einlassen" (admission: admit ticket), `object_types: ["ticket"]`, role `member` |
| Condition | `admitted ne "ja"` → message **"This ticket has already been admitted"** ("Dieses Ticket wurde schon eingelassen") |
| Effect | `admitted = "ja"`, `admitted_at = {now}`, link `concerns` from `{object_udid}` to `{user_person}` with `replace: "source"` (whoever currently holds the ticket) |
| Counter | **"Already admitted"** ("Schon eingelassen"): active tickets with `admitted = "ja"` |
| Feedback | three stages, `dedupe_ms: 2000` (the same code does not book twice within 2 s) |
| Counterpart | `qr_leave`, label "Auslass: Ticket verlassen" (exit: leave ticket): condition `admitted eq "ja"` → **"This ticket is not at the event"** ("Dieses Ticket ist nicht auf der Veranstaltung"); sets `admitted = ""`, `left_at = {now}` and detaches the link (`remove: true`, `require: "present"`) |

What follows from this — and why it is built this way:

- **The condition is the control, not the interface.** The second scan is rejected server-side
  and says in plain text why. At an entrance this is the most important case: it happens
  five hundred times in an evening.
- **The state `admitted` is the truth**, the link only shows who last had the ticket
  (`replace: "source"` — the last holder wins).
- **Counters count state, not events.** "Already admitted" is the number of tickets in the
  admitted state. Anyone who wants "currently inside" must subtract those who left (take `left_at`
  into account) — otherwise the total number of all admissions is there in the evening.
- **`qr_leave` never runs automatically**: it detaches a link, so there are buttons. `qr_admit`
  runs immediately with one code (only `remove` forces confirmation, `replace` does not — anyone
  who wants a deliberate tap confirmation sets `scan.ausfuehrung: "bestaetigen"`).
- **A ticket without an event reference is worthless.** `event` needs to be filled, otherwise the
  counter counts tickets from all events together.
- **What the evidence cannot do:** it shows ticket, time and account — not that the person
  was present, and not that nobody enters twice with two tickets. Anyone who needs that
  works with person instead of ticket (separate task).

## Use case: chaotic storage (types `package`, `storage`)

No fixed slot: **the package gets its slot at the moment it is put down.**
The slot is an object (`storage`) with its own glued-on code — a shelf number, a
floor marking, a box.

| Part | Configuration (proven) |
|---|---|
| Check in | `qr_shelf_in`, label "Regal: Paket einchecken" (shelf: check in package), `object_types: ["package"]`, prompt `place` (`required`, `object_types: ["storage"]` → **object selection**, the client fills in the UDID) |
| Link | `concerns` from `{object_udid}` to `{place}`, `replace: "source"`, `require: "absent"` → message **"The package is already checked in at this slot"** ("Das Paket ist an diesem Platz schon eingecheckt") |
| Check out | `qr_shelf_out`: sets `place = ""` and detaches the same link (`remove: true`, `require: "present"`) → **"The package is not checked in at this slot"** ("Das Paket ist an diesem Platz nicht eingecheckt") |

What follows from this:

- **Two codes, but the order is free.** The client can scan the package first and the slot first
  — the server checks both paths and decides what execution runs on. Which one is scanned first
  is not an operating rule that has to be explained to the warehouse.
- **The shelf code is the address.** There is no master data maintenance in advance: create the
  slot object, print the code, stick it on. That is why "chaotic" works at all — the shelf does
  not have to be in a list, it only has to carry a code.
- **`require: "absent"` / `"present"` make the error visible.** Double check-in or
  check-out at the wrong shelf ends in a sentence, not in a silent data error.
- **Check-out never runs automatically** (`remove`) — there the tap is deliberate. Check-in may
  run immediately after the prompt.
- **One state, not two.** Currently check-in only maintains the link, check-out
  additionally clears the field `place` on the package. That is a contradiction in the source of truth:
  maintain either the link **or** the field. A state that is kept twice falls apart at some point.
  (Legacy: the test package still carries the old value `platz_udid` — not declared,
  cleaning it up would be a data change.)
- **No slot per package in the model.** The statement "package P is in box K" sits in the
  link, not in a list. Evaluations ("how many packages in this box") count via
  the link; a counter on the shelf page is not built yet.

## Evidence

- The source is `onto_action_logs`. For the control evidence every execution with
  `action = 'qr_control'` counts.
- The **assessment belongs in the report, not in the scan**: the interval to the previous control at the
  same checkpoint against `interval_min`, plus the travel time since the previous control at a **different**
  checkpoint of the same account — conspicuously short travel times expose ticking off without changing location.
- **Reports never widen access.** A report shows what its reader may see — build the query so that it
  filters by scope, and check with a second account that it does.
- Filter values are **third-party input**. The built-in filters handle that; a self-written query
  does not — take column names from your own definition and never paste a value from the URL into it.
- The report header is a **comma-separated string**, not a JSON structure, and must not contain a
  comma in a heading. Filters come in the order of the
  `search_cols` and take effect **only via POST**; the JSON/GET route ignores them.
- A report may carry `candownload = 1`, then the CSV export is enabled.

## Pitfalls

1. **One code is not the other.** An action with a link needs two codes; one without a
   link is not offered in pair mode. Anyone who wants both in one action builds two
   actiondefs.
2. **Renamed action keys and fields tear the history**, if the log rows (`action`,
   `payload`) and the report SQL are not carried along. The report then shows 0 rows,
   although the actions are in the log.
3. **Do not put plausibility into the scan.** The scan must stay fast; the report computes
   the assessment from the same raw data.
4. **The client caches.** After every change to a client file check the cache-buster
   (`?v=<Dateizeit>`); otherwise the user tests the old version.
5. **The error text belongs to the user.** Formulate `message`/`text` in plain text, no codes.
6. **`replace` does not force a confirmation — only `remove` does that.** Anyone who wants a deliberate
   tap at admission does not rely on the link type, but sets `scan.ausfuehrung:
   "bestaetigen"`. Conversely: an action without `remove` runs immediately with exactly one candidate
   — even if it replaces an existing link.
7. **The same state in two places is a predicted error.** Maintaining a link **and** a field
   (`place`) at the same time sounds harmless and only shows up when the two
   diverge. Define one source of truth, only read the other.
