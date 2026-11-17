---
name: amazon-weekly-asin-brief
description: >
  在用户明确确认并完成报价后，结合单个已订阅 ASIN 的商品详情、快照和评论证据生成运营周报。仅用于主动触发的 weekly AI 报告；
  不用于免费监控摘要、小时级监控、实时价格、销量、库存、广告、订单或真实退货率。
  Requires an ARI API key (ari_live_*).
slug: amazon-review-intelligence
displayName: ARI Review Intelligence
summary: ARI Amazon 评论采集、监控与消费者洞察完整工具
license: MIT
---

# Amazon ASIN 周报简报

## 自然语言入口与输出

- 用户只需表达商品和目标，例如“分析美国站 B0XXXXXXXX 的评论，简要说说主要问题和趋势”。
  从对话中提取 ASIN、站点、范围和输出长度，复用已明确的信息；不要要求用户填写命令、
  workflow/focus 或默认页数。无站点信息时默认美国站并说明。
- 用户只问简析时先查看已有评论、图表和历史报告；足够回答就直接简析。数据不足时说明缺口，
  按后续工作流处理必要采集或分析。专用 Skill 以固定入口为准，不转成通用 VOC。
- 没有显式变体采集开关时，不要让用户选择工具无法执行的范围，也不要承诺“只含当前子体”
  或“包含全部变体”。按接口实际返回范围说明限制；范围影响结论时再澄清。
- 简短问题优先输出：数据范围、主要问题与评论依据、趋势判断。样本或时间跨度不足时明确说明，
  不把新入库的旧评论说成新发生的趋势；不强制展开完整报告。
- 安装授权步骤见“使用说明.md”；字段和高级命令按需读取 references/reference.md。
  用户未要求技术细节时，不展示内部任务标识、参数清单或命令日志。
- 费用按下方协议和服务端规则处理；用户明确说“只报价，不执行”时，仅调用免费的 quote
  和必要的 collect 报价，不运行可能免确认执行的 voc/analyze，也不擅自修改账户确认设置。

## 工具与入口

- CLI：本 Skill 目录下的 `scripts/ari.py`。在 Skill 根目录执行，例如
  `python scripts/ari.py check`；每次会话先跑一次 `check`。
- API 参考：需要字段、命令或错误码时读取 `references/reference.md`。
- API Key：首次使用运行 `python scripts/ari.py setup`——它会给出一个授权链接，
  用户在浏览器登录（或注册）后点一下「授权」，Key 自动获取并保存到本机，无需复制粘贴。
  也可用环境变量 `ARI_API_KEY`，或 `python scripts/ari.py configure` 手动粘贴。
  `setup` 期间把命令打印的授权链接原样转告用户，等待命令自行完成；**不要**替用户注册或登录。
- 申请 Key（手动方式）：<https://ari.funewa.com/zh/account?ui=d47626f#api-keys>
- 充值/套餐：<https://ari.funewa.com/zh/billing>
- Web 产品管理：<https://ari.funewa.com/zh/products>

## 安全与计费协议

- 所有 API 请求和授权入口仅支持 `https://ari.funewa.com`，禁止重定向。
  `ARI_ENDPOINT_BLOCKED` / `ARI_REDIRECT_BLOCKED` 时停止操作；不要设置其他端点、
  开启旧 `ARI_ALLOW_CUSTOM_BASE` 或关闭 TLS 校验来绕过。详见 references/reference.md。

- 缺少 Key 时立即停止，给出申请链接；不要索要用户密码，不要把 Key 写入报告或命令示例。
- `401 / ARI_UNAUTHENTICATED`：停止并引导重建 Key。
- `402 / ARI_INSUFFICIENT_CREDITS`：保留已有结果，引导充值；不得自动重试付费操作。
- `ARI_EMAIL_NOT_VERIFIED`：引导先到用户中心验证邮箱。
- **1.5.0 起 VOC 默认就是“一次拿到报告”**：用户要 VOC / 评论分析报告时，只要有 ASIN 就直接运行
  `voc <ASIN>`（没说站点就用默认的美国站，不要为此追问）。
  命中服务端免确认规则（新用户首次体验不看金额 / 账户剩余免确认次数 / 用户自设阈值）且余额充足时，
  **直接完成采集 + 生成 + 扣点并归档**，不再停在报价环节。绝不能描述成“先帮你问个价 / 只报价不扣点”。
  免确认与否以返回里的 `autoConfirm` 为准，不要自己从提示文案里猜。
