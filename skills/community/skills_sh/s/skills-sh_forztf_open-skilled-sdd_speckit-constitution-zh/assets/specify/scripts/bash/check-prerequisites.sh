#!/usr/bin/env bash

# 前置条件统一校验脚本
#
# 本脚本为 Spec-Driven Development 工作流提供统一的前置条件校验。
# 用于替代此前分散在多个脚本中的校验功能。
#
# 用法: ./check-prerequisites.sh [选项]
#
# 选项:
#   --json              以 JSON 格式输出
#   --require-tasks     要求存在 tasks.md（实现阶段）
#   --include-tasks     在 AVAILABLE_DOCS 列表中包含 tasks.md
#   --paths-only        仅输出路径变量（不执行校验）
#   --help, -h          显示帮助信息
#
# 输出:
#   JSON 模式: {"FEATURE_DIR":"...", "AVAILABLE_DOCS":["..."]}
#   文本模式: FEATURE_DIR:... \n 可用文档: \n ✓/✗ file.md
#   仅路径: REPO_ROOT: ... \n BRANCH: ... \n FEATURE_DIR: ... 等

set -e

# 解析命令行参数
JSON_MODE=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false
PATHS_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --require-tasks)
            REQUIRE_TASKS=true
            ;;
        --include-tasks)
            INCLUDE_TASKS=true
            ;;
        --paths-only)
            PATHS_ONLY=true
            ;;
        --help|-h)
            cat << 'EOF'
用法: check-prerequisites.sh [选项]

用于 Spec-Driven Development 工作流的前置条件统一校验。

选项:
  --json              以 JSON 格式输出
  --require-tasks     要求存在 tasks.md（实现阶段）
  --include-tasks     在 AVAILABLE_DOCS 列表中包含 tasks.md
  --paths-only        仅输出路径变量（不执行校验）
  --help, -h          显示帮助信息

示例:
  # 校验任务阶段前置条件（要求存在 plan.md）
  ./check-prerequisites.sh --json
  
  # 校验实现阶段前置条件（要求存在 plan.md + tasks.md）
  ./check-prerequisites.sh --json --require-tasks --include-tasks
  
  # 仅获取特性路径（不执行校验）
  ./check-prerequisites.sh --paths-only
  
EOF
            exit 0
            ;;
        *)
            echo "错误: 未知选项 '$arg'。使用 --help 查看帮助信息。" >&2
            exit 1
            ;;
    esac
done

# 加载通用函数
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 获取特性路径并校验分支
eval $(get_feature_paths)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# 仅路径模式：输出路径并退出（支持同时使用 JSON + paths-only）
if $PATHS_ONLY; then
    if $JSON_MODE; then
        # 最小化的 JSON 路径负载（不执行校验）
        printf '{"REPO_ROOT":"%s","BRANCH":"%s","FEATURE_DIR":"%s","FEATURE_SPEC":"%s","IMPL_PLAN":"%s","TASKS":"%s"}\n' \
            "$REPO_ROOT" "$CURRENT_BRANCH" "$FEATURE_DIR" "$FEATURE_SPEC" "$IMPL_PLAN" "$TASKS"
    else
        echo "REPO_ROOT: $REPO_ROOT"
        echo "BRANCH: $CURRENT_BRANCH"
        echo "FEATURE_DIR: $FEATURE_DIR"
        echo "FEATURE_SPEC: $FEATURE_SPEC"
        echo "IMPL_PLAN: $IMPL_PLAN"
        echo "TASKS: $TASKS"
    fi
    exit 0
fi

# 校验必要的目录与文件
if [[ ! -d "$FEATURE_DIR" ]]; then
    echo "错误: 未找到特性目录: $FEATURE_DIR" >&2
    echo "请先运行 /speckit.specify 以创建特性目录结构。" >&2
    exit 1
fi

if [[ ! -f "$IMPL_PLAN" ]]; then
    echo "错误: 在 $FEATURE_DIR 中未找到 plan.md" >&2
    echo "请先运行 /speckit.plan 以生成实现计划。" >&2
    exit 1
fi

# Check for tasks.md if required
if $REQUIRE_TASKS && [[ ! -f "$TASKS" ]]; then
    echo "错误: 在 $FEATURE_DIR 中未找到 tasks.md" >&2
    echo "请先运行 /speckit.tasks 以创建任务列表。" >&2
    exit 1
fi

# 构建可用文档列表
docs=()

# 始终检查这些可选文档
[[ -f "$RESEARCH" ]] && docs+=("research.md")
[[ -f "$DATA_MODEL" ]] && docs+=("data-model.md")

# 检查 contracts 目录（仅在存在且包含文件时）
if [[ -d "$CONTRACTS_DIR" ]] && [[ -n "$(ls -A "$CONTRACTS_DIR" 2>/dev/null)" ]]; then
    docs+=("contracts/")
fi

[[ -f "$QUICKSTART" ]] && docs+=("quickstart.md")

# 若请求且存在，则包含 tasks.md
if $INCLUDE_TASKS && [[ -f "$TASKS" ]]; then
    docs+=("tasks.md")
fi

# 输出结果
if $JSON_MODE; then
    # 构建文档的 JSON 数组
    if [[ ${#docs[@]} -eq 0 ]]; then
        json_docs="[]"
    else
        json_docs=$(printf '"%s",' "${docs[@]}")
        json_docs="[${json_docs%,}]"
    fi
    
    printf '{"FEATURE_DIR":"%s","AVAILABLE_DOCS":%s}\n' "$FEATURE_DIR" "$json_docs"
else
    # 文本输出
    echo "特性目录:$FEATURE_DIR"
    echo "可用文档:"
    
    # Show status of each potential document
    check_file "$RESEARCH" "research.md"
    check_file "$DATA_MODEL" "data-model.md"
    check_dir "$CONTRACTS_DIR" "contracts/"
    check_file "$QUICKSTART" "quickstart.md"
    
    if $INCLUDE_TASKS; then
        check_file "$TASKS" "tasks.md"
    fi
fi
