---
name: travel-map-generator-skill
description: >-
  Generate illustrated travel itinerary maps in Studio Ghibli/Miyazaki anime style.
  Creates a hand-drawn style map PNG with cartoon POI illustrations placed at real
  geographic coordinates, connected by a numbered route.
  Use when the user mentions travel maps, trip itineraries, illustrated maps, Ghibli maps,
  cartoon travel plans, travel route visualization, hand-drawn maps, anime-style maps,
  or wants to visualize any travel plan on a cute/artistic map. Also trigger when the user
  asks to "draw a map" for a trip, generate an itinerary graphic, or create a visual
  travel guide.
license: MIT
metadata:
  author: Qoder Community
  version: 1.1.0
  created: 2026-04-02
  last_reviewed: 2026-04-02
  review_interval_days: 90
  dependencies:
    - name: Pillow
      type: python-package
      install: pip3 install Pillow
  schema_expectations:
    - file: config.json
      expected_keys:
        - city_name
        - viewport
        - pois
---

# /travel-map-generator — Ghibli Style Travel Map Generator

You are an expert travel map illustrator. Your job is to generate beautiful,
hand-drawn style travel itinerary maps in Studio Ghibli / Hayao Miyazaki aesthetic.

## Trigger

User invokes `/travel-map-generator` followed by their input:

```
/travel-map-generator Create a Ghibli-style map of Tokyo
/travel-map-generator I'm going to Paris, make me a cute illustrated map
/travel-map-generator Draw a travel map for Rome with Colosseum, Vatican, Trevi Fountain
```

Or activate naturally:

```
Make me a travel map for Kyoto
Generate a cartoon itinerary map
I need a hand-drawn map of my trip
```

Generate a single illustrated PNG travel map in Studio Ghibli / Miyazaki style.
The map shows a destination city with cartoon POI icons at real coordinates,
connected by a hand-drawn numbered route.

## Quick Start

Follow the seven-phase workflow below **in order**. Do not skip phases.
Each phase specifies which tools to use and what outputs to produce.

**Prerequisites**: Run the dependency installer first:
```bash
python3 SKILL_DIR/scripts/install_deps.py
```

---

## Phase 1: Setup & Input Gathering

**Goal**: Extract travel info from conversation and prepare the workspace.

1. Parse the conversation to identify:
   - **Destination city** (required)
   - **Specific attractions/POIs** the user mentioned (optional)
   - **Visit order** if the user specified a sequence (optional)
2. If the city is ambiguous (e.g., "Springfield"), ask the user to clarify.
3. Create a temporary workspace:
   ```bash
   mkdir -p /tmp/travel-map-CITY_SLUG
   ```
   Use a URL-safe slug of the city name (e.g., `tokyo`, `new-york`).

**Output**: City name, list of POI names (may be empty), visit order (may be null).

---

## Phase 2: POI Discovery (if needed)

**Goal**: Find top attractions if the user didn't specify any.

Skip this phase if the user already named specific attractions.

1. Use the **WebSearch** tool to find popular attractions:
   ```
   Query: "top attractions things to do in {CITY}"
   ```

2. Extract 5-8 popular attractions from the search results.

3. Present the discovered attractions to the user and confirm before proceeding.

**Output**: Final list of POI names (typically 3-10, ideally 5).

---

## Phase 3: Coordinate Collection

**Goal**: Get the latitude/longitude of each POI.

Use **WebSearch** to find coordinates for each POI:
```
Query: "{POI_NAME} {CITY} coordinates latitude longitude"
```

Or use the **Task tool with `browser-agent`**:
1. Navigate to `https://www.google.com/maps/search/{POI_NAME}+{CITY}`
2. Extract coordinates from the URL format `@{lat},{lng},{zoom}z`

Collect all POI data into a structured list:
```json
[
  {"name": "POI Name", "lat": 35.6586, "lng": 139.7454},
  ...
]
```

**Important**: Record coordinates with at least 4 decimal places for accuracy.

**Output**: List of POIs with name, lat, lng.

---

## Phase 4: Map Background Generation

**Goal**: Generate a map background covering all POIs.

**Option A: Use ImageGen (Recommended)**

Generate an artistic map background directly:
```
ImageGen prompt: "A hand-drawn illustrated bird's-eye-view map of {CITY} in Studio Ghibli watercolor style, showing major streets as soft pencil lines, rivers in gentle blue watercolor, parks in soft green, buildings as tiny charming houses, warm parchment background, Miyazaki aesthetic, no text labels, map only"
Size: 1536x1024
Output: /tmp/travel-map-CITY_SLUG/stylized_map.png
```

**Option B: Google Maps Screenshot + Stylization**

If you need precise geographic accuracy:

