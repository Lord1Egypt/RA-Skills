#!/bin/bash

# Textin 文档解析脚本
# 用法: ./parse.sh <file_url|file_path> [options...]

CONFIG_FILE="$HOME/.openclaw/textin-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 请先配置 API 凭证"
    echo "告诉阿星你的 x-ti-app-id 和 x-ti-secret-code"
    exit 1
fi

APP_ID=$(cat "$CONFIG_FILE" | python3 -c "import sys,json;print(json.load(sys.stdin).get('app_id',''))")
SECRET_CODE=$(cat "$CONFIG_FILE" | python3 -c "import sys,json;print(json.load(sys.stdin).get('secret_code',''))")

if [ -z "$APP_ID" ] || [ -z "$SECRET_CODE" ]; then
    echo "❌ 凭证配置不完整"
    exit 1
fi

API_URL="https://api.textin.com/ai/service/v1/pdf_to_markdown"

# 默认参数
PARSE_MODE="scan"
TABLE_FLAVOR="html"
GET_IMAGE="objects"
APPLY_DOCUMENT_TREE=1
FORMULA_LEVEL=0
REMOVE_WATERMARK=0
APPLY_CHART=0
MARKDOWN_DETAILS=1
PAGE_DETAILS=1
GET_EXCEL=0
CROP_DEWARP=0

# 解析命令行参数
FILE_PATH=""
while [ $# -gt 0 ]; do
    case "$1" in
        --parse-mode)
            PARSE_MODE="$2"
            shift 2
            ;;
        --table-flavor)
            TABLE_FLAVOR="$2"
            shift 2
            ;;
        --get-image)
            GET_IMAGE="$2"
            shift 2
            ;;
        --apply-document-tree)
            APPLY_DOCUMENT_TREE="$2"
            shift 2
            ;;
        --formula-level)
            FORMULA_LEVEL="$2"
            shift 2
            ;;
        --remove-watermark)
            REMOVE_WATERMARK="$2"
            shift 2
            ;;
        --apply-chart)
            APPLY_CHART="$2"
            shift 2
            ;;
        --markdown-details)
            MARKDOWN_DETAILS="$2"
            shift 2
            ;;
        --page-details)
            PAGE_DETAILS="$2"
            shift 2
            ;;
        --get-excel)
            GET_EXCEL="$2"
            shift 2
            ;;
        --crop-dewarp)
            CROP_DEWARP="$2"
            shift 2
            ;;
        --page-start)
            PAGE_START="$2"
            shift 2
            ;;
        --page-count)
            PAGE_COUNT="$2"
            shift 2
            ;;
        --pdf-pwd)
            PDF_PWD="$2"
            shift 2
            ;;
        --dpi)
            DPI="$2"
            shift 2
            ;;
        *)
            FILE_PATH="$1"
            shift
            ;;
    esac
done

if [ -z "$FILE_PATH" ]; then
    echo "用法: $0 <file_url|file_path> [options]"
    echo "选项:"
    echo "  --parse-mode <auto|scan|lite|parse|vlm>"
    echo "  --table-flavor <html|md|none>"
    echo "  --get-image <none|page|objects|both>"
    echo "  --apply-document-tree <0|1>"
    echo "  --formula-level <0|1|2>"
    echo "  --remove-watermark <0|1>"
    echo "  --apply-chart <0|1>"
    echo "  --markdown-details <0|1>"
    echo "  --page-details <0|1>"
    echo "  --get-excel <0|1>"
    echo "  --crop-dewarp <0|1>"
    echo "  --page-start <number>"
    echo "  --page-count <number>"
    echo "  --pdf-pwd <password>"
    echo "  --dpi <72|144|216>"
    exit 1
fi

# 构建请求
if [[ "$FILE_PATH" =~ ^https?:// ]]; then
    # 在线文件 URL
    CONTENT_TYPE="text/plain"
    BODY="$FILE_PATH"
else
    # 本地文件
    if [ ! -f "$FILE_PATH" ]; then
        echo "❌ 文件不存在: $FILE_PATH"
        exit 1
    fi
    CONTENT_TYPE="application/octet-stream"
    BODY="--data-binary @${FILE_PATH}"
fi

# 构建查询参数
QUERY_PARAMS="parse_mode=${PARSE_MODE}&table_flavor=${TABLE_FLAVOR}&get_image=${GET_IMAGE}&apply_document_tree=${APPLY_DOCUMENT_TREE}&formula_level=${FORMULA_LEVEL}&remove_watermark=${REMOVE_WATERMARK}&apply_chart=${APPLY_CHART}&markdown_details=${MARKDOWN_DETAILS}&page_details=${PAGE_DETAILS}&get_excel=${GET_EXCEL}&crop_dewarp=${CROP_DEWARP}"

[ -n "$PAGE_START" ] && QUERY_PARAMS="${QUERY_PARAMS}&page_start=${PAGE_START}"
[ -n "$PAGE_COUNT" ] && QUERY_PARAMS="${QUERY_PARAMS}&page_count=${PAGE_COUNT}"
[ -n "$PDF_PWD" ] && QUERY_PARAMS="${QUERY_PARAMS}&pdf_pwd=${PDF_PWD}"
[ -n "$DPI" ] && QUERY_PARAMS="${QUERY_PARAMS}&dpi=${DPI}"

# 发送请求
if [ "$CONTENT_TYPE" = "text/plain" ]; then
    RESPONSE=$(curl -s -X POST "${API_URL}?${QUERY_PARAMS}" \
        -H "x-ti-app-id: ${APP_ID}" \
        -H "x-ti-secret-code: ${SECRET_CODE}" \
        -H "Content-Type: ${CONTENT_TYPE}" \
        -d "$BODY")
else
    RESPONSE=$(curl -s -X POST "${API_URL}?${QUERY_PARAMS}" \
        -H "x-ti-app-id: ${APP_ID}" \
        -H "x-ti-secret-code: ${SECRET_CODE}" \
        -H "Content-Type: ${CONTENT_TYPE}" \
        $BODY)
fi

# 解析响应
CODE=$(echo "$RESPONSE" | python3 -c "import sys,json;print(json.load(sys.stdin).get('code',''))" 2>/dev/null)

if [ "$CODE" = "200" ]; then
    echo "$RESPONSE" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('result',{}).get('markdown','')[:5000])"
    echo ""
    echo "✅ 解析成功！（仅显示前5000字符）"
else
    MESSAGE=$(echo "$RESPONSE" | python3 -c "import sys,json;print(json.load(sys.stdin).get('message',''))" 2>/dev/null)
    echo "❌ 解析失败: $CODE - $MESSAGE"
    echo "原始响应: $RESPONSE"
fi