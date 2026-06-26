#!/usr/bin/env bash
# ============================================================================
# 查询 Notebook 详情
# 接口: DescribeNotebook
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

usage() {
    cat <<EOF
用法: $(basename "$0") --id <notebook-id> [选项]

查询 Notebook 详情

选项:
  --id <notebook-id>        Notebook ID (必填)
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息

示例:
  $(basename "$0") --region ap-shanghai --id nb-xxx
EOF
    exit 0
}

main() {
    local region="${DEFAULT_REGION}"
    local notebook_id=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --region) region="$2"; shift 2 ;;
            --id) notebook_id="$2"; shift 2 ;;
            --help) usage ;;
            *) log_error "未知参数: $1"; usage ;;
        esac
    done

    if [[ -z "$notebook_id" ]]; then
        log_error "缺少必填参数: --id"
        usage
    fi

    log_info "查询 Notebook 详情 (region=${region}, id=${notebook_id})"
    local result
    result=$(call_tione_api "DescribeNotebook" "$region" --Id "$notebook_id")
    format_json "$result"
}

main "$@"
