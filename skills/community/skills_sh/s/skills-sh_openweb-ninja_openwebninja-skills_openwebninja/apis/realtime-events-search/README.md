# realtime-events-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/realtime_events_data.yaml

**Host:** `real-time-events-search.p.rapidapi.com`
**Notes:** Offset-based pagination using 'start' param. Use 'num' param to control results per page (default 10).

## Endpoints

### GET /search-events
Search Events — Search for local public events in real-time. Supports filters and options as available on Google Events (i.e date and online filters).

**Required:**
- `query` (string) — Search query / keyword. Example: `Concerts in San-Francisco`

**Optional:**
- `date` (string, default: any) — values: any, today, tomorrow, week, weekend, next_week, month, next_month
- `is_virtual` (boolean, default: false) Example: `false`
- `start` (integer, default: 0) Example: `0`

**Pagination:** offset (param: `start`)

---

### GET /event-details
Event Details — Get the details of a specific event by Event ID (i.e. *event_id* field of an event).

**Required:**
- `event_id` (string) — The ID of the event to fetch (i.e. event_id field of an event). Example: `L2F1dGhvcml0eS9ob3Jpem9uL2NsdXN0ZXJlZF9ldmVudC8yMDI0LTExLTIyfDE2OTA0Nzc5MjUwNzQwODY5OTc4`

**Pagination:** none

---
