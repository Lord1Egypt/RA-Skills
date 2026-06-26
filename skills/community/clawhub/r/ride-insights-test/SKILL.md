---
name: ride-receipts-gateway-llm
description: Build a local SQLite ride-history database from Gmail ride receipt emails using gog for fetch and OpenClaw Gateway /v1/responses for extraction. Use when you want a portable Gateway-based pipeline that fetches taxi receipts into emails.json, iterates through each email with the Gateway-backed LLM, writes rides.json, and inserts the results into SQLite.
metadata:
  openclaw:
    requires:
      bins:
        - gog
        - python3
      config:
        - gateway.port
        - gateway.auth.token
        - gateway.http.endpoints.responses.enabled
---

# ride-receipts-gateway-llm

Build a ride-receipt pipeline that fetches Gmail receipts into one `emails.json` file, sends each email to the local OpenClaw Gateway `/v1/responses` endpoint for structured extraction, writes one `rides.json` array, and inserts the result into SQLite.

## Before you start

- Require `gog` CLI authenticated for the target Gmail account.
- Always run `gog auth list` before fetching, even if the user already named an account.
- If multiple accounts are configured, present explicit choices using the real account emails, e.g. `Which account should I use: (A) name1@example.com or (B) name2@example.com?` Do not summarize as "default" or make the user infer which accounts exist.
- If exactly one account is configured, use it and mention it briefly.
- Do not assume an account named `default` exists.
- Require a reachable local OpenClaw Gateway.
- Require Gateway auth token available via `OPENCLAW_GATEWAY_TOKEN` or `~/.openclaw/openclaw.json`.
- Require the Gateway HTTP Responses endpoint to be enabled.
- Ask the user for date scope: all-time, after a date, or between two dates.
- Treat receipt emails as sensitive financial/location data.
- Tell the user that `emails.json` stores fetched receipt emails locally and may include full HTML receipt content.
- Before extraction, confirm the user is okay sending raw receipt email JSON/HTML to the active local/private Gateway-backed model.
- Prefer loopback or private Gateway targets. Only use a non-local Gateway when the user explicitly accepts that data flow.

## Outputs

Primary artifacts:
- `data/gateway-llm/emails.json` — fetched receipt emails in one JSON array; may include full HTML receipt content
- `data/gateway-llm/rides.json` — extracted ride records in one JSON array
- `data/gateway-llm/rides.sqlite` — queryable SQLite database containing normalized ride fields plus `extracted_ride_json`, but not raw source email JSON

## Pipeline

Run each step in order. Stop and report on failure.

## Summary and querying

- When summarizing the SQLite output, do not guess schema field names.
- First inspect the actual schema with `PRAGMA table_info(rides)` or read `references/schema_rides.sql`.
- Base SQL queries only on confirmed columns from the live DB schema.
- If the schema and your expected fields differ, adapt the query to the real schema instead of forcing old column names.
- Prefer stable summary dimensions that are explicitly present in the schema, such as `provider`, `email_date_text`, `currency`, `amount`, `pickup_city`, and `dropoff_city`.

### 1. Initialize DB

```bash
python3 skills/ride-receipts-gateway-llm/scripts/init_db.py \
  --db ./data/gateway-llm/rides.sqlite \
  --schema skills/ride-receipts-gateway-llm/references/schema_rides.sql
```

### 2. Fetch Gmail receipts into `emails.json`

```bash
python3 skills/ride-receipts-gateway-llm/scripts/fetch_emails_json.py \
  --account <gmail-account> \
  --after YYYY-MM-DD \
  --before YYYY-MM-DD \
  --max-per-provider 5000 \
  --out ./data/gateway-llm/emails.json
```

Notes:
- Omit `--after` / `--before` when not needed.
- Supported provider queries live in `references/provider_queries.json`.
- Current coverage includes Uber, Bolt, Yandex, Lyft, Free Now, Curb, and Via.

### 3. Extract rides with Gateway `/v1/responses` into `rides.json`

```bash
OPENCLAW_GATEWAY_URL=http://127.0.0.1:18789 \
OPENCLAW_GATEWAY_TOKEN=... \
python3 skills/ride-receipts-gateway-llm/scripts/extract_rides_gateway.py \
  --emails-json ./data/gateway-llm/emails.json \
  --out ./data/gateway-llm/rides.json
```

