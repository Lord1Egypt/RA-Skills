#!/usr/bin/env bash
# ============================================================================
# 生成 TI-ONE 控制台 URL
# 根据资源类型和 ID 生成可直接访问的控制台链接
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../common.sh"

# ---------------------------------------------------------------------------
# 地域 → regionId 映射
# ---------------------------------------------------------------------------
declare -A REGION_ID_MAP=(
    ["ap-guangzhou"]=1
    ["ap-shanghai"]=4
    ["ap-beijing"]=8
    ["ap-nanjing"]=33
    ["ap-shanghai-adc"]=78
    ["ap-zhongwei"]=102
)

readonly CONSOLE_BASE="https://console.cloud.tencent.com/tione/v2"

# ---------------------------------------------------------------------------
# 帮助信息
# ---------------------------------------------------------------------------
usage() {
    cat <<EOF
用法: $(basename "$0") --type <资源类型> --id <资源ID> [选项]

生成 TI-ONE 控制台详情页 URL。

必填参数:
  --type <type>             资源类型: training | notebook | service | resource-group
  --id <id>                 资源 ID (如 train-xxx, nb-xxx, ms-xxx, rsg-xxx)

可选参数:
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --workspace-id <id>       工作空间 ID (默认: 0)
  --help                    显示帮助信息

示例:
  $(basename "$0") --type training --id train-1542619990512406272
  $(basename "$0") --type notebook --id nb-1542622025290711936 --region ap-beijing
  $(basename "$0") --type service --id ms-z4ddl2xp --workspace-id 12345
  $(basename "$0") --type resource-group --id rsg-x865ng7l
EOF
}

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
main() {
    local region="${DEFAULT_REGION}"
    local resource_type=""
    local resource_id=""
    local workspace_id="${TIONE_WORKSPACE_ID:-0}"

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --type) resource_type="$2"; shift 2 ;;
            --id) resource_id="$2"; shift 2 ;;
            --region) region="$2"; shift 2 ;;
            --workspace-id) workspace_id="$2"; shift 2 ;;
            --help) usage; exit 0 ;;
            *) log_error "未知参数: $1"; usage; exit 1 ;;
        esac
    done

    # 参数校验
    if [[ -z "$resource_type" ]]; then
        log_error "缺少必填参数: --type"
        usage
        exit 1
    fi
    if [[ -z "$resource_id" ]]; then
        log_error "缺少必填参数: --id"
        usage
        exit 1
    fi

    # 地域 → regionId
    local region_id="${REGION_ID_MAP[$region]:-}"
    if [[ -z "$region_id" ]]; then
        log_error "不支持的地域: ${region}"
        log_error "支持的地域: ${!REGION_ID_MAP[*]}"
        exit 1
    fi

    # 生成 URL
    local url=""
    case "$resource_type" in
        training|train)
            url="${CONSOLE_BASE}/job/detail/${resource_id}?regionId=${region_id}&workspaceId=${workspace_id}"
            ;;
        notebook|nb)
            url="${CONSOLE_BASE}/notebook/detail/${resource_id}?detail=info&regionId=${region_id}&workspaceId=${workspace_id}"
            ;;
        service|ms)
            url="${CONSOLE_BASE}/service/group/detail/${resource_id}?tab=management&regionId=${region_id}&workspaceId=${workspace_id}"
            ;;
        resource-group|rsg)
            url="${CONSOLE_BASE}/space-manage/resource/detail/${resource_id}?regionId=${region_id}&tab=detail"
            ;;
        *)
            log_error "不支持的资源类型: ${resource_type}"
            log_error "支持的类型: training, notebook, service, resource-group"
            exit 1
            ;;
    esac

    # 输出 JSON 格式结果
    jq -n \
        --arg type "$resource_type" \
        --arg id "$resource_id" \
        --arg region "$region" \
        --arg regionId "$region_id" \
        --arg workspaceId "$workspace_id" \
        --arg url "$url" \
        '{
            type: $type,
            id: $id,
            region: $region,
            regionId: ($regionId | tonumber),
            workspaceId: ($workspaceId | tonumber),
            consoleUrl: $url
        }'
}

main "$@"
