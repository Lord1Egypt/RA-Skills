#!/usr/bin/env bash
# BluTRV Thermostat Control via Shelly Gateway G3
# Supports: temp, boost, override, calibrate, info, firmware-check, firmware-update

set -euo pipefail

# =============================================================================
# ALIAS RESOLUTION
# =============================================================================

resolve_gateway_alias() {
  local alias="$1"
  
  # If it's an IP address, return as-is
  if [[ "$alias" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "$alias"
    return 0
  fi
  
  # Load aliases from config
  if [[ -f ~/.openclaw/skills/.shelly-blutrv-manager.env ]]; then
    source ~/.openclaw/skills/.shelly-blutrv-manager.env
  fi
  
  # Check SHELLY_GATEWAYS for alias
  if [[ -n "${SHELLY_GATEWAYS:-}" ]]; then
    local gateway_ip
    gateway_ip=$(echo "$SHELLY_GATEWAYS" | tr ',' '\n' | grep "^${alias}:" | cut -d: -f2)
    if [[ -n "$gateway_ip" ]]; then
      echo "$gateway_ip"
      return 0
    fi
  fi
  
  # Fallback to alias name (might be a hostname)
  echo "$alias"
}

# =============================================================================
# SUBCOMMANDS
# =============================================================================

cmd_temp() {
  local gateway_ip="$1"
  local trv_id="$2"
  local target_temp="$3"
  
  echo "Setting BluTRV $trv_id to ${target_temp}°C via gateway $gateway_ip..."
  
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.SetTarget\",\"params\":{\"id\":0,\"target_C\":${target_temp}}}}")
  
  echo "Gateway response: $response"
  
  echo "Waiting 3 seconds for BluTRV to process..."
  sleep 3
  
  echo ""
  echo "Verifying applied target..."
  cmd_status "$gateway_ip" "$trv_id"
  
  # Verify the target was applied
  local actual_target
  actual_target=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.GetRemoteStatus\",\"params\":{\"id\":${trv_id}}}" | jq -r '.result.status["trv:0"].target_C // empty')
  
  if [[ -n "$actual_target" ]]; then
    if (( $(echo "$actual_target == $target_temp" | bc -l 2>/dev/null || echo "0") )); then
      echo "✓ Target verified: ${actual_target}°C"
    else
      echo "⚠ Target mismatch: expected ${target_temp}°C, got ${actual_target}°C"
    fi
  fi
}

cmd_boost() {
  local gateway_ip="$1"
  local trv_id="$2"
  local duration="${3:-1800}"  # Default 30 min
  
  echo "Activating boost mode for BluTRV $trv_id (${duration}s) via gateway $gateway_ip..."
  
  # Boost = TRV.SetBoost with boost_enable=true and boost_reason=manual
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.SetBoost\",\"params\":{\"id\":0,\"boost_enable\":true,\"boost_reason\":\"manual\"}}}")
  
  echo "Gateway response: $response"
  
  echo ""
  echo "Current status:"
  cmd_status "$gateway_ip" "$trv_id"
}

cmd_boost_clear() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Clearing boost mode for BluTRV $trv_id via gateway $gateway_ip..."
  
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.SetBoost\",\"params\":{\"id\":0,\"boost_enable\":false}}}")
  
  echo "Gateway response: $response"
}

cmd_override() {
  local gateway_ip="$1"
  local trv_id="$2"
  local target_temp="$3"
  local duration="${4:-1800}"  # Default 30 min
  
  echo "Setting override for BluTRV $trv_id to ${target_temp}°C for ${duration}s via gateway $gateway_ip..."
  
  # Override = TRV.SetTarget with schedule override
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.SetTarget\",\"params\":{\"id\":0,\"target_C\":${target_temp}}}}")
  
  echo "Gateway response: $response"
  
  echo ""
  echo "Current status:"
  cmd_status "$gateway_ip" "$trv_id"
  
  echo ""
  echo "Note: Override will revert after ${duration}s (schedule resumes automatically)"
}

cmd_override_clear() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Clearing override for BluTRV $trv_id via gateway $gateway_ip..."
  
  # Clear override = resume schedule
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.SetTarget\",\"params\":{\"id\":0,\"target_C\":null}}}")
  
  echo "Gateway response: $response"
}

cmd_calibrate() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Starting calibration for BluTRV $trv_id via gateway $gateway_ip..."
  
  # Calibration = TRV.Calibrate
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.Call\",\"params\":{\"id\":${trv_id},\"method\":\"TRV.Calibrate\",\"params\":{\"id\":0}}}")
  
  echo "Gateway response: $response"
  
  echo ""
  echo "Calibration initiated. This may take several minutes..."
}

cmd_status() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.GetRemoteStatus\",\"params\":{\"id\":${trv_id}}}" | jq '.result.status["trv:0"] | {target_C, current_C, pos, errors}'
}

cmd_info() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Device info for BluTRV $trv_id via gateway $gateway_ip..."
  
  curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.GetRemoteDeviceInfo\",\"params\":{\"id\":${trv_id}}}" | jq '.result.device_info'
}

cmd_firmware_check() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Checking for firmware updates for BluTRV $trv_id via gateway $gateway_ip..."
  
  curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.CheckForUpdates\"}" | jq '.'
}

