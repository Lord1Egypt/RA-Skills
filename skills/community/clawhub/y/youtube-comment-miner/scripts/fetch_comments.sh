#!/bin/bash
# YouTube 批量评论获取脚本
# 用法: ./fetch_comments.sh "search_term" [count]

SEARCH_TERM=${1:-"openclaw"}
MAX_RESULTS=${2:-10}
OUTPUT_DIR="youtube_comments"

mkdir -p "$OUTPUT_DIR"

echo "🔍 搜索: $SEARCH_TERM (最多 $MAX_RESULTS 个视频)"

# 搜索视频并获取评论
yt-dlp "https://www.youtube.com/results?search_query=$(echo $SEARCH_TERM | tr ' ' '+')" \
    --dump-json --flat-playlist 2>/dev/null | \
    jq -r '.id' | head -$MAX_RESULTS | while read video_id; do
    output_file="$OUTPUT_DIR/${video_id}.json"
    
    if [ -f "$output_file" ]; then
        echo "⏭️ 跳过: $video_id (已存在)"
        continue
    fi
    
    echo "📥 获取评论: https://youtube.com/watch?v=$video_id"
    
    # 获取视频信息 + 评论
    yt-dlp --write-comments --dump-json \
        "https://www.youtube.com/watch?v=$video_id" \
        > "$output_file" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        comment_count=$(jq '.comments | length' "$output_file" 2>/dev/null || echo "0")
        echo "✅ 完成: $video_id ($comment_count 条评论)"
    else
        echo "❌ 失败: $video_id"
        rm -f "$output_file"
    fi
    
    # 避免请求过快
    sleep 2
done

echo ""
echo "🎉 完成! 评论保存在 $OUTPUT_DIR 目录"
echo "📊 运行分析: python3 scripts/analyze.py $OUTPUT_DIR"
