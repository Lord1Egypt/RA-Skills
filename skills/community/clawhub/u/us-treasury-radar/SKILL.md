# US Treasury Radar - 美债需求监测表

## 触发词
- 美债分析
- 美债雷达
- 浑水报告
- Muddy Waters
- US Treasury analysis
- 戴维期双杀

## 功能
实时获取美国国债供需数据，生成"浑水风险雷达"报告，检测"戴维期双杀"信号。

## 数据来源

### 1. 美债总量
- **来源**: TreasuryDirect.gov API
- **URL**: https://www.treasurydirect.gov/NP_WS/debt/current
- **频率**: 每日更新

### 2. 美联储持有
- **来源**: TreasuryDirect.gov API (Fed Securities Holdings)
- **URL**: https://www.treasurydirect.gov/NP_WS/feddata/current
- **频率**: 每日更新

### 3. 各国持有 (日本、中国、英国等)
- **来源**: TIC (Treasury International Capital) 报告
- **说明**: TIC 数据每月月中旬发布，存在约2周延迟
- **状态**: 估算值 (基于最新报告 + 趋势调整)

## 核心指标

| 指标 | 说明 |
|------|------|
| Delta (Δ) | 每周新增债务规模 |
| Gamma (Γ) | 债务加速度（本月新增 vs 上月新增） |
| MoM | 环比变化 |
| YoY | 同比变化 |

## 信号判定
- **戴维期双杀**：Gamma > 0 + 外资 YoY < 0
- **空头警告**：发债速度非线形扩张

## 数据准确性说明

⚠️ **重要提示**：
- **美债总量**: ✅ 实时准确 (TreasuryDirect API)
- **美联储持有**: ✅ 实时准确 (TreasuryDirect API)
- **各国持有**: ⚠️ 估算值 (TIC 报告有月度延迟)

本工具致力于提供准确数据，但部分数据依赖公开估算，仅供参考。

## 使用方式

```bash
python3 radar.py
```

## 输出示例

```
📊 美债需求监测表 | 2026年04月07日 星期二
======================================================================
项目                当前($T)     每周环比      每月环比      每月同比       数据来源
...
📈 供应端:
   • 美债总量: $38.982 T (周环比: +$45.0B, 月环比: +$210.0B)
   • 债务加速度 (Gamma): +10.53%
```

## 风险提示
本工具数据仅供参考，不构成投资建议。
