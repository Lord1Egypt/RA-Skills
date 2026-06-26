# Search Workflow

Use this reference for Step 2 only. It defines the exact discovery contract.
Do **not** inspect package source or call `--help` during a normal run.

## Hard rules

- Execute phases strictly in this order: `A -> B -> C -> D -> save -> cache-query -> score -> format/send`.
- Do **not** perform any `WebSearch` or `WebFetch` after Phase D completes.
- Do **not** call `cache-query` before `save` except in the documented cached-only path.
- Every phase must end with either a `skip` log or a `phase_summary` log before moving on.
- Do not silently abandon tier loops while budget remains; if you stop early, state the reason.
- Do **not** stop early just because some events were found.
- If uncovered tier1 cities remain, continue searching while budget remains.
- If home-city picks are still below `max_city_options` or there are still eligible uncovered cities that could improve trip options, continue into the next eligible city/tier while thresholds allow.
- Tier2 and tier3 are requested on demand. Do **not** preload or infer later-tier city queues from earlier context.

## Event filter

Include:

- open-air festivals (music, food, craft, cultural)
- City Days and town celebrations
- large fairs and markets
- historical reenactments and outdoor spectacles
- street art festivals and performer festivals
- food truck rallies, beer festivals, wine festivals
- outdoor concerts and open-air cinema
- large sporting events with public attendance
- religious festivals and processions

Exclude:

- museum openings, gallery exhibitions
- indoor theater, cinema, opera, and conferences
- small recurring weekly farmers markets
- private corporate events
- ticketed indoor concerts
- religious services

## Cached-only path

If invoked with `--cached-only`:

- This is a skill-invocation mode. Do **not** append `--cached-only` to
  `python -m weekend_scout init` or `python -m weekend_scout init-skill`.
- Do not branch on cache coverage completeness. If cached-only was requested, use this bypass.
- Cached-only bypasses the offline pre-check and discovery Phases A-D.

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "cached_only_requested"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase search --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

Then load the cached weekend rows:

```bash
python -m weekend_scout cache-query --date "<saturday>"
```

Here, `saturday` means `output.config.target_weekend.saturday` in ISO format (`YYYY-MM-DD`),
for example `2026-04-04`.

Then build the Step 3 scoring input:

```bash
python -m weekend_scout prepare-digest --date "<saturday>"
```

Store that helper result as `digest_input` and use only `digest_input` for Step 3.
After this cached-only bypass, continue with the normal Step 3 and Step 5/6 flow.

## Offline pre-check (normal discovery only)

Skip this section entirely when invoked with `--cached-only`.

If `cached_covered_cities` already covers every city in `tier1`, log the skip and proceed
directly to Step 3:

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "all_tier1_cached"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase search --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

## Budget and counters

Budget: up to `max_searches` `WebSearch` calls and up to `max_fetches` discovery `WebFetch`
calls during Phases A-C. Phase D gets a separate fixed validation reserve from
`workflow.phase_d.validation_fetch_limit`. Bash/CLI calls are free.

Initialize before Phase A:

- `searches_used = 0`
- `fetches_used = 0`
- `validation_fetches_used = 0`
- `validation_fetch_limit = workflow.phase_d.validation_fetch_limit`

Track usage explicitly:

- Increment `searches_used` after every `WebSearch`.
- Increment `fetches_used` after every discovery `WebFetch` in Phases B/C.
- Increment `validation_fetches_used` after every verification `WebFetch` in Phase D.
- Keep only the current action's event payload in memory. The CLI owns the canonical run-level candidate set.
- Before any `WebSearch`, stop if `searches_used >= max_searches`.
- Before any discovery `WebFetch`, stop if `fetches_used >= max_fetches`.
- Before any verification `WebFetch`, stop if `validation_fetches_used >= validation_fetch_limit`.

Before every `WebSearch` or `WebFetch`, show the user a short progress line with:

- phase
- action type
- only the budget counter relevant to the pending action
- the exact query or URL about to be used

### Status line templates

