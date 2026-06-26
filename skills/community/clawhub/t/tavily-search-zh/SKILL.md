---
name: tavily-search-zh
description: "通过 AISA 调用 Tavily 网页搜索，并支持深度、主题和时间范围过滤。触发条件：当用户需要比普通关键词搜索更灵活的网页检索过滤能力时使用。"
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
# Tavily 网页搜索

## 何时使用

- 通过 AISA 调用 Tavily 网页搜索，并支持深度、主题和时间范围过滤。触发条件：当用户需要比普通关键词搜索更灵活的网页检索过滤能力时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 提供带 Tavily 专属过滤能力的网页搜索。

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

- 使用 Tavily 过滤条件搜索过去一个月的 AI 融资新闻。

## 说明

- 当时效性和过滤条件很重要时特别适合。
