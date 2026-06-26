---
name: stock-pe-pb-analyzer
description: 分析股票PE/PB历史水位的专业工具。使用BaoStock API获取真实股票数据，计算股票在过去十年中的PE、PB历史百分位水位。适用于：1）查询单个股票的PE/PB历史估值水平；2）评估当前估值相对于历史的高低位置；3）为投资决策提供估值参考数据。支持通过股票名称（如贵州茅台）或代码（如600519）查询A股所有股票。
---

# 股票PE/PB历史水位分析器

基于BaoStock数据源的股票估值分析工具，帮助分析股票当前PE、PB在历史区间中的位置（水位）。

## 功能特点

- 支持股票名称和代码查询
- 自动计算10年、5年、3年、1年的历史水位
- 提供详细的统计指标（最低、最高、中位数、平均值）
- 输出估值评级（低估/适中/偏高）

## 使用方法

### 1. 直接调用分析脚本

```python
# 执行分析脚本
python .agents/skills/stock-pe-pb-analyzer/scripts/analyze_stock.py <股票名称或代码>
```

示例：
```bash
python .agents/skills/stock-pe-pb-analyzer/scripts/analyze_stock.py 贵州茅台
python .agents/skills/stock-pe-pb-analyzer/scripts/analyze_stock.py 600519
```

### 2. 作为Python模块使用

```python
from .agents.skills.stock-pe-pb-analyzer.scripts.analyze_stock import StockPEPBAnalyzer

# 创建分析器实例
analyzer = StockPEPBAnalyzer()

# 分析单只股票
result = analyzer.analyze("贵州茅台", years=10)

# 打印详细报告
analyzer.print_report(result)

# 获取原始数据
historical_data = result['historical_data']  # DataFrame包含date, peTTM, pbMRQ等字段
percentiles = result['percentiles']  # 各周期水位计算结果
```

## 输出说明

- **PE水位**: 当前PE在过去N年中的百分位（0%-100%）
  - 🔴 低估: 0-20%（历史较低水平，可能存在估值修复机会）
  - 🟡 适中: 20-50%（估值相对合理）
  - 🟢 偏高: >50%（估值偏高，需注意风险）

- **PB水位**: 当前PB在过去N年中的百分位，评级标准同上

## 依赖要求

需要安装以下Python包：
- baostock
- pandas
- numpy

## 注意事项

1. 首次使用时会自动登录BaoStock并加载股票列表
2. 数据基于日频估值指标（PE-TTM, PB-MRQ）
3. 过滤了PE>1000的异常数据点
4. 分析结果仅供参考，不构成投资建议
