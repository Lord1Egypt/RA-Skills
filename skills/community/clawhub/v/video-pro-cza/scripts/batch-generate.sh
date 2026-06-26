#!/bin/bash
# Video Pro - 批量视频生成脚本
# 高级版功能，需要许可证密钥

set -e

# 配置
PROJECT_DIR="$HOME/openclaw-video-pro"
OUTPUT_DIR="$PROJECT_DIR/output/batch"
LOG_DIR="$PROJECT_DIR/logs"
CONFIG_FILE="$HOME/.video-pro/config.json"
LICENSE_FILE="$HOME/.video-pro/license.key"

# 检查许可证
check_license() {
    if [ ! -f "$LICENSE_FILE" ]; then
        echo "错误: 批量生成需要高级版许可证"
        echo ""
        echo "批量生成是 Video Pro 高级版功能，需要商业授权"
        echo ""
        echo "授权级别:"
        echo "  个人版 ($9.99/月): 每月100个视频"
        echo "  专业版 ($29.99/月): 每月500个视频"
        echo "  企业版 ($99.99/月): 无限视频"
        echo ""
        echo "获取授权: https://clawhub.com/@cza999/video-pro"
        echo ""
        echo "或者使用免费版单次生成:"
        echo "  ./generate.sh '你的脚本内容'"
        exit 1
    fi
    
    # 这里可以添加更复杂的许可证验证逻辑
    echo "✅ 许可证验证通过 (高级版)"
}

# 批量生成
batch_generate() {
    local input_file="$1"
    local template="${2:-basic}"
    local voice="${3:-alloy}"
    local speed="${4:-1.0}"
    local count=0
    
    if [ ! -f "$input_file" ]; then
        echo "错误: 输入文件不存在: $input_file"
        exit 1
    fi
    
    echo "开始批量视频生成..."
    echo "输入文件: $input_file"
    echo "模板: $template"
    echo "语音: $voice"
    echo "语速: $speed"
    echo ""
    
    # 创建输出目录
    local batch_id="batch_$(date +%Y%m%d_%H%M%S)"
    local batch_dir="$OUTPUT_DIR/$batch_id"
    mkdir -p "$batch_dir"
    
    # 读取文件并生成
    local line_num=0
    while IFS= read -r line || [ -n "$line" ]; do
        line_num=$((line_num + 1))
        
        # 跳过空行和注释
        if [ -z "$line" ] || [[ "$line" == \#* ]]; then
            continue
        fi
        
        echo "生成第 $line_num 个视频: ${line:0:50}..."
        
        # 调用单视频生成
        local output_name="video_${line_num}_$(date +%H%M%S).mp4"
        cd "$PROJECT_DIR"
        
        if [ -f "./generate-for-openclaw.sh" ]; then
            ./generate-for-openclaw.sh "$line" --voice "$voice" --speed "$speed" > "$batch_dir/log_$line_num.txt" 2>&1
        else
            ./agents/video-cli.sh generate "$line" --voice "$voice" --speed "$speed" > "$batch_dir/log_$line_num.txt" 2>&1
        fi
        
        # 查找并复制生成的视频
        local generated_file=""
        if [ -f "./out/generated.mp4" ]; then
            generated_file="./out/generated.mp4"
        else
            generated_file=$(find . -name "*.mp4" -type f -newer /tmp -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
        fi
        
        if [ -n "$generated_file" ] && [ -f "$generated_file" ]; then
            cp "$generated_file" "$batch_dir/$output_name"
            count=$((count + 1))
            echo "  ✅ 完成: $output_name"
        else
            echo "  ❌ 失败: 查看日志 $batch_dir/log_$line_num.txt"
        fi
        
        # 短暂延迟，避免API限制
        sleep 2
        
    done < "$input_file"
    
    echo ""
    echo "✅ 批量生成完成!"
    echo "📁 目录: $batch_dir"
    echo "📊 成功生成: $count 个视频"
    echo ""
    
    # 生成汇总报告
    generate_report "$batch_dir" "$count"
}

# 生成报告
generate_report() {
    local batch_dir="$1"
    local count="$2"
    local report_file="$batch_dir/report.json"
    
    cat > "$report_file" << EOF
{
  "batch_id": "$(basename "$batch_dir")",
  "generated_at": "$(date -Iseconds)",
  "total_videos": $count,
  "input_file": "$input_file",
  "template": "$template",
  "voice": "$voice",
  "speed": "$speed",
  "videos": [
EOF
    
    # 添加视频列表
    local first=true
    for video in "$batch_dir"/*.mp4; do
        if [ -f "$video" ]; then
            local size=$(stat -f%z "$video" 2>/dev/null || stat -c%s "$video" 2>/dev/null || echo "0")
            local duration=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$video" 2>/dev/null || echo "0")
            
            if [ "$first" = true ]; then
                first=false
            else
                echo "    ," >> "$report_file"
            fi
            
            cat >> "$report_file" << EOF
    {
      "filename": "$(basename "$video")",
      "size_bytes": $size,
      "duration_seconds": $duration,
      "created_at": "$(date -r "$video" -Iseconds)"
    }
EOF
        fi
    done
    
    cat >> "$report_file" << EOF
  ]
}
EOF
    
    echo "📋 报告: $report_file"
}

# 主流程
if [ $# -lt 1 ]; then
    echo "用法: $0 <脚本文件> [模板] [语音] [语速]"
    echo ""
    echo "示例:"
    echo "  $0 scripts.txt marketing nova 1.2"
    echo ""
    echo "脚本文件格式:"
    echo "  # 每行一个视频脚本"
    echo "  AI工具提升工作效率"
    echo "  ChatGPT帮助写作和编程"
    echo "  Midjourney生成精美图像"
    echo ""
    echo "注意: 批量生成需要高级版许可证"
    echo "获取授权: https://clawhub.com/@cza999/video-pro"
    exit 1
fi

check_license
batch_generate "$@"