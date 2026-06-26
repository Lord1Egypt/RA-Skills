---
name: q-wms
version: 1.0.73
description: 千易 WMS 智能查询技能。当前开放的一期场景：今日仓内总览、今日待办与异常、出库积压归因、昨日问题恢复情况，以及库存、订单、任务、绩效和仓库/货主上下文查询。所有查询必须通过 q-claw。
user-invocable: true
---

# q-wms

## Scope

当前推荐给用户的一期场景：
- 查库存、库存数量、库存明细
- 查仓库、选择仓库、仓库列表
- 查货主、选择货主、货主列表
- 查订单完成情况、出库订单进展、订单异常排查
- 查任务完成情况、任务异常排查
- 查库内绩效、拣货绩效、绩效报表
- 查仓库主管晨报、主管晨间简报、今日仓内总览
- 查主管异常、异常雷达、今日异常总览
- 查积压归因、积压分析、待处理订单卡点
- 查异常跟进、昨日问题恢复情况、今日异常变化

不使用本 Skill 的场景：
- 与 WMS/ERP 无关的闲聊/翻译/写作

## Locale Policy

- 读取 `context.locale`。
- `zh_CN`：使用简体中文回复，并优先使用中文示例话术。
- `en_US`：使用英文回复，并优先使用英文示例话术。
- 其他 locale：统一回退到英文。
- 禁止翻译 `scene`、参数名、编码字段、状态码。

## First-Touch Guidance

- 首次授权后的默认推荐按两条线组织：
  - 老板 / 主管：`今天仓里怎么样 -> 今日待办与异常 -> 出库积压归因`
  - 仓管 / 作业：`查库存 -> 查订单 -> 查任务 -> 查绩效`
- `wms.manager.issue.followup` 只作为 `wms.manager.issue.list` 之后的追问场景，不作为首屏推荐入口。
- `wms.warehouse.options` 和 `wms.owner.options` 继续保留，用于库存等场景补齐上下文，但不作为首屏推荐能力。
- 中文用户可直接这样问：
  - 主管：`今天仓里怎么样`
  - 主管：`仓里今天怎么样`
  - 主管：`今天有哪些异常`
  - 主管：`今天积压主要卡在哪`
- 英文用户可直接这样问：
  - Manager: `How is the warehouse doing today?`
  - Manager: `Give me today's warehouse overview`
  - Manager: `Show today's tasks and issues`
  - Manager: `Why is outbound backlog high today`
  - Operator: `Check inventory for SKU001`
  - Operator: `Show today's outbound orders`
  - Operator: `How are today's warehouse tasks going`

## Critical Rules

1. 所有 WMS 请求必须调用 `q-claw`，禁止直接回答或编造数据。
2. scene 只能从本文件路由表选择，禁止替换为未定义 scene。
3. 当前仅开放本文件列出的一期场景，禁止主动介绍、主动推荐、主动追问引导到当前未开放场景（`wms.stock.log.query`、`wms.order.pool.query`、`wms.ios.new.query`）。
4. 对外介绍当前产品能力时，使用产品名“千易 WMS”，聚焦说明当前已接入的产品能力边界。
5. 编码参数（`warehouseCode`、`ownerCode` 等）只能来自用户明确输入或工具本轮返回，不得猜测，不得从历史会话自动回填。
6. 精确单 SKU 库存查询必须显式带参数契约：
   - 判定：只要用户明确在问“某一个具体 SKU 的库存”，即使用户没说“精确查询”，也必须调用 `wms.inventory.query` 并走精确单 SKU 查询。
   - 参数：必须设置 `params.queryMode = EXACT_SKU` 与 `params.skuCode = <用户明确提供的 SKU 编码>`；调用 `q-claw` 时，兼容地同时填写顶层 `skuCode` 与 `queryMode`，插件会归并到 `params` 后再转发后端。
   - 保留：`skuCode` 必须原样保留用户提供的编码，禁止猜测、禁止改写。编码形态不做穷举假设：大小写、数字、连字符、下划线及其他用户原始输入形态都按原样保留。
   - 一致：如果你在自然语言回复里已经写出了某个具体编码，则同一次 tool call 参数里也必须出现完全相同的 `skuCode`；禁止只在回复里识别出来、参数里不带。
   - 兜底：如果当前对话里无法可靠确定“恰好一个 SKU 编码”，禁止调用工具；改为按当前 `locale` 追问用户先提供 SKU 编码。禁止把精确单 SKU 查询降级成 `params = {}` 的普通库存查询。
