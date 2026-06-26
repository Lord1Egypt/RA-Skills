# Changelog

All notable changes to the **Working with Emm AI** skill (ClawHub slug: `working-with-emm`; previously published under `managing-actingweb-memory`).

## [2.0.0] — 2026-06-01 — GA

First generally-available release of the skill, shipping with the Emm
AI GA. The skill now leads with a **Critical Rules** table (every
must-follow rule on one screen) and a four-question save-vs-don't-save
decision table, documents what "tool loading mid-cycle" looks like on
Claude.ai so the assistant doesn't pause to ask, and uses the new
`status()` / `how_to_use()` orientation surface and `mode:
normal/instructions_update` language throughout. Net effect: fewer
subtly-broken outputs and fewer mid-run confusions.

The `## [2.0.5]`–`## [2.0.19]` sections below are the pre-GA
development series (one bump per usability-evaluation round); they are
kept for history. Installed skills compare their frontmatter `version`
against the server's `status().latest_skill_version` and nudge a
reinstall only when the server's value is newer — so a clean 2.0.0
baseline is what new users install from here.

## [2.0.19] — 2026-05-29

Polish follow-up to the v2.0.18 usability evaluation (grade A−).
Closes the recurring `news` auto-categorisation misroute, makes the
quick-mode framing honest about its savings, adds a queue-vs-search
caveat to Task Check, fixes the dashboard "last run" time drift, and
completes the prefixed-tool-name sweep in `how_to_use()`.

### Changed

- **Quick-mode framing is honest about the savings.** The mode
  table and bundle description said quick mode is "filtered to
  `[quick]`-tagged tasks," which read as a much smaller bundle than
  it is. Quick mode runs *fewer tasks* and drops
  `personal`/`style`/`skills`, but still ships the full `agents`
  brief, the full `tasks` doc, and the Pre-Run procedure — so the
  bundle is only moderately smaller (≈30%). The skill now says so,
  and frames quick mode as "do less work," not "save a lot of
  context."
- **Task Check distinguishes the ready queue from search hits.**
  A note (skill + `default_tasks`) that
  `work_on_task(list_only=true)` is the only authoritative source
  of ready one-off tasks: items the user is still preparing in the
  Builder wizard also live in `memory_requests` and surface in
  `memory_search`, but they are not yet ready and a search hit on
  one is not a pending task.
- **Dashboard `Last run:` uses a server-provided stamp.** The
  `agent_run()` preamble now carries a ready-to-paste `Last-run
  stamp` (`YYYY-MM-DD HH:MM UTC`); the skill and `default_tasks`
  tell the assistant to paste it verbatim and only append the
  highlight, instead of formatting its own time. Stops the
  dashboard "last run" from drifting away from the real run record.

### Fixed

- **`how_to_use()` prefixed-tool-name sweep is now complete.**
  v2.0.18 fixed Recipe 1 and the URL-mapping table, but the eval
  found `save()` / `search()` / `create_type()` still in the
  Available-Tools list, the retrieval-patterns examples, the
  custom-category example, and the agent-run "Now" step. Every
  remaining bare mention is now the canonical prefixed name
  (`memory_save`, `memory_search`, `memory_create_type`), so a
  skill-less LLM following the onboarding never reaches for a tool
  that doesn't exist.

### Server-side (paired Emm AI release)

- **First-person work/process notes stop landing in News.**
  Auto-categorisation no longer treats a bare verb (track /
  monitor / follow / read) as a News signal; the keyword list keeps
  the subject nouns so genuine cues ("track AI regulations") still
  route to News while "tracking my findings" routes to Notes/Work.
  Low-confidence specific-category guesses now fall back to Notes.
- **Account snapshots count durable memories, not the agent-task
  queue.** `how_to_use()` and the memory-stats view exclude
  system-managed types (the `work_on_task` queue) from the
  "memories stored" total; the system queue is tallied separately.

## [2.0.18] — 2026-05-29

Round-13 evaluation follow-up. The transport-id surface from
round 12 was correctly structured but inert in Claude.ai web —
the library fell back to a synthetic `<ip>:<hash(UA)>` placeholder
that leaked as `unknown:0` when the transport carried no
`Mcp-Session-Id`, no remote_addr, and no User-Agent. The library
now returns `None` instead, the skill teaches the fallback rule,
and the text view renders `(none)`. Plus batch `memory_save`
now carries per-input-position duplicate disposition matching
the single-path `-32096` envelope's richness, the `you_are`
text view drops the compact dash form for path-style lines that
match every sibling field, and the last two cosmetic envelope
leaks (`how_to_use()` recipe tool names, empty `id` in
`not_found` envelopes) close.

### Added

- **Per-input-position duplicate disposition in batch `memory_save`.**
  Each `batch_result.results[i]` now carries an explicit
  `disposition` (`saved` | `duplicate` | `failed`); duplicate rows
  also include `existing_id`, `similarity`, and the existing
  item's `short_description` preview — matching the single-path
  `-32096 duplicate_memory` envelope's richness. The visible
  text annotates each row: `items[0]=memory_work:7 (saved),
  items[1]=duplicate→memory_work:5 (sim 0.92)` instead of the
  prior aggregate `(1 duplicate)` count.

### Changed

- **`your_transport_session_id` returns `None` when the transport
  carries no header.** Earlier revisions fell back to a synthetic
  `<client_ip>:<hash(UA)>` form for cache-keying convenience; that
  same value leaked into the public field as `unknown:0` for
  every Claude.ai web session (no header, no remote_addr, no UA).
  The cache-key path (`_get_session_key`) is unchanged; only the
  public per-connection identifier surface is honest about not
  having one. Text view renders `your_transport_session_id:
  (none)`. The skill teaches: when either side of the transport-id
  comparison is null, fall back to the client-id guard alone.
- **`status().you_are` text view renders path-style.** Two lines
  (`you_are.client_name: …` / `you_are.description: …`) instead
  of the compact `you_are: <name> — <description>`, matching how
  `sessions.total_active: N`, `limits.memory_max_kb: K`, and
  every other field render. The structured payload is unchanged
  (`{client_name, description}` as the skill has always
  documented). This closes the Q drift that recurred across
  evals #5 – #7.

### Fixed

- **`how_to_use()` Recipe code blocks use prefixed tool names.**
  Recipe 1 and the URL-mapping table referenced `search(query=…)`
  and `save(content=…)` — but the loaded tools are
  `memory_search` and `memory_save`. A skill-less LLM that
  followed `how_to_use()`'s onboarding would look for a `search`
  tool and not find one. The recipes now match the canonical
  prefix.
- **`not_found_envelope` drops the empty `id` field for
  category-level lookups.** Category lookups (empty `item_id`,
  e.g. `output_delete_category("missing")`,
  `memory_delete_type("missing")`) used to surface
  `action_required.id: ''` — a stray empty field. The field is
  omitted entirely when the lookup is category-level; item-level
  lookups keep the `id` field as before.

## [2.0.17] — 2026-05-29

Round-12 evaluation follow-up. The multi-session story is the
headline this round: `status()` and `agent_run_complete(last_open=true)`
used to disagree about whether a stale `in_progress` run was still
"open" — `status` showed it past the resume window, the close path
silently said "no open run." Both now agree, and the rendered
`runs.open` text carries `started_by_session` / `started_by_client`
so an LLM reading the text can perform the coordination check the
structured payload always supported. A new `your_transport_session_id`
field surfaces the per-MCP-connection identifier alongside the
stable `your_session_id` so two browser tabs on the same Claude.ai
login are now distinguishable. Plus a sweep that brings every
remaining bare `-32000` / `-32602` error envelope into the
structured `data.code` family — symmetric with the round-11 T fix.

