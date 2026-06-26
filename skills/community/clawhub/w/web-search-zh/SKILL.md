---
name: web-search-zh
description: "通过 AISA 网页搜索接口检索公开互联网，并返回结构化标题、链接和摘要。触发条件：当用户要求联网查找、收集近期来源或获取通用网页结果时使用。"
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
# 网页搜索

## 何时使用

- 通过 AISA 网页搜索接口检索公开互联网，并返回结构化标题、链接和摘要。触发条件：当用户要求联网查找、收集近期来源或获取通用网页结果时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 为通用联网检索任务返回快速结构化网页结果。

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

- 搜索最新的开源浏览器自动化工具。

## 说明

- 这是整套包里最轻量的通用搜索选项。
