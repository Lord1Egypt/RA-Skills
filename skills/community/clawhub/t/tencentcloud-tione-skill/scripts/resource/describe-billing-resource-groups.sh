#!/usr/bin/env bash
# ============================================================================
# 查询资源组列表
# 接口: DescribeBillingResourceGroups
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") [选项]

查询资源组列表

选项:
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --limit <n>               返回数量 (默认: 20)
  --offset <n>              偏移量 (默认: 0)
  --search-word <word>      模糊查找资源组 ID 或名称
  --filters <filters>       过滤条件 (格式: "Name=xxx,Values=yyy" 可多次指定)
                            模糊匹配: "Name=xxx,Values=yyy,Fuzzy=true"
  --tag-filters <json>      标签过滤条件 (JSON 数组)
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai
  $(basename "$0") --region ap-shanghai --search-word "gpu-group"
  # 过滤有可用节点的资源组（多值用分号分隔）
  $(basename "$0") --region ap-shanghai --filters "Name=AvailableNodeCount,Values=1;2;4"
  # 按名称模糊搜索
  $(basename "$0") --region ap-shanghai --filters "Name=ResourceGroupName,Values=test,Fuzzy=true"
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local limit=""
    local offset=""
    local search_word=""
    local tag_filters=""
    local -a filters=()
    local -a extra_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --offset) offset="$2"; shift 2 ;;
            --search-word) search_word="$2"; shift 2 ;;
            --tag-filters) tag_filters="$2"; shift 2 ;;
            --filters) filters+=("$2"); shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    [[ -n "$limit" ]] && extra_args+=(--Limit "$limit")
    [[ -n "$offset" ]] && extra_args+=(--Offset "$offset")
    [[ -n "$search_word" ]] && extra_args+=(--SearchWord "$search_word")
    [[ -n "$tag_filters" ]] && extra_args+=(--TagFilters "$tag_filters")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询资源组列表 (region=${region})"
    local result
    result=$(call_tione_api "DescribeBillingResourceGroups" "$region" "${extra_args[@]}")
    convert_resource_units "$result"
}

main "$@"
