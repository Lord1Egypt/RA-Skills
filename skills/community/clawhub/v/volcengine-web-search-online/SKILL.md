---
name: volcengine-web-search
description: "调用火山引擎联网搜索接口，获取 web / web_summary / image 搜索结果。使用此技能当用户需要：联网搜索、火山联网搜索、web_summary 总结、调用 /volcengine/web-search 接口、使用 Python 脚本请求并读取 summary_text / 搜索结果。Use this skill for Volcengine web search API calls and summarized web search results."
argument-hint: "必填：query, search_type, azt_api_key；可选：count, need_summary, time_range, content_formats, industry, query_rewrite"
user-invocable: true
---

# 火山联网搜索 Skill

调用接口：
- `POST https://coze-js-api.devtool.uk/volcengine/web-search`

执行随附的 Python 脚本来完成请求，不要在回复中内联构造 curl 命令（除非用户明确要求）。

## 使用场景

以下情况触发本技能：
- 用户想做联网网页搜索（`web`）
- 用户想要联网搜索总结（`web_summary`）
- 用户想做图片搜索（`image`）
- 用户希望直接读取聚合结果（如 `summary_text`、`usage`）

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | **必填** | — | 搜索词，对应接口 `query/Query` |
| `search_type` | **必填** | — | 搜索类型：`web` / `web_summary` / `image` |
| `azt_api_key` | **必填** | — | 平台鉴权 Key（映射为 payload 的 `api_key`） |
| `count` | 可选 | `20` | 返回条数（未传走接口默认 20） |
| `need_summary` | 可选 | 自动 | 是否需要总结；`web_summary` 建议为 `true` |
| `time_range` | 可选 | — | 时间范围，如 `OneDay/OneWeek/OneMonth/OneYear` |
| `content_formats` | 可选 | — | 正文格式：`text` / `markdown` |
| `industry` | 可选 | — | 行业类型，如 `finance` / `game` |
| `query_rewrite` | 可选 | `false` | 是否开启 Query 改写 |

说明：`search_api_key` 由服务端内置配置提供，Skill 侧不对用户暴露该参数。

## API Key 获取方式

**必须提供 `azt_api_key`**，解析顺序如下：

1. 读取环境变量 `AZT_API_KEY`。
2. 用户在参数中直接传入。
3. 如果两者均未提供，**停止执行**并提示：

> 未检测到 API Key。请前往 **https://devtool.uk/plugin** 购买或查看使用说明后重试。

说明：脚本对外参数使用 `azt_api_key`（或 `AZT_API_KEY`），请求接口时映射为 payload 字段 `api_key`。

## 执行方式

```bash
# 1) web 搜索
export AZT_API_KEY="your_key_here"
python3 scripts/web_search.py --query "今日最新的AI资讯" --search_type web

# 2) web_summary 总结搜索
python3 scripts/web_search.py --query "今日最新的AI资讯" --search_type web_summary --need_summary true

# 3) image 搜索
python3 scripts/web_search.py --query "北京天气" --search_type image --count 5
```

## 响应处理

1. 显示请求状态（`code: 200` 为成功，`code: -1` 为失败）。
2. `search_type=web_summary` 时，优先输出 `summary_text`（若存在）。
3. 输出 `result_count`、`usage`、`search_context` 等关键字段。
4. `web` / `image` 时输出结果条目（标题、链接、摘要等）。

常见失败原因：
- `azt_api_key` 无效或已过期 → 前往 https://devtool.uk/plugin 重新购买
- `azt_api_key` 积分已用完 → 联系作者续费
- 上游搜索 key 缺失或无权限 → 检查服务端内置配置（`VOLCENGINE_WEB_SEARCH_API_KEY`）
- 网络问题或服务器错误 → 稍后重试

## 输出格式

```markdown
# 火山联网搜索结果

- 接口：POST https://coze-js-api.devtool.uk/volcengine/web-search
- 搜索词：<query>
- 搜索类型：<search_type>
- API Key 来源：<env: AZT_API_KEY | 用户传入>

## 返回数据
<summary_text / web_results / image_results>

## 状态
<成功/失败信息及剩余积分>
```
