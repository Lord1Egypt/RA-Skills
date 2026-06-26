# Tier 2 ingest protocol (phone → Wellness Bridge)

This defines the minimal JSON contract a phone-side exporter should POST to the Wellness Bridge.

## Endpoint

- `POST https://<tunnel-host>/ingest`
- Header: `Authorization: Bearer <token>`
- Content-Type: `application/json`

## Minimal required fields

```json
{
  "date": "YYYY-MM-DD",
  "source": "apple_health" | "health_connect",
  "timezone": "IANA/Zone",
  "generated_at": "ISO-8601",
  "activity": {
    "steps": 1234,
    "distance_km": 3.2,
    "active_calories_kcal": 420
  },
  "sleep": {
    "duration_minutes": 440
  },
  "body": {
    "weight_kg": 70.5
  },
  "vitals": {
    "resting_hr_bpm": 52
  }
}
```

Notes:
- Any section/field may be omitted if unavailable.
- Keep values numeric; do not include units in strings.
- The bridge will store the full JSON as-is.

## Example curl

```bash
curl -X POST "https://<tunnel-host>/ingest" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date":"2026-03-13",
    "source":"apple_health",
    "timezone":"Asia/Shanghai",
    "generated_at":"2026-03-13T11:00:00Z",
    "activity":{"steps":8000}
  }'
```