### Added

- **`status().your_transport_session_id`.** New top-level field
  carrying the `Mcp-Session-Id` HTTP header (per-MCP-connection
  identifier). Distinct from `your_session_id`, which is per
  OAuth2 client *registration* (shared across two browser tabs on
  one Claude.ai login). The multi-session coordination guidance
  in §"What to call up front" now teaches both comparisons.
- **`runs.open` text rendering includes `started_by_session` and
  `started_by_client`.** Same structured fields the JSON payload
  always carried — now an LLM looking at only the text can decide
  whether the open run belongs to it without falling back to
  message-text parsing.

### Changed

- **`status()` auto-abandons stale `in_progress` records.** When
  `_resolve_runs` finds an `in_progress` record older than the
  60-minute resume window, it marks it abandoned and excludes it
  from `runs.open`. This is the same window `agent_run_complete(last_open=true)`
  has always applied — both surfaces now agree on "no open run"
  for stale records. Eliminates the eval-#6 case where the close
  path silently refused while `status` still showed the run as
  open.

### Fixed

- **`memory_delete_type` errors carry `data.code`.** Symmetric
  with `output_delete_category`: missing category returns
  `-32094 not_found` with `action_required.search_or_create` and
  `tool: memory_types`; non-empty category returns `-32602
  category_not_empty` with `item_count` and `action_required.delete_items_first`
  pointing at `memory_delete`. `output_delete_category(non_empty)`
  picks up the parallel `category_not_empty` shape so both
  pillars use the same vocabulary.
- **`describe_method` / `execute_method` refuse OAuth2 session
  ids with `-32094 not_a_peer`.** `list_connections()` returns
  a merged `connections` array with `kind: peer` vs `kind:
  oauth2_session`; an LLM that grabs a session id by mistake
  used to see a bare `-32000 "No methods available for peer:
  …"` (or `"Method execution failed with HTTP 0"` from execute).
  Both tools now short-circuit with a structured envelope
  pointing at `list_connections().peers`. The `HTTP 0` plumbing
  leak in execute's generic-failure branch is also stripped —
  the message reads "No reachable methods on peer …" without
  exposing the internal transport state.
- **`output_create` / `output_update` schema-length rejections
  carry `data.code`.** The round-11 T fix structured the
  category-related `-32602`s; this sweep extends the same shape
  to the `short_description` / `title` length-and-type
  validators (`short_description_too_long`,
  `title_too_long`, `short_description_invalid_type`,
  `title_invalid_type`). Each envelope carries `actual_length`
  / `max_length` + `action_required.fix_argument` so an LLM
  doesn't parse text to learn it overshot the cap.
- **`memory_search` results include `importance` and
  `updated_at`.** Same fields `memory_get`, `memory_delete`,
  and the `-32096 duplicate_memory` envelope's `existing_memory`
  preview have always exposed; the browse builder used to omit
  them, so the response normaliser defaulted them to `null` and
  the same record showed two different shapes across read
  surfaces.
- **Internal `(round-9 #11)` / `(round 9 fix)` references removed
  from user-visible surfaces.** The `output_update` tool
  description and the `you_are` SKILL.md bullet no longer leak
  internal eval-cycle nomenclature; comments inside source files
  keep the context for code archaeology.

## [2.0.16] — 2026-05-28

Round-11 evaluation follow-up. Closes the multi-session
identity-pin regression that re-opened after round-10, renames
`status().peers.*` to `sessions.*` so the word no longer collides
with `list_connections().total_peers`, brings the
argument-validation rejections (`output_search` category gate,
`output_delete_category` standard-category refusal) into the
structured `data.code` envelope family, and tightens batch
`memory_save` so input-position is unambiguous when storage
allocates ids in non-monotonic order.

### Added

- **Batch `memory_save` text annotates each id by input position.**
  ``items[0]=memory_work:8, items[1]=memory_work:7`` instead of
  the bare ``memory_work:8, memory_work:7`` form. An LLM no
  longer has to assume monotonic id order = input order when
  storage allocates ids in task-completion order.
- **Argument-validation rejections carry `data.code`.**
  `output_search(category="log")` returns `category_excluded`,
  `output_search(category=<unknown>)` returns `category_unknown`,
  and `output_delete_category(<standard>)` returns
  `category_is_standard`. These remain on JSON-RPC `-32602`
  (the canonical "invalid params" code), but the inner code
  brings them into parity with the `-3209x` envelope family so
  one branch table covers every recoverable Emm error.

### Changed

- **`status().peers.*` renamed to `status().sessions.*`.**
  That field counts MCP OAuth2 sessions, not trusted peer
  connections — but the word "peers" already means trusted
  peers in `list_connections().total_peers`. The rename
  removes the collision; an LLM reading `sessions.total_active`
  no longer plans a shared-memory workflow that doesn't exist.
- **`default_tasks` template re-versioned (v10 → v11).**
  The round-10 fix that dropped the undefined `❓` urgency
  marker landed on the seed file but kept version 10, so
  existing actors' stored copies never got the dashboard nudge
  to upgrade. v11 triggers the nudge on next `agent_run`.

### Fixed

- **Multi-session `you_are.client_name` regression.**
  Round-9 added the per-session live `client_info` pin, but the
  cache key (`client_ip:hash(user_agent[:50])`) still collided
  when two clients on one OAuth2 credential shared IP and UA
  prefix — a second client's `initialize` overwrote the first
  client's cached identity. The cache key now prefers the
  `Mcp-Session-Id` header (the canonical per-connection
  identifier per the MCP spec) and falls back to IP+UA only
  when the header is genuinely absent. Two concurrent sessions
  on one credential now keep distinct `you_are` values
  throughout the session lifetime.
