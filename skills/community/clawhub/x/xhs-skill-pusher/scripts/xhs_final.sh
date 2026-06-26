#!/bin/bash
# xhs-kit最终发布脚本 - 统一设计，简单易用
# 核心设计：只使用文件路径，不使用账号名映射

set -e

cd "$(dirname "$0")"

# 激活虚拟环境
if [[ -f "xhs-env/bin/activate" ]]; then
    source xhs-env/bin/activate
    echo "✅ 虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在：xhs-env"
    echo "请先创建：python3 -m venv xhs-env && source xhs-env/bin/activate && pip install xhs-kit"
    exit 1
fi

# 执行简单脚本
exec ./xhs_simple.sh "$@"