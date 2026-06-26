# Delivery And Audit

Use this reference for Step 5 and Step 6. It defines the exact pre-send
summary, staged audit, formatting, sending, `run_complete`, and
post-send audit contract.

## Final user report

Before formatting, compute:

```text
events_sent = len(city_events_selected) + len(trip_options)
```

Then run:

```bash
python -m weekend_scout prepare-delivery --run-id "<run_id>" \
  --target-weekend "<saturday>" \
  --events-sent <city_count + trip_count>
```

`prepare-delivery` returns machine-readable delivery stats derived from the
same accounting used by `run_complete`. It does **not** log anything.

Build `delivery_stats_lines` as a JSON array of plain strings from
`prepare-delivery.detail`. Keep it concise. Include:

- how many events were found and how many were new vs cached
- discovery budget used: `searches_used/max_searches`, `fetches_used/max_fetches`
- validation budget used: `validation_fetches_used/validation_fetch_limit`
- any cities with zero coverage, especially tier1 cities

If there are no uncovered tier1 cities, omit that line instead of adding a
dummy success note.

## Audit gate

Before `format-message`, always run the pre-send audit:

```bash
python -m weekend_scout audit-run --run-id "<run_id>" --stage pre_send
```

If a required delivery command returns a top-level `error`, report the
human-readable `error`, include the `failure_id`, include any short safe
detail that was returned, and stop the run without inventing a diagnosis.

If `ok: false`, print the audit mismatches and warnings in the agent CLI only
after the normal report. Keep that debug section brief. Do **not** append it
to `preview`, Telegram delivery, or native channel delivery.

The pre-send audit validates prerequisites for delivery content. It does **not**
replace the post-send audit.

## Format-message contract

`format-message` must receive:

- `city-events`: a JSON array of event dicts
- `trips`: a JSON array of trip dicts
- optional `stats-lines`: a JSON array of plain strings to append after the digest
- optional `notes-lines`: a JSON array of plain strings to append after the stats block

`city-events` payload contract:

```text
event_name, location_name, start_date
optional: end_date, time_info, description, source_url, free_entry
```

`trips` payload contract:

```text
name, route, events, timing
optional: url
```

`stats-lines` / `notes-lines` payload contract:

```text
JSON array of plain strings
```

`city-events` example:

```json
[
  {
    "event_name": "Spring Festival",
    "location_name": "Main Square",
    "start_date": "2026-04-04",
    "time_info": "10:00-18:00",
    "description": "Outdoor city festival.",
    "source_url": "https://example.com/event",
    "free_entry": true
  }
]
```

`trips` example:

```json
[
  {
    "name": "Lodz Day Trip",
    "route": "Lodz (130 km, ~1h45)",
    "events": "Spring Fair | Main Square | Sat-Sun all day",
    "timing": "Leave by: 10:00 | Back by: ~20:00",
    "url": "https://example.com/event"
  }
]
```

The `format-message` response returns:

- `written`: HTML file path for Telegram sending
- `preview`: markdown-ish composite report for showing in the conversation or returning through native channel delivery

`preview` is the authoritative user-visible report for this run. It already
includes the normal digest and the stats block. Do **not** reconstruct it
manually from separate pieces.

## Format and send

Before writing delivery payloads, read `references/platform-transport.md`.
Use fresh `_tmp_*.tmp` transport filenames only, for example:

- `_tmp_city_events.tmp`
- `_tmp_trips.tmp`
- `_tmp_delivery_stats.tmp`
- `_tmp_delivery_notes.tmp`

Set `city_events_json_path`, `trips_json_path`, `delivery_stats_json_path`, and
`delivery_notes_json_path` under `cache_dir` from `init-skill`, write the
selected home-city event array, selected trip array, stats lines array, and
notes lines array there, then run:

```bash
python -m weekend_scout format-message \
  --saturday "<saturday>" --sunday "<sunday>" \
  --city-events-file "$city_events_json_path" \
  --trips-file "$trips_json_path" \
  --stats-lines-file "$delivery_stats_json_path" \
  --notes-lines-file "$delivery_notes_json_path" \
  --run-id "<run_id>" \
  [--low-results true]

python -m weekend_scout send --file "<path from written>" --run-id "<run_id>"
```

Use `--low-results true` when `total_events < 3`.

Expected response shape:

