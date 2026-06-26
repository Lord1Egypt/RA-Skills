#!/usr/bin/env bash
# Resolve the directory that contains zhihu_publish.sh (scripts/ or skill root).
resolve_skill_scripts_dir() {
  local base="$1"
  if [[ -f "$base/zhihu_publish.sh" ]] || [[ -f "$base/zhihu_attach_standalone.py" ]]; then
    echo "$base"
    return
  fi
  if [[ -f "$base/scripts/zhihu_publish.sh" ]]; then
    echo "$base/scripts"
    return
  fi
  echo "$base"
}
