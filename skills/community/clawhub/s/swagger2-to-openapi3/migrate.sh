#!/bin/bash
#
# Swagger 2 到 OpenAPI 3.0 迁移工具 - 便捷启动脚本
#

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 显示帮助信息
show_help() {
    cat << EOF
Swagger 2 到 OpenAPI 3.0 迁移工具

使用方法:
    $0 [命令] [选项]

命令:
    migrate         执行完整迁移（注解 + import）
    annotations     仅迁移注解
    imports         仅迁移 import 语句
    help            显示此帮助信息

选项:
    --project-path  指定项目路径（必需）
    --dry-run       预览模式，不实际修改文件
    --help          显示帮助信息

示例:
    # 预览完整迁移
    $0 migrate --project-path /path/to/project --dry-run
    
    # 执行实际迁移
    $0 migrate --project-path /path/to/project
    
    # 仅迁移注解
    $0 annotations --project-path /path/to/project --dry-run

EOF
}

# 检查 Python 是否可用
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo "错误: 未找到 Python。请确保 Python 3 已安装。"
        exit 1
    fi
    
    # 确定 Python 命令
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
}

# 执行迁移
run_migration() {
    local script_name="$1"
    local project_path="$2"
    local dry_run="$3"
    
    local script_path="${SCRIPT_DIR}/scripts/${script_name}.py"
    
    if [[ ! -f "$script_path" ]]; then
        echo "错误: 找不到脚本文件: $script_path"
        exit 1
    fi
    
    # 构建命令参数
    local args=("--project-path" "$project_path")
    if [[ "$dry_run" == "true" ]]; then
        args+=("--dry-run")
    fi
    
    # 执行脚本
    echo "执行命令: $PYTHON_CMD \"$script_path\" ${args[*]}"
    echo ""
    "$PYTHON_CMD" "$script_path" "${args[@]}"
}

# 解析命令行参数
parse_args() {
    COMMAND=""
    PROJECT_PATH=""
    DRY_RUN="false"
    
    # 检查第一个参数是否是命令
    if [[ $# -gt 0 ]]; then
        case "$1" in
            migrate|annotations|imports|help)
                COMMAND="$1"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                # 不是命令，可能是旧式调用方式
                ;;
        esac
    fi
    
    # 解析剩余参数
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --project-path)
                PROJECT_PATH="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            migrate|annotations|imports|help)
                COMMAND="$1"
                shift
                ;;
            *)
                echo "未知参数: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done
    
    # 如果没有指定命令，默认使用 migrate
    if [[ -z "$COMMAND" ]]; then
        COMMAND="migrate"
    fi
    
    # 验证必需参数
    if [[ "$COMMAND" != "help" && -z "$PROJECT_PATH" ]]; then
        echo "错误: 缺少必需参数 --project-path"
        echo ""
        show_help
        exit 1
    fi
}

# 主函数
main() {
    # 解析参数
    parse_args "$@"
    
    # 处理 help 命令
    if [[ "$COMMAND" == "help" ]]; then
        show_help
        exit 0
    fi
    
    # 检查 Python
    check_python
    
    # 验证项目路径
    if [[ ! -d "$PROJECT_PATH" ]]; then
        echo "错误: 项目路径不存在或不是目录: $PROJECT_PATH"
        exit 1
    fi
    
    # 根据命令执行相应的迁移
    case "$COMMAND" in
        migrate)
            echo "执行完整迁移（注解 + import）..."
            run_migration "migrate_swagger_to_openapi" "$PROJECT_PATH" "$DRY_RUN"
            ;;
        annotations)
            echo "执行仅迁移注解..."
            run_migration "migrate_annotations" "$PROJECT_PATH" "$DRY_RUN"
            ;;
        imports)
            echo "执行仅迁移 import 语句..."
            run_migration "migrate_imports" "$PROJECT_PATH" "$DRY_RUN"
            ;;
        *)
            echo "错误: 未知命令: $COMMAND"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
