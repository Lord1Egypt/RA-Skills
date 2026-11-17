#!/usr/bin/env bash
# text-utils: 文本处理小工具（纯本地，无网络依赖）
# 用法:
#   text-utils count "你好 world 123"     # 字数/字符/单词统计
#   text-utils upper "hello"              # 转大写
#   text-utils lower "HELLO"              # 转小写
#   text-utils reverse "abc"              # 反转
#   text-utils unique a b b c c           # 去重
#   text-utils lines < file.txt           # 统计行数
#   text-utils trim "  hi  "              # 去首尾空格
set -euo pipefail

case "${1:-}" in
  count)
    [ $# -lt 2 ] && { echo "用法: text-utils count <文本>" >&2; exit 1; }
    shift
    TEXT="$*"
    echo "$TEXT" | python3 -c '
import sys
t = sys.stdin.read().rstrip("\n")
h_start = "\u4e00"
h_end = "\u9fff"
han_count = sum(1 for c in t if h_start <= c <= h_end)
no_space = len(t.replace(" ", ""))
words = len(t.split())
lines = t.count("\n") + 1 if t else 0
print(f"📝 字符数（含空格）: {len(t)}")
print(f"📝 字符数（不含空格）: {no_space}")
print(f"📝 汉字数: {han_count}")
print(f"📝 英文单词数: {words}")
print(f"📝 行数: {lines}")
'
    ;;
  upper) shift; [ $# -eq 0 ] && { echo "用法: text-utils upper <文本>" >&2; exit 1; }; echo "$*" | tr '[:lower:]' '[:upper:]' ;;
  lower) shift; [ $# -eq 0 ] && { echo "用法: text-utils lower <文本>" >&2; exit 1; }; echo "$*" | tr '[:upper:]' '[:lower:]' ;;
  reverse) shift; [ $# -eq 0 ] && { echo "用法: text-utils reverse <文本>" >&2; exit 1; }; echo "$*" | rev ;;
  unique)
    shift
    [ $# -eq 0 ] && { echo "用法: text-utils unique <词>..." >&2; exit 1; }
    echo "$@" | tr ' ' '\n' | awk '!seen[$0]++' | tr '\n' ' '
    echo ;;
  lines)
    if [ -t 0 ]; then
      [ $# -lt 2 ] && { echo "用法: text-utils lines < 文件 或 直接传文本>" >&2; exit 1; }
      shift; echo "$*" | wc -l
    else
      wc -l
    fi ;;
  trim)
    shift
    [ $# -eq 0 ] && { echo "用法: text-utils trim <文本>" >&2; exit 1; }
    echo "$*" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' ;;
  --help|-h|"")
    sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
    ;;
  *)
    echo "未知命令: $1（试试 count / upper / lower / reverse / unique / lines / trim）" >&2
    exit 1
    ;;
esac
