---
name: twitter-autopilot-zh
description: "搜索 X Twitter 数据、监控账号动态、追踪热点，并通过 AISA 中继完成发帖与互动。触发条件：当用户需要 Twitter 搜索、社媒监听、博主监控、发帖、回复、点赞或关注流程时使用。"
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
# Twitter 自动化助手

## 何时使用

- 搜索 X Twitter 数据、监控账号动态、追踪热点，并通过 AISA 中继完成发帖与互动。触发条件：当用户需要 Twitter 搜索、社媒监听、博主监控、发帖、回复、点赞或关注流程时使用。

## 不适用场景

- 当用户明确要本地浏览器 Cookie、密码、Keychain 或其他本地敏感凭据时，不要使用这个 skill。
- 当问题与该 skill 的主题无关时，优先选择更贴切的 skill。

## 核心能力

- 通过 AISA API 读取 Twitter X 用户资料、时间线、提及、粉丝、热点和搜索结果。
- 通过内置 OAuth 中继客户端支持发帖、回复、引用、点赞、取消点赞、关注和取关。
- 读取能力只需要 API Key，写入能力走 OAuth，不要求密码或浏览器 Cookie。

## 快速开始

```bash
export AISA_API_KEY="your-key"
```

## 运行方式

首选运行路径是仓库内置的 Python 客户端：

```bash
python3 scripts/twitter_client.py
```

## 示例请求

- 查看 @OpenAI 最近 20 条和 GPT 发布有关的推文并总结。
- 分析 X Twitter 上 AI 相关的热门话题并按情绪分组。
- 在授权完成后，把这条产品发布线程发到 X Twitter。

## 说明

- 写入动作使用内置的 `twitter_oauth_client.py` 与 `twitter_engagement_client.py`。
- 如果发帖或互动提示未授权，先完成 OAuth 授权，再重试动作。
