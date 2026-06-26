#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
workspace_path="${PWD}"
package_name=""
launch_name=""
launch_path=""
node_package=""
node_type=""
node_name=""
target_name=""
state_root="${TMPDIR:-/tmp}/ros1_skill_runtime"
wait_seconds="6"
extra_args=()

print_help() {
  cat <<'EOF'
Usage:
  ros1_start_target.sh --workspace <path> --package <pkg> --launch <file.launch> [options]
  ros1_start_target.sh --workspace <path> --launch-path <path/to/file.launch> [options]
  ros1_start_target.sh --workspace <path> --node-package <pkg> --node-type <node> [options]

Start a ROS1 target in the background, record pid/log/state files, and print the state file path.

Options:
  --workspace <path>        Workspace root or subdirectory to inspect
  --package <pkg>           Package for roslaunch
  --launch <file.launch>    Launch file name for roslaunch
  --launch-path <path>      Absolute or workspace-relative launch file path
  --node-package <pkg>      Package for rosrun
  --node-type <node>        Executable/script for rosrun
  --node-name <name>        Optional ROS node name override
  --name <name>             Friendly target name stored in state metadata
  --arg <value>             Extra argument passed to roslaunch/rosrun (repeatable)
  --state-root <path>       Directory for state/log files
  --wait-seconds <n>        Seconds to watch for early failure, default: 6
  --help                    Show this help
EOF
}

require_value() {
  local flag="$1"
  local value="${2:-}"
  [[ -n "$value" ]] || { echo "[ERROR] missing value for $flag" >&2; exit 2; }
}

quote_join() {
  local out=""
  local item=""
  for item in "$@"; do
    out+="${out:+ }${(q)item}"
  done
  print -r -- "$out"
}

append_state_line() {
  local key="$1"
  local value="${2:-}"
  print -r -- "${key}=${(q)value}" >> "$state_file"
}

infer_package_from_launch_path() {
  local file="$1"
  local dir="${file:h}"
  local name=""

  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/package.xml" ]]; then
      name="$(sed -n 's:.*<name>\([^<]*\)</name>.*:\1:p' "$dir/package.xml" | head -n 1)"
      if [[ -n "$name" ]]; then
        print -r -- "$name"
        return 0
      fi
      print -r -- "${dir:t}"
      return 0
    fi
    dir="${dir:h}"
  done

  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace|--path)
      workspace_path="${2:-}"
      require_value "$1" "$workspace_path"
      shift 2
      ;;
    --package)
      package_name="${2:-}"
      require_value "$1" "$package_name"
      shift 2
      ;;
    --launch)
      launch_name="${2:-}"
      require_value "$1" "$launch_name"
      shift 2
      ;;
    --launch-path)
      launch_path="${2:-}"
      require_value "$1" "$launch_path"
      shift 2
      ;;
    --node-package)
      node_package="${2:-}"
      require_value "$1" "$node_package"
      shift 2
      ;;
    --node-type)
      node_type="${2:-}"
      require_value "$1" "$node_type"
      shift 2
      ;;
    --node-name)
      node_name="${2:-}"
      require_value "$1" "$node_name"
      shift 2
      ;;
    --name)
      target_name="${2:-}"
      require_value "$1" "$target_name"
      shift 2
      ;;
    --arg)
      extra_args+=("${2:-}")
      require_value "$1" "${extra_args[-1]}"
      shift 2
      ;;
    --state-root)
      state_root="${2:-}"
      require_value "$1" "$state_root"
      shift 2
      ;;
    --wait-seconds)
      wait_seconds="${2:-}"
      require_value "$1" "$wait_seconds"
      shift 2
      ;;
    --help|-h)
      print_help
      exit 0
      ;;
    *)
      echo "[ERROR] unknown argument: $1" >&2
      print_help >&2
      exit 2
      ;;
  esac
done

workspace_path="${workspace_path:A}"
eval "$("$script_dir/ros1_workspace_probe.sh" --path "$workspace_path" --export)"
workspace_root="$WORKSPACE_ROOT"
workspace_setup="$WORKSPACE_SETUP"

if [[ -z "$workspace_root" ]]; then
  echo "[ERROR] no ROS1 workspace found from: $workspace_path" >&2
  exit 1
fi

eval "$("$script_dir/ros1_shell_detect.sh" --workspace "$workspace_root" --export)"
if [[ -z "$ROS_SETUP" ]]; then
  echo "[ERROR] ROS setup file not found under /opt/ros/noetic" >&2
  exit 1
fi

mode=""
resolved_launch_path=""
command=()

