#!/usr/bin/env bash
# 新建一个沙雕漫剧项目骨架
# 用法：bash new_project.sh <剧名> [--season 1]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:-}"
SEASON=1
shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --season) SEASON="$2"; shift 2 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

[ -n "${NAME}" ] || { echo "用法：bash new_project.sh <剧名> [--season 1]" >&2; exit 2; }

# 剧名会拼进路径：不许带分隔符、不许 . / ..，也不许控制字符
case "${NAME}" in
  .|..|.*|*/*|*\\*|*[[:cntrl:]]*)
    echo "✗ 剧名不合法：${NAME}（不能以 . 开头，不能含 / 或 \\）" >&2; exit 2 ;;
esac
[ "${#NAME}" -le 64 ] || { echo "✗ 剧名太长（上限 64 字）：${NAME}" >&2; exit 2; }

case "${SEASON}" in
  ''|*[!0-9]*) echo "✗ --season 必须是数字：${SEASON}" >&2; exit 2 ;;
esac
[ "${SEASON}" -ge 1 ] && [ "${SEASON}" -le 99 ] || { echo "✗ --season 必须在 1–99：${SEASON}" >&2; exit 2; }

SEASON_PAD="$(printf '%02d' "${SEASON}")"
BASE="$ROOT/99-项目/${NAME}"
SEASON_DIR="$BASE/第${SEASON_PAD}季"

# 双保险：解析后的路径必须仍在 99-项目 下
case "$SEASON_DIR" in
  "$ROOT/99-项目/"*) ;;
  *) echo "✗ 路径越界：$SEASON_DIR" >&2; exit 2 ;;
esac

mkdir -p "$SEASON_DIR"/{00-立项,01-剧本,02-配音,03-素材/{角色,背景,道具,封面},04-工程,05-成片,06-质检}

[ -f "$BASE/全剧设定.md" ] || cp "$ROOT/00-工作台/全剧设定模板.md" "$BASE/全剧设定.md"
[ -f "$SEASON_DIR/00-立项/立项单.md" ] || cp "$ROOT/00-工作台/立项单模板.md" "$SEASON_DIR/00-立项/立项单.md"
[ -f "$SEASON_DIR/01-剧本/第${SEASON_PAD}集.md" ] || cp "$ROOT/01-剧本/shadiao-script-skill/templates/单集剧本.md" "$SEASON_DIR/01-剧本/第${SEASON_PAD}集.md"
[ -f "$SEASON_DIR/01-剧本/剧本.json" ] || cp "$ROOT/01-剧本/shadiao-script-skill/templates/结构化剧本.json" "$SEASON_DIR/01-剧本/剧本.json"

echo "已创建：$SEASON_DIR"
echo ""
echo "下一步："
echo "  1) 填 $SEASON_DIR/00-立项/立项单.md"
echo "  2) 写 $SEASON_DIR/01-剧本/第${SEASON_PAD}集.md + 剧本.json"
echo "  3) python3 01-剧本/shadiao-script-skill/scripts/validate_script.py ..."
echo "  4) python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py --project '$NAME' --season $SEASON --episode 1"
echo "  5) 出素材 → python3 03-素材/shadiao-asset-skill/scripts/make_index.py --season-dir '$SEASON_DIR'"
echo "  6) node 04-工程/shadiao-anime-skill/scripts/build_anime.mjs --project '$NAME' --season $SEASON --episode 1"
