#!/bin/bash
# 一键配置脚本
# 自动配置 self-evolution-cn 技能

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

log_info() {
    echo -e "${GREEN}[信息]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

log_error() {
    echo -e "${RED}[错误]${NC} $1" >&2
}

log_step() {
    echo -e "${BLUE}[步骤]${NC} $1"
}

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 默认配置
SHARED_LEARNING_DIR="${SHARED_LEARNING_DIR:-/root/.openclaw/shared-learning}"
OPENCLAW_DIR="${OPENCLAW_DIR:-/root/.openclaw}"

log_info "开始配置 self-evolution-cn 技能..."
echo ""

# 步骤 1：检查 OpenClaw 安装
log_step "1. 检查 OpenClaw 安装..."
if ! command -v openclaw &> /dev/null; then
    log_error "未找到 OpenClaw。请先安装 OpenClaw。"
    exit 1
fi
log_info "OpenClaw 已安装：$(openclaw --version)"
echo ""

# 步骤 2：创建共享目录
log_step "2. 创建共享目录..."
mkdir -p "$SHARED_LEARNING_DIR"
mkdir -p "$SKILL_DIR/logs"
log_info "共享目录：$SHARED_LEARNING_DIR"
log_info "日志目录：$SKILL_DIR/logs"
echo ""

# 步骤 2.5：设置脚本执行权限
log_step "2.5. 设置脚本执行权限..."
chmod +x "$SCRIPT_DIR"/*.sh
log_info "脚本执行权限已设置"
echo ""

# 步骤 3：初始化状态文件
log_step "3. 初始化状态文件..."
if [ ! -f "$SKILL_DIR/heartbeat-state.json" ]; then
    echo '{"agents":{}}' > "$SKILL_DIR/heartbeat-state.json"
    log_info "状态文件已创建：$SKILL_DIR/heartbeat-state.json"
else
    log_info "状态文件已存在：$SKILL_DIR/heartbeat-state.json"
fi
echo ""

# 步骤 4：复制模板文件到共享目录
log_step "4. 复制模板文件到共享目录..."
cp "$SKILL_DIR/.learnings/ERRORS.md" "$SHARED_LEARNING_DIR/"
cp "$SKILL_DIR/.learnings/LEARNINGS.md" "$SHARED_LEARNING_DIR/"
cp "$SKILL_DIR/.learnings/FEATURE_REQUESTS.md" "$SHARED_LEARNING_DIR/"
log_info "模板文件已复制到共享目录"
echo ""

# 步骤 5：遍历所有 agent 工作区
log_step "5. 配置所有 agent 工作区..."

# 默认共享的 agent（主 agent）
DEFAULT_AGENTS="workspace-agent1"

# 从环境变量获取需要共享的 agent 列表
SHARED_AGENTS="${SHARED_AGENTS:-$DEFAULT_AGENTS}"

# 将空格分隔的列表转换为数组
IFS=' ' read -ra SHARED_AGENT_ARRAY <<< "$SHARED_AGENTS"

log_info "需要共享的 agent：$SHARED_AGENTS"
echo ""

# 遍历所有 workspace-* 目录
for agent_dir in "$OPENCLAW_DIR"/workspace-*; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename "$agent_dir")
        learnings_path="$agent_dir/.learnings"

        # 检查是否需要共享
        is_shared=false
        for shared_agent in "${SHARED_AGENT_ARRAY[@]}"; do
            if [ "$shared_agent" = "$agent_name" ]; then
                is_shared=true
                break
            fi
        done

        if [ "$is_shared" = true ]; then
            # 需要共享：创建软链接
            log_info "配置共享 agent：$agent_name"

            # 如果存在软链接，删除重建
            if [ -L "$learnings_path" ]; then
                rm -f "$learnings_path"
                log_info "  删除旧软链接"
            fi

            # 如果存在目录，先备份
            if [ -d "$learnings_path" ]; then
                backup_path="$learnings_path.backup.$(date +%Y%m%d%H%M%S)"
                mv "$learnings_path" "$backup_path"
                log_info "  备份现有目录到：$backup_path"
            fi

            # 创建软链接
            ln -s "$SHARED_LEARNING_DIR" "$learnings_path"
            log_info "  创建软链接：$learnings_path → $SHARED_LEARNING_DIR"
        else
            # 不需要共享：创建独立目录
            log_info "配置独立 agent：$agent_name"

            # 如果存在软链接，删除
            if [ -L "$learnings_path" ]; then
                rm -f "$learnings_path"
                log_info "  删除旧软链接"
            fi

            # 如果存在目录，先备份
            if [ -d "$learnings_path" ]; then
                backup_path="$learnings_path.backup.$(date +%Y%m%d%H%M%S)"
                mv "$learnings_path" "$backup_path"
                log_info "  备份现有目录到：$backup_path"
            fi

            # 创建独立目录
            mkdir -p "$learnings_path"
            log_info "  创建独立目录：$learnings_path"

            # 复制模板文件
            cp "$SKILL_DIR/.learnings/ERRORS.md" "$learnings_path/"
            cp "$SKILL_DIR/.learnings/LEARNINGS.md" "$learnings_path/"
            cp "$SKILL_DIR/.learnings/FEATURE_REQUESTS.md" "$learnings_path/"
            log_info "  复制模板文件到独立目录"
        fi
    fi
done
echo ""

# 步骤 6：配置 hook
log_step "6. 配置 hook..."
HOOK_DIR="$OPENCLAW_DIR/hooks/self-evolution-cn"
if [ -d "$HOOK_DIR" ]; then
    rm -rf "$HOOK_DIR"
    log_info "  删除旧 hook 目录"
fi
cp -r "$SKILL_DIR/hooks/openclaw" "$HOOK_DIR"
log_info "Hook 已复制到：$HOOK_DIR"

# 启用 hook
if openclaw hooks enable self-evolution-cn 2>/dev/null; then
    log_info "Hook 已启用"
else
    log_warn "Hook 启用失败，可能需要手动启用"
fi
echo ""

# 步骤 7：设置 cron 任务
log_step "7. 设置 cron 任务..."
LOG_FILE="$SKILL_DIR/logs/heartbeat-daily.log"
CRON_JOB="0 0 * * * $SCRIPT_DIR/trigger-daily-review.sh >> $LOG_FILE 2>&1"

# 删除旧的 cron 任务
crontab -l 2>/dev/null | grep -v "trigger-daily-review.sh" | crontab -
log_info "  删除旧 cron 任务"

# 添加新的 cron 任务
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
log_info "Cron 任务已添加"
echo ""

# 步骤 8：验证配置
log_step "8. 验证配置..."
echo ""

# 检查共享目录
if [ -d "$SHARED_LEARNING_DIR" ]; then
    log_info "✓ 共享目录存在：$SHARED_LEARNING_DIR"
else
    log_error "✗ 共享目录不存在：$SHARED_LEARNING_DIR"
fi

# 检查模板文件
if [ -f "$SHARED_LEARNING_DIR/ERRORS.md" ] && [ -f "$SHARED_LEARNING_DIR/LEARNINGS.md" ] && [ -f "$SHARED_LEARNING_DIR/FEATURE_REQUESTS.md" ]; then
    log_info "✓ 共享目录模板文件存在"
else
    log_error "✗ 共享目录模板文件缺失"
fi

# 检查所有 agent 的配置
for agent_dir in "$OPENCLAW_DIR"/workspace-*; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename "$agent_dir")
        learnings_path="$agent_dir/.learnings"

        # 检查是否需要共享
        is_shared=false
        for shared_agent in "${SHARED_AGENT_ARRAY[@]}"; do
            if [ "$shared_agent" = "$agent_name" ]; then
                is_shared=true
                break
            fi
        done

        if [ "$is_shared" = true ]; then
            # 检查软链接
            if [ -L "$learnings_path" ]; then
                log_info "✓ 软链接存在：$agent_name/.learnings"
            else
                log_error "✗ 软链接不存在：$agent_name/.learnings"
            fi
        else
            # 检查独立目录
            if [ -d "$learnings_path" ]; then
                if [ -f "$learnings_path/ERRORS.md" ] && [ -f "$learnings_path/LEARNINGS.md" ] && [ -f "$learnings_path/FEATURE_REQUESTS.md" ]; then
                    log_info "✓ 独立目录存在：$agent_name/.learnings"
                else
                    log_error "✗ 独立目录文件缺失：$agent_name/.learnings"
                fi
            else
                log_error "✗ 独立目录不存在：$agent_name/.learnings"
            fi
        fi
    fi
done

# 检查 hook
if openclaw hooks list 2>/dev/null | grep -q "self-evolution-cn"; then
    log_info "✓ Hook 已启用"
else
    log_warn "✗ Hook 未启用"
fi

# 检查 cron
if crontab -l 2>/dev/null | grep -q "trigger-daily-review.sh"; then
    log_info "✓ Cron 任务已设置"
else
    log_warn "✗ Cron 任务未设置"
fi

echo ""
log_info "配置完成！"
echo ""
echo "下一步："
echo "  1. 测试技能：在对话中说'执行日检查'"
echo "  2. 查看学习记录：cat $SHARED_LEARNING_DIR/ERRORS.md"
echo "  3. 手动触发检查：bash $SCRIPT_DIR/daily_review.sh"
echo ""
echo "配置其他 agent："
echo "  export SHARED_AGENTS=\"workspace-agent1 workspace-agent2 workspace-agent3\""
echo "  ./scripts/setup.sh"
echo ""
echo "环境变量："
echo "  export SHARED_LEARNING_DIR=\"$SHARED_LEARNING_DIR\""
echo "  export SHARED_AGENTS=\"$SHARED_AGENTS\""
echo ""
