---
name: twitterwebapi
description: "调用 Twitter 推文详情和搜索时间线接口，获取推文内容、作者信息、互动数据和搜索结果。Use this skill for Twitter tweet detail and search timeline API calls."
argument-hint: "必填：mode(detail/search)；detail 需要 tweet_id，search 需要 keyword；可选：search_type, cursor, azt_api_key"
user-invocable: true
---

# Twitter 接口 Skill

调用接口：
- `POST https://coze-js-api.devtool.uk/twitter/fetch_tweet_detail`
- `POST https://coze-js-api.devtool.uk/twitter/fetch_search_timeline`

执行随附的 Python 脚本来完成请求，不要在回复中内联构造 curl 命令（除非用户明确要求）。

## 使用场景

以下情况触发本技能：
- 用户想查看某条推文的详细内容
- 用户想按关键词搜索 Twitter / X 时间线
- 用户想获取推文正文、作者信息、发布时间、互动数据
- 用户想用 Python 调用 Twitter API 接口
- 用户想调试 Twitter 接口调用失败的原因

补充说明：
- 具体参数匹配和调用示例放在下面的输入参数与执行方式里。

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | **必填** | — | `detail` 或 `search`，决定调用哪个接口 |
| `tweet_id` | `detail` 必填 | — | 推文 ID，仅 `mode=detail` 时需要 |
| `keyword` | `search` 必填 | — | 搜索关键词，仅 `mode=search` 时需要 |
| `search_type` | 可选 | `Top` | 搜索类型，仅 `mode=search` 时使用 |
| `cursor` | 可选 | — | 翻页游标，仅 `mode=search` 时使用 |
| `azt_api_key` | 可选 | — | 付费版鉴权 Key；不填则使用免费版限制 |

## API Key 获取方式

`azt_api_key` 为可选参数，解析顺序如下：

1. 读取环境变量 `AZT_API_KEY`。
2. 用户在参数中直接传入 `--azt_api_key`。
3. 两者均未提供时，使用**免费版**（可能存在次数限制）。

> 免费版次数已用完或需要更高频率，请前往 **https://devtool.uk/plugin** 购买付费版。

## 执行方式

```bash
# 推文详情
python3 scripts/twitter_api.py detail --tweet_id 1234567890

# 推文搜索
python3 scripts/twitter_api.py search --keyword "OpenAI" --search_type Top

# 搜索并带游标
python3 scripts/twitter_api.py search --keyword "AI" --cursor ABC123

# 付费版（设置环境变量）
export AZT_API_KEY="your_key_here"
python3 scripts/twitter_api.py detail --tweet_id 1234567890

# 付费版（直接传参）
python3 scripts/twitter_api.py search --keyword "elon musk" --azt_api_key your_key_here

# 输出原始 JSON
python3 scripts/twitter_api.py search --keyword "OpenAI" --json
```

## 响应处理

1. 显示请求结果状态（`code: 200` 为成功，`code: -1` 为失败）。
2. `detail` 模式优先展示推文正文、作者、发布时间、互动数据。
3. `search` 模式优先列出返回的推文条目（作者、正文摘要、时间、链接）。
4. 如果失败，给出可能原因及修正建议。

常见失败原因：
- `azt_api_key` 无效或已过期 → 前往 https://devtool.uk/plugin 重新购买
- `azt_api_key` 积分已用完 → 联系作者续费
- 免费版额度已用完 → 等待重置或购买付费版
- 网络问题或服务器错误 → 稍后重试

## 输出格式

```markdown
# Twitter 接口请求结果

- 接口：POST https://coze-js-api.devtool.uk/twitter/fetch_tweet_detail 或 /twitter/fetch_search_timeline
- 模式：<detail | search>
- API Key 来源：<env: AZT_API_KEY | 用户传入 | 免费版>

## 返回数据
<推文详情或搜索结果列表>

## 状态
<成功/失败信息及剩余积分>
```
