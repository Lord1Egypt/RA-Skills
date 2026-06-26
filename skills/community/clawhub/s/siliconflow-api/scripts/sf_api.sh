#!/bin/bash
# SiliconFlow API 封装脚本
# 支持：文生图、图生图、文生视频、图生视频、语音合成

set -e

CONFIG_FILE="$(dirname "$0")/../.sf-config.json"
BASE_URL="https://api.siliconflow.cn/v1"

# 读取配置
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ 未配置 API Key，请先运行: bash scripts/sf_api.sh setup"
        exit 1
    fi
    API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['api_key'])")
}

# 子命令: setup - 配置 API Key
cmd_setup() {
    echo "=== SiliconFlow API 配置 ==="
    read -p "请输入 API Key: " key
    if [ -z "$key" ]; then
        echo "❌ API Key 不能为空"
        exit 1
    fi
    cat > "$CONFIG_FILE" <<< "{\"api_key\": \"$key\"}"
    echo "✅ API Key 已保存到 $CONFIG_FILE"
    
    # 测试连通性
    echo "测试 API 连通性..."
    resp=$(curl -s https://api.siliconflow.cn/v1/models \
        -H "Authorization: Bearer $key")
    if echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('data',[])))" 2>/dev/null; then
        echo "✅ API 连接成功"
    else
        echo "❌ API 连接失败，请检查 Key"
    fi
}

