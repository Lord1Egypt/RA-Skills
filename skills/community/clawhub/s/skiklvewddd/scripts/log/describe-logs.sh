#!/usr/bin/env bash
# ============================================================================
# 查询日志
# 接口: DescribeLogs
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --service <type> [选项]

查询日志

选项:
  --service <type>          服务类型 (必填): TRAIN | NOTEBOOK | INFER | BATCH
                            - TRAIN: 训练任务
                            - NOTEBOOK: Notebook 实例
                            - INFER: 在线推理服务
                            - BATCH: 批量预测任务
  --service-id <id>         实例级 ID (必填):
                            - TRAIN: LatestInstanceId (如 train-xxx-yyy, 从 DescribeTrainingTask 获取)
                            - NOTEBOOK: PodName (如 nb-xxx-yyy, 从 DescribeNotebook 获取)
                            - INFER: 服务实例 ID (如 ms-xxx-1, 从 DescribeModelServiceGroup 获取)
                            注意: 不支持顶层 ID (train-xxx / nb-xxx / ms-xxx)
  --pod-name <name>         Pod 名称 (可选, 支持通配符*)
                            - 不指定则返回所有 Pod 的日志
                            - 指定后只返回该 Pod 的日志
  --start-time <time>       开始时间 (RFC3339 格式, 如 2026-03-16T20:25:00+08:00)
                            建议从详情接口获取任务/实例的 StartTime
                            不指定则不传此参数 (由服务端决定)
  --end-time <time>         结束时间 (RFC3339 格式)
                            建议从详情接口获取任务/实例的 EndTime
                            不指定则默认为当前时间 (UTC)
  --limit <n>               返回条数 (默认: 100, 最大: 1000)
  --offset <n>              偏移量 (默认: 0)
  --order <ASC|DESC>        排序方向 (默认: DESC)
  --order-field <field>     排序字段 (默认: Timestamp)
  --context <ctx>           日志查询上下文 (用于翻页，值来自本接口返回)
  --filters <filters>       过滤条件 (格式: "Name=Key,Values=关键字" 可多次指定)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  # === 训练任务日志（标准流程） ===
  # 步骤 1: 查询训练任务详情，获取 LatestInstanceId 和 StartTime/EndTime
  describe-training-task.sh --region ap-shanghai --id train-xxx
  # 从返回中获取 LatestInstanceId (如 train-xxx-yyy) 和时间范围
  
  # 步骤 2: 使用 LatestInstanceId + 时间范围查询日志
  $(basename "$0") --region ap-shanghai --service TRAIN --service-id train-xxx-yyy \\
    --start-time "2026-03-16T20:00:00Z" --end-time "2026-03-16T21:00:00Z" --limit 50

  # === Notebook 日志（标准流程） ===
  # 步骤 1: 查询 Notebook 详情，获取 PodName 和 StartTime
  describe-notebook.sh --region ap-shanghai --id nb-xxx
  # 从返回中获取 PodName (如 nb-xxx-yyy)
  
  # 步骤 2: 使用 PodName 查询日志
  $(basename "$0") --region ap-shanghai --service NOTEBOOK --service-id nb-xxx-yyy \\
    --start-time "2026-03-16T20:00:00Z" --limit 50

  # === 在线推理服务日志（标准流程） ===
  # 步骤 1: 先获取服务实例 ID
  describe-model-service-group.sh --region ap-shanghai --id ms-xxx
  # 从 Services[].ServiceId 获取实例 ID，如 ms-xxx-1
  
  # 步骤 2: 使用服务实例 ID 查询日志
  $(basename "$0") --region ap-shanghai --service INFER --service-id ms-xxx-1 --limit 50
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
    local pod_name=""
    local context=""
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
            --pod-name) pod_name="$2"; shift 2 ;;
            --context) context="$2"; shift 2 ;;
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
    [[ -n "$pod_name" ]] && extra_args+=(--PodName "$pod_name")
    [[ -n "$context" ]] && extra_args+=(--Context "$context")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询日志 (region=${region}, service=${service}, service-id=${service_id:-未指定})"
    local result
    result=$(call_tione_api "DescribeLogs" "$region" "${extra_args[@]}")
    format_json "$result"
}

main "$@"
