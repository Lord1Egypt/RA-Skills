#!/bin/bash

# After-Sales CLI 快捷脚本
# 用于快速访问售后管理功能

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$(dirname "$SCRIPT_DIR")/cli"
CLI_FILE="$CLI_DIR/after_sales_cli.js"

# 检查 CLI 文件是否存在
if [ ! -f "$CLI_FILE" ]; then
    echo "❌ 错误：CLI 文件不存在：$CLI_FILE"
    exit 1
fi

# 显示帮助信息
show_help() {
    echo ""
    echo "🔧 After-Sales CLI - 售后管理工具"
    echo ""
    echo "用法：$0 <模块> <命令> [选项]"
    echo ""
    echo "模块:"
    echo "  complaint      投诉管理"
    echo "  repeat-order   返单报价"
    echo "  satisfaction   满意度调查"
    echo "  analytics      分析报表"
    echo "  okki           OKKI 同步"
    echo ""
    echo "常用命令:"
    echo "  $0 complaint list                    # 列出所有投诉"
    echo "  $0 complaint create -n '客户名' -t quality -d '问题描述'"
    echo "  $0 complaint get CMP-xxx             # 查看投诉详情"
    echo "  $0 complaint stats                   # 投诉统计"
    echo ""
    echo "  $0 repeat-order list                 # 列出返单"
    echo "  $0 repeat-order create -n '客户名' -R 50000"
    echo "  $0 repeat-order get RO-xxx           # 查看返单详情"
    echo ""
    echo "  $0 satisfaction list                 # 列出满意度调查"
    echo "  $0 satisfaction stats                # 满意度统计"
    echo ""
    echo "  $0 analytics summary                 # 综合摘要报告"
    echo "  $0 analytics complaint               # 投诉分析"
    echo "  $0 analytics risk                    # 客户风险分析"
    echo ""
    echo "  $0 okki sync-complaint CMP-xxx       # 同步投诉到 OKKI"
    echo "  $0 okki logs                         # 查看同步日志"
    echo ""
    echo "完整帮助：$0 --help"
    echo ""
}

# 主逻辑
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

if [ "$1" = "--help" ] || [ "$1" = "-h" ] || [ "$1" = "help" ]; then
    show_help
    exit 0
fi

# 执行 CLI
node "$CLI_FILE" "$@"
