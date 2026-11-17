#!/usr/bin/env bash
# 土建算量内部脚本入口：优先本技能脚本，底座仅提供识图模块与 vendor。
set -euo pipefail
_HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# SkillHub 分发包（zip）会丢失可执行位：首次运行时幂等自愈，避免 permission denied
find "$_HERE/../scripts" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x -exec chmod +x {} + 2>/dev/null || true
source "$_HERE/runtime_env.sh"
BASE_VAL="$(bash "$SKILL_DIR/scripts/ensure_base.sh")" || exit $?
if [ -z "$BASE_VAL" ]; then
  echo "[土建算量] 降级模式：未能获取识图底座 cad-file-reader；请提供已有扫描/测量 JSON 或设置 CAD_SKILL_DIR。" >&2
  exit 2
fi
CAD_SKILL_DIR="$BASE_VAL"
export CAD_SKILL_DIR
: "${CAD_MEM_LIMIT_MB:=4096}"; export CAD_MEM_LIMIT_MB
export PYTHONPATH="${SKILL_DIR}/scripts:${CAD_SKILL_DIR}/scripts:${CAD_SKILL_DIR}/vendor${PYTHONPATH:+:${PYTHONPATH}}"
if [ "$#" -lt 1 ]; then
  echo "用法: run_cad.sh <脚本名> [参数...]" >&2
  echo "示例: run_cad.sh cad_quantity --help" >&2
  exit 1
fi
SCRIPT_NAME="$1"; shift
# 脚本查找顺序：本技能 scripts/ → 识图底座 scripts/（底座脚本也允许用同名入口调用）
TARGET="${SKILL_DIR}/scripts/${SCRIPT_NAME}.py"
if [ ! -f "$TARGET" ] && [ -n "${CAD_SKILL_DIR:-}" ] && [ -f "${CAD_SKILL_DIR}/scripts/${SCRIPT_NAME}.py" ]; then
  TARGET="${CAD_SKILL_DIR}/scripts/${SCRIPT_NAME}.py"
fi
if [ ! -f "$TARGET" ]; then
  echo "[土建算量] 找不到脚本 ${SCRIPT_NAME}：本技能与识图底座的 scripts/ 下均无此文件。" >&2
  exit 2
fi
exec "${PYTHON_BIN}" "$TARGET" "$@"
