#!/bin/bash
# generate-lyrics.sh - 歌词生成脚本
# 用途：根据主题生成歌词 + 法律审查

set -e

THEME="$1"
OUTPUT_DIR="${OUTPUT_DIR:-/Users/huang/.openclaw/workspace/knowledge/video/daily-mv-tasks}"
DATE=$(date +%Y-%m-%d)

if [ -z "$THEME" ]; then
  echo "❌ 用法：./generate-lyrics.sh [主题]"
  echo "示例：./generate-lyrics.sh 油价上涨"
  exit 1
fi

echo "🎵 创作歌词：$THEME"

LYRICS_FILE="$OUTPUT_DIR/$DATE-lyrics-$THEME.md"

cat > "$LYRICS_FILE" << EOF
# 🎤 歌词创作 - $THEME

## 歌曲信息
- **主题**：$THEME
- **女主**：捌十肆（烟嗓）
- **风格**：（待确定）
- **时长**：1:30-2:00

## 歌词

### 主歌 1
（待填充）

### 副歌
（待填充）

### 主歌 2
（待填充）

### 副歌
（重复）

### 桥段
（待填充）

### 副歌（升调）
（重复）

## 法律审查

### 审查项
- [ ] 宪法合规
- [ ] 网络安全法
- [ ] 广告法（禁用"最""第一"等）
- [ ] 著作权法（原创性）
- [ ] 敏感单位/政府部门（禁止提及）

### 风险等级
🟢 低风险 / 🟡 中风险 / 🔴 高风险

### 审查结果
（待填充）

## Suno 提示词建议

```
[风格]，烟嗓女声，[情绪]，[节奏]，[乐器]
示例：Rock ballad, smoky female vocals, emotional, mid-tempo, electric guitar
```

---
*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
*下一步：运行 legal-check.sh 审查*
EOF

echo "✅ 歌词草稿完成"
echo "📄 文件：$LYRICS_FILE"
echo ""
echo "下一步："
echo "1. 编辑 $LYRICS_FILE 填写歌词"
echo "2. 运行：./legal-check.sh $LYRICS_FILE"
