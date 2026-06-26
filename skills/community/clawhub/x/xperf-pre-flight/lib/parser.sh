#!/usr/bin/env bash
# parser.sh — Skippable failure classification and JSON output formatting.

# Associative array: test_id -> pipe-separated skippable failure signatures
declare -A SKIPPABLE_SIGNATURES=(
  ["health.1.11"]="amd peer memory module signature not found|nvidia peer memory module not loaded"
  ["health.1.14"]="unable to read firewall state|firewalld service not found"
  ["health.1.15"]="no gpu pci device detected for pcie link check|pcie link info unavailable"
  ["health.1.16"]="extended capability 000d not found|acs capability not exposed on this platform"
  ["health.1.18"]="cannot get driver information: no such device|no usable network interface found"
  ["health.1.19"]="smbios_entry_point: permission denied|dmidecode: /dev/mem: permission denied|you must be root|ipmitool: command not found|/dev/ipmi0"
  ["health.1.20"]="can't open umad port|cannot get stats strings information: no such device|no usable network interface found"
  ["health.1.21"]="netlink error: operation not permitted|operation not permitted|no usable network interface found"
  ["health.1.22"]="device \"eth0\" does not exist|cannot find device|no usable network interface found"
  ["health.1.23"]="can't open umad port|ib fabric discovery tool not available"
  ["health.1.24"]="mlnx_qos not available|show_gids not available|no usable network interface found"
  ["health.1.25"]="switch validation requires switch_cli_cmd or switch_host"
)

# Classify whether a failure is skippable.
# Args: $1=test_id, $2=combined_output (stdout+stderr)
# Returns: 0 if skippable (prints matched signature), 1 if not skippable
classify_skippable_failure() {
  local test_id="$1"
  local output="$2"
  local sigs="${SKIPPABLE_SIGNATURES[$test_id]:-}"

  [ -z "$sigs" ] && return 1

  local lower_output
  lower_output=$(echo "$output" | tr '[:upper:]' '[:lower:]')

  IFS='|' read -ra sig_array <<< "$sigs"
  for sig in "${sig_array[@]}"; do
    if echo "$lower_output" | grep -qF "$sig"; then
      echo "$sig"
      return 0
    fi
  done
  return 1
}

# JSON helpers — build output without requiring jq at format time
_json_escape() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

# Start the JSON results array — call once at the beginning
json_start() {
  local node_id="${PREFLIGHT_NODE_ID:-$(hostname)}"
  local hostname_val
  hostname_val=$(hostname)
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local gpu_vendor
  gpu_vendor=$(_gpu_vendor 2>/dev/null || echo "unknown")

  cat <<HEADER
{
  "timestamp": "$timestamp",
  "node_id": "$(_json_escape "$node_id")",
  "hostname": "$(_json_escape "$hostname_val")",
  "gpu_vendor": "$gpu_vendor",
HEADER
}

# Format a single check result as a JSON object (no trailing comma)
# Args: $1=id, $2=name, $3=status, $4=exit_code, $5=output, $6=duration_ms, $7=skip_reason
json_check_result() {
  local id="$1" name="$2" status="$3" exit_code="$4" output="$5" duration_ms="$6" skip_reason="${7:-}"

  printf '    {\n'
  printf '      "id": "%s",\n' "$(_json_escape "$id")"
  printf '      "name": "%s",\n' "$(_json_escape "$name")"
  printf '      "status": "%s",\n' "$status"
  printf '      "exit_code": %d,\n' "$exit_code"
  printf '      "output": "%s",\n' "$(_json_escape "$output")"
  printf '      "duration_ms": %d' "$duration_ms"
  if [ -n "$skip_reason" ]; then
    printf ',\n      "skip_reason": "%s"\n' "$(_json_escape "$skip_reason")"
  else
    printf '\n'
  fi
  printf '    }'
}

# Finalize the JSON output with summary stats
# Args: $1=total, $2=passed, $3=failed, $4=skipped, $5=checks_json_array
json_finish() {
  local total="$1" passed="$2" failed="$3" skipped="$4" checks_json="$5"
  local overall="pass"
  [ "$failed" -gt 0 ] && overall="fail"

  cat <<SUMMARY
  "overall_status": "$overall",
  "total_checks": $total,
  "passed": $passed,
  "failed": $failed,
  "skipped": $skipped,
  "checks": [
$checks_json
  ],
  "errors": []
}
SUMMARY
}
