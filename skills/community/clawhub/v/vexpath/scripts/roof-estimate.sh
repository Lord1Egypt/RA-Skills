#!/usr/bin/env bash
# =============================================================================
# roof-estimate.sh — VexPath Roofing Estimator
# =============================================================================
# Usage: ./roof-estimate.sh "123 Main St, Baltimore, MD 21201"
#
# Requires:
#   - GOOGLE_MAPS_API_KEY env var
#   - curl, python3, jq
#
# Output: JSON report to stdout
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [[ -z "${GOOGLE_MAPS_API_KEY:-}" ]]; then
  echo '{"error":"GOOGLE_MAPS_API_KEY environment variable is not set"}' >&2
  exit 1
fi

if [[ $# -lt 1 || -z "$1" ]]; then
  echo '{"error":"Usage: roof-estimate.sh \"<address>\""}' >&2
  exit 1
fi

ADDRESS="$1"
API_KEY="${GOOGLE_MAPS_API_KEY}"

# ---------------------------------------------------------------------------
# Helper: URL-encode a string
# ---------------------------------------------------------------------------
urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"
}

# ---------------------------------------------------------------------------
# Step 1 — Geocode address
# ---------------------------------------------------------------------------
ENCODED_ADDRESS="$(urlencode "$ADDRESS")"
GEO_URL="https://maps.googleapis.com/maps/api/geocode/json?address=${ENCODED_ADDRESS}&key=${API_KEY}"

GEO_RESPONSE="$(curl -sf "$GEO_URL")" || {
  echo '{"error":"Geocoding API request failed"}' >&2
  exit 1
}

GEO_STATUS="$(echo "$GEO_RESPONSE" | jq -r '.status')"
if [[ "$GEO_STATUS" != "OK" ]]; then
  echo "{\"error\":\"Geocoding failed: ${GEO_STATUS}\",\"address\":\"${ADDRESS}\"}" >&2
  exit 1
fi

LAT="$(echo "$GEO_RESPONSE" | jq -r '.results[0].geometry.location.lat')"
LNG="$(echo "$GEO_RESPONSE" | jq -r '.results[0].geometry.location.lng')"
FORMATTED_ADDRESS="$(echo "$GEO_RESPONSE" | jq -r '.results[0].formatted_address')"

if [[ -z "$LAT" || "$LAT" == "null" ]]; then
  echo '{"error":"Could not extract coordinates from geocoding response"}' >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Step 2 — Google Solar API: Building Insights
# ---------------------------------------------------------------------------
SOLAR_URL="https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude=${LAT}&location.longitude=${LNG}&requiredQuality=HIGH&key=${API_KEY}"

SOLAR_RESPONSE="$(curl -sf "$SOLAR_URL")" || {
  echo '{"error":"Solar API request failed"}' >&2
  exit 1
}

# Check for API error
SOLAR_ERROR="$(echo "$SOLAR_RESPONSE" | jq -r '.error.message // empty')"
if [[ -n "$SOLAR_ERROR" ]]; then
  echo "{\"error\":\"Solar API error: ${SOLAR_ERROR}\",\"address\":\"${FORMATTED_ADDRESS}\"}" >&2
  exit 1
fi

WHOLE_AREA_M2="$(echo "$SOLAR_RESPONSE" | jq -r '.solarPotential.wholeRoofStats.areaMeters2 // .wholeRoofStats.areaMeters2 // empty')"
if [[ -z "$WHOLE_AREA_M2" || "$WHOLE_AREA_M2" == "null" ]]; then
  echo "{\"error\":\"No roof data returned for this address. Try a different address or quality level.\",\"address\":\"${FORMATTED_ADDRESS}\"}" >&2
  exit 1
fi

NUM_SEGMENTS="$(echo "$SOLAR_RESPONSE" | jq '.solarPotential.roofSegmentStats | length')"

# ---------------------------------------------------------------------------
# Step 3 — Python: parse segments, calculate waste + materials + cost
# ---------------------------------------------------------------------------
python3 - "$SOLAR_RESPONSE" "$FORMATTED_ADDRESS" "$LAT" "$LNG" "$NUM_SEGMENTS" <<'PYEOF'
import sys, json, math

raw_json   = sys.argv[1]
address    = sys.argv[2]
lat        = float(sys.argv[3])
lng        = float(sys.argv[4])
# num_segments passed for validation; recalculate from parsed data

data = json.loads(raw_json)
solar = data.get("solarPotential", data)  # handle both response shapes

segments_raw = solar.get("roofSegmentStats", [])
whole_area_m2 = solar.get("wholeRoofStats", {}).get("areaMeters2", 0)

# Convert m2 → ft2 (1 m2 = 10.7639 ft2)
M2_TO_FT2 = 10.7639

# Parse segments
segments = []
total_pitch_deg = 0
for seg in segments_raw:
    area_m2  = seg.get("stats", {}).get("areaMeters2", 0)
    pitch_deg = seg.get("pitchDegrees", 0)
    azimuth  = seg.get("azimuthDegrees", 0)
    area_ft2 = area_m2 * M2_TO_FT2
    segments.append({
        "area_ft2":    round(area_ft2, 1),
        "pitch_deg":   round(pitch_deg, 1),
        "azimuth_deg": round(azimuth, 1)
    })
    total_pitch_deg += pitch_deg

num_segments = len(segments)
avg_pitch_deg = total_pitch_deg / num_segments if num_segments > 0 else 0

# Convert pitch degrees to x/12 ratio
def deg_to_ratio(deg):
    return math.tan(math.radians(deg)) * 12

avg_pitch_ratio = deg_to_ratio(avg_pitch_deg)
total_area_ft2  = whole_area_m2 * M2_TO_FT2

# ---------------------------------------------------------------------------
# Waste calculation
# ---------------------------------------------------------------------------
if num_segments <= 2:
    base_waste = 7
elif num_segments <= 4:
    base_waste = 12
elif num_segments <= 8:
    base_waste = 17
else:
    base_waste = 22

pitch_adjustment   = max(0, avg_pitch_ratio - 6) * 1
segment_adjustment = max(0, num_segments - 4) * 1.5
waste_pct = base_waste + pitch_adjustment + segment_adjustment
waste_pct = max(5, min(30, waste_pct))  # clamp 5–30

# ---------------------------------------------------------------------------
# Material quantities
# ---------------------------------------------------------------------------
roof_squares = (total_area_ft2 * (1 + waste_pct / 100)) / 100

est_perimeter_ft = math.sqrt(total_area_ft2) * 4 * 0.85
num_valleys      = max(0, num_segments - 2)

shingle_bundles    = math.ceil(roof_squares * 3)
underlayment_rolls = math.ceil(roof_squares * 1.1)
ridge_cap_bundles  = math.ceil(est_perimeter_ft * 0.15 / 33)
drip_edge_sections = math.ceil(est_perimeter_ft / 10)
starter_strip_ft   = round(est_perimeter_ft)
nails_lbs          = math.ceil(roof_squares * 2.5)
ice_water_rolls    = num_valleys * 2

# ---------------------------------------------------------------------------
# Cost estimation (low / mid / high)
# ---------------------------------------------------------------------------
mat_low  = (shingle_bundles * 30) + (underlayment_rolls * 45) + (ridge_cap_bundles * 35) + (drip_edge_sections * 8)
mat_mid  = (shingle_bundles * 40) + (underlayment_rolls * 55) + (ridge_cap_bundles * 45) + (drip_edge_sections * 10)
mat_high = (shingle_bundles * 50) + (underlayment_rolls * 65) + (ridge_cap_bundles * 55) + (drip_edge_sections * 12)

lab_low  = roof_squares * 75
lab_mid  = roof_squares * 100
lab_high = roof_squares * 125

total_low  = round(mat_low  + lab_low)
total_mid  = round(mat_mid  + lab_mid)
total_high = round(mat_high + lab_high)

# ---------------------------------------------------------------------------
# Output JSON report
# ---------------------------------------------------------------------------
report = {
    "address":          address,
    "lat":              lat,
    "lng":              lng,
    "total_area_sqft":  round(total_area_ft2, 1),
    "num_segments":     num_segments,
    "avg_pitch":        round(avg_pitch_ratio, 2),
    "waste_percent":    round(waste_pct, 1),
    "total_squares":    round(roof_squares, 2),
    "materials": {
        "shingle_bundles":    shingle_bundles,
        "underlayment_rolls": underlayment_rolls,
        "ridge_cap_bundles":  ridge_cap_bundles,
        "drip_edge_sections": drip_edge_sections,
        "starter_strip_ft":   starter_strip_ft,
        "nails_lbs":          nails_lbs,
        "ice_water_rolls":    ice_water_rolls
    },
    "cost_estimate": {
        "low":  total_low,
        "mid":  total_mid,
        "high": total_high
    },
    "raw_segments": segments
}

print(json.dumps(report, indent=2))
PYEOF
