#!/usr/bin/env bash
# Check whether a UNIHIKER M10 is reachable from macOS or Linux.

set -u

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=m10_common.sh
source "$SCRIPT_DIR/m10_common.sh" || exit 1

host="10.1.2.3"
user="root"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) host=${2:?Missing value for --host}; shift 2 ;;
    --user) user=${2:?Missing value for --user}; shift 2 ;;
    -h|--help)
      printf 'Usage: bash scripts/check_connection.sh [--host 10.1.2.3] [--user root]\n'
      exit 0
      ;;
    *) m10_die "Unknown option: $1" ;;
  esac
done

m10_validate_host_user "$host" "$user"
m10_require_command ping
m10_require_command ssh

printf '=== UNIHIKER M10 connection check ===\n'
printf 'Target: %s@%s\n\n' "$user" "$host"
printf '[1/2] Ping %s ...\n' "$host"

if [[ $(uname -s) == "Darwin" ]]; then
  ping -c 1 -W 2000 "$host" >/dev/null 2>&1
else
  ping -c 1 -W 2 "$host" >/dev/null 2>&1
fi
if [[ $? -ne 0 ]]; then
  m10_die "Ping failed. Check the USB cable or confirm both devices are on the same Wi-Fi network."
fi
printf 'OK: Ping succeeded\n'

printf '[2/2] Checking SSH (the factory-default password is dfrobot)...\n'
remote_cmd='hostname && python3 --version && python3 -c "import unihiker, pinpong; print(1)"'
if ! ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "$user@$host" "$remote_cmd"; then
  m10_die "The SSH or M10 Python library check failed."
fi

printf '\nUNIHIKER M10 connected @ %s\n' "$host"
