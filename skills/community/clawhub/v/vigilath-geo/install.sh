#!/usr/bin/env bash
# Vigilath GEO skill 一行安装 —— 给对方 agent(小龙虾)drop-in。
#
#   # 免 token(推荐):终端出配对码,浏览器点一下批准即可
#   curl -fsSL https://vigilath.cn/skill/install.sh | bash
#
#   # 只装某几个窄技能(默认装全部 7 个窄技能)
#   curl -fsSL https://vigilath.cn/skill/install.sh | bash -s -- --skills site-audit,seo-audit
#   # 装兜底全能包(一次只肯装一个技能的宿主用这个)
#   curl -fsSL https://vigilath.cn/skill/install.sh | bash -s -- --skills geo
#
#   # 已有 token(老方式,仍支持)
#   curl -fsSL https://vigilath.cn/skill/install.sh | bash -s -- <你的token> --base https://vigilath.cn
#
# 干三件事:① 把 skill 拷进探测到的 skills 目录(可多个平台同时装);
#           ② 拿到 token 写进 ~/.vigilath/config(chmod 600);③ 自检。
# 不挑框架:自动探测 OpenClaw / Claude / .agents / 当前项目,也可用 --dir 或 VIGILATH_SKILLS_DIR 指定。
#
# ★ --base 是"从哪个域名装就指向哪个域名"的关键:本脚本被 `curl | bash` 管道执行时,
#   拿不到自己的下载 URL($0 只是 "bash"),所以基址只能靠外部传入或走下面的默认值。
#   控制台「对接集成」页生成的命令会自动带上 --base <当前站点 origin>,
#   这样 test / vigilath.cn / www.vigilath.cn / www.vigilath.com.cn 全部自动对齐。
set -euo pipefail

# 默认基址:已备案的国内域名。仅在没传 --base 也没设环境变量时兜底。
SKILL_BASE="${VIGILATH_SKILL_BASE:-https://vigilath.cn/skill}"   # skill 文件托管地址
TOKEN=""
SKILLS_DIR="${VIGILATH_SKILLS_DIR:-}"
# 七个窄技能 = 默认装的一组。**不含兜底全能包 vigilath-geo** ——
# 全能包的触发语覆盖全部七种场景,和窄技能同装会让宿主 agent 选不准,只能二选一。
NARROW="site-audit seo-audit mention report radar content weekly sentinel"
WANT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --dir)   SKILLS_DIR="$2"; shift 2 ;;
    --token) TOKEN="$2"; shift 2 ;;
    # --base 接受带不带 /skill 后缀都行,统一归一成 <origin>/skill
    --base)  SKILL_BASE="${2%/}"; SKILL_BASE="${SKILL_BASE%/skill}/skill"; shift 2 ;;
    # --skills all|geo|<逗号分隔的短名>;不传 = 七个窄技能
    --skills) WANT="$(printf '%s' "$2" | tr ',' ' ')"; shift 2 ;;
    -*) echo "未知参数:$1" >&2; exit 2 ;;
    *) [ -z "$TOKEN" ] && TOKEN="$1"; shift ;;
  esac
done

say() { printf '\033[36m[vigilath-geo]\033[0m %s\n' "$*"; }
die() { printf '\033[31m[vigilath-geo] 错误:%s\033[0m\n' "$*" >&2; exit 1; }
warn() { printf '\033[33m[vigilath-geo] %s\033[0m\n' "$*" >&2; }

command -v python3 >/dev/null 2>&1 || die "需要 python3(skill 客户端纯标准库,无三方依赖)"
command -v curl    >/dev/null 2>&1 || die "需要 curl"

API_BASE="${SKILL_BASE%/skill}/api/agent/v1"

