#!/usr/bin/env bash
# wdp 会话级钩子（SessionStart / PreCompact）
# 用法: bash wdp-hook.sh <load|load-after-clear|load-after-compact|save-precompact>
# 行为: 仅当当前项目已有 wdp 快照时输出 systemMessage 提醒；否则静默退出（exit 0）。
# 提醒只提示、不自动执行；/clear 前无法提醒（官方无此钩子），改为清空后新会话提醒。
set -u

event="${1:-}"
[ -z "$event" ] && exit 0

slug="$(basename "$PWD")"

# 存储根解析（与 /wdp-ctx 技能一致）：项目级优先，用户级兜底。
# 数据与技能代码分离：数据在 .claude/wdp/（技能重装不影响）。
# 只认 2*.md（时间戳快照），latest.md / profile.md 不算"已有快照"。
root=""
for r in "$PWD/.claude/wdp/summaries" "$HOME/.claude/wdp/summaries"; do
  if ls "$r/$slug"/2*.md >/dev/null 2>&1; then
    root="$r"
    break
  fi
done

[ -z "$root" ] && exit 0

case "$event" in
  load)
    msg="本会话存在 wdp 工作快照。运行 /wdp-ctx init 可载入项目上下文（档案 + 最新快照），快速接续上次工作。"
    ;;
  load-after-clear)
    msg="上次会话已结束。运行 /wdp-ctx init 可载入项目上下文，接续上次工作。"
    ;;
  load-after-compact)
    msg="上下文刚被压缩。运行 /wdp-ctx init 可重新载入项目上下文，接续上次工作。"
    ;;
  save-precompact)
    msg="上下文即将压缩。建议先运行 /wdp-ctx sum 保存当前工作快照，压缩后 /wdp-ctx init 即可接续。"
    ;;
  *)
    exit 0
    ;;
esac

printf '{"systemMessage": "%s"}\n' "$msg"
