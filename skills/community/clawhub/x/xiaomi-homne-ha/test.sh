#!/usr/bin/env bash
# =============================================================================
# xiaomi-home-ha — Integration Test Suite (Live HA)
# 针对真实 Home Assistant 实例的集成测试
#
# Usage:
#   HA_URL=http://192.168.31.202:8123 HA_TOKEN=<token> bash test.sh
#   HA_URL=... HA_TOKEN=... HA_TEST_ENTITY=light.bed_lamp bash test.sh
#
# Environment:
#   HA_URL            Required. HA base URL.
#   HA_TOKEN          Required. Long-lived access token.
#   HA_TEST_ENTITY    Optional. Entity for write tests (default: auto-detect first light)
#   HA_SKIP_WRITE     Set to 1 to skip write (control) tests (read-only mode)
#
# Requires: curl, node (v18+)
# =============================================================================

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

PASS=0; FAIL=0; SKIP=0

pass() { echo -e "${GREEN}✓ PASS${RESET} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}✗ FAIL${RESET} $1"; FAIL=$((FAIL+1)); }
skip() { echo -e "${YELLOW}⊘ SKIP${RESET} $1"; SKIP=$((SKIP+1)); }
section() { echo -e "\n${CYAN}${BOLD}── $1 ──${RESET}"; }

# ── JSON helper via node (no jq required) ──────────────────────────────────
jq_val() {
  local json="$1"
  local expr="$2"
  node --input-type=module - <<EOF
const d = ${json};
const result = (${expr});
if (result === null || result === undefined) process.stdout.write("null\n");
else if (typeof result === "string") process.stdout.write(result + "\n");
else process.stdout.write(JSON.stringify(result) + "\n");
EOF
}

# ── Preflight ────────────────────────────────────────────────────────────────
section "Preflight: Environment & Dependencies"

for bin in curl node; do
  if command -v "$bin" &>/dev/null; then
    pass "binary available: $bin"
  else
    fail "binary missing: $bin"
    exit 1
  fi
done

: "${HA_URL:?'HA_URL is required. Export it before running.'}"
: "${HA_TOKEN:?'HA_TOKEN is required. Export it before running.'}"
pass "HA_URL set: ${HA_URL}"
pass "HA_TOKEN set (${#HA_TOKEN} chars)"

# ── HTTP helpers ──────────────────────────────────────────────────────────────
ha_get() {
  curl -sf "${HA_URL}$1" \
    -H "Authorization: Bearer ${HA_TOKEN}" \
    -H "Content-Type: application/json"
}
ha_post() {
  curl -sf -X POST "${HA_URL}$1" \
    -H "Authorization: Bearer ${HA_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$2"
}
ha_status() {
  curl -s -o /dev/null -w "%{http_code}" "${HA_URL}$1" \
    -H "Authorization: Bearer ${HA_TOKEN}"
}

# ── Group 1: Connectivity ─────────────────────────────────────────────────────
section "Group 1: HA API Connectivity"

API_RESP=$(ha_get "/api/")
MSG=$(jq_val "$API_RESP" "d.message")
[[ "$MSG" == "API running." ]] && pass "T1.1 GET /api/ — API running" || fail "T1.1 — unexpected: ${MSG}"

STATUS=$(ha_status "/api/")
[[ "$STATUS" == "200" ]] && pass "T1.2 Auth — token accepted (HTTP 200)" || fail "T1.2 — HTTP ${STATUS} (check HA_TOKEN)"

BAD_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${HA_URL}/api/" \
  -H "Authorization: Bearer invalid_token_xyz")
[[ "$BAD_STATUS" == "401" ]] && pass "T1.3 Auth — invalid token → HTTP 401" || fail "T1.3 — expected 401, got ${BAD_STATUS}"

# ── Group 2: Query All Entities ───────────────────────────────────────────────
section "Group 2: Query — GET /api/states"

STATES=$(ha_get "/api/states")

STATES_TYPE=$(jq_val "$STATES" "Array.isArray(d) ? 'array' : typeof d")
if [[ "$STATES_TYPE" == "array" ]]; then
  TOTAL=$(jq_val "$STATES" "d.length")
  pass "T2.1 GET /api/states — returned array with ${TOTAL} entities"
else
  fail "T2.1 GET /api/states — expected JSON array, got ${STATES_TYPE}"
fi