```json
{
  "written": ".weekend_scout\\cache\\scout_message.txt",
  "preview": "_Events found: 4 \\(2 new, 2 cached\\)_\n...\n**🗓 Weekend Scout | April 4\\-5, 2026**\n..."
}
```

## Send handling

Always treat the returned `preview` as the authoritative composite report for
the user-facing conversation and channel-delivery fallback.

`send` returning `{"sent": false, "reason": "telegram_not_configured", ...}` is a documented
delivery outcome, not contract drift, as long as the command itself succeeds.

`send` returning `{"sent": false, "reason": "send_failed", ...}` is a documented delivery outcome,
not contract drift, as long as the command itself succeeds.

If `{"sent": true, "reason": "sent", ...}`:

- show the returned `preview` to the user
- if the pre-send audit returned `ok: false`, then print a separate short CLI-only debug section such as `Debug information from audit:` followed by the brief mismatches
- tell the user the composite report was sent to Telegram
- proceed to served marking

If `{"sent": false, "reason": "telegram_not_configured", ...}`:

- do **not** mark served
- show the returned `preview` to the user
- if the pre-send audit returned `ok: false`, then print a separate short CLI-only debug section such as `Debug information from audit:` followed by the brief mismatches
- then tell the user:

```text
python -m weekend_scout config telegram_bot_token YOUR_BOT_TOKEN
python -m weekend_scout config telegram_chat_id YOUR_CHAT_ID
```

If `{"sent": false, "reason": "send_failed", ...}`:

- if `error_code = "telegram_network_blocked"`, handle it as a local execution restriction, not a bad Telegram token/chat configuration
- do **not** mark served
- show the returned `preview` to the user
- if the pre-send audit returned `ok: false`, then print a separate short CLI-only debug section such as `Debug information from audit:` followed by the brief mismatches
- then report the failure briefly using `reason` plus any short returned `error` / `status_code`
- do **not** guess that Telegram is unconfigured unless `reason` says so

## Mark served

If send succeeds:

```bash
python -m weekend_scout cache-mark-served --date "<saturday>" --run-id "<run_id>"
```

Here, `saturday` means the ISO Saturday date from `init-skill`
(`output.config.target_weekend.saturday`), for example `2026-04-04`.

Set:

- `served_marked = true`
- `send_reason = "sent"`

If send failed because Telegram is not configured:

- `served_marked = false`
- `send_reason = "telegram_not_configured"`

If send failed because Telegram sending failed:

- `served_marked = false`
- `send_reason = "send_failed"`
- `run_complete.send_reason` must copy `send.reason`

## Run-complete contract

After the send/no-send outcome is known, always log `run_complete`.

`events_sent` means the number of items selected for the digest:

```text
events_sent = len(city_events_selected) + len(trip_options)
```
It does **not** become zero just because Telegram was unconfigured. Delivery
state is represented by `sent`, `send_reason`, and `served_marked`.

`run_complete` computes fetch accounting from the action log:

- `fetches_used/max_fetches` = discovery fetches from Phases A-C
- `validation_fetches_used/validation_fetch_limit` = verification fetches from Phase D
- `uncovered_tier1` = derived from `run_init.tier1` plus the saved weekend cache

```bash
python -m weekend_scout run-complete --run-id "<run_id>" \
  --target-weekend "<saturday>" \
  --events-sent <city_count + trip_count> \
  --sent <true|false> \
  --send-reason <sent|telegram_not_configured|send_failed> \
  --served-marked <true|false>
```

After `run_complete`, always run the post-send audit:

```bash
python -m weekend_scout audit-run --run-id "<run_id>" --stage post_send
```

If the post-send audit returns a `remediation` object, execute the command in
`remediation.command` exactly as printed, then rerun the audit exactly once.

`audit-run` returning `ok: false` is debug information, not contract drift, as
long as the command itself succeeds. `audit-run` is debug-only by default,
should not block the normal user summary, and does **not** rewrite an already
sent message.

If the post-send audit returns `ok: false`, print a separate short CLI-only debug
section after the normal report. If pre-send audit debug was also printed,
combine both into one short CLI-only debug section with brief labels such as
`Pre-send audit:` and `Post-send audit:`. Do **not** append that debug section to
`preview`, Telegram delivery, or native channel delivery. Do **not** tell the
user to fix the skill, switch modes, or perform maintenance.
