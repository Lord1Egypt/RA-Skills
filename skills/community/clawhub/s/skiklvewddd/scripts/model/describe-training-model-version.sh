#!/usr/bin/env bash
# ============================================================================
# 查询模型版本详情
# 接口: DescribeTrainingModelVersion
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --training-model-version-id <id> [选项]

查询模型版本详情

选项:
  --training-model-version-id <id>  模型版本 ID (必填)
  --region <region>                 地域 (默认: ${DEFAULT_REGION})
  --help                            显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --training-model-version-id ver-xxx
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local version_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --training-model-version-id) version_id="$2"; shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$version_id" ]]; then
        log_error "缺少必填参数: --training-model-version-id"
        usage
    fi

    log_info "查询模型版本详情 (region=${region}, version-id=${version_id})"
    local result
    result=$(call_tione_api "DescribeTrainingModelVersion" "$region" --TrainingModelVersionId "$version_id")
    format_json "$result"
}

main "$@"
