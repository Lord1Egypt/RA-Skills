#!/usr/bin/env bash
# yt2podcast 环境自检:装完/换机器/出问题先跑这个。
#
#   bash scripts/doctor.sh          # 人看的清单
#   bash scripts/doctor.sh --json   # 机读结果
#
# 退出码: 0 = 全部就绪; 1 = 有阻塞项(❌); 2 = 只有警告(⚠️)
set -uo pipefail

JSON=0
[ "${1:-}" = "--json" ] && JSON=1

ROOT="${YT2PODCAST_ROOT:-$HOME/.openclaw/workspace/yt2podcast}"

OKS=()
FAILS=()
WARNS=()

ok()   { OKS+=("$1");   [ "$JSON" -eq 0 ] && printf '✅ %s\n' "$1"; }
bad()  { FAILS+=("$1|||$2"); [ "$JSON" -eq 0 ] && printf '❌ %s\n   → 修复: %s\n' "$1" "$2"; }
warn() { WARNS+=("$1|||$2"); [ "$JSON" -eq 0 ] && printf '⚠️  %s\n   → %s\n' "$1" "$2"; }

have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- 1. 命令行依赖
for bin in opencli ffmpeg ffprobe python3; do
  if have "$bin"; then ok "命令行: $bin"; else
    case "$bin" in
      opencli) bad "缺少 opencli" "npm i -g @jackwener/opencli" ;;
      ffmpeg|ffprobe) bad "缺少 $bin" "brew install ffmpeg" ;;
      python3) bad "缺少 python3" "xcode-select --install 或 brew install python3" ;;
    esac
  fi
done
if have openclaw; then ok "命令行: openclaw(完成通知用)"; else
  warn "没有 openclaw CLI" "任务仍会跑完,但不会唤醒会话发通知"
fi

# ---------------------------------------------------------------- 2. opencli adapter
if have opencli; then
  if opencli notebooklm --help >/dev/null 2>&1; then ok "adapter: notebooklm"; else
    bad "缺少 notebooklm adapter" "按 opencli 文档安装 notebooklm adapter(本 skill 不含 adapter)"
  fi
  if opencli xiaoyuzhou --help >/dev/null 2>&1; then ok "adapter: xiaoyuzhou"; else
    bad "缺少 xiaoyuzhou adapter" "按 opencli 文档安装 xiaoyuzhou adapter(本 skill 不含 adapter)"
  fi
fi

# ---- 2.5 本 skill 自带的 adapter(opencli 基线里没有这三个命令) ----
CLIS_DIR="${OPENCLI_HOME:-$HOME/.opencli}/clis"
ADAPTER_SRC="$(cd "$(dirname "$0")/.." && pwd)/adapters"
for rel in notebooklm/download-audio.js xiaoyuzhou/upload.js xiaoyuzhou/upload-status.js; do
  if [ ! -f "$CLIS_DIR/$rel" ]; then
    bad "缺少 adapter: $rel(opencli 基线没有这个命令)" "bash $(dirname "$0")/install-adapters.sh --install"
  elif [ -f "$ADAPTER_SRC/$rel" ] && ! cmp -s "$ADAPTER_SRC/$rel" "$CLIS_DIR/$rel"; then
    warn "adapter 与仓库版本不一致: $rel" "bash $(dirname "$0")/install-adapters.sh --install 同步(旧文件会自动备份)"
  else
    ok "adapter 文件: $rel"
  fi
done

# ---------------------------------------------------------------- 3. 登录态
if have opencli && opencli notebooklm --help >/dev/null 2>&1; then
  if timeout 120 opencli notebooklm whoami -f json >/tmp/yt2p-doctor-nb.json 2>&1; then
    ok "登录: NotebookLM"
  else
    bad "NotebookLM 未登录" "opencli notebooklm login(或先 opencli notebooklm open <nb> 在浏览器里登录)"
  fi
fi
PODCAST_ID="${YT2PODCAST_PODCAST_ID:-}"
if have opencli && opencli xiaoyuzhou --help >/dev/null 2>&1 && [ -n "$PODCAST_ID" ]; then
  # 小宇宙主播后台的登录态没法直接探测,借"查一个已知单集的状态"来验证:
  # 能查到 = 会话有效;查不到 = 未登录或会话过期。
  KNOWN_EP=$(python3 - "$ROOT" <<'PY'
import glob, json, os, sys
best = ""
for path in glob.glob(os.path.join(sys.argv[1], "jobs", "*.json")):
    try:
        job = json.load(open(path, encoding="utf-8"))
    except Exception:
        continue
    if job.get("episode_id"):
        best = job["episode_id"]
print(best)
PY
)
  if [ -n "$KNOWN_EP" ]; then
    if timeout 150 opencli xiaoyuzhou upload-status "$KNOWN_EP" --podcast "$PODCAST_ID" --site-session persistent --keep-tab true -f json >/dev/null 2>&1; then
      ok "登录: 小宇宙主播后台(用单集 $KNOWN_EP 验证)"
    else
      bad "小宇宙主播后台未登录或会话过期" "浏览器打开 https://podcaster.xiaoyuzhoufm.com/ 登录后重试"
    fi
  else
    warn "小宇宙登录态无法自动探测(还没有历史单集)" "首次上传前先在浏览器登录 https://podcaster.xiaoyuzhoufm.com/"
  fi
