#!/usr/bin/env bash
# ============================================================
# api.sh — 车险快速投保含中文字段的接口调用工具
#
# 适用场景：JSON body 中含中文字段（车牌省份汉字、车主姓名等）的接口。
# 纯 ASCII body 的接口（sendCode / verifyCode / revokeGrant 等）
# 可直接用 curl，无需通过本脚本。
#
# 依赖：curl（macOS/Linux/Windows Git Bash 均内置）
#
# 用法：bash scripts/api.sh <接口名> '<JSON body>' "$CAR_API_KEY"
#
# 支持的接口名（均需要 car_api_key）：
#   quickQuote            POST /api/quickInsure/quickQuote
#   quickConfirmAndPay    POST /api/quickInsure/quickConfirmAndPay
#   getCreatePolicy       POST /api/quickInsure/getCreatePolicy
#
# 参数：
#   $1  接口名（见上方列表）
#   $2  完整 JSON body（调用方原样传入，脚本写入临时文件后发送）
#   $3  car_api_key（也可通过环境变量 CAR_API_KEY 传入）
#
# 示例：
#   # 快速报价（已绑车）
#   bash scripts/api.sh quickQuote '{"vehicleNo":"沪A12345"}' "$CAR_API_KEY"
#
#   # 快速报价（未绑车，含姓名）
#   bash scripts/api.sh quickQuote \
#     '{"vehicleNo":"粤B88888","carOwnerName":"张三","certificateNo":"110101199001011234","isInquireBusiness":true,"isInquireCompel":true}' \
#     "$CAR_API_KEY"
#
#   # 核保+支付链接
#   bash scripts/api.sh quickConfirmAndPay \
#     '{"vehicleNo":"沪A12345","insureFlowCode":"FLOW001","payChannel":"wxpay"}' \
#     "$CAR_API_KEY"
#
#   # 查询出单结果
#   bash scripts/api.sh getCreatePolicy \
#     '{"vehicleNo":"沪A12345","zaOrderNo":"ZA001","outTradeNo":"OUT001"}' \
#     "$CAR_API_KEY"
# ============================================================

set -euo pipefail

BASE_URL="https://car.zhongan.com"

# ------------------------------------------------------------------
# 接口名 → 路径映射
# ------------------------------------------------------------------
resolve_path() {
  case "$1" in
    quickQuote)         printf '/api/quickInsure/quickQuote' ;;
    quickConfirmAndPay) printf '/api/quickInsure/quickConfirmAndPay' ;;
    getCreatePolicy)    printf '/api/quickInsure/getCreatePolicy' ;;
    *)
      printf 'ERROR: 未知接口名 "%s"\n' "$1" >&2
      printf '可用接口：quickQuote quickConfirmAndPay getCreatePolicy\n' >&2
      printf '纯 ASCII body 的接口（sendCode/verifyCode 等）请直接使用 curl。\n' >&2
      exit 1
      ;;
  esac
}

# ==================================================================
# 入口
# ==================================================================
API_NAME="${1:-}"
RAW_BODY="${2:-}"
API_KEY="${3:-${CAR_API_KEY:-}}"

[ -z "$API_NAME" ] && {
  printf 'Usage: bash scripts/api.sh <接口名> <JSON body> <car_api_key>\n' >&2
  printf '接口名：quickQuote | quickConfirmAndPay | getCreatePolicy\n' >&2
  exit 1
}

[ -z "$API_KEY" ] && {
  printf 'ERROR: car_api_key 未提供，请作为第3个参数传入或设置环境变量 CAR_API_KEY\n' >&2
  exit 1
}

PATH_SUFFIX=$(resolve_path "$API_NAME")

# ------------------------------------------------------------------
# 将 JSON body 写入系统临时目录的 UTF-8 无 BOM 文件。
# 用文件替代字符串传参，彻底规避 Windows Git Bash 多字节截断问题。
# 随机后缀防止并发调用时文件名冲突；系统 %TEMP%/tmp 定期自动回收。
# ------------------------------------------------------------------
TMP_DIR="${TMPDIR:-${TEMP:-${TMP:-/tmp}}}"
TMP_FILE="${TMP_DIR}/car_api_body_$$_${RANDOM}.json"

# printf '%s' 输出无换行、无 BOM，保证文件内容与入参完全一致
printf '%s' "$RAW_BODY" > "$TMP_FILE"

# 脚本退出时（含异常）自动删除临时文件
trap 'rm -f "$TMP_FILE"' EXIT

printf '>> POST %s%s\n>> body: %s\n\n' "$BASE_URL" "$PATH_SUFFIX" "$RAW_BODY" >&2

# curl -d @file 直接读取文件字节流发送，不经过 shell 字符串处理
curl -s -X POST "${BASE_URL}${PATH_SUFFIX}" \
  -H "car-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "@${TMP_FILE}"

printf '\n' >&2