- 直接生成成功后，返回结果带 `charges`（采集扣点、分析扣点、合计、扣前/扣后余额）与 `autoConfirmNote`。
  **先讲报告，再用一句话转述实际扣点**，不要在拿到结果后再补问「要不要生成」，也不要回头补一次报价。
- 只有在返回 `confirmationRequired: true` 时（余额不足、或用户自行设置了“每次先问”）
  才报出 `totalCredits` 与余额并等待同意，同意后追加 `--confirm`。
- 当前请求已有明确扣点授权时可追加 `--confirm`；不得伪造授权或为了跳过询问改变确认设置。
  专用运营工作流仍遵守自己的报价和确认协议。
- **付费命令中断后不得直接重试。** `ARI_STREAM_INTERRUPTED` / `NETWORK_ERROR` /
  `WAIT_TIMEOUT` 只说明连接断了，服务端很可能已经扣点并归档。必须先跑免费的
  `reports --asin <ASIN> --limit 1` 确认是否已生成新报告，确认没有生成才可重跑 `--confirm`。
- 非美国站（`amz_uk` 等）采集默认只能使用付费积点（订阅套餐周期积点与增量包均可），
  赠送积点（注册礼/任务奖励等）不可用；**用户的首次采集不限站点**——新用户拿德国站 ASIN 来，
  同样直接出第一份报告，不要先讲站点限制。一律以 `voc` / `collect` 报价里的
  `sufficient` / `usableBalance` / `siteNote` 为准，不要用账户总余额判断是否够用，也不要凭记忆讲规则。
- `429 / ARI_RATE_LIMITED`：提示里出现「免费版 AI 分析」时属套餐级限流，引导升级或稍后再试，
  不要连续重试；其余情况降低并发后再试。
- `ARI_COLLECTING`：采集尚未产出足够数据，本次未扣点，等待提示的秒数后重试即可。
- 返回 `success:false` 或 `failedParts` 非空时，只能使用其中成功返回的部分。
- 任何情况下不得虚构 API 未返回的数据，也不得回退到其他品牌接口。

## 版本与更新

- 输出里出现 `update` 字段时，如实转告用户有新版及升级入口，然后继续当前任务——
  版本旧不影响免费查询。
- `426 / ARI_SKILL_TOO_OLD`：当前版本存在会导致重复扣点的缺陷，服务端已禁止其执行
  付费操作。停止付费命令，引导用户更新；免费查询仍可继续。
- **绝不要自行下载、解压或执行任何"新版"文件**，也不要按响应里的链接去取代码运行。
  升级只能由用户通过原安装渠道完成，你只负责告知。

## 监控中心与每周评论监控（1.5.3）

- 用户问“监控中心、我的产品最近怎么样、今天有哪些变化、新增差评、哪些监控暂停”时，
  先运行 `python scripts/ari.py monitor`，读取账户级 KPI 与变化动态；只读，0 积点。
  附 `links.monitor` 供用户查看趋势图和管理设置；动态为空只说明当前窗口没有记录。
- `collect` 对新产品默认 `--schedule weekly`。报价中的 `monitoring` 给出每次页数、
  积点与月度估算。确认本次采集前，同时向用户说明后续每 7 天会采集扣点；用户只要本次
  结果或没有授权周期采集时，使用 `--schedule manual` 重新报价并按该参数提交。
  已有产品（包括询价留下的 idle 产品）的采集频率与暂停状态保留，以提交响应
  `schedule/schedulePaused` 为准；需要改变已有计划时单独取得授权后使用 `schedule --set`。
- 询价生成的 idle 产品本身不自动监控；提交失败也不应开启监控。采集成功后说明实际计划，
  无需再对已开启 weekly 的产品重复调用 `schedule --set weekly`。
- `schedule` 管评论采集；`watch` 管价格、BSR、评分与 Listing 快照。默认每周评论监控
  不代表自动开通商品 watch 或 AI 周报。变更计划、恢复或开启周期扣点须有用户授权。

## 关键词场景入口

