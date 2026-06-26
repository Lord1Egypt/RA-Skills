#!/bin/bash
# 統計套利 Skill 依賴安裝腳本

echo "📦 安裝統計套利 Skill 依賴..."

# 檢查 Python 版本
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python 版本: $python_version"

# 使用Python進行版本檢查
python3 -c "
import sys
major, minor = sys.version_info[:2]
if major < 3 or (major == 3 and minor < 8):
    print(f'需要 Python 3.8+，當前版本: {major}.{minor}')
    sys.exit(1)
else:
    print(f'Python 版本 {major}.{minor} 符合要求')
" || exit 1

# 檢查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3，請先安裝 pip"
    exit 1
fi

# 安裝依賴
echo "正在安裝 Python 套件..."
pip3 install yfinance pandas numpy statsmodels matplotlib --quiet

# 驗證安裝
echo "✅ 依賴安裝完成"
echo "驗證安裝:"
python3 -c "import yfinance, pandas, numpy, statsmodels, matplotlib; print('所有套件加載成功')"

# 創建測試配置
cat > test_config.json << EOF
{
  "stock1": "AAPL",
  "stock2": "GOOGL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "entry_threshold": 2.0,
  "exit_threshold": 0.5,
  "stop_loss": 3.5
}
EOF

echo ""
echo "🚀 安裝完成！"
echo "快速測試命令:"
echo "  python3 scripts/statistical_arbitrage.py --stock1 AAPL --stock2 GOOGL --start 2023-01-01 --end 2023-12-31"
echo ""
echo "在 OpenClaw 中使用方式:"
echo "  \"幫我分析 AAPL 和 GOOGL 的統計套利策略\""