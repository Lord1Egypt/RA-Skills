#!/usr/bin/env bash
# Shared configuration helpers for the shelly-blutrv-manager skill.

set -euo pipefail

ENV_FILES=(
  "${HOME}/.openclaw/skills/.shelly-blutrv-manager.env"
)

load_shelly_skill_env() {
  local env_file
  for env_file in "${ENV_FILES[@]}"; do
    if [[ -f "$env_file" ]]; then
      load_env_file_selective "$env_file"
    fi
  done
}

load_env_file_selective() {
  local env_file="$1"
  local line key value

  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -n "$line" ]] || continue
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" == export\ * ]] && line="${line#export }"
    [[ "$line" == *=* ]] || continue

    key="${line%%=*}"
    value="${line#*=}"

    key="${key#"${key%%[![:space:]]*}"}"
    key="${key%"${key##*[![:space:]]}"}"

    case "$key" in
      SHELLY_*|OPENCLAW_SHELLY_*)
        if [[ "$value" =~ ^\".*\"$ ]] || [[ "$value" =~ ^\'.*\'$ ]]; then
          value="${value:1:${#value}-2}"
        fi
        printf -v "$key" '%s' "$value"
        export "$key"
        ;;
    esac
  done <"$env_file"
}

shelly_default_gateway_ip() {
  printf '%s\n' "${SHELLY_DEFAULT_GATEWAY_IP:-192.168.0.102}"
}

shelly_normalize_alias() {
  local value="${1:-}"
  value="${value,,}"
  value="${value// /-}"
  printf '%s\n' "$value"
}

shelly_gateways_config() {
  printf '%s\n' "${SHELLY_GATEWAYS:-bedroom-gateway|192.168.0.101|deadc0debeef;main-gateway|192.168.0.102|cafebabec0de}"
}

shelly_targets_config() {
  printf '%s\n' "${SHELLY_TARGETS:-schlafzimmer,bedroom,sz|bedroom-gateway|200|cafebabefeed;wohnzimmer,living-room,wz|main-gateway|200|bad0ff1ce123;flur,hallway|main-gateway|202|f00dbabecafe}"
}

# H&T Sensors config (WiFi temperature + humidity sensors)
# Format: alias1,alias2,...|device_id
# Example: schlafzimmer,sz,bedroom|decafbadf00d
shelly_ht_sensors_config() {
  printf '%s\n' "${SHELLY_HT_SENSORS:-}"
}

shelly_gateway_ip_for_key() {
  local gateway_key="$1"
  local config entry key ip gateway_device_id
  config="$(shelly_gateways_config)"

  IFS=';' read -r -a entries <<<"$config"
  local entry
  for entry in "${entries[@]}"; do
    [[ -n "$entry" ]] || continue
    IFS='|' read -r key ip gateway_device_id <<<"$entry"
    if [[ "$key" == "$gateway_key" ]]; then
      printf '%s\n' "$ip"
      return 0
    fi
  done

  return 1
}

shelly_gateway_key_for_ip() {
  local gateway_ip="$1"
  local config entry key ip gateway_device_id
  config="$(shelly_gateways_config)"

  IFS=';' read -r -a entries <<<"$config"
  local entry
  for entry in "${entries[@]}"; do
    [[ -n "$entry" ]] || continue
    IFS='|' read -r key ip gateway_device_id <<<"$entry"
    if [[ "$ip" == "$gateway_ip" ]]; then
      printf '%s\n' "$key"
      return 0
    fi
  done

  return 1
}

shelly_target_record_for_alias() {
  local alias_input normalized_alias alias_list gateway_key trv_id device_id alias_entry normalized_entry
  normalized_alias="$(shelly_normalize_alias "$1")"
  local config
  config="$(shelly_targets_config)"

  IFS=';' read -r -a entries <<<"$config"
  local entry
  for entry in "${entries[@]}"; do
    [[ -n "$entry" ]] || continue
    IFS='|' read -r alias_list gateway_key trv_id device_id <<<"$entry"
    IFS=',' read -r -a aliases <<<"$alias_list"
    local alias_entry
    for alias_entry in "${aliases[@]}"; do
      normalized_entry="$(shelly_normalize_alias "$alias_entry")"
      if [[ "$normalized_entry" == "$normalized_alias" ]]; then
        printf '%s|%s|%s|%s\n' "$alias_list" "$gateway_key" "$trv_id" "$device_id"
        return 0
      fi
    done
  done

  return 1
}

shelly_resolve_target_alias() {
  local alias_input="$1"
  local alias_list gateway_key trv_id device_id gateway_ip

  IFS='|' read -r alias_list gateway_key trv_id device_id <<<"$(shelly_target_record_for_alias "$alias_input")"
  gateway_ip="$(shelly_gateway_ip_for_key "$gateway_key")"
  printf '%s %s %s %s %s\n' "$alias_list" "$gateway_key" "$gateway_ip" "$trv_id" "$device_id"
}

shelly_gateway_device_id_for_ip() {
  local gateway_ip="$1"
  local config entry key ip gateway_device_id
  config="$(shelly_gateways_config)"

  IFS=';' read -r -a entries <<<"$config"
  local entry
  for entry in "${entries[@]}"; do
    [[ -n "$entry" ]] || continue
    IFS='|' read -r key ip gateway_device_id <<<"$entry"
    if [[ "$ip" == "$gateway_ip" ]]; then
      printf '%s\n' "$gateway_device_id"
      return 0
    fi
  done

  return 1
}

# H&T Sensor alias resolution
# Returns: alias_list|device_id
# Example: schlafzimmer,sz,bedroom|decafbadf00d
shelly_ht_record_for_alias() {
  local alias_input normalized_alias alias_list device_id alias_entry normalized_entry
  normalized_alias="$(shelly_normalize_alias "$1")"
  local config
  config="$(shelly_ht_sensors_config)"

  # Return early if no H&T sensors configured
  [[ -n "$config" ]] || return 1

  IFS=';' read -r -a entries <<<"$config"
  local entry
  for entry in "${entries[@]}"; do
    [[ -n "$entry" ]] || continue
    IFS='|' read -r alias_list device_id <<<"$entry"
    IFS=',' read -r -a aliases <<<"$alias_list"
    local alias_entry
    for alias_entry in "${aliases[@]}"; do
      normalized_entry="$(shelly_normalize_alias "$alias_entry")"
      if [[ "$normalized_entry" == "$normalized_alias" ]]; then
        printf '%s|%s\n' "$alias_list" "$device_id"
        return 0
      fi
    done
  done

  return 1
}

# Resolve H&T alias to device_id
# Returns: device_id
shelly_resolve_ht_alias() {
  local alias_input="$1"
  local alias_list device_id

  IFS='|' read -r alias_list device_id <<<"$(shelly_ht_record_for_alias "$alias_input")"
  printf '%s\n' "$device_id"
}