Notes:
- The script iterates one email at a time.
- It sends raw email JSON to the Gateway `/v1/responses` endpoint.
- By default it refuses non-local Gateway hosts for this sensitive data flow; override only with `OPENCLAW_ALLOW_NONLOCAL_GATEWAY=1` when the user explicitly trusts that target.
- It expects JSON-only output matching the current ride schema.
- It retries failed requests up to 3 times.
- It writes `rides.json` after each successful extraction, so progress is checkpointed.
- If `rides.json` already exists, it skips emails whose `gmail_message_id` is already present there.
- If rate limits become a problem, re-run with `--delay-ms <n>`.

### 4. Insert `rides.json` into SQLite

```bash
python3 skills/ride-receipts-gateway-llm/scripts/insert_rides_json_sqlite.py \
  --db ./data/gateway-llm/rides.sqlite \
  --rides-json ./data/gateway-llm/rides.json
```

### 5. Generate a schema-aware summary from SQLite

```bash
python3 skills/ride-receipts-gateway-llm/scripts/summary_rides_sqlite.py \
  --db ./data/gateway-llm/rides.sqlite
```

Notes:
- This script inspects the live `rides` table schema first.
- It chooses available date/amount fields dynamically instead of assuming a fixed schema revision.
- Use this script for provider/month/currency/city summaries to avoid column-name mismatches.

### 6. Generate short ride insights

Do this as an agent action, not a dedicated insights script.

Recommended workflow:
- Read `data/gateway-llm/rides.json` when available because it preserves the extracted ride objects directly.
- Optionally query `data/gateway-llm/rides.sqlite` for a few basic totals if helpful, but do not turn the output into a raw SQL dump.
- Feed the ride records plus a compact factual summary into the active Gateway-backed model.
- Ask the model to produce 8-10 short behavioral insights.

Notes:
- Prefer interpretation over aggregation.
- Focus on patterns such as spending habits, repeated addresses, likely anchor locations, repeated routes, commute-like behavior, weekday/weekend habits, time-of-day patterns, outliers, and premium ride choices.
- Use light factual grounding first (totals, counts, repeated places), then let the model write the final insight bullets.
- Keep the output short and human.
- Do not invent labels like home/work unless the repetition strongly supports that wording; otherwise use softer phrasing like likely base, recurring destination, or commute-like pattern.
- Do not create or rely on dedicated Python insights scripts unless the user later asks for deterministic reporting artifacts.

### 7. Export anonymized CSV report

Use the bundled Python exporter when the user asks for an anonymized/shareable ride report.

```bash
python3 skills/ride-receipts-gateway-llm/scripts/export_anonymized_rides_csv.py \
  --db ./data/gateway-llm/rides.sqlite \
  --out ./data/gateway-llm/anonymized_rides.csv
```

Export rules:
- Read from SQLite only.
- Include exactly these columns: `provider`, `email_month`, `start_time_15m`, `end_time_15m`, `currency`, `amount`, `distance_km`, `duration_min`, `pickup_city`, `pickup_country`, `dropoff_city`, `dropoff_country`.
- Convert `email_date_text` to month-only format like `2025-05`.
- Round `start_time_text` and `end_time_text` upward to the next 15-minute bucket. Exact quarter-hours stay unchanged.
- Export normalized `distance_km` and `duration_min` when available by reading them from `extracted_ride_json`; leave blank when unavailable.
- Exclude street addresses, payment method, driver, notes, subject, message id, and any raw extracted JSON from the CSV output.
- When the user asks for the anonymized CSV, generate it as a real `.csv` file in the workspace; do not paste inline CSV text into chat.
- Save the file to a stable path such as `data/gateway-llm/anonymized_rides.csv`.
- To send it to chat, use OpenClaw's outbound media attachment mechanism: include a short text line plus a separate line containing exactly `MEDIA:./data/gateway-llm/anonymized_rides.csv`.
- Keep the accompanying message very short, e.g. `Done — I regenerated the anonymized CSV and attached the updated file.` followed by the `MEDIA:` line.
- Do not paste inline CSV text into chat.
- Saving a local copy is allowed and expected when needed to send the attachment cleanly.

## Constraints

- Use only the scripts bundled in this skill.
- Do not silently switch to direct provider APIs or embedded agent internals.
- Never hallucinate fields; use `null` when unknown.
- Keep addresses and time strings verbatim.
- Keep user-facing output brief: counts, paths, and failures.

## References

- Schema: `skills/ride-receipts-gateway-llm/references/schema_rides.sql`
- Provider Gmail queries: `skills/ride-receipts-gateway-llm/references/provider_queries.json`