1. Compute the optimal viewport:
```bash
python3 -c "
import sys; sys.path.insert(0, 'SKILL_DIR/scripts')
from utils import compute_viewport
pois = POI_LIST_AS_PYTHON
vp = compute_viewport(pois, 1536, 1024)
print(f\"center_lat={vp['center_lat']}, center_lng={vp['center_lng']}, zoom={vp['zoom']}\")
"
```

2. Use **Task tool with `browser-agent`**:
   - Navigate to `https://www.google.com/maps/@{center_lat},{center_lng},{zoom}z`
   - Take screenshot: `/tmp/travel-map-CITY_SLUG/map_screenshot.png`

3. Stylize the screenshot:
```bash
python3 SKILL_DIR/scripts/stylize_map.py \
  --input /tmp/travel-map-CITY_SLUG/map_screenshot.png \
  --output /tmp/travel-map-CITY_SLUG/stylized_map.png
```

**Output**: `stylized_map.png` + viewport metadata dict.

---

## Phase 5: POI Icon Generation

**Goal**: Generate cartoon icons for each POI.

For **each POI**, call the **ImageGen** tool:

- **Name**: `poi_{SLUG}.png` (e.g., `poi_tokyo_tower.png`)
- **Prompt**:
  ```
  A charming Studio Ghibli watercolor illustration of {POI_FULL_NAME} in {CITY},
  Hayao Miyazaki art style, soft warm pastel colors, whimsical and dreamy,
  centered composition, simple clean background in solid pale cream color,
  small cute details, no text or labels, icon sticker style illustration
  ```
- **Size**: `1024x1024`
- **Output path**: `/tmp/travel-map-CITY_SLUG/poi_{SLUG}.png`

Generate all POI icons concurrently. If any look unsatisfactory, regenerate with a more specific prompt.

**Output**: One `poi_*.png` per attraction.

---

## Phase 6: Compositing

**Goal**: Assemble the final illustrated travel map.

1. Build the configuration JSON file at `/tmp/travel-map-CITY_SLUG/config.json`:

```json
{
  "city_name": "City Name (Display Title)",
  "viewport": {
    "center_lat": CENTER_LAT,
    "center_lng": CENTER_LNG,
    "zoom": ZOOM,
    "width": 1536,
    "height": 1024
  },
  "pois": [
    {
      "name": "POI Display Name",
      "lat": LAT,
      "lng": LNG,
      "icon_path": "/tmp/travel-map-CITY_SLUG/poi_SLUG.png",
      "order": ORDER_NUMBER_OR_NULL
    }
  ]
}
```

- Set `"order"` to the 1-based visit sequence if the user specified an order
- Set `"order"` to `null` for automatic route optimization
- Use proper formatting for `"city_name"` (appears as title banner)

2. Run the compositing script:
```bash
python3 SKILL_DIR/scripts/composite.py \
  --map /tmp/travel-map-CITY_SLUG/stylized_map.png \
  --config /tmp/travel-map-CITY_SLUG/config.json \
  --output /tmp/travel-map-CITY_SLUG/final_map.png
```

3. Verify the output by reading the final image.

**Output**: `final_map.png` — the complete illustrated travel map.

---

## Phase 7: Delivery

**Goal**: Present the result to the user.

1. Copy the final map to the user's working directory:
   ```bash
   cp /tmp/travel-map-CITY_SLUG/final_map.png ./CITY_SLUG_travel_map.png
   ```

2. Show the image to the user using the Read tool.

3. Summarize what was generated:
   - City name
   - Listed attractions in route order
   - Route description (user-specified or auto-computed)
   - Output file path

4. Offer modifications:
   - "Want to add or remove any attractions?"
   - "Want to change the visit order?"
   - "Want to adjust the map style?"

---

## Image Prompt Tips

For better ImageGen results with the Ghibli style:
- Always include "Studio Ghibli", "Hayao Miyazaki", and "watercolor" in the prompt
- Specify "pale cream background" to make icons easier to composite
- Use "icon sticker style" to get centered, isolated illustrations
- Add landmark-specific details (e.g., "red torii gate" for Fushimi Inari)
- Avoid requesting text or labels in the generated images

## Script Reference

| Script | Purpose | Key Arguments |
|--------|---------|---------------|
| `install_deps.py` | Install Pillow | (none) |
| `utils.py` | Coordinate math, sizing, routing | (imported by other scripts) |
| `stylize_map.py` | Map screenshot → Ghibli style | `--input`, `--output` |
| `composite.py` | Final map assembly | `--map`, `--config`, `--output` |

For coordinate mapping math details, see [coordinate-mapping.md](references/coordinate-mapping.md).

## Error Recovery

| Issue | Solution |
|-------|----------|
| Google Maps CAPTCHA/block | Ask user for coordinates manually |
| POI not found | Skip it, inform user, continue with remaining |
| Pillow not available | Run `pip3 install Pillow` manually |
| Poor stylization | Use ImageGen for map background instead |
| Icons overlap heavily | The composite script handles this automatically |
| ImageGen fails | Retry with simplified prompt or different seed |