- **`output_delete_category(missing)` not-found message.**
  Used to render with a trailing empty `:` (e.g. *"No item
  found for nonexistent_eval_cat:."*) because the
  `not_found_envelope` helper assumed an item-level lookup.
  Category-level lookups (empty `item_id`) now render as
  *"No category found for &lt;cat&gt;."*

## [2.0.15] — 2026-05-28

Round-10 evaluation follow-up. Polishes the error taxonomy
(`output_delete` joins `-32094 not_found`; batch per-item errors
carry the same envelope shape), adds an output-side category
cleanup tool, converges memory_get and memory_search on one field
vocabulary, and rounds the response surface so `memory_save`
returns the new id(s) alongside `output_create`.

### Added

- **`output_delete_category` tool.** Mirror of
  `memory_delete_type` on the outputs pillar — drops empty custom
  output categories that previously lingered in the catalogue
  with no MCP path to remove. Refuses standard built-in
  categories and categories that still contain items.
- **`memory_save` returns created id(s).** Both single
  (`memory_save(content=…)`) and batch (`memory_save(items=[…])`)
  paths now surface the new id in the visible confirmation text
  (so chat-only clients can reference it without a follow-up
  search) and in per-item batch result rows. Matches the
  long-standing behaviour of `output_create`.
- **`output_search` empty-result hint surfaces in the text body.**
  The hint pointing at `output_list(category="log")` now appears
  in `content[0].text` so chat-only renderings see it; the
  structured `hint` / `excluded_categories` fields are still
  emitted unchanged.
- **`memory_get` field vocabulary matches `memory_search`.**
  Single, batch, and type-record paths now return
  `short_description` / `full_description` plus a top-level
  `source` (instead of `title` / `text` / `metadata.source`). One
  parser serves both lookup tools across the memory pillar.
  ChatGPT clients are unaffected — the OpenAI MCP spec's
  `title` / `text` shape is restored at the client-adapter
  boundary.
- **`memory_get(id='type:memory_<x>')` carries `owned_by_me`.**
  The flag now ships at the top level of the type-record (and on
  the metadata projection) so an LLM deciding "can I write
  here?" no longer needs to call `memory_types()` separately.

### Changed

- **`output_search` hard-rejects unsearchable categories.**
  `category="log"` and unknown / custom-without-items categories
  now return a `-32602 invalid_params` error with a recovery
  hint instead of silently returning "No matches", which a
  reviewer cannot distinguish from a genuinely empty result.
- **`output_delete` not-found uses `-32094`.** Round-9 #85
  swept memory plus `output_get` onto the structured `not_found`
  envelope; `output_delete` was the one site the sweep missed.
  Now consistent across the lookup-by-id surface.
- **Batch per-item not-found carries `code`/`action_required`.**
  `memory_get(ids=[…])` and `memory_delete(ids=[…])` per-item
  error dicts now include the same structured fields the
  single-mode envelope ships, so an LLM uses one parser for
  both shapes.
- **`memory_save` confirmation uses stored `display_name`.**
  Custom-typed saves no longer derive the visible label from the
  slug (`"Eval 2026 05 28"`) — the stored `display_name`
  (`"Eval Session 2026-05-28"`) is used instead.
- **`memory_save` single-mode text starts with "Saved …".**
  Aligns with the batch path's lead-in so one parser sees the
  same shape across modes.
- **Error table.** Mission-control reference card now lists
  `-32094 not_found`, `-32095 explicit_run_id_required`, and
  `-32096 duplicate_memory` (previously only documented in body
  prose).

### Fixed

- **`memory_types` description.** Said each entry carried a
  `count` field; the actual field is `item_count`. Description
  now matches the wire.
- **`default_tasks` Normalise step.** Referenced a fifth `❓`
  urgency marker that the canonical *Urgency Markers* table
  didn't define. Step now matches the table (🔥 ⏰ 📅 💡).
- **`SKILL.md` stale version self-reference.** Body line that
  said *"compare against this file's frontmatter `version`
  (currently `2.0.13`)"* drifted from the actual frontmatter.
  The parenthetical is dropped; the frontmatter is the sole
  source of truth.

## [2.0.14] — 2026-05-28

Round-9 evaluation follow-up. Per-MCP-session identity threads
through `agent_run_complete(last_open=true)` and `status().you_are`,
plus a polish sweep covering envelope URLs, error taxonomy,
response symmetry, search heal-on-read, and annotation accuracy.

### Added

- **Multi-session caveat for `agent_run_complete(last_open=true)`.**
  Agent Runs section now explains that when two MCP sessions
  share one credential (interactive Claude.ai plus a scheduled
  `claude -p` on the same account is the common shape), the
  `last_open=true` shortcut refuses to close another session's
  run and returns a structured `-32095 explicit_run_id_required`
  envelope. Pass the explicit `run_id` if the close is intended.
- **`runs.open` cross-check guidance.** Documented in the
  `status()` field reference: when `runs.open` is populated with
  a `started_by_transport_session_id` different from yours,
  another session sharing this credential is mid-cycle — wait
  rather than start a competing run. The three `started_by_*`
  fields are now exposed on the wire so the check is observable.
- **Structured `-32094 not_found` envelope.** Lookup-by-id misses
  on `memory_update`, `memory_get` single-mode, `output_get`, and
  `output_update` preview now carry `category` + `id` +
  `action_required.kind: "search_or_create"` with a pointer to
  the right search tool. Previously these returned a generic
  `-32000` an LLM had to parse out of the message text.
- **`output_update(preview=true)`.** Mirror of
  `memory_save(preview=true)` — runs validation (slug/folder
  resolution, title/short_description length, target item
  exists) and returns the would-be shape without writing. Useful
  before committing a large rewrite where a slug rename would
  invalidate references.
- **`memory_types()` carries an `origin` field.** `"explicit"`
  (deliberate `memory_create_type`), `"auto"` (side-effect of
  `memory_save` with a new memory_type), or `"system"`
  (predefined). Replaces the `mcp_client:` vs `mcp_auto_custom:`
  prefix split on `created_by`, which is now uniform across both
  custom-creation paths.
- **Single/batch response symmetry.** `memory_delete(id=…)` and
  `memory_save(content=…)` now additively emit the same
  structured fields their batch siblings produce (`results: [<row>]`,
  `deleted_count` / `stored_count`, `total_items`,
  `batch_result` envelope). One parser regardless of how many
  items were passed.

### Fixed

- **`status().you_are.client_name` no longer drifts during a
  session.** With concurrent sessions on one credential, the
  field used to reflect whichever session most recently
  registered — leading to self-misattribution in run logs. Now
  pinned to the calling session's live `clientInfo`.
- **Envelope URLs are absolute.** `action_required.url` on every
  envelope (locks, premium gates, agent_os_not_enabled) now
  carries the full host so an LLM can render a clickable link
  without combining with `status().links.app_home`.
- **`memory_search` result `type` heals on read.** Older records
  that returned `type: "memory_item"` (generic placeholder) now
  always come back with the derived short form (`"work"`,
  `"requests"`, etc.) — no data migration needed.
- **Three tool annotation bugs.** `agent_run` was marked
  `readOnlyHint: true` despite writing a RunRecord on every
  non-preview call; `execute_method` was marked
  `destructiveHint: false` despite its own description warning
  peer methods "may be irreversible"; `memory_delete_type` was
  marked `idempotentHint: false` while every other delete tool
  correctly says it is. All three corrected to the audited values
  so MCP-host safety affordances align with what the tools
  actually do.

## [2.0.13] — 2026-05-27

Round-8 evaluation follow-ups. Skill bump forces MCP host
schema-cache invalidation after the `memory_search` result-schema
normalisation and the new `memory_save` duplicate envelope.

### Added

- **`status().peers` block.** Two counts let the agent decide
  whether to ask about shared memory without triggering the
  `list_connections` approval gate: `total_active` (within the
  30-day recency window matching `list_connections`) and
  `total_active_today` (since UTC midnight). `recency_window_days`
  echoes the window for transparency.
- **Memory duplicate-detection envelope: `existing_id` + `action_required`.**
  When `memory_save` blocks a near-duplicate (similarity ≥ ~0.88),
  the error envelope now carries a flat `existing_id` and
  `action_required.kind: "use_existing_or_update"` pointing the
  agent at `memory_update` as recovery. Mirrors the `slug_exists`
  envelope on outputs. New JSON-RPC outer code `-32096`
  (`duplicate_memory`) lets clients dispatch on duplicate-vs-other
  failures without parsing the message.
- **`output_search` empty-result hint.** When no results, the
  response includes `hint` and `excluded_categories: ["log"]` so
  the agent doesn't conclude "no logs exist" — pointing at
  `output_list(category="log")` as the right tool. Mirrors the
  empty-hint pattern landed for `memory_search` in 2.0.12.

### Changed

- **`memory_search` result schema is now consistent across items.**
  Every result item carries the same keys regardless of vintage or
  code path (browse vs enhanced): `id`, `full_id`, `memory_type`,
  `type` (short form of memory_type), `short_description`,
  `full_description`, `created_at`, `updated_at`, `importance` —
  `null` where the field isn't populated. The tool description
  documents the schema.
- **`memory_get(id="type:<memory_type>")` works in batch mode.**
  The single-id path already supported the `type:` prefix; the
  batch path silently treated `type` as a memory_type and returned
  *"Access denied to memory type 'type'"*. Batch now matches the
  single-id behaviour.
- **SKILL.md §2 Save Memories — soft duplicate-detection
  documented.** One paragraph explaining the ~0.88 threshold and
  pointing at the new `existing_id` recovery affordance.

### Fixed

- **`memory_delete` no longer leaks embedding vectors.** Previously
  each deleted item carried its full record including the 768-dim
  embedding (~50KB per item × N items, ~250KB on a 5-item cleanup)
  into the LLM's context. Service-layer scrub now strips `embedding`,
  `vector`, and any `*_embedding`/`*_vector` keys before returning.
- **`owned_by_me: True` works for custom memory types created by
  the calling client.** Bug: `MemoryService.get_memory_types()`
  projected metadata into the result dict but dropped `created_by`
  / `created_at`, so `tools/types.py` always saw an empty string
  and `endswith(":peer_id")` returned False. Fixed by propagating
  the fields through the projection.

### Maintenance

- `LATEST_SKILL_VERSION` advertised through `status()`
  bumped to `2.0.13`. Older skills continue to operate against the
  newer server — the nudge is informational.

---

## [2.0.12] — 2026-05-27

Round-7 evaluation follow-ups. Skill bump forces MCP host
schema-cache invalidation after the `instruction_save` schema
enrichment, the `memory_search` empty-response shape change, and
the new `status()` fields.

### Added

- **`status().server_time`** — current ISO-8601 UTC time on every
  call. Also visible in the text view as a `server_time:` line.
- **`agent_run()` preamble** carries a `**Now:** <iso>` line so the
  cycle starts with explicit knowledge of "now" — unblocking
  time-of-day urgency reasoning across the dashboard.
- **`status().your_session_id`** — the calling client's `peer_id`.
  Match it against `list_connections().oauth2_sessions[*].peer_id`
  to identify yourself and skip your own session when scanning for
  concurrent runs.
- **Same-day time-of-day urgency rules** in the default task
  procedures. Items whose deadline is today and includes a time:
  past → promote ⏰ → 🔥; > 60 min out → stay ⏰; within 60 min → ⏰.
- **Artefact Hygiene** (the weekly Memory Hygiene task, extended):
  scans memory bodies for malformed `[<text>](<text>)` wiki links
  and outputs for category drift by shape (logs not in `log:`,
  digests not in `email:`, self-reviews not in `improvement:`,
  slugs containing whitespace).
- **`memory_search` empty-result envelope.** When a query matches
  nothing, the response now carries `query` (echoed), `searched_types`
  (short-form names), and a `hint` string telling the agent how to
  recover. Browse mode (no query) unchanged.
- **`instruction_save` per-parameter descriptions.** Schema parity
  with every other Emm write tool; agents inspecting just the
  schema can now see what `name`, `content`, `short_description`,
  and `tags` mean and what constraints apply.
- **`list_connections` recency filter (30 days).** Both peers and
  OAuth2 sessions are filtered by default to entries that have
  authenticated in the last 30 days. Each entry now also carries
  `last_connected_at`. New optional `include_stale: true` to bypass
  (audit / cleanup queries). Response envelope gains
  `recency_window_days`, `stale_filtered_count`, and `include_stale`
  so the agent can see the cleanup opportunity.

### Changed

- **`tools_recommended` reframed as a contract, not a directive.**
  References to driving the LLM's MCP loader (`tool_search(...)`)
  removed from SKILL.md, the `agents` brief, and tool descriptions.
  The field now publishes "the tools this skill assumes will be
  available"; the agent's platform decides how to load them.
- **SKILL.md ↔ `how_to_use()` role split** named in both surfaces:
  skill is the *authoritative reference*, `how_to_use()` is a
  *personalised account snapshot + first-call recipes*.
- **`memory_shopping` emoji** 🛑 → 🛍️ (was a stop sign).

### Fixed

- `[<text>](<text>)`-shaped malformed wiki-link detection ships as
  part of Artefact Hygiene (recurring prevention; the one-off scrub
  of historical user data is still owner-driven via the new
  `## Pending decisions` items).

### Why

A seventh blind-discovery evaluation surfaced the recurring theme
that the skill had been *prescribing how the LLM loads its tools*
instead of *publishing what tools the skill expects*. This release
draws the line: server publishes the contract; agent's platform
handles loading.

## [2.0.11] — 2026-05-27

Memory wiki-links now work inside output bodies. Until this release
the wiki scheme only supported `output:<category>/<slug>`; references
to memories had to be made in prose. The SPA renderer now also
resolves `memory:<type_name>/<id>` and routes the click to the
canonical `/<actor>/app/memory#<type>-<id>` hash form.

### Added

- **`memory:<type_name>/<id>` wiki-link scheme.** Use the full type
  prefix (e.g. `memory:memory_food/42`) so the link target matches
  the user-visible identifier `memory_food:42` and the canonical
  hash URL. Resolves at click time via the new
  `/{actor_id}/api/memory/_resolve` batch endpoint.
- **Display Rules + Link forms now document both directions.** Memory
  IDs may appear as link text inside output bodies via
  `[memory_food:42](memory:memory_food/42)`, mirroring the existing
  `[email:5](output:email/2026-05-26)` pattern for outputs.

### Why

Memories and outputs both have a canonical SPA route that opens a
single item. There was no good reason the wiki only supported one
of the two — making the asymmetry visible inside Run Logs and the
dashboard, where memory references were stuck in plain prose while
output references were clickable.

## [2.0.10] — 2026-05-27

Replaces the server-too-old check (`min_server_contract_version` +
`contract_version`) with a skill-too-old check the other way:
`status().latest_skill_version` advertises the newest skill the
server knows about. An LLM holding a locally-cached older skill
compares against its frontmatter `version:` and nudges the user to
reinstall.

### Breaking

- **`status().contract_version` removed; `status().latest_skill_version`
  added.** Any client pattern-matching on the old name returns
  `KeyError`. The new field carries semver matching SKILL.md's
  frontmatter `version`.
- **`min_server_contract_version` frontmatter key removed.** The
  server is always at least as new as the latest skill (single
  deployment), so the "server too old for skill" check was dead
  weight. The skill now does the opposite check: "is my cached
  copy older than what the server says is current?"
- **AGENTS.md `contract_version: 2.0.0` frontmatter key removed.**
  Seed version bumped 8 → 9 so installed actors get the upgrade
  nudge via the existing `default_tasks` flow.

### Why

The previous contract-version check assumed two independently-
versioned components (server + skill) that might drift. In
practice this repo ships them as one — the server publishes the
skill, and a release always bumps both. The forward direction
(server-too-old) never fires; only the reverse (skill-cached-and-
stale) matters. The rework removes the dead surface and turns the
SKILL.md `version` and the Python `LATEST_SKILL_VERSION` into a
single source of truth tied together by a CI test.

## [2.0.9] — 2026-05-27

Round-6 LLM evaluation follow-ups — four small skill/description
fixes, a bundle trim for unedited customisation docs, and a clearer
shape for `list_connections` when OAuth2 sessions outnumber peers.
The version bump also forces MCP hosts to invalidate cached
descriptions.

### Bug fixes

- **`tool_search` typo.** The skill referenced `tool_memory_search`
  (collateral damage from the v2.0.8 memory-tool rename) — agents
  following the deferred-loading recipe literally would hit a
  tool-not-found error. Renamed to `tool_search` in both occurrences
  (`tools_recommended` paragraph and the Worked-example block).
- **`memory_types` description for system types** now names the
  current tools (`memory_search` / `memory_get`) for read paths
  instead of the bare `search` / `get` form (also v2.0.8 rename
  collateral).

### Tool descriptions

- **`output_dashboard.created` semantics clarified.** The description
  now explains that `created: true` means "had to seed-create on this
  call" — not "brand-new account". The user can clear the dashboard
  between runs; subsequent calls re-seed.
- **`list_connections` response shape advertised explicitly.** The
  payload now carries `peers` and `oauth2_sessions` as separate
  arrays alongside the merged `connections` (peers first) and adds a
  `kind` field on every entry. The description names the new fields
  so agents can stop pattern-matching the `oauth2_client:` prefix.

### Behaviour

- **Bundle trim for unedited customisation docs.** When the user has
  not edited `personal`, `style`, or `skills` since install, the
  `agent_run` bundle replaces the ~3 KB placeholder body with a
  one-line marker that names the doc and invites the user to fill it
  in. Detection compares an md5 of the actor's stored body against
  the rendered canonical seed; any user edit re-enables the full
  body. Net saving: ~3 K tokens per cycle for a fresh actor.
- **`agent_run(mode="preview")` opening line no longer contradicts
  the preview banner.** "You requested a preview of an agent run"
  replaces "You triggered an agent run" so the body text matches the
  ⚠️ PREVIEW header.

### Skill editorial

- **Custom Categories section collapsed to a pointer.** The full
  guide already lives in `references/custom-categories.md`; the
  inline block has been condensed to the two rules that matter at
  call time (short-form parameters, per-agent isolation) plus a
  load-on-demand pointer. Net: ~10 lines off SKILL.md.

## [2.0.8] — 2026-05-26

Round-5 LLM evaluation follow-ups. Six small, agent-facing fixes the
eval surfaced as real (not cache) inconsistencies between SKILL.md,
the tool descriptions, and the live response shape, **plus two
contract-level changes**: memory-pillar tools renamed with a
`memory_` prefix (hard cut, no aliases), and write tools now emit
MCP-spec `structuredContent` instead of non-standard top-level
extras. The version bump also forces MCP hosts (notably claude.ai)
to invalidate cached tool schemas.

### Breaking

- **Memory tool rename.** `search` → `memory_search`, `save` →
  `memory_save`, `get` → `memory_get`, `update` → `memory_update`,
  `delete` → `memory_delete`, `types` → `memory_types`,
  `create_type` → `memory_create_type`, `delete_type` →
  `memory_delete_type`. Anyone running an older skill (v2.0.7 or
  earlier) against a v2.0.8 server will see "tool not found" on
  every memory call until the skill is reinstalled. Rationale: the
  bare names collide with other MCP servers and don't match the
  existing `output_*` / `instruction_*` namespaces. `status`,
  `how_to_use`, `agent_run`, `agent_run_complete`, `work_on_task`,
  `list_connections`, `describe_method`, `execute_method` are
  unchanged — they cross pillars or have no pillar.

- **Write tools emit `structuredContent`.** `memory_save`,
  `memory_update`, `memory_delete`, `memory_create_type`,
  `memory_delete_type`, `output_create`, `output_update`,
  `output_delete`, `instruction_save`, `instruction_delete` (and
  any future write tool) now place typed result fields under
  `result.structuredContent` instead of at the top of
  `result`. Clients that read `result.id` / `result.stored_item`
  directly will get nothing — switch to
  `result.structuredContent.id`. Spec-compliant with MCP
  2025-06-18. The text content (`result.content[0].text`) is
  unchanged.

### Changed

- **`search` tool description, relevance scale.** The on-the-wire
  description still taught the 0–1 thresholds (`≥0.7` / `0.4–0.7` /
  `<0.4`) and named the field `relevance` after 2.0.7 rewrote the
  SKILL.md side to 0–100 with `relevance_score`. Description now
  matches: `score_scale: "0_to_100"`, >50 / 25–50 / <25 thresholds,
  with an explicit pointer that `output_search` uses a different
  scale.

- **`output_search` tool description, distinct scale call-out.**
  Description now names `score_scale: "rrf_0_to_1"` (rank-fusion,
  typically 0.01–0.05) and tells the agent to rank-order rather than
  threshold-filter. Prevents the cross-scale confusion the eval
  flagged.

- **`how_to_use` instruction listing — short form.** The "Installed
  instructions" block now strips the `instruction_` storage prefix
  before rendering, so the listed names (`agents`, `default_tasks`,
  `personal`) actually match the `instruction_load(name=...)` API.
  The long form was rejected by the loader — two conventions in one
  surface.

- **`how_to_use` mode line — emoji removed.** The "Mode: 🔒 `normal`"
  line read as "writes blocked" while the explanatory text said
  memory/output writes were OK. Replaced with plain text framing in
  both `normal` and `instructions_update` modes.

- **SKILL.md `relevance_score` table now names `score_scale`** and
  adds an explicit note that `output_search` uses a different
  (rank-fusion) scale. Consolidates the score interpretation across
  both surfaces.

- **SKILL.md `work_on_task` section now documents the inside-cycle /
  outside-cycle swap.** The ready-task brief carries different
  step 3 wording depending on whether an `agent_run` cycle is open;
  the skill now points the agent at "follow whichever step 3 the
  brief actually carries; the server picks for you".

### Added

- **`status().tools_recommended` field.** Lists the minimal-set tool
  names a lazy-loading client (Claude.ai with deferred MCP-tool
  loading) should `tool_search` for before substantive work. Memory-
  only actors get `["status", "search", "save"]`; mission-control
  actors get the agent_run / work_on_task / dashboard tools added.
  SKILL.md's Session-check section now references the field so the
  agent uses it without rote knowledge.

### Fixed

- **Memory `search` semantic-only results now carry `full_id`.** The
  keyword path stamped it; the semantic path didn't. Hybrid hits
  inherited `full_id` from the keyword side, but semantic-only hits
  silently dropped it after the merge — leaving agents that iterate
  the result list to reconstruct it manually for non-top results.
  Fixed at the combine site so every result entry has `full_id`
  regardless of `match_type`. Also stamps `score_scale: "0_to_100"`
  on every entry for self-describing scale.

- **`work_on_task` no longer tells the LLM to pause mid-cycle.** When
  invoked inside an open `agent_run` cycle the ready-task brief
  swaps step 3 from "Ask the user 2–3 focused questions" to "Flag
  gaps inline as an `## Open questions` section at the bottom of the
  task output." Resolves the eval's "single-response cycle vs ask
  the user" conflict that surfaced in Run 1.

### Deferred (tracked separately)

- **Bundle-size delta protocol for `agent_run`.** Eval suggested
  `agent_run(mode="full", instruction_versions={...})` so the server
  returns only changed instructions. Worth ~5K tokens on Run 2 of a
  multi-cycle session; most cycles are one-per-session and quick mode
  already trims ~3K. Not pursued.

## [2.0.7] — 2026-05-26

Round-4 LLM evaluation follow-ups. Mix of skill prose changes and
server-side contract narrowings; the version bump also forces MCP
hosts (notably claude.ai) to invalidate the cached tool schema after
`save` and `update` lost the legacy `full_description` parameter.

### Changed

- **Relevance score scale.** SKILL.md §1 now names `relevance_score`
  (0–100) and `match_type` (`keyword` | `semantic` | `hybrid`), matching
  the references file and the actual API. The non-existent `relevance`
  field name and the 0–1 thresholds (`≥0.7` / `0.4–0.7` / `<0.4`) are
  replaced with `>50` / `25–50` / `<25`. The server response no longer
  emits `combined_relevance` (dual scale that confused agents) or
  `search_enhanced` / `keyword_match` / `semantic_match` /
  `keyword_relevance` / `semantic_similarity` / `search_method` /
  `similarity_score` — the contract is `relevance_score` +
  `match_type` plus the existing memory data fields.

- **Error-handling table is now driven by JSON-RPC *outer* code.**
  Round 3 used a single outer code `-32099` for three distinct
  conditions; round 4 splits them: `-32099` = lock-states (instructions
  / memory / outputs / `agent_os_not_enabled` / premium / suspended);
  `-32098` = `system_type_readonly`; `-32097` = `slug_exists`. The
  inner `data.code` is still authoritative for fine-grained handling.

- **`save` / `update` only accept `content` for the body.** The legacy
  `full_description` alias was dropped in 2.0.0 collapse; the schemas
  no longer list it and the server no longer coalesces.

- **Quick-mode `agent_run` bundle trim.** `personal`, `style`, and
  `skills` are skipped in quick mode and replaced with a one-line
  pointer telling the agent how to `instruction_load(...)` them on
  demand. Saves ~3–4K tokens; the `agents` brief (operational rules)
  stays unfiltered.

### Added

- **`list_connections` client-approval gate note.** Some clients
  (notably Claude.ai web UI) gate `list_connections` behind a per-tool
  approval and return the literal string `"No approval received."` on
  denial. The skill now tells the agent to treat that as a client-side
  denial (ask the user to grant the connector permission), not a
  server error.

- **Trust-body-over-preview rule.** SKILL.md §1 and
  `references/memory-best-practices.md` both add: "if
  `short_description` contradicts the body, treat the body as
  canonical." Prevents the inherited-misdiagnosis pattern where two
  agents in the eval flagged a "server bug" off a stale preview.

### Fixed

- **`output_search` no longer silently degrades to keyword-only.**
  Output bodies longer than Cohere's per-text 2048-char limit (every
  dashboard, every email digest, most run logs) used to fail
  embedding generation with a `ValidationException`, leaving the
  sidecar index empty and forcing the search service into keyword-only
  mode without surfacing the cause. The embedding helpers now truncate
  to 2000 chars before calling Bedrock.

