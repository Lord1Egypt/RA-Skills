#!/bin/bash
# 示例 0：首次使用初始化（必做！）
# 使用场景：新安装 skill 后，配置默认 agents

echo "=== Session Reset 示例：首次使用初始化 ==="
echo ""

echo "⚠️  首次使用前必须先执行初始化！"
echo ""

echo "[步骤 1] 运行初始化命令"
echo "命令：openclaw session-reset --init"
echo ""

# 显示交互式流程说明
echo "初始化流程："
echo "  1. 自动扫描 ~/.openclaw/ 发现所有 agents"
echo "  2. 交互选择："
echo "     [1] 导入全部 agents"
echo "     [2] 多选（自定义）"
echo "     [3] 取消"
echo "  3. 保存配置到 ~/.openclaw/session-reset-config.json"
echo ""

echo "[步骤 2] 验证配置"
echo "命令：openclaw session-reset --scope agents --dry-run"
echo ""

echo "[提示] 如需修改 agents 列表，重新运行 --init 即可"
echo ""

# 实际初始化（取消注释以运行）
# openclaw session-reset --init
