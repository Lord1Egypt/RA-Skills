#!/usr/bin/env bash
# 把本 skill 自带的 opencli adapter 安装到 ~/.opencli/clis/
#
# 为什么需要:opencli 官方基线里没有 notebooklm download-audio、
# xiaoyuzhou upload / upload-status 这三个命令(我们补的),不装就缺核心能力。
#
#   bash scripts/install-adapters.sh --check     # 只检查装没装(默认)
#   bash scripts/install-adapters.sh --install   # 安装/覆盖(自动备份旧文件)
#   bash scripts/install-adapters.sh --restore   # 用最近的备份还原
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADAPTERS_DIR="$SKILL_DIR/adapters"
DEST_ROOT="${OPENCLI_HOME:-$HOME/.opencli}/clis"

FILES=(
  "notebooklm/download-audio.js"
  "xiaoyuzhou/upload.js"
  "xiaoyuzhou/upload-status.js"
)

MODE="check"
case "${1:-}" in
  --install) MODE="install" ;;
  --check|"") MODE="check" ;;
  --restore) MODE="restore" ;;
  -h|--help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "unknown option: $1" >&2; exit 2 ;;
esac

status=0
for rel in "${FILES[@]}"; do
  src="$ADAPTERS_DIR/$rel"
  dst="$DEST_ROOT/$rel"
  if [ ! -f "$src" ]; then
    echo "❌ 缺少源文件: $src" >&2
    status=1
    continue
  fi
  case "$MODE" in
    check)
      if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
        echo "✅ 已安装且与 skill 自带版本一致: $rel"
      elif [ -f "$dst" ]; then
        echo "⚠️  已存在但不一致(可能是旧版或你本地改过的): $rel"
        status=1
      else
        echo "❌ 未安装: $rel"
        status=1
      fi
      ;;
    install)
      mkdir -p "$(dirname "$dst")"
      if [ -f "$dst" ] && ! cmp -s "$src" "$dst"; then
        backup="$dst.bak-$(date +%Y%m%d-%H%M%S)"
        cp "$dst" "$backup"
        echo "↩️  已备份旧文件: $backup"
      fi
      cp "$src" "$dst"
      echo "✅ 安装: $rel"
      ;;
    restore)
      backup=$(ls -1t "$dst".bak-* 2>/dev/null | head -1 || true)
      if [ -n "$backup" ]; then
        cp "$backup" "$dst"
        echo "↩️  已从备份还原: $backup"
      else
        echo "⚠️  没有备份可还原: $dst"
      fi
      ;;
  esac
done

if [ "$MODE" = "install" ]; then
  echo
  echo "自检:"
  echo "  opencli adapter status    # 应看到 notebooklm / xiaoyuzhou 的 override"
  echo "  opencli xiaoyuzhou --help | grep upload"
fi

if [ "$status" -ne 0 ] && [ "$MODE" = "check" ]; then
  echo
  echo "修复: bash $SKILL_DIR/scripts/install-adapters.sh --install" >&2
fi
exit "$status"
