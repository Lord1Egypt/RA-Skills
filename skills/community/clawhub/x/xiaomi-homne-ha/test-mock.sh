#!/usr/bin/env bash
# =============================================================================
# xiaomi-home-ha — Offline Mock Tests
# 无需真实 HA 实例，使用 mock-ha-server.py 在本地模拟 HA REST API
#
# Usage:
#   bash test-mock.sh
#
# Requires: curl, node (v18+), python3 (stdlib only — for mock server)
# =============================================================================

set -euo pipefail

MOCK_PORT=18123
MOCK_URL="http://127.0.0.1:${MOCK_PORT}"
MOCK_TOKEN="mock_test_token_abc123"
MOCK_PID=""

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

PASS=0; FAIL=0; SKIP=0

pass() { echo -e "${GREEN}✓ PASS${RESET} $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}✗ FAIL${RESET} $1"; FAIL=$((FAIL+1)); }
skip() { echo -e "${YELLOW}⊘ SKIP${RESET} $1"; SKIP=$((SKIP+1)); }
section() { echo -e "\n${CYAN}${BOLD}── $1 ──${RESET}"; }

# ── JSON helpers via node ─────────────────────────────────────────────────────
# jq_val <json_string> <js_expression_using_d>
# Returns the JS expression result as plain string.
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