Use these templates verbatim. Substitute the actual counters and query/URL values,
and do **not** add extra prose on the same line.

The counter shown in a status line is always the current pre-action counter.
Increment only after the matching web tool call completes. The next status line
must use the incremented value.

- `SEARCH STATUS`

```text
STATUS phase=<A|C> action=WebSearch searches=<searches_used>/<max_searches> target="<query>"
```

- `DISCOVERY FETCH STATUS`

```text
STATUS phase=<B|C> action=WebFetch fetches=<fetches_used>/<max_fetches> target="<url>"
```

- `VALIDATION FETCH STATUS`

```text
STATUS phase=D action=WebFetch validation_fetches=<validation_fetches_used>/<validation_fetch_limit> target="<url>"
```

Budget allocation guidance:

```text
Phase A (broad): up to 5 searches
Phase A+B combined: up to 6 discovery fetches total
Phase C (per-city):
  tier1: up to 2 searches + 1 discovery fetch per uncovered tier1 city
  tier2: after tier1, sweep every uncovered tier2 city in emitted order while main search budget remains
  tier3: after tier2, sweep every uncovered tier3 city in emitted order while main search budget remains
Phase D (verification): up to 5 validation fetches from the fixed reserve
```

## SEARCH STEP

For every `WebSearch`, execute this sequence exactly:

Action triplet rule for this step:

- exactly one `SEARCH STATUS` line, emitted only through the platform's local CLI/exec command tool (for example `exec(command="echo 'STATUS ...'")`, `Bash("echo \"STATUS ...\"")`, or equivalent)
- then the matching `WebSearch(query)`
- then the matching `log-search`
- the status line must describe the immediate next web tool call
- `log-search --query` must exactly match the target shown in the immediately preceding status line
- do **not** repeat the status line after the tool call
- do **not** emit another status line or run another web action until that `log-search` succeeds
- never include status lines in the assistant's text response or final delivery

1. Gate on `searches_used >= max_searches`.
2. Show the exact `SEARCH STATUS` line.
3. Execute `WebSearch(query)`.
4. Increment `searches_used`.
5. Keep only relevant outdoor weekend events.
6. Log immediately with `log-search`.
7. Do **not** start another web action until the matching `log-search` succeeds.

Do not batch `log-search` calls at the end of a phase. The `log-search` must succeed before the next `WebSearch` or `WebFetch`.

## FETCH STEP

For every `WebFetch`, execute this sequence exactly:

Action triplet rule for this step:

- exactly one fetch status line, emitted only through the platform's local CLI/exec command tool (for example `exec(command="echo 'STATUS ...'")`, `Bash("echo \"STATUS ...\"")`, or equivalent)
- then the matching `WebFetch(url, prompt)`
- then the matching `log-search`
- the status line must describe the immediate next web tool call
- `log-search --query` must exactly match the target shown in the immediately preceding status line
- do **not** repeat the status line after the tool call
- do **not** change the phase, action type, or target between status and log
- do **not** emit another status line or run another web action until that `log-search` succeeds
- never include status lines in the assistant's text response or final delivery

1. Gate on the correct fetch budget:
   - discovery fetch in Phases B/C: stop if `fetches_used >= max_fetches`
   - verification fetch in Phase D: stop if `validation_fetches_used >= validation_fetch_limit`
2. Show the exact status line for the current fetch type:
   - discovery fetch in Phases B/C: show the exact `DISCOVERY FETCH STATUS` line
   - verification fetch in Phase D: show the exact `VALIDATION FETCH STATUS` line
3. Execute `WebFetch(url, prompt)`.
4. Increment the correct counter:
   - discovery fetch in Phases B/C: increment `fetches_used`
   - verification fetch in Phase D: increment `validation_fetches_used`
5. Keep only relevant outdoor weekend events.
6. Log immediately with `log-search`.
7. Do **not** start another web action until the matching `log-search` succeeds.

Use only `FETCH STEP` for queued page extraction in Phase B and Phase D.