# ── ① 没给 token 就走设备码授权:终端出码,人在浏览器点批准 ────────────────────
# 好处:token 不经过剪贴板、不进 shell history,官网可以印同一条无参数命令。
device_login() {
  local resp status
  resp="$(curl -fsS -m 20 -X POST "$API_BASE/device/code" \
            -H 'Content-Type: application/json' \
            -d "{\"client\":\"$(hostname 2>/dev/null || echo cli)\"}" 2>/dev/null)" \
    || die "连不上 $API_BASE —— 检查网络,或用 --base 指定正确的站点域名"

  # 用 python3 解析并吐出 shell 赋值(值都经 shlex.quote,不怕特殊字符)
  eval "$(printf '%s' "$resp" | python3 -c '
import json, shlex, sys
try:
    d = json.load(sys.stdin)
except Exception:
    print("DEV_STATUS=" + shlex.quote("parse_error")); sys.exit(0)
for k in ("status", "device_code", "user_code", "verify_url", "verify_url_complete", "interval", "expires_in"):
    print("DEV_" + k.upper() + "=" + shlex.quote(str(d.get(k, ""))))
')"
  [ "${DEV_STATUS:-}" = "ok" ] || die "起授权流程失败(服务端返回:${DEV_STATUS:-空})"

  printf '\n'
  say "请在浏览器完成授权(10 分钟内有效):"
  printf '\n    打开:\033[4m%s\033[0m\n' "${DEV_VERIFY_URL_COMPLETE:-$DEV_VERIFY_URL}"
  printf '    配对码:\033[1;33m%s\033[0m\n\n' "$DEV_USER_CODE"
  say "等待批准中…(在浏览器点「批准」后这里会自动继续)"

  local interval="${DEV_INTERVAL:-5}" deadline out st
  deadline=$(( $(date +%s) + ${DEV_EXPIRES_IN:-600} ))
  while [ "$(date +%s)" -lt "$deadline" ]; do
    sleep "$interval"
    # 轮询失败(网络抖动)不该中断整个流程,吞掉错误继续等
    out="$(curl -fsS -m 20 -X POST "$API_BASE/device/token" \
             -H 'Content-Type: application/json' \
             -d "{\"device_code\":\"$DEV_DEVICE_CODE\"}" 2>/dev/null || true)"
    [ -n "$out" ] || continue
    eval "$(printf '%s' "$out" | python3 -c '
import json, shlex, sys
try:
    d = json.load(sys.stdin)
except Exception:
    d = {"status": "pending"}
for k in ("status", "token", "message"):
    print("POLL_" + k.upper() + "=" + shlex.quote(str(d.get(k, ""))))
')"
    st="${POLL_STATUS:-pending}"
    case "$st" in
      approved) TOKEN="$POLL_TOKEN"; say "✅ 授权成功"; return 0 ;;
      pending|slow_down) : ;;
      denied)   die "${POLL_MESSAGE:-用户拒绝了本次授权}" ;;
      expired)  die "${POLL_MESSAGE:-配对码已过期,请重新运行安装命令}" ;;
      *) : ;;
    esac
  done
  die "等待授权超时(10 分钟),请重新运行安装命令"
}

[ -n "$TOKEN" ] || device_login

# ── ② 探测 skills 目录 ───────────────────────────────────────────────────────
# --dir / 环境变量指定时只装那一个;否则装进**所有**已存在的 agent skills 目录,
# 这样同一台机器上装了多个 agent(OpenClaw + Claude Code …)都能扫到本 skill。
DESTS=()
if [ -n "$SKILLS_DIR" ]; then
  DESTS+=("$SKILLS_DIR")
else
  [ -d "$HOME/.openclaw/skills" ] && DESTS+=("$HOME/.openclaw/skills")          # OpenClaw 全局
  [ -d "$HOME/.claude/skills" ]   && DESTS+=("$HOME/.claude/skills")            # Claude Code 全局
  [ -d "$HOME/.agents/skills" ]   && DESTS+=("$HOME/.agents/skills")            # 通用个人 agent 目录
  # 当前项目 workspace(OpenClaw 的 <workspace>/skills 就长这样)。
  # ★ 但要排掉「这就是 skill 源码仓库本身」的情况 —— 在仓库根跑一次安装,
  #   会把安装产物(client 副本)写回源码目录,污染 git 工作区。2026-08-19 踩过。
  if [ -d "./skills" ] && [ ! -f "./skills/vigilath-geo/install.sh" ]; then
    DESTS+=("$(pwd)/skills")
  fi
  [ ${#DESTS[@]} -eq 0 ] && DESTS+=("$HOME/.vigilath/skills")                   # 都没有时的兜底
fi

# 决定装哪些技能。短名 → 目录名 vigilath-<短名>;`all` = 七个窄技能 + 兜底全能包。
case "${WANT:-}" in
  "")    PICK="$NARROW" ;;
  all)   PICK="$NARROW geo" ;;
  *)     PICK="$WANT" ;;
