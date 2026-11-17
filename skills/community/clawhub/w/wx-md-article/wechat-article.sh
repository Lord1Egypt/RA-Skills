#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/wechat-api.sh"

show_help() {
    cat <<'EOF'
微信公众号文章生成器

默认只生成本地 HTML，不发送网络请求。

用法:
  ./wechat-article.sh <input_file> [选项]

选项:
  -t, --title <title>       文章标题
  -s, --subtitle <text>     副标题
  -a, --author <name>       作者名
  -d, --digest <text>       文章摘要
  -i, --image <path>        封面图片路径
  -o, --output <path>       输出 HTML 路径
  --tags <tags>             空格分隔标签
  --upload                  请求上传到微信公众号草稿箱
  --confirm-upload          确认发送文章 HTML 和可选封面到 WECHAT_ACCOUNT_LABEL
  -h, --help                显示帮助

上传要求:
  1. 通过环境变量或密钥存储配置 WECHAT_APP_ID、WECHAT_APP_SECRET、
     WECHAT_ACCOUNT_LABEL 和 WECHAT_DEFAULT_THUMB_MEDIA_ID。
  2. 同时传入 --upload --confirm-upload。
  3. 不要把凭据写入 config.json、命令行、聊天或仓库。
EOF
}

convert_markdown() {
    local input=$1

    sed 's/^# \(.*\)/<div style="margin:30px 0 15px 0;padding-left:12px;border-left:3px solid #07c160;"><h2 style="font-size:17px;color:#07c160;margin:0;font-weight:bold;">\1<\/h2><\/div>/g' "$input" |
        sed 's/^## \(.*\)/<p style="margin:20px 0 10px 0;"><strong>\1<\/strong><\/p>/g' |
        sed 's/^### \(.*\)/<p style="margin:15px 0 10px 0;"><strong>\1<\/strong><\/p>/g' |
        sed 's/^[-*] \(.*\)/<p style="margin:0 0 5px 0;">· \1<\/p>/g' |
        sed 's/^[0-9]\+\. \(.*\)/<p style="margin:0 0 5px 0;">\0<\/p>/g' |
        sed 's/^> \(.*\)/<p style="margin:15px 0;text-align:center;font-size:15px;color:#666;font-style:italic;"><strong>\1<\/strong><\/p>/g' |
        sed 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g' |
        sed 's/\*\([^*]*\)\*/<em>\1<\/em>/g' |
        sed 's/^\([^<].*\)$/<p style="margin:0 0 15px 0;">\1<\/p>/g'
}

generate_tags() {
    local tags=$1
    local html=""
    local tag
    for tag in $tags; do
        html="${html}<span style=\"display:inline-block;padding:5px 12px;background:#07c160;color:#fff;border-radius:15px;font-size:12px;margin:3px;\">${tag}</span>"
    done
    printf '%s' "$html"
}

main() {
    local input_file=""
    local title=""
    local subtitle=""
    local author=""
    local digest=""
    local image_path=""
    local output_file=""
    local tags=""
    local upload=false
    local confirm_upload=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--title) title=${2:?missing title}; shift 2 ;;
            -s|--subtitle) subtitle=${2:?missing subtitle}; shift 2 ;;
            -a|--author) author=${2:?missing author}; shift 2 ;;
            -d|--digest) digest=${2:?missing digest}; shift 2 ;;
            -i|--image) image_path=${2:?missing image path}; shift 2 ;;
            -o|--output) output_file=${2:?missing output path}; shift 2 ;;
            --tags) tags=${2:?missing tags}; shift 2 ;;
            --upload) upload=true; shift ;;
            --confirm-upload) confirm_upload=true; shift ;;
            -h|--help) show_help; exit 0 ;;
            -*) printf 'Unknown option: %s\n' "$1" >&2; show_help; exit 1 ;;
            *) input_file=$1; shift ;;
        esac
    done

    [[ -n "$input_file" ]] || { printf 'Input file is required.\n' >&2; show_help; exit 1; }
    [[ -f "$input_file" ]] || { printf 'Input file not found: %s\n' "$input_file" >&2; exit 1; }

    [[ -n "$title" ]] || title=$(basename "$input_file" | sed 's/\.[^.]*$//')
    [[ -n "$digest" ]] || digest=$(head -n 5 "$input_file" | grep -v '^#' | head -n 1 | cut -c 1-100 || true)
    [[ -n "$output_file" ]] || output_file=$(mktemp "${TMPDIR:-/tmp}/wechat-article.XXXXXX.html")

    local content tags_html date html
    content=$(convert_markdown "$input_file")
    tags_html=$(generate_tags "$tags")
    date=$(date +%Y-%m-%d)
    html=$(sed \
        -e "s/{{TITLE}}/${title}/g" \
        -e "s/{{SUBTITLE}}/${subtitle}/g" \
        -e "s/{{DATE}}/${date}/g" \
        -e "s/{{FOOTER_TEXT}}//g" \
        -e "s#{{TAGS}}#${tags_html}#g" \
        "$SCRIPT_DIR/template.html")
    html=$(
        awk '
            FNR == NR {
                content = content $0 ORS
                next
            }
            {
                marker = index($0, "{{CONTENT}}")
                if (marker == 0) {
                    print
                } else {
                    print substr($0, 1, marker - 1) content substr($0, marker + 11)
                }
            }
        ' <(printf '%s\n' "$content") <(printf '%s\n' "$html")
    )

    printf '%s\n' "$html" >"$output_file"
    printf 'HTML generated locally: %s\n' "$output_file"

    if ! $upload; then
        return 0
    fi

    if ! $confirm_upload; then
        printf 'Upload blocked: add --confirm-upload after reviewing the local HTML and destination.\n' >&2
        return 2
    fi

    require_wechat_credentials
    printf 'Uploading article content to WeChat account: %s\n' "$WECHAT_ACCOUNT_LABEL"

    local access_token thumb_media_id upload_response json_file response media_id
    access_token=$(get_access_token)
    thumb_media_id=${WECHAT_DEFAULT_THUMB_MEDIA_ID:-}

    if [[ -n "$image_path" ]]; then
        [[ -f "$image_path" ]] || { printf 'Cover image not found: %s\n' "$image_path" >&2; exit 1; }
        upload_response=$(upload_image "$access_token" "$image_path")
        thumb_media_id=$(jq -r '.media_id // empty' <<<"$upload_response")
    fi

    [[ -n "$thumb_media_id" ]] || {
        printf 'WECHAT_DEFAULT_THUMB_MEDIA_ID or --image is required for upload.\n' >&2
        exit 1
    }

    json_file=$(mktemp "${TMPDIR:-/tmp}/wechat-draft.XXXXXX.json")
    trap 'rm -f "$json_file"' EXIT
    jq -n \
        --arg title "$title" \
        --arg author "$author" \
        --arg digest "$digest" \
        --arg content "$html" \
        --arg thumb_media_id "$thumb_media_id" \
        '{articles:[{title:$title,author:$author,digest:$digest,content:$content,thumb_media_id:$thumb_media_id,need_open_comment:1,only_fans_can_comment:0}]}' \
        >"$json_file"

    response=$(add_draft "$access_token" "$json_file")
    media_id=$(jq -r '.media_id // empty' <<<"$response")
    if [[ -z "$media_id" ]]; then
        printf 'Upload failed: %s\n' "$(jq -c '{errcode,errmsg}' <<<"$response")" >&2
        exit 1
    fi

    printf 'Draft uploaded successfully to %s. Draft ID: %s\n' "$WECHAT_ACCOUNT_LABEL" "$media_id"
}

main "$@"
