#!/bin/bash
# 1688 Sourcing Skill 依赖安装脚本
# 运行方式: bash scripts/setup.sh

echo "安装 1688 Sourcing Skill 依赖..."

pip install requests beautifulsoup4 --quiet

echo "依赖安装完成！"
