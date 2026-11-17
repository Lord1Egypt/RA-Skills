#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 [--force] /path/to/platformio-project" >&2
}

force=0
if [[ ${1:-} == "--force" ]]; then
  force=1
  shift
fi

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

project_dir=$1
if [[ ! -f "$project_dir/platformio.ini" ]]; then
  echo "Error: platformio.ini not found in $project_dir" >&2
  exit 1
fi

target_dir="$project_dir/lib/DFRobot_K10Box"
if [[ -e "$target_dir" && $force -ne 1 ]]; then
  echo "Error: $target_dir already exists; pass --force to replace it" >&2
  exit 1
fi

commit=cde0ad33a6c76089b72a8b73fd74ae71213cf1c7
base="https://gitee.com/zhaoruiz/ext-unihiker-k10-box/raw/$commit"
source_root="$base/arduinoC/libraries/DFRobot_K10Box"
temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/k10-box-driver.XXXXXX")
trap 'rm -rf "$temp_dir"' EXIT

mkdir -p "$temp_dir/DFRobot_K10Box/src"
curl -fsSL --retry 3 --connect-timeout 15 \
  "$source_root/src/DFRobot_K10Box.h" \
  -o "$temp_dir/DFRobot_K10Box/src/DFRobot_K10Box.h"
curl -fsSL --retry 3 --connect-timeout 15 \
  "$source_root/src/DFRobot_K10Box.cpp" \
  -o "$temp_dir/DFRobot_K10Box/src/DFRobot_K10Box.cpp"
curl -fsSL --retry 3 --connect-timeout 15 \
  "$source_root/library.properties" \
  -o "$temp_dir/DFRobot_K10Box/library.properties"
curl -fsSL --retry 3 --connect-timeout 15 \
  "$base/LICENSE.TXT" \
  -o "$temp_dir/DFRobot_K10Box/LICENSE.TXT"

python3 - "$temp_dir/DFRobot_K10Box" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
header = root / "src" / "DFRobot_K10Box.h"
source = root / "src" / "DFRobot_K10Box.cpp"

header_text = header.read_text()
old_pi = "#define M_PI\t\t\t(3.14159265358979323846f)"
new_pi = "#ifndef M_PI\n#define M_PI\t\t\t(3.14159265358979323846f)\n#endif"
if old_pi not in header_text:
    raise SystemExit("Unexpected upstream header: M_PI definition not found")
header.write_text(header_text.replace(old_pi, new_pi, 1))

source_text = source.read_text()
old_request_io = "Wire.requestFrom(IO_Device_addr, (uint8_t) size);"
new_request_io = "Wire.requestFrom((uint8_t)IO_Device_addr, (uint8_t)size);"
old_request_addr = "Wire.requestFrom(addr, (uint8_t) size);"
new_request_addr = "Wire.requestFrom((uint8_t)addr, (uint8_t)size);"
old_return = "  // return value;\n}\n\n// //获取所有巡线探头的原始值"
new_return = "  return 0;\n}\n\n// //获取所有巡线探头的原始值"

for old, new, label in (
    (old_request_io, new_request_io, "IO requestFrom"),
    (old_request_addr, new_request_addr, "addressed requestFrom"),
    (old_return, new_return, "line tracker fallback return"),
):
    if old not in source_text:
        raise SystemExit(f"Unexpected upstream source: {label} pattern not found")
    source_text = source_text.replace(old, new, 1)

source.write_text(source_text)
PY

mkdir -p "$project_dir/lib"
if [[ -e "$target_dir" ]]; then
  backup_dir="$project_dir/lib/DFRobot_K10Box.backup.$(date +%Y%m%d%H%M%S).$$"
  mv "$target_dir" "$backup_dir"
  echo "Existing driver moved to $backup_dir"
fi
mv "$temp_dir/DFRobot_K10Box" "$target_dir"

echo "Installed DFRobot_K10Box at commit $commit into $target_dir"
