#!/bin/bash
# Amazon Movers & Shakers Skill 依赖安装脚本
# 运行方式: bash scripts/setup.sh

echo "安装 Amazon Movers & Shakers Skill 依赖..."

# 核心依赖（必需）
pip install requests --quiet

# 可选依赖（用于 HTML 解析）
pip install beautifulsoup4 --quiet

echo "依赖安装完成！"
echo ""
echo "可选配置："
echo "  export SELLERSPRITE_API_KEY='your_api_key'  # 配置卖家精灵 API"
