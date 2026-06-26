#!/bin/bash
#
# Skill Review Script
# 用于审查 Agent Skills 的规范性、完整性和代码质量
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
VERBOSE=false
JSON_OUTPUT=false
SKILL_PATH=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印帮助信息
print_help() {
    cat << EOF
Usage: review.sh [OPTIONS] <skill-path>

审查 Agent Skills 的规范性、完整性和代码质量

Arguments:
  skill-path    要审查的 skill 目录路径

Options:
  -v, --verbose    详细输出（包含代码分析）
  -j, --json       输出 JSON 格式报告
  -h, --help       显示此帮助信息

Examples:
  review.sh /path/to/my-skill
  review.sh /path/to/my-skill --verbose
  review.sh /path/to/my-skill --json
EOF
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -j|--json)
                JSON_OUTPUT=true
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            -*)
                echo -e "${RED}错误: 未知选项 $1${NC}"
                print_help
                exit 1
                ;;
            *)
                if [ -z "$SKILL_PATH" ]; then
                    SKILL_PATH="$1"
                fi
                shift
                ;;
        esac
    done

    if [ -z "$SKILL_PATH" ]; then
        echo -e "${RED}错误: 请提供 skill 路径${NC}"
        print_help
        exit 1
    fi

    # 转换为绝对路径
    SKILL_PATH="$(cd "$(dirname "$SKILL_PATH")" && pwd)/$(basename "$SKILL_PATH")"
}

# 检查依赖
check_dependencies() {
    local deps=("python3" "yamllint" "jq")
    local missing=()

    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing+=("$dep")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${YELLOW}警告: 缺少以下依赖: ${missing[*]}${NC}"
        echo "某些检查可能无法执行"
    fi
}

# 主函数
main() {
    parse_args "$@"
    check_dependencies

    if [ ! -d "$SKILL_PATH" ]; then
        echo -e "${RED}错误: 目录不存在: $SKILL_PATH${NC}"
        exit 1
    fi

    echo -e "${BLUE}开始审查 skill: $(basename "$SKILL_PATH")${NC}"
    echo "路径: $SKILL_PATH"
    echo ""

    # 调用 Python 审查脚本
    local python_args=""
    if [ "$VERBOSE" = true ]; then
        python_args="$python_args --verbose"
    fi
    if [ "$JSON_OUTPUT" = true ]; then
        python_args="$python_args --json"
    fi

    python3 "$SCRIPT_DIR/review_skill.py" "$SKILL_PATH" $python_args

    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ 审查完成${NC}"
    else
        echo ""
        echo -e "${YELLOW}⚠️  审查发现一些问题${NC}"
    fi

    exit $exit_code
}

main "$@"
