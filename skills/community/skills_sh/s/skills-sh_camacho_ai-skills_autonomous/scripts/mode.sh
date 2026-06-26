#!/usr/bin/env bash
# mode.sh — Skill-owned wrappers around session-state mode helpers.

_mode_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
_mode_repo_root="$(cd "$_mode_script_dir/../../../.." && pwd -P)"

# shellcheck source=../../../../scripts/lib/session-state.sh
source "$_mode_repo_root/scripts/lib/session-state.sh"

atomic_write() { session_state_atomic_write "$@"; }
_resolve_session_dir() { session_state_resolve_session_dir "$@"; }
expire_if_stale() { session_state_expire_mode_if_stale "$@"; }
get_mode() { session_state_get_mode "$@"; }
set_mode() { session_state_set_mode "$@"; }
is_copilot_strict() { session_state_is_copilot_strict "$@"; }
is_copilot() { [ "$(get_mode)" = "copilot" ]; }
