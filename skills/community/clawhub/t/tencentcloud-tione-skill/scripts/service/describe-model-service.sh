#!/usr/bin/env bash
# ============================================================================
# 查询单个在线服务详情
# 接口: DescribeModelService
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --service-id <id> [选项]

查询单个在线推理服务详情

选项:
  --service-id <id>         服务 ID (必填)
  --service-group-id <id>   服务组 ID (可选，兼容旧用法)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --service-id ms-7slhdl7d-1
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local service_id=""
    local service_group_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --service-id) service_id="$2"; shift 2 ;;
            --service-group-id) service_group_id="$2"; shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$service_id" ]]; then
        log_error "缺少必填参数: --service-id"
        usage
    fi

    local -a extra_args=(--ServiceId "$service_id")
    [[ -n "$service_group_id" ]] && extra_args+=(--ServiceGroupId "$service_group_id")

    log_info "查询服务详情 (region=${region}, service-id=${service_id}${service_group_id:+, group-id=${service_group_id}})"
    local result
    result=$(call_tione_api "DescribeModelService" "$region" "${extra_args[@]}")
    format_json "$result"
}

main "$@"
