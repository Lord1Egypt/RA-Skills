#!/bin/bash
# skill-assessment 安装脚本

set -euo pipefail

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 开始安装 skill-assessment 技能${NC}"
echo ""

# 检查是否在技能目录中
if [ ! -f "SKILL.md" ]; then
    echo -e "${RED}错误：请在 skill-assessment 技能目录中运行此脚本${NC}"
    echo "cd /path/to/skill-assessment"
    echo "./install.sh"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖工具..."
missing_deps=0

for cmd in bash jq grep find; do
    if ! command -v "$cmd" &> /dev/null; then
        echo -e "  ${RED}✗ 缺少: $cmd${NC}"
        missing_deps=1
    else
        echo -e "  ${GREEN}✓ 已安装: $cmd${NC}"
    fi
done

if [ $missing_deps -eq 1 ]; then
    echo ""
    echo "请安装缺失的依赖："
    echo "  macOS: brew install jq"
    echo "  Ubuntu/Debian: sudo apt install jq"
    echo "  CentOS/RHEL: sudo yum install jq"
    exit 1
fi

# 设置执行权限
echo ""
echo "🔧 设置执行权限..."
chmod +x assess.sh
chmod +x evaluators/*.sh 2>/dev/null || true

echo -e "  ${GREEN}✓ assess.sh 已设置为可执行${NC}"
echo -e "  ${GREEN}✓ 评估器脚本已设置为可执行${NC}"

# 创建必要的目录
echo ""
echo "📁 创建目录结构..."
mkdir -p reports
mkdir -p examples
mkdir -p templates

echo -e "  ${GREEN}✓ 目录结构就绪${NC}"

# 检查配置
echo ""
echo "⚙️  检查配置文件..."
if [ ! -f "config.yaml" ]; then
    if [ -f "examples/config.example.yaml" ]; then
        cp examples/config.example.yaml config.yaml
        echo -e "  ${GREEN}✓ 已创建 config.yaml（从示例）${NC}"
    else
        echo -e "  ${YELLOW}⚠  未找到 config.yaml，使用默认配置${NC}"
    fi
else
    echo -e "  ${GREEN}✓ config.yaml 已存在${NC}"
fi

# 创建符号链接到技能目录
echo ""
echo "🔗 创建技能链接..."
SKILLS_DIR="${HOME}/.openclaw/skills"
if [ -d "$SKILLS_DIR" ]; then
    ln -sf "$(pwd)" "${SKILLS_DIR}/skill-assessment" 2>/dev/null || true
    echo -e "  ${GREEN}✓ 已链接到 ${SKILLS_DIR}/skill-assessment${NC}"
else
    echo -e "  ${YELLOW}⚠  未找到 ~/.openclaw/skills 目录${NC}"
    echo "  请确保 OpenClaw 已正确安装"
fi

# 测试安装
echo ""
echo "🧪 测试安装..."
if ./assess.sh --help &> /dev/null; then
    echo -e "  ${GREEN}✓ 主脚本运行正常${NC}"
else
    echo -e "  ${RED}✗ 主脚本运行失败${NC}"
    exit 1
fi

# 显示使用说明
echo ""
echo -e "${GREEN}🎉 安装完成！${NC}"
echo ""
echo "使用方式："
echo "  1. 评估单个技能："
echo "     ./assess.sh ~/.openclaw/skills/skill-creator"
echo ""
echo "  2. 评估当前目录："
echo "     ./assess.sh ."
echo ""
echo "  3. 查看帮助："
echo "     ./assess.sh --help"
echo ""
echo "  4. 安装到系统（可选）："
echo "     sudo ln -sf $(pwd)/assess.sh /usr/local/bin/skill-assess"
echo ""
echo "配置说明："
echo "  - 修改 config.yaml 调整评估权重"
echo "  - 查看 examples/ 目录获取示例"
echo "  - 报告保存在 reports/ 目录"
echo ""
echo "下一步："
echo "  尝试评估一个技能："
echo "    ./assess.sh ../skill-creator  # 如果相邻目录有技能"
echo ""
echo "问题反馈："
echo "  查看 SKILL.md 中的故障排除章节"