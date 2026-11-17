#!/usr/bin/env bash
# Download ARM64 wheels on macOS/Linux, upload them, and install them on an offline M10.

set -u

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# shellcheck source=m10_common.sh
source "$SCRIPT_DIR/m10_common.sh" || exit 1

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  printf 'Usage: bash scripts/install_m10_package_offline.sh PACKAGE [--env-file FILE] [--wheelhouse DIR]\n'
  exit 0
fi
[[ $# -gt 0 ]] || m10_die "Usage: bash scripts/install_m10_package_offline.sh PACKAGE [options]"
package="$1"
shift

host="10.1.2.3"
host_set=false
user="root"
env_file=""
mode=""
python_bin=""
uv_path="uv"
wheelhouse=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) host=${2:?Missing value for --host}; host_set=true; shift 2 ;;
    --user) user=${2:?Missing value for --user}; shift 2 ;;
    --env-file) env_file=${2:?Missing value for --env-file}; shift 2 ;;
    --mode) mode=${2:?Missing value for --mode}; shift 2 ;;
    --python-bin) python_bin=${2:?Missing value for --python-bin}; shift 2 ;;
    --uv-path) uv_path=${2:?Missing value for --uv-path}; shift 2 ;;
    --wheelhouse) wheelhouse=${2:?Missing value for --wheelhouse}; shift 2 ;;
    -h|--help)
      printf 'Usage: bash scripts/install_m10_package_offline.sh PACKAGE [--env-file FILE] [--wheelhouse DIR]\n'
      exit 0
      ;;
    *) m10_die "Unknown option: $1" ;;
  esac
done

m10_validate_package "$package"

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

local_python=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -m pip --version >/dev/null 2>&1; then
    local_python="$candidate"
    break
  fi
done
[[ -n "$local_python" ]] || m10_die "Offline dependency installation needs Python 3 and pip on the computer."

cleanup_local=false
if [[ -n "$wheelhouse" ]]; then
  mkdir -p "$wheelhouse"
  local_wheelhouse=$(cd "$wheelhouse" && pwd)
else
  temp_root=${TMPDIR:-/tmp}
  temp_root=${temp_root%/}
  local_wheelhouse=$(mktemp -d "$temp_root/unihiker-m10-wheels.XXXXXX") || m10_die "Could not create a temporary wheelhouse."
  cleanup_local=true
fi

cleanup() {
  if [[ "$cleanup_local" == true && -n "${local_wheelhouse:-}" ]]; then
    case "$local_wheelhouse" in
      "${temp_root%/}"/unihiker-m10-wheels.*) rm -rf -- "$local_wheelhouse" ;;
    esac
  fi
}
trap cleanup EXIT

upload_id="pkg-$(date +%s)-$$"
remote_parent="/tmp/m10_nl/wheelhouse"
remote_wheelhouse="$remote_parent/$upload_id"
probe_code='import platform,sys; print("%d.%d" % sys.version_info[:2]); print(platform.machine()); print(platform.libc_ver()[1])'
probe_cmd="$python_bin -c '$probe_code'; mkdir -p '$remote_parent'"

printf '=== Preparing an offline M10 dependency ===\n'
printf 'Package: %s\n' "$package"
printf 'Target: %s@%s mode=%s python=%s\n' "$user" "$host" "$mode" "$python_bin"
printf 'SSH/SCP may prompt for the factory-default password: dfrobot\n'

probe=$(ssh -o ConnectTimeout=12 -o StrictHostKeyChecking=accept-new "$user@$host" "$probe_cmd") || m10_die "Could not inspect the selected Python environment on the M10."
python_version=$(printf '%s\n' "$probe" | sed -n '1p')
machine=$(printf '%s\n' "$probe" | sed -n '2p' | tr '[:upper:]' '[:lower:]')
glibc_version=$(printf '%s\n' "$probe" | sed -n '3p')

[[ "$python_version" =~ ^([0-9]+)\.([0-9]+)$ ]] || m10_die "Unexpected target Python version: $python_version"
python_major=${BASH_REMATCH[1]}
python_minor=${BASH_REMATCH[2]}
[[ "$machine" == "aarch64" || "$machine" == "arm64" ]] || m10_die "Expected M10 ARM64, but the target reported: $machine"

python_tag="$python_major$python_minor"
primary_abi="cp$python_tag"
if [[ "$python_major" == "3" && "$python_minor" -le 7 ]]; then primary_abi="cp${python_tag}m"; fi

platforms=()
if [[ "$glibc_version" =~ ^2\.([0-9]+)$ ]]; then
  glibc_minor=${BASH_REMATCH[1]}
  for ((minor=glibc_minor; minor>=17; minor--)); do
    platforms+=("manylinux_2_${minor}_aarch64")
  done
else
  platforms+=("manylinux_2_17_aarch64")
fi
platforms+=("manylinux2014_aarch64")

download_args=(-m pip download "$package" --dest "$local_wheelhouse" --only-binary=:all: --implementation cp --python-version "$python_tag" --no-cache-dir)
for platform in "${platforms[@]}"; do download_args+=(--platform "$platform"); done
for abi in "$primary_abi" abi3 none; do download_args+=(--abi "$abi"); done

printf 'Downloading wheels for CPython %s / aarch64...\n' "$python_version"
"$local_python" "${download_args[@]}" || m10_die "No complete compatible wheel set was found. Pin another version or build on ARM64 Linux."

wheel_count=0
for wheel in "$local_wheelhouse"/*.whl; do
  [[ -f "$wheel" ]] && ((wheel_count+=1))
done
[[ "$wheel_count" -gt 0 ]] || m10_die "pip completed without producing wheel files."

printf 'Uploading %s wheel file(s)...\n' "$wheel_count"
scp -o StrictHostKeyChecking=accept-new -r "$local_wheelhouse" "$user@$host:$remote_wheelhouse" || m10_die "Wheel upload failed."

if [[ "$mode" == "uv" ]]; then
  install_cmd="$uv_path pip install --python $python_bin --no-index --find-links '$remote_wheelhouse' '$package'"
else
  install_cmd="$python_bin -m pip install --no-index --find-links '$remote_wheelhouse' '$package'"
fi
install_and_clean="$install_cmd; status=\$?; rm -rf '$remote_wheelhouse'; exit \$status"

printf 'Installing from the uploaded wheelhouse...\n'
ssh -o StrictHostKeyChecking=accept-new "$user@$host" "$install_and_clean" || m10_die "The M10 rejected the downloaded wheel set. Review the pip error above."
printf 'Installed %s for M10 Python %s.\n' "$package" "$python_version"
