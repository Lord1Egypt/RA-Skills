---
name: tradealpha-open-platformv2
description: Fetch realtime TradeAlpha news across Reuters, Bloomberg, Truth Social, research alerts, and domestic news sources via `POST /api/v1/news/realtime_news`. Use when the user asks to pull TradeAlpha news, realtime news, Reuters news, Bloomberg news, Truth news, domestic headlines, or to filter news by source, category, level, or time range.
version: 0.0.2
homepage: https://quantaccess.lxaa.top/
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["node"] },
        "primaryEnv": "TradeAlphaToken"
      },
  }
---

# TradeAlpha Realtime News

在用户明确表示“帮我拽 TradeAlpha 新闻”“帮我拉取实时新闻”或提到 TradeAlpha 新闻筛选需求时，优先使用本 skill。

本 skill 是可执行版本，默认通过本目录下的脚本完成新闻拉取：

- `scripts/get-realtime-news.js`

## Trigger Rules

以下表达默认视为触发词：

- 帮我拽 TradeAlpha 新闻
- 帮我拉 TradeAlpha 新闻
- TradeAlpha 实时新闻
- 拉取路透新闻
- 拉取彭博新闻
- 拉取 Truth 新闻
- 拉取国内新闻
- 按来源、分类、重要程度筛选新闻

## Endpoint

- 基础地址：`https://quantaccess.lxaa.top`
- 方法：`POST`
- 路径：`/api/v1/news/realtime_news`
- 完整地址：`https://quantaccess.lxaa.top/api/v1/news/realtime_news`

## Security Disclosure

执行前必须明确下面这些行为：

- 新闻请求会发送到 `https://quantaccess.lxaa.top`
- 脚本只读取系统环境变量 `TradeAlphaToken`
- 如果没有 `TradeAlphaToken`，必须直接报错，并提示用户去 `https://quantaccess.lxaa.top/#/login` 注册、登录、获取 token 后再设置环境变量
- 不要在回复中回显用户 token

如果用户关心安全性，应直接说明以上行为。

## Workflow

1. 判断用户是否要“TradeAlpha 新闻”或相关筛选新闻。
2. 根据用户自然语言补齐请求参数。
3. 先运行新闻脚本：
   - `node scripts/get-realtime-news.js '{"source":"bloomberg"}'`
4. 如果脚本返回 `success: true`，整理 `list` 返回给用户。
5. 如果脚本提示缺少 `TradeAlphaToken`，直接告诉用户去 `https://quantaccess.lxaa.top/#/login` 注册、登录、获取 token，并把它设置到系统环境变量 `TradeAlphaToken` 后再试。
6. 如果脚本返回接口错误码，按错误码含义明确告诉用户失败原因。
7. 如果当前运行环境根本没有 shell / exec 能力，立即停止，不要重试，直接告诉用户：当前会话无法执行本地脚本，因此现在不能代为拉取新闻。

## Execution Rules

- 优先运行 `scripts/get-realtime-news.js`
- 不要再次读取当前 skill 文件，不要为了执行去查找 `SKILL.md` 路径
- 不要调用 `read`、`sessions_send`、`taskflow` 或类似“先开子任务再执行”的流程
- 不要反复自言自语地宣布“马上执行”或“先读技能文档”
- 不要跳过脚本直接编造接口返回
- 不要要求用户自己拼请求体，优先根据自然语言帮用户补参数
- 需要命令示例时，使用本 skill 目录下的脚本路径
- 运行脚本时优先传 JSON 参数对象，不要拆成多组零散命令参数
- 不要再走账号密码登录流程
- 缺少 `TradeAlphaToken` 时，直接停止并给出注册网址说明
- 如果当前会话缺少执行脚本的工具能力，只回复一次明确失败原因，不要循环重试

## Parameter Mapping

- 用户说“今天新闻”“今日新闻”“当天新闻”：优先传当天的 `start_time` 和当前时刻的 `end_time`
- 用户未提供时间范围：默认按接口近 24 小时逻辑处理
- 用户说“路透”：`source: "rtrs"`
- 用户说“彭博”：`source: "bloomberg"`
- 用户说“Truth” 或 “川普 Truth”：`source: "truth"`
- 用户说“国内”：`source: "domestic"`
- 用户说“研报”：`source: "research_report"`
- 用户说“很重要”“重要”“一般”：映射到 `level`
- 用户提到分类时，直接使用接口要求的中文全称：`政治军事`、`社会`、`娱乐体育`、`公司`、`超大型公司`、`政策`、`市场与货币`
- 用户未指定分页时，默认 `page: 1`、`page_size: 20`
- 若用户要求更多结果，可提高 `page_size`，但不得超过 `100`

## Guardrails

- `start_time` 和 `end_time` 不能早于北京时间 `2025-04-01`
- 若用户显式给出的时间早于下界，应先提醒该限制，不要伪造成功请求
- 单次请求 `page_size` 最大为 `100`
- 接口存在客观延迟，新闻通常会晚 `0-5` 分钟
- 不要编造新闻内容、来源、时间或状态码
- 如果接口返回成功，按文档理解 `data.list[]` 只读取 `id`、`datetime`、`content`、`source`、`category`、`level`

## Error Handling

- `1001`：token 无效或已过期
- `1002`：请求参数错误
- `1003`：超出请求频率限制
- `1004`：账户余额不足或无权限访问该接口
- `5000`：服务器内部错误

遇到错误时，直接说明原因，并在适合时提示用户检查 token、时间范围、分页大小或频率限制。

## Response Style

- 先给简明摘要，再列出关键新闻
- 保留原始新闻中的时间和来源
- 当结果很多时，优先展示最相关或最新的几条，并说明还有更多结果
- 输出风格保持直接，不要把回复写成接口文档
- 如果因能力限制无法执行，就直接说明“当前会话没有本地脚本执行能力”，不要输出内部思考过程

## Script Usage

```bash
node scripts/get-realtime-news.js
node scripts/get-realtime-news.js '{"source":"bloomberg","level":"重要","page_size":5}'
```

## Additional Resources

- 详细参数和错误码见 [reference.md](reference.md)
- 请求体和响应示例见 [examples.md](examples.md)
