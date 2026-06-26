#!/bin/bash
# generate-suno.sh - Suno 提示词生成脚本
# 用途：根据歌词风格生成适合捌十肆的 Suno 提示词

set -e

THEME="$1"
STYLE="$2"

if [ -z "$THEME" ]; then
  echo "❌ 用法：./generate-suno.sh [主题] [风格]"
  echo "风格选项：rock, pop, ballad, electronic, hiphop, folk"
  echo "示例：./generate-suno.sh 油价上涨 rock"
  exit 1
fi

STYLE=${STYLE:-"rock"}  # 默认摇滚风格

echo "🎵 生成 Suno 提示词"
echo "主题：$THEME"
echo "风格：$STYLE"
echo ""

# 风格映射
case $STYLE in
  rock)
    GENRE="Rock ballad"
    MOOD="emotional, powerful"
    TEMPO="mid-tempo, 80-100 BPM"
    INSTRUMENTS="electric guitar, drums, bass"
    ;;
  pop)
    GENRE="Pop"
    MOOD="catchy, uplifting"
    TEMPO="upbeat, 100-120 BPM"
    INSTRUMENTS="synthesizer, drums, piano"
    ;;
  ballad)
    GENRE="Ballad"
    MOOD="melancholic, introspective"
    TEMPO="slow, 60-80 BPM"
    INSTRUMENTS="piano, strings, acoustic guitar"
    ;;
  electronic)
    GENRE="Electronic"
    MOOD="energetic, futuristic"
    TEMPO="fast, 120-140 BPM"
    INSTRUMENTS="synthesizer, drum machine, bass"
    ;;
  hiphop)
    GENRE="Hip-hop"
    MOOD="confident, rhythmic"
    TEMPO="mid-tempo, 90-100 BPM"
    INSTRUMENTS="808 drums, bass, samples"
    ;;
  folk)
    GENRE="Folk"
    MOOD="warm, storytelling"
    TEMPO="mid-tempo, 80-100 BPM"
    INSTRUMENTS="acoustic guitar, harmonica, light percussion"
    ;;
  *)
    echo "❌ 未知风格：$STYLE"
    exit 1
    ;;
esac

echo "## Suno 提示词"
echo ""
echo "\`\`\`"
echo "$GENRE, smoky female vocals (Chinese), $MOOD, $TEMPO, $INSTRUMENTS, professional production, radio quality"
echo "\`\`\`"
echo ""
echo "## 中文提示词"
echo ""
echo "\`\`\`"
echo "$GENRE，烟嗓女声（中文），$MOOD，$TEMPO，$INSTRUMENTS，专业制作，电台音质"
echo "\`\`\`"
echo ""
echo "## 使用指南"
echo ""
echo "1. 登录 Suno.com"
echo "2. 选择 Custom Mode"
echo "3. 粘贴提示词到 Style 字段"
echo "4. 填写歌词到 Lyrics 字段"
echo "5. 点击 Create"
echo ""
echo "## 注意事项"
echo "- 账号：手机号 4454654118（美国区号 +1）"
echo "- 验证码：https://api.sms8.net/api/record?token=age41qfusk74s7g3po9sr2ljazq0omw4m3jz&format=json3"
echo "- 登录态有效期：7 天"
echo "- 如显示 50 积分无会员 → 清理历史记录（cookie）"
