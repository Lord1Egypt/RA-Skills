# Sources and credit lines

Always end with: **Camp records: American Adventurer (davelalande.com)** and the record's own link.

Each record names its own source. Read it from the record and credit it. The API root states the site's license: free to use, no key, credit "American Adventurer / davelalande.com". Ask for about two requests a second.

| Source | What it feeds | Credit to give |
|---|---|---|
| US Forest Service (USFS) | National forest camp inventory; recorded fees, seasons and rules from forest pages | "USDA Forest Service" |
| Bureau of Land Management (BLM) | BLM camp records; fee and rule notes read from BLM pages (the record gives the read date) | "Bureau of Land Management" |
| State, county and other agencies | Montana FWP, Bureau of Reclamation and municipal records and stay limits | The agency named in the record's `land_manager` |
| OpenStreetMap | Resupply points (fuel, groceries, water, dump, propane and more) and camp records whose source names OpenStreetMap | "(c) OpenStreetMap contributors" (ODbL 1.0). Required wherever those points or counts appear. A floor, never a survey. |
| USGS National Hydrography Dataset | Nearest named stream or lake and its distance | "USGS National Hydrography Dataset" |
| USGS 3DEP | Slope of the hillside around the pin | "USGS 3DEP" |
| National Weather Service | Forecast, via `/api/weather` | "National Weather Service (weather.gov)", with the read time |
| NIFC | Wildfire incident reports, via `/api/fire` (reports, not perimeters or restrictions) | "National Interagency Fire Center" |
| US Forest Service alerts pages | Orders a national forest posted on its own alerts page, via `posted_orders` (the forest's words, with our read time) | "USDA Forest Service" and the alerts page link the answer gives |
| US Forest Service Motor Vehicle Use Map | The recorded road nearest a camp, via `road_to_camp` | "USDA Forest Service Motor Vehicle Use Map", with the record's own link |
| US DOE Alternative Fuels Data Center | Nearest DC fast charger, snapshot dated in the record | "US DOE AFDC", with the snapshot date |
| USDOT/BTS and US Census | Nearest mapped rail line and primary highway (a mapped line is not a running train) | "USDOT/BTS NARN" and "US Census TIGER/Line" |

Rules of thumb:

- The record date is the build date the API states (its `data_built_at` and the `cite` line). Show it. `aa.py` prints it as `record_date`.
- Where a record carries its own checked date (for example "read 19 Sep 2026" in a `fee_note`), quote that too.
- Weather and fire reads carry their own read time. Show it.
- If you are not sure which source a field came from, say "source named in the record" and link the record. Do not guess a credit.
