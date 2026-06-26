#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法:
  refresh_devices.sh [--speaker-server 名称] [--iot-server 名称] [--out-dir 目录]

示例:
  refresh_devices.sh
  refresh_devices.sh --speaker-server xiaodu --iot-server xiaodu-iot
EOF
}

SPEAKER_SERVER="xiaodu"
IOT_SERVER="xiaodu-iot"
OUT_DIR="${XIAODU_WORKSPACE_DIR:-$HOME/.openclaw/workspace/xiaodu-control}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --speaker-server)
      SPEAKER_SERVER="${2:-}"
      shift 2
      ;;
    --iot-server)
      IOT_SERVER="${2:-}"
      shift 2
      ;;
    --out-dir)
      OUT_DIR="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if ! command -v mcporter >/dev/null 2>&1; then
  echo "PATH 中未找到 mcporter" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

SPEAKER_JSON="$OUT_DIR/speaker-devices.json"
IOT_JSON="$OUT_DIR/iot-devices.json"
SUMMARY_MD="$OUT_DIR/device-summary.md"

echo "[xiaodu-control] 正在从 '$SPEAKER_SERVER' 拉取智能屏设备"
mcporter call "${SPEAKER_SERVER}.list_user_devices" --output json >"$SPEAKER_JSON"

if [[ -n "$IOT_SERVER" ]]; then
  echo "[xiaodu-control] 正在从 '$IOT_SERVER' 拉取 IoT 设备"
  if ! mcporter call "${IOT_SERVER}.GET_ALL_DEVICES_WITH_STATUS" --output json >"$IOT_JSON"; then
    echo "[xiaodu-control] 警告: 从 '$IOT_SERVER' 拉取 IoT 设备失败" >&2
    rm -f "$IOT_JSON"
  fi
fi

python3 - "$SPEAKER_JSON" "$IOT_JSON" "$SUMMARY_MD" <<'PY'
import json
import os
import sys
from pathlib import Path

speaker_path = Path(sys.argv[1])
iot_path = Path(sys.argv[2])
summary_path = Path(sys.argv[3])

def load_json(path):
    if not path.exists():
        return None
    with path.open() as f:
        return json.load(f)

def extract_rows(obj, limit=20):
    rows = []

    def walk(node):
        if len(rows) >= limit:
            return
        if isinstance(node, dict):
            lowered = {str(k).lower(): v for k, v in node.items()}
            if any(k in lowered for k in ("name", "devicename", "appliancename", "roomname")):
                rows.append({
                    "name": lowered.get("devicename") or lowered.get("appliancename") or lowered.get("name") or "",
                    "room": lowered.get("roomname") or lowered.get("room") or "",
                    "status": lowered.get("status") or lowered.get("online") or lowered.get("power") or "",
                })
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)
    return rows

speaker = load_json(speaker_path)
iot = load_json(iot_path)

lines = [
    "# 小度设备快照",
    "",
    f"- 智能屏 JSON: `{speaker_path}`",
]

if iot is not None:
    lines.append(f"- IoT JSON: `{iot_path}`")
lines.append("")

if speaker is not None:
    rows = extract_rows(speaker)
    lines.append("## 智能屏设备")
    lines.append("")
    lines.append("| 设备名 | 房间 | CUID | Client ID | 在线 |")
    lines.append("| --- | --- | --- | --- | --- |")
    devices = speaker if isinstance(speaker, list) else []
    if devices:
        for item in devices:
            location = item.get("location") or {}
            room = location.get("room") or location.get("floor") or location.get("house") or ""
            lines.append(
                f"| {item.get('device_name', '')} | {room} | {item.get('cuid', '')} | {item.get('client_id', '')} | {item.get('online_status', '')} |"
            )
        lines.append("")
    lines.append("### 自动抽取摘要")
    lines.append("")
    if rows:
        lines.append("| 设备名 | 房间 | 状态 |")
        lines.append("| --- | --- | --- |")
        for row in rows:
            lines.append(f"| {row['name']} | {row['room']} | {row['status']} |")
    else:
        lines.append("没有提取到明显的智能屏设备行，请直接检查 JSON。")
    lines.append("")

if iot is not None:
    rows = extract_rows(iot)
    lines.append("## IoT 设备")
    lines.append("")
    if rows:
        lines.append("| 设备名 | 房间 | 状态 |")
        lines.append("| --- | --- | --- |")
        for row in rows:
            lines.append(f"| {row['name']} | {row['room']} | {row['status']} |")
    else:
        lines.append("没有提取到明显的 IoT 设备行，请直接检查 JSON。")
    lines.append("")

summary_path.write_text("\n".join(lines))
PY

echo "[xiaodu-control] 已写入:"
echo "  $SPEAKER_JSON"
if [[ -f "$IOT_JSON" ]]; then
  echo "  $IOT_JSON"
fi
echo "  $SUMMARY_MD"
