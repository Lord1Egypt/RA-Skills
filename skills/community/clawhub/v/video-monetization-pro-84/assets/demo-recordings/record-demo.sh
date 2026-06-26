#!/bin/bash
# 演示视频录制脚本

OUTPUT_DIR="/Users/huang/.openclaw/workspace/skills/video-monetization-pro/assets/demo-recordings"
SKILLS_DIR="/Users/huang/.openclaw/workspace/skills/video-monetization-pro"

echo "🎬 开始录制演示视频..."

# 录制片段 1：热点分析
echo "录制片段 1：热点分析..."
cd "$SKILLS_DIR"
./scripts/analyze-trends.sh > "$OUTPUT_DIR/01-analyze-trends.txt" 2>&1

# 录制片段 2：歌词生成
echo "录制片段 2：歌词生成..."
./scripts/generate-lyrics.sh 油价狂飙 > "$OUTPUT_DIR/02-generate-lyrics.txt" 2>&1

# 录制片段 3：Suno 提示词
echo "录制片段 3：Suno 提示词..."
./scripts/generate-suno.sh 油价狂飙 rock > "$OUTPUT_DIR/03-suno-prompt.txt" 2>&1

# 录制片段 4：分镜脚本
echo "录制片段 4：分镜脚本..."
./scripts/create-storyboard.sh 油价狂飙 > "$OUTPUT_DIR/04-storyboard.txt" 2>&1

# 录制片段 5：收益监控
echo "录制片段 5：收益监控..."
./scripts/monitor-revenue.sh > "$OUTPUT_DIR/05-revenue-report.txt" 2>&1

echo "✅ 所有片段录制完成！"
echo "输出目录：$OUTPUT_DIR"
ls -la "$OUTPUT_DIR"/*.txt
