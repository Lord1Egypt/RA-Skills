# 联网搜索统一接口

一个接口完成联网搜索，自动选择最优服务商（百炼 / Tavily / 火山引擎 / 智谱 GLM / 腾讯云 WSA），支持降级、合并、告警。

## 特性

- ✅ **统一接口** - 一个 `search()` 函数，自动选择服务商
- ✅ **智能区域路由** - 自动判断国内/海外搜索，按中英文关键词推断目标源
- ✅ **多服务商并行** - 五个搜索源可同时调用，按强度并发
- ✅ **自动降级与 Key 池轮换** - 主 Key 额度耗尽时自动切换备用 Key
- ✅ **结果合并** - 去重、排序、合并多个来源
- ✅ **告警机制** - 服务商失败时返回 `alerts` 字段

## 安装

将本目录放入你的 Skill 目录（OpenClaw / Hermes / 任意支持 Markdown Skill 协议的运行时）即可。

### Python 依赖

```bash
pip install requests
```

> `requests` 是唯一硬依赖。脚本未使用 `httpx`、`openai`、`tenacity` 等额外包。

## 快速开始

```python
from web_search import search

# 快速查询
result = search("北京天气", intensity="quick")

# 一般查询 + 时效筛选
result = search("AI新闻", intensity="normal", freshness=7)

# 精确日期窗口
result = search("AI新闻", start_date="2026-06-21", end_date="2026-06-22")

# 深度查询 + 站点限定
result = search("政策分析", intensity="deep", sites=["gov.cn"])

# 平台定向（小红书 / 微信）
result = search("护肤测评", platforms=["xiaohongshu"])
result = search("行业周报", platforms=["wechat"], freshness=7)

# 强制走海外源
result = search("HuggingFace 最新模型", region="overseas")

# 使用结果
if result["success"]:
    print(result["answer"])      # 答案文本
    print(result["sources"])     # 来源列表
    print(result["provider"])    # 使用的服务商
else:
    print(result["error"])       # 错误信息
```

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| query | str | 必填 | 搜索问题 |
| intensity | str | `"normal"` | 搜索强度：`quick`/`normal`/`deep` |
| freshness | int | None | 相对时效：7/30/180/365 天 |
| start_date | str | None | 起始日期 `YYYY-MM-DD` |
| end_date | str | None | 结束日期 `YYYY-MM-DD` |
| sites | list | None | 域名白名单 |
| exclude_sites | list | None | 域名黑名单 |
| platforms | list | None | 平台别名：`xiaohongshu`/`wechat`/`weibo` 等 |
| auth_level | int | 0 | 权威过滤（火山原生） |
| topic | str | `"general"` | Tavily 话题：`general`/`news`/`finance` |
| region | str | `"auto"` | 区域路由：`auto`（自动）/`domestic`（国内）/`overseas`（海外） |

参数按后端能力路由：支持则原生传入，否则用较宽 freshness + 后处理过滤。

## 返回值

```python
{
    "success": True,
    "answer": "答案文本",
    "sources": [{"title": "...", "url": "...", "snippet": "..."}],
    "provider": ["bailian", "volcengine"],   # 使用的服务商
    "alerts": [{"provider": "tavily", "error": "..."}],  # 失败告警
    "filters_applied": {
        "routing": {...},
        "params_applied": {...},
        "retry_hint": "..."
    }
}
```

## 配置密钥

至少配置一个服务商的 API Key 即可运行——脚本会自动跳过未配置的后端。建议至少配齐"国内 + 海外"各一个，覆盖大部分查询场景。

### 方式 1：环境变量（推荐）

```bash
# 百炼（阿里云，推荐国内搜索）
export BAILIAN_API_KEY="<your-bailian-key>"

# Tavily（推荐海外搜索，支持多 key 池轮换：逗号分隔）
export TAVILY_API_KEY="<your-tavily-key>"
# 或多 key：export TAVILY_API_KEY="<key1>,<key2>,<key3>"

# 火山引擎联网搜索（国内搜索，每月 500 次免费额度）
export WEB_SEARCH_API_KEY="<your-web-search-token>"

# 智谱 GLM 搜索（国内/海外双向）
export ZHIPU_API_KEY="<your-zhipu-key>"

# 腾讯云 WSA 搜索（国内）
export TENCENT_WSA_APIKEY="<your-tencent-wsa-key>"
```

### 方式 2：`.env` 文件

在 skill 目录下放 `.env`，脚本会自动加载：

```env
BAILIAN_API_KEY=<your-bailian-key>
TAVILY_API_KEY=<your-tavily-key>
WEB_SEARCH_API_KEY=<your-web-search-token>
ZHIPU_API_KEY=<your-zhipu-key>
TENCENT_WSA_APIKEY=<your-tencent-wsa-key>
```

## 服务商说明

| 服务商 | 适用场景 | 特点 | 环境变量 |
|--------|----------|------|----------|
| 百炼（Bailian） | 国内 | 阿里云，中文优化，answer 质量高 | `BAILIAN_API_KEY` |
| Tavily | 海外 | 专为 AI 设计，结果质量高，支持 key 池轮换 | `TAVILY_API_KEY` |
| 火山引擎（Volcengine Search） | 国内 | 字节跳动，每月 500 次免费，支持权威过滤 | `WEB_SEARCH_API_KEY` |
| 智谱 GLM 搜索 | 国内 + 海外 | 智谱 BigModel，跨区域可用 | `ZHIPU_API_KEY` |
| 腾讯云 WSA | 国内 | 腾讯云搜索 Agent，结构化 sources | `TENCENT_WSA_APIKEY` |

## 搜索强度与服务商路由

| 强度 | 国内搜索 | 海外搜索 | 耗时 |
|------|----------|----------|------|
| quick | 火山引擎 | Tavily / 智谱 | ~2s |
| normal | 火山引擎 + 智谱 / 百炼 | Tavily + 智谱 | ~4s |
| deep | 火山 + 百炼 + 智谱 + 腾讯 WSA | Tavily + 智谱 + 百炼 | ~6s |

- 仅调用已配置密钥的后端，未配置的源自动跳过
- `platforms` 指定国内平台时不调跨国服务商
- `topic=news|finance` 且海外 → 优先 Tavily
- 主力 Key 额度耗尽时自动切换备用 Key 并继续可用 route
- 主路由全部失败时自动 fallback 到其他可用后端

## ⚠️ 火山引擎密钥说明

火山引擎有**三种不同的 key**，用途完全不同，互不通用：

| Key 类型 | 格式 | 用途 | 本 skill 支持 |
|----------|------|------|--------------|
| 联网搜索 API Key | 非标准（如 `<web-search-token>`） | 联网搜索专用 | ✅ 使用 `WEB_SEARCH_API_KEY` |
| agentplan key | `ark-<agentplan-token>` | 仅 Agent Plan 聊天 | ❌ |
| 通用 ARK API Key | `ark-<token>`（标准格式） | 模型推理 + 搜索工具 | ❌ |

联网搜索 API Key 获取方式：
- 个人用户：[联网搜索控制台](https://console.volcengine.com/search-infinity/api-key) → 创建 API Key
- Agent Plan 用户：[Agent Plan 控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan) → 配置 Harness → 联网搜索 → 查看 API Key

详见 `references/volcengine-key-types.md`。

## 开发

```bash
# 克隆仓库
git clone https://github.com/naive-white-expert/unified-web-search.git
cd unified-web-search

# 安装依赖（仅 requests）
pip install requests
```

## License

MIT
