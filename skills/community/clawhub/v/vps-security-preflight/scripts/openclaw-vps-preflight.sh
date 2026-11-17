#!/usr/bin/env bash

set -u
set -o pipefail

STRICT=0
SHOW_AUDIT=0
OPENCLAW_BIN="${OPENCLAW_BIN:-openclaw}"
PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0
INFO_COUNT=0

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
  GREEN='\033[32m'
  YELLOW='\033[33m'
  RED='\033[31m'
  BLUE='\033[34m'
  BOLD='\033[1m'
  RESET='\033[0m'
else
  GREEN=''
  YELLOW=''
  RED=''
  BLUE=''
  BOLD=''
  RESET=''
fi

usage() {
  cat <<'EOF'
Usage: openclaw-vps-preflight.sh [--strict] [--show-audit]

Runs read-only OpenClaw and Linux host checks. The script does not change
configuration, install packages, write files, or upload host data.

Options:
  --strict       Return nonzero when any warning or failure is found.
  --show-audit   Print the official OpenClaw deep security-audit output.
  -h, --help     Show this help text.

Environment:
  OPENCLAW_BIN   OpenClaw executable name or absolute path.
  NO_COLOR       Disable colored output when set.
EOF
}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf '%bPASS%b  %s\n' "$GREEN" "$RESET" "$1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf '%bWARN%b  %s\n' "$YELLOW" "$RESET" "$1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  printf '%bFAIL%b  %s\n' "$RED" "$RESET" "$1"
}

info() {
  INFO_COUNT=$((INFO_COUNT + 1))
  printf '%bINFO%b  %s\n' "$BLUE" "$RESET" "$1"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

run_quiet() {
  if command_exists timeout; then
    timeout 20s "$@" >/dev/null 2>&1
  else
    "$@" >/dev/null 2>&1
  fi
}

config_value() {
  local output value
  output=$("$OPENCLAW_BIN" config get "$1" 2>/dev/null) || return 1
  value=$(printf '%s\n' "$output" | awk 'NF { value=$0 } END { print value }')
  value="${value#\"}"
  value="${value%\"}"
  printf '%s' "$value"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --strict)
      STRICT=1
      ;;
    --show-audit)
      SHOW_AUDIT=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

printf '%bOpenClaw VPS Security Preflight%b\n' "$BOLD" "$RESET"
printf 'Read-only checks; no changes will be made.\n\n'

if [[ "$(uname -s 2>/dev/null || true)" != "Linux" ]]; then
  fail 'This audit targets Linux VPS hosts.'
  printf '\nSummary: %d passed, %d warned, %d failed, %d informational.\n' \
    "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT" "$INFO_COUNT"
  exit 2
fi
pass 'Linux host detected.'

if ! command -v "$OPENCLAW_BIN" >/dev/null 2>&1; then
  fail "OpenClaw CLI was not found (${OPENCLAW_BIN})."
  printf '\nSummary: %d passed, %d warned, %d failed, %d informational.\n' \
    "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT" "$INFO_COUNT"
  exit 1
fi

version=$("$OPENCLAW_BIN" --version 2>/dev/null | awk 'NR == 1 { print; exit }')
if [[ -n "$version" ]]; then
  pass "OpenClaw CLI is available (${version})."
else
  warn 'OpenClaw CLI is present but did not report a version.'
fi

if run_quiet "$OPENCLAW_BIN" gateway status --require-rpc; then
  pass 'Gateway service and read-only RPC probe are healthy.'
else
  fail 'Gateway RPC probe failed; run: openclaw gateway status --deep'
fi

bind_mode=$(config_value gateway.bind || true)
case "$bind_mode" in
  loopback)
    pass 'Gateway bind mode is loopback.'
    ;;
  lan)
    fail 'Gateway bind mode is lan; verify authentication and intended exposure immediately.'
    ;;
  tailnet)
    warn 'Gateway bind mode is tailnet; confirm the tailnet ACL and operator boundary.'
    ;;
  auto|custom)
    warn "Gateway bind mode is ${bind_mode}; verify the resolved listener address manually."
    ;;
  '')
    warn 'Gateway bind mode could not be read.'
    ;;
  *)
    warn "Gateway bind mode is unrecognized (${bind_mode}); compare it with current OpenClaw documentation."
    ;;
esac

auth_mode=$(config_value gateway.auth.mode || true)
case "$auth_mode" in
  token|password|trusted-proxy)
    pass "Gateway authentication mode is ${auth_mode}."
    ;;
  none)
    if [[ "$bind_mode" == 'loopback' ]]; then
      warn 'Gateway authentication is none on loopback; valid for an isolated local-only setup, but shared-secret auth adds defense in depth.'
    else
      fail 'Gateway authentication is none while bind mode is not confirmed as loopback.'
    fi
    ;;
  '')
    warn 'Gateway authentication mode could not be read.'
    ;;
  *)
    warn "Gateway authentication mode is unrecognized (${auth_mode})."
    ;;
esac

gateway_port=$(config_value gateway.port || true)
if [[ ! "$gateway_port" =~ ^[0-9]+$ ]]; then
  gateway_port=18789
fi

