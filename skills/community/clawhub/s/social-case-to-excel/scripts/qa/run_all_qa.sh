#!/usr/bin/env bash
# run_all_qa.sh —— 一条命令跑完一轮 QA（十条闸门 + 探针 + 两道人工闸门 + 脱敏），并把
# 全部输出落到一个日志文件里。
#
# 为什么需要它：
#   ① gate_01 / gate_02 / qa_11 内部**没有**上一轮的路径字面量，00_prep_qa.py 的
#      「确定性替换」不会（也不该）动它们——必须显式传参才会跑对；忘了传参时它们要么
#      用默认值静默跳过，要么直接退出，很容易被当成"这关过了"。
#   ② 四十多条案例的 QA 输出远超一次终端回显的量（在 Clacky 的 PTY 里大约 3800 字符就
#      开始截断、溢出到临时文件），逐条敲命令 + 逐段翻屏既慢又容易漏看某一段的结论。
#
# 用法（先跑过 00_prep_qa.py 生成本轮适配副本）：
#   bash scripts/qa/run_all_qa.sh --tag bf --outdir /tmp/bf \
#     --cases /tmp/bf/bf_cases_final.json \
#     --xlsx '/Users/you/clacky_workspace/xxx拆解库.xlsx' \
#     --md   '/Users/you/clacky_workspace/xxx案例研究_40条.md'
#
#   --cases 是**构建产出的中间 json**，两道人工闸门读的就是它。改了 rows/tcb 之后如果不
#   重建 xlsx，闸门读到的是旧数据 —— 看起来像"改了没用"。所以本脚本会先用 mtime 提醒。
#
# 输出：<outdir>/<tag>_qa_out.txt（全量日志），终端只打印每个脚本的结论行。

set -u

TAG=""; OUTDIR="/tmp"; CASES=""; XLSX=""; MD=""; SKIP_PROBE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --tag) TAG="$2"; shift 2 ;;
    --outdir) OUTDIR="$2"; shift 2 ;;
    --cases) CASES="$2"; shift 2 ;;
    --xlsx) XLSX="$2"; shift 2 ;;
    --md) MD="$2"; shift 2 ;;
    --skip-probe) SKIP_PROBE=1; shift ;;
    -h|--help) sed -n '2,26p' "$0"; exit 0 ;;
    *) echo "未知参数：$1" >&2; exit 2 ;;
  esac
done

if [ -z "$TAG" ]; then
  echo "用法：bash run_all_qa.sh --tag <本轮前缀> --outdir <工作目录> [--cases <中间json>] [--xlsx <xlsx>] [--md <md>]" >&2
  echo "提示：--tag/--outdir 要和 00_prep_qa.py 那一次一致（适配副本名为 <tag>_qa_0*.py）。" >&2
  exit 2
fi

OUTDIR="${OUTDIR%/}"
LOG="$OUTDIR/${TAG}_qa_out.txt"
[ -n "$CASES" ] || CASES="$OUTDIR/${TAG}_cases_final.json"

: > "$LOG"
run() {  # run <标题> <命令...>
  local title="$1"; shift
  { echo "## $title"; "$@" 2>&1; echo; } >> "$LOG"
}

# ---- 0. 重建提醒：闸门读的是构建产出的中间 json，rows/tcb 更新后必须重建 ----
if [ -f "$CASES" ]; then
  newer=$(ls -1 "$OUTDIR"/${TAG}_rows*.py "$OUTDIR"/${TAG}_tcb*.py /tmp/${TAG}_rows*.py /tmp/${TAG}_tcb*.py 2>/dev/null | head -1)
  if [ -n "$newer" ] && [ "$newer" -nt "$CASES" ]; then
    echo "!! 写作文件比 $CASES 更新 —— 先重跑构建脚本再跑 QA，否则闸门看的是旧数据" | tee -a "$LOG"
  fi
else
  echo "!! 找不到闸门入参 $CASES —— 两道人工闸门会跳过（构建脚本应产出这个文件，或用 --cases 指定）" | tee -a "$LOG"
fi
for p in "$XLSX" "$MD"; do
  [ -n "$p" ] && [ ! -f "$p" ] && echo "!! 交付物不存在：$p" | tee -a "$LOG"
done

# ---- 1. 十条闸门（路径已由 00_prep_qa.py 适配）----
for f in "$OUTDIR"/${TAG}_qa_0*.py; do
  [ -f "$f" ] && run "$f" python3 "$f"
done

# ---- 2. 探针（候选池/原始记录体检，可选）----
if [ "$SKIP_PROBE" = 0 ]; then
  for f in "$OUTDIR"/${TAG}_probe_0*.py; do
    [ -f "$f" ] && run "$f" python3 "$f"
  done
fi

# ---- 3. 两道人工闸门（必须显式传参）----
for g in gate_01_no_english_leftover gate_02_second_person; do
  f="$OUTDIR/${TAG}_${g}.py"
  if [ -f "$f" ] && [ -f "$CASES" ]; then
    run "$f" python3 "$f" "$CASES"
  fi
done

# ---- 4. 脱敏（交付物，必须显式传参；xlsx 要解压扫，grep 查不到里面的字）----
leak_args=()
[ -n "$XLSX" ] && [ -f "$XLSX" ] && leak_args+=("$XLSX")
[ -n "$MD" ] && [ -f "$MD" ] && leak_args+=("$MD")
if [ ${#leak_args[@]} -gt 0 ]; then
  f="$OUTDIR/${TAG}_qa_11_no_vendor_leak.py"
  [ -f "$f" ] && run "$f" python3 "$f" "${leak_args[@]}"
fi

# ---- 5. 结论摘要（只看这几行就够）----
# 注意：变量后面紧跟中文/全角字符时必须写成 ${VAR}，否则 set -u 下 bash 会把多字节字符
# 吃进变量名，报 `LOG?: unbound variable` 这种与真实原因无关的错。
echo "== 结论摘要（全量日志：${LOG}）=="
grep -nE '结论|缺失总数|空单元格\(非图片列\)|图片数|可疑数字|需要行高|中文帖计数|LOW|!! |通过|Traceback' "$LOG" | head -40
echo
echo "全量日志：$LOG"
