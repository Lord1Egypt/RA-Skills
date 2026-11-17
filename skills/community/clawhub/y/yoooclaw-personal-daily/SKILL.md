---
name: yoooclaw-personal-daily
description: 个性化新闻日报：根据用户配置或定时任务中的关注话题，在 Hermes 中自主选择当前可用的联网工具并在全部不可用时回退内置 RSS，或在 OpenClaw 及其兼容宿主 JVSClaw、ArkClaw、EClaw 中依次选择 byted-web-search、web_search、内置 RSS，获取当日新闻并生成带来源与趋势信号的中文日报。用户要求运行日报、按关注话题生成今日资讯，或定时任务要求生成个性化日报时使用。
---

# 个性化新闻日报

基于当前 Agent 平台对应的关注配置和当日联网结果，生成一份可核验的中文日报。

## 1. 确定宿主

根据当前 Agent 自身的宿主身份设置一次 `runtime`：

- 当前 Agent 是 Hermes：`runtime=hermes`。
- 当前 Agent 是 OpenClaw，或宿主标识为 `jvsclaw`、`arkclaw`、`eclaw`（不区分大小写）：统一设置 `runtime=openclaw`。
- 无法识别为以上任一平台：回复“无法识别当前 Agent，个性化日报未运行”，然后停止。

只以当前 Agent 的自身宿主身份或宿主标识为依据；不执行 `hostname`，本机是否同时存在 Hermes、OpenClaw、其安装目录或命令不改变判断。JVSClaw、ArkClaw、EClaw 不是独立分支，统一使用 OpenClaw 的配置路径、联网能力选择和任务流程。设置后在本次任务中复用 `runtime`，不再次判断。

**完成条件：** `runtime` 已且仅已取 `hermes` 或 `openclaw` 中的一个值。

## 2. 选择生成分支

根据 `runtime` 只执行一个平台生成分支：

- `runtime=hermes`：读取 [`references/generate/hermes.md`](references/generate/hermes.md)。
- `runtime=openclaw`：读取 [`references/generate/openclaw.md`](references/generate/openclaw.md)。
- 所选平台生成 reference 设置 `acquisition=search` 时，读取 [`references/acquisition/search.md`](references/acquisition/search.md)；设置 `acquisition=rss` 时，读取 [`references/acquisition/rss.md`](references/acquisition/rss.md)、[`references/rss/domestic.md`](references/rss/domestic.md) 和 [`references/rss/international.md`](references/rss/international.md)。
- 所选平台生成 reference 和唯一的 acquisition reference 完成后，继续下面的“日报生成”流程。

**完成条件：** 只加载与 `runtime` 匹配的一个平台生成 reference；只加载与 `acquisition` 匹配的一个 acquisition reference，仅 RSS 额外加载国内、海外源清单。

## 日报生成

### 1. 读取并规范化关注话题

按以下优先级取得话题：

1. 定时任务 message 中明确携带的 `interests`、`topics` 或“关注话题”列表。
2. 所选平台生成 reference 指定的 `interests.md`。

`interests.md` 使用 UTF-8；每个非空普通行或 Markdown 列表项表示一个话题。去掉列表符号和首尾空白，忽略标题、注释与空行，按首次出现顺序对完全相同的话题去重。message 解析出至少一个有效话题时，以 message 列表为本次唯一输入。

将明显同义或上下位关系紧密的话题合并成搜索组，按输入顺序保留最多 6 组。超过 6 组时，本次覆盖前 6 组，并在日报的“今日关注”中只列实际检索的话题。

没有取得有效话题时，回复“关注话题尚未配置，请先在场景设置中配置”，然后停止。

**完成条件：** 得到 1–6 个有序搜索组，且每组都能追溯到至少一个原始关注话题。

### 2. 获取候选新闻

执行任务路由已加载的唯一 acquisition reference，取得候选新闻和实际来源范围；不要执行另一种获取方式。

**完成条件：** 所选 acquisition reference 的完成条件满足，或已按其失败规则停止；成功时每个候选都记录所属搜索组、来源、链接和发布时间，候选数量允许为 0。

### 3. 通过当日证据门

逐条检查候选结果，按以下标准形成事件：

1. **相关性：** 新闻事实直接涉及至少一个原始关注话题。
2. **发布时间：** 搜索结果的正式发布时间或原文发布时间落在宿主时区的当日时间窗内。将“刚刚”“N 小时前”等相对时间换算为绝对时间；标题、摘要、正文或 URL 中出现当日日期只作为辅助信号。
3. **来源：** 至少保留一个可打开的官方来源、当事方原始发布、有编辑责任的媒体页面或已成功解析的内置 RSS 条目链接。营销软文、SEO 聚合页和无法核验发布时间的页面不进入日报。
4. **交叉验证：** 重大数字、争议性事件和会影响判断的结论使用两个相互独立的来源核验；只有单一来源时明确归因，不把它上升为整体趋势。

按同一事件而不是同一标题聚类，合并重复 URL 和转述报道。每个事件保留信息最完整的 1–2 个来源，并记录所属话题、发布时间、核心事实及重要性。

**完成条件：** 每个候选都已归入一个已验证事件或有明确排除原因；每个保留事件都有已核验的当日发布时间和可打开来源。

### 4. 排序并输出

按“与用户关注的相关度 → 事件重要性 → 来源强度 → 发布时间”排序。最多输出 6 条新闻，每个话题最多 2 条；有 1–6 条时如实输出，0 条时使用空日报。

完成检索、验真和排序后，读取 [`references/output/template.md`](references/output/template.md)，选择对应模板生成会话文本。输出中文摘要，保留关键数据、人名、公司名和产品名原文；每项事实在相邻位置附来源链接。全文不超过 1500 个中文字符，不生成文件。

**最终完成条件：** 输出中的每条新闻都来自已验证事件，条目数和字数均在上限内；只有所选获取方式成功完成且 0 条事件通过证据门时，才输出空日报模板。