- **Search-side `short_description` no longer drifts after task
  re-open / mark-done.** When `work_on_task` marks a task done it
  rewrites the body's first heading line `# Ready: …` → `# Completed:
  …` so the preview matches the body. The context-creator transition
  endpoint, when targeting `completed`, similarly rewrites the heading
  and writes a "Done:" short_description (previously it wrote "Ready:"
  regardless of target).

- **`search(query="in <unknown_type>: ...")` distinguishes unknown
  from denied.** Previously both returned the same "Access denied"
  envelope, suggesting to the agent that asking for access would
  help. Now unknown types return `type_not_found` with the list of
  accessible short forms.

- **`save(preview=true)` and batch preview return enough detail to
  verify.** Per-item category short-form, user-supplied or
  "AI-on-commit" short_description placeholder, a 200-char body
  preview, and body length, plus a "re-run without preview" hint in
  the text content.

- **`how_to_use()` no longer prints the deprecated `agent_os_enabled`
  field.** 2.0.0 replaced it with the `pillars_enabled` array via
  `status()`; the snapshot in `how_to_use()` now points readers at
  that.

## [2.0.6] — 2026-05-26

Version-bump-only release driven by the 2026-05-26 round-2 LLM
evaluation: server-side fixes for `agent_run` run-record persistence,
`memory_search` `full_id` field, plus prose tightening in
`list_connections` and `default_tasks`. Skill body is unchanged from
2.0.5 — but bumping the version forces MCP hosts (notably claude.ai)
to invalidate cached tool-schema entries that were re-prompting
approval on `types()`.

### Changed

- **`memory_search` results now include `full_id`** (e.g.
  `memory_food:42`). The v2.0.5 enrichment was added to
  `MemoryService.search_memories` but the live MCP `search` tool
  routes through `memory_search.search_memory_items` (the hybrid
  path), which had not been updated. The skill's Display Rules
  section in `agents` v7 names `full_id` directly as the
  follow-up-call exemplar; it now actually appears in the response.
- **`list_connections` description** distinguishes trusted peer
  connections from OAuth2 client sessions for this account.
  Empty-state responses (peer fields null, `peer_id` of shape
  `oauth2_client:…:mcp_…`) now match the documented contract.

### Fixed

- **`agent_run` runs now persist their RunRecord on first call for
  any actor.** Previously, the first cycle for an actor with no
  `run_records` property list silently failed to persist (the append
  raised `PropertyListNotFoundError` and the exception was caught and
  logged at debug level), leaving `agent_run_complete` to return
  `already_complete: true` and `status().runs.last_completed` to read
  `(none)`. Root-caused to `PropertyListAccessor.append` requiring
  the list to pre-exist; the accessor now lazy-creates so the silent
  swallow in `start_run` is no longer load-bearing — and the swallow
  itself was removed so any future storage error surfaces loudly.
  Resolves the round-1 F5 ("agent_run_complete already-complete on
  first call") and round-2 N2 ("agent_run mints a run_id without
  opening the RunRecord") findings.
- **`default_tasks` v7 → v8** strips the
  `frontend/src/components/EditorModal/dashboard-command-completion.ts`
  path leak from the comment-vocabulary section. The "keep this in
  sync" reminder now references *"the web app's comment-line
  completion palette"* rather than a frontend source path that an
  LLM has no way to access. Eval round-1 F7.

## [2.0.5] — 2026-05-25

Unified follow-up to v2.0.4 covering the 2026-05-24 LLM evaluation
discussion. Requires Emm server v2.0.5+ (frontmatter now declares
`requires_emm_server: ">=2.0.5"`).

### Changed

- **`capabilities()` → `status()` (hard rename).** Older skill
  installs against a v2.0.5 server will see tool-not-found until
  reinstalled. New payload:
  - `mode: "normal" | "instructions_update"` (was `lock_state`).
  - `you_are: {client_name, description}` — caller self-identification.
  - `runs: {open, last_completed}` — peer-LLM coordination signal.
  - `suggested_actions` — only populated when mode is
    `instructions_update`.
  - `links.how_to_use` — pointer to the orientation tool.
  - `your_client_has_only_used_reads` — server detects clients that
    have been connected past a week and never invoked a write tool.
- **Lock-state terminology shifts to "mode".** Tool descriptions,
  `agent_run()` preamble, and SKILL.md now use `mode: normal` /
  `mode: instructions_update` instead of `lock_state: locked/unlocked`.
  Error envelope codes (`memory_write_locked` etc.) unchanged.
- **`how_to_use()` reframed** as the entry point for LLMs *without*
  this skill (skill-equipped clients should keep calling `status()`).
  Tool descriptions explicit about audience.
- **`agent_run_complete()` guidance sharpened.** "Call exactly once
  per cycle; repeated calls (or stale `run_id`s) return
  `already_complete: true` — harmless, don't surface or retry."
- **SKILL.md gained** explicit relevance-score thresholds (≥0.7 strong,
  0.4–0.7 loose, <0.4 noise), a save-after-cycle worked example, and
  a named "Slug-skip guards" section to prevent near-duplicate output
  creates.

### Added

- **`agent_run(mode="quick" | "preview" | "full")`.**
  - `quick` filters tasks to those whose heading ends with `[quick]`
    (e.g. `## 3. Task Check [quick]`); appends a "Likely tools needed"
    footer scoped to the smaller cycle.
  - `preview` returns the same bundle but does NOT mint a run id; no
    RunRecord persisted; the response starts with an unmistakable
    `⚠️ PREVIEW MODE — NOT YET STARTED` header.
  - `full` is the default and matches v2.0.4 behaviour.
