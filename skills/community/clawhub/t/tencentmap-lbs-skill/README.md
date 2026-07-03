---
name: tencentmap-lbs-skill
description: 'Tencent Map Location Services, supporting POI search, route planning, travel planning, nearby search, trajectory data visualization and map data visualization. ⚠️ Mandatory behavior: After this Skill is loaded, the first action must be to check whether a production Key exists (environment variable TMAP_WEBSERVICE_KEY or the user has already provided one in the conversation). If a production Key already exists, proceed to handle the user request directly. If no production Key is found, the Key selection prompt must be displayed immediately (production Key registration guide + temporary trial Key application), then stop and wait for the user to choose. No analysis, file reading, solution planning, or code writing is allowed before the user makes a selection.'
version: 1.0.2
metadata:
  openclaw:
    requires:
      env: TMAP_WEBSERVICE_KEY
      bins:
        - tmap-lbs
    primaryEnv: TMAP_WEBSERVICE_KEY
    install:
      - id: node
        kind: node
        package: '@tencent-map/lbs-skills'
        bins:
          - tmap-lbs
        label: Install tmap-lbs (node)
    homepage: https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
---

# tencentmap-lbs-skill

Tencent Map Location Services provides developers with comprehensive map data services, including nearby search, place search, route planning, travel planning and more.

## Requirements

### tmap-lbs

If tmap-lbs is not installed on first use, please install it first. The same command applies if the user needs to update.

```bash
npm install @tencent-map/lbs-skills -g
```

### Pre-check: API Key

#### Check Steps

1. Check whether a production Key already exists (via `tmap-lbs config get-key`, environment variable `TMAP_WEBSERVICE_KEY`, or the user has already provided one in the conversation)

2. **Case A: Production Key detected**

   Silently record the Key, **proceed directly with the user's original intent, no prompt or interruption needed**.

3. **Case B: No production Key detected**

> ⛔ **Mandatory Interception (Highest Priority)**
>
> When no production Key is detected, **before the user explicitly completes their selection**, the following operations are prohibited:
>
> - Analyzing user requirements
> - Reading any files or documents
> - Planning implementation solutions
> - Writing any code
> - Calling any API
>
> **The first and only step is: immediately output the selection prompt below, then stop and wait for the user's response.**

Output the following content, then **stop and wait for the user's selection**:

> ⚠️ You currently have no production Key configured. Please select your usage method:
>
> **Option 1: Register for a production Key on the official website for complete, stable service**
> 👉 https://lbs.qq.com/dev/console/key/manage
> After registration, you can configure it via:
>
> - Command line: `tmap-lbs config set-key <your-Key>`
> - Environment variable: `export TMAP_WEBSERVICE_KEY=<your-Key>`
>   Or tell me directly in the conversation to configure it.
>
> **Option 2: Apply for a temporary trial Key (no registration required, phone verification only)**
> Quickly obtain a temporary Key via phone verification. Valid for 14 days, covers 30 WebService APIs (PV=5000/day, QPS=5/s).
>
> **Please tell me your choice:**
>
> - Reply "I have a Key" or provide the Key directly → Switch to production mode
> - Reply "Apply for trial Key" → Start the temporary Key application process

After receiving the user's explicit reply, proceed according to the user's choice:

- User provides a production Key → Configure via `tmap-lbs config set-key <key>` or record the Key, switch to production mode, and continue processing the request
- User selects to apply for a trial Key → **Must first read `tempkey-guide.md` for the complete application flow** (display agreement → collect phone → send_code → wait for code → create_key → save_config → persist to `~/.tencentmap/tempkey.json`), strictly follow the steps and error code tables, then configure the obtained Key via `tmap-lbs config set-key <key>`, switch to production mode, and continue processing the request

#### Temporary Key Notes

The temporary Key obtained via the tempkey flow works exactly like a production Key, using the `apis.map.qq.com` production endpoint:

- Valid for 14 days, covers 30 WebService APIs (including electric bicycle route and all other interfaces, no interface restrictions)
- PV=5000/day, QPS=5/s
- Key is persisted in `~/.tencentmap/tempkey.json` and automatically read in subsequent calls
- Re-application is required after expiration

> **Scene 5 (Trajectory Visualization)**: Does not require an API Key. Simply use the `tmap-lbs trail` command; no Key application process is needed.

## Features

- Search
  - Supports keyword and POI search
  - Supports nearby search based on center coordinates and radius
- Planning
  - Travel itinerary planning
  - Route planning (walking, driving, cycling, transit)
- Data Visualization
  - Map data visualization
  - Trajectory data visualization

Use this skill when the user wants to search for addresses, places, nearby information (such as restaurants, hotels, attractions, etc.), or plan routes.

## Trigger Conditions

The user expresses one of the following intents:

