#!/usr/bin/env bash
# ============================================================================
# 查询 Notebook 列表
# 接口: DescribeNotebooks
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") [选项]

查询 Notebook 列表

选项:
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --limit <n>               返回数量 (默认: 10)
  --offset <n>              偏移量 (默认: 0)
  --order <asc|desc>        排序方向 (默认: DESC)
  --order-field <field>     排序字段: CreateTime | UpdateTime (默认: UpdateTime)
  --tag-filters <json>      标签过滤条件 (JSON 数组)
  --filters <filters>       过滤条件 (格式: "Name=xxx,Values=yyy" 可多次指定)
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai
  # 按状态过滤（多值用分号分隔）
  $(basename "$0") --region ap-shanghai --filters "Name=Status,Values=Running;Starting;Stopping"

支持的 Status 值:
  Starting | Submitting | Running | Stopping | Stopped | Failed | SubmitFailed
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local limit=""
    local offset=""
    local order=""
    local order_field=""
    local -a filters=()
    local tag_filters=""
    local -a extra_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --offset) offset="$2"; shift 2 ;;
            --order) order="$2"; shift 2 ;;
            --order-field) order_field="$2"; shift 2 ;;
            --tag-filters) tag_filters="$2"; shift 2 ;;
            --filters) filters+=("$2"); shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    [[ -n "$limit" ]] && extra_args+=(--Limit "$limit")
    [[ -n "$offset" ]] && extra_args+=(--Offset "$offset")
    [[ -n "$order" ]] && extra_args+=(--Order "$order")
    [[ -n "$order_field" ]] && extra_args+=(--OrderField "$order_field")
    [[ -n "$tag_filters" ]] && extra_args+=(--TagFilters "$tag_filters")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询 Notebook 列表 (region=${region})"
    local result
    result=$(call_tione_api "DescribeNotebooks" "$region" "${extra_args[@]}")
    format_json "$result"
}

main "$@"