fi

# ---------------------------------------------------------------- 4. 节目 id
if [ -n "$PODCAST_ID" ]; then ok "节目 id: $PODCAST_ID"; else
  bad "没有小宇宙节目 id" "export YT2PODCAST_PODCAST_ID=<你的节目id>,或建 job 时传 --podcast"
fi

# ---------------------------------------------------------------- 5. Google 存储可达性
PROXY="${YT2PODCAST_PROXY:-${HTTPS_PROXY:-}}"
if [ -z "$PROXY" ] && [ "$(uname -s)" = "Darwin" ]; then
  SPROXY=$(scutil --proxy 2>/dev/null)
  if echo "$SPROXY" | grep -q "HTTPSEnable : 1"; then
    HOSTP=$(echo "$SPROXY" | awk -F': ' '/HTTPSProxy/{print $2}')
    PORTP=$(echo "$SPROXY" | awk -F': ' '/HTTPSPort/{print $2}')
    PROXY="http://$HOSTP:$PORTP"
  fi
fi
CHECK_URL="https://lh3.googleusercontent.com/"
if [ -n "$PROXY" ]; then
  CODE=$(curl -sS -m 20 -o /dev/null -w '%{http_code}' -x "$PROXY" "$CHECK_URL" 2>/dev/null || echo 000)
  if [ "$CODE" != "000" ]; then ok "Google 存储可达(代理 $PROXY)"; else
    bad "代理 $PROXY 打不开 lh3.googleusercontent.com" "检查 Clash/代理是否在跑;音频下载会失败"
  fi
else
  CODE=$(curl -sS -m 15 -o /dev/null -w '%{http_code}' "$CHECK_URL" 2>/dev/null || echo 000)
  if [ "$CODE" != "000" ]; then ok "Google 存储可达(直连)"; else
    warn "直连 lh3.googleusercontent.com 超时,也没检测到代理" "设置 YT2PODCAST_PROXY=http://127.0.0.1:7897 或打开系统代理,否则下载音频会 fetch failed"
  fi
fi

# ---------------------------------------------------------------- 6. 数据目录
if mkdir -p "$ROOT/jobs" 2>/dev/null; then ok "数据目录: $ROOT"; else
  bad "数据目录不可写: $ROOT" "检查权限,或设置 YT2PODCAST_ROOT 到可写目录"
fi

# ---------------------------------------------------------------- 汇总
if [ "$JSON" -eq 1 ]; then
  python3 - "$(printf '%s\n' "${OKS[@]:-}")" "$(printf '%s\n' "${FAILS[@]:-}")" "$(printf '%s\n' "${WARNS[@]:-}")" <<'PY'
import json, sys
def split(block):
    out = []
    for line in block.splitlines():
        line = line.strip()
        if not line:
            continue
        if "|||" in line:
            name, fix = line.split("|||", 1)
            out.append({"item": name, "fix": fix})
        else:
            out.append({"item": line, "fix": None})
    return out
ok_block, fail_block, warn_block = sys.argv[1], sys.argv[2], sys.argv[3]
print(json.dumps({
    "ok": split(ok_block),
    "blocking": split(fail_block),
    "warnings": split(warn_block),
    "ready": len(split(fail_block)) == 0,
}, ensure_ascii=False, indent=2))
PY
fi

if [ "${#FAILS[@]}" -gt 0 ]; then
  [ "$JSON" -eq 0 ] && printf '\n%d 项阻塞,%d 项警告。修好后重跑本脚本。\n' "${#FAILS[@]}" "${#WARNS[@]}"
  exit 1
fi
if [ "${#WARNS[@]}" -gt 0 ]; then
  [ "$JSON" -eq 0 ] && printf '\n没有阻塞项,%d 项警告。\n' "${#WARNS[@]}"
  exit 2
fi
[ "$JSON" -eq 0 ] && printf '\n全部就绪,可以开始跑任务了。\n'
exit 0
