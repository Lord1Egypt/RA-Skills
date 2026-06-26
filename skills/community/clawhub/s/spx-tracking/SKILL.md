---
name: spx-tracking
license: MIT
description: 'Query SPX Express shipment tracking by tracking number. Call this skill when the user mentions a tracking number matching the SPX format (CNMY..., SPXMY...), or uses Chinese or English trigger phrases in the context of a delivery: "快递" "物流" "到了吗" "到哪了" "派送" "签收" "发货" "tracking" "delivered" "parcel" "package" "delivery" "shipment". Also invoke for CAINIAO / 菜鸟 / 菜鸟集运 tracking numbers — CAINIAO last-mile in Malaysia uses SPX Express, so the same number is queryable via the SPX API. Do NOT use for J&T, Pos Laju, DHL, FedEx, UPS, or any non-SPX courier. The script calls the public SPX API and returns structured JSON, human-readable text, or a one-line summary.'
metadata: {"openclaw":{"requires":{"anyBins":["python3","python"]}}}
---

# SPX Express Tracking

Query SPX Express (spx.com.my) shipment tracking and return structured results.

## Invocation

```bash
python skills/spx-tracking/scripts/spx_tracking.py <tracking_number> [--format json|text|summary] [--cookie "..."] [--timeout 15]
```

## Arguments

| Argument | Description |
|---|---|
| `tracking_number` | SPX tracking number (format: CNMY..., SPXMY...) |
| `--format` | `json` (default) — structured data; `text` — human-readable; `summary` — one-line status |
| `--cookie` | Browser cookie for authenticated requests (**optional, sensitive** — contains session data, never log or echo to user) |
| `--timeout` | Request timeout in seconds (default: 15) |

## Dependencies

The `run` script auto-creates a venv and installs `requests` on first use. Manual install:
```bash
pip install -r requirements.txt
```

## Output Format Detail

- **`--format json`** (default) — Full JSON. `retcode` is at the top level. Agent checks `retcode == 0` for success; non-zero means API error.
- **`--format text`** — Human-readable sections: status block, timeline, delay analysis, geo route.
- **`--format summary`** — Single-line: `[<tracking_number>] status: <status> | last update: <time> | est. delivery: <min> ~ <max>`.

## Response Schema

| Field | Contents |
|---|---|
| `retcode` | 0 = success; non-zero = API error (check `response.message`) |
| `response` | API-level status message and detail |
| `shipment` | Core info: `tracking_number`, `status`, `receiver_name`, `edd_min`, `edd_max`, `first_event_time`, `last_event_time` |
| `timeline.grouped_events` | Chronological events, deduplicated (use for display) |
| `timeline.raw_events` | All raw events (use for debugging) |
| `geo_route` | Events with GPS: `current_lng`, `current_lat`, `current_full_address` |
| `stay_analysis` | Time between consecutive events (`duration_seconds`) |
| `bottleneck` | The longest stay segment — where the package stalled |

## Intent → Action Mapping

| Observed user intent | Recommended format |
|---|---|
| User provides a SPX tracking number (CNMY..., SPXMY...) | `--format summary` → one-liner reply |
| "快递到哪了" / "where is my package" / "parcel status" | `--format json` → `status` + `last_event_time` + last location |
| "预计什么时候到" / "when will it arrive" / "ETA" | `--format json` → `edd_min` ~ `edd_max` |
| "快递卡住了" / "is it stuck" / "delay" | `--format json` → `bottleneck` section |
| "完整物流" / "full details" / "tracking history" | `--format text` → full human-readable report |

## Usage Constraints

- **SPX Express (spx.com.my) and CAINIAO (菜鸟 / 菜鸟集运)**: This skill covers both SPX Direct and CAINIAO Smart Logistics tracking numbers used in the Malaysia region. CAINIAO's last-mile carrier in Malaysia is SPX Express, so CAINIAO numbers are queryable via this same API.
- **Tracking number format**: SPX numbers start with `CNMY` or `SPXMY`. CAINIAO numbers may have different prefixes but can be searched directly if the user identifies them as CAINIAO/菜鸟/菜鸟集运.
- **Do NOT use for**: J&T, Pos Laju, DHL, FedEx, UPS, Ninja Van, or any other courier.
- **Privacy**: Never output the raw API response body. Only use the structured fields described above.
