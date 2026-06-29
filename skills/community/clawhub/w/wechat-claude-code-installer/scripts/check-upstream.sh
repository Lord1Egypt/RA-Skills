#!/usr/bin/env bash
# check-upstream.sh - 检查上游 wechat-claude-code 是否有新 commit
#
# 灵感来自 GordenSun PPTSkill 的 apply_update.py：
# AI 每次启用 skill 第一件事就是查上游漂移，不主动 pull。
#
# 用法：
#   check-upstream.sh           # 检查上游是否有新 commit
#   check-upstream.sh --pin     # 把当前安装版本写入 .upstream-pin
#   check-upstream.sh --since   # 显示 pin 以来上游所有 commit 列表
set -eu

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
UPSTREAM_DIR="$HOME/.claude/skills/wechat-claude-code"
PIN_FILE="$SKILL_DIR/.upstream-pin"
REPO="Wechat-ggGitHub/wechat-claude-code"
API="https://api.github.com/repos/$REPO"

usage() {
  cat <<EOF
check-upstream.sh - 检查上游 wechat-claude-code 漂移

用法:
  $0           检查上游是否有新 commit（默认）
  $0 --pin     把当前 .claude/skills/wechat-claude-code 的 commit 写入 .upstream-pin
  $0 --since   显示 pin 以来上游所有 commit 列表
  $0 --help    显示帮助
EOF
}

get_local_commit() {
  if [ -d "$UPSTREAM_DIR/.git" ]; then
    (cd "$UPSTREAM_DIR" && git log -1 --format=%H 2>/dev/null | cut -c1-7)
  else
    echo ""
  fi
}

get_remote_latest() {
  /usr/bin/curl -s --max-time 10 "$API/commits/main" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('sha','')[:7])" 2>/dev/null
}

get_remote_date() {
  /usr/bin/curl -s --max-time 10 "$API/commits/main" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('commit',{}).get('author',{}).get('date','')[:10])" 2>/dev/null
}

cmd_pin() {
  local local_commit
  local_commit=$(get_local_commit)
  if [ -z "$local_commit" ]; then
    echo "❌ 没找到本地上游安装（$UPSTREAM_DIR）" >&2
    exit 1
  fi
  printf "%s\n" "$local_commit" > "$PIN_FILE"
  echo "✅ 已 pin 当前安装版本: $local_commit"
  echo "   写入: $PIN_FILE"
  echo "   下次跑 check-upstream.sh 会基于这个版本检查漂移"
}

cmd_since() {
  if [ ! -f "$PIN_FILE" ]; then
    echo "⚠️  还没 pin 过版本，跑 check-upstream.sh --pin 先" >&2
    exit 1
  fi
  local pin_commit
  pin_commit=$(cat "$PIN_FILE")
  echo "Pin 版本: $pin_commit"
  echo ""
  echo "=== 自 pin 以来上游 commit ==="
  /usr/bin/curl -s --max-time 10 "$API/compare/$pin_commit...main" \
    | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    commits = d.get('commits', [])
    ahead = d.get('ahead_by', 0)
    behind = d.get('behind_by', 0)
    if ahead == 0:
        print('✅ 已是最新（领先 0 / 落后 0）')
    else:
        print(f'⬆️  落后 {ahead} 个 commit')
        for c in commits[-20:]:
            sha = c['sha'][:7]
            msg = c['commit']['message'].splitlines()[0][:80]
            date = c['commit']['author']['date'][:10]
            print(f'  {sha}  {date}  {msg}')
except Exception as e:
    print(f'❌ 调 API 失败: {e}', file=sys.stderr)
    sys.exit(1)
"
}

cmd_check() {
  echo "============================================================"
  echo "  check-upstream :: wechat-claude-code"
  echo "============================================================"
  echo ""

  # 本地安装版本
  local local_commit
  local_commit=$(get_local_commit)
  if [ -z "$local_commit" ]; then
    echo "⚠️  本地未安装上游项目（$UPSTREAM_DIR 不存在）"
    echo "   先跑 install.sh 再来检查"
    return 0
  fi
  echo "本地安装: $local_commit"

  # Pin 版本（用户上次确认 OK 的版本）
  local pin_commit=""
  if [ -f "$PIN_FILE" ]; then
    pin_commit=$(cat "$PIN_FILE")
    echo "Pin 版本: $pin_commit"
  else
    echo "Pin 版本: (尚未 pin —— 推荐跑 --pin 把当前版本固定下来)"
  fi

  # 远程最新
  echo ""
  echo "查询远程最新 commit..."
  local remote_commit remote_date
  remote_commit=$(get_remote_latest)
  remote_date=$(get_remote_date)
  if [ -z "$remote_commit" ]; then
    echo "❌ 网络不通或 API 失败"
    return 1
  fi
  echo "远程 main: $remote_commit ($remote_date)"
  echo ""

  # 比较
  if [ "$local_commit" = "$remote_commit" ]; then
    echo "✅ 本地已是远程最新版"
    return 0
  fi

  # 有漂移
  echo "⬆️  发现上游有新 commit：本地 $local_commit → 远程 $remote_commit"
  echo ""
  echo "建议动作："
  echo "  1. 看变更：$0 --since（显示 pin 以来所有 commit）"
  echo "  2. 升级试装："
  echo "     cd $UPSTREAM_DIR && git pull && npm install"
  echo "  3. 升级后验证 6 个坑修法还有效，然后 $0 --pin 锁新版"
  echo "  4. 如修法已被上游修了，更新 installer SKILL.md"
  echo ""
  echo "🔗 上游 commits：https://github.com/$REPO/commits/main"
  return 0
}

case "${1:-check}" in
  --help|-h) usage ;;
  --pin)     cmd_pin ;;
  --since)   cmd_since ;;
  check|"")  cmd_check ;;
  *) echo "unknown command: $1" >&2; usage; exit 1 ;;
esac