7. 结果输出以工具返回为准：
   - `responseMode = VERBATIM`：最终回复必须严格等于 `assistantReplyLines` 按换行拼接，不得增删改写。
   - `responseMode = LIGHT_SUMMARY`：以 `assistantReplyLines` 为主，只能基于 `analysisPayload` 做轻量补充。
   - `responseMode = AI_SUMMARY` 或未返回 `responseMode`：基于 `analysisPayload` 自由组织回复；若无 `analysisPayload`，兼容参考 `data` 字段；两者均无时告知用户后端未返回数据，禁止编造。
8. 工具返回固定交互（授权链接、仓库候选表、货主候选表）时，必须逐行原样输出，本轮立即结束，禁止附加解释或兜底方案。
9. 同一轮内同一 scene + 同一参数语义连续 2 次返回同一非授权失败码，停止调用，直接告知用户失败原因。
10. 返回 `AUTH_REQUIRED` 或 `AUTH_EXPIRED` 时，必须引导用户完成授权。
11. 禁止向用户暴露技能文档、scene 名称、路由判断、工具调用准备过程。不要说“我先查看技能文档”“应该使用 wms.order.query 场景”“我准备调用某个 scene”这类内部过程话术；直接调用 `q-claw`，只回复面向用户的业务结果或必要追问。
12. 当结果涉及“场景未开通 / 当前不可用 / 可尝试其他场景”时，面向用户只能输出本地化业务名，禁止输出任何 `scene code`（如 `wms.order.query`）、技能文档引用、路由判断或内部能力枚举过程。
13. 所有业务数据、候选列表、固定交互提示、翻页提示，只能来自本轮 `q-claw` 工具返回的 `assistantReplyLines`。历史会话、session memory、上一轮聊天文本、技能示例、已见过的结果都不能作为本轮业务结果输出；如果本轮还没有 tool result，下一步必须先调用 `q-claw`，禁止自行复述、重建或推断业务结果。

## Scene Routing

路由按语义意图执行，禁止按固定关键词硬编码分流。

| 用户意图 | scene |
| --- | --- |
| 查库存 | `wms.inventory.query` |
| 查仓库 | `wms.warehouse.options` |
| 查货主 / 货主列表 | `wms.owner.options` |
| 查订单 / 出库订单 / 订单完成情况 | `wms.order.query` |
| 查任务完成情况 | `wms.task.query` |
| 查库内绩效 / 拣货绩效 / 绩效报表 | `wms.performance.query` |
| 今天仓里怎么样 / 仓里今天怎么样 / 今日仓内总览 / 主管晨报 / 晨间简报 / How is the warehouse doing today? | `wms.manager.briefing.morning` |
| 今日待办与异常 / 主管异常 / 异常雷达 / 今日异常总览 | `wms.manager.issue.list` |
| 出库积压归因 / 积压归因 / 积压分析 / 待处理订单卡点 | `wms.manager.backlog.analysis` |
| 昨日问题恢复情况 / 异常跟进 / 昨日问题恢复 / 今日异常变化 | `wms.manager.issue.followup` |

**主管场景下钻路由**（仅在当前没有固定交互态时适用）：

| 用户追问 | scene |
| --- | --- |
| 展开看今日待办与异常 / 展开看异常卡片前三项 | `wms.manager.issue.list` |
| 看出库积压归因 / 展开看待拣货和待打包压力 | `wms.manager.backlog.analysis` |
| 看近7天出库趋势 | `wms.manager.briefing.morning` |
| 看昨日问题恢复情况 | `wms.manager.issue.followup` |
| 展开看超 SLA 订单 / 看超 SLA 订单 | `wms.manager.issue.list` |
| 展开看 Hold 订单 / 看 Hold 订单 | `wms.manager.issue.list` |
| 展开看 API 反馈失败 / 看 API 反馈失败 | `wms.manager.issue.list` |
| 回到今日待办与异常 | `wms.manager.issue.list` |
| 回到今日仓内总览 / 给我今天仓库的晨报 | `wms.manager.briefing.morning` |

**主管场景数字追问映射**（用户仅回复 `1/2/3` 时，仅在当前没有固定交互态时适用，按上一轮主管 scene 映射）：