- Search for a type of place or a specific place (e.g., "Where is the Forbidden City", "Search for hotels", "Find gas stations")
- Search nearby based on a location (e.g., "Restaurants near Olympic Park", "Gas stations near Beijing West Railway Station")
- Contains keywords like "search", "find", "look up", "nearby", "surrounding", "route", "plan", etc.
- Travel planning (e.g., "Plan a one-day tour of Beijing", "Tour route for West Lake in Hangzhou")
- Route planning (e.g., "How to get from the Forbidden City to Nanluoguxiang", "Plan a cycling route")
- Trajectory visualization (e.g., "Generate a trajectory map for me", "Upload trajectory data", "GPS trajectory display")

## Scene Determination

After receiving a user request, first determine which scene it belongs to:

- **Scene 1**: The user searches for a type of place **near or around a specific location**, where the input contains both a "location" and a "search category or POI type" (e.g., "Restaurants near Xizhimen", "Hotels near Beijing South Railway Station", "Search for milk tea shops near Asia Financial Tower")
- **Scene 2**: Detailed POI search (using Web Service API)
- **Scene 3**: Route planning
- **Scene 4**: Travel planning
- **Scene 5**: Trajectory visualization (the user provides a trajectory data address and wants to generate a trajectory map)

---

## Scene 1: Location-based Nearby Search

The user wants to search for a type of place **near or around a specific location**. First, the geocoding API is used to obtain the latitude and longitude of that location, then a search link with coordinates is constructed.

> 📖 After matching this scene, **you must first read** `references/scene1-nearby-search.md` for detailed execution steps, API format, complete examples, and reply templates. Follow the steps in the document strictly.

---

## Scene 2: Detailed POI Search

Use Tencent Map tmap-lbs for POI search, supporting keyword search, city restriction, nearby search, and more.

> 📖 For detailed format, parameter descriptions, and response data format, please refer to [references/scene2-poi-search.md](references/scene2-poi-search.md)

---

## Scene 3: Route Planning

Use Tencent Map tmap-lbs for route planning. Supports walking, driving, cycling (bicycle), electric bicycle, transit, and other travel modes.

> 📖 For detailed format, API endpoints for each travel mode, parameter descriptions, and response data format, please refer to [references/scene3-route-planning.md](references/scene3-route-planning.md)

---

## Scene 4: Travel Planning

The user wants to travel to a city, provides multiple attractions they want to visit, and needs an optimal itinerary planned, with optional restaurant and hotel recommendations. First, the geocoding API is used to obtain the latitude and longitude of each attraction, then a travel planning link is constructed.

> 📖 After matching this scene, **you must first read** `references/scene4-travel-planner.md` for detailed execution steps, API format, complete examples, and reply templates. Follow the steps in the document strictly.

---

## Scene 5: Map Data Visualization

When the user has trajectory coordinate data and wants to visualize it as a trajectory map on a map. No API Key is required.

## Trigger Conditions

The user mentions intents like "trajectory", "trajectory map", "trajectory visualization", "GPS trajectory", "exercise trajectory", "driving trajectory", etc., and provides a data address or trajectory data.

> 📖 After matching this scene, **you must first read** `references/scene5-trail-map.md` for detailed URL format, execution steps, complete examples, and reply templates. Follow the steps in the document strictly.

---

## Notes

- **Scene determination is key**: Distinguish whether the user is "directly searching for something", "searching for something near a specific location", "planning a route", or "planning a trip"
- Keywords should be as concise and accurate as possible, extracting what the user truly wants to search for
- Chinese keywords in URLs will be automatically encoded by the browser; no manual encoding is needed
- Tencent Map coordinate format is `latitude,longitude` (Note: latitude comes first, longitude comes second)
- If the API returns a `status` other than `0`, it means the request failed; prompt the user to check whether the address is valid
- Keep your API Key secure and never share it with others

## Documentation References

Detailed operation documents for each scene are stored in the `references/` directory:

| File                                                                       | Description                                                                   |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [references/scene1-nearby-search.md](references/scene1-nearby-search.md)   | Scene 1: Nearby Search — Execution steps, API format, complete examples, reply templates |
| [references/scene2-poi-search.md](references/scene2-poi-search.md)         | Scene 2: Detailed POI Search — Request format, parameter descriptions, response data format |
| [references/scene3-route-planning.md](references/scene3-route-planning.md) | Scene 3: Route Planning — Request format, API endpoints, parameters, and response data description |
| [references/scene4-travel-planner.md](references/scene4-travel-planner.md) | Scene 4: Travel Planning — Usage instructions, feature description            |
| [references/scene5-trail-map.md](references/scene5-trail-map.md)           | Scene 5: Trajectory Visualization — URL format, execution steps, complete examples, reply templates |

---

## Related Links

- [Tencent Location Service](https://lbs.qq.com/)
- [Web Service API Overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
