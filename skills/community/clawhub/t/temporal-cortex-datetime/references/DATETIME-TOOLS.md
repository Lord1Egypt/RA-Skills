# Datetime Tools Reference

Complete input/output schemas for the 5 datetime tools. All are pure computation (no external API calls), read-only, and idempotent.

## Tool Annotations

| Tool | `readOnlyHint` | `destructiveHint` | `idempotentHint` | `openWorldHint` |
|------|:-:|:-:|:-:|:-:|
| `get_temporal_context` | true | false | true | false |
| `resolve_datetime` | true | false | true | false |
| `convert_timezone` | true | false | true | false |
| `compute_duration` | true | false | true | false |
| `adjust_timestamp` | true | false | true | false |

All tools are closed-world (no external API calls).

---

## get_temporal_context

**Input:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `timezone` | string | No | IANA timezone override |

**Output:** `utc`, `local`, `timezone`, `timezone_configured`, `utc_offset`, `dst_active`, `dst_next_transition`, `dst_next_offset`, `day_of_week`, `iso_week`, `is_weekday`, `day_of_year`, `week_start`

---

## resolve_datetime

**Input:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `expression` | string | Yes | Human time expression |
| `timezone` | string | No | IANA timezone override |

**Supported expressions:** `"now"`, `"today"`, `"tomorrow"`, `"yesterday"`, `"next Monday"`, `"this Friday"`, `"morning"` (09:00), `"noon"`, `"evening"` (18:00), `"eob"` (17:00), `"2pm"`, `"14:00"`, `"+2h"`, `"-30m"`, `"in 2 hours"`, `"3 days ago"`, `"next Tuesday at 2pm"`, `"tomorrow morning"`, `"start of week"`, `"end of month"`, `"start of next week"`, `"end of last month"`, `"first Monday of March"`, `"third Friday of next month"`, RFC 3339 passthrough.

**Output:** `resolved_utc`, `resolved_local`, `timezone`, `interpretation`

---

## convert_timezone

**Input:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `datetime` | string | Yes | RFC 3339 datetime |
| `target_timezone` | string | Yes | Target IANA timezone |

**Output:** `utc`, `local`, `timezone`, `utc_offset`, `dst_active`

---

## compute_duration

**Input:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `start` | string | Yes | First timestamp (RFC 3339) |
| `end` | string | Yes | Second timestamp (RFC 3339) |

**Output:** `total_seconds`, `days`, `hours`, `minutes`, `seconds`, `human_readable`

---

## adjust_timestamp

**Input:**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `datetime` | string | Yes | RFC 3339 datetime |
| `adjustment` | string | Yes | Duration: `"+2h"`, `"-30m"`, `"+1d2h30m"` |
| `timezone` | string | No | IANA timezone for day-level adjustments |

DST-aware: `"+1d"` across spring-forward maintains same wall-clock time.

**Output:** `original`, `adjusted_utc`, `adjusted_local`, `adjustment_applied`
