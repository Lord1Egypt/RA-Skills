---
version: 1.0.0
---

# SAR指标计算工具

**SAR（抛物线转向指标）计算工具，用于A股技术分析。**

## 功能说明

1. **获取股票K线数据** - 使用Baostock接口获取历史K线数据
2. **计算SAR值** - 抛物线转向指标计算
3. **判断SAR趋势** - 识别上涨/下跌趋势
4. **判断价格位置** - 判断收盘价是否在SAR上方/下方
5. **计算成交量比** - 今日成交量与5日均量的比值
6. **四维评分** - 从趋势、位置、成交量、动量四个维度评分

## 使用方法

```bash
# 查看帮助
python ~/.openclaw/workspace/skills/sar-calculator/sar_calculator.py --help

# 分析单只股票
python ~/.openclaw/workspace/skills/sar-calculator/sar_calculator.py --stock 600519

# 分析多只股票
python ~/.openclaw/workspace/skills/sar-calculator/sar_calculator.py --stock 600519 000858 300750

# 指定日期范围
python ~/.openclaw/workspace/skills/sar-calculator/sar_calculator.py --stock 600519 --start 2025-01-01 --end 2025-03-17

# 简短输出
python ~/.openclaw/workspace/skills/sar-calculator/sar_calculator.py --stock 600519 --quiet
```

## 安装依赖

```bash
pip install baostock pandas
```

## 评分维度说明

| 维度 | 分数范围 | 评分标准 |
|------|----------|----------|
| 趋势评分 | 0-25 | 上涨趋势=25，下跌趋势=0 |
| 位置评分 | 0-25 | 价格在SAR上方=25，下方=0 |
| 成交量评分 | 0-25 | 量比≥1.5=25，≥1.2=18，≥1.0=12，≥0.8=6，<0.8=0 |
| 动量评分 | 0-25 | 5日涨幅≥10%=25，≥5%=20，≥0%=15，≥-5%=8，<-5%=0 |

## 综合建议

- **总分 ≥ 75**: 强烈看多
- **总分 ≥ 50**: 谨慎看多  
- **总分 ≥ 25**: 谨慎看空
- **总分 < 25**: 强烈看空