esac

# 下载一次到临时目录,再分发到各个 skills 目录(避免重复下载)。
# 客户端**全仓库只有一份源**(vigilath-geo/scripts/geo_client.py),装的时候复制进每个技能目录 ——
# 各技能自带一份副本是 skill 规范要求的自包含,但源只有一份,不会各自漂移。
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
ROOT_DIR="$(cd "$SELF_DIR/.." 2>/dev/null && pwd || true)"   # 本地仓库直跑时的 skills/ 根

fetch() { # fetch <相对 skills/ 的路径> <目标>;本地有就用本地,否则下载
  if [ -n "$ROOT_DIR" ] && [ -f "$ROOT_DIR/$1" ]; then cp "$ROOT_DIR/$1" "$2"; return 0; fi
  # 新版托管布局:<base>/<技能目录>/...;老布局只暴露了全能包,兼容一下
  curl -fsSL "$SKILL_BASE/$1" -o "$2" 2>/dev/null && return 0
  curl -fsSL "$SKILL_BASE/${1#vigilath-geo/}" -o "$2" 2>/dev/null && return 0
  return 1
}

fetch "vigilath-geo/scripts/geo_client.py" "$STAGE/geo_client.py" \
  || die "下载客户端失败(基址 $SKILL_BASE)——检查网络或 --base"

FIRST_DEST=""
INSTALLED=""
for name in $PICK; do
  slug="vigilath-${name#vigilath-}"
  if ! fetch "$slug/SKILL.md" "$STAGE/SKILL.md"; then
    warn "跳过 $slug(取不到 SKILL.md,可能是技能名写错了)"
    continue
  fi
  # 全能包多带一份 README,窄技能不需要
  HAS_README=0
  [ "$slug" = "vigilath-geo" ] && fetch "$slug/README.md" "$STAGE/README.md" && HAS_README=1

  for d in "${DESTS[@]}"; do
    dest="$d/$slug"
    mkdir -p "$dest/scripts"
    cp "$STAGE/SKILL.md" "$dest/SKILL.md"
    [ "$HAS_README" = "1" ] && cp "$STAGE/README.md" "$dest/README.md"
    cp "$STAGE/geo_client.py" "$dest/scripts/geo_client.py"
    [ -z "$FIRST_DEST" ] && FIRST_DEST="$dest"
  done
  INSTALLED="$INSTALLED $slug"
done

[ -n "$INSTALLED" ] || die "一个技能都没装上 —— 检查 --skills 的名字,或基址 $SKILL_BASE 是否可达"
for d in "${DESTS[@]}"; do say "已安装到 $d:$INSTALLED"; done

# ── ③ token + API 基址写配置(基址与下载 skill 的 host 同源,自动对齐 test/prod)──
mkdir -p "$HOME/.vigilath"
umask 077
{
  echo "# Vigilath GEO —— 机密,勿提交"
  echo "VIGILATH_AGENT_TOKEN=$TOKEN"
  echo "VIGILATH_BASE=$API_BASE"
} > "$HOME/.vigilath/config"
chmod 600 "$HOME/.vigilath/config"
say "凭证已写入 ~/.vigilath/config(权限 600,API 基址 $API_BASE)"

# ── ④ 自检 ──────────────────────────────────────────────────────────────────
# 免登录那条(check)必须能跑 —— 它是唯一不依赖凭证的能力,先验它,再验授权链路。
say "自检中…"
if python3 "$FIRST_DEST/scripts/geo_client.py" check https://example.com --no-seo >/dev/null 2>&1; then
  say "✅ 免登录检测可用(无需凭证):geo_client.py check <网址>"
else
  warn "免登录检测没跑通 —— 检查网络能否访问 ${API_BASE%/agent/v1}"
fi
if python3 "$FIRST_DEST/scripts/geo_client.py" capabilities >/dev/null 2>&1; then
  say "✅ 授权链路已通。试试:python3 $FIRST_DEST/scripts/geo_client.py chat \"我被搜到几个问题?\""
else
  warn "已安装,但授权链路未通(token 失效?)。重新授权:python3 $FIRST_DEST/scripts/geo_client.py login"
fi
