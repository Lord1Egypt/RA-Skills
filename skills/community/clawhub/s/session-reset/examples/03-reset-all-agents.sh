#!/bin/bash
# 示例 3：批量重置六部+秘书
# 使用场景：团队配置大规模更新后

echo "=== Session Reset 示例：批量重置六部+秘书 ==="
echo ""

echo "六部+秘书列表："
echo "  - main (秘书/BinClaw)"
echo "  - gongbu (工部/小工)"
echo "  - bingbu (兵部/小兵)"
echo "  - hubu (户部/小户)"
echo "  - libu (礼部/小礼)"
echo "  - xingbu (刑部/小刑)"
echo "  - libu_hr (吏部/小吏)"
echo ""

# 步骤 1：预览
echo "[步骤 1] 预览将要重置的六部+秘书 sessions..."
openclaw session-reset --scope agents --dry-run

echo ""
echo "[步骤 2] 确认后执行批量重置"
echo "命令：openclaw session-reset --scope agents"
echo ""

# 步骤 2：实际执行（取消注释以运行）
# openclaw session-reset --scope agents

echo "[提示] 重置完成后，下次 @mention 各 agent 时将创建新 session，加载最新配置。"
