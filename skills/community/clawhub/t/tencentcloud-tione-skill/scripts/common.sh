#!/usr/bin/env bash
# ============================================================================
# TI-ONE 公共函数库
# 提供日志输出、参数解析、tccli 调用封装等基础能力
# ============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# 颜色定义
# ---------------------------------------------------------------------------
readonly COLOR_RED='\033[0;31m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[0;33m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_NC='\033[0m'

# ---------------------------------------------------------------------------
# 默认配置
# ---------------------------------------------------------------------------
DEFAULT_REGION="${TENCENT_TIONE_DEFAULT_REGION:-ap-shanghai}"

# ---------------------------------------------------------------------------
# 日志函数
# ---------------------------------------------------------------------------
log_info() {
    echo -e "${COLOR_GREEN}[INFO]${COLOR_NC} $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_NC} $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

log_debug() {
    if [[ "${TIONE_DEBUG:-0}" == "1" ]]; then
        echo -e "${COLOR_BLUE}[DEBUG]${COLOR_NC} $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
    fi
}

# ---------------------------------------------------------------------------
# 前置检查
# ---------------------------------------------------------------------------
check_dependencies() {
    local missing=()
    for cmd in tccli jq; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "缺少依赖工具: ${missing[*]}"
        log_error "请先安装: pip3 install tccli && apt install jq"
        exit 1
    fi
}

check_credentials() {
    if [[ -z "${TENCENTCLOUD_SECRET_ID:-}" ]] || [[ -z "${TENCENTCLOUD_SECRET_KEY:-}" ]]; then
        log_error "未配置腾讯云凭证"
        log_error "请设置环境变量: TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY"
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# tccli 调用封装
# ---------------------------------------------------------------------------
# 调用 tccli tione 接口
# 参数: $1=接口名 $2=地域 $3...=额外参数
call_tione_api() {
    local action="$1"
    local region="$2"
    shift 2
    local extra_args=("$@")

    check_dependencies
    check_credentials

    log_info "调用接口: tione ${action} --region ${region}"
    log_debug "额外参数: ${extra_args[*]:-无}"

    local result
    local exit_code=0

    result=$(tccli tione "$action" --region "$region" "${extra_args[@]}" 2>&1) || exit_code=$?

    if [[ $exit_code -ne 0 ]]; then
        log_error "接口调用失败 (exit_code=${exit_code})"
        log_error "错误信息: ${result}"
        echo "$result"
        return $exit_code
    fi

    log_info "接口调用成功: tione ${action}"
    echo "$result"
}

# 格式化 JSON 输出
format_json() {
    local input="${1:-}"
    if [[ -n "$input" ]]; then
        echo "$input" | jq '.' 2>/dev/null || echo "$input"
    else
        jq '.' 2>/dev/null || cat
    fi
}

# ---------------------------------------------------------------------------
# 参数构建辅助函数
# ---------------------------------------------------------------------------
# 构建 Filters 参数
# 用法: 每个 filter 作为一个独立参数，多次 --filters 指定多个条件
#   build_filters_args "Name=Status,Values=Running" "Name=ResourceGroupId,Values=rsg-xxx"
# 多值用分号分隔: "Name=Status,Values=RUNNING;STARTING;STOPPING"
# 模糊匹配加 Fuzzy=true: "Name=ResourceGroupName,Values=test,Fuzzy=true"
build_filters_args() {
    local filters_json="["
    local first=true
    for filter in "$@"; do
        local name="" fuzzy=""
        # 提取 Name 值: Name= 后到第一个逗号
        name=$(echo "$filter" | sed 's/Name=\([^,]*\).*/\1/')
        # 提取 Values 值: Values= 后的内容，去掉尾部的 ,Fuzzy=true（如果有）
        local value
        value=$(echo "$filter" | sed 's/.*Values=//' | sed 's/,Fuzzy=true$//')
        # 检查是否包含 Fuzzy=true
        if echo "$filter" | grep -q 'Fuzzy=true'; then
            fuzzy=true
        fi
        if [[ "$first" == "true" ]]; then
            first=false
        else
            filters_json+=","
        fi
        # 支持多值: 用分号分隔，拆分为 JSON 数组
        local values_json=""
        IFS=';' read -ra val_arr <<< "$value"
        local vfirst=true
        for v in "${val_arr[@]}"; do
            if [[ "$vfirst" == "true" ]]; then
                vfirst=false
            else
                values_json+=","
            fi
            values_json+="\"${v}\""
        done
        filters_json+="{\"Name\":\"${name}\",\"Values\":[${values_json}]"
        if [[ "$fuzzy" == "true" ]]; then
            filters_json+=",\"Fuzzy\":true"
        fi
        filters_json+="}"
    done
    filters_json+="]"
    echo "$filters_json"
}

# ---------------------------------------------------------------------------
# 资源单位转换函数
# ---------------------------------------------------------------------------
# 将资源组返回的原始值转换为可读单位
# CPU: 0.001核 → 核, Mem: MB → GB, GPU: 0.01卡 → 卡, GpuMem: 0.01GB → GB
convert_resource_units() {
    local input="${1:-}"
    if [[ -z "$input" ]]; then
        cat
        return
    fi
    echo "$input" | jq '
      # 转换单个资源组对象中的资源字段
      def convert_rg:
        if . == null then .
        else
          (.Cpu           // null) as $cpu |
          (.Mem           // null) as $mem |
          (.Gpu           // null) as $gpu |
          (.GpuMem        // null) as $gpumem |
          (.AvailableCpu  // null) as $acpu |
          (.AvailableMem  // null) as $amem |
          (.AvailableGpu  // null) as $agpu |
          (.AvailableGpuMem // null) as $agpumem |
          (if $cpu     != null then .Cpu           = (($cpu / 1000 * 100 | round) / 100) | .CpuUnit = "核"   else . end) |
          (if $mem     != null then .Mem           = (($mem / 1024 * 100 | round) / 100) | .MemUnit = "GB"   else . end) |
          (if $gpu     != null then .Gpu           = (($gpu / 100  * 100 | round) / 100) | .GpuUnit = "卡"   else . end) |
          (if $gpumem  != null then .GpuMem        = (($gpumem / 100 * 100 | round) / 100) | .GpuMemUnit = "GB" else . end) |
          (if $acpu    != null then .AvailableCpu  = (($acpu / 1000 * 100 | round) / 100) | .AvailableCpuUnit = "核" else . end) |
          (if $amem    != null then .AvailableMem  = (($amem / 1024 * 100 | round) / 100) | .AvailableMemUnit = "GB" else . end) |
          (if $agpu    != null then .AvailableGpu  = (($agpu / 100  * 100 | round) / 100) | .AvailableGpuUnit = "卡" else . end) |
          (if $agpumem != null then .AvailableGpuMem = (($agpumem / 100 * 100 | round) / 100) | .AvailableGpuMemUnit = "GB" else . end)
        end;

      # 转换单个节点实例中的资源字段
      def convert_instance:
        if . == null then .
        else
          (.Cpu    // null) as $cpu |
          (.Memory // null) as $mem |
          (.Gpu    // null) as $gpu |
          (.GpuMem // null) as $gpumem |
          (if $cpu    != null then .Cpu    = (($cpu / 1000 * 100 | round) / 100) | .CpuUnit = "核"   else . end) |
          (if $mem    != null then .Memory = (($mem / 1024 * 100 | round) / 100) | .MemoryUnit = "GB" else . end) |
          (if $gpu    != null then .Gpu    = (($gpu / 100  * 100 | round) / 100) | .GpuUnit = "卡"   else . end) |
          (if $gpumem != null then .GpuMem = (($gpumem / 100 * 100 | round) / 100) | .GpuMemUnit = "GB" else . end)
        end;

      if .ResourceGroupSet then
        .ResourceGroupSet |= [.[] | convert_rg]
      elif .InstanceSet then
        .InstanceSet |= [.[] | convert_instance]
      else
        .
      end
    '
}

# ---------------------------------------------------------------------------
# 通用帮助信息
# ---------------------------------------------------------------------------
print_common_options() {
    cat <<EOF
通用选项:
  --region <region>         地域 (默认: ${DEFAULT_REGION})
  --help                    显示帮助信息
EOF
}