SCHEMA_OK=$(jq_val "$STATES" "d.every(e=>'entity_id' in e && 'state' in e && 'attributes' in e)?'yes':'no'")
[[ "$SCHEMA_OK" == "yes" ]] && pass "T2.2 Schema — all entities have entity_id, state, attributes" || fail "T2.2 Schema"

LIGHT_N=$(jq_val  "$STATES" "d.filter(e=>e.entity_id.startsWith('light.')).length")
SWITCH_N=$(jq_val "$STATES" "d.filter(e=>e.entity_id.startsWith('switch.')).length")
SENSOR_N=$(jq_val "$STATES" "d.filter(e=>e.entity_id.startsWith('sensor.')).length")
pass "T2.3 Domain filter — light:${LIGHT_N}  switch:${SWITCH_N}  sensor:${SENSOR_N}"

HAS_NAME=$(jq_val "$STATES" "d.some(e=>e.attributes.friendly_name!=null)?'yes':'no'")
[[ "$HAS_NAME" == "yes" ]] && pass "T2.4 Attributes — at least one entity has friendly_name" \
  || skip "T2.4 Attributes — no friendly_name found (unusual)"

# ── Group 3: Query Single Entity ──────────────────────────────────────────────
section "Group 3: Query — GET /api/states/<entity_id>"

if [[ -z "${HA_TEST_ENTITY:-}" ]]; then
  HA_TEST_ENTITY=$(jq_val "$STATES" \
    "d.find(e=>e.entity_id.startsWith('light.'))?.entity_id || d.find(e=>e.entity_id.startsWith('switch.'))?.entity_id || null")
fi

if [[ -z "$HA_TEST_ENTITY" || "$HA_TEST_ENTITY" == "null" ]]; then
  skip "T3.x — no test entity found; set HA_TEST_ENTITY to override"
else
  echo "    Using test entity: ${HA_TEST_ENTITY}"

  ENTITY_JSON=$(ha_get "/api/states/${HA_TEST_ENTITY}")
  EID=$(jq_val "$ENTITY_JSON" "d.entity_id")
  if [[ "$EID" == "$HA_TEST_ENTITY" ]]; then
    ENTITY_STATE=$(jq_val "$ENTITY_JSON" "d.state")
    pass "T3.1 GET /api/states/${HA_TEST_ENTITY} — state: ${ENTITY_STATE}"
  else
    fail "T3.1 GET /api/states/${HA_TEST_ENTITY} — entity_id mismatch: ${EID}"
  fi

  TS=$(jq_val "$ENTITY_JSON" "d.last_updated")
  [[ -n "$TS" && "$TS" != "null" ]] && pass "T3.2 Timestamp — last_updated: ${TS}" || fail "T3.2 last_updated missing"

  STATUS_404=$(ha_status "/api/states/light.this_entity_does_not_exist_zzz")
  [[ "$STATUS_404" == "404" ]] && pass "T3.3 Not found — non-existent entity → HTTP 404" || fail "T3.3 — expected 404, got ${STATUS_404}"
fi

# ── Group 4: Sensors / Read-Only Entities ────────────────────────────────────
section "Group 4: Sensor & Read-Only Entities"

SENSOR_N_2=$(jq_val "$STATES" "d.filter(e=>e.entity_id.startsWith('sensor.')).length")
pass "T4.1 Sensor domain — ${SENSOR_N_2} sensor entities found"

ENV_N=$(jq_val "$STATES" \
  "d.filter(e=>['temperature','humidity','pm25','co2','illuminance'].includes(e.attributes.device_class||'')).length")
pass "T4.2 Environment sensors — ${ENV_N} temp/humidity/air-quality sensors"

NUMERIC_N=$(jq_val "$STATES" \
  "d.filter(e=>/^-?[0-9]+(\.[0-9]+)?$/.test(e.state)).length")
pass "T4.3 Numeric sensors — ${NUMERIC_N} entities with numeric state"

# ── Group 5: Write — Control Devices ─────────────────────────────────────────
section "Group 5: Write — POST /api/services/<domain>/<service>"

if [[ "${HA_SKIP_WRITE:-0}" == "1" ]]; then
  skip "T5.x — write tests skipped (HA_SKIP_WRITE=1)"
elif [[ -z "${HA_TEST_ENTITY:-}" || "$HA_TEST_ENTITY" == "null" ]]; then
  skip "T5.x — no test entity found; write tests skipped"