# 子命令: text2image - 文生图
cmd_text2image() {
    load_config
    local prompt="$1"
    local size="${2:-1024x1024}"
    local model="${3:-Kwai-Kolors/Kolors}"
    local output="${4:-/tmp/sf_output.png}"
    
    echo "🎨 生成图片中..."
    echo "  模型: $model"
    echo "  提示词: $prompt"
    echo "  尺寸: $size"
    
    resp=$(curl -s -X POST "$BASE_URL/images/generations" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$model\",
            \"prompt\": \"$prompt\",
            \"n\": 1,
            \"size\": \"$size\"
        }")
    
    url=$(echo "$resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'images' in d and d['images']:
    print(d['images'][0]['url'])
else:
    print('ERROR:' + json.dumps(d))
" 2>/dev/null)
    
    if [[ "$url" == ERROR:* ]]; then
        echo "❌ 生成失败: $url"
        return 1
    fi
    
    curl -s "$url" -o "$output"
    echo "✅ 图片已保存: $output"
}

# 子命令: image2image - 图生图
cmd_image2image() {
    load_config
    local image_path="$1"
    local prompt="$2"
    local output="${3:-/tmp/sf_edit.png}"
    
    if [ ! -f "$image_path" ]; then
        echo "❌ 图片文件不存在: $image_path"
        return 1
    fi
    
    echo "🎨 编辑图片中..."
    echo "  源图: $image_path"
    echo "  提示词: $prompt"
    
    # 写 base64 到临时文件（防止命令行参数过长）
    base64 -w0 "$image_path" > /tmp/sf_b64.txt
    b64=$(cat /tmp/sf_b64.txt)
    
    # 生成请求 JSON
    python3 -c "
import json
b64 = open('/tmp/sf_b64.txt').read().strip()
payload = {
    'model': 'Kwai-Kolors/Kolors',
    'prompt': '$prompt',
    'n': 1,
    'size': '1024x1024',
    'image': 'data:image/png;base64,' + b64
}
open('/tmp/sf_req.json', 'w').write(json.dumps(payload))
"
    
    resp=$(curl -s -X POST "$BASE_URL/images/generations" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d @/tmp/sf_req.json)
    
    url=$(echo "$resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'images' in d and d['images']:
    print(d['images'][0]['url'])
else:
    print('ERROR:' + json.dumps(d))
" 2>/dev/null)
    
    if [[ "$url" == ERROR:* ]]; then
        echo "❌ 编辑失败: $url"
        return 1
    fi
    
    curl -s "$url" -o "$output"
    echo "✅ 编辑完成: $output"
}

# 子命令: text2video - 文生视频
cmd_text2video() {
    load_config
    local prompt="$1"
    local duration="${2:-5}"
    local output="${3:-/tmp/sf_video.mp4}"
    
    echo "🎬 提交视频生成..."
    echo "  模型: Wan-AI/Wan2.2-T2V-A14B"
    echo "  提示词: $prompt"
    echo "  时长: ${duration}s"
    
    resp=$(curl -s -X POST "$BASE_URL/video/submit" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"Wan-AI/Wan2.2-T2V-A14B\",
            \"prompt\": \"$prompt\",
            \"duration\": $duration
        }")
    
    req_id=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('requestId',''))" 2>/dev/null)
    
    if [ -z "$req_id" ]; then
        echo "❌ 提交失败: $resp"
        return 1
    fi
    
    echo "⏳ 任务已提交 (ID: $req_id)，等待生成..."
    echo "   可稍后用以下命令查询状态:"
    echo "   bash scripts/sf_api.sh video_status $req_id"
    
    # 轮询等待
    for i in $(seq 1 60); do
        sleep 10
        status_resp=$(curl -s -X POST "$BASE_URL/video/status" \
            -H "Authorization: Bearer $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"requestId\": \"$req_id\"}")
        
        status=$(echo "$status_resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
        
        if [ "$status" = "Succeed" ]; then
            video_url=$(echo "$status_resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
results = d.get('results', {})
if isinstance(results, dict):
    url = results.get('url', results.get('video_url', results.get('output', '')))
    print(url)
else:
    print(results)
" 2>/dev/null)
            
            if [ -n "$video_url" ] && [ "$video_url" != "None" ]; then
                curl -s "$video_url" -o "$output"
                echo "✅ 视频已生成: $output"
            else
                echo "✅ 视频已生成"
                echo "$status_resp" | python3 -m json.tool 2>/dev/null
            fi
            return 0
        elif [ "$status" = "Failed" ]; then
            reason=$(echo "$status_resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('reason',''))" 2>/dev/null)
            echo "❌ 生成失败: $reason"
            return 1
        fi
        
        echo "  等待中... ($((i*10))秒, 状态: $status)"
    done
    
    echo "⏰ 等待超时，任务仍在进行中"
    echo "   查询命令: bash scripts/sf_api.sh video_status $req_id"
}

# 子命令: image2video - 图生视频
cmd_image2video() {
    load_config
    local image_path="$1"
    local prompt="$2"
    local duration="${3:-5}"
    local output="${4:-/tmp/sf_video.mp4}"
    
    if [ ! -f "$image_path" ]; then
        echo "❌ 图片文件不存在: $image_path"
        return 1
    fi
    
    echo "🎬 提交图生视频..."
    echo "  模型: Wan-AI/Wan2.2-I2V-A14B"
    echo "  源图: $image_path"
    echo "  提示词: $prompt"
    
    # 写 base64 到临时文件
    base64 -w0 "$image_path" > /tmp/sf_b64.txt
    
    # 生成请求 JSON
    python3 -c "
import json
b64 = open('/tmp/sf_b64.txt').read().strip()
payload = {
    'model': 'Wan-AI/Wan2.2-I2V-A14B',
    'prompt': '$prompt',
    'duration': $duration,
    'image': 'data:image/png;base64,' + b64
}
open('/tmp/sf_req.json', 'w').write(json.dumps(payload))
"
    
    resp=$(curl -s -X POST "$BASE_URL/video/submit" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d @/tmp/sf_req.json)
    
    req_id=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('requestId',''))" 2>/dev/null)
    
    if [ -z "$req_id" ]; then
        echo "❌ 提交失败: $resp"
        return 1
    fi
    
    echo "⏳ 任务已提交 (ID: $req_id)，等待生成..."
    cmd_video_status "$req_id" "$output"
}

# 子命令: video_status - 查询视频生成状态
cmd_video_status() {
    load_config
    local req_id="$1"
    local output="${2:-/tmp/sf_video.mp4}"
    
    echo "📊 查询视频状态..."
    
    resp=$(curl -s -X POST "$BASE_URL/video/status" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"requestId\": \"$req_id\"}")
    
    status=$(echo "$resp" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null)
    echo "  状态: $status"
    
    if [ "$status" = "Succeed" ]; then
        video_url=$(echo "$resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
results = d.get('results', {})
if isinstance(results, dict):
    url = results.get('url', results.get('video_url', results.get('output', '')))
    print(url)
else:
    print(results)
" 2>/dev/null)
        
        if [ -n "$video_url" ] && [ "$video_url" != "None" ]; then
            curl -s "$video_url" -o "$output"
            echo "✅ 视频已下载: $output"
        else
            echo "$resp" | python3 -m json.tool 2>/dev/null
        fi
    else
        echo "$resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'  Position: {d.get(\"position\", \"N/A\")}')
reason = d.get('reason', '')
if reason:
    print(f'  Reason: {reason}')
" 2>/dev/null
    fi
}

# 子命令: tts - 文字转语音
cmd_tts() {
    load_config
    local text="$1"
    local voice="${2:-中文男声}"
    local output="${3:-/tmp/sf_tts.mp3}"
    
    echo "🔊 生成语音..."
    echo "  文本: $text"
    echo "  音色: $voice"
    
    curl -s -X POST "$BASE_URL/audio/speech" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"FunAudioLLM/CosyVoice2-0.5B\",
            \"input\": \"$text\",
            \"voice\": \"$voice\"
        }" -o "$output" 2>/dev/null
    
    if [ -f "$output" ] && [ -s "$output" ]; then
        echo "✅ 语音已保存: $output"
    else
        echo "❌ 语音生成失败"
        cat "$output" 2>/dev/null
    fi
}

# 子命令: list_models - 列出可用模型
cmd_list_models() {
    load_config
    echo "📋 可用模型（图像/视频/语音相关）："
    curl -s "$BASE_URL/models" \
        -H "Authorization: Bearer $API_KEY" | python3 -c "
import json,sys
data = json.load(sys.stdin)
keywords = ['image', 'video', 'wan', 'kolors', 'qwen-image', 'cosyvoice', 'sensevoice']
for m in data.get('data', []):
    mid = m.get('id', '')
    if any(k in mid.lower() for k in keywords):
        print(f'  {mid}')
" 2>/dev/null
}

# 主入口
case "${1:-help}" in
    setup)
        cmd_setup
        ;;
    text2image|t2i)
        shift
        cmd_text2image "$@"
        ;;
    image2image|i2i)
        shift
        cmd_image2image "$@"
        ;;
    text2video|t2v)
        shift
        cmd_text2video "$@"
        ;;
    image2video|i2v)
        shift
        cmd_image2video "$@"
        ;;
    video_status|vs)
        shift
        cmd_video_status "$@"
        ;;
    tts)
        shift
        cmd_tts "$@"
        ;;
    list_models|models)
        cmd_list_models
        ;;
    *)
        echo "SiliconFlow API 工具"
        echo ""
        echo "用法:"
        echo "  bash scripts/sf_api.sh setup                    # 首次配置 API Key"
        echo "  bash scripts/sf_api.sh text2image <提示词> [尺寸] [模型] [输出路径]"
        echo "  bash scripts/sf_api.sh image2image <图片路径> <提示词> [输出路径]"
        echo "  bash scripts/sf_api.sh text2video <提示词> [时长] [输出路径]"
        echo "  bash scripts/sf_api.sh image2video <图片路径> <提示词> [时长] [输出路径]"
        echo "  bash scripts/sf_api.sh video_status <任务ID> [输出路径]"
        echo "  bash scripts/sf_api.sh tts <文本> [音色] [输出路径]"
        echo "  bash scripts/sf_api.sh models                   # 列出可用模型"
        echo ""
        echo "示例:"
        echo "  bash scripts/sf_api.sh t2i '一个穿西装的老板'"
        echo "  bash scripts/sf_api.sh i2i photo.jpg '变成油画风格'"
        echo "  bash scripts/sf_api.sh t2v '一只猫在玩球' 5"
        echo "  bash scripts/sf_api.sh i2v photo.jpg '微笑挥手' 5"
        echo "  bash scripts/sf_api.sh vs abc123"
        echo "  bash scripts/sf_api.sh tts '你好，我们公司做软件开发'"
        ;;
esac