- **RunRecord enrichment.** Now carries `started_by_client_id`,
  `started_by_client_description`, and `mode`. The agent_run preamble's
  "Previous run" line surfaces them in markdown-safe code spans
  (XSS-resistant against hostile user-editable descriptions).
- **Resume window 10 → 60 minutes.** Long-running cycles (Daily News
  alone budgets ~10 min) no longer fall outside the window and leave
  zombie in-progress records.
- **Search results carry both `id` (short, for prose) and `full_id`
  (e.g. `memory_food:42`, for tool calls).** No more manual
  `<memory_type>:<id>` reconstruction.
- **`output_dashboard()` returns a JSON-shaped `content` block** with
  the same `{id, url, created}` structured fields the call already had
  at the top level. Easier for LLMs that only read content.

### Removed

- **Silent system-template auto-upgrade.** `agent_run()` no longer
  rewrites installed system instructions. Instead, a 💡 nudge appears
  on the actions dashboard with a link to the Instructions page,
  where the existing diff-and-apply UI handles the upgrade
  explicitly. User stays in the driver's seat.

## [2.0.4] — 2026-05-23

Thread A′ skill-review fixes — addresses ten regressions and contract
mismatches surfaced by the 2026-05-23 external skill review. Pairs with
server-side schema changes (title / short_description as real fields on
outputs, `output_list` slug + recency filters, idempotent
`agent_run_complete`, dotted limits text in `capabilities()`, drop of
`agent_os_enabled` from the response).

