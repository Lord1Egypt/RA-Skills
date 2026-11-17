#!/usr/bin/env bash
# Upload a Python file to the M10 and run it from macOS or Linux.

set -u

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=m10_common.sh
source "$SCRIPT_DIR/m10_common.sh" || exit 1

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  printf 'Usage: bash scripts/run_on_m10.sh PROGRAM.py [--env-file FILE] [--background] [--pip-install PACKAGE] [--offline-pip-install]\n'
  exit 0
fi
[[ $# -gt 0 ]] || m10_die "Usage: bash scripts/run_on_m10.sh PROGRAM.py [options]"
script="$1"
shift

host="10.1.2.3"
host_set=false
user="root"
env_file=""
mode=""
python_bin=""
uv_path="uv"
background=false
pip_install=""
offline_pip_install=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) host=${2:?Missing value for --host}; host_set=true; shift 2 ;;
    --user) user=${2:?Missing value for --user}; shift 2 ;;
    --env-file) env_file=${2:?Missing value for --env-file}; shift 2 ;;
    --mode) mode=${2:?Missing value for --mode}; shift 2 ;;
    --python-bin) python_bin=${2:?Missing value for --python-bin}; shift 2 ;;
    --uv-path) uv_path=${2:?Missing value for --uv-path}; shift 2 ;;
    --background) background=true; shift ;;
    --pip-install) pip_install=${2:?Missing value for --pip-install}; shift 2 ;;
    --offline-pip-install) offline_pip_install=true; shift ;;
    -h|--help)
      printf 'Usage: bash scripts/run_on_m10.sh PROGRAM.py [--env-file FILE] [--background] [--pip-install PACKAGE] [--offline-pip-install]\n'
      exit 0
      ;;
    *) m10_die "Unknown option: $1" ;;
  esac
done

[[ -f "$script" ]] || m10_die "File does not exist: $script"

if [[ -n "$env_file" ]]; then
  [[ -f "$env_file" ]] || m10_die "Environment file does not exist: $env_file"
  env_host=$(m10_json_string "$env_file" host)
  env_mode=$(m10_json_string "$env_file" mode)
  env_python_bin=$(m10_json_string "$env_file" python_bin)
  env_uv_path=$(m10_json_string "$env_file" uv_path)
  [[ "$host_set" == true || -z "$env_host" ]] || host="$env_host"
  [[ -n "$mode" || -z "$env_mode" ]] || mode="$env_mode"
  [[ -n "$python_bin" || -z "$env_python_bin" ]] || python_bin="$env_python_bin"
  [[ -z "$env_uv_path" ]] || uv_path="$env_uv_path"
fi

case "$mode" in
  "") if [[ -n "$python_bin" ]]; then mode="pyenv"; else mode="system"; fi ;;
  pyenv|uv|system) ;;
  *) m10_die "Mode must be pyenv, uv, or system." ;;
esac
[[ -n "$python_bin" || "$mode" != "system" ]] || python_bin="python3"
[[ -n "$python_bin" || "$mode" != "pyenv" ]] || python_bin="/root/.pyenv/versions/3.12.7/bin/python3"
[[ -n "$python_bin" || "$mode" != "uv" ]] || m10_die "uv mode needs --python-bin or python_bin in the environment file."

m10_validate_host_user "$host" "$user"
m10_validate_remote_path "$python_bin"
m10_validate_remote_path "$uv_path"
m10_require_command ssh
m10_require_command scp
[[ -z "$pip_install" ]] || m10_validate_package "$pip_install"

local_file=$(cd "$(dirname "$script")" && pwd)/$(basename "$script")
file_name=$(basename "$local_file" | sed 's/[^A-Za-z0-9._-]/_/g')
remote_dir="/tmp/m10_nl"
remote_path="$remote_dir/$file_name"
log_path="/tmp/$file_name.log"

printf '=== Deploying to UNIHIKER M10 ===\n'
printf 'Local: %s\n' "$local_file"
printf 'Remote: %s@%s:%s\n' "$user" "$host" "$remote_path"
printf 'Environment: mode=%s python=%s uv=%s\n' "$mode" "$python_bin" "$uv_path"
printf 'SSH/SCP may prompt for the factory-default password: dfrobot\n\n'

ssh -o StrictHostKeyChecking=accept-new "$user@$host" "mkdir -p '$remote_dir'" || m10_die "Could not prepare the remote directory."
scp -o StrictHostKeyChecking=accept-new "$local_file" "$user@$host:$remote_path" || m10_die "Program upload failed."

if [[ -n "$pip_install" ]]; then
  printf 'Installing dependency: %s\n' "$pip_install"
  if [[ "$offline_pip_install" == true ]]; then
    offline_args=("$pip_install" --host "$host" --user "$user" --mode "$mode" --python-bin "$python_bin" --uv-path "$uv_path")
    bash "$SCRIPT_DIR/install_m10_package_offline.sh" "${offline_args[@]}" || m10_die "Offline dependency installation failed."
  else
    if [[ "$mode" == "uv" ]]; then
      pip_cmd="$uv_path pip install '$pip_install'"
    else
      pip_cmd="$python_bin -m pip install '$pip_install'"
    fi
    ssh -o StrictHostKeyChecking=accept-new "$user@$host" "$pip_cmd" || m10_die "Dependency installation failed. Use --offline-pip-install when the M10 has no Internet access."
  fi
fi

if [[ "$mode" == "uv" ]]; then
  run_prefix="$uv_path run python"
else
  run_prefix="$python_bin"
fi

if [[ "$background" == true ]]; then
  run_cmd="pkill -f '$remote_path' 2>/dev/null; nohup $run_prefix '$remote_path' > '$log_path' 2>&1 & sleep 2; head -5 '$log_path'"
  printf 'Starting in the background...\n'
else
  run_cmd="$run_prefix '$remote_path'"
  printf 'Running in the foreground...\n'
fi

ssh -o StrictHostKeyChecking=accept-new "$user@$host" "$run_cmd"
status=$?
if [[ $status -eq 0 ]]; then
  printf 'Completed\n'
else
  printf 'Exit code: %s\n' "$status" >&2
fi
exit "$status"
