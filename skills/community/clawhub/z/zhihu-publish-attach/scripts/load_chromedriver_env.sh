#!/usr/bin/env bash
# Source from other scripts: . "$(dirname "$0")/load_chromedriver_env.sh"
load_chromedriver_env() {
  local script_dir="${1:-}"
  if [[ -z "$script_dir" ]]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  fi
  local env_file="$script_dir/chromedriver.env"
  if [[ ! -f "$env_file" ]]; then
    local parent_env="$(dirname "$script_dir")/chromedriver.env"
    if [[ -f "$parent_env" ]]; then
      env_file="$parent_env"
    fi
  fi
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a
  fi
  if [[ -n "${CHROMEDRIVER_PATH:-}" && -x "$CHROMEDRIVER_PATH" ]]; then
    export PATH="$(dirname "$CHROMEDRIVER_PATH"):${PATH}"
    return 0
  fi
  if [[ -x "${HOME}/.local/bin/chromedriver" ]]; then
    export CHROMEDRIVER_PATH="${HOME}/.local/bin/chromedriver"
    export PATH="${HOME}/.local/bin:${PATH}"
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  load_chromedriver_env "$(cd "$(dirname "$0")" && pwd)"
  echo "CHROMEDRIVER_PATH=${CHROMEDRIVER_PATH:-<unset>}"
fi
