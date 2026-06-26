#!/bin/bash
# vwu.ai 视频生成脚本 - 支持 Vidu/Kling/Veo 等模型
# 使用正确的 API 端点: https://api.vwu.ai/v1/videos

set -e

VWU_API_KEY="${VWU_API_KEY:-}"
VWU_BASE_URL="${VWU_BASE_URL:-https://api.vwu.ai}"

# 颜色输出
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查 API key
check_api_key() {
    if [ -z "$VWU_API_KEY" ]; then
        echo -e "${RED}❌ 错误: 未设置 VWU_API_KEY${NC}"
        echo ""
        echo -e "${YELLOW}⚠️  使用前需要创建 API Key:${NC}"
        echo ""
        echo "步骤:"
        echo "  1. 访问 https://vwu.ai"
        echo "  2. 登录账号"
        echo "  3. 进入「令牌管理」"
        echo "  4. 点击「新建令牌」"
        echo "  5. 设置名称（如：claw-video）"
        echo "  6. 复制生成的密钥"
        echo ""
        echo "然后设置环境变量:"
        echo "  export VWU_API_KEY='sk-your-key-here'"
        echo ""
        echo "或添加到 ~/.zshrc 永久保存:"
        echo "  echo 'export VWU_API_KEY=\"sk-your-key-here\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
        echo ""
        exit 1
    fi
    
    # 检查是否是默认占位符
    if [[ "$VWU_API_KEY" == *"your-key-here"* ]] || [[ "$VWU_API_KEY" == "sk-" ]]; then
        echo -e "${YELLOW}⚠️  警告: VWU_API_KEY 似乎未设置正确的值${NC}"
        echo ""
        echo "请在 vwu.ai 控制台创建真实的 API Key"
        echo "https://vwu.ai → 令牌管理 → 新建令牌"
        echo ""
        exit 1
    fi
}

# 显示帮助
show_help() {
    echo "用法: vwu-video [选项]"
    echo ""
    echo "选项:"
    echo "  --model <模型>        视频生成模型 (默认: viduq3-pro)"
    echo "  --prompt <提示词>     视频描述（必需）"
    echo "  --image <图片路径>    参考图片（可选，用于图生视频）"
    echo "  --duration <秒数>     视频时长（默认: 5，建议 2-10）"
    echo "  --ratio <宽高比>      16:9, 9:16, 1:1（默认: 16:9）"
    echo "  --output <文件路径>   输出文件（默认: auto）"
    echo "  --wait               等待生成完成并下载"
    echo "  --status <任务ID>     查询任务状态"
    echo "  --download <任务ID>   下载已完成的视频"
    echo "  --list-models        列出可用的视频生成模型"
    echo "  -h, --help           显示此帮助"
    echo ""
    echo "示例:"
    echo "  # 文生视频"
    echo "  vwu-video --prompt '一只猫咪跳舞' --wait"
    echo ""
    echo "  # 图生视频"
    echo "  vwu-video --image photo.jpg --prompt '让人物跳舞' --wait"
    echo ""
    echo "  # 高级用法"
    echo "  vwu-video --model viduq3-pro --prompt '风景延时' --duration 10 --wait"
    echo ""
    echo "可用的视频生成模型:"
    echo "  Vidu: viduq3-pro (推荐), viduq2-turbo"
    echo "  Kling: kling-v3"
    echo "  Veo: veo-3.0-generate-001"
    echo ""
    echo "配置:"
    echo "  需要先在 https://vwu.ai 控制台创建 API Key"
    echo "  然后设置: export VWU_API_KEY='your-key'"
}

# 列出可用的视频生成模型
list_models() {
    echo -e "${BLUE}可用的视频生成模型:${NC}"
    echo ""
    echo "✅ 已验证可用:"
    echo "  - viduq3-pro (Vidu Q3 Pro) - 推荐，完全支持"
    echo "  - kling-v3 (Kling V3)"
    echo ""
    echo "⏳ 需测试:"
    echo "  - viduq2-turbo (Vidu Q2 Turbo)"
    echo ""
    echo "⚠️  需特殊处理:"
    echo "  - veo-3.0-generate-001 (返回 Vertex AI ID)"
    echo ""
    echo "❌ 不支持:"
    echo "  - vidu2.0, viduq1, viduq1-classic, viduq2-pro"
}

