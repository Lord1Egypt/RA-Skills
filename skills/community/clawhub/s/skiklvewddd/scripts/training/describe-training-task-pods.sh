#!/usr/bin/env bash
# ============================================================================
# 查询训练任务 Pod 列表
# 接口: DescribeTrainingTaskPods
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --id <task-id> [选项]

查询训练任务 Pod 列表

选项:
  --id <task-id>            训练任务 ID (必填)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --id train-1541487017891259392
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local task_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --id) task_id="$2"; shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$task_id" ]]; then
        log_error "缺少必填参数: --id"
        usage
    fi

    log_info "查询训练任务 Pod 列表 (region=${region}, id=${task_id})"
    local result
    result=$(call_tione_api "DescribeTrainingTaskPods" "$region" --Id "$task_id")
    format_json "$result"
}

main "$@"
