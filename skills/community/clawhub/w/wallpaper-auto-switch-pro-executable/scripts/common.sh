#!/bin/bash
set -euo pipefail

SUPPORTED_EXTENSIONS=(jpg jpeg png heic webp)
LAUNCHD_LABEL="com.openclaw.wallpaperrotator"
LAUNCHD_PLIST="$HOME/Library/LaunchAgents/${LAUNCHD_LABEL}.plist"

expand_path() {
  local input="$1"
  if [[ "$input" == ~* ]]; then
    eval "printf '%s' $input"
  else
    printf '%s' "$input"
  fi
}

ensure_dir_exists() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    echo "ERROR: 目录不存在: $dir" >&2
    exit 1
  fi
}

collect_images() {
  local dir="$1"
  ensure_dir_exists "$dir"
  find "$dir" -type f \( \
    -iname "*.jpg" -o \
    -iname "*.jpeg" -o \
    -iname "*.png" -o \
    -iname "*.heic" -o \
    -iname "*.webp" \
  \) | sort
}

pick_random_image() {
  local dir="$1"
  local list
  list="$(collect_images "$dir")"
  if [[ -z "$list" ]]; then
    echo "ERROR: 目录中没有可用图片: $dir" >&2
    exit 1
  fi
  printf '%s
' "$list" | shuf -n 1
}

set_wallpaper_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    echo "ERROR: 文件不存在: $file" >&2
    exit 1
  fi

  /usr/bin/osascript <<OSA
set targetFile to POSIX file "$file"
tell application "System Events"
    set picture of every desktop to targetFile
end tell
OSA
}
