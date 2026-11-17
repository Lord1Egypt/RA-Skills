#!/usr/bin/env bash
# Detect pyenv, uv, and system Python environments on the M10 from macOS or Linux.

set -u

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=m10_common.sh
source "$SCRIPT_DIR/m10_common.sh" || exit 1

host="10.1.2.3"
user="root"
save_env_file=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) host=${2:?Missing value for --host}; shift 2 ;;
    --user) user=${2:?Missing value for --user}; shift 2 ;;
    --save-env-file) save_env_file=${2:?Missing value for --save-env-file}; shift 2 ;;
    -h|--help)
      printf 'Usage: bash scripts/detect_python_env.sh [--host IP] [--user root] [--save-env-file .m10-env.json]\n'
      exit 0
      ;;
    *) m10_die "Unknown option: $1" ;;
  esac
done

m10_validate_host_user "$host" "$user"
m10_require_command ssh

printf '=== Detecting M10 Python environments @ %s@%s ===\n' "$user" "$host"
printf 'SSH may prompt for the factory-default password: dfrobot\n'

raw=$(ssh -o ConnectTimeout=12 -o StrictHostKeyChecking=accept-new "$user@$host" 'sh -s' <<'REMOTE'
echo "===M10_PYTHON_ENV_BEGIN==="
printf 'hostname='
hostname
printf 'pyenv_global='
(pyenv global 2>/dev/null || cat /root/.python-version 2>/dev/null || echo "")
printf 'system_python='
(python3 --version 2>/dev/null | awk '{print $2}' || echo "")
printf 'uv_path='
(command -v uv 2>/dev/null || echo "")
printf 'uv_version='
(uv --version 2>/dev/null | head -1 || echo "")
echo "pyenv_versions_begin"
(ls -1 /root/.pyenv/versions/ 2>/dev/null || true)
echo "pyenv_versions_end"
echo "===M10_PYTHON_ENV_END==="
REMOTE
) || m10_die "SSH environment detection failed."

hostname_value=$(printf '%s\n' "$raw" | sed -n 's/^hostname=//p' | head -n 1)
pyenv_global=$(printf '%s\n' "$raw" | sed -n 's/^pyenv_global=//p' | head -n 1)
system_python=$(printf '%s\n' "$raw" | sed -n 's/^system_python=//p' | head -n 1)
uv_path=$(printf '%s\n' "$raw" | sed -n 's/^uv_path=//p' | head -n 1)
uv_version=$(printf '%s\n' "$raw" | sed -n 's/^uv_version=//p' | head -n 1)
versions=$(printf '%s\n' "$raw" | sed -n '/^pyenv_versions_begin$/,/^pyenv_versions_end$/p' | sed '1d;$d')

printf '\nHost: %s @ %s\n' "$hostname_value" "$host"
printf 'System python3: %s\n' "$system_python"
printf 'Global pyenv version: %s\n' "$pyenv_global"

recommended="$pyenv_global"
if [[ -n "$versions" ]]; then
  printf 'Installed pyenv versions:\n'
  while IFS= read -r version; do
    [[ -n "$version" ]] || continue
    printf '  - %s => /root/.pyenv/versions/%s/bin/python3\n' "$version" "$version"
    if [[ -z "$pyenv_global" ]]; then recommended="$version"; fi
  done <<< "$versions"
else
  printf 'pyenv versions: none found under /root/.pyenv/versions/\n'
fi

if [[ -n "$uv_path" ]]; then
  printf 'uv: %s %s\n' "$uv_path" "$uv_version"
else
  printf 'uv: not installed\n'
fi

if [[ -n "$recommended" ]]; then
  mode="pyenv"
  python_bin="/root/.pyenv/versions/$recommended/bin/python3"
  printf '\nRecommended default: pyenv %s\n' "$recommended"
else
  mode="system"
  python_bin="python3"
fi

if [[ -n "$save_env_file" ]]; then
  parent=$(dirname "$save_env_file")
  [[ "$parent" == "." ]] || mkdir -p "$parent"
  if [[ -n "$uv_path" ]]; then uv_available=true; else uv_available=false; fi
  cat > "$save_env_file" <<JSON
{
  "host": "$(m10_json_escape "$host")",
  "mode": "$(m10_json_escape "$mode")",
  "python_version": "$(m10_json_escape "$recommended")",
  "python_bin": "$(m10_json_escape "$python_bin")",
  "uv_path": "$(m10_json_escape "$uv_path")",
  "uv_available": $uv_available,
  "detected_at": "$(date '+%Y-%m-%d %H:%M:%S')"
}
JSON
  printf 'Saved environment configuration: %s\n' "$save_env_file"
fi

printf '\nNext: select a detected pyenv version, uv, or system Python.\n'
