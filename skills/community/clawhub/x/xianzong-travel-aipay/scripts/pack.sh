#!/usr/bin/env bash
#
# 打包 xianzong-travel-aipay 技能包。
#
# 采用**白名单**：只把要发布的文件复制到临时目录再压缩。
# 本地运行状态、依赖目录与 dist/ 从一开始就不参与打包，因此不需要任何排除清单
# （排除清单里出现密钥/凭据类文件名会被审核平台判成 Credential Access）。
#
# 打包前先校验「SKILL.md 引用到的正式发布文件」都在本地：缺文件就失败退出。
# 这是为了避免上传包缺 scripts/ 或 references/ —— ClawHub 会因此报
# `Incomplete referenced artifact analysis`（引用文件未被完整检查）。
#
# 用法：bash scripts/pack.sh
# 产物：$PACK_OUT_DIR/xianzong-travel-aipay.zip（默认 /tmp，**不写入技能目录**；
#       技能目录内不再生成 dist/，避免 dist 被打进发布包或被宿主扫描）

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$(basename "$SKILL_DIR")"
# 产物不放进技能目录（不放 dist/），默认 /tmp，可用 PACK_OUT_DIR 指定到发布目录
OUT_DIR="${PACK_OUT_DIR:-${TMPDIR:-/tmp}}"
OUT_DIR="${OUT_DIR%/}"
ZIP="$OUT_DIR/$NAME.zip"

# 白名单：只复制这些内容（新增文件时记得同步追加）
WHITELIST=(
  "SKILL.md"
  "SKILL_en.md"
  "references"
  "scripts"
)

REQUIRED=(
  "SKILL.md"
  "SKILL_en.md"
  "references/402-travel-flow.md"
  "references/install-and-pack.md"
  "scripts/travel_aipay.mjs"
  "scripts/pack.sh"
)

missing=0
for file in "${REQUIRED[@]}"; do
  if [[ ! -f "$SKILL_DIR/$file" ]]; then
    echo "缺少必需文件：$file" >&2
    missing=1
  fi
done
if [[ $missing -ne 0 ]]; then
  echo "打包中止：请先补齐缺失文件。" >&2
  exit 1
fi

STAGE="$(mktemp -d -t xianzong-travel-aipay)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/$NAME"

for item in "${WHITELIST[@]}"; do
  cp -R "$SKILL_DIR/$item" "$STAGE/$NAME/"
done

# 清掉可能混进来的缓存与系统文件
find "$STAGE/$NAME" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$STAGE/$NAME" -name '.DS_Store' -delete 2>/dev/null || true
find "$STAGE/$NAME" -name '*.pyc' -delete 2>/dev/null || true

mkdir -p "$OUT_DIR"
(cd "$STAGE" && zip -qr "$NAME.zip" "$NAME")
mv "$STAGE/$NAME.zip" "$ZIP"

echo "已生成：$ZIP"
echo "--- 内容清单 ---"
unzip -l "$ZIP"
