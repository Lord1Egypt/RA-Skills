---
name: stock-watchlist-zh
description: "利用 AISA 的实时价格检查来管理股票加密观察列表，并设置目标位和止损提醒。触发条件：当用户想添加观察标的、设置目标价、跟踪止损或检查提醒触发情况时使用。"
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
# 观察列表管理

## 何时使用

- 利用 AISA 的实时价格检查来管理股票加密观察列表，并设置目标位和止损提醒。触发条件：当用户想添加观察标的、设置目标价、跟踪止损或检查提醒触发情况时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 在命令行中添加、移除、列出和检查观察列表条目。
- 默认把观察列表状态存放在仓库内目录中，便于更安全地发布。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/watchlist.py
```

## 示例请求

- 把 NVDA 加入观察列表，并设置目标价和止损价。

## 说明

- 除非显式设置 `CLAWDBOT_STATE_DIR`，默认状态保存在 `./.clawdbot/skills/stock-analysis/watchlist.json`。
