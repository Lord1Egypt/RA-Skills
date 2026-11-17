# Statistics

Read for counts, rankings, response times, retention or view and reaction counters.

Use `tg personal stats chats show <chat> --offline --json` for stored group/channel activity. The online command also
requests joins/leaves; MCP and offline results omit `members`. Incomplete counts are lower bounds.

Rank held data with `tg personal stats messages top` / `tg personal stats contacts top`, using `--measure` or
`--score helpful|active|engaging`. Read coverage, quality and exclusions; unknown snapshots
are not zero and freshness is disclosed per field; legacy observations remain unknown. Pass a row's `selection` to the matching
`stats messages evidence` / `stats contacts evidence` (the `stats.evidence` step); continue with `page.next` and restart
without it if contributing data changed.
Guide: [rankings](https://github.com/WireCatLabs/tg-cli/blob/main/docs/rankings.md).

For questions waiting and selected admin response times, use `stats messages unanswered` and
`stats contacts responses --answerer <person>`. Known-join newcomer help is `stats chats newcomers <chat>`;
viewed posts with little stored discussion are `stats messages discussion`. Inspect graph/archive
quality and use each row’s exact `selection` with `--component report`; missing history/join dates
are not zero. All four reports read stored data; do not infer historical administrator roles.

Retention: `tg personal stats chats retention <chat> --checkpoints 1d,7d,30d --within 7d --json`.
Only a known join date defines cohorts. Report observable denominators, unknown/pending and actual snapshot time.
Partial absence is unknown; checkpoint membership is not continuous survival. Use the cohort row's `selection`
with `stats messages evidence --component report` for bounded member evidence.

Counters: `tg personal stats messages counters show --chat <chat> --counters views,reactions,comments --json`.
Check each field's observedAt/source/freshness (24h default). Refresh is a remote read and local write:
`stats messages counters sync --chat <chat> --max-messages 20 --sync-time 30s --dry-run --json`.
Preview exact targets before refreshing; it never connects. Actual refresh requires write permission and explicit
chat or pinned selection from show; never implicitly refresh account-wide. Missing/unsupported/failed counters
remain explicit. Never send, mark read or increment views. Imported/legacy values have unknown freshness.

## Names in statistics requests

The owner may name a chat or person naturally. Find the chat with `chats list`, the person
with `contacts show` / `contacts list`, or stored authors with `stats contacts top`; use the confirmed ID
in the intended account for the report. If several candidates match, show them and ask the
owner to choose. Never guess an ID or turn an unresolved name into a claim of zero activity.
After a failed lookup, explain which name, @username or account clarification would help.
Counts describe only observed history.

Statistics `--answerer` also accepts stored names, aliases and @usernames directly, without
connecting. Resolve ambiguity using the returned candidates in the intended account; never
guess. `identityKnown: false` with `status: unknown` means the explicit ID was not observed,
so zero answers do not prove zero activity.
