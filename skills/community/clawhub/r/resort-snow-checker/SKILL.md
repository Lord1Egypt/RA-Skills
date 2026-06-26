---
name: resort-snow-checker
description: "A universal skill to check snow conditions, weather, and gear requirements for ANY ski resort globally."
---

# Global Resort Conditions

This skill fetches the latest mountain reports, weather forecasts, and surface conditions to provide a "go/no-go" recommendation and specific gear advice for skiers and snowboarders.

## 1. Request Validation

### Supported Dates
- **Past Dates:** Inform the user that historical data is not supported and stop.
- **Current/Future Dates:** Proceed to data gathering.

## 2. Mountain Report
1. **Search Phase:** Use `web_search` for: `"[Resort Name] current mountain report snow conditions"`.
2. **Extraction Phase:** Identify:
   - **New Snow:** (Last 24h/48h).
   - **Base Depth:** Current snow pack thickness.
   - **Operational Status:** Open lifts vs. total (check for "Wind Holds" or "Delayed Openings").
   - **Surface:** (e.g., Powder, Packed Powder, Hardpack, Spring Slush, Crusty).

## 3. Weather & Gear Analysis
1. **Search Phase:** Use `web_search` for: `"[Resort Name] weather forecast [Requested Date]"`.
2. **Key Data Points:** Temperature (High/Low), Wind Speed (mph/kph), and Visibility/Precipitation.
3. **Gear Logic:**
   - **Sub-Zero (<15°F / -10°C):** Recommend heavy insulators, face masks, and hand warmers.
   - **Spring/Warm (>35°F / 2°C):** Recommend shells/layers, high-SPF sunscreen, and "warm-weather" wax.
   - **High Wind/Snow:** Recommend high-contrast (low light) goggles.
   - **Wet Snow/Rain:** Recommend waterproof hardshells and spare gloves.

## 4. Verdict & Response
Provide a concise, formatted response:

🏔️ Mountain Report
*Summary of new snow, base depth, and lift operations.*

❄️ Weather Report
*Summary of temp, wind, and sky conditions.*

🧤 Gear & Prep
*Provide 2-3 specific gear recommendations based on the weather (e.g., "Pack your low-light goggles for the fog" or "Bring a face mask for the wind chill").*

🎿 Recommendation
Provide a verdict:
- **Strongly Recommended:** Fresh snow, calm winds, good visibility.
- **Recommended:** Stable base, groomed trails, standard winter weather.
- **Caution:** High winds (lift hold risk), rain/ice, or heavy fog (low visibility).
- **Not Recommended:** Resort is closed, lightning, or extreme storm warnings.