### Changed
- `SKILL.md` — Outputs section now teaches `title` and
  `short_description` as **real server fields** on `output_create` /
  `output_update`; the server falls back to body H1 / body slice on
  read only when the LLM omits them. Removed the older "always pass
  `short_description`" framing in favour of pass-both guidance.
- `SKILL.md` Capability Check — dropped the `agent_os_enabled`
  bullet (server no longer returns it); `pillars_enabled` is the sole
  source of truth.
- `SKILL.md` Memory Maintenance — note that `search()` results split
  the id into `id` (integer) and `memory_type`; reconstruct as
  `<memory_type>:<id>` for `get` / `update` / `delete`.
- `SKILL.md` §1 Search — call out browse mode: `search(recency_days)` /
  `search(last_n)` skip `relevance_score` / `match_type` (only present
  on query-driven results).
- `SKILL.md` Tool Prefix — pre-empt the prefix trap. Claude.ai shows
  `Emm AI:` (display), raw MCP registers as `emm:` (the value
  `capabilities().server_prefix` reports), some clients show no
  prefix at all — always read the actual loaded tool list.
- `SKILL.md` Quick Reference — added a row noting that
  `include_remote=true` on `search` requires the once-per-conversation
  user ask.
- `SKILL.md` Agent Runs — note that `agent_run_complete` is
  idempotent: `already_complete: true` means another path closed the
  run; don't surface to the user, don't retry.
