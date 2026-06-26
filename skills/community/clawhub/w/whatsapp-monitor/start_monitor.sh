#!/usr/bin/env bash
# WhatsApp Monitor - interactive launcher (Linux/macOS)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "WhatsApp Monitor Skill - 启动脚本"
echo

if command -v python3 &>/dev/null; then
  PYTHON=python3
elif command -v python &>/dev/null; then
  PYTHON=python
else
  echo "错误: 未找到 Python，请先安装 Python 3.8+"
  exit 1
fi

if ! "${PYTHON}" --version &>/dev/null; then
  echo "错误: 未找到 Python，请先安装 Python 3.8+"
  exit 1
fi

if [[ ! -f requirements.txt ]]; then
  echo "错误: requirements.txt 文件不存在"
  exit 1
fi

if ! "${PYTHON}" -c "import aiohttp" &>/dev/null; then
  echo "安装依赖中..."
  if ! "${PYTHON}" -m pip install -r requirements.txt; then
    echo "错误: 依赖安装失败"
    exit 1
  fi
fi

mkdir -p config
if [[ ! -f config/whatsapp-targets.json ]] || [[ ! -f config/feishu-settings.json ]]; then
  echo "创建默认配置文件..."
  "${PYTHON}" scripts/setup.py
fi

echo
echo "请按需编辑配置文件:"
echo "1. config/whatsapp-targets.json - WhatsApp 监控目标配置"
echo "2. config/feishu-settings.json  - 飞书集成配置"
echo

read -r -p "选择操作: [1]测试配置 [2]启动监控 [3]查看状态 [4]强制导出: " choice

case "${choice}" in
  1)
    echo "测试配置..."
    "${PYTHON}" scripts/monitor.py --test-config
    ;;
  2)
    echo "启动监控..."
    "${PYTHON}" scripts/monitor.py --start
    ;;
  3)
    echo "查看状态..."
    "${PYTHON}" scripts/monitor.py --status
    ;;
  4)
    echo "强制导出..."
    "${PYTHON}" scripts/monitor.py --export
    ;;
  *)
    echo "无效选择"
    ;;
esac

echo
read -r -p "按回车键退出"
