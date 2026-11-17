---
name: quant-x-v13
version: 13.0.0
author: MiniMax-M3
description: A股 4维OBI + OBV增强 + 龙虎榜3维验证 + 主力吸筹5大铁律 量化分析器
categories:
  - finance
  - quantitative-trading
  - a-share
tags:
  - obi
  - obv
  - main-force
  - longhubang
  - china-stock
  - quant
---

# Quant-X v13 - A股主力量化分析器

## 功能
基于 2026 最新主流量化策略，集成 7 大模块：

1. **4 大数据源融合**: 腾讯报价 + 腾讯分时 + 东方财富 push2 + 板块联动
2. **4 维 OBI 引擎**: 计数 + 量加权 + 时间衰减 + 大单 (权重 0.15/0.30/0.25/0.30)
3. **OBV 增强**: 主力线 + 散户线 + 增强趋势 + 30 周期 MAOBV
4. **龙虎榜 3 维验证**: 买卖结构 + 资金性质 + 量价配合
5. **主力吸筹 5 大铁律**: 筹码结构 + 量能节奏 + 累计换手 + K线重心 + 控盘度
6. **6 因子综合评分**: 趋势 + 动量 + 量价 + 波动 + 资金流向 + DDX/DDY + 板块 + 涨停
7. **操作建议**: 自动生成关键位 + 主力行为判断

## 数据源
- 腾讯 qt.gtimg.cn
- 腾讯 ifzq.gtimg.cn
- 东方财富 push2.eastmoney.com
- 板块联动 (CPO + 半导体 + 宽基 ETF)

## 使用方法
python3 quant_v13.py

## 风险提示
本工具仅供学习和研究使用，不构成投资建议。
