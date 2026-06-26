#!/usr/bin/env bash
set -euo pipefail

SANDBOX_ROOT="/home/cmart/.openclaw/workspace"

usage() {
  cat <<'USAGE'
Usage: workspace-files.sh <command> [args]

Commands:
  list-dir <relative_path>
  read-file <relative_path>
  write-file <relative_path> <content>
  search-files <pattern>
  help
USAGE
}

resolve_path() {
  local input="${1:-}"

  if [[ -z "$input" ]]; then
    echo "Error: path required" >&2
    exit 1
  fi

  local target
  target="$(realpath -m "$SANDBOX_ROOT/$input")"

  case "$target" in
    "$SANDBOX_ROOT"/*|"$SANDBOX_ROOT")
      printf '%s\n' "$target"
      ;;
    *)
      echo "Error: path outside sandbox is not allowed" >&2
      exit 1
      ;;
  esac
}

cmd_list_dir() {
  local rel="${1:-.}"
  local path
  path="$(resolve_path "$rel")"

  if [[ ! -d "$path" ]]; then
    echo "Error: directory not found: $rel" >&2
    exit 1
  fi

  find "$path" -maxdepth 1 -mindepth 1 | sort
}

cmd_read_file() {
  local rel="${1:-}"
  local path
  path="$(resolve_path "$rel")"

  if [[ ! -f "$path" ]]; then
    echo "Error: file not found: $rel" >&2
    exit 1
  fi

  cat "$path"
}

cmd_write_file() {
  local rel="${1:-}"
  local content="${2:-}"
  local path
  path="$(resolve_path "$rel")"

  mkdir -p "$(dirname "$path")"
  printf '%s' "$content" > "$path"
  echo "OK: wrote $rel"
}

cmd_search_files() {
  local pattern="${1:-}"

  if [[ -z "$pattern" ]]; then
    echo "Error: pattern required" >&2
    exit 1
  fi

  find "$SANDBOX_ROOT" -iname "*$pattern*" | sort
}

main() {
  local cmd="${1:-help}"
  shift || true

  case "$cmd" in
    list-dir) cmd_list_dir "$@" ;;
    read-file) cmd_read_file "$@" ;;
    write-file) cmd_write_file "$@" ;;
    search-files) cmd_search_files "$@" ;;
    help|-h|--help) usage ;;
    *)
      echo "Error: unknown command: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