## Log and payload patterns

After every search or fetch, call `log-search`.

- Broad searches must log `cities = [home_city]`.
- Targeted and verification searches/fetches must log `cities = [city_name]` for the city being worked.
- Every `log-search` in the normal run must also include the kept event array for that single action.
- If a kept event has a known event/source URL, include it as `source_url` in that event object.
- Use the best known relevant URL the first time you keep that event. If only a listing or aggregator page URL is known, use that instead of leaving `source_url` blank.
- If a follow-up `WebFetch` fails, keep any earlier known `source_url`. A failed fetch blocks extraction from that page, not URL retention.
- Keep event URLs inside the `log-search --events` payload itself. Do **not** leave them only in scratch notes or a final sources list.

Before writing the cities and events payloads, read `references/platform-transport.md`.
Write a fresh payload file immediately before each `log-search` call. Never reuse a path that may have been auto-deleted by the CLI.
Use a `_tmp_*.tmp` filename for each transport payload in this step, for example `_tmp_cities.tmp`, `_tmp_detail.tmp`, or `_tmp_events.tmp`.
Set `cities_json_path` and `events_json_path` under `cache_dir` from `init-skill`,
write the covered city list JSON array and kept event array there, then run:

`--cities-file` and `--events-file` must point to different files.

```bash
python -m weekend_scout log-search \
  --query "<query_or_url>" --target-weekend "<saturday>" \
  --cities-file "$cities_json_path" \
  --events-file "$events_json_path" \
  --phase <broad|aggregator|targeted|verification> \
  --result-count <N> \
  --run-id "<run_id>"
```

Use `[]` when the action produced no kept events.
When `--events` or `--events-file` is present, `log-search` returns the authoritative
`events_discovered` count from the run session upsert plus the current
`session_candidate_count` and `duplicates_merged`.

Event payloads written to the run session use this schema. Minimal required keys:

```text
event_name, city, start_date
```

Useful optional keys:

```text
confidence, category, free_entry, source_url, source_name,
end_date, time_info, location_name, lat, lon, description, country
```

In practice, `source_url` is expected whenever the current action gives you a URL for a kept event.

## Phase lifecycle and helper success

Start any phase with:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action phase_start \
  --phase <A|B|C|D> --target-weekend "<saturday>"
```

End any completed phase with `phase-summary`, which computes the canonical detail payload from logged discovery actions.

```bash
python -m weekend_scout phase-summary --run-id "<run_id>" --phase <A|B|C|D> --target-weekend "<saturday>"
```

Required Step 2 CLI calls must succeed before discovery continues. If any such call exits non-zero,
returns a top-level `error`, or returns a required-success payload indicating failure, stop the run,
show the human-readable `error` plus the `failure_id`, and stop the run without inventing a
diagnosis. Do **not** repair failed Step 2 state by retroactive logging or manual payload
synthesis.

## Phase A: Broad sweep

Use `workflow.phase_a.queries` in the emitted order.

1. Log Phase A start:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action phase_start \
  --phase A --target-weekend "<saturday>"
```

2. If every broad query card is already marked `query_already_done`, log `skip` for Phase A and jump to Phase B.

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "all_queries_in_done_q"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase A --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

3. Otherwise, for each broad query card:
   - skip cards already marked `query_already_done`
   - execute `SEARCH STEP` with `phase_label = broad`
   - keep direct event hits immediately
   - queue aggregator URLs for Phase B
4. Show the short Phase A summary to the user.
5. End Phase A with:

```bash
python -m weekend_scout phase-summary --run-id "<run_id>" --phase A --target-weekend "<saturday>"
```

6. After Phase A completes, continue only to Phase B.

## Phase B: Aggregator deep-dive

1. Log Phase B start:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action phase_start \
  --phase B --target-weekend "<saturday>"
