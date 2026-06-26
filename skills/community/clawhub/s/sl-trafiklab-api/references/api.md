# SL Trafiklab API References

## Base URL
All API calls use: `https://transport.integration.sl.se/v1`

No API key is required for this API.

## State Storage (`.sl/preferences.json`)
Preferences are for **autonomous background monitoring only**. The skill can query ANY stop or route on demand without registration.

```json
{
  "favourite_stops": [
    { 
      "id": 9001, 
      "name": "T-Centralen" 
    },
    { 
      "id": 9117, 
      "name": "Odenplan",
      "transport_modes": ["METRO"]
    },
    { 
      "id": 9192, 
      "name": "Gullmarsplan",
      "lines": [4, 66],
      "transport_modes": ["BUS", "METRO"]
    }
  ],
  "favourite_routes": [
    {
      "name": "Work Commute",
      "legs": [
        { 
          "lines": [66], 
          "from": { "id": 1386, "name": "Pokalvägen" }, 
          "to": { "id": 1339, "name": "Södra station" } 
        },
        { 
          "lines": [40, 41], 
          "from": { "id": 9530, "name": "Stockholms södra" }, 
          "to": { "id": 9526, "name": "Flemingsberg" } 
        }
      ]
    }
  ]
}
```

**Field descriptions:**
- `favourite_stops`: Array of stops to monitor autonomously. Each stop can optionally have:
  - `id` (required): Site ID
  - `name` (required): Stop name for display
  - `lines` (optional): Array of line IDs to monitor specifically at this stop
  - `transport_modes` (optional): Filter transports at this stop (`BUS`, `METRO`, `TRAM`, `TRAIN`, `SHIP`, `FERRY`, `TAXI`)
- `favourite_routes`: Array of multi-leg routes for precise deviation monitoring. Each route has:
  - `name` (required): Route name for display
  - `legs` (required): Array of journey segments with `lines`, `from`, and `to` using the same structure as before

*(Note: Allowed `transport_modes` are strictly limited to: `BUS`, `METRO`, `TRAM`, `TRAIN`, `SHIP`, `FERRY`, `TAXI`)*

## API Operations

### 1. `search_sl_sites`
Finds the numeric Site ID for a given stop name. The Departures and Deviations APIs require numeric IDs when searching for specific locations.

**CRITICAL WARNING:** The `/sites` endpoint returns a massive JSON payload containing every stop in Stockholm. NEVER attempt to read the entire response directly into the context window. You MUST pipe the response through `jq` to filter it locally.

```bash
read -r SEARCH_TERM << 'EOF'
T-Centralen
EOF

curl -s "https://transport.integration.sl.se/v1/sites" | \
jq -c --arg st "$SEARCH_TERM" '.[] | select(.name | test($st; "i")) | {id, name}' | head -n 5
```

### 2. `fetch_departures`
Fetch real-time departures from a specific site. **Can be used with ANY site ID** — does not need to be in `favourite_stops`.

**Endpoint:** `GET /sites/{siteId}/departures`

**Parameters:**
- `siteId` (path, required): The site ID to fetch departures from
- `transport` (query, optional): Filter by transport mode (`BUS`, `METRO`, `TRAM`, `TRAIN`, `SHIP`, `FERRY`, `TAXI`)
- `line` (query, optional): Filter by line ID
- `direction` (query, optional): Filter by direction code (1 or 2)
- `forecast` (query, optional): Time window in minutes (default 60, min 5, max 1200)

**Returns:**
- `departures`: Array of upcoming departures (max 3 per line & direction)
- `stop_deviations`: Array of deviations affecting the site

```bash
SITE_ID=9192
LINE_FILTER=4
TRANSPORT_MODE=METRO

# Basic departures fetch (any site)
curl -s "https://transport.integration.sl.se/v1/sites/${SITE_ID}/departures"

# With line filter
curl -s "https://transport.integration.sl.se/v1/sites/${SITE_ID}/departures?line=${LINE_FILTER}"

# With transport mode filter
curl -s "https://transport.integration.sl.se/v1/sites/${SITE_ID}/departures?transport=${TRANSPORT_MODE}"

# Combined filters
curl -s "https://transport.integration.sl.se/v1/sites/${SITE_ID}/departures?line=${LINE_FILTER}&transport=${TRANSPORT_MODE}&forecast=30"
```

**Response format:**
Each departure contains:
- `direction`: Destination name
- `direction_code`: 1 or 2 (back & forth)
- `destination`: Display destination name
- `scheduled`: Officially scheduled departure time
- `expected`: Real-time estimated departure
- `display`: User-friendly formatted time
- `state`: Departure state (`EXPECTED`, `CANCELLED`, `ATSTOP`, etc.)
- `line`: Line info including designation, transport_mode, group_of_lines
- `stop_point`: Stop point details (name, designation)
- `deviations`: Array of deviations for this specific departure

### 3. `fetch_deviations`
Fetches disruption information. **Can be queried for ANY site/line** — favourites are for autonomous monitoring only.
Trafiklab limit: maximum 1 request per minute.

```bash
# FUTURE_FLAG: "false" for active disruptions, "true" for planned maintenance.
# QUERY_PARAMS: Formatted string of sites and lines (e.g., site=9001&line=4&line=18).

curl -s "https://deviations.integration.sl.se/v1/messages?future=${FUTURE_FLAG}&${QUERY_PARAMS}"
```

**Autonomous Filtering for favourite_routes (CRITICAL):**
When processing autonomous checks for `favourite_routes`, analyze the JSON array and extract `message_variants[].header`, `message_variants[].details`, and `scope.stop_areas[]`. Use your analytical capabilities to filter out irrelevant information:
- **Ignore (Silence):** If the disruption text only describes problems at a localized stop (e.g., "stop moved 30 meters", "withdrawn stop", "does not stop at [Stop X]") AND this stop ID does not match any of the boarding, alighting, or transfer Site IDs for that specific leg of the saved `favourite_routes`.
- **Report:** If the disruption affects the entire line generally (e.g., "canceled departures", "diverted traffic affecting total travel time", "vehicle fault", "major delays") OR if it explicitly affects the specific Site IDs the user intends to use.
- For `favourite_stops`, deviations affecting the stop's registered `lines` should be reported.

### 4. `fetch_lines`
List all lines within Region Stockholm, grouped by transport mode.

**Endpoint:** `GET /lines?transport_authority_id={id}`

**Parameters:**
- `transport_authority_id` (query, required): 1 for SL, 8 for UL

```bash
curl -s "https://transport.integration.sl.se/v1/lines?transport_authority_id=1"
```

### 5. `fetch_stop_points`
List all stop points within Region Stockholm.

**Endpoint:** `GET /stop-points`

```bash
curl -s "https://transport.integration.sl.se/v1/stop-points" | head -c 10000
```