- `references/memory-best-practices.md` — fixed the lone surviving
  `search(query="…", memory_type="…")` example to the canonical
  `search(query="in <type>: …")` syntax (`memory_type` is **not** a
  `search` parameter).
- `references/custom-categories.md` — document the three name-shaped
  fields on `types()` (`type_name`, `name`, `id_prefix`) and the
  rule: pass `id_prefix` when calling a tool, `name` for surfacing
  prose, `type_name` for inspecting storage.
- `references/mission-control.md` — updated the Output Mechanics
  guidance to match the new title + short_description contract.
- `hooks/mcp/tools/guide.py` — `how_to_use` tool description reworked
  to match the SKILL.md framing: only call when the user asks how Emm
  is configured, or when account metadata is genuinely needed (use
  `capabilities()` for the lightweight discovery check otherwise).

### Seeds
- `seeds/agent-os-templates/default-tasks.md` bumped to version 4.
  Replaced six `since=<today midnight>` / `since=<N days ago>` calls
  with the supported parameters: `output_list(..., recency_days=N)`
  (parity with `search`), `search(recency_days=N)` for browse mode,
  and exact `slug=` for the lookup paths the new `output_list` schema
  exposes.
- `seeds/agent-os-templates/agents.md` bumped to version 4. Dropped
  the "compare against frontmatter `contract_version`" instruction
  (the schema-wins rule already covers drift) and tightened the
  Outputs section so the agent passes `title` + `short_description`
  by default.

## [2.0.3] — 2026-05-23

Drift sweep across the skill `references/` and the bundled Claude Code
plugin. Aligns both surfaces with the foundation-plan contract that
landed 2026-05-23 (memory short-form only; dedicated `output_dashboard`
tool; explicit `agent_run_complete` closeout). No new behaviour.

### Fixed
- `references/custom-categories.md` — removed two stale "backward
  compatibility" claims about the storage-form memory type
  (`memory_recipes`). The server now rejects the storage form on
  `create_type` / `delete_type` parameters with a -32602 error; the
  reference now matches the rule already stated in SKILL.md §Custom
  Categories.

### Plugin (Claude Code)
- `commands/dashboard.md` — replaced `output_get(category="actions",
  slug="dashboard")` with `output_dashboard()`. The dedicated tool is
  the canonical entry point for the singleton actions dashboard (it
  ensure-creates if missing); the previous flow assumed the dashboard
  already existed.
- `commands/run.md` — added the `agent_run_complete(run_id="<id from
  preamble>")` closeout step that SKILL.md §Agent Runs requires.
  Skipping it leaves a stale "previous run" hint on the server.
- `README.md` — `/emm:memory-delete-type` example switched from
  `memory_recipes` (storage form) to `recipes` (short form) to match
  the contract.
- `.claude-plugin/plugin.json` — bumped from `2.0.0` to track the
  skill version (`2.0.3`); previous bumps to 2.0.1/2.0.2 didn't
  propagate to the plugin manifest.

## [2.0.2] — 2026-05-23

Wave E polish — ten findings from a full end-to-end agent run + skill
read-through. No server changes; behaviour identical, guidance sharper.

### Added
- **Quick Reference** cheat sheet after Three Pillars — maps user intents
  (recommendation, "remember that", "run the cycle", "what's on my list?",
  …) to the first tool call. Subsumes the URL↔MCP table for the most
  common cases.
- **Display Rules** table promoted to its own section near the top.
  Cross-cuts every response: memory IDs never in prose, output IDs as
  link text, internal doc names backstage, unsubstituted
  `{{ACTOR_…_URL}}` tokens never emitted. Attribution cap of 2.
- **Worked examples** section — three short scripts (recommendation
  with attribution, save with rationale, recurring cycle). Anchors
  the abstract rules in concrete tool sequences.