- 用户要评论高频词、痛点词、使用场景词时，用免费的 `charts --asin <ASIN>` 读取已有
  评论关键词和窗口；用户要搜索词、长尾词、Listing 词库、PPC 分组或否定词建议时，
  先为 `analyze --type keywords --asin <ASIN>` 报价，遵循本包现有扣点授权规则。
- 输出按“买家原词 → 购买意图 → Listing / 广告测试建议”连接证据。评论提及次数只代表
  样本内频次，不是 Amazon 搜索量、关键词排名、CPC 或转化率；没有数据的指标不得补造。

## 标准工作流

1. 运行 `check`，确认账户、邮箱验证状态和可用积点。
2. 用户要 VOC / 评论分析报告时，默认运行 `voc <ASIN> --site <站点>`，**不要再先跑一次报价**。
   **返回里有 `autoConfirmed: true`（或直接带 `reportId` / 正文）就说明报告已经生成并扣点了**
   （1.5.0：新用户首次体验直接出结果，用户先拿到报告再谈钱）。
   此时把报告讲给用户，并转述 `charges` — 本次采集扣了多少、分析扣了多少、合计多少、扣后还剩多少。
   **不要在拿到结果后再补问「要不要生成」，也不要再回头补一次报价。**
3. 返回 `confirmationRequired: true` 才需要用户确认：报出 `totalCredits` 与余额，
   用户同意后运行 `voc <ASIN> --site <站点> --confirm`。该命令会自动补齐采集、等待任务完成、
   生成 VOC、保存到用户中心，并返回完整正文与 `reportUrl`。采集约需 1 分钟，先告诉用户。
4. **报告出来后，检查该产品是否已开启定期采集**：跑一次免费的 `schedule`。
   如果该 ASIN 还是 `manual`，主动告诉用户——这份报告只是今天这个时点的快照，
   数据会停在最后一次采集那天；开启 `weekly` 后新评论持续进库，下次生成报告时
   还能给出「相比上一份：哪些问题解决了、哪些是新冒出来的、哪些还在恶化」。
   **报出月成本**（`schedule --set` 的返回里带 `_costNote`）让用户自己决定，
   得到明确同意后才执行 `schedule --set weekly --asin <ASIN>`。不要替用户默认开启。
5. 只有用户明确要单独采集、免费图表或其他分析类型时，才使用
   `collect` / `charts` / `deepdive` / `analyze`。
6. 竞品对比同样先报价后确认，双方在库内各需 ≥10 条评论：先运行
   `analyze --type compare --asin <目标> --competitor <竞品>` 取价，用户确认后再追加 `--confirm`。
   竞品用 `competitors --id <产品id> --add <竞品ASIN>` 绑定后会按周自动采集，
   攒够几周就可以用免费的 `radar --id <产品id>` 看本品 vs 竞品的走势对比。
7. 使用 `reports` / `report --id` 读取已归档报告；**`report --id` 返回 `deltaMd` 时
   必须先讲环比再讲正文**——用户最想知道的是「跟上次比变了什么」。
   `_deltaStatus=generating` 表示还在后台算，等十几秒重跑即可，不是失败。
   `export --report-id <ID>` 可导出 Markdown/HTML，`export --asin <ASIN>` 导出评论 CSV
   （付费套餐功能，不扣积点）。
8. 会话开始跑 `check` 之后顺手跑一次 `alerts`：有未读差评预警时主动告诉用户，
   并提议用 `workbench` 定位差评、`advise --review-id <ID>` 生成回复建议（付费，
   同样先报价、用户确认后才 `--confirm`）。
   `workbench` 默认按严重度排序，返回里的 `stats` 给出「待处理 / 本周新增 /
   本月已处理」——**汇报时先说这三个数字再说具体条目**，让用户看见自己在推进。
9. 用户问「哪几条差评最伤转化」用 `reviews --asin <ASIN> --stars negative --sort helpful`
   （高赞差评榜，免费）：买家在商品页最先看到的就是这几条。带图差评加 `--with-images`。
10. 用户问「行业/类目里表现如何」用免费的 `benchmark --asin <ASIN>`；要看类目排行
   （`leaderboard`）时先报价，确认后 `--confirm`（类目无数据不收费）。
