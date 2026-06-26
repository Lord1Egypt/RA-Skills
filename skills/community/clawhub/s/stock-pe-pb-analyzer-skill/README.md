# 股票PE/PB历史水位分析器 📊

一个基于 BaoStock 数据源的股票估值分析工具，用于分析股票当前 PE（市盈率）、PB（市净率）在历史区间中的相对位置（水位）。

## ✨ 功能特点

- 🔍 **智能股票搜索**：支持通过股票名称（如：贵州茅台）或代码（如：600519）查询
- 📈 **多周期分析**：自动计算 10年、5年、3年、1年 的历史水位
- 🎯 **可视化评级**：
  - 🟢 **低估** (0-20%)：历史较低水平，可能存在估值修复机会
  - 🟡 **适中** (20-50%)：估值相对合理
  - 🔴 **偏高** (>50%)：估值偏高，需注意回调风险
- 📊 **详细统计**：提供最低、最高、中位数、平均值、标准差等指标
- 💾 **数据导出**：支持导出 CSV 格式历史数据和文本摘要

## 📦 安装

### 1. 克隆仓库

```bash
git clone https://github.com/caoyachao/stock-pe-pb-analyzer-skill.git
cd stock-pe-pb-analyzer-skill
```

### 2. 安装依赖

```bash
pip install baostock pandas numpy
```

## 🚀 使用方法

### 方式一：命令行直接调用

```bash
# 分析贵州茅台
python scripts/analyze_stock.py 贵州茅台

# 或按股票代码
python scripts/analyze_stock.py 600519
```

### 方式二：作为 Python 模块导入

```python
from scripts.analyze_stock import StockPEPBAnalyzer

# 创建分析器实例
analyzer = StockPEPBAnalyzer()

# 分析单只股票
result = analyzer.analyze("贵州茅台", years=10)

# 打印详细报告
analyzer.print_report(result)

# 获取原始数据
historical_data = result['historical_data']  # DataFrame 包含 date, peTTM, pbMRQ 等字段
percentiles = result['percentiles']  # 各周期水位计算结果

# 获取 10 年 PE 水位
pe_10y = result['percentiles']['periods']['10年']['pe']['percentile']
print(f"10年PE水位: {pe_10y:.1f}%")
```

## 📋 输出示例

```
📊 贵州茅台 (sh.600519) PE/PB历史水位分析报告
================================================================================

📈 当前估值指标:
   PE (TTM): 28.50
   PB (MRQ): 8.20

📉 历史水位分析（基于历史估值数据）:
--------------------------------------------------------------------------------
周期       数据点      PE当前        PE水位              PB当前        PB水位
--------------------------------------------------------------------------------
10年       2450        28.50        65.2% 🔴偏高        8.20         70.5% 🔴偏高
5年        1220        28.50        45.3% 🟡适中        8.20         55.2% 🔴偏高
3年        730         28.50        38.2% 🟡适中        8.20         48.5% 🟡适中
1年        245         28.50        42.1% 🟡适中        8.20         52.3% 🔴偏高
--------------------------------------------------------------------------------
水位说明: 🟢低估(0-20%) | 🟡适中(20-50%) | 🔴偏高(>50%)

📊 详细统计指标:

   【10年】
   PE - 最低: 15.20, 最高: 65.80, 中位数: 28.50, 平均: 30.20
   PB - 最低: 3.50, 最高: 18.20, 中位数: 8.00, 平均: 8.50

💡 参考建议:

   基于PE/PB综合水位分析:
   • 当前PE/PB综合水位为 67.9%，处于历史较高水平
   • 估值较高，需注意估值回调风险

   分项分析:
   • PE水位65.2%：市盈率处于历史偏高位置
   • PB水位70.5%：市净率处于历史高位

================================================================================
⚠️ 免责声明：本分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。
================================================================================
```

## 🏗️ 项目结构

```
stock-pe-pb-analyzer-skill/
├── README.md                 # 项目说明文档
├── SKILL.md                  # OpenClaw Skill 元数据
└── scripts/
    └── analyze_stock.py      # 核心分析脚本
```

## 📊 数据来源

- **数据提供商**: [BaoStock](http://www.baostock.com/) - 免费开源的证券数据平台
- **数据类型**: 沪深A股日频估值数据
- **估值指标**: PE-TTM（滚动市盈率）、PB-MRQ（市净率）、PS-TTM、PCF-TTM

## ⚠️ 注意事项

1. **首次使用**: 会自动登录 BaoStock 并加载股票列表，可能需要几秒时间
2. **数据质量**: 过滤了 PE > 1000 的异常数据点
3. **使用限制**: BaoStock 有访问频率限制，大批量查询请适当添加延迟
4. **免责声明**: 本分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。

## 🔧 作为 OpenClaw Skill 使用
对话安装
```
安装skill: https://github.com/caoyachao/stock-pe-pb-analyzer-skill
```

或将此仓库克隆到 OpenClaw 的 skills 目录：

```bash
mkdir -p ~/.config/agents/skills/
cd ~/.config/agents/skills/
git clone https://github.com/caoyachao/stock-pe-pb-analyzer-skill.git stock-pe-pb-analyzer
```

然后对话调用：
```
分析贵州茅台估值水位
```

## 📝 License

MIT License

## 👤 作者

- GitHub: [@caoyachao](https://github.com/caoyachao)

## 🙏 致谢

- [BaoStock](http://www.baostock.com/) 提供免费的股票数据支持
