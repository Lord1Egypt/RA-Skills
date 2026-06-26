#!/usr/bin/env zsh
set -euo pipefail

script_dir="${0:A:h}"
search_path="${PWD}"
pattern=""

print_help() {
  cat <<'EOF'
Usage: ros1_launch_discover.sh [--path <path>] [--pattern <text>]

Discover launch files in the nearest ROS1 workspace.

Options:
  --path <path>      Starting file or directory, default: current working directory
  --pattern <text>   Filter launch paths by substring
  --help             Show this help
EOF
}

package_name_for_file() {
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

  print -r -- "unknown_package"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      search_path="${2:?missing path}"
      shift 2
      ;;
    --pattern)
      pattern="${2:?missing pattern}"
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

eval "$("$script_dir/ros1_workspace_probe.sh" --path "$search_path" --export)"
if [[ -z "$WORKSPACE_ROOT" ]]; then
  echo "[ERROR] no ROS1 workspace found from: ${search_path:A}" >&2
  exit 1
fi

launch_files=()
while IFS= read -r line; do
  [[ -n "$line" ]] || continue
  if [[ -n "$pattern" && "$line:l" != *"${pattern:l}"* ]]; then
    continue
  fi
  launch_files+=("$line")
done < <(find "$WORKSPACE_ROOT/src" \( -name '*.launch' -o -name '*.launch.xml' \) -type f | sort)

if (( ${#launch_files[@]} == 0 )); then
  echo "[ros1-launch-discover] workspace_root=$WORKSPACE_ROOT"
  echo "[ros1-launch-discover] no launch files found"
  exit 1
fi

echo "[ros1-launch-discover] workspace_root=$WORKSPACE_ROOT"
for launch_file in "${launch_files[@]}"; do
  pkg_name="$(package_name_for_file "$launch_file")"
  rel_path="${launch_file#$WORKSPACE_ROOT/}"
  launch_name="${launch_file:t}"
  echo "[LAUNCH] package=$pkg_name file=$launch_name path=$rel_path"
  echo "roslaunch $pkg_name $launch_name"
done