if [[ -n "$launch_path" ]]; then
  mode="launch"
  if [[ "$launch_path" != /* ]]; then
    resolved_launch_path="$workspace_root/$launch_path"
  else
    resolved_launch_path="$launch_path"
  fi
  resolved_launch_path="${resolved_launch_path:A}"
  [[ -f "$resolved_launch_path" ]] || { echo "[ERROR] launch file not found: $resolved_launch_path" >&2; exit 1; }
  [[ -n "$package_name" ]] || package_name="$(infer_package_from_launch_path "$resolved_launch_path" || true)"
  [[ -n "$launch_name" ]] || launch_name="${resolved_launch_path:t}"
  [[ -n "$package_name" ]] || { echo "[ERROR] could not infer package from launch path" >&2; exit 1; }
  command=(roslaunch "$package_name" "$launch_name" "${extra_args[@]}")
elif [[ -n "$package_name" && -n "$launch_name" ]]; then
  mode="launch"
  command=(roslaunch "$package_name" "$launch_name" "${extra_args[@]}")
elif [[ -n "$node_package" && -n "$node_type" ]]; then
  mode="run"
  command=(rosrun "$node_package" "$node_type")
  if [[ -n "$node_name" ]]; then
    command+=("__name:=$node_name")
  fi
  command+=("${extra_args[@]}")
else
  echo "[ERROR] choose either launch mode (--package + --launch or --launch-path) or run mode (--node-package + --node-type)" >&2
  exit 2
fi

mkdir -p "$state_root"
timestamp="$(date +%Y%m%d_%H%M%S)"
safe_name="${target_name:-${package_name:-$node_package}_${launch_name:-$node_type}}"
safe_name="${safe_name//\//_}"
run_dir="$state_root/${safe_name}_${timestamp}"
mkdir -p "$run_dir"
log_file="$run_dir/stdout.log"
meta_file="$run_dir/metadata.env"
state_file="$run_dir/state.env"
launcher_file="$run_dir/launcher.zsh"
ros_home="$run_dir/ros_home"
mkdir -p "$ros_home"

cat > "$meta_file" <<EOF
MODE=${(q)mode}
WORKSPACE_ROOT=${(q)workspace_root}
WORKSPACE_SETUP=${(q)workspace_setup}
ROS_SETUP=${(q)ROS_SETUP}
PACKAGE_NAME=${(q)package_name}
LAUNCH_NAME=${(q)launch_name}
LAUNCH_PATH=${(q)resolved_launch_path}
NODE_PACKAGE=${(q)node_package}
NODE_TYPE=${(q)node_type}
NODE_NAME=${(q)node_name}
TARGET_NAME=${(q)target_name}
COMMAND=${(q)"$(quote_join "${command[@]}")"}
STARTED_AT=${(q)"$(date -Iseconds)"}
LOG_FILE=${(q)log_file}
RUN_DIR=${(q)run_dir}
ROS_HOME=${(q)ros_home}
EOF

cat > "$launcher_file" <<EOF
#!/usr/bin/env zsh
set -euo pipefail
export ROS_HOME=${(q)ros_home}
source ${(q)ROS_SETUP}
if [[ -n ${(q)workspace_setup} && -f ${(q)workspace_setup} ]]; then
  source ${(q)workspace_setup}
fi
cd ${(q)workspace_root}
exec ${(@q)command}
EOF
chmod +x "$launcher_file"

: > "$state_file"
append_state_line "MODE" "$mode"
append_state_line "RUN_DIR" "$run_dir"
append_state_line "WORKSPACE_ROOT" "$workspace_root"
append_state_line "ROS_SETUP" "$ROS_SETUP"
append_state_line "WORKSPACE_SETUP" "$workspace_setup"
append_state_line "LOG_FILE" "$log_file"
append_state_line "LAUNCHER_FILE" "$launcher_file"
append_state_line "ROS_HOME" "$ros_home"
append_state_line "COMMAND" "$(quote_join "${command[@]}")"
append_state_line "STATUS" "starting"
append_state_line "STARTED_AT" "$(date -Iseconds)"

nohup "$launcher_file" >"$log_file" 2>&1 < /dev/null &

pid="$!"
sleep 0.2
pgid="$(ps -o pgid= -p "$pid" | tr -d ' ' || true)"

append_state_line "PID" "$pid"
append_state_line "PGID" "$pgid"

if ! kill -0 "$pid" 2>/dev/null; then
  append_state_line "STATUS" "failed_early"
  echo "[ros1-start-target] status=failed_early"
  echo "[ros1-start-target] state_file=$state_file"
  echo "[ros1-start-target] log_file=$log_file"
  tail -n 40 "$log_file" || true
  exit 1
fi

sleep "$wait_seconds"

if kill -0 "$pid" 2>/dev/null; then
  append_state_line "STATUS" "running"
  append_state_line "LAST_HEALTH" "unchecked"
  echo "[ros1-start-target] status=running"
  echo "[ros1-start-target] mode=$mode"
  echo "[ros1-start-target] pid=$pid"
  echo "[ros1-start-target] pgid=${pgid:-unknown}"
  echo "[ros1-start-target] state_file=$state_file"
  echo "[ros1-start-target] log_file=$log_file"
  exit 0
fi

if wait "$pid"; then
  exit_code="0"
else
  exit_code="$?"
fi
append_state_line "STATUS" "exited_early"
append_state_line "EXIT_CODE" "$exit_code"
echo "[ros1-start-target] status=exited_early"
echo "[ros1-start-target] exit_code=$exit_code"
echo "[ros1-start-target] state_file=$state_file"
echo "[ros1-start-target] log_file=$log_file"
tail -n 40 "$log_file" || true
exit 1
