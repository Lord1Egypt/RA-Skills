---
name: stock-rumors-zh
description: "通过 AISA 扫描并购、内幕、分析师、社交媒体和监管相关的市场传闻信号。触发条件：当用户关心早期市场信号、传闻、内幕活动、分析师变动或收购风声时使用。"
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
# 市场传闻扫描

## 何时使用

- 通过 AISA 扫描并购、内幕、分析师、社交媒体和监管相关的市场传闻信号。触发条件：当用户关心早期市场信号、传闻、内幕活动、分析师变动或收购风声时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 按潜在影响对多种类型的传闻信号进行排序。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/rumor_scanner.py
```

## 示例请求

- 扫描本周最强的收购或内幕信号。

## 说明

- 传闻未被证实，建议独立核验。
