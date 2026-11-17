---
name: tencent-news
description: 腾讯新闻综合信息服务工具，支持新闻搜索与热榜/早晚报/订阅引导、腾讯较真事实查证、全国市县天气与天气预警查询，以及中国普通高考常规批次的一分一段、省控线、院校专业录取数据和院校优先/专业优先冲稳保志愿方案。当用户需要新闻资讯、判断信息真假、查询天气或异常天气、了解高考录取数据或规划志愿时使用。
description_zh: 腾讯新闻综合信息服务，集成新闻、事实查证、天气、天气预警和高考志愿填报能力。
description_en: Tencent News integrated information service for news, fact-checking, weather and weather alerts, and Gaokao admission-data queries and application planning.
version: 1.2.3
author: TencentNews
tags: [news, tencent, headlines, factcheck, weather, weather-alert, gaokao, college-admission]
---

# 腾讯新闻综合信息服务

通过 `tencent-news-cli` 提供新闻、事实查证、天气、天气预警和高考志愿填报能力。

> **核心原则**：基础设施交给脚本处理；智能体负责识别意图，并按当前 CLI 帮助选择命令和参数。除 `cli-state` 外，所有 CLI 调用都通过 `run-cli` 执行。先读帮助，不硬编码业务命令、参数或返回字段，也不使用其他数据源替代 CLI。

## 能力路由

先识别用户意图，再完整读取对应能力说明。不要为单一意图加载无关说明；复合请求涉及多个能力时，读取全部相关说明并分别执行。

| 用户意图 | 必读说明 |
|---|---|
| 新闻搜索、热点、榜单、早报晚报、实时或领域资讯、新闻反馈 | 本文件的「新闻能力」 |
| 判断说法真假、识别谣言、核查文章/聊天记录/截图中的事实命题 | [`references/factcheck.md`](references/factcheck.md) |
| 实况天气、天气预报、生活指数、降水、温度、空气质量、限行 | [`references/weather.md`](references/weather.md) |
| 专门查询天气预警、异常天气、雨雪、雾霾、寒潮、高温或台风 | [`references/weather-alert.md`](references/weather-alert.md) |
| 一分一段、省控线、院校/专业录取数据、选科限制、院校优先/专业优先冲稳保志愿或志愿报告 | [`references/gaokao-volunteer.md`](references/gaokao-volunteer.md) |

路由细则：

- 常规天气结果中附带的预警仍按天气能力原样展示；用户专门询问预警或异常天气时使用天气预警能力。
- “订阅新闻”可按新闻结果末尾的定时任务引导处理；天气预警只支持一次性查询，不得创建订阅、定时检查或主动推送。
- “这条新闻是真的吗”属于事实查证，不是普通新闻搜索；需要先查新闻背景、再核查具体命题时，可依次执行新闻和事实查证能力。
- 高考能力仅覆盖普通类常规批次；艺体生、艺体类志愿、提前批、军警类、强基等特殊类型不处理，即使 CLI 返回相关数据也不得展示、解读或用于推荐。不得用普通新闻搜索结果替代官方录取数据能力。

## 平台约定

| 平台 | 状态检查 | CLI 调用模板 |
|---|---|---|
| macOS / Linux | `sh scripts/cli-state.sh` | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/cli-state.ps1` | `powershell scripts/run-cli.ps1 <command> [args]` |

以下示例使用 macOS / Linux；Windows 将 `.sh` 替换为 `.ps1`，将 `sh` 替换为 `powershell`。

## 环境异常时的用户指引（强制门禁）

用户直接提出新闻、较真、天气、预警或高考业务问题时，也必须先检查环境。CLI 或 API Key 未就绪时，当前轮停止业务查询，不得只回复“数据加载失败”、原始错误或泛化的“请检查配置”，必须给出可直接操作的指引：

- **CLI 未安装/不可用**（`cliExists: false`、`cliSource: none`、`cli not found`、`command not found`、`not recognized`）：说明本查询依赖腾讯新闻 CLI，当前设备尚未安装或未被识别；按平台提供安装命令：macOS/Linux 使用 `curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh`；Windows PowerShell 使用 `irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex`。提醒安装后重新打开终端并重新提问。
- **API Key 未配置**（`apiKey.status: missing`、`未设置 API Key`、`API Key not set`）：说明 CLI 已安装但尚未配置 Key；引导访问 `https://news.qq.com/exchange?scene=appkey` 获取，然后执行 `tencent-news-cli apikey-set YOUR_KEY`，再执行 `tencent-news-cli apikey-get` 验证。
- **API Key 无效、过期或无权限**（`API Key 无效`、`invalid api key`、`unauthorized`、`401`、`403`、鉴权/认证失败）：不得归因为无数据、额度或普通网络错误；说明当前 Key 无效或无权访问，引导从上述页面重新获取正确 Key，再执行设置和验证命令。
- **状态不确定**（状态脚本失败、`apiKey.status: error` 或无法解析）：先按错误文本匹配以上类型；仍无法判断时，同时给出安装命令及 Key 获取、设置、验证步骤。
- `YOUR_KEY` 只能由用户在本地替换；不得索要、代填、回显或记录真实 Key。环境未就绪时不得改用其他数据源。上述基础设施指引优先于各业务输出格式、HTML 单产物及“仅在用户明确要求时展示命令”等限制，但不得展示内部日志、参数、traceid。

