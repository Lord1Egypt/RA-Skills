#!/bin/bash
# Memory Auto Manager 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"

echo "=== Memory Auto Manager 安装脚本 ==="

# 1. 创建必要目录
echo "[1/5] 创建目录..."
mkdir -p "$OPENCLAW_DIR/scripts"
mkdir -p "$MEMORY_DIR"

# 2. 复制扫描脚本
echo "[2/5] 复制扫描脚本..."
cp "$SCRIPT_DIR/memory-scan.py" "$OPENCLAW_DIR/scripts/memory-scan.py"
chmod +x "$OPENCLAW_DIR/scripts/memory-scan.py"

# 3. 初始化 scan-state.json
echo "[3/5] 初始化 scan-state.json..."
if [ ! -f "$MEMORY_DIR/scan-state.json" ]; then
    echo '{"last_scan_ts": 0}' > "$MEMORY_DIR/scan-state.json"
    echo "  已创建 scan-state.json"
else
    echo "  scan-state.json 已存在，跳过"
fi

# 4. 查找主会话 transcript
echo "[4/5] 查找主会话 transcript..."
TRANSCRIPT=$(ls -t "$OPENCLAW_DIR/agents/main/sessions/"*.jsonl 2>/dev/null | head -1)
if [ -n "$TRANSCRIPT" ]; then
    echo "  找到: $TRANSCRIPT"
    # 更新 memory-scan.py 中的路径
    sed -i.bak "s|5e9610e3-6282-4d8b-baeb-4ef78ff9e577.jsonl|$(basename "$TRANSCRIPT")|g" "$OPENCLAW_DIR/scripts/memory-scan.py"
    echo "  已更新脚本中的 transcript 路径"
else
    echo "  警告：未找到 transcript 文件，请在安装后手动配置"
fi

# 5. 创建 Memory自动检查 cron
echo "[5/5] 创建 Memory自动检查 cron..."
read -p "请提供你的飞书 user id (ou_xxx)，直接回车跳过：" USER_ID

if [ -n "$USER_ID" ]; then
    openclaw cron add \
        --name "Memory自动检查" \
        --every "15m" \
        --session isolated \
        --message "你是记忆管理员。执行memory扫描：
1. exec 运行：python3 ~/.openclaw/scripts/memory-scan.py
2. 读取输出的新消息内容（user + assistant）
3. 分析是否有重要信息（完成的任务/决策/教训/配置变更）
4. 有重要信息？→ 写入 memory/YYYY-MM-DD.md + 更新 last-memory-write.json
5. 输出：检查完成，写入X条/无新增

判断标准：
- 完成了什么（任务、里程碑）
- 确认了什么（方案、决策）
- 发现了什么（关键数据）
- 犯了什么错（教训、踩坑）
- 配置改了什么
- 有阻塞/待确认" \
        --tools "exec,read,write" \
        --no-deliver 2>/dev/null && echo "  cron 创建成功" || echo "  cron 创建失败，请手动创建"
else
    echo "  跳过 cron 创建，请手动创建："
    echo "  openclaw cron add --name 'Memory自动检查' --every '15m' --session isolated ..."
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "下一步："
echo "1. 确认 transcript 路径：cat ~/.openclaw/scripts/memory-scan.py | grep TRANSCRIPT"
echo "2. 测试脚本：python3 ~/.openclaw/scripts/memory-scan.py"
echo "3. 手动触发 cron 测试：openclaw cron list | grep Memory"
echo ""
