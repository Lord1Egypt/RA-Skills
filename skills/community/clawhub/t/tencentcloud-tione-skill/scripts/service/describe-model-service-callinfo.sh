#!/usr/bin/env bash
# ============================================================================
# 查询服务调用信息
# 接口: DescribeModelServiceCallInfo
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --service-group-id <group-id> [选项]

查询在线推理服务的调用信息（调用地址等）

选项:
  --service-group-id <id>   服务组 ID (必填)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --service-group-id ms-7slhdl7d
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local service_group_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --service-group-id) service_group_id="$2"; shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$service_group_id" ]]; then
        log_error "缺少必填参数: --service-group-id"
        usage
    fi

    log_info "查询服务调用信息 (region=${region}, group-id=${service_group_id})"
    local result
    result=$(call_tione_api "DescribeModelServiceCallInfo" "$region" --ServiceGroupId "$service_group_id")
    format_json "$result"
}

main "$@"
