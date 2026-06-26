#!/bin/bash
# WeChat macOS Proxy 技能反馈检查脚本
# 每周五下午自动运行，生成反馈报告

SKILL_SLUG="wechat-macos-proxy"
REPORT_FILE="/tmp/wechat_proxy_weekly_report.txt"
DATE_STR=$(date '+%Y年%m月%d日')

cat > "$REPORT_FILE" << EOF
╔══════════════════════════════════════════════════════════════╗
║     📊 WeChat macOS Proxy 技能周度反馈报告                  ║
╠══════════════════════════════════════════════════════════════╣
║  日期: $DATE_STR（周五）                                      ║
╚══════════════════════════════════════════════════════════════╝

📌 技能信息
EOF

# 查询技能信息
echo "" >> "$REPORT_FILE"
echo "技能名称: WeChat macOS Proxy" >> "$REPORT_FILE"
echo "Slug: $SKILL_SLUG" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 尝试获取技能详情
echo "🔍 ClawHub 技能详情:" >> "$REPORT_FILE"
clawhub inspect "$SKILL_SLUG" 2>&1 >> "$REPORT_FILE" || echo "   获取失败（可能是 API 限制）" >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "📈 探索页面检查:" >> "$REPORT_FILE"
clawhub explore --limit 50 2>&1 | grep -A3 -B3 "$SKILL_SLUG" >> "$REPORT_FILE" || echo "   暂无数据或查询受限" >> "$REPORT_FILE"

cat >> "$REPORT_FILE" << EOF

💡 建议行动
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 手动访问 https://clawhub.ai/skills/$SKILL_SLUG 查看最新评论
2. 查看 GitHub 仓库 Issues（如有）
3. 根据用户反馈规划下版本功能

📝 反馈收集方式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ClawHub 页面评论区
- GitHub Issues（如有开源）
- 直接联系用户

下次检查: 下周五 17:00
EOF

# 发送报告（通过多种方式）
echo ""
echo "═══════════════════════════════════════════════════════════════"
cat "$REPORT_FILE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "报告已保存: $REPORT_FILE"

# 尝试通过 imsg 发送（如果配置了）
# imsg send ... 2>/dev/null || true

exit 0