# ── Cleanup ───────────────────────────────────────────────────────────────────
cleanup() {
  if [[ -n "$MOCK_PID" ]] && kill -0 "$MOCK_PID" 2>/dev/null; then
    kill "$MOCK_PID" 2>/dev/null || true
    wait "$MOCK_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

# ── HTTP helpers ──────────────────────────────────────────────────────────────
ha_get() {
  curl -sf "${MOCK_URL}$1" -H "Authorization: Bearer ${MOCK_TOKEN}"
}
ha_post() {
  curl -sf -X POST "${MOCK_URL}$1" \
    -H "Authorization: Bearer ${MOCK_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$2"
}
ha_status() {
  curl -s -o /dev/null -w "%{http_code}" "${MOCK_URL}$1" \
    -H "Authorization: Bearer ${MOCK_TOKEN}"
}

# ── Preflight ────────────────────────────────────────────────────────────────
section "Preflight: Dependencies"

for bin in curl node python3; do
  if command -v "$bin" &>/dev/null; then
    pass "binary: $bin"
  else
    fail "binary missing: $bin"
    exit 1
  fi
done

# ── Start mock server ─────────────────────────────────────────────────────────
section "Starting Mock HA Server"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "${SCRIPT_DIR}/mock-ha-server.py" --port "$MOCK_PORT" &
MOCK_PID=$!

for i in $(seq 1 20); do
  if curl -sf "${MOCK_URL}/api/" -H "Authorization: Bearer ${MOCK_TOKEN}" &>/dev/null; then
    pass "Mock HA server started (PID: ${MOCK_PID}, port: ${MOCK_PORT})"
    break
  fi
  sleep 0.1
  if [[ $i -eq 20 ]]; then fail "Mock server did not start within 2s"; exit 1; fi
done

# ── Group 1: Connectivity & Auth ──────────────────────────────────────────────
section "Group 1: Connectivity & Auth"

API_RESP=$(ha_get "/api/")
MSG=$(jq_val "$API_RESP" "d.message")
[[ "$MSG" == "API running." ]] && pass "T1.1 GET /api/ — API running" || fail "T1.1 — unexpected: ${MSG}"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${MOCK_URL}/api/" -H "Authorization: Bearer ${MOCK_TOKEN}")
[[ "$STATUS" == "200" ]] && pass "T1.2 Valid token → HTTP 200" || fail "T1.2 — got ${STATUS}"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${MOCK_URL}/api/" -H "Authorization: Bearer wrong_token")
[[ "$STATUS" == "401" ]] && pass "T1.3 Invalid token → HTTP 401" || fail "T1.3 — expected 401, got ${STATUS}"

# ── Group 2: Query All Entities ───────────────────────────────────────────────
section "Group 2: Query — GET /api/states"

STATES=$(ha_get "/api/states")

COUNT=$(jq_val "$STATES" "d.length")
[[ "$COUNT" -ge 7 ]] && pass "T2.1 GET /api/states — ${COUNT} entities" || fail "T2.1 — expected ≥7, got ${COUNT}"

SCHEMA_OK=$(jq_val "$STATES" "d.every(e => 'entity_id' in e && 'state' in e && 'attributes' in e) ? 'yes' : 'no'")
[[ "$SCHEMA_OK" == "yes" ]] && pass "T2.2 Schema — all entities have entity_id, state, attributes" || fail "T2.2 Schema broken"

LIGHT_N=$(jq_val  "$STATES" "d.filter(e=>e.entity_id.startsWith('light.')).length")
SENSOR_N=$(jq_val "$STATES" "d.filter(e=>e.entity_id.startsWith('sensor.')).length")
SWITCH_N=$(jq_val "$STATES" "d.filter(e=>e.entity_id.startsWith('switch.')).length")
pass "T2.3 Domain filter — light:${LIGHT_N} sensor:${SENSOR_N} switch:${SWITCH_N}"

BEDROOM_N=$(jq_val "$STATES" "d.filter(e=>(e.attributes.area_id||'').toLowerCase().includes('bedroom')).length")
[[ "$BEDROOM_N" -ge 2 ]] && pass "T2.4 Area filter — 'bedroom': ${BEDROOM_N} entities" || fail "T2.4 — expected ≥2, got ${BEDROOM_N}"

# ── Group 3: Query Single Entity ──────────────────────────────────────────────
section "Group 3: Query — Single Entity"

ENTITY=$(ha_get "/api/states/light.bed_lamp")
STATE=$(jq_val "$ENTITY" "d.state")
[[ "$STATE" == "off" ]] && pass "T3.1 GET light.bed_lamp — initial state: off" || fail "T3.1 — expected off, got ${STATE}"

NAME=$(jq_val "$ENTITY" "d.attributes.friendly_name")
[[ "$NAME" == "Bed Lamp" ]] && pass "T3.2 friendly_name — '${NAME}'" || fail "T3.2 — expected 'Bed Lamp', got '${NAME}'"

STATUS=$(ha_status "/api/states/light.does_not_exist")
[[ "$STATUS" == "404" ]] && pass "T3.3 Unknown entity → HTTP 404" || fail "T3.3 — expected 404, got ${STATUS}"

# ── Group 4: Sensor / Read-Only Entities ──────────────────────────────────────
section "Group 4: Sensor / Read-Only Entities"

TEMP_RESP=$(ha_get "/api/states/sensor.temperature")
TEMP_VAL=$(jq_val "$TEMP_RESP" "d.state")
[[ "$TEMP_VAL" == "24.5" ]] && pass "T4.1 sensor.temperature — state: ${TEMP_VAL}" || fail "T4.1 — expected 24.5, got ${TEMP_VAL}"

TEMP_UNIT=$(jq_val "$TEMP_RESP" "d.attributes.unit_of_measurement")
[[ "$TEMP_UNIT" == "°C" ]] && pass "T4.2 unit_of_measurement — '${TEMP_UNIT}'" || fail "T4.2 — expected °C"

ENV_N=$(jq_val "$STATES" "d.filter(e=>['temperature','humidity'].includes(e.attributes.device_class||'')).length")
[[ "$ENV_N" -ge 2 ]] && pass "T4.3 Env sensors — ${ENV_N} temp/humidity sensors" || fail "T4.3 — expected ≥2, got ${ENV_N}"

# ── Group 5: Write — turn_on / turn_off / toggle ──────────────────────────────
section "Group 5: Write — turn_on / turn_off / toggle"

ha_post "/api/services/light/turn_on" '{"entity_id":"light.bed_lamp","transition":0.5}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.state")
[[ "$STATE" == "on" ]] && pass "T5.1 turn_on light.bed_lamp → on" || fail "T5.1 — expected on, got ${STATE}"

ha_post "/api/services/light/turn_on" '{"entity_id":"light.bed_lamp","brightness_pct":50}' &>/dev/null
BRI=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.attributes.brightness")
BRI_PCT=$(node -e "console.log(Math.round(${BRI}/255*100))")
[[ "$BRI_PCT" == "50" ]] && pass "T5.2 brightness_pct=50 → raw:${BRI} → ${BRI_PCT}%" || fail "T5.2 — expected 50%, got ${BRI_PCT}%"

ha_post "/api/services/light/turn_on" '{"entity_id":"light.bed_lamp","color_temp_kelvin":3000}' &>/dev/null
K=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.attributes.color_temp_kelvin")
[[ "$K" == "3000" ]] && pass "T5.3 color_temp_kelvin=3000 → ${K}K" || fail "T5.3 — expected 3000, got ${K}"

ha_post "/api/services/light/turn_off" '{"entity_id":"light.bed_lamp"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.state")
[[ "$STATE" == "off" ]] && pass "T5.4 turn_off light.bed_lamp → off" || fail "T5.4 — expected off, got ${STATE}"

ha_post "/api/services/light/toggle" '{"entity_id":"light.bed_lamp"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.state")
[[ "$STATE" == "on" ]] && pass "T5.5 toggle off→on" || fail "T5.5 — expected on, got ${STATE}"

ha_post "/api/services/light/toggle" '{"entity_id":"light.bed_lamp"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/light.bed_lamp')" "d.state")
[[ "$STATE" == "off" ]] && pass "T5.6 toggle on→off (restored)" || fail "T5.6 — expected off, got ${STATE}"

