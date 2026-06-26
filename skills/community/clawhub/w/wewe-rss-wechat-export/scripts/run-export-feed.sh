#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
EXPORT_SCRIPT="$SCRIPT_DIR/export-feed-single-pages.mjs"
DEFAULT_EXPORT_ROOT="${EXPORT_FEED_OUTPUT_ROOT:-$PWD/export}"
MAX_BATCH_SIZE="5"

usage() {
  cat <<'EOF'
Usage:
  run-export-feed.sh <feed_url> [count] [output_dir] [--batch-size N] [--output-mode docx|full] [--rename-mode dated|plain] [--zip]
EOF
}

if [[ $# -lt 1 ]]; then
  usage >&2
  exit 1
fi

feed_url="$1"
shift

count="100"
output_dir=""
batch_size="2"
output_mode="docx"
rename_mode="dated"
make_zip="false"

if [[ $# -gt 0 && "$1" != --* ]]; then
  count="$1"
  shift
fi

if [[ $# -gt 0 && "$1" != --* ]]; then
  output_dir="$1"
  shift
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --batch-size)
      batch_size="${2:-}"
      shift 2
      ;;
    --output-mode)
      output_mode="${2:-}"
      shift 2
      ;;
    --rename-mode)
      rename_mode="${2:-}"
      shift 2
      ;;
    --zip)
      make_zip="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! "$feed_url" =~ ^https?:// ]]; then
  echo "feed_url must start with http:// or https://" >&2
  exit 1
fi

if ! [[ "$count" =~ ^[0-9]+$ ]] || [[ "$count" -le 0 ]]; then
  echo "count must be a positive integer" >&2
  exit 1
fi

if ! [[ "$batch_size" =~ ^[0-9]+$ ]] || [[ "$batch_size" -le 0 ]]; then
  echo "batch_size must be a positive integer" >&2
  exit 1
fi

if [[ "$batch_size" -gt "$MAX_BATCH_SIZE" ]]; then
  batch_size="$MAX_BATCH_SIZE"
fi

if [[ "$output_mode" != "docx" && "$output_mode" != "full" ]]; then
  echo "output_mode must be docx or full" >&2
  exit 1
fi

if [[ "$rename_mode" != "dated" && "$rename_mode" != "plain" ]]; then
  echo "rename_mode must be dated or plain" >&2
  exit 1
fi

if [[ ! -f "$EXPORT_SCRIPT" ]]; then
  echo "missing export script: $EXPORT_SCRIPT" >&2
  exit 1
fi

for command_name in node pandoc curl python3; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "$command_name is required" >&2
    exit 1
  fi
done

slugify() {
  python3 - "$1" <<'PY'
import re, sys
value = sys.argv[1]
value = re.sub(r'https?://', '', value)
value = re.sub(r'[^A-Za-z0-9._-]+', '-', value)
value = re.sub(r'-+', '-', value).strip('-._')
print(value[:60] or 'feed-export')
PY
}

if [[ -z "$output_dir" ]]; then
  slug="$(slugify "$feed_url")"
  output_dir="$DEFAULT_EXPORT_ROOT/${slug}-${count}-${output_mode}-${rename_mode}"
fi

mkdir -p "$output_dir"

node "$EXPORT_SCRIPT" "$feed_url" "$output_dir" "$count" "$batch_size" --output-mode "$output_mode" --rename-mode "$rename_mode"

zip_path=""
if [[ "$make_zip" == "true" ]]; then
  zip_path="${output_dir%/}.zip"
  python3 - "$output_dir" "$zip_path" <<'PY'
from pathlib import Path
import sys, zipfile
base = Path(sys.argv[1])
out = Path(sys.argv[2])
if out.exists():
    out.unlink()
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for path in sorted(base.rglob('*')):
        if path.is_file():
            zf.write(path, path.relative_to(base.parent))
print(out)
PY
fi

cat <<EOF
skill_root=$SKILL_ROOT
output_dir=$output_dir
index_path=$output_dir/index.txt
zip_path=$zip_path
output_mode=$output_mode
rename_mode=$rename_mode
EOF
