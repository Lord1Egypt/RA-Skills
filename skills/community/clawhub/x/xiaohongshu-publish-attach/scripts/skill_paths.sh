#!/usr/bin/env bash
resolve_skill_scripts_dir() {
  local base="$1"
  if [[ -f "$base/xhs_publish.sh" ]] || [[ -f "$base/xhs_attach_standalone.py" ]]; then
    echo "$base"
    return
  fi
  if [[ -f "$base/scripts/xhs_publish.sh" ]]; then
    echo "$base/scripts"
    return
  fi
  echo "$base"
}
