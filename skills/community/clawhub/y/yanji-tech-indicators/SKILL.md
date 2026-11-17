---
name: yanji-tech-indicators
description: 研技Skill — 技术指标教学演示计算（基于内置示例K线，非真实行情）
---

# 研技 · 技术指标计算 (yanji-tech-indicators)

> **⚠️ 数据来源与限制（重要披露）：**
> 本Skill的所有指标（MACD/RSI/KDJ/布林带/均线等）均由标准数学公式基于**内置示例K线数据**计算得出，输出为**教学演示结果，非真实行情结论**。
> 结果仅用于课程教学演示，不构成投资建议。

## 功能
基于示例K线数据计算常用技术指标：
1. **趋势类** — MACD（DIF/DEA/柱）、均线系统（MA5/10/20/60/120/250）
2. **震荡类** — RSI(6/12/24)、KDJ、威廉指标WR
3. **通道类** — 布林带（中轨/上轨/下轨/带宽）
4. **量价类** — OBV、量价背离检测、放量/缩量判断
5. **形态识别** — 金叉/死叉、顶背离/底背离、突破/跌破

## 数据来源说明（重要）
- 本Skill**不联网、不获取真实行情数据**，脚本仅使用 Python 标准库。
- 指标基于**内置示例基准价/示例K线数据**计算得出，输出 JSON 中 `data_source` 字段恒为"演示数据（固定基准价计算，非真实行情；仅供教学演示）"。
- 所有计算结果仅为教学演示，请勿当作真实行情结论或投资参考。

## 调用方式
```bash
python3 {baseDir}/scripts/calc_indicators.py [--code sh600519] [--indicators macd,rsi,kdj,boll] [--output json|text]
```

## 输出示例
```json
{
  "code": "sh600519",
  "name": "贵州茅台",
  "date": "2026-07-03",
  "data_source": "演示数据（固定基准价计算，非真实行情；仅供教学演示）",
  "indicators": {
    "macd": {"dif": 12.5, "dea": 8.3, "hist": 4.2, "signal": "金叉运行中"},
    "rsi": {"rsi6": 62.5, "rsi12": 55.3, "rsi24": 48.7, "signal": "中性偏强"},
    "kdj": {"k": 70.2, "d": 65.8, "j": 79.0, "signal": "偏多"},
    "boll": {"mid": 1162.80, "upper": 1250.50, "lower": 1075.10, "bandwidth": 15.1, "position": "中轨上方"},
    "ma_signal": "多头排列（MA5>MA10>MA20>MA60）",
    "volume_signal": "量价配合良好"
  },
  "support_resistance": {
    "support": [1150, 1120, 1080],
    "resistance": [1200, 1250, 1300]
  }
}
```
