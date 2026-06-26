---
name: robotaxi-tracker
description: Use this skill when the user asks for the latest or current US autonomous vehicle, self-driving car, robotaxi, Tesla, or Waymo vehicle counts, fleet size, city distribution, official fleet numbers, tracker-collected counts, or comparison tables, especially when the data should come from robotaxitracker.com / Robotaxi Tracker. It covers natural requests like "帮我查下最新的美国自动驾驶车辆数量" and provides the workflow to inspect frontend bundles, discover Convex backend queries, separate official-fleet vs tracker-collected metrics, validate city counts and totals, and format compact comparison tables.
---

# Robotaxi Tracker

Use this skill for requests about `robotaxitracker.com`, especially when the user wants:

- latest US autonomous vehicle counts
- current self-driving car / robotaxi counts in the US
- Tesla vs Waymo fleet comparison
- city distribution
- official fleet numbers
- tracker-collected / discovered vehicle counts
- output in a compact table

This skill should also trigger for natural-language requests like:

- 帮我查下最新的美国自动驾驶车辆数量
- 帮我查下最新的美国 robotaxi 数量
- 最新的 Tesla 和 Waymo 车队数量
- 美国自动驾驶车辆城市分布

## Core rules

1. Do not rely on HTML alone. Inspect JS bundles and query the public backend.
2. Do not mix metric types. Separate:
   - official fleet
   - tracker-collected / discovered vehicles
3. Validate:
   - service area count
   - row count in the city table
   - city sum vs chosen aggregate metric
4. If the user requests a final table only, output only the table.
5. Do not assume the first Convex host you find is valid. Test candidate hosts and keep only hosts that return `status: success` for the expected public queries.
6. Do not claim the backend requires authentication unless you have confirmed a direct API response that explicitly indicates auth is required. A `404` or wrong host is not an auth failure.

## Required tools

- `curl`
- `rg`
- `jq`

If network is restricted, switch to a tool or environment that can fetch the site.

## Workflow

### 1. Fetch homepage HTML

```bash
curl -sS https://robotaxitracker.com/ -o /tmp/robotaxi_home.html
```

### 2. Extract and download homepage JS bundles

You must scan all homepage chunks. Do not pick a single chunk by guesswork.

```bash
grep -o '/_next/static/chunks/[^"?]*\.js' /tmp/robotaxi_home.html | sort -u > /tmp/robotaxi_chunks.txt
cat /tmp/robotaxi_chunks.txt
```

```bash
mkdir -p /tmp/robotaxi_js
while read -r u; do
  [ -n "$u" ] || continue
  f=$(basename "$u")
  curl -sS "https://robotaxitracker.com$u" -o "/tmp/robotaxi_js/$f"
done < /tmp/robotaxi_chunks.txt
```

If you have not scanned all chunks listed in `/tmp/robotaxi_chunks.txt`, stop and finish that first.

### 3. Find backend query names and enumerate all candidate hosts

```bash
rg -o 'api\.[A-Za-z0-9_.]+' -n /tmp/robotaxi_js/*.js | sort -u
```

```bash
rg -o '[A-Za-z0-9-]+\.convex\.cloud' -n /tmp/robotaxi_js/*.js | sort -u > /tmp/robotaxi_hosts.txt
cat /tmp/robotaxi_hosts.txt
```

```bash
rg -n 'convex\.cloud|ConvexReactClient' /tmp/robotaxi_js/*.js
```

Look for queries like:

- `api.queries.serviceAreas.list`
- `api.queries.fleet.getHomepageData`
- `api.queries.fleet.getRecentlyAddedCounts`

Known current host notes:

- Prefer `graceful-eel-151.convex.cloud` first. It was verified on 2026-04-10 to return `status: success` for the public queries above.
- `happy-otter-123.convex.cloud` was observed returning `404 Not Found` on 2026-04-10. Treat it as stale or invalid unless re-verified.

Do not stop after finding one host. Enumerate all candidate hosts first.