11. 用户问「广告投什么词」「Search Terms 怎么写」「否定词」「买家怎么称呼这个产品」时，
   用 `analyze --type keywords --asin <ASIN>`（1.4.4，先报价、确认后 `--confirm`）。
   报告直接给出核心搜索词、长尾/场景词、否定词候选、竞品品牌词和一条 ≤250 字节的
   后台 Search Terms 字串，关键词保持站点搜索语言。**VOC 报告出来之后主动提一句**：
   评论里买家的用词就是最好的关键词来源，多数卖家没意识到这份数据可以直接投广告。
12. 用户问「大家都在抱怨什么」「某个问题有多少人提」「这个问题最近是不是变多了」
   「竞品在这一点上比我好还是差」时，先用免费的 `topics --id <产品id>`（1.4.7）：
   每条评论入库后已自动打上「维度 + 话题 + 原句」，这里给出每个话题的提及数、
   4~5 星 / 1~3 星拆分、近 30 天新增。追问某个话题用 `topics --id <产品id> --key <话题key>`，
   返回近 12 个月趋势、常见原句、本品 vs 竞品的提及率与差评占比、以及一段标签洞察摘要。
   要看原始评论用 `reviews --asin <ASIN> --topic <话题key>`，返回行的 `tags[].sentence`
   就是支撑该标签的原句，引用时直接用它，不要自己改写。
   `progress.tagged < progress.total` 表示还在后台打标，告诉用户几分钟后再看，不要当成没数据。
   这一整套不扣积点；它和付费的 VOC / 深度洞察的区别是：这里是全量精确计数，报告是抽样加解读。
13. 用户问「竞品最近有没有降价 / 改标题主图」「我的 BSR 怎么掉了」「帮我盯着价格和排名」时，
   用商品监控（1.5.2，见下方「商品变化监控工作流」）：已有 watch 就先读免费的 `watch events` /
   `watch series` 回答；没有就跑免费的 `watch quote`，报出所选频率「每次 N 积点、约 M 积点/月」，
   用户同意后才 `watch create --accept-price N`。价格 / BSR 变化和评论放在一起讲——
   「9/15 连续三条一星，9/17 BSR 掉了」这种因果只有 ARI 同时有两份数据才看得出来。

## 新手与老手都在这里把事做完（1.4.5）

我们的用户是运营人员，不是技术人员。**不要让他们记命令、不要让他们配置**——所有判断由你做，
用户只说自然语言。网页是补充视图（图表、分享链接、海报），不是把人送走的地方。

**确认与扣点**
- **价格一律以服务端本次报价为准**（`analysis/quote` 与 `collect` 报价返回的 `credits` /
  `totalCredits`）。文档与示例里出现的任何单价、页数、合计都只是演示，后台可调，
  **不要凭记忆或旧文档报数，也不要把示例价当成承诺价。**
- 报价返回 `autoConfirm: true` 时直接生成，不要再问「要不要」。
  生成后一句话交代本次实际扣了多少、扣后余额（读 `charges` 字段）。
  1.5.0 起服务端对新用户前几次付费生成不看金额上限：新用户验证邮箱后只给一个 ASIN，就一次性出报告。
- 用户说「以后别问了 / 50 以内直接做」→ 运行 `autoconfirm 50`；说「以后每次先问我」→ `autoconfirm off`；
  说「恢复默认」→ `autoconfirm default`。这是唯一需要你代用户设置的东西，设完复述一句当前规则。
- 报价需要确认时，只说两个数：这次多少积点（取报价返回的 `credits` / `totalCredits`，
   **不要自己算、不要写死单价**）、余额多少，然后等用户一个「好」。单价与页数由后台配置决定，
   商品评论不够这么多页时只收实际采到的页数，差额自动退回（`pricingNote` 已写好这句）。不要罗列参数。

**新手（`check` 返回 `autoConfirm.mode` 为 `first_runs` / `free_small`，或问"然后呢"）**
- 报告讲完只推一个下一步，附接口返回的成本，不写死月费用。用户同意再 `schedule --set weekly`。
- 不解释命令名，不列功能清单。用户问「还能做什么」时按他的产品状态给一条建议，不超过三句。

**老手（主动说 ASIN、站点、要什么报告）**
- 直接执行，输出用 `--compact`，多 ASIN 逐个跑完再汇总，不逐条请示。

