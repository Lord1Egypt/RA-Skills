# Dashboard reference

Read this when doing Lovelace/UI work. Core deploy/verify rules are in `../SKILL.md`.

## Fundamentals
- Dashboards are JSON in `.storage/lovelace.*` (e.g. `.storage/lovelace.control_center`).
- **UI edits** (via the dashboard editor) show on a **browser hard-refresh** (Ctrl/Cmd+Shift+R).
  **Direct file edits** (scp/git) may not appear until a `ha core restart` — HA caches the
  lovelace store in memory; if a refresh doesn't show your change, restart.
- Adding a **new** dashboard requires registering it in `.storage/lovelace_dashboards` and a
  **restart** for it to appear in the sidebar.
- Validate JSON before deploying: `python3 -m json.tool .storage/lovelace.x > /dev/null`.

## Fast iteration loop
```bash
# edit .storage/lovelace.control_center locally, then:
scp .storage/lovelace.control_center root@homeassistant.local:/config/.storage/
# hard-refresh browser. Repeat. Commit to git only once stable.
```
If a hard-refresh doesn't reflect the change, the instance is caching the store —
`ha core restart` to pick up direct file edits.

## View types
- **sections** (modern default): responsive drag-drop grid, supports badges and `heading`
  cards. Use for organized multi-card layouts. Has ~10% side margins.
- **panel**: one card, full width, zero margins. Use for maps/cameras or anything that
  should fill the screen without scrolling.

```json
{ "type": "panel", "title": "Vacuum", "path": "map",
  "cards": [ { "type": "custom:xiaomi-vacuum-map-card", "entity": "vacuum.dusty" } ] }
```

## Card choices (prefer native first)
Modern HA covers most needs without custom cards:
- **tile** — entity control with features (hvac modes, target temp, fan speed, toggles).
  First choice for climate/lights/switches.
- **heading** / badges — section titles and compact status in sections view.
- **custom:mushroom-*** — use when you specifically want Mushroom's look (animated icons,
  collapsible sliders). Requires HACS install.
- **custom:mushroom-template-card** / markdown — dynamic Jinja content with color-coding.

```json
{ "type": "tile", "entity": "climate.thermostat",
  "features": [
    {"type": "climate-hvac-modes", "hvac_modes": ["heat","cool","fan_only","off"]},
    {"type": "climate-fan-modes"},
    {"type": "target-temperature"} ] }
```

```json
{ "type": "custom:mushroom-template-card",
  "primary": "All Doors",
  "secondary": "{% set d = ['binary_sensor.front_door','binary_sensor.back_door'] %}\n{% set open = d | select('is_state','on') | list | length %}\n{{ open }} / {{ d | length }} open",
  "icon": "mdi:door",
  "icon_color": "{% if open > 0 %}red{% else %}green{% endif %}" }
```

## Template patterns for cards
Always coerce types (`| int(0)` / `| float(0)`) — bare states are strings and comparisons
raise `TypeError`; the default guards `None` at startup.

```jinja2
{# count open #}
{% set s = ['binary_sensor.front_door','binary_sensor.back_door'] %}
{{ s | select('is_state','on') | list | length }} / {{ s | length }} open

{# color by days-until #}
{% set days = state_attr('sensor.bin_collection','daysTo') | int(99) %}
{% if days <= 1 %}red{% elif days <= 3 %}amber{% elif days <= 7 %}yellow{% else %}grey{% endif %}
```

## Tablet layout
- 11" tablet: 3-4 columns; touch targets ≥44px.
- Use `panel` for full-screen content to kill margins/scrolling.
- Color-code status (red/green/amber) for glanceable state.

```json
{ "type": "grid", "columns": 3, "square": false,
  "cards": [ {"type":"tile","entity":"light.living_room"},
             {"type":"tile","entity":"light.bedroom"} ] }
```

## Pitfalls
| Symptom | Cause → Fix |
|---------|-------------|
| Dashboard not in sidebar | Not registered → add to `lovelace_dashboards`, restart |
| "Custom element doesn't exist" | Card not installed → install via HACS |
| Card "Configuration error" | Bad syntax/template → check browser console (F12), test template in Dev Tools |
| `TypeError: '<' not supported …` | String vs int → `| int(0)` before comparing |
| Map has margins/scrolls | Using sections → switch to `panel` view |
| `auto-entities` does nothing | Target card lacks `card_param` → use cards taking `entities` (entities/vertical-stack/horizontal-stack) |

## Debugging
1. Browser console (F12) for red errors on load.
2. `python3 -m json.tool <file>` to catch JSON syntax breaks.
3. Dev Tools → Template to test Jinja before committing.
4. `hass-cli state get <entity>` to confirm the entity id exists.
5. Hard-refresh / incognito to rule out cache.

## Visual validation in the browser (Claude-in-Chrome)
Cards render client-side, so logs and entity state can't confirm a dashboard change actually
*looks* right — a broken card, a wrong color, or a mis-sorted popup only shows in the UI.
After deploying (and the restart the storage cache needs), validate visually:

1. Drive the user's real, logged-in browser via the **Claude-in-Chrome** extension (native;
   no Playwright/MCP). Confirm the connection (`tabs_context_mcp`), open a fresh tab, navigate
   to the dashboard.
2. **Use the URL where the session is authenticated** (often an external/reverse-proxy domain).
   A fresh tab on the LAN hostname may show a login page — **never enter credentials**; ask the
   user to log in or navigate.
3. The extension needs a **one-time per-site permission grant** for the HA domain (separate
   from navigating to it) — the user toggles "allow Claude to act on this site".
4. **HA cards live in shadow DOM**, so the accessibility tree / `find` can't see them. Drive
   **visually**: screenshot, then click by coordinate. Don't waste turns on `find` for cards.
5. Validate popups/modals (e.g. browser_mod) by clicking the trigger and screenshotting; press
   `Escape` to close. Scroll + screenshot to reach cards below the fold.
6. Capture a screenshot as proof, then report what rendered vs. expected.
