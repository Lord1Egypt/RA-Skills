#!/usr/bin/env bash
# runtime_env.sh —— 统一运行时解析（供各技能 .sh 入口 source，不直接执行）
#
# 解决三件事：
#   1) 解释器：显式指定 > Codex 运行时 > PATH 上的 python3.12/3.11 > python3，且必须 >= 3.10
#   2) 底座：CAD_SKILL_DIR 显式指定 > 同级目录 > WorkBuddy/Claude/Codex 各 skills 目录
#   3) 依赖：把「本技能 scripts + 底座 scripts + 底座 vendor」拼进 PYTHONPATH，
#      让 ezdxf / ezdwg / openpyxl / typing_extensions 等无需全局 pip 安装即可导入
#
# 产出变量：SKILL_DIR、PYTHON_BIN、CAD_SKILL_DIR、PYTHONPATH
# 覆盖方式：CAD_SKILL_PYTHON=<python>、CAD_SKILL_DIR=<cad-file-reader 目录>
set -uo pipefail

_RT_SRC="${BASH_SOURCE[0]:-$0}"
_RT_SCRIPTS="$(cd "$(dirname "${_RT_SRC}")" && pwd)"
SKILL_DIR="$(cd "$_RT_SCRIPTS/.." && pwd)"
# SkillHub 分发包（zip）会丢失可执行位：首次运行时幂等自愈，避免 permission denied
find "$SKILL_DIR/scripts" -maxdepth 1 -type f \( -name '*.sh' -o -name '*.py' \) ! -perm -u+x -exec chmod +x {} + 2>/dev/null || true
export SKILL_DIR

# ---- 1) 解释器 ----
PYTHON_BIN=""
for _c in "${CAD_SKILL_PYTHON:-}" "${CODEX_PYTHON:-}" \
          "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" \
          "$HOME"/.cache/codex-runtimes/*/dependencies/python/bin/python3 \
          "$(command -v python3.12 || true)" \
          "$(command -v python3.11 || true)" \
          "$(command -v python3 || true)"; do
  if [ -n "${_c}" ] && [ -x "${_c}" ] && \
     "${_c}" -c 'import sys; assert sys.version_info >= (3, 10)' >/dev/null 2>&1; then
    PYTHON_BIN="${_c}"
    break
  fi
done
if [ -z "${PYTHON_BIN}" ]; then
  echo "❌ 未找到 Python 3.10+。" >&2
  echo "   请安装 Python 3.10 及以上，或用 CAD_SKILL_PYTHON=/path/to/python3 指定。" >&2
  return 2 2>/dev/null || exit 2
fi
export PYTHON_BIN

# ---- 2) 识图底座 ----
if [ -z "${CAD_SKILL_DIR:-}" ]; then
  for _d in "$SKILL_DIR/../cad-file-reader" \
            "$HOME"/.workbuddy/skills/*/cad-file-reader \
            "$HOME"/.claude/skills/cad-file-reader \
            "$HOME"/.codex/skills/cad-file-reader; do
    if [ -d "${_d}/scripts" ]; then
      CAD_SKILL_DIR="$(cd "${_d}" 2>/dev/null && pwd)"
      [ -d "${_d}/vendor" ] && break
    fi
  done
fi
export CAD_SKILL_DIR="${CAD_SKILL_DIR:-}"

# ---- 3) 依赖搜索路径 ----
if [ -n "${CAD_SKILL_DIR}" ] && [ -d "${CAD_SKILL_DIR}/vendor" ]; then
  export PYTHONPATH="${SKILL_DIR}/scripts:${CAD_SKILL_DIR}/scripts:${CAD_SKILL_DIR}/vendor${PYTHONPATH:+:${PYTHONPATH}}"
elif [ -n "${CAD_SKILL_DIR}" ]; then
  export PYTHONPATH="${SKILL_DIR}/scripts:${CAD_SKILL_DIR}/scripts${PYTHONPATH:+:${PYTHONPATH}}"
else
  export PYTHONPATH="${SKILL_DIR}/scripts${PYTHONPATH:+:${PYTHONPATH}}"
fi

export PYTHONIOENCODING="${PYTHONIOENCODING:-utf-8}"
