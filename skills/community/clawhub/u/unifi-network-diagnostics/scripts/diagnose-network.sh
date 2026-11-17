#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${OPERATOR_SKILLS_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/operator-skills}"
CONFIG_FILE="${UNIFI_DIAGNOSTICS_CONFIG:-$CONFIG_DIR/unifi-network-diagnostics.json}"
UNIFI_HELPER="${UNIFI_HELPER:-}"
UNIFI_HELPER_SOURCE="unset"
DNS_NAME="${DNS_NAME:-example.com}"
EXTERNAL_PING_TARGET="${EXTERNAL_PING_TARGET:-1.1.1.1}"

errors=()
missing_tools=()

have() {
  command -v "$1" >/dev/null 2>&1
}

add_error() {
  errors+=("$1")
}

array_to_json() {
  if (($# == 0)); then
    printf '[]'
  else
    printf '%s\n' "$@" | jq -R . | jq -cs .
  fi
}

bool_json() {
  if [[ "$1" == "true" ]]; then
    printf 'true'
  else
    printf 'false'
  fi
}

fallback_without_jq() {
  printf '%s\n' '{"schema_version":1,"mode":"read-only","status":"degraded","errors":["missing required tool: jq"],"security":{"redaction":"no raw diagnostic output emitted because jq is unavailable"}}'
}

if ! have jq; then
  fallback_without_jq
  exit 0
fi

discover_unifi_helper() {
  if [[ -n "${UNIFI_HELPER:-}" ]]; then
    UNIFI_HELPER_SOURCE="environment"
    return
  fi

  if [[ -r "$CONFIG_FILE" ]]; then
    local configured_helper
    configured_helper="$(jq -r 'if type == "object" then (.unifi_helper // empty) else empty end' "$CONFIG_FILE" 2>/dev/null || true)"
    if [[ -n "$configured_helper" ]]; then
      UNIFI_HELPER="$configured_helper"
      UNIFI_HELPER_SOURCE="local-config"
      return
    fi
  fi

  if have unifi; then
    UNIFI_HELPER="$(command -v unifi)"
    UNIFI_HELPER_SOURCE="path"
    return
  fi

  UNIFI_HELPER_SOURCE="missing"
}

discover_unifi_helper

for tool in awk date ip sed timeout; do
  if ! have "$tool"; then
    missing_tools+=("$tool")
  fi
done

if ! have timeout; then
  add_error "missing timeout; skipped commands that require bounded execution"
fi

run_capture() {
  local seconds="$1"
  shift

  if ! have timeout; then
    return 127
  fi

  local output
  local status
  set +e
  output="$(timeout "$seconds" "$@" 2>&1)"
  status=$?
  set -e

  printf '%s' "$output"
  return "$status"
}

status_name() {
  local status="$1"
  case "$status" in
    0) printf 'ok' ;;
    124) printf 'timeout' ;;
    127) printf 'missing-command' ;;
    *) printf 'exit-%s' "$status" ;;
  esac
}

sanitize_text() {
  if ! have sed; then
    while IFS= read -r _line; do :; done
    printf '%s\n' '[redaction unavailable]'
    return
  fi

  sed -E \
    -e 's/([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}/[redacted-mac]/g' \
    -e 's/([[:xdigit:]]{2}-){5}[[:xdigit:]]{2}/[redacted-mac]/g' \
    -e 's/([0-9]{1,3}\.){3}[0-9]{1,3}/[redacted-ip]/g' \
    -e 's/([0-9A-Fa-f]{0,4}:){2,}[0-9A-Fa-f:]{0,4}/[redacted-ipv6]/g' \
    -e 's/([Pp]ass(word)?|[Tt]oken|[Ss]ecret|[Cc]ookie|[Aa]uthorization|[Aa]pi[-_]?[Kk]ey)[[:space:]]*[:=][[:space:]]*[^[:space:]]+/\1=[redacted]/g'
}

compact_lines() {
  local limit="${1:-24}"

  if ! have awk; then
    return 0
  fi

  awk -v limit="$limit" '
    NF {
      gsub(/[[:space:]]+/, " ")
      sub(/^ /, "")
      sub(/ $/, "")
      if (length($0) > 240) {
        $0 = substr($0, 1, 237) "..."
      }
      print
      n++
      if (n >= limit) {
        exit
      }
    }
  '
}

line_count() {
  if ! have awk; then
    printf '0'
    return
  fi

  awk 'END { print NR + 0 }'
}