# 创建视频生成任务
create_task() {
    local model="$1"
    local prompt="$2"
    local image="$3"
    local duration="$4"
    local ratio="$5"

    echo -e "${BLUE}🎬 创建视频生成任务...${NC}"
    echo "  模型: $model"
    echo "  提示词: $prompt"
    [ -n "$image" ] && echo "  参考图片: $image"
    echo "  时长: ${duration}秒"
    echo "  宽高比: $ratio"
    echo ""

    # 构建 JSON payload
    metadata="{\"duration\": $duration, \"aspect_ratio\": \"$ratio\"}"

    if [ -n "$image" ]; then
        # 如果有图片，转换为 base64
        if [ ! -f "$image" ]; then
            echo -e "${RED}❌ 错误: 图片文件不存在: $image${NC}"
            exit 1
        fi
        image_base64=$(base64 -i "$image" | tr -d '\n')
        prompt_json="\"prompt\": \"$prompt\", \"image\": \"data:image/jpeg;base64,$image_base64\""
    else
        prompt_json="\"prompt\": \"$prompt\""
    fi

    # 调用 API
    response=$(curl -s -w "\n%{http_code}" "$VWU_BASE_URL/v1/videos" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $VWU_API_KEY" \
        -d "{
            \"model\": \"$model\",
            $prompt_json,
            \"metadata\": $metadata
        }" 2>&1)

    http_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        task_id=$(echo "$body" | jq -r '.id // .task_id')
        echo -e "${GREEN}✅ 任务创建成功!${NC}"
        echo "  任务 ID: $task_id"
        echo ""
        echo "后续操作:"
        echo "  查询状态: vwu-video --status $task_id"
        echo "  等待下载: vwu-video --wait --task-id $task_id"
        echo "$task_id"
    else
        echo -e "${RED}❌ 任务创建失败${NC}"
        echo "HTTP 状态: $http_code"
        echo "$body" | jq -r '.error.message // .message // .' 2>/dev/null || echo "$body"
        
        # 检查是否是额度问题
        if echo "$body" | grep -i "额度\|quota\|余额" > /dev/null 2>&1; then
            echo ""
            echo -e "${YELLOW}⚠️  API Key 额度不足！${NC}"
            echo ""
            echo "解决方法:"
            echo "  1. 访问 https://vwu.ai 控制台"
            echo "  2. 为当前 API Key 充值，或"
            echo "  3. 创建新的 API 令牌"
        fi
        exit 1
    fi
}

# 查询任务状态
check_status() {
    local task_id="$1"

    echo -e "${BLUE}🔍 查询任务状态...${NC}"
    echo "任务 ID: $task_id"
    echo ""

    response=$(curl -s "$VWU_BASE_URL/v1/videos/$task_id" \
        -H "Authorization: Bearer $VWU_API_KEY")

    task_status=$(echo "$response" | jq -r '.status')
    progress=$(echo "$response" | jq -r '.progress')

    echo "  状态: $task_status"
    echo "  进度: $progress%"

    case "$task_status" in
        "queued")
            echo -e "  ${YELLOW}⏳ 队列中...${NC}"
            ;;
        "in_progress")
            echo -e "  ${YELLOW}🔄 生成中...${NC}"
            ;;
        "succeeded"|"completed")
            echo -e "  ${GREEN}✅ 已完成!${NC}"
            echo ""
            echo "下载视频:"
            echo "  vwu-video --download $task_id --output video.mp4"
            ;;
        "failed")
            echo -e "  ${RED}❌ 生成失败${NC}"
            echo "$response" | jq '.'
            ;;
        *)
            echo "  未知状态: $task_status"
            echo "$response" | jq '.'
            ;;
    esac
}