```

2. If no aggregator URLs were queued in Phase A, log `skip` for Phase B and jump to Phase C.

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "no_aggregator_urls"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase B --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

3. Otherwise, for each queued aggregator URL, execute `FETCH STEP` with `phase_label = aggregator` and this prompt:

Queued aggregator URL work in Phase B uses the exact `DISCOVERY FETCH STATUS` line.
Every Phase B web action must be `DISCOVERY FETCH STATUS` -> `WebFetch(url, prompt)` -> `log-search --phase aggregator`.
Do **not** run fresh `WebSearch` queries inside Phase B. If a new search seems necessary, defer it to Phase C or Phase D.

> "List ALL outdoor events, festivals, fairs, markets, city days, reenactments, food
> festivals, and street events happening on [DATES] within the area covered by this page.
> For each: event name, city, venue, dates/times, 1-sentence description, free entry or not.
> Exclude: museums, galleries, theaters, cinemas, indoor events, weekly markets."

4. Keep only events within the configured travel scope and useful for this run.
5. Out-of-scope hits may be mentioned as discarded evidence, but must not be saved as usable trip candidates.
6. Phase B is URL-based extraction. Use only `FETCH STEP` for queued page work, not ad hoc substitute search-only flows.
7. Broad or aggregator hits outside the radius do **not** justify ending targeted search if nearby-city coverage is still weak.
8. Show the short Phase B summary to the user.
9. End Phase B with:

```bash
python -m weekend_scout phase-summary --run-id "<run_id>" --phase B --target-weekend "<saturday>"
```

## Phase C: Targeted city searches

Use `workflow.phase_c.tier1` first. Request tier2 and tier3 on demand only after the earlier tier is finished.

Rules:

- Always search each uncovered city individually.
- A city is covered if it has at least one event across `cached_covered_cities` plus Phase A/B/C results.
- Follow the emitted tier order exactly.
- Do **not** skip tier2 or tier3 because coverage looks good elsewhere. Sweep later tiers deterministically while main search budget remains.

1. Log Phase C start:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action phase_start \
  --phase C --target-weekend "<saturday>"
```

2. If all cities in all tiers are already covered, log `skip` for Phase C and jump to Phase D.

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "all_cities_covered"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase C --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

3. Otherwise, search cities in priority order: tier1 first, then tier2, then tier3. Stop only when the main search budget is exhausted or the current tier is fully exhausted.

Tier 1:

- Each tier1 card includes:
  - `query`
  - `retry_query`
  - `query_already_done`
  - `still_uncovered`
  - `retry_on_rerun`
- If `retry_on_rerun = true`, do **not** repeat the already-done base query.
  Use `retry_query` as the first search for that city on this rerun.
- Otherwise use the base `query` first.
- For each tier1 card, execute `SEARCH STEP` with `phase_label = targeted`.
- Targeted searches in Phase C use the exact `SEARCH STATUS` line with `phase=C`.
- If the first targeted search for that city returns nothing useful and `retry_query`
  has not been used yet, run one more `SEARCH STEP` with `retry_query` as the
  deterministic more-specific second variant.
- If a promising URL appears, use at most one targeted `FETCH STEP` with `phase_label = targeted` for that city.
- Any targeted fetch in Phase C uses the exact `DISCOVERY FETCH STATUS` line with `phase=C`.
- Do **not** log a search phrase as an aggregator or verification fetch.
- Do **not** request tier2 until every emitted tier1 card is finished, including
  any required rerun retry where `retry_on_rerun = true`.

Tier 2:

- After tier1, request tier2 batches while `searches_used < max_searches`.
- Request the next batch explicitly:
```bash
python -m weekend_scout phase-c-cities --run-id "<run_id>" --tier 2 \
  --offset <offset> --limit 6
```
- Use only the returned batch cards.
- Tier2 targeted searches in Phase C use the exact `SEARCH STATUS` line with `phase=C`.
- Any targeted fetch in tier2 uses the exact `DISCOVERY FETCH STATUS` line with `phase=C`.
- Do **not** log a search phrase as an aggregator or verification fetch.
- Finish and log the current batch before requesting the next one.
- If a batch returns `has_more = true` and `searches_used < max_searches`, request the next tier2 batch.
- If the batch returns `has_more = false`, tier2 is exhausted; continue to tier3 if main search budget remains.
- Phase C stays open while tier2 batches run. Do **not** log another `phase_start` for a later-tier batch.
- Do **not** call `phase-summary` between tier batches. Keep Phase C open while you request more cities.

