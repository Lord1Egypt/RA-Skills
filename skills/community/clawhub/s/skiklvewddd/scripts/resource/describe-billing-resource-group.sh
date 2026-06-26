#!/usr/bin/env bash
# ============================================================================
# 查询资源组节点列表
# 接口: DescribeBillingResourceGroup
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --resource-group-id <id> [选项]

查询资源组节点列表

选项:
  --resource-group-id <id>  资源组 ID (必填)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --limit <n>               返回数量 (默认: 20)
  --offset <n>              偏移量 (默认: 0)
  --order <ASC|DESC>        排序方向
  --order-field <field>     排序字段: CreateTime | ExpireTime
  --filters <filters>       过滤条件 (格式: "Name=xxx,Values=yyy" 可多次指定)
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --resource-group-id rg-xxx
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local resource_group_id=""
    local limit=""
    local offset=""
    local order=""
    local order_field=""
    local -a filters=()
    local -a extra_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --resource-group-id) resource_group_id="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --offset) offset="$2"; shift 2 ;;
            --order) order="$2"; shift 2 ;;
            --order-field) order_field="$2"; shift 2 ;;
            --filters) filters+=("$2"); shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$resource_group_id" ]]; then
        log_error "缺少必填参数: --resource-group-id"
        usage
    fi

    [[ -n "$limit" ]] && extra_args+=(--Limit "$limit")
    [[ -n "$offset" ]] && extra_args+=(--Offset "$offset")
    [[ -n "$order" ]] && extra_args+=(--Order "$order")
    [[ -n "$order_field" ]] && extra_args+=(--OrderField "$order_field")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询资源组节点列表 (region=${region}, resource-group-id=${resource_group_id})"
    local result
    result=$(call_tione_api "DescribeBillingResourceGroup" "$region" --ResourceGroupId "$resource_group_id" "${extra_args[@]}")
    convert_resource_units "$result"
}

main "$@"
