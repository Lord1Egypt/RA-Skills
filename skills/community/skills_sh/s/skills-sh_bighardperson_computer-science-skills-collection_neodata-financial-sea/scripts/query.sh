#!/usr/bin/env bash
# NeoData 金融数据查询 - curl 封装（通过代理 API）
#
# Usage:
#   bash query.sh --token "<JWT>" "腾讯最新财报"
#   bash query.sh --token "<JWT>" "贵州茅台股价"
#
# 鉴权优先级: --token 参数 > NEODATA_TOKEN 环境变量
#
# 环境变量 (可选):
#   NEODATA_TOKEN     - JWT token (当未使用 --token 参数时的备选)
#   NEODATA_ENDPOINT  - 代理 URL (可选，默认 https://copilot.tencent.com/agenttool/v1/neodata)
#   NEODATA_DATA_TYPE - 数据类型 all/api/doc (可选，默认不传由代理填充)

set -euo pipefail

DEFAULT_ENDPOINT="https://copilot.tencent.com/agenttool/v1/neodata"

# 解析参数
CLI_TOKEN=""
QUERY=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --token)
            CLI_TOKEN="$2"
            shift 2
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

if [[ -z "$QUERY" ]]; then
    echo "用法: bash query.sh [--token <JWT>] <query>" >&2
    exit 1
fi

ENDPOINT="${NEODATA_ENDPOINT:-$DEFAULT_ENDPOINT}"
TOKEN="${CLI_TOKEN:-${NEODATA_TOKEN:-}}"
DATA_TYPE="${NEODATA_DATA_TYPE:-}"

if [[ -z "$TOKEN" ]]; then
    echo "错误: 未提供 token。请使用 --token 参数或设置 NEODATA_TOKEN 环境变量" >&2
    exit 1
fi

# 构建请求体，channel 和 sub_channel 为固定字段
if [[ -n "$DATA_TYPE" ]]; then
    BODY=$(printf '{"query": "%s", "channel": "neodata", "sub_channel": "workbuddy", "data_type": "%s"}' "$QUERY" "$DATA_TYPE")
else
    BODY=$(printf '{"query": "%s", "channel": "neodata", "sub_channel": "workbuddy"}' "$QUERY")
fi

RESPONSE=$(curl --silent --show-error --location --max-time 30 --connect-timeout 10 \
    --write-out "\n%{http_code}" \
    "${ENDPOINT}" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer ${TOKEN}" \
    --data "$BODY")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY_RESP=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" -ne 200 ]]; then
    echo "请求失败: HTTP ${HTTP_CODE}" >&2
    [[ -n "$BODY_RESP" ]] && echo "$BODY_RESP" >&2
    exit 1
fi

echo "$BODY_RESP" | python3 -m json.tool 2>/dev/null || echo "$BODY_RESP"