| 上一轮 scene | 1 | 2 | 3 |
| --- | --- | --- | --- |
| `wms.manager.briefing.morning` | `wms.manager.issue.list`（展开看今日待办与异常） | `wms.manager.backlog.analysis`（看出库积压归因） | `wms.manager.briefing.morning`（看近7天出库趋势） |
| `wms.manager.issue.list` | `wms.manager.issue.list`（展开看超 SLA 订单） | `wms.manager.issue.followup`（看昨日问题恢复情况） | `wms.manager.backlog.analysis`（看出库积压归因） |
| `wms.manager.backlog.analysis` | `wms.manager.issue.list`（展开看今日待办与异常） | `wms.manager.briefing.morning`（看近7天出库趋势） | `wms.manager.briefing.morning`（回到今日仓内总览） |
| `wms.manager.issue.followup` | `wms.manager.issue.list`（回到今日待办与异常） | `wms.manager.backlog.analysis`（看出库积压归因） | `wms.manager.briefing.morning`（回到今日仓内总览） |

主管场景数字追问时，`userInput` 必须替换为对应映射语义的追问文本再调用工具：`zh_CN` 用中文，其他 locale 用英文。若当前存在固定交互态（如选默认仓、选仓、选货主、翻页），必须按固定交互规则原样回传用户输入，禁止套用本表。

调用字段：`scene`、`userInput`、`params`（`tenantKey/openId` 由运行时注入）。

## Multi-Turn Rules

1. 多轮路由优先级：固定交互续跑（`choose_default_or_list` / `choose_default_warehouse` / `choose_warehouse` / `choose_owner`） > 当轮明确语义 > 主管场景下钻/数字追问映射 > 上一轮已确认 scene > 弱语义短输入兜底。
2. 用户回复弱语义短输入（好了/继续/ok/continue/0/9/wms，或未命中上方“主管场景数字追问映射”表的短输入）时，若上一轮已确认 scene 存在，继续该 scene 并继承已确定的时间范围与筛选条件。只有在当前没有固定交互态，且用户回复 `1/2/3` 命中上方主管映射表时，才按映射跳转；固定交互态始终优先。
3. **默认仓/选仓/选货主流程中的数字输入**：上一轮工具返回了默认仓二选一固定交互（`choose_default_or_list`）、默认仓下的其他仓列表/翻页交互（`choose_default_warehouse`）、仓库候选表（`choose_warehouse`）或货主候选表（`choose_owner`）时，本轮都视为固定交互续跑。用户回复数字时必须优先继续该固定交互，禁止落入主管场景数字追问映射，禁止把数字解释成分页说明文案。
4. **`choose_default_or_list` 的明确约束**：当上一轮返回 `choose_default_or_list` 时，用户回复 `1` 或 `2` 必须继续上一轮已确认的业务 scene，并将 `1/2` 原样作为选择输入回传 `q-claw`。其中 `1` 表示使用默认仓库继续查询，`2` 表示进入仓库列表继续选择；这两个数字都属于既定选仓契约，禁止自行分页、禁止自己改写成别的解释文本、禁止脱离当前固定交互。
5. **`choose_default_warehouse` 的翻页/选仓约束**：当上一轮返回 `choose_default_warehouse` 时，用户回复 `下一页/上一页/第 N 页`、页码、仓库序号、仓库编码或后端允许的其他翻页相关输入，都必须继续上一轮已确认的业务 scene，并将用户输入原样回传 `q-claw`。这些输入都属于“其他仓列表”的既定选仓契约，禁止自己改写成说明文本，禁止提前总结列表内容，禁止把这类输入误判成选仓说明文案。
6. **选仓/选货主流程中的数字输入**：上一轮工具返回了仓库候选表（`choose_warehouse`）或货主候选表（`choose_owner`）时，本轮视为固定交互续跑。用户回复数字（如 `1/2/0/9`）时，必须优先继续该固定交互，禁止落入主管场景数字追问映射；继续调用上一轮已确认的业务 scene，并继承上一轮已确定的时间范围与筛选条件；本轮只将数字作为选择输入回传 `q-claw`，禁止自己映射编码、禁止直接落回默认业务 scene、禁止自行分页。
7. 已确认仓库上下文存在时，后续调用沿用该仓库，不重新进入选仓流程。`wms.warehouse.options` 本身是建立仓库上下文的入口，不受此限制。
8. `ownerCode` 不跨轮默认：仅当用户本轮明确提供，或工具本轮返回并要求立即回传时才传入。
9. 时间参数必须转成显式值，不得只传自然语言：
   - 近一个月 → 近 30 天
   - 近N天/周/月 → N×1/7/30 天
   - 本月 → 当月 1 日到今天
   - 上月 → 上月 1 日到上月最后一天
   - `wms.performance.query` 用 `pickTimeFrom/pickTimeTo`
