#!/bin/bash
# publish-video.sh - 一键发布脚本
# 用途：发布视频到 B 站/抖音/YouTube/视频号

set -e

VIDEO_FILE="$1"
TITLE="$2"
DESCRIPTION="$3"
TAGS="$4"

if [ -z "$VIDEO_FILE" ] || [ -z "$TITLE" ]; then
  echo "❌ 用法：./publish-video.sh [视频文件] [标题] [描述] [标签]"
  echo "示例：./publish-video.sh /path/to/video.mp4 \"油价狂飙\" \"幽默讽刺 MV\" \"油价，通胀，搞钱\""
  exit 1
fi

TAGS=${TAGS:-"MV,音乐，热点"}

echo "📤 发布视频"
echo "文件：$VIDEO_FILE"
echo "标题：$TITLE"
echo "描述：$DESCRIPTION"
echo "标签：$TAGS"
echo ""

# 检查文件是否存在
if [ ! -f "$VIDEO_FILE" ]; then
  echo "❌ 视频文件不存在：$VIDEO_FILE"
  exit 1
fi

# 获取文件大小
FILE_SIZE=$(stat -f%z "$VIDEO_FILE" 2>/dev/null || stat -c%s "$VIDEO_FILE" 2>/dev/null)
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))
echo "文件大小：${FILE_SIZE_MB}MB"
echo ""

# 发布到各平台
echo "## 发布状态"
echo ""

# B 站
echo "### B 站（我叫捌十肆）"
echo "- 状态：待发布"
echo "- 工具：bilibili-upload"
echo "- 命令：bilibili-upload --file \"$VIDEO_FILE\" --title \"$TITLE\" --desc \"$DESCRIPTION\" --tags \"$TAGS\""
echo ""

# 抖音
echo "### 抖音"
echo "- 状态：待发布"
echo "- 工具：新榜小豆芽（需登录态）"
echo "- 手动上传：打开抖音 APP → 上传 → 填写信息"
echo ""

# YouTube
echo "### YouTube"
echo "- 状态：待发布"
echo "- 工具：youtube-publisher（需 OAuth 配置）"
echo "- 账号：dahuang8426@gmail.com / dahuang8426@126.com"
echo "- 命令：youtube-publisher --file \"$VIDEO_FILE\" --title \"$TITLE\" --desc \"$DESCRIPTION\" --tags \"$TAGS\""
echo ""

# 视频号
echo "### 视频号"
echo "- 状态：待发布"
echo "- 工具：浏览器自动化（需保持登录）"
echo "- 手动上传：打开视频号 → 上传 → 填写信息"
echo ""

# 生成发布清单
CHECKLIST_FILE="/Users/huang/.openclaw/workspace/knowledge/video/daily-mv-tasks/$(date +%Y-%m-%d)-publish-checklist.md"

cat > "$CHECKLIST_FILE" << EOF
# 📤 发布清单 - $TITLE

## 视频信息
- 文件：$VIDEO_FILE (${FILE_SIZE_MB}MB)
- 标题：$TITLE
- 描述：$DESCRIPTION
- 标签：$TAGS

## 发布状态

| 平台 | 状态 | 工具 | 备注 |
|------|------|------|------|
| B 站 | ⏳ 待发布 | bilibili-upload | 账号：我叫捌十肆 |
| 抖音 | ⏳ 待发布 | 新榜小豆芽 | 需登录态 |
| YouTube | ⏳ 待发布 | youtube-publisher | 需 OAuth |
| 视频号 | ⏳ 待发布 | 手动 | 微信生态 |

## 发布后检查
- [ ] 播放量正常（>100/24h）
- [ ] 评论开启
- [ ] 弹幕开启（B 站）
- [ ] 收益监控开启

---
*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*
EOF

echo "✅ 发布清单生成完成"
echo "📄 文件：$CHECKLIST_FILE"
echo ""
echo "下一步："
echo "1. 按清单逐个平台发布"
echo "2. 发布后更新状态"
echo "3. 运行：./monitor-revenue.sh 监控收益"