Tier 3:

- After tier2 is exhausted, request tier3 batches while `searches_used < max_searches`.
```bash
python -m weekend_scout phase-c-cities --run-id "<run_id>" --tier 3 \
  --offset <offset> --limit 6
```
- Use only the returned batch cards.
- Tier3 targeted searches in Phase C use the exact `SEARCH STATUS` line with `phase=C`.
- Any targeted fetch in tier3 uses the exact `DISCOVERY FETCH STATUS` line with `phase=C`.
- Do **not** log a search phrase as an aggregator or verification fetch.
- Finish and log the current batch before requesting the next one.
- If a batch returns `has_more = true` and `searches_used < max_searches`, request the next tier3 batch.
- If the batch returns `has_more = false`, tier3 is exhausted.
- Phase C stays open while tier3 batches run. Do **not** log another `phase_start` for a later-tier batch.
- Do **not** call `phase-summary` between tier batches. Keep Phase C open while you request more cities.

After all tiers:

- Show the short Phase C summary to the user.
- End Phase C with:

```bash
python -m weekend_scout phase-summary --run-id "<run_id>" --phase C --target-weekend "<saturday>"
```

- Do not start Phase D until Phase C ends with `phase-summary` or `skip`.

## Phase D: Verification

Use the fixed validation reserve from `workflow.phase_d.validation_fetch_limit`.
Do **not** count Phase D fetches against `max_fetches`.

1. Log Phase D start:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action phase_start \
  --phase D --target-weekend "<saturday>"
```

2. If all top candidates are already `confidence: "confirmed"`, log `skip` for Phase D.

Before writing the detail payload, read `references/platform-transport.md`.
Set `detail_json_path` under `cache_dir` from `init-skill`, write
`{"reason": "all_confirmed"}` there, then run:

```bash
python -m weekend_scout log-action --run-id "<run_id>" --action skip \
  --phase D --target-weekend "<saturday>" --detail-file "$detail_json_path"
```

3. Otherwise, load the canonical weekend candidate set:

```bash
python -m weekend_scout session-query --run-id "<run_id>"
```

4. Select the top five most promising unconfirmed candidate events from that CLI-managed session result.
5. For each candidate with a known source URL:
   - verification fetches in Phase D use the exact `VALIDATION FETCH STATUS` line
   - the `VALIDATION FETCH STATUS` line must include `validation_fetches_used/validation_fetch_limit`
   - every Phase D web action must be `VALIDATION FETCH STATUS` -> `WebFetch(url, prompt)` -> `log-search --phase verification`
   - do **not** run fresh `WebSearch` queries inside Phase D
   - do not re-fetch a URL already fetched in this run
   - execute `FETCH STEP` with `phase_label = verification`
   - update `confidence` to `"confirmed"` only when the source matches the timing/details
   - do **not** drop an already known `source_url` just because the verification fetch fails
6. Show the short Phase D summary to the user.
7. End Phase D with:

```bash
python -m weekend_scout phase-summary --run-id "<run_id>" --phase D --target-weekend "<saturday>"
```


After Phase D completes, discovery work is over. Do not return to targeted or broad searching.

## Save after discovery

Save all discovered events once, after discovery is complete.

```bash
python -m weekend_scout save --run-id "<run_id>" --from-session
```

Then load cached rows once with:

```bash
python -m weekend_scout cache-query --date "<saturday>"
```

Then build deterministic scoring input:

```bash
python -m weekend_scout prepare-digest --date "<saturday>"
```

Store that helper result as `digest_input`. Use only `digest_input` for Step 3
scoring and trip building. Do **not** carry raw cache rows forward as scoring
context after `prepare-digest`.
