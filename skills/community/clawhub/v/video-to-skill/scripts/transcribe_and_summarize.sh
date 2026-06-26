#!/bin/bash
# Step 3: Transcribe and summarize video content using MiniMax API
# Usage: ./transcribe_and_summarize.sh <subtitle_srt_or_audio_file> <output_dir>
set -e

INPUT_FILE="$1"
OUTPUT_DIR="${2:-/tmp}"
TRANSCRIPT_FILE="$OUTPUT_DIR/video_transcript.md"
SUMMARY_FILE="$OUTPUT_DIR/video_summary.md"
MINIMAX_API_KEY="${MINIMAX_API_KEY:-}"

if [ -z "$INPUT_FILE" ]; then
  echo "ERROR: input file is required"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "ERROR: file not found: $INPUT_FILE"
  exit 1
fi

if [ -z "$MINIMAX_API_KEY" ]; then
  echo "ERROR: MINIMAX_API_KEY is not set"
  exit 1
fi

echo "Transcribing and summarizing: $INPUT_FILE"

EXT="${INPUT_FILE##*.}"

if [ "$EXT" = "srt" ] || [ "$EXT" = "vtt" ] || [ "$EXT" = "txt" ]; then
  # 字幕文件直接读取并总结
  CONTENT=$(cat "$INPUT_FILE")
  
  # 调用 MiniMax LLM 生成摘要和文字稿
  RESPONSE=$(curl -s -X POST "https://api.minimax.chat/v1/chat/completions" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg system "你是一个视频内容分析助手。用户会提供视频字幕。请生成：1）完整文字稿（保留所有关键信息）；2）视频摘要（包含主题、关键要点、结论）。用中文输出。" \
      --arg content "【字幕内容】\n$CONTENT\n\n请生成：1) video_transcript_md：完整文字稿；2) video_summary_md：视频摘要（包含主题、主要内容、关键知识点、总结）。" \
      '{
        model: "MiniMax-Text-01",
        messages: [
          {role: "system", content: $system},
          {role: "user", content: $content}
        ],
        temperature: 0.3,
        max_tokens: 8000
      }')")
  
  USAGE=$(echo "$RESPONSE" | jq -r '.usage.total_tokens // empty')
  CHOICES=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty')
  
  if [ -z "$CHOICES" ]; then
    echo "ERROR: API call failed"
    echo "$RESPONSE"
    exit 1
  fi
  
  # 解析 LLM 输出，分离 transcript 和 summary
  # 假设格式：---TRANSCRIPT---...---SUMMARY---... 或直接输出两部分
  echo "$CHOICES" | awk '
    /^---TRANSCRIPT---$/ { mode=1; next }
    /^---SUMMARY---$/ { mode=2; next }
    mode==1 { transcript = transcript $0 "\n" }
    mode==2 { summary = summary $0 "\n" }
    BEGIN { mode=0 }
    END {
      gsub(/\n+$/, "", transcript)
      gsub(/\n+$/, "", summary)
      print transcript > "'"$TRANSCRIPT_FILE"'" 
      print summary > "'"$SUMMARY_FILE"'"
    }
  '
  
  # 如果 awk 解析失败（格式不匹配），直接写入原文
  if [ ! -s "$TRANSCRIPT_FILE" ]; then
    echo "$CHOICES" > "$TRANSCRIPT_FILE"
    echo "$CHOICES" > "$SUMMARY_FILE"
  fi
  
else
  # 音频文件需要先做语音识别
  echo "Transcribing audio file..."
  
  if [ "$EXT" = "mp3" ] || [ "$EXT" = "wav" ] || [ "$EXT" = "m4a" ] || [ "$EXT" = "aac" ]; then
    # 使用 MiniMax 语音识别 API
    RESPONSE=$(curl -s -X POST "https://api.minimax.chat/v1/audio/transcriptions" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      -F "file=@$INPUT_FILE" \
      -F "language=zh,en" \
      -F "response_format=json" \
      -F "temperature=0.3" \
      -F "max_tokens=8000")
    
    TEXT=$(echo "$RESPONSE" | jq -r '.text // .content // .result // empty')
    
    if [ -z "$TEXT" ]; then
      echo "ERROR: transcription failed"
      echo "$RESPONSE"
      exit 1
    fi
    
    echo "$TEXT" > "$TRANSCRIPT_FILE"
    
    # 总结
    SUMMARY_RESP=$(curl -s -X POST "https://api.minimax.chat/v1/chat/completions" \
      -H "Authorization: Bearer $MINIMAX_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$(jq -n \
        --arg content "【视频文字稿】\n$TEXT\n\n请生成视频摘要，包含：1）主题；2）主要内容/关键知识点；3）总结。JSON格式：{\"topic\": \"...\", \"key_points\": [\"...\"], \"summary\": \"...\"}" \
        '{
          model: "MiniMax-Text-01",
          messages: [{role: "user", content: $content}],
          temperature: 0.3,
          max_tokens: 2000
        }')")
    
    SUMMARY=$(echo "$SUMMARY_RESP" | jq -r '.choices[0].message.content // empty')
    echo "$SUMMARY" > "$SUMMARY_FILE"
  else
    echo "ERROR: unsupported file format: $EXT"
    exit 1
  fi
fi

echo "TRANSCRIPT_FILE=$TRANSCRIPT_FILE"
echo "SUMMARY_FILE=$SUMMARY_FILE"
