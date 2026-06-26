#!/bin/bash
# Session Guardian 一键安装脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Session Guardian 🛡️  - 对话守护者                  ║"
echo "║                                                            ║"
echo "║  三层防护：增量备份 + 快照 + 智能总结                        ║"
echo "║  零 Token 成本 | 不影响主对话 | 一键恢复                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检查目录
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE_DIR="$(cd "$SKILL_DIR/../.." && pwd)"

echo "📂 检测到的路径："
echo "   Skill 目录: $SKILL_DIR"
echo "   Workspace: $WORKSPACE_DIR"
echo ""

# 加载配置
source "$SKILL_DIR/scripts/config.sh"

# 创建备份目录
echo "📁 创建备份目录..."
mkdir -p "$BACKUP_ROOT"/{incremental,hourly,daily}
echo -e "${GREEN}✅ 备份目录已创建: $BACKUP_ROOT${NC}"
echo ""

# 赋予执行权限
echo "🔧 设置脚本权限..."
chmod +x "$SKILL_DIR/scripts"/*.sh
echo -e "${GREEN}✅ 脚本权限已设置${NC}"
echo ""

# 测试增量备份
echo "🧪 测试增量备份..."
if bash "$SKILL_DIR/scripts/incremental-backup.sh"; then
    echo -e "${GREEN}✅ 增量备份测试通过${NC}"
else
    echo -e "${RED}❌ 增量备份测试失败${NC}"
    exit 1
fi
echo ""

# 测试快照
echo "🧪 测试快照备份..."
if bash "$SKILL_DIR/scripts/hourly-snapshot.sh"; then
    echo -e "${GREEN}✅ 快照备份测试通过${NC}"
else
    echo -e "${RED}❌ 快照备份测试失败${NC}"
    exit 1
fi
echo ""

# 显示当前 crontab
echo "📋 当前系统定时任务："
crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" || echo "   (无)"
echo ""

# 询问是否添加 crontab
echo "❓ 是否添加系统定时任务（增量备份 + 快照）？"
echo "   这将修改你的 crontab 配置"
read -p "   输入 y 继续，n 跳过: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 备份现有 crontab
    crontab -l > /tmp/crontab.backup 2>/dev/null || true
    
    # 添加新任务
    (crontab -l 2>/dev/null || true; cat << EOF

# Session Guardian - 对话守护者
# 增量备份（每5分钟）
*/$INCREMENTAL_INTERVAL * * * * bash "$SKILL_DIR/scripts/incremental-backup.sh" >> "$LOG_FILE" 2>&1

# 快照（每小时）
0 */$HOURLY_INTERVAL * * * bash "$SKILL_DIR/scripts/hourly-snapshot.sh" >> "$LOG_FILE" 2>&1
EOF
    ) | crontab -
    
    echo -e "${GREEN}✅ 系统定时任务已添加${NC}"
    echo "   增量备份: 每 $INCREMENTAL_INTERVAL 分钟"
    echo "   快照备份: 每 $HOURLY_INTERVAL 小时"
else
    echo -e "${YELLOW}⏭️  跳过系统定时任务配置${NC}"
    echo "   你可以稍后手动添加："
    echo "   crontab -e"
fi
echo ""

# 询问是否添加 OpenClaw cron
echo "❓ 是否添加 OpenClaw 定时任务（每日智能总结）？"
echo "   这将使用 LLM 生成每日对话总结"
read -p "   输入 y 继续，n 跳过: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 检查 OpenClaw 是否运行
    if ! openclaw status > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  OpenClaw Gateway 未运行${NC}"
        echo "   请先启动 Gateway: openclaw gateway"
        echo ""
    else
        # 构建 OpenClaw cron 命令
        CRON_CMD="openclaw cron add \
  --name \"Session Guardian 每日总结\" \
  --cron \"$DAILY_SUMMARY_CRON\" \
  --tz \"$TIMEZONE\" \
  --session isolated \
  --message \"$SUMMARY_PROMPT_TEMPLATE\" \
  --model \"$SUMMARY_MODEL\""
        
        # 如果启用推送，添加推送参数
        if [ "$DELIVERY_ENABLED" = true ]; then
            if [ "$DELIVERY_CHANNEL" = "last" ]; then
                # 使用 last 渠道，自动路由到用户最后使用的渠道
                CRON_CMD="$CRON_CMD --announce"
            else
                # 指定渠道和目标
                CRON_CMD="$CRON_CMD \
  --announce \
  --channel \"$DELIVERY_CHANNEL\""
                
                # 如果有目标，添加 --to
                if [ -n "$DELIVERY_TARGET" ]; then
                    CRON_CMD="$CRON_CMD \
  --to \"$DELIVERY_TARGET\""
                fi
            fi
        else
            CRON_CMD="$CRON_CMD --no-deliver"
        fi
        
        # 执行命令
        if eval "$CRON_CMD"; then
            echo "✅ OpenClaw 定时任务已添加"
            echo "   执行时间: $DAILY_SUMMARY_CRON ($TIMEZONE)"
            echo "   使用模型: $SUMMARY_MODEL"
            if [ "$DELIVERY_ENABLED" = true ]; then
                if [ "$DELIVERY_CHANNEL" = "last" ]; then
                    echo "   推送渠道: 自动（用户最后使用的渠道）"
                else
                    echo "   推送渠道: $DELIVERY_CHANNEL"
                fi
            fi
        else
            echo -e "${RED}❌ OpenClaw 定时任务添加失败${NC}"
        fi
    fi
else
    echo -e "${YELLOW}⏭️  跳过 OpenClaw 定时任务配置${NC}"
    echo "   你可以稍后手动添加："
    echo "   openclaw cron add --name \"每日总结\" --cron \"0 2 * * *\" --session isolated --message \"总结今天对话\" --model \"qwen-max\" --announce"
fi
echo ""

# 显示安装总结
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    🎉 安装完成！                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 备份配置："
echo "   增量备份: 每 $INCREMENTAL_INTERVAL 分钟"
echo "   快照备份: 每 $HOURLY_INTERVAL 小时"
echo "   每日总结: $DAILY_SUMMARY_CRON ($TIMEZONE)"
echo ""
echo "📁 备份位置："
echo "   $BACKUP_ROOT"
echo ""
echo "🔍 查看备份："
echo "   ls -lh $BACKUP_ROOT/incremental/"
echo "   ls -lh $BACKUP_ROOT/hourly/"
echo "   ls -lh $BACKUP_ROOT/daily/"
echo ""
echo "📝 查看日志："
echo "   tail -f $LOG_FILE"
echo ""
echo "🔄 恢复数据："
echo "   bash $SKILL_DIR/scripts/restore.sh --help"
echo ""
echo "⚙️  修改配置："
echo "   vim $SKILL_DIR/scripts/config.sh"
echo ""
echo "💡 提示："
echo "   - 增量备份和快照是纯脚本，不消耗 Token"
echo "   - 每日总结使用 LLM，建议使用阿里云 qwen-max（便宜）"
echo "   - 备份不影响主对话，完全独立运行"
echo ""
echo "📚 完整文档："
echo "   cat $SKILL_DIR/SKILL.md"
echo ""
