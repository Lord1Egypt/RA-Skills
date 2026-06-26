#!/bin/bash
# 定时任务配置脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$SCRIPT_DIR/../.."
CRON_FILE="$WORKSPACE_DIR/xianyu-crontab.txt"

echo "🐾 闲鱼数据抓取 - 定时任务配置"
echo "========================================"
echo ""

# 创建定时任务配置
cat > "$CRON_FILE" << 'EOF'
# 闲鱼数据抓取定时任务
# 格式：分 时 日 月 周 命令

# 每天上午 9 点 - 抓取核心关键词
0 9 * * * cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh grab "Magisk" "KernelSU" "救砖" "刷机" >> logs/xianyu-cron.log 2>&1

# 每周一上午 10 点 - 抓取所有关键词
0 10 * * 1 cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh grab-all >> logs/xianyu-cron.log 2>&1

# 每天下午 3 点 - 生成可视化报告
0 15 * * * cd ~/.openclaw/workspace && python3 skills/xianyu-data-grabber/visualize.py >> logs/xianyu-visualize.log 2>&1

# 每天晚上 8 点 - 生成智能推荐
0 20 * * * cd ~/.openclaw/workspace && python3 skills/xianyu-data-grabber/recommend.py >> logs/xianyu-recommend.log 2>&1

# 每周日下午 5 点 - 上传 Gitee（如有配置）
0 17 * * 0 cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh upload >> logs/xianyu-upload.log 2>&1

# 每天凌晨 2 点 - 清理临时文件
0 2 * * * cd ~/.openclaw/workspace && ./skills/xianyu-data-grabber/run.sh clean >> logs/xianyu-clean.log 2>&1
EOF

echo "✅ 定时任务配置已创建：$CRON_FILE"
echo ""
echo "📋 任务列表:"
echo "  1. 每天 09:00 - 抓取核心关键词（4 个）"
echo "  2. 每周一 10:00 - 抓取所有关键词（60+ 个）"
echo "  3. 每天 15:00 - 生成可视化报告"
echo "  4. 每天 20:00 - 生成智能推荐"
echo "  5. 每周日 17:00 - 上传 Gitee"
echo "  6. 每天 02:00 - 清理临时文件"
echo ""
echo "⚙️  安装到系统 crontab:"
echo ""
echo "方法 1: 手动安装"
echo "  crontab -e"
echo "  # 复制 $CRON_FILE 内容到编辑器"
echo ""
echo "方法 2: 自动安装"
echo "  crontab $CRON_FILE"
echo ""
echo "方法 3: 合并安装（推荐）"
echo "  crontab -l > /tmp/my-cron.txt 2>/dev/null || true"
echo "  cat $CRON_FILE >> /tmp/my-cron.txt"
echo "  crontab /tmp/my-cron.txt"
echo ""

# 检查是否已安装
if command -v crontab &> /dev/null; then
    echo "🔍 检查当前 crontab:"
    crontab -l 2>/dev/null | grep -c "xianyu" && echo "✅ 已安装闲鱼定时任务" || echo "⚠️  未安装闲鱼定时任务"
else
    echo "⚠️  crontab 未安装，跳过检查"
fi

echo ""
echo "📝 日志位置：~/.openclaw/workspace/logs/"
echo "  - xianyu-cron.log - 抓取日志"
echo "  - xianyu-visualize.log - 可视化日志"
echo "  - xianyu-recommend.log - 推荐日志"
echo "  - xianyu-upload.log - 上传日志"
echo "  - xianyu-clean.log - 清理日志"
echo ""
echo "========================================"
echo "👋 配置完成！"