### 4. Validate all candidate hosts before choosing one

Before using any discovered Convex host for real data extraction, probe every candidate host with a known public query.

```bash
while read -r host; do
  [ -n "$host" ] || continue
  echo "=== $host ==="
  curl -sS "https://$host/api/query"     -H 'Content-Type: application/json'     --data '{"path":"queries/serviceAreas:list","args":[{"provider":"waymo"}]}'
  echo
done < /tmp/robotaxi_hosts.txt
```

Selection rules:

1. You must test every host in `/tmp/robotaxi_hosts.txt` before choosing one, unless the first verified-success host is `graceful-eel-151.convex.cloud`.
2. Choose the first host that clearly returns `{"status":"success", ...}` for the expected public query.
3. If a host returns `404 Not Found`, empty output, HTML, or malformed JSON, treat it as invalid and continue to the next candidate host.
4. Do not describe `404`, empty output, or wrong-host behavior as an authentication requirement.
5. Only describe the backend as auth-protected if the API response explicitly indicates authentication or authorization failure.
6. If `graceful-eel-151.convex.cloud` returns `status: success`, prefer it immediately.

After choosing a host, keep using that same validated host for all subsequent queries in the run.

### 5. Get service areas

```bash
curl -sS https://<convex-host>/api/query \
  -H 'Content-Type: application/json' \
  --data '{"path":"queries/serviceAreas:list","args":[{"provider":"waymo"}]}'
```

Extract rows:

```bash
curl -sS https://<convex-host>/api/query \
  -H 'Content-Type: application/json' \
  --data '{"path":"queries/serviceAreas:list","args":[{"provider":"waymo"}]}' \
  | jq -r '.value[] | [.name,.slug,.id] | @tsv'
```

Repeat for `tesla`.

### 6. Tracker-collected counts

Homepage aggregate:

```bash
curl -sS https://<convex-host>/api/query \
  -H 'Content-Type: application/json' \
  --data '{"path":"queries/fleet:getHomepageData","args":[{"provider":"waymo"}]}'
```

Per city:

```bash
curl -sS https://<convex-host>/api/query \
  -H 'Content-Type: application/json' \
  --data '{"path":"queries/fleet:getHomepageData","args":[{"provider":"waymo","serviceAreaId":"<serviceAreaId>"}]}'
```

Use `.value.totalVehiclesCount` for the per-city tracker count unless the user explicitly asks for another field.

### 7. Official fleet counts

Search bundles:

```bash
rg -n 'getOfficialFleetCount|getTotalOfficialFleet|officialFleet|official fleet' /tmp/robotaxi_js/*.js
```

Important:

- the site may expose official fleet only for some providers
- official total and official city mapping may not cover exactly the same set of cities
- do not infer missing city numbers unless the user explicitly asks for estimation

### 8. Validation

Always check:

1. number of service areas
2. number of city rows in the final table
3. sum of chosen city metric
4. chosen total metric
5. the selected Convex host and whether it returned `status: success` during validation

If totals differ, mention the mismatch only if the user asked for explanation. Otherwise, use the requested metric and keep output compact.

If you cannot produce live data, explain exactly which host was tested, what raw failure happened, and why that failure implies the next step. Never jump directly from a wrong-host response to an authentication conclusion.

## Output defaults

If the user asks for a combined comparison table, use:

| 城市 | Waymo数量 | Tesla数量 |
|---|---:|---:|
| Bay Area | ... | ... |
| Austin | ... | ... |
| 总数量 | ... | ... |

Rules:

1. Put the same city on the same row.
2. Fill missing values with `0`.
3. Add `总数量` as the last row.
4. Do not include extra prose if the user asked for table-only output.

## Common mixed-metric case

If the user says:

- Waymo uses official fleet
- Tesla uses site/tracker data

Then:

1. fetch Waymo official city numbers from frontend-exposed config
2. fetch Tesla tracker city numbers from backend query
3. merge by city
4. output one table only
