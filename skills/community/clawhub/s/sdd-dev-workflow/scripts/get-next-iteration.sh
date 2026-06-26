#!/bin/bash
# 获取下一个迭代序号
# 用法: get-next-iteration.sh [项目目录]

set -e

PROJECT_DIR="${1:-.}"
SPECS_DIR="$PROJECT_DIR/specs"

# 检查 specs 目录是否存在
if [ ! -d "$SPECS_DIR" ]; then
  echo "001"
  exit 0
fi

# 检测现有迭代
existing_specs=$(ls -d "$SPECS_DIR"/[0-9][0-9][0-9]-* 2>/dev/null | xargs -n1 basename | cut -d- -f1 | sort -n | tail -1)

# 计算下一个序号
if [ -z "$existing_specs" ]; then
  next_num="001"
else
  next_num=$(printf "%03d" $((10#$existing_specs + 1)))
fi

echo "$next_num"
