#!/bin/bash
# 日志分析系统启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 启动日志分析系统..."
echo ""
echo "📊 功能：纯本地日志文件分析，无需任何外部连接"
echo "🎯 特点："
echo "   - 直接读取本地日志文件"
echo "   - 日志统计和重复检测"
echo "   - 错误检测和异常分析"
echo "   - 时间分布和趋势分析"
echo ""
echo "🌐 访问地址：http://localhost:8506"
echo ""

# 启动 Streamlit（使用新端口避免冲突）
streamlit run log-analyzer.py --server.port 8506