- §Outputs: `output_categories()` mentioned inline ("call before
  minting a new category to avoid near-duplicates") and added to
  the Available Tools inventory.
- §Capability Check: explains `lock_state: "locked"` is the normal
  default — only gates instruction writes; memory/output writes
  proceed. Don't surface the banner unless an actual `-32099`
  comes back from a tool call.
- §Agent Runs: characterises the `agent_run()` bundle as large
  (several thousand tokens); plan context budget accordingly.
- §Agent Runs: clarifies that deferred tool loading (Claude.ai and
  similar) is not a violation of the "single response" mandate —
  `tool_search` round trips are mechanical setup, not a user-facing
  pause.
- §Agent Runs / mission-control.md preamble: explicit rule that the
  `agents` brief is **advisory** and the live tool schema wins when
  they disagree. Tells the LLM to surface drift to the user instead
  of following stale tool names.

### Changed
- Preamble: tool-prefix callout softened — drops the misleading
  `ActingWeb:` / `emm:` example pair (neither matches the current
  Claude.ai default of `Emm AI:`) and just says "use whatever prefix
  appears in your tool list, exactly as it appears".
- Preamble: explicit guidance on when to call `capabilities()` vs
  `how_to_use()` — they overlap; don't call both back-to-back.
- §Available Tools: dropped the redundant tool-prefix callout (was
  stated three times across the bundle; now stated once).
- `references/mission-control.md` preamble: same simplification —
  drops the prefix callout, replaces "always defer to `agents`" with
  the schema-wins rule.

## [2.0.1] — 2026-05-23

Polish pass from a second external LLM review. No behaviour changes, only
documentation contradictions corrected.

### Fixed
- `references/custom-categories.md` — `create_type` and `delete_type` examples
  now use the short form (`recipes`), matching the §Custom Categories rule in
  SKILL.md. Previous examples taught the storage form and would have produced
  inconsistent calls.
- §Outputs link-form rule and `references/mission-control.md` — removed the
  fictitious `outputs_base_url` field name and clarified that the absolute
  app URL appears already-substituted in `agent_run()`'s preamble (the server
  expands an `{{ACTOR_OUTPUTS_URL}}` template into a real URL before sending).
  The LLM should copy the URL as-is rather than looking up a field or trying
  to compose it from parts.

### Changed
- §Memory Maintenance — memory-ID vs output-ID visibility rule promoted to a
  2-row mini-table contrasting "never in prose" (memory) with "yes, as link
  text" (output). Easier to internalise than the previous parenthetical.
- §Custom Categories — the 9 default category names are now listed inline
  (`health`, `travel`, `work`, `food`, `shopping`, `entertainment`, `news`,
  `notes`, `personal`) so the model doesn't burn a `types()` call to recall
  them.
- §Setup — collapsed the dead section header into a one-line cross-reference
  to the setup guide.

## [2.0.0] — 2026-05-22

Major rebrand + scope expansion. Breaking change: ClawHub slug renamed from
`managing-actingweb-memory` to `working-with-emm`. Re-install required.

### Added
- **Capability Check** section at the top of SKILL.md — model detects from its
  own tool list whether mission-control pillars (instructions, outputs, agent
  runs) are enabled or whether to stay in memory-only mode. Surfaces
  `capabilities()` return fields including `contract_version`, `client_id`
  (OAuth identity of the calling MCP connection — useful for per-client
  custom-category visibility), `pillars_enabled`, and `lock_state`.
- Concrete contract-mismatch action: continue working; on a missing feature,
  tell the user *"Your Emm AI server is older than this skill expects —
  update or downgrade"*.
- Pillar-toggle invariant: `outputs` and `instructions` are toggled together;
  if you see one without the other, treat as memory-only and report.
- `references/mission-control.md` — reference card covering outputs, link
  forms, the recurring cycle, dashboard format, run logs, instruction docs,
  and error envelopes. Replaces the deprecated `references/agent-os.md`.
- Coverage of the full Emm AI surface: memory, outputs (the Wiki), standing
  instructions, the recurring agent-run cycle, one-off task drain (via
  `work_on_task`), shared memories, and remote actions.
- §2 Save Memories: explicit **"Don't save"** list (small talk, one-shot
  questions, content already in outputs, momentary moods) — prevents
  over-saving.
- §4 Memory Maintenance: **"Never surface raw memory IDs in prose to the
  user"** rule (mirrors the existing bare `category:id` rule for outputs).
- §1 Search: signpost to `references/mission-control.md#error-handling-during-a-run`
  for tool-error envelopes (auth, network, lock-state -32099).
- §Outputs link form: worked `{{ACTOR_OUTPUTS_URL}}` substitution example
  plus an explicit *"never emit the literal `{{ACTOR_OUTPUTS_URL}}` token"*
  rule.
- §Agent Runs: explicit closeout step — call `agent_run_complete(run_id=…)`
  and append `Last run: <run_id> at <ISO timestamp>` to the dashboard
  Summary. Skipping the close leaves a stale in-progress marker.
- §Available Tools `search()` line: inline reminder that `include_remote=true`
  requires the once-per-conversation user ask.
- §Available Tools `output_search()` line: stated the `log` exclusion
  rationale (append-only audit trail; semantic search would surface noise)
  and the alternative (`output_list(category="log")` + date filter on slug).
- One-off tasks: pointer to `references/task-builder.md` so an LLM
  reading SKILL.md alone knows the wizard exists upstream of
  `work_on_task`.
- Custom Categories: system-managed memory types (e.g. `memory_requests`)
  report `system: true`, `writable: false`, and `owner_tool` in `types()`;
  generic `save` / `update` / `delete` return a `system_type_readonly`
  envelope pointing at the right tool.

### Changed
- Slug `managing-actingweb-memory` → `working-with-emm`.
- ClawHub display name "ActingWeb Memory" → "Working with Emm AI".
- All tool examples use bare names (`search`, `save`, `agent_run`, …) with
  a single preamble explaining that MCP clients prefix them
  (e.g. `ActingWeb:search`, `emm:search`) — use whatever prefix appears in
  the tool list. The server can't know the prefix, so there's no
  `server_prefix` field on `capabilities()`.
- "ActingWeb Task Check" default task renamed to "Task Check" (dropped the
  framework prefix; the cycle step calls `work_on_task` under the hood).
- `references/setup.md` mcporter commands register the server as `emm`.
- Icons renamed: `actingweb-small.svg` → `emm-small.svg`, `actingweb.png` →
  `emm.png`. Brand color and visual identity unchanged.
- `agents/openai.yaml` `display_name` simplified from "ActingWeb Memory" to
  "Emm AI"; MCP dependency value renamed `actingweb` → `emm`.
- SKILL.md `description` trimmed to 775 characters (under the 1024 limit).
- §3 Attribution: tightened to **"never more than two attributions per
  response, even if a dozen memories informed it"**. Internal doc names
  (`personal`, `style`, …) stay backstage — same rule as raw memory IDs.
- Shared memories consent: scoped to **once per conversation**.
  Cross-conversation: ask again next session.
- Output-category guidance: categories are *dynamic* (Emm AI mints new
  categories on first `output_create`), not a fixed list.
- Memory type parameter (`save`, `search`) accepts **short form only**
  (`health`, `food`, …). The storage form `memory_health` is reserved for
  IDs and the `id_prefix` field on `types()`; passing it returns a -32602
  error pointing at the short form.

### Removed
- `SKILL-AGENTOS.md` — the dual-variant approach was replaced by a single
  consolidated SKILL.md that adapts to the user's tool list at runtime.

## [1.0.0] — Initial release

First public release under ClawHub slug `managing-actingweb-memory`. Memory-only
behaviour: search, save, get, update, delete, types, create_type, delete_type,
how_to_use; plus shared-memory access and remote actions through trusted
connections.
