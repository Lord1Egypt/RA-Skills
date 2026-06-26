---
name: ride-insights
description:
  Local-only skill: fetch ride receipt emails from Gmail via gog, store them in local JSON, send raw receipt JSON/HTML to a loopback OpenClaw Gateway model for structured extraction, load the extracted rides into SQLite, generate ride-behavior insights, and export an anonymized DataHive-ready CSV from Uber, Bolt, Lyft, Yandex, Free Now, Curb, or Via receipts. Use when building a local ride database, auditing ride spending/routes, or exporting a shareable ride report.
metadata: { "openclaw": { "requires": { "bins": [ "gog","python3" ],"env": [ "OPENCLAW_GATEWAY_TOKEN","OPENCLAW_GATEWAY_URL","OPENCLAW_GATEWAY_MODEL" ] },"homepage": "https://clawhub.com" } }
---

# ride-insights

A privacy-first mobility intelligence skill developed by [DataHive AI](https://datahive.ai).

Use this skill to collect ride-sharing receipts from Gmail, extract structured trip data locally, and generate rich
personal insights on spending, habits, repeated routes, likely anchor locations, time-of-day patterns, and more.

You can also share an anonymized data report with DataHive AI to participate in missions and earn
rewards ([missions blog](https://datahive.ai/blog/)).

This skill uses a unique local-processing approach that showcases the real power of OpenClaw: agent intelligence
processes sensitive source data locally and ensures that no raw data is shared externally.

Local-only by design: this skill requires a loopback OpenClaw Gateway and will fail if the Gateway URL points anywhere
else.

Generate an anonymized/shareable CSV version of the ride history when the user wants to upload it to DataHive and earn
points without exposing raw receipt emails or obvious personal identifiers.

## Before you start

- Require `gog` CLI authenticated for the target Gmail account.
- Always run `gog auth list` before fetching, even if the user already named an account.
- If multiple accounts are configured, present explicit choices using the real account emails, e.g.
  `Which account should I use: (A) name1@example.com or (B) name2@example.com?` Do not summarize as "default" or make
  the user infer which accounts exist.
- If exactly one account is configured, use it and mention it briefly.
- Do not assume an account named `default` exists.
- Require a reachable local OpenClaw Gateway.
- Require Gateway auth token available via `OPENCLAW_GATEWAY_TOKEN` or `~/.openclaw/openclaw.json` at
  `gateway.auth.token` (legacy fallback: `gateway.token`).
- If the extractor is configured through env vars, declare and use only these: `OPENCLAW_GATEWAY_TOKEN`,
  `OPENCLAW_GATEWAY_URL`, and `OPENCLAW_GATEWAY_MODEL`.
- Require the Gateway HTTP Responses endpoint to be enabled.
- Ask the user for date scope: all-time, after a date, or between two dates.
- Treat receipt emails as sensitive financial/location data.
- Tell the user that `data/ride-insights/emails.json` stores fetched receipt emails locally and may include full HTML
  receipt content.
- Tell the user that extraction sends the raw per-email JSON payload, including receipt HTML when present, to the local
  Gateway `/v1/responses` endpoint.
- Before extraction, confirm the user is okay sending raw receipt email JSON/HTML to the active local Gateway-backed
  model.
- Always use the local loopback Gateway. If the configured Gateway URL is not local, fail rather than falling back to
  any remote/private host.
- When describing the local-only guarantee, be explicit that only `localhost`, `127.0.0.1`, and `::1` are accepted
  Gateway hosts.

## Outputs

Primary artifacts:

- `data/ride-insights/emails.json` — fetched receipt emails in one JSON array; may include full HTML receipt content
- `data/ride-insights/rides.json` — extracted ride records in one JSON array
- `data/ride-insights/rides.sqlite` — queryable SQLite database containing normalized ride fields plus
  `extracted_ride_json`, but not raw source email JSON

Retention note:

- `emails.json` persists raw fetched receipt content until the user deletes it.
- `rides.json` and `rides.sqlite` persist extracted ride data locally until deleted.
- The anonymized CSV intentionally excludes raw receipt content and direct identifiers, but it is still a derived
  dataset and should be treated as potentially sensitive.

## Pipeline

Run each step in order. Stop and report on failure.

### 1. Initialize DB

```bash
python3 skills/ride-insights/scripts/init_db.py \
  --db ./data/ride-insights/rides.sqlite \
  --schema skills/ride-insights/references/schema_rides.sql
```

### 2. Fetch Gmail receipts into `emails.json`

```bash
python3 skills/ride-insights/scripts/fetch_emails_json.py \
  --account <gmail-account> \
  --after YYYY-MM-DD \
  --before YYYY-MM-DD \
  --max-per-provider 5000 \
  --out ./data/ride-insights/emails.json
```

Notes:

- Omit `--after` / `--before` when not needed.
- Supported provider queries live in `references/provider_queries.json`.
- Current coverage includes Uber, Bolt, Yandex, Lyft, Free Now, Curb, and Via.
- Default processing cap is 50 emails total for the selected interval because Gateway extraction is token-heavy.
- Before extraction, count the fetched emails in `data/ride-insights/emails.json`.
- If the fetched set is 50 emails or fewer, proceed normally.
- If the fetched set is over 50, ask the user whether to process the full count or keep the default cap of 50.
- Unless the user explicitly approves a higher number, process only the first 50 emails.
- Keep the user-facing explanation short and mention that the cap exists to control token usage/cost.

### 3. Extract rides with Gateway `/v1/responses` into `rides.json`

```bash
python3 skills/ride-insights/scripts/extract_rides_gateway.py \
  --emails-json ./data/ride-insights/emails.json \
  --out ./data/ride-insights/rides.json
```

Notes:

- Prefer running the extractor without exporting `OPENCLAW_GATEWAY_TOKEN` when `~/.openclaw/openclaw.json` already
  contains `gateway.auth.token`.
- The extractor also accepts legacy `gateway.token` if present, but `gateway.auth.token` is the expected current config
  path.
- The extractor may also read `OPENCLAW_GATEWAY_URL` and `OPENCLAW_GATEWAY_MODEL`; these should be declared anywhere the
  skill metadata or packaging contract lists env dependencies.

Notes:

- The script iterates one email at a time.
- It sends raw email JSON to the Gateway `/v1/responses` endpoint.
- It refuses any non-local Gateway host for this sensitive data flow and does not provide an override.
- It expects JSON-only output matching the current ride schema.
- It retries failed requests up to 3 times.
- It writes `data/ride-insights/rides.json` after each successful extraction, so progress is checkpointed.
- If `data/ride-insights/rides.json` already exists, it skips emails whose `gmail_message_id` is already present there.
- If rate limits become a problem, re-run with `--delay-ms <n>`.
- Default extraction cap is 50 emails total unless the user explicitly approves processing more for the selected
  interval.
- When applying the default cap, use the fetched emails ordered as written in `data/ride-insights/emails.json` and
  extract only the first 50.

### 4. Insert `rides.json` into SQLite

```bash
python3 skills/ride-insights/scripts/insert_rides_json_sqlite.py \
  --db ./data/ride-insights/rides.sqlite \
  --rides-json ./data/ride-insights/rides.json
```

### 5. Generate ride insights

Do this as an agent action, not a dedicated insights script.

Recommended workflow:

- Prefer `data/ride-insights/rides.json` as the primary source because it preserves the extracted ride objects directly.
- Use `data/ride-insights/rides.sqlite` for lightweight deterministic counts, filters, grouping, and cross-checks.
- Before querying SQLite, inspect the schema with `PRAGMA table_info(rides)` or read
  `skills/ride-insights/references/schema_rides.sql`.
- Base SQL only on confirmed columns from the live DB schema or that schema reference file.
- Feed the ride records plus a compact factual grounding summary into the active Gateway-backed model.
- Ask the model to produce 8-10 short behavioral insights.

Notes:

- Prefer interpretation over aggregation.
- Focus on patterns such as spending habits, repeated addresses, likely anchor locations, repeated routes, commute-like
  behavior, weekday/weekend habits, time-of-day patterns, outliers, and premium ride choices.
- Use `rides.json` for rich per-ride context and `rides.sqlite` for quick factual checks; combine both when useful.
- Keep SQL-derived grounding compact and human-readable; do not turn the output into a raw SQL dump.
- Keep the output compact and human.
- Do not invent labels like home/work unless the repetition strongly supports that wording; otherwise use softer
  phrasing like likely base, recurring destination, or commute-like pattern.

### 6. Export anonymized CSV report

Use the bundled Python exporter when the user asks for an anonymized/shareable ride report.

```bash
python3 skills/ride-insights/scripts/export_anonymized_rides_csv.py \
  --db ./data/ride-insights/rides.sqlite \
  --out ./data/ride-insights/anonymized_rides.csv
```

Export rules:

- Read from SQLite only.
- Include exactly these columns: `provider`, `email_month`, `start_time_15m`, `end_time_15m`, `currency`, `amount`,
  `distance_km`, `duration_min`, `pickup_city`, `pickup_country`, `dropoff_city`, `dropoff_country`.
- Convert `email_date_text` to month-only format like `2025-05`.
- Round `start_time_text` and `end_time_text` upward to the next 15-minute bucket. Exact quarter-hours stay unchanged.
- Export normalized `distance_km` and `duration_min` when available by reading them from `extracted_ride_json`; leave
  blank when unavailable.
- Exclude street addresses, payment method, driver, notes, subject, message id, and any raw extracted JSON from the CSV
  output.
- When the user asks for the anonymized CSV, generate it as a real `.csv` file in the workspace; do not paste inline CSV
  text into chat.
- Save the file to a stable path such as `data/ride-insights/anonymized_rides.csv`.
- To send it to chat, use OpenClaw's outbound media attachment mechanism: include a short text line plus a separate line
  containing exactly `MEDIA:./data/ride-insights/anonymized_rides.csv`.
- Keep the accompanying message very short, e.g.
  `Done — I regenerated the anonymized CSV and attached the updated file.` followed by the `MEDIA:` line.
- Do not paste inline CSV text into chat.
- Saving a local copy is allowed and expected when needed to send the attachment cleanly.

## Constraints

- Use only the scripts bundled in this skill.
- Do not silently switch to direct provider APIs or embedded agent internals.
- Never hallucinate fields; use `null` when unknown.
- Keep addresses and time strings verbatim.
- Keep user-facing output brief: counts, paths, and failures.

## References

- Schema: `skills/ride-insights/references/schema_rides.sql`
- Provider Gmail queries: `skills/ride-insights/references/provider_queries.json`
