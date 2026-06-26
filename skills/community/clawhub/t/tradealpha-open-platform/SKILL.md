---
name: tradealpha-open-platform
description: Route beginner-friendly natural-language requests for TradeAlpha news and login into the TradeAlpha plugin tools. Use `tradealpha_news` for news and `tradealpha_login` for login or token refresh.
homepage: https://quantaccess.lxaa.top
version: 0.6.0
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["node"] },
        "primaryEnv": "TRADEALPHA_API_KEY",
      },
  }
---

# TradeAlpha开放平台

TradeAlpha 开放平台：路透、彭博、Truth、国内主流消息源，一网打尽。

这是一个给 OpenClaw 使用的独立 skill。

这个 skill 不负责真实执行，只负责把用户的自然语言请求稳定路由到 plugin 提供的两个真实工具：

- `tradealpha_news`
- `tradealpha_login`

## Security Disclosure

在用户安装或首次使用前，应明确知道下面这些运行时行为：

- 登录和新闻请求都会发送到 `https://quantaccess.lxaa.top`
- `tradealpha_news` 会优先读取环境变量 `TRADEALPHA_API_KEY`
- 如果环境变量里没有 token，`tradealpha_news` 会读取本地配置文件 `~/.config/tradealpha-open-platform/config.json`
- `tradealpha_login` 登录成功后，会把返回的 token 保存到 `~/.config/tradealpha-open-platform/config.json`
- 本地配置文件用于后续复用 token，避免每次拉新闻都重新登录
- 不要在回复里回显用户密码或 token

如果用户对安全性有顾虑，应直接提醒用户：

- 先确认自己信任 `quantaccess.lxaa.top`
- 如果不想输入账号密码，可以优先使用 `TRADEALPHA_API_KEY`
- 如果不希望 token 落盘，可以先检查或删除 `~/.config/tradealpha-open-platform/config.json`

如果用户是小白用户，只说一句：

- “给我拉取当天的新闻”
- “帮我看今天的市场新闻”
- “帮我拉彭博新闻”
- “登录 TradeAlpha”

都应优先使用本 skill。

## Tool Contract

本 skill 只允许使用以下两个真实工具：

- `tradealpha_news`
- `tradealpha_login`

不要改用别的工具来冒充新闻或登录能力。

## Availability Check

在执行任何请求前，先确认当前会话里真实可用的工具是否包含：

- `tradealpha_news`
- `tradealpha_login`

如果当前会话里没有这两个工具，说明 skill 已安装，但对应的 TradeAlpha plugin 没有成功加载。

此时必须立即停止执行，并直接告诉用户：

- 当前会话还没有加载 `tradealpha_news` 和 `tradealpha_login`
- 现在不能直接帮你登录或拉新闻
- 这不是账号密码错误，而是插件没有在当前环境里成功启用
- 请先启用或安装 TradeAlpha plugin，然后再重试

不要假装工具存在，不要反复重试不存在的工具，不要使用无关动作代替 plugin 能力。

## Trigger Rules

用户出现以下任一表达时，优先触发本 skill：

- 今天的新闻
- 今日新闻
- 当天新闻
- 现在的新闻
- 最新新闻
- 最近新闻
- 市场新闻
- 宏观新闻
- 路透新闻
- 彭博新闻
- Truth 新闻
- 国内新闻快讯
- 帮我拉新闻
- 帮我看新闻
- 拉取实时新闻
- 按来源、分类、重要程度筛选新闻
- 登录 TradeAlpha
- 获取 token
- 初始化 token
- 刷新 token
- 重新登录 TradeAlpha

## Routing Rules

所有请求都遵守下面的固定路由规则。

### 1. 登录类请求

如果用户明确要登录、初始化 token、刷新 token、重新登录：

1. 向用户索要 `account` 和 `password`
2. 调用 `tradealpha_login`
3. 传入 `account`、`password`
4. 登录成功后，如果用户还要求新闻，再继续新闻请求

### 2. 新闻类请求

如果用户要新闻，先直接调用 `tradealpha_news`，不要先假设用户已经登录。

#### 默认参数映射

- 用户说“今天新闻”“今日新闻”“当天新闻”“今天的市场新闻”，默认传 `timeframe: "today"`
- 用户说“最新新闻”“最近新闻”“最新市场新闻”，默认传 `timeframe: "latest"`
- 用户明确给了 `start_time`、`end_time`，优先使用用户提供的时间范围
- 用户提到新闻源时，附加 `source`
- 用户提到分类时，附加 `category`
- 用户提到重要程度时，附加 `level`
- 用户没有提页码时，优先使用工具默认分页行为，不要自行编造页码

#### 来源映射

- “路透” 对应 `source: "rtrs"`
- “彭博” 对应 `source: "bloomberg"`
- “Truth” 对应 `source: "truth"`
- “国内” 对应 `source: "domestic"`
- “研报” 对应 `source: "research_report"`

#### 新闻请求顺序

1. 按用户口语补齐默认参数
2. 调用 `tradealpha_news`
3. 如果返回 `auth_required: false`，读取结果并整理给用户
4. 如果返回 `auth_required: true`，立即向用户索要 `account` 和 `password`
5. 调用 `tradealpha_login`
6. 如果登录失败，直接告诉用户登录失败原因，不要假装已经登录成功
7. 登录成功后，使用同一组新闻参数再次调用 `tradealpha_news`
8. 再整理结果回复用户

## Runtime Rules

- 只使用 `tradealpha_login` 和 `tradealpha_news`
- 如果当前会话根本没有 `tradealpha_login` 或 `tradealpha_news`，必须先说明“插件未加载”，不要继续执行
- 对“今天新闻”“今日新闻”“当天新闻”这类自然语言，默认视为新闻请求，并传 `timeframe: "today"`
- 对“最新新闻”“最近新闻”这类自然语言，默认视为新闻请求，并传 `timeframe: "latest"`
- 如果工具返回 `auth_required: true`，必须先登录，不能跳过
- 如果 `tradealpha_login` 失败，必须停止后续新闻调用，并把失败原因明确告诉用户
- 登录前不要假设用户已经有 token
- 如果用户询问安全性、隐私、权限或本地存储，必须主动说明网络主机、环境变量和本地配置文件行为
- 返回结果是 JSON 时，先读 `details` 或主返回体，再总结给用户
- 如果同时存在 `details` 和文本内容，优先以 `details` 为准
- 总结时优先保留时间、来源、标题、重要程度等关键信息
- 不要在回复里回显用户密码或 token
- 不要编造新闻内容、来源、时间或登录状态
- 新闻通常存在 `0-5` 分钟客观延迟

## Response Style

对小白用户，回复要直接、短、像助手，而不是像接口文档。

- 能直接拉新闻就直接拉，不要先讲一大段规则
- 需要登录时，只索要必要字段：`account`、`password`
- 插件未加载时，明确告诉用户下一步该做什么
- 成功返回新闻后，先给简明摘要；如果内容较多，再按条列出重点
