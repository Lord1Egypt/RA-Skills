#!/bin/bash
# 一集到底：剧本 → 配音 → 工程 → 无头导出 → 混音 → 字幕 → 结尾卡 → 只留一个成片
# 用法：bash render_ep.sh 1 "如有雷同，说明你们也不敢回"
set -e

EP="$1"
LINE2="${2:-如有雷同，纯属巧合}"

case "${EP:-}" in
  ''|*[!0-9]*) echo "✗ 集号必须是数字：${EP:-<空>}" >&2; exit 1 ;;
esac

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL="$(cd "$SCRIPT_DIR/../.." && pwd)"
SEASON="$SCRIPT_DIR/第01季"
APP="${FAA_HOME:-$HOME/FunnyAnimationAssitant}"
CHROME="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
# 每次跑都新建一个独立临时目录，退出时只删这一个（trap 兜底，不会误删别的）
WORK="$(mktemp -d "${TMPDIR:-/tmp}/shadiao-render.XXXXXX")"
trap 'rm -rf -- "$WORK"' EXIT
PROFILE="$WORK/chrome-profile"
EPDIR="$SEASON/02-配音/第0${EP}集"
OUT="$SEASON/05-成片/第0${EP}集.mp4"

echo "═══ 第 0${EP} 集 ═══"

# 1) 剧本
cd "$SEASON/01-剧本" && python3 make_eps.py "$EP"

# 2) 校验
cd "$SKILL"
python3 01-剧本/shadiao-script-skill/scripts/validate_script.py \
  "$SEASON/01-剧本/第0${EP}集.md" --json "$SEASON/01-剧本/第0${EP}集.json" | tail -2

# 3) 配音
python3 02-配音/shadiao-voice-skill/scripts/tts_batch.py \
  --project 示例-周一打工人 --season 1 --episode "$EP" --engine edge --rate-boost +35% --force | tail -2

# 4) 工程：旧工程先备份再重建，不直接删（避免误删其它集的手工修改）
[ -d "$SEASON" ] || { echo "✗ 季目录不存在：$SEASON" >&2; exit 1; }
case "$SEASON" in
  */99-项目/*) ;;
  *) echo "✗ 季目录不在 99-项目 下，拒绝清理：$SEASON" >&2; exit 1 ;;
esac

if [ -d "$SEASON/04-工程" ]; then
  TRASH="$SEASON/.trash/04-工程-$(date '+%Y%m%d-%H%M%S')"
  mkdir -p "$(dirname "$TRASH")"
  mv "$SEASON/04-工程" "$TRASH"
  echo "  旧工程已备份到 ${TRASH#$SEASON/}"
fi
mkdir -p "$SEASON/04-工程" "$APP/public/spike-project"
cd "$SKILL"
node 04-工程/shadiao-anime-skill/scripts/build_anime.mjs \
  --project 示例-周一打工人 --season 1 --episode "$EP" \
  --out "$APP/public/spike-project/示例-周一打工人.anime" | grep -E "场景：|警告" || true

cd "$APP/public/spike-project"
python3 - <<'PY'
import json
from pathlib import Path
root = Path(".")
d = json.loads((root / "示例-周一打工人.anime").read_text())
paths = set()
for ep in d.get("episodes", []):
    for sc in ep.get("scenes", []):
        for b in sc.get("script", []):
            if b.get("ttsConfig", {}).get("audioPath"):
                paths.add(b["ttsConfig"]["audioPath"])
for bg in d.get("assets", {}).get("backgrounds", []):
    paths.add(bg["url"])
for pr in d.get("assets", {}).get("props", []):
    paths.add(pr["url"])
for c in d.get("compositeCharacters", []):
    for o in c.get("objects", []):
        if o.get("type") == "symbol":
            for m in o.get("materials", []):
                paths.add(m["url"])
paths = {p for p in paths if p}
(root / "files.json").write_text(json.dumps(sorted(paths), ensure_ascii=False, indent=2))
print(f"  素材 {len(paths)} 个")
PY

# 5) 无头导出
#    页面只加载本机 localhost:5173 的 dev server，不访问外网；
#    不要把下面的 URL 换成外部地址。容器/CI 里若报 sandbox 权限错误，再自行补参数。
"$CHROME" \
  --headless=new --disable-gpu --enable-unsafe-swiftshader \
  --autoplay-policy=no-user-gesture-required \
  --user-data-dir="$PROFILE" \
  http://localhost:5173/export.html > /dev/null 2>&1 &
CHROME_PID=$!

for i in $(seq 1 120); do
  sleep 5
  if [ -s "$WORK/export.mp4" ]; then break; fi
done
kill $CHROME_PID 2>/dev/null || true

if [ ! -s "$WORK/export.mp4" ]; then
  echo "✗ 导出失败：$WORK/export.mp4 没出现"
  exit 1
fi
echo "  ✓ 导出 $(du -h "$WORK/export.mp4" | cut -f1)"

# 6) 混音 + 字幕 + 结尾卡
cd "$SKILL"
python3 05-出片/shadiao-export-skill/scripts/mix_audio.py \
  --video "$WORK/export.mp4" --out "$WORK/ep${EP}-mix.mp4" \
  --manifest "$EPDIR/配音表.json" \
  --sfx-dir "$SEASON/03-素材/音效" \
  --bgm "$SEASON/03-素材/BGM/bgm_loop.wav" | tail -1

python3 05-出片/shadiao-export-skill/scripts/burn_subtitles.py \
  --video "$WORK/ep${EP}-mix.mp4" --out "$WORK/ep${EP}-sub.mp4" \
  --manifest "$EPDIR/配音表.json" --crf 20 --ratio 9:16 | tail -1

python3 05-出片/shadiao-export-skill/scripts/add_endcard.py \
  --video "$WORK/ep${EP}-sub.mp4" --out "$OUT" \
  --line1 "本故事纯属虚构" --line2 "$LINE2" --duration 2.6 | tail -1

# 7) 抽封面（临时目录由 trap 在退出时清理）
ffmpeg -y -ss 2 -i "$OUT" -frames:v 1 -q:v 2 "$SEASON/05-成片/第0${EP}集-封面.jpg" > /dev/null 2>&1 || true

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
echo "✓ $OUT"
