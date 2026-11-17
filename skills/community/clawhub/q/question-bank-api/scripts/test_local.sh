#!/usr/bin/env bash
# 题库 API 本地联调脚本
# 用法（在你自己的终端里）：
#   方式一（推荐，不依赖环境变量）：
#     bash scripts/test_local.sh --base "https://你的真实网关地址" --key "你的key"
#   方式二（先设环境变量，注意 PowerShell 设的 $env 不会跨窗口继承给 bash）：
#     export QB_API_BASE="https://你的真实网关地址"   # 不含末尾 /
#     export QB_API_KEY="你的key"
#     bash scripts/test_local.sh
#   可选：--py 指定 python 解释器，例如 --py "C:/path/python.exe"
#
# 说明：
#   - 标注 [需替换] 的命令，请先用前面接口返回的真实 id 替换 REPLACE 再跑；
#     脚本遇到 REPLACE 会自动跳过，不会真的打错请求。
#   - 想看原始 JSON，可在任意命令后加 --json。
#   - 其他科目按章节取题默认只扫 3 个叶子、限 10 题，防止一次消耗过多额度。
set -u

# 支持直接传参：bash test_local.sh --base <网关> --key <key> [--py <python>]
# 没传则回退到环境变量 QB_API_BASE / QB_API_KEY（避免 PowerShell→bash 环境变量继承丢失）
BASE=""; KEY=""; PY="${PYTHON:-python3}"
while [ $# -gt 0 ]; do
  case "$1" in
    --base) BASE="$2"; shift 2;;
    --key)  KEY="$2";  shift 2;;
    --py)   PY="$2";   shift 2;;
    *) echo "[忽略未知参数] $1"; shift;;
  esac
done
BASE="${BASE:-${QB_API_BASE:-}}"
KEY="${KEY:-${QB_API_KEY:-}}"
if [ -z "$BASE" ] || [ -z "$KEY" ]; then
  echo "[错误] 请提供 --base 和 --key 参数，或先设置 QB_API_BASE / QB_API_KEY 环境变量" >&2
  exit 1
fi

# 你的机器上若 python3 不可用，改成完整路径，例如：
# PY="C:/Users/10909/.workbuddy/binaries/python/versions/3.13.12/python.exe"

run() {
  echo
  echo "=================================================="
  echo "### $*"
  echo "=================================================="
  "$PY" "$(dirname "$0")/qb.py" "$@" --base "$BASE" --key "$KEY"
}

skip_if_replace() {
  # 用法：skip_if_replace <值> <说明>  — 值为 REPLACE 时打印跳过并返回 0(跳过)
  if [ "${1:-}" = "REPLACE" ]; then
    echo "[跳过] $2 （先把前面接口返回的真实 id 填进来再跑）"
    return 0
  fi
  return 1
}

echo ">>> 基础连通性：catalog（学段/年级/学科/版本树）"
run catalog

echo ">>> 字典：dict（题型/试卷类型/难易度）"
run dict

echo ">>> 知识点树（取第三级 oldId 作为 knowledgeId）"
run knowledge-tree --pharseId 1 --subjectId 2

if skip_if_replace "REPLACE" "按知识点取题 by-knowledge"; then :; else
  run by-knowledge --knowledgeId REPLACE --page 1
fi

echo ">>> 章节树（其他科目按章节取题用）"
run chapter-tree --pharseId 2 --subjectId 2 --editionId 74 --gradeId 201

echo ">>> 列出章节叶子 32 位 oldId"
run chapter-leaves --pharseId 2 --subjectId 2 --editionId 74 --gradeId 201

if skip_if_replace "REPLACE" "其他科目按章节取题 by-chapter-knowledge"; then :; else
  run by-chapter-knowledge --pharseId 2 --subjectId 2 --editionId 74 --gradeId 201 \
      --knowledgeId REPLACE --max-leaves 3 --limit 10
fi

if skip_if_replace "REPLACE" "语文/英语按章节取题 by-chapter"; then :; else
  run by-chapter --chapterId REPLACE --page 1
fi

echo ">>> 试卷列表"
run papers --gradeId 200 --subjectId 2

echo ">>> 试卷搜索"
run paper-search --keyword "七年级 数学"

if skip_if_replace "REPLACE" "试卷详情 paper"; then :; else
  run paper --paperId REPLACE
fi

echo ">>> 试题搜索"
run search --keyword 浮力 --gradeId 200

if skip_if_replace "REPLACE" "按 md52 取答案 answer"; then :; else
  run answer --md52 REPLACE
fi

if skip_if_replace "REPLACE" "提交试题报错 report"; then :; else
  run report --qid REPLACE --content "联调测试报错"
fi

echo
echo ">>> 全部接口已轮询完毕。to-word 需要 paperData JSON，单独手测："
echo "    python scripts/qb.py to-word --data '<paperData JSON>' --out paper.docx \\"
echo "        --base \"$BASE\" --key \"\$QB_API_KEY\""