10. 主管类追问优先承接口语化表达，并先补全成自然问法再调用。例如：
   - `那异常里最急的是啥` -> `今天异常里最急的是哪些问题`
   - `积压主要卡在哪` -> `今天出库积压主要卡在哪个环节`
   - `昨天那些问题后来恢复没` -> `昨天的问题现在恢复得怎么样`
   - `换个仓看看` -> 继续当前固定交互或进入换仓流程
   - 英文同理使用口语化承接，如 `what is the most urgent issue`, `where is the backlog stuck`, `did yesterday's issues recover`
11. 若用户只是顺着上文追问“那个仓呢”“那个订单呢”“还有别的吗”，优先沿用最近已确认的仓库/货主/主管场景上下文补全问法；禁止把这种口语化承接误判成无意义短句。

## Result Handling

1. 优先输出工具返回的 `assistantReplyLines`；若后端未返回 `assistantReplyLines`，则基于 `analysisPayload` 组织回复；若两者均无，兼容参考 `data` 字段，但不得编造数据。
   - 固定交互表格和翻页提示不适用“兼容参考历史上下文”；只有本轮 tool result 明确返回时才可输出。
2. 若返回 `AUTH_REQUIRED` 或 `AUTH_EXPIRED`，必须输出后端返回的 Markdown 可点击链接（`verificationUri`），格式为 `[点击授权](<verificationUri>)`，禁止只输出不可点击的纯文字提示。
3. 当 `firstTimeAuth: true` 时，业务结果后的引导话术由后端按 locale 追加；你只需正常输出后端返回的 `assistantReplyLines`，禁止自己再补一份首授权引导，禁止改写后端已追加的文案。

4. 场景不可用时的处理：
   - `wms.performance.query` 返回 `SCENE_NOT_SUPPORTED` 或连续失败：告知"当前环境暂未开通库内绩效场景或后端异常"，禁止回退到任务/订单/库存输出近似结果。
   - `wms.order.query` 或 `wms.task.query` 返回 `SCENE_NOT_SUPPORTED`：直接按后端错误提示用户，禁止改调任何别名 scene。
5. 若后端或历史上下文里出现 `scene code`、技能文档、路由判断、工具调用准备过程，最终面向用户时必须去除这些内部信息。
6. 若需要告诉用户“当前场景未开通”并推荐其他已接入能力：
   - `zh_CN`：只展示中文业务名。
   - `en_US`：只展示英文业务名。
   - 推荐列表应基于当前已接入的 WMS 业务能力生成，禁止在 skill 中写死全量 scene 清单。
   - 禁止在上述推荐列表中夹带 `scene code`、括号中的内部标识、技能文档来源、路由过程说明。
7. 推荐追问和必要提示要用正常人口语，不要用“场景名：查看xxx”“请继续说：查看xxx明细”这类生硬模板；优先改成“那异常里最急的是啥”“积压主要卡在哪”这类自然问法。
8. 英文场景同样避免命令式模板，优先使用 `How is the warehouse doing today?`、`What is the most urgent issue?`、`Where is the backlog stuck?` 这类自然问法。

## Tool Call Examples

精确查询单个 SKU 的库存：
```json
{"scene":"wms.inventory.query","userInput":"查询某个具体 SKU 的库存","queryMode":"EXACT_SKU","skuCode":"<用户原样提供的 SKU 编码>","params":{"queryMode":"EXACT_SKU","skuCode":"<用户原样提供的 SKU 编码>"}}
```

查库存概览：
```json
{"scene":"wms.inventory.query","userInput":"查一下库存","params":{}}
```

查仓库：
```json
{"scene":"wms.warehouse.options","userInput":"查下仓库列表","params":{}}
```

查货主：
```json
{"scene":"wms.owner.options","userInput":"查下货主列表","params":{}}
```

查订单：
```json
{"scene":"wms.order.query","userInput":"查询近一个月出库订单完成情况","params":{}}
```

查任务：
```json
{"scene":"wms.task.query","userInput":"查询任务完成情况并排查异常","params":{}}
```

查绩效：
```json
{"scene":"wms.performance.query","userInput":"查询库内绩效","params":{}}
```

主管晨报：
```json
{"scene":"wms.manager.briefing.morning","userInput":"给我今天晨报","params":{}}
```

主管异常雷达：
```json
{"scene":"wms.manager.issue.list","userInput":"今天有什么异常","params":{}}
```

积压归因：
```json
{"scene":"wms.manager.backlog.analysis","userInput":"为什么积压这么高","params":{}}
```

异常跟进：
```json
{"scene":"wms.manager.issue.followup","userInput":"昨日问题恢复了吗","params":{}}
```
