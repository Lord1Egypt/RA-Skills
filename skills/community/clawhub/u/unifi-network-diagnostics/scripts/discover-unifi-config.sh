#!/usr/bin/env bash
set -euo pipefail

WRITE_CONFIG=false
SHOW_PATHS=false
EXPLICIT_HELPER="${UNIFI_HELPER:-}"
CONFIG_DIR="${OPERATOR_SKILLS_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/operator-skills}"
CONFIG_FILE="${UNIFI_DIAGNOSTICS_CONFIG:-$CONFIG_DIR/unifi-network-diagnostics.json}"

errors=()

usage() {
  cat <<'USAGE'
Usage: discover-unifi-config.sh [--helper PATH] [--write] [--show-paths]

Discovers a local read-only UniFi helper for UniFi diagnostics. By default, output
redacts full local paths. Use --write only after owner approval.
USAGE
}

while (($# > 0)); do
  case "$1" in
    --helper)
      shift
      if (($# == 0)); then
        printf '%s\n' "missing value for --helper" >&2
        exit 2
      fi
      EXPLICIT_HELPER="$1"
      ;;
    --write)
      WRITE_CONFIG=true
      ;;
    --show-paths)
      SHOW_PATHS=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

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

path_label() {
  local path="$1"

  if [[ "$SHOW_PATHS" == "true" ]]; then
    printf '%s' "$path"
  else
    basename -- "$path"
  fi
}

fallback_without_jq() {
  printf '%s\n' '{"schema_version":1,"mode":"read-only","status":"degraded","errors":["missing required tool: jq"],"security":{"local_paths_emitted":false,"secrets_emitted":false}}'
}

if ! have jq; then
  fallback_without_jq
  exit 0
fi

candidate_paths=()
candidate_sources=()

add_candidate() {
  local source="$1"
  local path="$2"

  [[ -n "$path" ]] || return

  local existing
  for existing in "${candidate_paths[@]}"; do
    if [[ "$existing" == "$path" ]]; then
      return
    fi
  done

  candidate_paths+=("$path")
  candidate_sources+=("$source")
}

if [[ -n "$EXPLICIT_HELPER" ]]; then
  add_candidate "explicit" "$EXPLICIT_HELPER"
fi

if have unifi; then
  add_candidate "path" "$(command -v unifi)"
fi

for path in "$HOME/bin/unifi" "$HOME/.local/bin/unifi" "/usr/local/bin/unifi" "/usr/bin/unifi"; do
  if [[ -e "$path" ]]; then
    add_candidate "common-location" "$path"
  fi
done

selected_path=""
selected_source="missing"
selected_usable=false
sites_ok=false
devices_ok=false
clients_summary_ok=false

for index in "${!candidate_paths[@]}"; do
  path="${candidate_paths[$index]}"
  source="${candidate_sources[$index]}"

  if [[ -x "$path" ]]; then
    selected_path="$path"
    selected_source="$source"
    selected_usable=true
    break
  fi
done

if [[ -z "$selected_path" ]]; then
  add_error "no executable UniFi helper discovered"
elif have timeout; then
  if timeout 8 "$selected_path" sites >/dev/null 2>&1; then
    sites_ok=true
  fi
  if timeout 8 "$selected_path" devices >/dev/null 2>&1; then
    devices_ok=true
  fi
  if timeout 8 "$selected_path" clients-summary >/dev/null 2>&1; then
    clients_summary_ok=true
  fi
else
  add_error "missing timeout; skipped helper capability probes"
fi

config_written=false
if [[ "$WRITE_CONFIG" == "true" ]]; then
  if [[ "$selected_usable" != "true" || -z "$selected_path" ]]; then
    add_error "not writing config because no usable helper was discovered"
  else
    mkdir -p "$CONFIG_DIR"
    tmp_file="${CONFIG_FILE}.tmp"
    jq -n \
      --arg helper "$selected_path" \
      --arg updated_at "$(date -u +'%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || printf 'unknown')" \
      '{
        schema_version: 1,
        unifi_helper: $helper,
        updated_at: $updated_at,
        contains_secrets: false,
        note: "Local Operator config. Do not commit."
      }' > "$tmp_file"
    chmod 600 "$tmp_file" 2>/dev/null || true
    mv "$tmp_file" "$CONFIG_FILE"
    config_written=true
  fi
fi

errors_json="$(array_to_json "${errors[@]}")"
selected_label=""
if [[ -n "$selected_path" ]]; then
  selected_label="$(path_label "$selected_path")"
fi

jq -cn \
  --argjson errors "$errors_json" \
  --argjson candidate_count "${#candidate_paths[@]}" \
  --arg selected_label "$selected_label" \
  --arg selected_source "$selected_source" \
  --argjson selected_usable "$selected_usable" \
  --argjson sites_ok "$sites_ok" \
  --argjson devices_ok "$devices_ok" \
  --argjson clients_summary_ok "$clients_summary_ok" \
  --argjson write_requested "$WRITE_CONFIG" \
  --argjson config_written "$config_written" \
  --argjson local_paths_emitted "$SHOW_PATHS" \
  '{
    schema_version: 1,
    mode: (if $write_requested then "local-config-write" else "read-only-discovery" end),
    security: {
      secrets_emitted: false,
      local_paths_emitted: $local_paths_emitted,
      private_topology_emitted: false,
      credentials_stored: false
    },
    unifi_helper: {
      candidate_count: $candidate_count,
      selected: ($selected_label | length > 0),
      selected_label: (if ($selected_label | length) == 0 then null else $selected_label end),
      source: $selected_source,
      usable: $selected_usable,
      capabilities: {
        sites: $sites_ok,
        devices: $devices_ok,
        clients_summary: $clients_summary_ok
      }
    },
    remembered_config: {
      written: $config_written,
      location_emitted: false,
      contains_secrets: false
    },
    errors: $errors
  }'
