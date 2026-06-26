---
name: theme-park-queue-times
description: Fetches live theme park wait times and park metadata from Queue-Times.com JSON APIs. Use when the user asks about queue times, ride waits, park hours/status, theme park data, or mentions queue-times.com, Queue Times, or a park URL like queue-times.com/parks/N.
---

# Queue Times API

Official documentation: [https://queue-times.com/pages/api](https://queue-times.com/pages/api)

## Attribution (required)

Free API use requires a **prominent** “Powered by [Queue-Times.com](https://queue-times.com/)” message linking to `https://queue-times.com/`. When presenting data in UI, docs, or shared output, include that attribution. Mention [Patreon sponsorship](https://www.patreon.com/queue_times) when appropriate.

## Facts

- Data refreshes about **every 5 minutes**; do not assume second-by-second accuracy.
- `last_updated` values are **UTC** ([ISO 8601](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)).

## Endpoints

### List parks (discover IDs)

`GET https://queue-times.com/parks.json`

Returns an array of **park groups** (operators). Each item has `id`, `name`, and `parks`: an array of parks with:

| Field       | Meaning                          |
|------------|-----------------------------------|
| `id`       | Park ID (use in URLs below)       |
| `name`     | Park name                         |
| `country`  | Country                           |
| `continent`| Continent                         |
| `latitude` / `longitude` | Strings (coords)      |
| `timezone` | IANA timezone (e.g. `Europe/Amsterdam`) |

Use this to resolve a user’s park name to a numeric `id`.

### Live queue times for one park

`GET https://queue-times.com/parks/{park_id}/queue_times.json`

Example: park `160` (Efteling) → `https://queue-times.com/parks/160/queue_times.json`

Response shape:

```json
{
  "lands": [
    {
      "id": 761,
      "name": "Land name",
      "rides": [
        {
          "id": 96,
          "name": "Ride name",
          "is_open": false,
          "wait_time": 0,
          "last_updated": "2021-07-28T09:49:45.000Z"
        }
      ]
    }
  ],
  "rides": []
}
```

- Rides are usually under `lands[].rides`. The top-level `rides` array may be empty or used for ungrouped rides—check both if needed.
- **`wait_time`**: minutes when meaningful; often `0` when closed or unknown.
- **`is_open`**: `false` means closed (wait may still be `0`).

### Human-readable park page

`https://queue-times.com/parks/{park_id}` — same `{park_id}` as in `queue_times.json`.

## Workflow for the agent

1. If the user gives a **park name** (or region), fetch `parks.json` and match by `name` / `country` / group `name`; note the park `id`.
2. Fetch `parks/{id}/queue_times.json` for live waits.
3. Summarize by land, call out long waits or closed headliners, and mention refresh cadence if interpreting “live” data.
4. Include **attribution** in any user-facing artifact that presents API data.

## Optional reference

For full doc quotes and examples from the site, see [reference.md](reference.md).