else
  DOMAIN="${HA_TEST_ENTITY%%.*}"
  echo "    Write tests on: ${HA_TEST_ENTITY} (domain: ${DOMAIN})"

  # T5.1 — turn_on
  ha_post "/api/services/${DOMAIN}/turn_on" \
    "{\"entity_id\": \"${HA_TEST_ENTITY}\", \"transition\": 0.5}" &>/dev/null || true
  sleep 0.8
  STATE=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.state")
  [[ "$STATE" == "on" ]] && pass "T5.1 turn_on → ${HA_TEST_ENTITY}: ${STATE}" || fail "T5.1 — expected on, got ${STATE}"

  # T5.2 — brightness (light only)
  if [[ "$DOMAIN" == "light" ]]; then
    ha_post "/api/services/light/turn_on" \
      "{\"entity_id\": \"${HA_TEST_ENTITY}\", \"brightness_pct\": 50, \"transition\": 0.5}" &>/dev/null || true
    sleep 0.8
    BRI=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.attributes.brightness")
    if [[ "$BRI" != "null" && -n "$BRI" ]]; then
      BRI_PCT=$(node -e "console.log(Math.round(${BRI}/255*100))")
      pass "T5.2 brightness_pct=50 — actual: ${BRI_PCT}% (raw:${BRI})"
    else
      skip "T5.2 brightness — entity does not support brightness"
    fi

    ha_post "/api/services/light/turn_on" \
      "{\"entity_id\": \"${HA_TEST_ENTITY}\", \"color_temp_kelvin\": 4000}" &>/dev/null || true
    sleep 0.8
    K=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.attributes.color_temp_kelvin")
    [[ "$K" != "null" ]] && pass "T5.3 color_temp_kelvin=4000 — actual: ${K}K" || skip "T5.3 — no color_temp support"
  else
    skip "T5.2 brightness — not a light entity"
    skip "T5.3 color_temp — not a light entity"
  fi

  # T5.4 — toggle
  BEFORE=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.state")
  ha_post "/api/services/${DOMAIN}/toggle" "{\"entity_id\": \"${HA_TEST_ENTITY}\"}" &>/dev/null || true
  sleep 0.8
  AFTER=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.state")
  [[ "$BEFORE" != "$AFTER" ]] && pass "T5.4 toggle — ${BEFORE} → ${AFTER}" \
    || fail "T5.4 toggle — state unchanged (${BEFORE})"

  # T5.5 — turn_off (restore)
  ha_post "/api/services/${DOMAIN}/turn_off" \
    "{\"entity_id\": \"${HA_TEST_ENTITY}\", \"transition\": 0.5}" &>/dev/null || true
  sleep 0.8
  FINAL=$(jq_val "$(ha_get "/api/states/${HA_TEST_ENTITY}")" "d.state")
  [[ "$FINAL" == "off" ]] && pass "T5.5 turn_off — ${HA_TEST_ENTITY} restored: off" \
    || fail "T5.5 turn_off — expected off, got ${FINAL}"
fi

# ── Group 6: Generic Service Call ─────────────────────────────────────────────
section "Group 6: Generic Service Call (Universal Template)"

# T6.1 — domain extraction
ENTITY_ID_SAMPLE="media_player.xiaomi_speaker"
EXTRACTED="${ENTITY_ID_SAMPLE%%.*}"
[[ "$EXTRACTED" == "media_player" ]] \
  && pass "T6.1 Domain extract — '${ENTITY_ID_SAMPLE}' → '${EXTRACTED}'" \
  || fail "T6.1 — expected media_player, got ${EXTRACTED}"

# T6.2 — service_data merge via node
MERGED=$(node -e "
const eid = 'light.test';
const extra = {brightness_pct: 80, transition: 0.5};
console.log(JSON.stringify({entity_id: eid, ...extra}));
")
CHECK=$(node -e "const d=JSON.parse(process.argv[1]); console.log(d.entity_id==='light.test'&&d.brightness_pct===80&&d.transition===0.5?'yes':'no')" "$MERGED")
[[ "$CHECK" == "yes" ]] && pass "T6.2 JSON merge — service_data with entity_id merged correctly" \
  || fail "T6.2 JSON merge — unexpected output: ${MERGED}"

# T6.3 — empty service_data
MERGED_EMPTY=$(node -e "console.log(JSON.stringify({entity_id:'switch.fan'}))")
CHECK=$(node -e "const d=JSON.parse(process.argv[1]); console.log(d.entity_id==='switch.fan'?'yes':'no')" "$MERGED_EMPTY")
[[ "$CHECK" == "yes" ]] && pass "T6.3 JSON merge — empty service_data produces clean payload" \
  || fail "T6.3 — unexpected: ${MERGED_EMPTY}"

# ── Group 7: jq Filter Logic (Offline) ────────────────────────────────────────
section "Group 7: Filter Logic (Offline, node)"

MOCK='[
  {"entity_id":"light.bedroom","state":"on",
   "attributes":{"friendly_name":"Bedroom Light","brightness":128,"area_id":"bedroom"}},
  {"entity_id":"light.living_room","state":"off",
   "attributes":{"friendly_name":"Living Room","area_id":"living_room"}},
  {"entity_id":"sensor.temperature","state":"24.5",
   "attributes":{"friendly_name":"Temp","unit_of_measurement":"°C","device_class":"temperature"}},
  {"entity_id":"switch.fan","state":"off",
   "attributes":{"friendly_name":"Fan","area_id":"bedroom"}},
  {"entity_id":"media_player.speaker","state":"idle",
   "attributes":{"friendly_name":"Xiaomi Speaker"}}
]'

