#!/usr/bin/env bash

set -e

# 解析命令行参数
JSON_MODE=false
ARGS=()

for arg in "$@"; do
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --help|-h) 
            echo "用法: $0 [--json]"
            echo "  --json    以 JSON 格式输出结果"
            echo "  --help    显示此帮助信息"
            exit 0 
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
done

# 获取脚本目录并加载通用函数
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 从通用函数获取所有路径与变量
eval $(get_feature_paths)

# 检查当前是否在正确的特性分支（仅在 Git 仓库中校验）
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# 确保特性目录存在
mkdir -p "$FEATURE_DIR"

# 若存在计划模板则复制
TEMPLATE="$REPO_ROOT/.specify/templates/plan-template.md"
if [[ -f "$TEMPLATE" ]]; then
    cp "$TEMPLATE" "$IMPL_PLAN"
    echo "已复制计划模板到 $IMPL_PLAN"
else
    echo "警告: 未在 $TEMPLATE 找到计划模板"
    # 若模板不存在则创建一个基础计划文件
    touch "$IMPL_PLAN"
fi

# 输出结果
if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","HAS_GIT":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH" "$HAS_GIT"
else
    echo "规格文件: $FEATURE_SPEC"
    echo "实现计划: $IMPL_PLAN" 
    echo "规格目录: $FEATURE_DIR"
    echo "当前分支: $CURRENT_BRANCH"
    echo "是否有 Git: $HAS_GIT"
fi
