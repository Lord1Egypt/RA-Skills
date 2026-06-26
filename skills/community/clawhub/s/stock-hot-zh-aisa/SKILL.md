---
name: stock-hot-zh
description: "通过 AISA 扫描热门股票和加密资产的实时异动。触发条件：当用户想知道现在什么最热、什么在大幅波动、市场动量如何、涨幅榜或消息驱动异动时使用。"
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
# 热门标的扫描

## 何时使用

- 通过 AISA 扫描热门股票和加密资产的实时异动。触发条件：当用户想知道现在什么最热、什么在大幅波动、市场动量如何、涨幅榜或消息驱动异动时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 找出涨跌幅居前标的、动量标的和快速市场总结。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/hot_scanner.py
```

## 示例请求

- 展示当前最热门的股票和加密异动标的。

## 说明

- 仅供信息参考，不构成投资建议。