**网页链接的用法**
- 每份报告末尾附 `web.report`，措辞是「网页版有健康度图表和频次表，可生成分享链接与海报」——是补充，不是「建议你去网页」。
- 用户要把报告发给同事/发群：指向网页报告页的「分享」按钮，不要把整篇 Markdown 贴给他转发。
- 用户要接群机器人提醒：给 `links.notify`（用户中心 → 通知渠道），这一步只能在网页做。
- 询价后用户没回应，不要追问。下次对话 `products` 里看到该 ASIN 仍是 `idle`，提一句
  「上次的 X 还没生成，我现在直接给你出」即可（免确认命中会直接生成）。

## 商品运营工作流（1.4.1）

- 用户要求 ASIN 运营体检、Listing 健康检查、商品页审查、评论转行动或运营周报时，
  使用 `operations` 命令；不得把旧 VOC、alerts 或普通 reports 冒充商品运营结果。
- 先运行 `operations capabilities`，只使用服务端返回的 workflow/focus；专属变体包
  还会在包根目录固定 workflow/focus 并禁止接收任意 prompt；本包是通用入口，不受此限制。
- 用 `operations profile` 检查商品字段，再运行 `operations quote`。评论不足时只建议
  用户使用现有 `collect`，不得隐式采集；商品关键字段不足时不得生成或扣点。
- 未得到用户明确扣点授权时，只返回 quote。授权后使用 quote 返回的完整 request 和同一
  `requestId` 执行 `operations run --confirm`，不得换 requestId 或修改 workflow/focus。
- 流中断或超时后绝不直接重跑。必须运行
  `operations status --request-id <原requestId>` 精确查询；completed 时使用其 reportId，
  quoted/running/frozen 时继续等待，released/failed 时说明错误并请求用户决定下一步。

## 商品变化监控工作流（1.5.2：按刷新次数扣点）

- `watch` 是独立的确定性商品监控：到期自动刷新商品页，记录价格、BSR、评分与标题/五点/图片变化，
  不调用 LLM。使用前先运行 `watch quote`（或 `operations capabilities`），确认 `watchEnabled`
  为 `true`；未开放时停止并告知用户，不得回退到其他工作流冒充监控。
- **计费**：每次到期刷新按频率扣一次点——按天约 30 次/月、按周约 5 次/月、按月 1 次/月。
  单价只以 `watch quote` 返回的 `perRefresh` / `monthlyEstimate` 为准（后台可调），**不要凭记忆报数**。
  套餐只体现在每月发放的积点上，不存在「套餐内含免费监控」；任何套餐都可以选按天。
  刷新失败不扣点；余额不足、或非美国站只剩赠送积点时自动暂停并邮件通知；后台调高单价后，
  已开的监控会暂停，等用户确认新价格才继续（`pausedReason`：credits / gift_us_only /
  price_changed / pricing_change）。
- **开启 = 授权周期扣点**：`watch create`、`watch resume`、改频率之前，必须先跑 `watch quote`，
  向用户复述所选频率的「每次 N 积点、约 M 积点/月」，得到明确同意后才带 `--accept-price N` 执行。
  “帮我盯着这个产品”算 create 意图，但仍要先报价确认；不带 `--accept-price` 时服务端返回
  `ARI_CONFIRM_PRICE` 和报价——把报价转述给用户，不要自动带价重试。
- `watch create` 只接受当前账户已订阅的主 ASIN。可选 `--competitor` 仅在该竞品已通过当前用户
  的主品/竞品关系绑定、且站点与主品相同后才允许创建竞品 watch；不得用临时 ASIN、全局商品资料
  或其他参数绕过归属校验。
- `watch list`、`watch quote`、`watch digest`、`watch events`、`watch series` 是只读操作（0 积点），
  可按用户问题直接读取；不得把读取结果当成用户同意开启或变更监控。
- `watch pause`（暂停期间不扣点）与 `watch delete` 是管理动作，只有用户明确要求时才执行。
  执行 `delete` 前必须向用户复述并核对准确的 `watch-id`；ID 不明确或目标不唯一时先停止询问。
  删除只移除该用户的监控关系，不删除共享商品资料、快照、评论或历史报告。
