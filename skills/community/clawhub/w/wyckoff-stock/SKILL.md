---
name: wyckoff-stock
description: A股诊股工具，基于Wyckoff 2.0方法论分析股票。支持获取实时K线数据、技术指标计算、趋势分析、支撑阻力识别、Wyckoff结构判断、风险收益评估。
metadata:
  inputs:
    - name: stock_code
      type: string
      required: true
      description: A股股票代码，如 601985、000001
    - name: days
      type: number
      required: false
      default: 250
      description: 分析用的K线天数，默认250天
  outputs:
    - name: report
      type: object
      description: 完整诊股报告JSON
---

# A股诊股 Skill (Wyckoff 2.0)

## 功能概述

本 Skill 基于 **Wyckoff 2.0** 方法论，对 A 股进行技术分析，包括：

- 📊 **数据获取** - 通过 efinance 获取 K 线数据
- 📈 **趋势分析** - 均线系统、趋势判断
- 🔍 **Wyckoff 结构** - 识别积累/派发、判断所处阶段
- 📉 **成交量分析** - 放量/缩量信号
- ⚖️ **风险收益评估** - 支撑阻力、入场止损、目标价位

## 使用方法

### 基础用法

```
诊股 <股票代码>
示例：诊股 601985
```

### 调用脚本

```bash
python3 scripts/diagnose.py <股票代码>
```

## 分析模块

### 1. 价格结构
- 当前价格与均线关系
- 支撑阻力位识别（最近20日高低点）
- 区间波动分析（最近120日）

### 2. 趋势判断

| 趋势 | 说明 |
|------|------|
| 上涨趋势 | 均线多头排列，价格在均线上方 |
| 下跌趋势 | 均线空头排列，价格在均线下方 |
| 震荡趋势 | 均线混乱，市场无明确方向 |

### 3. Wyckoff 五阶段

| 阶段 | 说明 |
|------|------|
| Phase A | 停止前期趋势，PS/SC 信号 |
| Phase B | 筑底/筑顶，积累/派发区间 |
| Phase C | 测试阶段，Spring/UT |
| Phase D | 突破确认，趋势开始 |
| Phase E | 趋势发展，趋势延续 |

### 4. 成交量分析
- 放量信号：当日成交量 > 5日均量 1.5倍
- 缩量信号：当日成交量 < 5日均量 0.7倍

### 5. 风险收益评估

| 等级 | 风险收益比 |
|------|-------------|
| 优质 | ≥ 2:1 |
| 一般 | 1:1 ~ 2:1 |
| 较差 | < 1:1 |

## 输出格式

诊股输出包含：
- 💰 价格数据（当前价、支撑阻力）
- 📈 趋势分析（趋势状态、均线排列）
- 🔍 Wyckoff结构（阶段、偏向、区间位置）
- ⚖️ 风险收益（评估、上涨/下跌空间、比率）
- 📋 总结（一句话概括）

## 脚本

- `scripts/diagnose.py` - 核心诊股脚本

## 依赖

- `efinance` - A股数据获取（pip install efinance）
- `python3` - 运行环境

## 注意事项

⚠️ 仅供参考，不构成投资建议！