if command_exists ss; then
  listeners=$(ss -H -ltn 2>/dev/null | awk -v port="$gateway_port" '$4 ~ (":" port "$") { print $4 }')
  if [[ -z "$listeners" ]]; then
    warn "No TCP listener was detected on the configured Gateway port (${gateway_port})."
  elif printf '%s\n' "$listeners" | grep -Eq "^(0\\.0\\.0\\.0|\\*|\\[::\\]):${gateway_port}$"; then
    fail "Gateway port ${gateway_port} has a wildcard network listener."
  elif printf '%s\n' "$listeners" | grep -Ev "^(127\\.0\\.0\\.1|\\[::1\\]):${gateway_port}$" | grep -q .; then
    warn "Gateway port ${gateway_port} listens on a non-loopback address; verify that the interface is intentional and access-controlled."
  else
    pass "Gateway port ${gateway_port} listens only on loopback."
  fi
else
  warn 'The ss utility is unavailable; inspect Gateway listeners manually.'
fi

if command_exists systemctl; then
  user_enabled=$(systemctl --user list-unit-files 'openclaw-gateway*.service' --state=enabled --no-legend 2>/dev/null || true)
  system_enabled=$(systemctl list-unit-files 'openclaw-gateway*.service' --state=enabled --no-legend 2>/dev/null || true)
  if [[ -n "$user_enabled$system_enabled" ]]; then
    pass 'An OpenClaw systemd service is enabled for reboot survival.'
  else
    warn 'No enabled OpenClaw systemd service was detected.'
  fi

  user_active=$(systemctl --user list-units 'openclaw-gateway*.service' --state=running --no-legend 2>/dev/null || true)
  system_active=$(systemctl list-units 'openclaw-gateway*.service' --state=running --no-legend 2>/dev/null || true)
  if [[ -n "$user_active$system_active" ]]; then
    pass 'An OpenClaw systemd service is running.'
  else
    warn 'No running OpenClaw systemd service was detected.'
  fi
else
  warn 'systemctl is unavailable; supervised startup was not verified.'
fi

firewall_detected=0
if command_exists ufw && ufw status 2>/dev/null | grep -qi '^Status: active'; then
  firewall_detected=1
elif command_exists firewall-cmd && run_quiet firewall-cmd --state; then
  firewall_detected=1
elif command_exists nft && [[ -n "$(nft list tables 2>/dev/null || true)" ]]; then
  firewall_detected=1
fi

if [[ "$firewall_detected" -eq 1 ]]; then
  pass 'An active host firewall or nftables ruleset was detected.'
else
  warn 'No active UFW, firewalld, or nftables ruleset was detected.'
fi

if command_exists sshd; then
  sshd_effective=$(sshd -T 2>/dev/null || true)
  if [[ -n "$sshd_effective" ]]; then
    password_auth=$(printf '%s\n' "$sshd_effective" | awk '$1 == "passwordauthentication" { print $2; exit }')
    root_login=$(printf '%s\n' "$sshd_effective" | awk '$1 == "permitrootlogin" { print $2; exit }')

    if [[ "$password_auth" == 'no' ]]; then
      pass 'SSH password authentication is disabled.'
    elif [[ -n "$password_auth" ]]; then
      fail 'SSH password authentication is enabled.'
    else
      warn 'SSH password-authentication policy could not be determined.'
    fi

    case "$root_login" in
      no|prohibit-password|forced-commands-only)
        pass "SSH root-login policy is ${root_login}."
        ;;
      yes)
        fail 'Direct SSH root login is enabled.'
        ;;
      *)
        warn 'SSH root-login policy could not be determined.'
        ;;
    esac
  else
    warn 'Effective sshd policy could not be read; verify key-only access and root-login restrictions manually.'
  fi
else
  warn 'sshd is unavailable; SSH hardening was not verified.'
fi

if command_exists fail2ban-client && run_quiet fail2ban-client status sshd; then
  pass 'fail2ban has an active sshd jail.'
else
  warn 'An active fail2ban sshd jail was not detected.'
fi

if command_exists systemctl && {
  run_quiet systemctl is-enabled apt-daily-upgrade.timer ||
  run_quiet systemctl is-enabled unattended-upgrades.service ||
  run_quiet systemctl is-enabled dnf-automatic.timer ||
  run_quiet systemctl is-enabled dnf5-automatic.timer;
}; then
  pass 'An automatic security-update service or timer is enabled.'
else
  warn 'Automatic security updates were not detected.'
fi

if command_exists timedatectl; then
  ntp_state=$(timedatectl show -p NTPSynchronized --value 2>/dev/null || true)
  if [[ "$ntp_state" == 'yes' ]]; then
    pass 'System time is synchronized.'
  else
    warn 'System time synchronization was not confirmed.'
  fi
else
  warn 'timedatectl is unavailable; time synchronization was not verified.'
fi

if run_quiet "$OPENCLAW_BIN" security audit --json; then
  info 'Official OpenClaw security audit completed. Run with --show-audit to review its findings.'
else
  warn 'The official OpenClaw security audit did not complete successfully.'
fi

info 'Backup freshness, restore testing, provider spend limits, and rollback evidence require manual verification.'

if [[ "$SHOW_AUDIT" -eq 1 ]]; then
  printf '\n%bOfficial OpenClaw deep security audit%b\n' "$BOLD" "$RESET"
  "$OPENCLAW_BIN" security audit --deep || warn 'The displayed deep security audit returned nonzero.'
fi

printf '\nSummary: %d passed, %d warned, %d failed, %d informational.\n' \
  "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT" "$INFO_COUNT"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi
if [[ "$STRICT" -eq 1 && "$WARN_COUNT" -gt 0 ]]; then
  exit 1
fi
exit 0