LIGHTS=$(jq_val "$MOCK" "d.filter(e=>e.entity_id.startsWith('light.')).length")
[[ "$LIGHTS" == "2" ]] && pass "T7.1 Domain filter — light prefix: ${LIGHTS}" || fail "T7.1 — expected 2, got ${LIGHTS}"

BEDROOM=$(jq_val "$MOCK" "d.filter(e=>(e.attributes.area_id||'').toLowerCase().includes('bedroom')).length")
[[ "$BEDROOM" == "2" ]] && pass "T7.2 Area filter — 'bedroom': ${BEDROOM} entities" || fail "T7.2 — expected 2, got ${BEDROOM}"

BRI_PCT=$(node -e "console.log(Math.round(128/255*100))")
[[ "$BRI_PCT" == "50" ]] && pass "T7.3 Brightness convert — 128→${BRI_PCT}%" || fail "T7.3 — expected 50, got ${BRI_PCT}"

NUMERIC=$(jq_val "$MOCK" "d.filter(e=>/^-?[0-9]+(\.[0-9]+)?$/.test(e.state)).length")
[[ "$NUMERIC" == "1" ]] && pass "T7.4 Numeric state filter — ${NUMERIC} (sensor.temperature)" || fail "T7.4 — expected 1, got ${NUMERIC}"

ENV=$(jq_val "$MOCK" "d.filter(e=>['temperature','humidity','pm25','co2'].includes(e.attributes.device_class||'')).length")
[[ "$ENV" == "1" ]] && pass "T7.5 Env sensor filter — ${ENV}" || fail "T7.5 — expected 1, got ${ENV}"

# ── Group 8: SKILL.md Format ──────────────────────────────────────────────────
section "Group 8: SKILL.md Format"

SKILL_FILE="$(dirname "$0")/SKILL.md"
if [[ -f "$SKILL_FILE" ]]; then
  pass "T8.1 SKILL.md exists"
  head -5 "$SKILL_FILE" | grep -q "^---$" && pass "T8.2 Frontmatter ---" || fail "T8.2 Frontmatter ---"

  for field in "name:" "description:" "metadata:"; do
    grep -q "^${field}" "$SKILL_FILE" && pass "T8.3 Field: ${field}" || fail "T8.3 Missing: ${field}"
  done

  grep -q "name: xiaomi-home-ha" "$SKILL_FILE"  && pass "T8.4 Skill name correct"          || fail "T8.4 Wrong skill name"
  grep -q 'bins'                 "$SKILL_FILE"  && pass "T8.5 requires.bins declared"        || fail "T8.5 requires.bins missing"
  grep -q '${DOMAIN}'            "$SKILL_FILE"  && pass 'T8.6 ${DOMAIN} template used'       || fail 'T8.6 ${DOMAIN} not found'

  grep -qE '^[[:space:]]*/xiaomi[[:space:]]' "$SKILL_FILE" \
    && fail "T8.7 /xiaomi slash commands found (should be removed)" \
    || pass "T8.7 No /xiaomi slash commands — clean"

  grep -q '小米\|控制\|适用' "$SKILL_FILE" && pass "T8.8 Chinese content present" || fail "T8.8 Chinese content missing"
else
  fail "T8.1 SKILL.md not found at: ${SKILL_FILE}"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  ${GREEN}PASS: ${PASS}${RESET}   ${RED}FAIL: ${FAIL}${RESET}   ${YELLOW}SKIP: ${SKIP}${RESET}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
else
  echo -e "\n${GREEN}All tests passed.${RESET}"
  exit 0
fi
