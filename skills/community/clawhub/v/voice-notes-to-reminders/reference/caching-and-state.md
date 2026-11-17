# Caching, state & idempotency

The poller runs repeatedly (every 30 min + a nightly sweep) and reruns must be safe. This is the
part people get wrong; get it right once here.

## Processed-IDs state (idempotency)

- Keep `state/processed_ids.json` — a set of label/conversation IDs already turned into outputs.
- Before processing a note, check membership; if present, **skip**.
- Only add an ID **after** its outputs (triage line and/or `.ics`) are written. If the run dies
  mid-way, the note is reprocessed next time rather than lost.
- Write the file atomically: write to `state/processed_ids.json.tmp`, then `os.replace()` it
  over the real file, so a crash can't corrupt it.

Suggested shape:

```json
{ "labels": ["id1", "id2"], "nxhub": ["convA"], "last_run_iso": "2026-07-23T14:00:00-04:00" }
```

## The overlapping poll window (do NOT use a hard "since last run" cursor)

Clinic Wi-Fi is flaky: the device LED goes red and **queues recordings**, so notes can arrive
minutes or hours after they were spoken. A strict `created_after = last_run` cursor silently
drops them.

Instead: **always re-scan a generous window** (e.g. the last 24h) and rely on
`processed_ids.json` to skip what's already handled. The cursor optimizes *fetch size*, the
processed-IDs set guarantees *correctness*. Overlap is cheap; missed notes are not.

## Empty transcripts are not "done"

A note can be `"{}"` / null until AI processing finishes. If the transcript is empty:

- Do **not** write outputs, and do **not** add the ID to `processed_ids.json`.
- Leave it for the next poll. It'll be picked up once the transcript populates.

## HTTP caching & conditional requests

- Respect `ETag` / `Last-Modified` when the API returns them: store the `ETag` per endpoint and
  send `If-None-Match` on the next poll; a `304 Not Modified` means "nothing changed" — cheap.
- Do not cache detail responses that were still empty (`"{}"`); you want to re-fetch those.
- Keep a tiny on-disk cache of *label detail* responses you've fully processed if you like, but
  the processed-IDs set already prevents rework — don't over-engineer.

## Rate limits & backoff

- On `429` or `5xx`, back off exponentially with jitter (e.g. 1s, 2s, 4s, 8s, cap ~60s) and
  respect a `Retry-After` header if present. Never hammer in a tight loop.
- Treat a total API outage as a no-op run: log it to `state/run.log` and exit 0 so the scheduler
  simply tries again next cycle. The overlapping window means nothing is lost.

## Run log

Append one line per run to `state/run.log`:

```
2026-07-23T14:00:00-04:00  fetched=12 new=2 empty-skipped=1 events=1 followups=1  ok
2026-07-23T14:30:00-04:00  API unreachable (timeout) — will retry next run
```
