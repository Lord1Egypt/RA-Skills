---
name: stock-portfolio-zh
description: "通过 AISA 的实时价格与盈亏跟踪来创建和管理股票加密投资组合。触发条件：当用户想新增持仓、查看组合表现、重命名组合或审查当前盈亏时使用。"
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
# 投资组合管理

## 何时使用

- 通过 AISA 的实时价格与盈亏跟踪来创建和管理股票加密投资组合。触发条件：当用户想新增持仓、查看组合表现、重命名组合或审查当前盈亏时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 在命令行中创建、更新、列出、重命名和删除投资组合。
- 使用仓库内本地状态目录跟踪实时盈亏，而不是默认写入家目录。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/portfolio.py
```

## 示例请求

- 创建一个 AI 股票组合并展示当前盈亏。

## 说明

- 除非显式设置 `CLAWDBOT_STATE_DIR`，默认状态保存在 `./.clawdbot/skills/stock-analysis/portfolios.json`。
