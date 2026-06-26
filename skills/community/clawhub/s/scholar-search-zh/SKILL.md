---
name: scholar-search-zh
description: "通过 AISA Scholar 接口检索学术论文与研究资料。触发条件：当用户需要论文、作者、最新研究、引用信息或带年份筛选的学术证据时使用。"
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
# 学术论文搜索

## 何时使用

- 通过 AISA Scholar 接口检索学术论文与研究资料。触发条件：当用户需要论文、作者、最新研究、引用信息或带年份筛选的学术证据时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 聚焦学术论文、学者索引与按年份筛选的检索。

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

- 查找 2024 年之后发表的 state-space model 论文。

## 说明

- 当学术证据是首要目标时使用。
