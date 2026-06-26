---
name: tavily-extract-zh
description: "通过 AISA Tavily 抽取接口从 URL 获取干净正文。触发条件：当用户已经有 URL，需要读取页面正文做总结、对比或证据审查时使用。"
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
# Tavily 页面抽取

## 何时使用

- 通过 AISA Tavily 抽取接口从 URL 获取干净正文。触发条件：当用户已经有 URL，需要读取页面正文做总结、对比或证据审查时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 把原始 URL 转成可分析的干净正文文本。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/search_client.py
```

## 示例请求

- 抽取这些产品公告 URL，并总结差异。

## 说明

- 最适合与搜索或后续综合分析配合使用。