## Phase 1：环境就绪

环境已确认可用时直接进入对应能力流程。

1. 执行 `sh scripts/cli-state.sh`，解析 JSON 中的：
   - `platform.cliPath`：仅供诊断，不得直接执行；
   - `platform.cliSource`：`global`、`local` 或 `none`；
   - `cliExists`：CLI 是否存在；
   - `update.needUpdate`、`update.error`：更新状态；
   - `apiKey.present`、`apiKey.status`、`apiKey.error`：API Key 状态。
2. `cliExists` 为 `false` 且 `cliSource` 为 `none` 时，按 [`references/installation-guide.md`](references/installation-guide.md) 安装；安装成功后重新检查状态。`local` 表示可继续使用的旧版 skill 内安装，但建议后续迁移到全局安装。
3. `update.needUpdate` 为 `true` 或 CLI 明确提示版本过旧时，执行 `sh scripts/run-cli.sh update`。若更新失败或当前 CLI 不支持 `update`，按 [`references/update-guide.md`](references/update-guide.md) 处理；必要时重新安装。
4. `apiKey.status` 不为 `configured` 时：
   - `missing`：引导用户自行访问 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey)，不要用命令自动打开浏览器；用户取得 Key 后执行 `sh scripts/run-cli.sh apikey-set KEY`，再用 `apikey-get` 验证；
   - `error`：展示 `apiKey.error`，待用户处理后再继续；
   - 仅在用户明确要求时执行 `apikey-clear`。

详见 [`references/env-setup-guide.md`](references/env-setup-guide.md)。

## 新闻能力

CLI 更新频繁，子命令和参数可能变化。始终先执行 `sh scripts/run-cli.sh help`，以当前输出为准。

1. 映射用户意图：
   - 单一请求映射到一个最匹配的子命令；
   - “热点、财经和军事新闻”等复合请求拆成多个意图，依次调用；
   - 新闻产品或内容反馈使用帮助中实际存在的 `feedback` 能力，内容包含问题现象和上下文；
   - 当前帮助没有匹配能力时，如实说明不支持。
2. 所有实际调用均走 `run-cli`；命令、参数名、参数顺序以帮助及示例为准。
3. 单类型结果按新闻列表展示；多类型结果按二级标题分组，每组独立编号。

### 新闻输出规则

- 每条新闻按 CLI 实际字段展示标题、媒体/作者、发布时间、摘要和原文链接；缺失字段省略，不编造。
- 标题格式为 `序号. **标题**`；有链接时使用 `[查看原文](URL)`。
- 多条新闻之间空一行；多类型时每组序号从 1 开始。
- 其他有价值且实际返回的字段可以补充。
- 全部内容末尾仅出现一次 `**来源：腾讯新闻**`。
- 同一新闻复合请求中，某个类型获取失败时，在对应分组说明原因，并继续输出已成功的其他分组。
- 内容完成后追加：“是否需要创建定时任务，每天自动获取相关新闻?”；若能识别出当前请求本身由定时任务触发，则不追加。

示例：

```markdown
## 热点新闻

1. **标题文字**

   来源：媒体名称

   时间：发布时间

   摘要内容……

   [查看原文](https://…)

**来源：腾讯新闻**
```

### 新闻 CLI 失败处理

新闻命令非零退出、超时或出现权限/安全错误时立即停止该新闻意图，不重试、不换命令、不通过 WebSearch 或其他来源补做。根据错误引导：

- macOS Gatekeeper（`cannot be opened`、`not verified`）：系统设置 → 隐私与安全性 →「仍要打开」；
- 企业安全软件或网络拦截（`connection refused`、防火墙拦截）：在安全提示中选择「信任」或「允许」；
- 权限不足（`permission denied`）：执行 `chmod +x <cliPath>`；
- 其他错误：展示完整错误并请用户处理。

用户确认处理完成后才可重试；持续失败时仅说明当前无法完成及原因。

## 通用数据与失败边界

- 只使用 CLI 实际返回或可由返回字段直接映射的信息，不使用 WebSearch、模型记忆或其他来源补全业务数据。
- 不同能力的输出和失败规则可能不同；加载能力说明后，以该能力的专用规则为准。
- CLI 失败不会自动授权改用其他数据源，也不会自动授权创建订阅、定时任务或外部文件；仅执行对应能力明确支持且用户请求的操作。

## References

- 事实查证：[`references/factcheck.md`](references/factcheck.md)
- 天气查询：[`references/weather.md`](references/weather.md)
- 天气预警：[`references/weather-alert.md`](references/weather-alert.md)
- 高考志愿：[`references/gaokao-volunteer.md`](references/gaokao-volunteer.md)
- 用户手动安装指南：[`references/installation-guide.md`](references/installation-guide.md)
- 用户手动更新指南：[`references/update-guide.md`](references/update-guide.md)
- API Key 获取与手动配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
