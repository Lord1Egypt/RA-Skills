#!/usr/bin/env bash
# preflight.sh — Main orchestrator for GPU cluster node pre-flight health checks.
#
# Runs all 26 health checks locally on a bare-metal GPU node.
# Cross-node checks (1.1, 1.25, 1.26, mesh_ping) only run when PREFLIGHT_PEER_IPS is set.
#
# Environment variables:
#   PREFLIGHT_NODE_ID    — Node identifier (default: hostname)
#   PREFLIGHT_CHECKS     — Comma-separated subset of checks to run (e.g. "1.2,1.3,1.5")
#   PREFLIGHT_STRICT     — "true" to treat skippable failures as errors (default: false)
#   PREFLIGHT_PEER_IPS   — Comma-separated peer IPs for cross-node checks
#   MOUNT_POINT          — Shared filesystem mount point for check 1.10
#   SWITCH_HOST          — Switch hostname for check 1.25
#   SWITCH_CLI_CMD       — Direct switch CLI command for check 1.25
#   SWITCH_USER          — Switch SSH user (default: admin)
#   SWITCH_SHOW_CMD      — Switch show command (default: "show interface status")
#
# Output: JSON to stdout, diagnostics to stderr
# Exit codes: 0 = all pass/skip, 1 = failures detected, 2 = config error
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source libraries
# shellcheck source=lib/helpers.sh
source "$SCRIPT_DIR/lib/helpers.sh"
# shellcheck source=lib/checks.sh
source "$SCRIPT_DIR/lib/checks.sh"
# shellcheck source=lib/parser.sh
source "$SCRIPT_DIR/lib/parser.sh"

# --- Configuration ---
STRICT="${PREFLIGHT_STRICT:-false}"
SELECTED_CHECKS="${PREFLIGHT_CHECKS:-}"

# Check ID -> function name + display name
declare -A CHECK_FUNCS=(
  ["health.1.1"]="check_1_1"
  ["health.1.2"]="check_1_2"
  ["health.1.3"]="check_1_3"
  ["health.1.4"]="check_1_4"
  ["health.1.5"]="check_1_5"
  ["health.1.6"]="check_1_6"
  ["health.1.7"]="check_1_7"
  ["health.1.8"]="check_1_8"
  ["health.1.9"]="check_1_9"
  ["health.1.10"]="check_1_10"
  ["health.1.11"]="check_1_11"
  ["health.1.12"]="check_1_12"
  ["health.1.13"]="check_1_13"
  ["health.1.14"]="check_1_14"
  ["health.1.15"]="check_1_15"
  ["health.1.16"]="check_1_16"
  ["health.1.17"]="check_1_17"
  ["health.1.18"]="check_1_18"
  ["health.1.19"]="check_1_19"
  ["health.1.20"]="check_1_20"
  ["health.1.21"]="check_1_21"
  ["health.1.22"]="check_1_22"
  ["health.1.23"]="check_1_23"
  ["health.1.24"]="check_1_24"
  ["health.1.25"]="check_1_25"
  ["health.1.26"]="check_1_26"
  ["network.l3_mesh_ping"]="check_mesh_ping"
)

declare -A CHECK_NAMES=(
  ["health.1.1"]="SSH Connectivity"
  ["health.1.2"]="Docker Service"
  ["health.1.3"]="GPU Detection"
  ["health.1.4"]="GPU Count and Model"
  ["health.1.5"]="GPU Driver Version"
  ["health.1.6"]="OS and Kernel Version"
  ["health.1.7"]="Network Type Detection"
  ["health.1.8"]="IB/NIC Ports Up"
  ["health.1.9"]="GPU Container Toolkit"
  ["health.1.10"]="Shared File System"
  ["health.1.11"]="GPUDirect Kernel Module"
  ["health.1.12"]="IOMMU Passthrough"
  ["health.1.13"]="NUMA Balancing"
  ["health.1.14"]="Firewall Disabled"
  ["health.1.15"]="PCIe Link Speed/Width"
  ["health.1.16"]="PCIe ACS Disabled"
  ["health.1.17"]="GPU-NIC PCIe Affinity"
  ["health.1.18"]="NIC Firmware Version"
  ["health.1.19"]="BIOS Settings"
  ["health.1.20"]="Link Quality/Errors"
  ["health.1.21"]="Transceiver Health"
  ["health.1.22"]="MTU Configuration"
  ["health.1.23"]="Fabric Topology"
  ["health.1.24"]="RoCE QoS/NIC Config"
  ["health.1.25"]="Switch QoS"
  ["health.1.26"]="Network Routing"
  ["network.l3_mesh_ping"]="L3 Mesh Ping"
)

