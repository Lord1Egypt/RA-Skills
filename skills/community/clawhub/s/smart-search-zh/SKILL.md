---
name: smart-search-zh
description: "把网页搜索与学术搜索组合成一个智能 AISA 搜索模式。触发条件：当用户需要兼顾公开网页覆盖与学术深度的平衡检索时使用。"
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
# 智能混合搜索

## 何时使用

- 把网页搜索与学术搜索组合成一个智能 AISA 搜索模式。触发条件：当用户需要兼顾公开网页覆盖与学术深度的平衡检索时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 在一次查询流程里同时结合网页覆盖和学术检索。

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

- 研究开放权重推理模型的基准进展。

## 说明

- 当问题同时涉及新闻与论文时，这是很好的默认选择。
