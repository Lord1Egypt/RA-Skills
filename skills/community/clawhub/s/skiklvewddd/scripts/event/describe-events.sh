#!/usr/bin/env bash
# ============================================================================
# 查询事件
# 接口: DescribeEvents
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --service <type> [选项]

查询事件

选项:
  --service <type>          服务类型 (必填): TRAIN | NOTEBOOK | INFER | BATCH
  --service-id <id>         实例级 ID:
                            - TRAIN: LatestInstanceId (从 DescribeTrainingTask 获取)
                            - NOTEBOOK: PodName (从 DescribeNotebook 获取)
                            - INFER: 服务实例 ID (从 DescribeModelServiceGroup 获取)
  --start-time <time>       开始时间 (RFC3339 格式)
                            建议从详情接口获取 StartTime; 不指定则不传
  --end-time <time>         结束时间 (RFC3339 格式)
                            不指定则默认为当前时间 (UTC)
  --limit <n>               返回条数 (默认: 100)
  --offset <n>              偏移量 (默认: 0)
  --order <ASC|DESC>        排序方向 (默认: DESC)
  --order-field <field>     排序字段: FirstTimestamp | LastTimestamp (默认: LastTimestamp)
  --filters <filters>       过滤条件 (格式: "Name=xxx,Values=yyy" 可多次指定)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  # 训练任务事件 (先从 DescribeTrainingTask 获取 LatestInstanceId)
  $(basename "$0") --region ap-shanghai --service TRAIN --service-id train-xxx-yyy \\
    --start-time "2026-03-16T20:00:00Z"
  # 在线推理事件 (先从 DescribeModelServiceGroup 获取 ServiceId)
  $(basename "$0") --region ap-shanghai --service INFER --service-id ms-xxx-1
  # 按事件级别过滤
  $(basename "$0") --region ap-shanghai --service INFER --service-id ms-xxx-1 --filters "Name=Type,Values=Warning"
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local service=""
    local service_id=""
    local start_time=""
    local end_time=""
    local limit=""
    local offset=""
    local order=""
    local order_field=""
    local -a filters=()
    local -a extra_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --service) service="$2"; shift 2 ;;
            --service-id) service_id="$2"; shift 2 ;;
            --start-time) start_time="$2"; shift 2 ;;
            --end-time) end_time="$2"; shift 2 ;;
            --limit) limit="$2"; shift 2 ;;
            --offset) offset="$2"; shift 2 ;;
            --order) order="$2"; shift 2 ;;
            --order-field) order_field="$2"; shift 2 ;;
            --filters) filters+=("$2"); shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$service" ]]; then
        log_error "缺少必填参数: --service (TRAIN | NOTEBOOK | INFER | BATCH)"
        usage
    fi

    # 默认时间范围: 仅在缺少 end-time 时补充为当前时间
    # start-time 应由调用方从详情接口获取，不在此处默认
    if [[ -z "$end_time" ]]; then
        end_time=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
        log_info "未指定 --end-time, 默认使用当前时间: ${end_time}"
    fi

    extra_args+=(--Service "$service")
    [[ -n "$service_id" ]] && extra_args+=(--ServiceId "$service_id")
    [[ -n "$start_time" ]] && extra_args+=(--StartTime "$start_time")
    extra_args+=(--EndTime "$end_time")
    [[ -n "$limit" ]] && extra_args+=(--Limit "$limit")
    [[ -n "$offset" ]] && extra_args+=(--Offset "$offset")
    [[ -n "$order" ]] && extra_args+=(--Order "$order")
    [[ -n "$order_field" ]] && extra_args+=(--OrderField "$order_field")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询事件 (region=${region}, service=${service}, service-id=${service_id:-未指定})"
    local result
    result=$(call_tione_api "DescribeEvents" "$region" "${extra_args[@]}")
    format_json "$result"
}

main "$@"