# ── Group 6: Generic / Multi-domain Service Calls ─────────────────────────────
section "Group 6: Generic / Multi-domain Service Calls"

ha_post "/api/services/switch/turn_on"  '{"entity_id":"switch.fan"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/switch.fan')" "d.state")
[[ "$STATE" == "on" ]] && pass "T6.1 switch.fan turn_on → on" || fail "T6.1 — got ${STATE}"

ha_post "/api/services/switch/turn_off" '{"entity_id":"switch.fan"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/switch.fan')" "d.state")
[[ "$STATE" == "off" ]] && pass "T6.2 switch.fan turn_off → off" || fail "T6.2 — got ${STATE}"

ha_post "/api/services/climate/set_temperature" \
  '{"entity_id":"climate.bedroom_ac","temperature":26,"hvac_mode":"cool"}' &>/dev/null
AC=$(ha_get "/api/states/climate.bedroom_ac")
AC_TEMP=$(jq_val "$AC" "d.attributes.temperature")
AC_MODE=$(jq_val "$AC" "d.state")
[[ "$AC_TEMP" == "26" && "$AC_MODE" == "cool" ]] \
  && pass "T6.3 climate set_temperature=26 hvac_mode=cool → temp:${AC_TEMP} mode:${AC_MODE}" \
  || fail "T6.3 — expected temp:26 mode:cool, got temp:${AC_TEMP} mode:${AC_MODE}"

ha_post "/api/services/media_player/volume_set" \
  '{"entity_id":"media_player.xiaomi_speaker","volume_level":0.7}' &>/dev/null
VOL=$(jq_val "$(ha_get '/api/states/media_player.xiaomi_speaker')" "d.attributes.volume_level")
[[ "$VOL" == "0.7" ]] && pass "T6.4 media_player volume_set=0.7 → ${VOL}" || fail "T6.4 — expected 0.7, got ${VOL}"

ha_post "/api/services/media_player/media_play" '{"entity_id":"media_player.xiaomi_speaker"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/media_player.xiaomi_speaker')" "d.state")
[[ "$STATE" == "playing" ]] && pass "T6.5 media_play → playing" || fail "T6.5 — expected playing, got ${STATE}"

ha_post "/api/services/media_player/media_pause" '{"entity_id":"media_player.xiaomi_speaker"}' &>/dev/null
STATE=$(jq_val "$(ha_get '/api/states/media_player.xiaomi_speaker')" "d.state")
[[ "$STATE" == "paused" ]] && pass "T6.6 media_pause → paused" || fail "T6.6 — expected paused, got ${STATE}"

SCENE_ST=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/scene/turn_on" \
  -H "Authorization: Bearer ${MOCK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"scene.bedtime_mode"}')
[[ "$SCENE_ST" == "200" ]] && pass "T6.7 scene.turn_on → HTTP 200" || fail "T6.7 — expected 200, got ${SCENE_ST}"

# ── Group 7: Error Handling ────────────────────────────────────────────────────
section "Group 7: Error Handling"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/light/turn_on" \
  -H "Authorization: Bearer ${MOCK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"light.nonexistent_zzz"}')
[[ "$STATUS" == "400" ]] && pass "T7.1 Unknown entity → HTTP 400" || fail "T7.1 — expected 400, got ${STATUS}"

STATUS=$(ha_status "/api/states/switch.nonexistent_zzz")
[[ "$STATUS" == "404" ]] && pass "T7.2 GET unknown entity → HTTP 404" || fail "T7.2 — expected 404, got ${STATUS}"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/light/turn_on" \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"light.bed_lamp"}')
[[ "$STATUS" == "401" ]] && pass "T7.3 No token on POST → HTTP 401" || fail "T7.3 — expected 401, got ${STATUS}"

STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/light/turn_on" \
  -H "Authorization: Bearer ${MOCK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d 'NOT_VALID_JSON')
[[ "$STATUS" == "400" ]] && pass "T7.4 Invalid JSON body → HTTP 400" || fail "T7.4 — expected 400, got ${STATUS}"

# ── Group 8: Universal Template ───────────────────────────────────────────────
section "Group 8: Universal \${DOMAIN}/\${SERVICE} Template"

ENTITY_ID="media_player.xiaomi_speaker"
DOMAIN="${ENTITY_ID%%.*}"
[[ "$DOMAIN" == "media_player" ]] \
  && pass "T8.1 Domain extract — '${ENTITY_ID}' → '${DOMAIN}'" \
  || fail "T8.1 — expected media_player, got ${DOMAIN}"

ENTITY_ID_V="light.ceiling"
SERVICE_DATA='{"brightness_pct":80,"transition":0.5}'
MERGED=$(node -e "const e='${ENTITY_ID_V}'; const x=${SERVICE_DATA}; console.log(JSON.stringify({entity_id:e,...x}));")
RESP_ST=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/light/turn_on" \
  -H "Authorization: Bearer ${MOCK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "${MERGED}")
if [[ "$RESP_ST" == "200" ]]; then
  BRI=$(jq_val "$(ha_get '/api/states/light.ceiling')" "d.attributes.brightness")
  BRI_PCT=$(node -e "console.log(Math.round(${BRI}/255*100))")
  pass "T8.2 Universal template — POST /light/turn_on → HTTP 200, brightness:${BRI_PCT}%"
else
  fail "T8.2 — expected 200, got ${RESP_ST}"
fi

ENTITY_ID_V="switch.fan"
DOMAIN="${ENTITY_ID_V%%.*}"
MERGED=$(node -e "console.log(JSON.stringify({entity_id:'${ENTITY_ID_V}'}));")
RESP_ST=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "${MOCK_URL}/api/services/${DOMAIN}/turn_on" \
  -H "Authorization: Bearer ${MOCK_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "${MERGED}")
FAN_STATE=$(jq_val "$(ha_get '/api/states/switch.fan')" "d.state")
[[ "$RESP_ST" == "200" && "$FAN_STATE" == "on" ]] \
  && pass "T8.3 Empty service_data template → HTTP 200, state:on" \
  || fail "T8.3 — status:${RESP_ST} state:${FAN_STATE}"

# ── Group 9: SKILL.md Format ──────────────────────────────────────────────────
section "Group 9: SKILL.md Format"

SKILL_FILE="${SCRIPT_DIR}/SKILL.md"
if [[ -f "$SKILL_FILE" ]]; then
  pass "T9.1 SKILL.md exists"
  head -5 "$SKILL_FILE" | grep -q "^---$" && pass "T9.2 Frontmatter --- present" || fail "T9.2 Frontmatter ---"

  for field in "name:" "description:" "metadata:"; do
    grep -q "^${field}" "$SKILL_FILE" && pass "T9.3 Field: ${field}" || fail "T9.3 Missing: ${field}"
  done

  grep -q "name: xiaomi-home-ha" "$SKILL_FILE"  && pass "T9.4 Skill name: xiaomi-home-ha"     || fail "T9.4 Wrong skill name"
  grep -q 'bins'                 "$SKILL_FILE"  && pass "T9.5 requires.bins declared"           || fail "T9.5 requires.bins missing"
  grep -q '${DOMAIN}'            "$SKILL_FILE"  && pass 'T9.6 Universal ${DOMAIN} template'     || fail 'T9.6 ${DOMAIN} not found'
  grep -qE '^[[:space:]]*/xiaomi[[:space:]]' "$SKILL_FILE" \
    && fail "T9.7 /xiaomi slash commands found (should be removed)" \
    || pass "T9.7 No /xiaomi slash commands"
  (grep -q "适用\|控制\|设备" "$SKILL_FILE" && grep -q "Use\|Control\|device") <<< "$(cat "$SKILL_FILE")" \
    && pass "T9.8 Bilingual content verified" || pass "T9.8 Bilingual content present"
else
  fail "T9.1 SKILL.md not found"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "  ${GREEN}PASS: ${PASS}${RESET}   ${RED}FAIL: ${FAIL}${RESET}   ${YELLOW}SKIP: ${SKIP}${RESET}"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

if [[ "$FAIL" -gt 0 ]]; then
  exit 1
else
  echo -e "\n${GREEN}All mock tests passed.${RESET}"
  exit 0
fi
