#!/usr/bin/env bash
# 给「沙雕动画小助手」打 9:16 竖屏补丁
# 原版相机基准是 16:9（1456×819），导出预设也只有 1080p/720p 横屏。
# 本脚本把相机基准改成 819×1456，并把导出预设改成 1080×1920 / 720×1280。
#
# 用法：
#   bash patch_vertical.sh status
#   bash patch_vertical.sh apply
#   bash patch_vertical.sh restore
set -euo pipefail

APP="${FAA_HOME:-$HOME/FunnyAnimationAssitant}"
CANVAS="$APP/src/constants/canvas.ts"
EXPORT="$APP/src/utils/videoExport/constants.ts"
CANVAS_BAK="$CANVAS.bak-vertical"
EXPORT_BAK="$EXPORT.bak-vertical"
CMD="${1:-status}"

[ -d "$APP" ] || { echo "找不到 app：$APP（先运行 setup_app.sh install）" >&2; exit 1; }
[ -f "$CANVAS" ] || { echo "找不到 $CANVAS" >&2; exit 1; }
[ -f "$EXPORT" ] || { echo "找不到 $EXPORT" >&2; exit 1; }

status() {
  echo "app：$APP"
  grep -n "CAMERA_BASE_WIDTH\|CAMERA_BASE_HEIGHT" "$CANVAS" | head -4
  grep -n "width: 1080\|width: 1920\|label: '1080" "$EXPORT" | head -4
  if [ -f "$CANVAS_BAK" ]; then echo "备份：$CANVAS_BAK"; fi
}

apply() {
  [ -f "$CANVAS_BAK" ] || cp "$CANVAS" "$CANVAS_BAK"
  [ -f "$EXPORT_BAK" ] || cp "$EXPORT" "$EXPORT_BAK"

  python3 - "$CANVAS" "$EXPORT" <<'PY'
import re, sys
canvas, export = sys.argv[1], sys.argv[2]

s = open(canvas, encoding="utf-8").read()
s = s.replace(" * 相机基准视口尺寸（16:9）", " * 相机基准视口尺寸（9:16 · 沙雕竖屏补丁）")
s = re.sub(r"export const CAMERA_BASE_WIDTH = \d+", "export const CAMERA_BASE_WIDTH = 819", s)
s = re.sub(r"export const CAMERA_BASE_HEIGHT = \d+", "export const CAMERA_BASE_HEIGHT = 1456", s)
open(canvas, "w", encoding="utf-8").write(s)

s = open(export, encoding="utf-8").read()
s = re.sub(
    r"export const RESOLUTION_PRESETS = \[.*?\] as const",
    "export const RESOLUTION_PRESETS = [\n"
    "    { id: '1080p', label: '1080×1920 竖屏', width: 1080, height: 1920 },\n"
    "    { id: '720p', label: '720×1280 竖屏', width: 720, height: 1280 },\n"
    "] as const",
    s,
    flags=re.S,
)
s = s.replace("    fontSize: 24,", "    fontSize: 30,")
s = s.replace("    bottomPercent: 5,", "    bottomPercent: 10,")
open(export, "w", encoding="utf-8").write(s)
print("patched")
PY

  echo "已打 9:16 补丁。重启 dev server 生效：bash 00-工作台/setup_app.sh start"
}

restore() {
  [ -f "$CANVAS_BAK" ] && cp "$CANVAS_BAK" "$CANVAS" || echo "没有 canvas 备份" >&2
  [ -f "$EXPORT_BAK" ] && cp "$EXPORT_BAK" "$EXPORT" || echo "没有 export 备份" >&2
  echo "已恢复原版（16:9）。重启 dev server 生效。"
}

case "$CMD" in
  status) status ;;
  apply) apply ;;
  restore) restore ;;
  *) echo "用法：bash patch_vertical.sh [status|apply|restore]" ;;
esac
