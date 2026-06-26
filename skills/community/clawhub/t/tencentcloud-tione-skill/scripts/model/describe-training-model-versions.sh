#!/usr/bin/env bash
# ============================================================================
# 查询模型版本列表
# 接口: DescribeTrainingModelVersions
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --training-model-id <id> [选项]

查询模型版本列表

选项:
  --training-model-id <id>  模型 ID (必填)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --filters <filters>       过滤条件 (格式: "Name=xxx,Values=yyy" 可多次指定)
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --training-model-id model-xxx
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local training_model_id=""
    local -a filters=()
    local -a extra_args=()

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --training-model-id) training_model_id="$2"; shift 2 ;;
            --filters) filters+=("$2"); shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$training_model_id" ]]; then
        log_error "缺少必填参数: --training-model-id"
        usage
    fi

    extra_args+=(--TrainingModelId "$training_model_id")

    if [[ ${#filters[@]} -gt 0 ]]; then
        local filters_json
        filters_json=$(build_filters_args "${filters[@]}")
        extra_args+=(--Filters "$filters_json")
    fi

    log_info "查询模型版本列表 (region=${region}, model-id=${training_model_id})"
    local result
    result=$(call_tione_api "DescribeTrainingModelVersions" "$region" "${extra_args[@]}")
    format_json "$result"
}

main "$@"