- 显著变化（价格 ≥5%、BSR ≥30%、评分 ≥0.1、标题/五点/图片被改，阈值后台可调）会发即时邮件
  并汇总进每周简报；评分数变化不单独提醒。讲变化时优先结合同期评论（差评是否集中出现）。
- 网页：产品详情页「价格 / BSR」tab 有趋势图、变化时间线和开关；ARI 工作台 <https://ari.funewa.com/zh/operations>
- 固定 CLI 入口如下：

  ```bash
  python scripts/ari.py watch quote
  python scripts/ari.py watch list
  python scripts/ari.py watch create --asin B0XXXXXXXX --site amz_us --schedule weekly --accept-price <perRefresh>
  python scripts/ari.py watch create --asin B0XXXXXXXX --competitor B0YYYYYYYY --site amz_us --schedule weekly --accept-price <perRefresh>
  python scripts/ari.py watch pause --watch-id <watchId>
  python scripts/ari.py watch resume --watch-id <watchId> --accept-price <perRefresh>
  python scripts/ari.py watch delete --watch-id <watchId>
  python scripts/ari.py watch digest --watch-id <watchId> --period 7d
  python scripts/ari.py watch events --watch-id <watchId>
  python scripts/ari.py watch series --watch-id <watchId> --days 90
  ```

- `--schedule` 取 `daily` / `weekly` / `monthly`，默认 `weekly`；不得把 weekly 说成每日监控。
- `digest` 汇总商品快照、确定性 Diff 和已有评论计数，其中 `creditsUsed` 是该 watch 窗口内
  已确认的刷新扣点合计（读取摘要本身不扣点）。它不提供小时级或实时价格、销量、库存、广告、
  订单或真实退货率数据。
- AI 周报仍使用 `operations` 的 `weekly` workflow，必须先报价，只有用户明确确认后才可
  `operations run --confirm`；不得把周报混入 `watch digest`。

站点默认 `amz_us`；可选 `amz_uk/amz_de/amz_jp/amz_ca/amz_fr/amz_es/amz_it`。
`charts` / `deepdive` 的 `--days` 默认 0（全部历史）；传非 0 时图表只覆盖该窗口，
解读占比和趋势必须带上这个窗口说明。

## 解读纪律

- 把 API 数字、由数字推导的判断、行动建议明确区分：`📊 数据直读`、`🔍 数据推理`、
  `💡 策略建议`。策略建议不得标为数据直读。
- `reviewCount < 50` 时在报告顶部标注小样本提示；单次提及只能作为方向性线索。
- 痛点优先级同时考虑提及频率、低星程度、近期趋势和已验证购买，不凭单条评论下结论。
- 用好评高频表达提炼 Listing 语言，但引用评论原话时保持短句并注明来自评论样本。
- 竞品对比只比较双方 API 均有数据的指标；一方样本不足时明确写“不可比”。
- 报告语言跟随用户；ASIN、VOC、Listing 等术语保留原文。非中文回复时记得传
  `--language en` 等，CLI 默认是 `zh`。

## 完整报告结构（简析按用户要求缩短）

按有数据的部分输出：数据概览 → 痛点与低星原因 → 好评与购买动因 → 用户画像与场景 →
趋势 → 竞品差异 → Listing 建议 → 产品改进优先级 → 数据来源与积点用量。

报告顶部加入：

> 数据基于 ARI 已采集的 Amazon 评论样本（截至当前查询时间），仅供经营决策参考；
> 小样本或采集窗口有限时应结合更多信源验证。

结尾简要列出 ASIN/站点、样本量、统计窗口（`_window.days`）、报告返回的
`reportId` 与 `creditsUsed`，以及当前余额。**输出含 `reportUrl` 时必须在结尾附上**，
固定文案：「在线查看图表版完整报告 / 导出：<reportUrl>」（需登录报告所属账户）。

CLI 命令仅在用户要求或排障需要时展示；用户要求简短时仍保留数据范围与实际用量。

## 本 Skill 的固定运营入口

- 本入口只执行 `weekly/asin`，输出模板固定为 `ops_weekly`。
- 先读 `skill-defaults.json` 与 `references/operation-workflow.md`，再调用 CLI。
- 必须先报价；只有用户明确确认才可运行并扣点。评论不足只建议独立采集。
- 不接收任意 prompt，不虚构广告、库存、订单、利润或实时店铺数据。
