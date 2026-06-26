#!/bin/bash
# 微信公众号文章生成器 - 简洁专业版

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/wechat-api.sh"

# 显示帮助
show_help() {
    cat << EOF
微信公众号文章生成器

设计规范:
- 小标题: 绿色 #07c160，带左边框
- 正文: 黑色 #333
- 重点: 加粗，不使用额外颜色
- 禁用: emoji、花里胡哨的背景色

用法:
    $0 <input_file> [选项]

参数:
    input_file          输入文件 (Markdown 或 HTML)

选项:
    -t, --title         文章标题
    -s, --subtitle      副标题
    -a, --author        作者名 (默认: 超哥)
    -d, --digest        文章摘要
    -i, --image         封面图片路径 (可选)
    -o, --output        输出HTML文件路径
    --upload            上传到微信公众号草稿箱
    -h, --help          显示帮助

示例:
    $0 article.md -t "文章标题" -s "副标题" --upload
EOF
}

# 转换 Markdown 到 HTML（简洁版）
convert_markdown() {
    local input=$1
    
    # 简洁版转换规则
    # 一级标题 → 绿色小标题带边框
    sed 's/^# \(.*\)/<div style="margin:30px 0 15px 0;padding-left:12px;border-left:3px solid #07c160;"><h2 style="font-size:17px;color:#07c160;margin:0;font-weight:bold;">\1<\/h2><\/div>/g' "$input" | \
    # 二级标题 → 加粗小标题
    sed 's/^## \(.*\)/<p style="margin:20px 0 10px 0;"><strong>\1<\/strong><\/p>/g' | \
    # 三级标题 → 普通加粗
    sed 's/^### \(.*\)/<p style="margin:15px 0 10px 0;"><strong>\1<\/strong><\/p>/g' | \
    # 列表（使用 · 代替 emoji）
    sed 's/^[-*] \(.*\)/<p style="margin:0 0 5px 0;">· \1<\/p>/g' | \
    sed 's/^[0-9]\+\. \(.*\)/<p style="margin:0 0 5px 0;">\0<\/p>/g' | \
    # 引用 → 居中斜体
    sed 's/^> \(.*\)/<p style="margin:15px 0;text-align:center;font-size:15px;color:#666;font-style:italic;"><strong>\1<\/strong><\/p>/g' | \
    # 强调 → 仅加粗，不添加颜色
    sed 's/\*\*\([^*]*\)\*\*/<strong>\1<\/strong>/g' | \
    sed 's/\*\([^*]*\)\*/<em>\1<\/em>/g' | \
    # 段落
    sed 's/^\([^<].*\)$/<p style="margin:0 0 15px 0;">\1<\/p>/g' | \
    # 移除 emoji（常见范围）
    sed 's/[😀-🿿]//g' | \
    sed 's/[🀀-🃏]//g' | \
    sed 's/[🄀-🇿]//g'
}

# 生成标签HTML（简洁版）
generate_tags() {
    local tags=$1
    local html=""
    for tag in $tags; do
        # 移除标签中的 emoji
        tag=$(echo "$tag" | sed 's/[😀-🿿]//g; s/[🀀-🃏]//g; s/[🄀-🇿]//g')
        html="${html}<span style=\"display:inline-block;padding:5px 12px;background:#07c160;color:#fff;border-radius:15px;font-size:12px;margin:3px;\">$tag<\/span>"
    done
    echo "$html"
}

# 主函数
main() {
    local input_file=""
    local title=""
    local subtitle=""
    local author="超哥"
    local digest=""
    local image_path=""
    local output_file=""
    local upload=false
    local tags=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--title)
                title="$2"
                shift 2
                ;;
            -s|--subtitle)
                subtitle="$2"
                shift 2
                ;;
            -a|--author)
                author="$2"
                shift 2
                ;;
            -d|--digest)
                digest="$2"
                shift 2
                ;;
            -i|--image)
                image_path="$2"
                shift 2
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            --tags)
                tags="$2"
                shift 2
                ;;
            --upload)
                upload=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            -*)
                echo "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                input_file="$1"
                shift
                ;;
        esac
    done
    
    # 检查输入文件
    if [[ -z "$input_file" ]]; then
        echo "错误: 请指定输入文件"
        show_help
        exit 1
    fi
    
    if [[ ! -f "$input_file" ]]; then
        echo "错误: 文件不存在: $input_file"
        exit 1
    fi
    
    # 从文件名提取标题（如果没有指定）
    if [[ -z "$title" ]]; then
        title=$(basename "$input_file" | sed 's/\.[^.]*$//')
    fi
    
    # 从内容提取摘要（如果没有指定）
    if [[ -z "$digest" ]]; then
        digest=$(head -n 5 "$input_file" | grep -v "^#" | head -n 1 | cut -c 1-100)
    fi
    
    # 转换内容
    echo "正在转换内容..."
    local content=$(convert_markdown "$input_file")
    
    # 生成标签
    local tags_html=$(generate_tags "$tags")
    
    # 读取模板并替换变量
    echo "正在生成HTML..."
    local date=$(date +"%Y-%m-%d")
    local html=$(cat "$SCRIPT_DIR/template.html" | \
        sed "s/{{TITLE}}/$title/g" | \
        sed "s/{{SUBTITLE}}/$subtitle/g" | \
        sed "s/{{DATE}}/$date/g" | \
        sed "s/{{FOOTER_TEXT}}/本文是养虾日记系列/g" | \
        sed "s/{{TAGS}}/$tags_html/g")
    
    # 替换内容（特殊处理）
    html=$(echo "$html" | awk -v content="$content" '{gsub(/{{CONTENT}}/, content)} 1')
    
    # 保存输出
    if [[ -z "$output_file" ]]; then
        output_file="/tmp/wechat_article_$(date +%s).html"
    fi
    
    echo "$html" > "$output_file"
    echo "HTML已生成: $output_file"
    
    # 上传到微信
    if $upload; then
        echo "正在上传到微信公众号..."
        
        # 获取 access_token
        local access_token=$(get_access_token)
        echo "Access Token: ${access_token:0:20}..."
        
        # 上传封面图（如果指定）
        local thumb_media_id=$(get_config "default_thumb_media_id")
        if [[ -n "$image_path" && -f "$image_path" ]]; then
            echo "正在上传封面图片..."
            local upload_response=$(upload_image "$access_token" "$image_path")
            thumb_media_id=$(echo "$upload_response" | jq -r '.media_id')
            echo "封面图片ID: $thumb_media_id"
        fi
        
        # 准备JSON数据
        local json_file="/tmp/wechat_article_$(date +%s).json"
        cat > "$json_file" << EOF
{
  "articles": [
    {
      "title": "$title",
      "author": "$author",
      "digest": "$digest",
      "content": $(echo "$html" | jq -Rs '.'),
      "thumb_media_id": "$thumb_media_id",
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
}
EOF
        
        # 上传草稿
        local response=$(add_draft "$access_token" "$json_file")
        local media_id=$(echo "$response" | jq -r '.media_id')
        
        if [[ "$media_id" != "null" && -n "$media_id" ]]; then
            echo "✓ 上传成功!"
            echo "草稿ID: $media_id"
            echo "请在微信公众号后台「草稿箱」中查看"
        else
            echo "✗ 上传失败"
            echo "响应: $response"
            exit 1
        fi
        
        # 清理临时文件
        rm -f "$json_file"
    fi
    
    echo "完成!"
}

main "$@"
