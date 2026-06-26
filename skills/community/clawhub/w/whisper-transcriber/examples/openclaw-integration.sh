#!/bin/bash

# =============================================================================
# Whisper Transcriber - OpenClaw 集成示例
# =============================================================================
# 用途：在 OpenClaw 中自动处理语音消息
# =============================================================================

# 配置
SKILL_DIR="$HOME/.openclaw/workspace/skills/whisper-transcriber"
MODEL="base"
LANG="zh"
OUTPUT_FORMAT="txt"

# 处理语音消息
# 参数：$1 = 音频文件路径
process_voice_message() {
    local audio_file="$1"
    
    if [ ! -f "$audio_file" ]; then
        echo "错误：文件不存在 $audio_file"
        return 1
    fi
    
    # 调用转写脚本
    local result
    result=$("$SKILL_DIR/transcribe.sh" "$audio_file" -m "$MODEL" -l "$LANG" -t 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "$result"
    else
        echo "转写失败"
        return 1
    fi
}

# 示例：处理 OpenClaw inbound 语音消息
# 当收到语音消息时自动调用
handle_inbound_voice() {
    local media_path="$1"
    
    # 转写
    local transcript
    transcript=$(process_voice_message "$media_path")
    
    # 输出结果
    if [ -n "$transcript" ]; then
        echo "🎤 语音转写结果："
        echo "$transcript"
    fi
}

# 主程序（测试用）
if [ "$1" = "test" ]; then
    echo "测试模式：处理示例音频"
    handle_inbound_voice "$2"
fi

# 导出函数供其他脚本使用
export -f process_voice_message
export -f handle_inbound_voice