cmd_firmware_update() {
  local gateway_ip="$1"
  local trv_id="$2"
  
  echo "Starting firmware update for BluTRV $trv_id via gateway $gateway_ip..."
  
  local response
  response=$(curl -s -m 10 -X POST "http://${gateway_ip}/rpc" \
    -H "Content-Type: application/json" \
    -d "{\"id\":1,\"method\":\"BluTrv.UpdateFirmware\",\"params\":{\"id\":${trv_id}}}")
  
  echo "Gateway response: $response"
  
  echo ""
  echo "Firmware update initiated. This may take several minutes via Bluetooth..."
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

usage() {
  echo "Usage: $0 <gateway_alias|ip> <trv_id> <command> [options]"
  echo ""
  echo "Commands:"
  echo "  temp <temp>              Set target temperature (°C)"
  echo "  boost [--clear]          Activate boost mode (30min default)"
  echo "  override <temp> [dur]   Override schedule with temp for duration (default 1800s)"
  echo "                           Use --clear to cancel override"
  echo "  calibrate                Start valve calibration"
  echo "  status                   Show current status"
  echo "  info                     Show device info (firmware version)"
  echo "  firmware-check           Check for firmware updates"
  echo "  firmware-update          Start firmware update"
  echo ""
  echo "Examples:"
  echo "  $0 sz 200 temp 21              Set Schlafzimmer TRV to 21°C"
  echo "  $0 sz 200 boost                Activate boost mode"
  echo "  $0 sz 200 override 22          Override to 22°C for 30min"
  echo "  $0 sz 200 calibrate            Start calibration"
  echo "  $0 sz 200 info                 Show firmware version"
  echo ""
  echo "Legacy syntax (still supported):"
  echo "  $0 <gateway_ip> <trv_id> <temp>   Set temperature directly"
  echo ""
  
  # Show available aliases
  if [[ -f ~/.openclaw/skills/.shelly-blutrv-manager.env ]]; then
    source ~/.openclaw/skills/.shelly-blutrv-manager.env
    if [[ -n "${SHELLY_GATEWAYS:-}" ]]; then
      echo "Available gateway aliases:"
      echo "$SHELLY_GATEWAYS" | tr ',' '\n' | while read -r entry; do
        alias_name=$(echo "$entry" | cut -d: -f1)
        ip=$(echo "$entry" | cut -d: -f2)
        echo "  $alias_name -> $ip"
      done
    fi
    if [[ -n "${SHELLY_TARGETS:-}" ]]; then
      echo ""
      echo "Available BluTRV aliases:"
      echo "$SHELLY_TARGETS" | tr ',' '\n' | while read -r entry; do
        alias_name=$(echo "$entry" | cut -d: -f1)
        gateway=$(echo "$entry" | cut -d: -f2)
        trv=$(echo "$entry" | cut -d: -f3)
        echo "  $alias_name -> gateway=$gateway trv_id=$trv"
      done
    fi
  fi
  
  exit 1
}

# Legacy mode: $0 gateway_ip trv_id temp
handle_legacy() {
  local gateway="$1"
  local trv_id="$2"
  local temp="$3"
  
  local gateway_ip
  gateway_ip=$(resolve_gateway_alias "$gateway")
  
  echo "Note: Using legacy syntax. Consider using: $0 <target> temp <temp>" >&2
  cmd_temp "$gateway_ip" "$trv_id" "$temp"
}

# =============================================================================
# MAIN
# =============================================================================

if [[ $# -lt 2 ]]; then
  usage
fi

# Parse arguments
gateway="$1"
trv_id="$2"
command="${3:-}"
shift 2 || true

# Resolve gateway alias to IP
gateway_ip=$(resolve_gateway_alias "$gateway")

# If no command or command is a number, assume legacy mode
if [[ -z "$command" || "$command" =~ ^[0-9]+$ ]]; then
  if [[ -z "$command" ]]; then
    echo "Error: Missing command or temperature" >&2
    usage
  fi
  handle_legacy "$gateway" "$trv_id" "$command"
  exit $?
fi

shift || true  # Remove command from args

# Route to subcommand
case "$command" in
  temp)
    if [[ $# -lt 1 ]]; then
      echo "Error: temp command requires temperature argument" >&2
      usage
    fi
    cmd_temp "$gateway_ip" "$trv_id" "$1"
    ;;
    
  boost)
    if [[ "${1:-}" == "--clear" ]]; then
      cmd_boost_clear "$gateway_ip" "$trv_id"
    else
      cmd_boost "$gateway_ip" "$trv_id" "${1:-1800}"
    fi
    ;;
    
  override)
    if [[ "${1:-}" == "--clear" ]]; then
      cmd_override_clear "$gateway_ip" "$trv_id"
    elif [[ $# -lt 1 ]]; then
      echo "Error: override command requires temperature argument" >&2
      usage
    else
      cmd_override "$gateway_ip" "$trv_id" "$1" "${2:-1800}"
    fi
    ;;
    
  calibrate)
    cmd_calibrate "$gateway_ip" "$trv_id"
    ;;
    
  status)
    cmd_status "$gateway_ip" "$trv_id"
    ;;
    
  info)
    cmd_info "$gateway_ip" "$trv_id"
    ;;
    
  firmware-check|fw-check)
    cmd_firmware_check "$gateway_ip" "$trv_id"
    ;;
    
  firmware-update|fw-update)
    cmd_firmware_update "$gateway_ip" "$trv_id"
    ;;
    
  *)
    echo "Error: Unknown command '$command'" >&2
    usage
    ;;
esac