# Default run order (local checks first, cross-node checks last)
DEFAULT_ORDER=(
  "health.1.6" "health.1.2" "health.1.3" "health.1.4" "health.1.5"
  "health.1.7" "health.1.8" "health.1.9" "health.1.10" "health.1.11"
  "health.1.12" "health.1.13" "health.1.14" "health.1.15" "health.1.16"
  "health.1.17" "health.1.18" "health.1.19" "health.1.20" "health.1.21"
  "health.1.22" "health.1.23" "health.1.24"
  "health.1.1" "health.1.25" "health.1.26" "network.l3_mesh_ping"
)

# --- Build check list ---
declare -a RUN_ORDER=()

if [ -n "$SELECTED_CHECKS" ]; then
  IFS=',' read -ra selected <<< "$SELECTED_CHECKS"
  for check in "${selected[@]}"; do
    check=$(echo "$check" | xargs)
    # Allow shorthand "1.3" -> "health.1.3"
    [[ "$check" =~ ^[0-9] ]] && check="health.$check"
    if [ -z "${CHECK_FUNCS[$check]:-}" ]; then
      echo "Unknown check: $check" >&2
      exit 2
    fi
    RUN_ORDER+=("$check")
  done
else
  RUN_ORDER=("${DEFAULT_ORDER[@]}")
fi

# --- Run checks ---
total=0
passed=0
failed=0
skipped=0
checks_json=""

for check_id in "${RUN_ORDER[@]}"; do
  func="${CHECK_FUNCS[$check_id]}"
  name="${CHECK_NAMES[$check_id]}"

  echo ">>> Running $check_id ($name)..." >&2

  # Capture output and timing
  start_ms=$(date +%s%N 2>/dev/null || echo 0)
  set +e
  output=$($func 2>&1)
  exit_code=$?
  set -e
  end_ms=$(date +%s%N 2>/dev/null || echo 0)

  # Calculate duration
  if [ "$start_ms" != "0" ] && [ "$end_ms" != "0" ]; then
    duration_ms=$(( (end_ms - start_ms) / 1000000 ))
  else
    duration_ms=0
  fi

  # Classify result
  status="pass"
  skip_reason=""

  if [ "$exit_code" -eq 3 ]; then
    # Exit code 3 = explicitly skipped (cross-node check without peers)
    status="skip"
    skip_reason="cross-node check skipped (no peer IPs configured)"
  elif [ "$exit_code" -ne 0 ]; then
    # Check for skippable failure signatures
    if [ "$STRICT" != "true" ]; then
      skip_reason=$(classify_skippable_failure "$check_id" "$output" 2>/dev/null || true)
      if [ -n "$skip_reason" ]; then
        status="skip"
      else
        status="fail"
      fi
    else
      status="fail"
    fi
  fi

  # Update counters
  total=$((total + 1))
  case "$status" in
    pass) passed=$((passed + 1)); echo "    PASS" >&2 ;;
    skip) skipped=$((skipped + 1)); echo "    SKIP: $skip_reason" >&2 ;;
    fail) failed=$((failed + 1)); echo "    FAIL (exit=$exit_code)" >&2 ;;
  esac

  # Build JSON entry
  entry=$(json_check_result "$check_id" "$name" "$status" "$exit_code" "$output" "$duration_ms" "$skip_reason")

  if [ -n "$checks_json" ]; then
    checks_json="${checks_json},
${entry}"
  else
    checks_json="$entry"
  fi
done

# --- Output final JSON ---
json_start
json_finish "$total" "$passed" "$failed" "$skipped" "$checks_json"

# --- Exit code ---
if [ "$failed" -gt 0 ]; then
  echo ">>> RESULT: $failed/$total checks failed" >&2
  exit 1
else
  echo ">>> RESULT: All $total checks passed ($skipped skipped)" >&2
  exit 0
fi
