---
name: unified-web-search
description: 联网搜索统一接口 - 自动选择最优服务商，支持降级、合并、告警
version: 2.2.0
author: Kang Rui
metadata:
  openclaw:
    requires:
      env:
        - BAILIAN_API_KEY
        - TAVILY_API_KEY
        - WEB_SEARCH_API_KEY
        - ZHIPU_API_KEY
        - TENCENT_WSA_APIKEY
    homepage: "https://github.com/naive-white-expert/unified-web-search"
---

# 联网搜索

一个接口完成联网搜索，自动选择最优服务商，支持降级和合并。

## 使用场景

- 用户需要搜索任何网络信息

## 使用流程

```
1. 判断搜索强度 → 2. 调用接口 → 3. 使用结果
```

### 1. 判断搜索强度

| 用户需求 | intensity 参数 | 说明 |
|----------|----------------|------|
| 快速查询（天气、股价） | `"quick"` | 速度最快 |
| 一般查询（新闻、常识） | `"normal"` | 平衡速度和覆盖 |
| 深度查询（研究、分析） | `"deep"` | 结果最全面 |

### 2. 调用接口

```python
from web_search import search

result = search("关键词", intensity="quick", freshness=7, sites=["gov.cn"])

# 精确日期窗口（昨天+今天）
result = search(
    "AI 行业新闻",
    start_date="2026-06-21",
    end_date="2026-06-22",
    topic="news",
)

# 平台定向（小红书 / 微信公众号）
result = search("护肤测评", platforms=["xiaohongshu"])
result = search("行业周报", platforms=["wechat"])
```

### 3. 使用结果

```python
if result["success"]:
    answer = result["answer"]      # 答案文本
    sources = result["sources"]    # 来源列表
    provider = result["provider"]  # 使用的服务商列表
else:
    error = result["error"]        # 错误信息
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | 必填 | 搜索问题 |
| intensity | str | `"normal"` | 搜索强度：`quick`（快速）/`normal`（平衡）/`deep`（全面） |
| freshness | int | None | 相对时效：7/30/180/365 天 |
| start_date | str | None | 起始日期 `YYYY-MM-DD`（与 end_date 搭配） |
| end_date | str | None | 结束日期 `YYYY-MM-DD` |
| sites | list | None | 域名白名单，如 `["gov.cn"]` |
| exclude_sites | list | None | 域名黑名单 |
| platforms | list | None | 平台别名：`xiaohongshu`/`wechat`/`weibo`/`zhihu`/`bilibili`/`douyin`/`gov`/`arxiv` |
| auth_level | int | 0 | 权威过滤：0=全部，1=高权威 |
| topic | str | `"general"` | Tavily 话题：`general`/`news`/`finance` |
| region | str | `"auto"` | 区域路由：`auto`（自动推断）/`domestic`（强制国内源）/`overseas`（强制海外源） |

## 返回值

```python
{
    "success": True,
    "answer": "答案文本",
    "sources": [{"title": "...", "url": "...", "snippet": "..."}],
    "provider": ["bailian", "volcengine"],   # 实际使用的服务商
    "alerts": [],                             # 失败的服务商告警
    "filters_applied": {
        "routing": {...},                     # 路由信息
        "params_applied": {...},              # 实际生效参数
        "retry_hint": "..."                   # 多轮搜索建议
    }
}
```

## 示例

```python
from web_search import search

# 快速查询
result = search("北京天气", intensity="quick")

# 一般查询 + 时效筛选
result = search("AI新闻", intensity="normal", freshness=7)

# 精确两天窗口
result = search("AI新闻", start_date="2026-06-21", end_date="2026-06-22")

# 深度查询 + 站点限定
result = search("政策分析", intensity="deep", sites=["gov.cn"])

# 小红书 / 微信定向
result = search("新品发布", platforms=["xiaohongshu", "wechat"], freshness=7)

# 强制走海外源
result = search("HuggingFace 最新模型", region="overseas")
```

## 搜索强度与服务商路由

| 强度 | API 次数 | 国内 | 海外 |
|------|----------|------|------|
| quick | 1 | 火山引擎 | Tavily / 智谱 |
| normal | 1 | 火山引擎 | Tavily / 智谱 |
| deep | ≤2 | 火山引擎 + 百炼 / 腾讯云 / 智谱 | Tavily + 智谱 / 百炼 |

- 仅调用已配置密钥的后端
- `platforms` 为国内平台时不调跨国服务商
- `topic=news|finance` 且海外 → 优先 Tavily
- 主力 Key 额度耗尽时自动切换备用 Key 和 route
- 主路由全部失败时自动 fallback 到其他可用后端

## 区域路由

内置中文/英文关键词智能推断：搜索"北京天气"自动走国内源，搜索 "GPT-5" 自动走海外源。可通过 `region` 参数强制指定：

| 值 | 行为 |
|----|------|
| `"auto"`（默认） | 根据 query 内容自动推断 |
| `"domestic"` | 强制走国内搜索源 |
| `"overseas"` | 强制走海外搜索源 |

## 前置条件

至少配置一个搜索服务商的 API Key（通过环境变量或配置文件）。支持的搜索源：

- 百炼（阿里云）
- Tavily（海外搜索）
- 火山引擎联网搜索
- 智谱 GLM 搜索
- 腾讯云 WSA 搜索

## 其他文件

- **搜索实现** → `scripts/web_search.py`
- **服务商对比与路由详情** → `references/comparison.md`
- **火山引擎三种 Key 区别** → `references/volcengine-key-types.md`
