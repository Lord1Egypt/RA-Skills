# Real use cases — verified end to end

These patterns are not hypothetical — they were played through completely in real agent
sessions, including a real human at the other end. They show how the individual capabilities
(objects, scopes, actions, marketplace) combine into an actual result.

## 1. Closing a documentation gap at a field service site

**Starting point:** A location object in a public, read-only reference scope had
an empty image storage category ("Schlüsseltresor / Position") and no on-site information.

**Procedure:**
1. `onto_object_search` (type filter or name) → find the location
2. `onto_file_structured` on the location → see categories + existing images (which
   category is still missing?)
3. `onto_object_addcomment` → record the observation ("key in the key box on the left
   next to the gate")
4. `upload_file_to_object` with `type: structuredimage`, `name: <Kategorie-Dateiname>` (the missing
   category) → the image lands automatically in your own write scope (SSR), **without**
   needing write permission on the external reference scope
5. For deeper documentation (an on-site photo instead of web research): `onto_object_execute_action`
   with `action_key: create_service_order` → a human receives the order, drives there,
   takes the photo themselves, uploads it, closes it (`complete_service_order`)

**Takeaway:** SSR (scope self-routing) turns a pure data consumer (read-only
access to external reference data) into an active curator, without touching the data
sovereignty of the original owner. Details: `service-order-dispatch.md`,
`structured-image-storage.md`.

## 2. Curating and monetising a public dataset (marketplace)

**Starting point:** Public OpenStreetMap data (defibrillator locations, tag
`emergency=defibrillator`) was to be offered as its own, more valuable dataset.

**Procedure:**
1. Have the import pipeline configured (the agent delivers the ETL spec: source = Overpass API query,
   target object type with property mapping) → the raw data lands in the new scope
2. `ontouser_scope_index` → confirm scope membership with `can_manage_scope: 1` (the agent
   is owner)
3. **Refinement, not just passing through:** `onto_object_geocode` (`direction: reverse`,
   `apply: true`) on every object → raw OSM coordinates become structured addresses
   (street, postcode, city) — exactly the gap that distinguishes raw data from curated data
4. `onto_object_search` with a `type` filter + spot check → verify completeness before
   publishing
5. `ontouser_scope_set_visibility` with `read_allowed_for: ["PUBLIC"]` → the scope becomes public
6. Other users work in the scope → `onto_credit_balance` shows `earnings_total` > 0,
   automatically included in `balance`

**Takeaway:** The value lies not in the import itself (anyone can do that) but in the
refinement (geocoding, completeness check, structure) — that is what other users
actually pay for. Details: `marketplace-revenue-share.md`.

## 3. Sensor time series: fleet and history

**Starting point:** A scope with 10 objects, one of which carries vehicle telemetry —
two series, `location` (geo) and `speed`.

**Procedure:**
1. `onto_object_index` → the object udids of the scope
2. `onto_series_last` with `objects: [alle udids]`, `series: ["location", "speed"]` →
   **one** call instead of N
3. For the history of a single object: `onto_series_range` with `resolution: 300`

**Measured result:** with 10 requested objects, **2 values** come back — nine
objects have no point in these series. This is not an error but the correct answer
to "which measurements exist". The answer is a list of **existing measurements**, not a
list of objects.

**Takeaway:** Anyone expecting "number of results = number of objects" considers a correct answer
broken. Likewise an **empty** list is a valid result — a vehicle that is currently sending
nothing has not disappeared. All times are UTC with `Z`. Details:
`sensor-time-series.md`.

## Building your own automations

The building blocks shown (schema introspection, pagination, service order dispatch) can be combined
into your own loops — for example a systematic completeness audit across one
object type that marks gaps automatically as a `serviceOrder` or comment.

**Caution when implementing:** Using `create_service_order` in a loop over
many objects carries the risk of accidentally triggering many real field deployments at once
— before such a batch run, always coordinate with the scope owner, do not
dispatch in series on your own authority.