# 等待任务完成并下载
wait_and_download() {
    local task_id="$1"
    local output="$2"

    if [ -z "$output" ]; then
        output="video_$(date +%s).mp4"
    fi

    echo -e "${BLUE}⏳ 等待视频生成完成...${NC}"
    echo "任务 ID: $task_id"
    echo ""

    local max_wait=300  # 最多等待5分钟
    local waited=0
    local check_interval=10

    while [ $waited -lt $max_wait ]; do
        response=$(curl -s "$VWU_BASE_URL/v1/videos/$task_id" \
            -H "Authorization: Bearer $VWU_API_KEY")

        task_status=$(echo "$response" | jq -r '.status')
        progress=$(echo "$response" | jq -r '.progress')

        echo "[$(date +%H:%M:%S)] 状态: $task_status | 进度: $progress%"

        if [ "$task_status" = "succeeded" ] || [ "$task_status" = "completed" ]; then
            echo ""
            echo -e "${GREEN}✅ 视频生成完成!${NC}"
            echo ""
            echo "⬇️  下载到: $output"

            curl -s "$VWU_BASE_URL/v1/videos/$task_id/content" \
                -H "Authorization: Bearer $VWU_API_KEY" \
                -o "$output"

            if [ -f "$output" ]; then
                file_size=$(ls -lh "$output" | awk '{print $5}')
                echo "  文件大小: $file_size"
                echo ""
                echo "播放: open \"$output\""
                echo "或: ffplay \"$output\""
            else
                echo -e "${RED}❌ 下载失败${NC}"
                exit 1
            fi
            return 0
        fi

        if [ "$task_status" = "failed" ]; then
            echo ""
            echo -e "${RED}❌ 视频生成失败${NC}"
            echo "$response" | jq '.'
            exit 1
        fi

        sleep $check_interval
        waited=$((waited + check_interval))
    done

    echo ""
    echo -e "${YELLOW}⏰ 等待超时${NC}"
    echo "任务可能仍在生成中，请稍后查询:"
    echo "  vwu-video --status $task_id"
}

# 下载视频
download_video() {
    local task_id="$1"
    local output="$2"

    echo -e "${BLUE}⬇️  下载视频...${NC}"
    echo "任务 ID: $task_id"
    echo "输出: $output"
    echo ""

    curl -s "$VWU_BASE_URL/v1/videos/$task_id/content" \
        -H "Authorization: Bearer $VWU_API_KEY" \
        -o "$output"

    if [ -f "$output" ]; then
        file_size=$(ls -lh "$output" | awk '{print $5}')
        echo -e "${GREEN}✅ 下载完成!${NC}"
        echo "  文件: $output"
        echo "  大小: $file_size"
    else
        echo -e "${RED}❌ 下载失败${NC}"
        exit 1
    fi
}

# 主程序
main() {
    local model=""
    local prompt=""
    local image=""
    local duration=5
    local ratio="16:9"
    local output=""
    local action=""
    local task_id=""

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --model)
                model="$2"
                shift 2
                ;;
            --prompt)
                prompt="$2"
                shift 2
                ;;
            --image)
                image="$2"
                shift 2
                ;;
            --duration)
                duration="$2"
                shift 2
                ;;
            --ratio)
                ratio="$2"
                shift 2
                ;;
            --output)
                output="$2"
                shift 2
                ;;
            --wait)
                action="wait"
                shift
                ;;
            --status)
                action="status"
                task_id="$2"
                shift 2
                ;;
            --task-id)
                task_id="$2"
                shift 2
                ;;
            --download)
                action="download"
                task_id="$2"
                output="$4"
                shift 4
                ;;
            --list-models)
                check_api_key
                list_models
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                echo "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done

    check_api_key

    # 执行操作
    case "$action" in
        status)
            if [ -z "$task_id" ]; then
                echo "错误: 需要提供任务 ID"
                exit 1
            fi
            check_status "$task_id"
            ;;
        download)
            if [ -z "$task_id" ]; then
                echo "错误: 需要提供任务 ID"
                exit 1
            fi
            download_video "$task_id" "$output"
            ;;
        wait)
            if [ -z "$task_id" ]; then
                # 创建新任务并等待
                if [ -z "$prompt" ]; then
                    echo "错误: 需要提供提示词"
                    exit 1
                fi
                [ -z "$model" ] && model="viduq3-pro"
                task_id=$(create_task "$model" "$prompt" "$image" "$duration" "$ratio")
            fi
            wait_and_download "$task_id" "$output"
            ;;
        "")
            # 默认：创建任务
            if [ -z "$prompt" ]; then
                echo "错误: 需要提供提示词 (--prompt)"
                show_help
                exit 1
            fi
            [ -z "$model" ] && model="viduq3-pro"
            create_task "$model" "$prompt" "$image" "$duration" "$ratio"
            ;;
    esac
}

main "$@"
