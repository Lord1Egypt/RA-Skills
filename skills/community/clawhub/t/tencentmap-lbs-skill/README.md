---
name: tencentmap-lbs-skill
description: 'Tencent Map Location Services, supporting POI search, route planning, travel planning, nearby search, trajectory data visualization and map data visualization. ⚠️ Mandatory behavior: After this Skill is loaded, the first action must be to check whether a production Key exists (environment variable TMAP_WEBSERVICE_KEY or the user has already provided one in the conversation). If a production Key already exists, proceed to handle the user request directly. If no production Key is found, the Key selection prompt must be displayed immediately (production Key registration guide + preset trial Key option), then stop and wait for the user to choose. No analysis, file reading, solution planning, or code writing is allowed before the user makes a selection.'
version: 1.0.0
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
> **Recommended: Register for a production Key on the official website for complete, stable service**
> 👉 https://lbs.qq.com/dev/console/key/manage
> After registration, you can configure it via:
>
> - Command line: `tmap-lbs config set-key <your-Key>`
> - Environment variable: `export TMAP_WEBSERVICE_KEY=<your-Key>`
>   Or tell me directly in the conversation to configure it.
>
> ---
>
> Alternatively, you can choose to use the preset trial Key provided by the Tencent Location Service platform (no registration required, use directly).
> Please note the limitations of the Tencent Location Service trial Key:
>
> - Rate limit: Call frequency is limited; throttling will be triggered when exceeded
> - Data stability is average; not recommended for production environments
> - Electric bicycle route and similar interfaces are not available
>
> **Please tell me your choice:**
>
> - Reply "I have a Key" or provide the Key directly → Switch to production mode
> - Reply "Use trial Key" → Continue in restricted mode with Tencent Location Service

After receiving the user's explicit reply, proceed according to the user's choice:

- User provides a production Key → Configure via `tmap-lbs config set-key <key>` or record the Key, switch to production mode, and continue processing the request
- User selects trial Key → Switch to trial mode and continue processing the request (see "Trial Mode Invocation Rules" below)

#### Trial Mode Invocation Rules

**Determining principle: Only interfaces that do not require passing through the user's Key can use trial mode.** Interfaces that require passing the user's Key cannot be supported in trial mode; the user must configure a production Key before calling them.

In trial mode, replace request parameters as follows:

- **Domain**: Replace `https://apis.map.qq.com` with `https://h5gw.map.qq.com`
- **Key parameter**: Set `key=none`
- **apptag parameter**: Look up the corresponding apptag value in the mapping table below based on the interface path

> ⚠️ **Trial mode has CORS cross-origin restrictions**
>
> `h5gw.map.qq.com` does not allow direct browser `fetch` (including localhost development environments).
> **Trial mode must use JSONP for invocation**, adding `output=jsonp&callback=functionName` parameters to the request and initiating the request via dynamically inserted `<script>` tags. The Tencent Location Service WebService API natively supports JSONP callbacks.
>
> ```javascript
> // ✅ Trial mode: JSONP method (available in browser)
> function jsonpRequest(url, params, callback) {
>   const cbName = 'tmap_cb_' + Date.now();
>   params.output = 'jsonp';
>   params.callback = cbName;
>   const query = Object.entries(params)
>     .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
>     .join('&');
>   window[cbName] = (data) => {
>     delete window[cbName];
>     script.remove();
>     callback(data);
>   };
>   const script = document.createElement('script');
>   script.src = `${url}?${query}`;
>   document.head.appendChild(script);
> }
>
> // Example: Trial mode geocoding
> jsonpRequest(
>   'https://h5gw.map.qq.com/ws/geocoder/v1',
>   {
>     address: '北京西站',
>     key: 'none',
>     apptag: 'lbs_geocoder',
>   },
>   (res) => console.log(res)
> );
> ```
>
> ❌ **JSONP is not recommended in production Key mode**: JSONP exposes the Key in plain text in frontend code, posing a Key leakage risk. Production Keys should forward requests through the `tmap-lbs` CLI or a **server-side proxy** to avoid direct browser-side calls.

**apptag Mapping Table:**

| Interface Path                 | apptag                   | Corresponding Scenario              |
| ------------------------------ | ------------------------ | ----------------------------------- |
| `/ws/geocoder/v1`             | `lbs_geocoder`           | Scene 1, 4 (Geocoding)             |
| `/ws/place/v1/search`         | `lbsplace_search`        | Scene 1, 2 (POI Search)            |
| `/ws/place/v1/explore`        | `lbsplace_explore`       | Scene 1 (Nearby Search)            |
| `/ws/direction/v1/driving`    | `lbsdirection_driving`   | Scene 3 (Driving Route)            |
| `/ws/direction/v1/walking`    | `lbsdirection_walking`   | Scene 3 (Walking Route)            |
| `/ws/direction/v1/bicycling`  | `lbsdirection_bicycling` | Scene 3 (Cycling Route)            |
| `/ws/direction/v1/transit`    | `lbsdirection_transit`   | Scene 3 (Transit Route)            |

**Interfaces unavailable in trial mode** (these interfaces require passing the user's own Key; trial mode cannot support them):

- `/ws/direction/v1/ebicycling/` (Electric bicycle route)

When a user requests the above unavailable interfaces in trial mode, reply with the following content and stop, waiting for the user's choice:

> ⚠️ The "Electric bicycle route" feature you requested is not available in trial mode. A production Key is required to call this interface.
> Please apply for a production Key on the official website → https://lbs.qq.com/dev/console/key/manage
> After obtaining your Key, let me know and I can switch to production mode to continue.

**After every trial mode API call returns a result, the following reminder must be appended at the end of the reply (must be included every time, cannot be omitted):**

> 📌 Friendly reminder: You are currently using the Tencent Location Service preset trial Key, which has limited data stability and call frequency. It is recommended to apply for a Tencent Location Service production Key as soon as possible → https://lbs.qq.com/dev/console/key/manage

**Scene handling notes for trial mode:**

- **Scene 5 (Trajectory Visualization)**: Does not require an API Key. In trial mode, simply use the `tmap-lbs trail` command as normal; no trial mode HTTP requests are needed.

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