keyword_count() {
  if ! have awk; then
    printf '0'
    return
  fi

  awk '
    {
      line = tolower($0)
      if (line ~ /(offline|disconnected|failed|failure|error|warning|alert|adopting|isolated|degraded|poor|timeout|rogue|unknown|blocked|threat|malware|excessive|high retry|high latency)/) {
        n++
      }
    }
    END { print n + 0 }
  '
}

is_private_ipv4() {
  local ip="$1"
  local old_ifs="$IFS"
  local a b c d

  [[ "$ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1

  IFS=.
  read -r a b c d <<< "$ip"
  IFS="$old_ifs"

  a=$((10#$a))
  b=$((10#$b))
  c=$((10#$c))
  d=$((10#$d))

  ((a <= 255 && b <= 255 && c <= 255 && d <= 255)) || return 1
  ((a == 10 || a == 127 || (a == 172 && b >= 16 && b <= 31) || (a == 192 && b == 168) || (a == 169 && b == 254)))
}

gateway_scope() {
  local gateway="$1"

  if [[ -z "$gateway" ]]; then
    printf 'none'
  elif is_private_ipv4 "$gateway"; then
    printf 'private'
  else
    printf 'public'
  fi
}

parse_packet_loss() {
  if ! have awk; then
    printf ''
    return
  fi

  awk -F',' '
    /packet loss/ {
      for (i = 1; i <= NF; i++) {
        if ($i ~ /packet loss/) {
          gsub(/[^0-9.]/, "", $i)
          print $i
          exit
        }
      }
    }
  '
}

parse_rtt_avg() {
  if ! have awk; then
    printf ''
    return
  fi

  awk -F'/' '
    /(rtt|round-trip).*=/ {
      avg = $5
      gsub(/[^0-9.]/, "", avg)
      print avg
      exit
    }
  '
}

now_utc="$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || printf 'unknown')"

unifi_devices_ok=false
unifi_devices_status="not-run"
unifi_devices_lines=0
unifi_devices_flags=0
unifi_devices_sample=""

unifi_clients_ok=false
unifi_clients_status="not-run"
unifi_clients_lines=0
unifi_clients_flags=0
unifi_clients_sample=""
unifi_helper_configured=false
unifi_helper_usable=false

if [[ -n "$UNIFI_HELPER" ]]; then
  unifi_helper_configured=true
fi

if [[ -n "$UNIFI_HELPER" && -x "$UNIFI_HELPER" ]]; then
  unifi_helper_usable=true
fi

if [[ "$unifi_helper_usable" != "true" ]]; then
  add_error "missing or non-executable UniFi helper; set UNIFI_HELPER or run local config discovery"
elif have timeout; then
  devices_status_code=0
  devices_raw=""
  if devices_raw="$(run_capture 12 "$UNIFI_HELPER" devices)"; then
    unifi_devices_ok=true
  else
    devices_status_code=$?
    add_error "unifi devices failed: $(status_name "$devices_status_code")"
  fi
  unifi_devices_status="$(status_name "$devices_status_code")"
  unifi_devices_lines="$(printf '%s\n' "$devices_raw" | line_count)"
  unifi_devices_flags="$(printf '%s\n' "$devices_raw" | sanitize_text | keyword_count)"
  unifi_devices_sample="$(printf '%s\n' "$devices_raw" | sanitize_text | compact_lines 24)"

  clients_status_code=0
  clients_raw=""
  if clients_raw="$(run_capture 12 "$UNIFI_HELPER" clients-summary)"; then
    unifi_clients_ok=true
  else
    clients_status_code=$?
    add_error "unifi clients-summary failed: $(status_name "$clients_status_code")"
  fi
  unifi_clients_status="$(status_name "$clients_status_code")"
  unifi_clients_lines="$(printf '%s\n' "$clients_raw" | line_count)"
  unifi_clients_flags="$(printf '%s\n' "$clients_raw" | sanitize_text | keyword_count)"
  unifi_clients_sample="$(printf '%s\n' "$clients_raw" | sanitize_text | compact_lines 24)"
fi

route_ok=false
route_status="not-run"
route_gateway=""
route_gateway_scope="none"
route_dev=""
route_gateway_present=false
route_dev_present=false

if have ip && have awk; then
  route_raw=""
  route_status_code=0
  if route_raw="$(run_capture 3 ip -4 route show default)"; then
    route_ok=true
  else
    route_status_code=$?
    add_error "default route check failed: $(status_name "$route_status_code")"
  fi
  route_status="$(status_name "$route_status_code")"
  route_gateway="$(printf '%s\n' "$route_raw" | awk 'NR == 1 { for (i = 1; i <= NF; i++) { if ($i == "via") { print $(i + 1); exit } } }')"
  route_dev="$(printf '%s\n' "$route_raw" | awk 'NR == 1 { for (i = 1; i <= NF; i++) { if ($i == "dev") { print $(i + 1); exit } } }')"
  route_gateway_scope="$(gateway_scope "$route_gateway")"
  if [[ -n "$route_gateway" ]]; then
    route_gateway_present=true
  fi
  if [[ -n "$route_dev" ]]; then
    route_dev_present=true
  fi
else
  add_error "missing ip or awk; skipped default route check"
fi

gateway_ping_ok=false
gateway_ping_status="not-run"
gateway_packet_loss=""
gateway_rtt_avg=""

if [[ -n "${route_gateway:-}" ]] && have ping && have timeout; then
  gateway_status_code=0
  gateway_ping_raw=""
  if gateway_ping_raw="$(run_capture 8 ping -n -c 3 -W 2 "$route_gateway")"; then
    gateway_ping_ok=true
  else
    gateway_status_code=$?
    add_error "gateway reachability failed: $(status_name "$gateway_status_code")"
  fi
  gateway_ping_status="$(status_name "$gateway_status_code")"
  gateway_packet_loss="$(printf '%s\n' "$gateway_ping_raw" | parse_packet_loss)"
  gateway_rtt_avg="$(printf '%s\n' "$gateway_ping_raw" | parse_rtt_avg)"
elif [[ -z "${route_gateway:-}" ]]; then
  add_error "no default gateway found; skipped gateway reachability"
elif ! have ping; then
  missing_tools+=("ping")
  add_error "missing ping; skipped gateway reachability"
fi

dns_ok=false
dns_status="not-run"
dns_method="none"
dns_query_ms=""

if have timeout && have dig; then
  dns_method="dig"
  dns_status_code=0
  dns_raw=""
  if dns_raw="$(run_capture 5 dig +tries=1 +time=2 +noall +stats "$DNS_NAME")"; then
    dns_ok=true
  else
    dns_status_code=$?
    add_error "DNS resolution failed with dig: $(status_name "$dns_status_code")"
  fi
  dns_status="$(status_name "$dns_status_code")"
  dns_query_ms="$(printf '%s\n' "$dns_raw" | awk '/Query time:/ { print $4; exit }')"
elif have timeout && have getent; then
  dns_method="getent"
  dns_status_code=0
  start_ms="$(date +%s%3N 2>/dev/null || date +%s)"
  if run_capture 5 getent hosts "$DNS_NAME" >/dev/null; then
    dns_ok=true
  else
    dns_status_code=$?
    add_error "DNS resolution failed with getent: $(status_name "$dns_status_code")"
  fi
  end_ms="$(date +%s%3N 2>/dev/null || date +%s)"
  dns_status="$(status_name "$dns_status_code")"
  if [[ "$start_ms" =~ ^[0-9]+$ && "$end_ms" =~ ^[0-9]+$ && "$end_ms" -ge "$start_ms" ]]; then
    dns_query_ms="$((end_ms - start_ms))"
  fi
else
  add_error "missing dig/getent or timeout; skipped DNS resolution timing"
fi

external_ping_ok=false
external_ping_status="not-run"
external_packet_loss=""
external_rtt_avg=""

if have ping && have timeout; then
  external_status_code=0
  external_ping_raw=""
  if external_ping_raw="$(run_capture 10 ping -n -c 5 -W 2 "$EXTERNAL_PING_TARGET")"; then
    external_ping_ok=true
  else
    external_status_code=$?
    add_error "external packet-loss probe failed: $(status_name "$external_status_code")"
  fi
  external_ping_status="$(status_name "$external_status_code")"
  external_packet_loss="$(printf '%s\n' "$external_ping_raw" | parse_packet_loss)"
  external_rtt_avg="$(printf '%s\n' "$external_ping_raw" | parse_rtt_avg)"
elif ! have ping; then
  missing_tools+=("ping")
  add_error "missing ping; skipped external packet-loss probe"
fi

missing_tools_json="$(array_to_json "${missing_tools[@]}")"
errors_json="$(array_to_json "${errors[@]}")"

jq -cn \
  --arg generated_at "$now_utc" \
  --argjson missing_tools "$missing_tools_json" \
  --argjson errors "$errors_json" \
  --argjson unifi_helper_configured "$(bool_json "$unifi_helper_configured")" \
  --argjson unifi_helper_usable "$(bool_json "$unifi_helper_usable")" \
  --arg unifi_helper_source "$UNIFI_HELPER_SOURCE" \
  --argjson unifi_devices_ok "$(bool_json "$unifi_devices_ok")" \
  --arg unifi_devices_status "$unifi_devices_status" \
  --arg unifi_devices_lines "$unifi_devices_lines" \
  --arg unifi_devices_flags "$unifi_devices_flags" \
  --arg unifi_devices_sample "$unifi_devices_sample" \
  --argjson unifi_clients_ok "$(bool_json "$unifi_clients_ok")" \
  --arg unifi_clients_status "$unifi_clients_status" \
  --arg unifi_clients_lines "$unifi_clients_lines" \
  --arg unifi_clients_flags "$unifi_clients_flags" \
  --arg unifi_clients_sample "$unifi_clients_sample" \
  --argjson route_ok "$(bool_json "$route_ok")" \
  --arg route_status "$route_status" \
  --arg route_gateway_scope "$route_gateway_scope" \
  --argjson route_gateway_present "$(bool_json "$route_gateway_present")" \
  --argjson route_dev_present "$(bool_json "$route_dev_present")" \
  --argjson gateway_ping_ok "$(bool_json "$gateway_ping_ok")" \
  --arg gateway_ping_status "$gateway_ping_status" \
  --arg gateway_packet_loss "$gateway_packet_loss" \
  --arg gateway_rtt_avg "$gateway_rtt_avg" \
  --argjson dns_ok "$(bool_json "$dns_ok")" \
  --arg dns_status "$dns_status" \
  --arg dns_method "$dns_method" \
  --arg dns_query_ms "$dns_query_ms" \
  --argjson external_ping_ok "$(bool_json "$external_ping_ok")" \
  --arg external_ping_status "$external_ping_status" \
  --arg external_packet_loss "$external_packet_loss" \
  --arg external_rtt_avg "$external_rtt_avg" \
  '
  def maybe_number($value):
    if ($value | length) == 0 then null else ($value | tonumber?) end;
  def sample_lines($value):
    $value | split("\n") | map(select(length > 0));

  {
    schema_version: 1,
    generated_at: $generated_at,
    mode: "read-only",
    security: {
      secrets_emitted: false,
      mac_addresses_emitted: false,
      public_wan_ips_emitted: false,
      local_paths_emitted: false,
      private_topology_emitted: false,
      redaction: "helper output is sanitized before inclusion; raw ping, DNS, route outputs, helper paths, gateway addresses, and DNS names are not emitted"
    },
    tools: {
      missing: $missing_tools
    },
    unifi: {
      helper: {
        configured: $unifi_helper_configured,
        usable: $unifi_helper_usable,
        source: $unifi_helper_source,
        path_emitted: false
      },
      devices: {
        ok: $unifi_devices_ok,
        status: $unifi_devices_status,
        line_count: maybe_number($unifi_devices_lines),
        flagged_line_count: maybe_number($unifi_devices_flags),
        sample: sample_lines($unifi_devices_sample)
      },
      clients_summary: {
        ok: $unifi_clients_ok,
        status: $unifi_clients_status,
        line_count: maybe_number($unifi_clients_lines),
        flagged_line_count: maybe_number($unifi_clients_flags),
        sample: sample_lines($unifi_clients_sample)
      }
    },
    network: {
      default_route: {
        ok: $route_ok,
        status: $route_status,
        gateway_present: $route_gateway_present,
        gateway_scope: $route_gateway_scope,
        gateway_value_emitted: false,
        interface_present: $route_dev_present
      },
      gateway_reachability: {
        ok: $gateway_ping_ok,
        status: $gateway_ping_status,
        packet_loss_percent: maybe_number($gateway_packet_loss),
        rtt_avg_ms: maybe_number($gateway_rtt_avg)
      },
      dns_resolution: {
        ok: $dns_ok,
        status: $dns_status,
        method: $dns_method,
        target: "dns-probe",
        name_emitted: false,
        query_time_ms: maybe_number($dns_query_ms)
      },
      external_packet_loss_latency: {
        ok: $external_ping_ok,
        status: $external_ping_status,
        target: "external-probe",
        packet_loss_percent: maybe_number($external_packet_loss),
        rtt_avg_ms: maybe_number($external_rtt_avg)
      }
    },
    errors: $errors
  }'
