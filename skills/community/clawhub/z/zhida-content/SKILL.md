---
slug: zhida-content
name: 知乎内容搜索
version: "1.0.0"
author: 千策
---


# Zhida Content — 知乎内容搜索与分析

知乎内容搜索、热度分析、选题挖掘工具。

## 核心功能

### 1. 话题搜索
按关键词搜索知乎问题，查看热度、回答数、关注者数据

### 2. 热榜获取
实时获取知乎热榜问题

### 3. 问题分析
深度分析单个问题：浏览量、回答质量、竞争程度、内容机会

### 4. 选题建议
基于搜索数据，推荐高价值创作选题

## 使用方式

```bash
# 搜索话题
python3 scripts/fetch_zhida.py --search "AI副业"

# 热榜问题
python3 scripts/fetch_zhida.py --hot --limit 10

# 问题分析
python3 scripts/fetch_zhida.py --analyze "https://www.zhihu.com/question/123456789"

# 选题推荐（关键词）
python3 scripts/fetch_zhida.py --topic "AI" --limit 20

# JSON输出
python3 scripts/fetch_zhida.py --topic "AI副业" --json
```

## 选题推荐逻辑

问题热度分级：
- 🔥🔥🔥 极热（100万+浏览）→ 蹭流量，但竞争激烈
- 🔥🔥 中热（10-100万浏览）→ 最佳选择，流量+竞争平衡
- 🔥 温热（1-10万浏览）→ 垂直领域机会
- ❄️ 冷门（1万以下）→ 竞争小但流量有限

回答机会评分：
- 高机会：回答少 + 关注多 + 浏览高
- 中机会：回答中等 + 浏览高
- 低机会：回答多 + 浏览低

## 数据来源

知乎搜索 API（无需登录）

## 注意事项

- 知乎反爬严格，脚本内置延迟和降级处理
- 部分 API 可能因地域限制不可用
