---
name: stock-dividend-zh
description: "通过 AISA 评估股票的股息率、派息安全性、增长情况和收益质量。触发条件：当用户关心股息安全、收益型投资、股息增长或股息贵族筛选时使用。"
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
# 股息分析

## 何时使用

- 通过 AISA 评估股票的股息率、派息安全性、增长情况和收益质量。触发条件：当用户关心股息安全、收益型投资、股息增长或股息贵族筛选时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 重点分析股息安全性、覆盖率、增长和收益质量。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/dividends.py
```

## 示例请求

- 评估 JNJ 和 PG 哪个更适合做稳定分红配置。

## 说明

- 仅供信息参考，不构成投资建议。
