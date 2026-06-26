---
name: stock-analysis-zh
description: "通过 AISA 做股票和加密资产分析，输出评分、信号、置信度和风险提示。触发条件：当用户要求分析某个代码、比较投资标的或评估市场位置时使用。"
author: aisa
version: "1.0.0"
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  env:
    - AISA_API_KEY
  bins:
    - python3
metadata:
  openclaw:
    primaryEnv: AISA_API_KEY
    requires:
      env:
        - AISA_API_KEY
      bins:
        - python3
---
# 股票与加密分析

## 何时使用

- 通过 AISA 做股票和加密资产分析，输出评分、信号、置信度和风险提示。触发条件：当用户要求分析某个代码、比较投资标的或评估市场位置时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 基于实时数据对股票和加密资产做评分分析。
- 返回 BUY HOLD SELL 风格的信号、置信度和关键风险。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/analyze_stock.py
```

## 示例请求

- 对比分析 AAPL 和 MSFT，并总结更强的一方。

## 说明

- 仅供信息参考，不构成投资建议。
