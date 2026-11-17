#!/usr/bin/env bash

m10_die() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

m10_validate_host_user() {
  local host="$1"
  local user="$2"
  [[ "$host" =~ ^[A-Za-z0-9.-]+$ ]] || m10_die "The SSH host contains unsupported characters."
  [[ "$user" =~ ^[A-Za-z0-9._-]+$ ]] || m10_die "The SSH user contains unsupported characters."
}

m10_validate_remote_path() {
  [[ "$1" =~ ^[/A-Za-z0-9._-]+$ ]] || m10_die "A remote executable path contains unsupported characters."
}

m10_validate_package() {
  local pattern='^[A-Za-z0-9_.-]+(\[[A-Za-z0-9_,.-]+\])?([<>=!~]+[A-Za-z0-9_.-]+)?$'
  [[ "$1" =~ $pattern ]] || m10_die "Package must be one PyPI package name with optional extras or a version specifier."
}

m10_json_string() {
  local file="$1"
  local key="$2"
  sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$file" | head -n 1
}

m10_json_escape() {
  local value="$1"
  value=${value//\\/\\\\}
  value=${value//\"/\\\"}
  value=${value//$'\n'/\\n}
  printf '%s' "$value"
}

m10_require_command() {
  command -v "$1" >/dev/null 2>&1 || m10_die "Required command not found: $1"
}
