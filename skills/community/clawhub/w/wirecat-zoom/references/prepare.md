# Preparing for an upcoming meeting

The core rules in [SKILL.md](../SKILL.md) apply. Preparation saves nothing: it does not summarize, accept findings
or create tasks. Use existing Memo workflows for reviewed writes, retaining meeting evidence and preconditions.

## Find the series

Use `zm personal meetings scheduled --limit 20 --json` when the provider series ID is unknown. It reads one Zoom
scheduled inventory page, needs `meeting:read:list_meetings` and network access, and opens no store.

- Titles and old or undated recurring start hints do not prove a future occurrence or complete calendar coverage.
  Preserve `coverage`, then verify a selected `meeting_id` with preparation.
- Continue `item.page.next_cursor` with the returned `item.after`/`item.until` as explicit
  `--since-time`/`--before-time`; cursors bind account and window. Input and output budgets refuse a whole oversized
  page.
- Never auto-select an ambiguous series or treat inventory hints as attendance or occurrence evidence.

## Prepare one series

`zm personal meetings prepare <series-id> --json` takes the exact provider series ID (from `meetings scheduled`),
not an internal stored meeting ID. It reads Zoom's schedule and stored history, requiring `meeting:read:meeting`; it
does not start login, change scopes or import missing text. Default windows look seven days ahead and thirty days
back. Use ISO `--since-time`, `--before-time` and `--history-since-time` for a fixed window; keep the returned
absolute windows when replaying.

- Preserve the candidate / verified-next distinction and all meeting and cue references, fingerprints, stored person
  links, confirmed project links, accepted facts and directly sourced tasks. Past attendees do not establish future
  attendance.
- `related.items` adds cited stored calls outside the series through existing person links or confirmed projects
  shared with included history. Keep its anchor refs and shared-person/project flags. Names and transcript words
  never create links.
- `--meetings` caps each history separately; exact-series evidence has priority within `--bytes`. Inspect related
  lookahead and output-limit flags.
- `knowledge.items` adds cited accepted facts about explicitly linked people and confirmed global projects, including
  decisions outside these meetings. Preserve fact, subject and project refs and association flags; inspect
  `knowledge.coverage.has_more` and `knowledge.coverage.output_limited`. These facts yield bytes to meeting evidence,
  and their source evidence is not revalidated.
- Coverage keeps imported documents, mail, messages and unselected project vocabularies unqueried; without usable
  anchors, related history is unqueried too. Archive completeness stays unknown.
- `notes.items` contains bounded owner notes and annotations about included earlier calls and through explicit
  person or project associations. Retain note refs, meeting, person and project refs, revision and update time.
  Meeting-scoped notes require an included same-account anchor; a shared project alone cannot include another
  meeting's notes. These comments are separate from accepted facts. Inspect `notes.coverage` for lookahead,
  truncation and sources that were not rechecked. Imported or file notes are outside that selection.
- Stored fact evidence is not revalidated. Inspect skipped sources and truncation.

## One selected project

Add `--project <existing-name-key-or-alias>` only for an explicitly selected project.

- Keep `project_evidence.pages` apart from confirmed memberships: each page retains its matched name, references and
  unknown or pending index coverage. Repeated refs across aliases are not independent corroboration.
- At most four pages fit; candidate pages yield bytes before notes and accepted context.
- Use `project_evidence.continuation` with `meetings projects evidence` (over MCP, `zm_read` with that command),
  keeping its frozen project, query, limit and read budget and its non-null cursor; omit a null cursor to restart.
  Do not pass its CLI `command` field as an MCP argument. Empty pages can have continuation.
- This reads existing words without refreshing the index, inferring a project or confirming membership.

## Messages, mail and notes as context

- Only use communications IDs explicitly configured for the selected profile through
  `zm personal config set context.sources`. A grant covers one whole message or mail account or document folder; do
  not broaden scope for an agent. `zm personal config show` reveals the configured selections.
- A document folder uses provider `local` (a plain folder) or `obsidian` (a vault) and account `notes:<folder-id>`
  from `memo folders list`.
- `meetings prepare <series-id> --context-source <id> --context-query '<words>'` adds cited literal matches. Repeat
  the source flag as needed. Default communications history is fourteen days before the preparation start; explicit
  time bounds allow at most ninety days.
- Do not infer confirmed project membership or resolve conflicting statements from word matches alone.
- Keep `communications.coverage` with the excerpts, including index state, unknown completeness, read limits and
  per-source continuation.
- Resume `--context-source ID=CURSOR` only with the same query and window; copy the returned coverage window into
  explicit time bounds when continuing a request that used defaults. Restart without the cursor when
  `restart_required` says so.
- Preparation opens an existing compatible database read-only and does not fill missing indexes or import missing
  data.
- Over MCP, call `zm_read` with `command: "meetings prepare"` and the same CLI arguments. The server captures source
  selections at startup; restart it after changing or revoking configuration.
