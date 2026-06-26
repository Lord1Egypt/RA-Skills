# Stream Digest Layout V1

## Goal
把当前 `zsxq-digest` 从“短摘要日报”升级为“分星球信息流摘要”：
- 优先把每个星球最近最值得看的内容兜出来
- 减少用户自己筛选的时间
- 仍然保留足够上下文，帮助用户判断是否点开原文
- 对长内容做截断，但尽量保留主体信息
- 所有条目都附原始 URL

这版不强依赖“严格今天”过滤。
核心目标从“按日期筛”转为“按最近可见价值排序”。

## Product framing
建议把输出名称从“日报”弱化成：
- `知识星球信息流摘要`
- 或 `知识星球最近更新精华`

因为它更像“近期高价值流”而不是严格日历日报。

## User value
用户打开摘要后，应在 2-4 分钟内完成三件事：
1. 先看到每个星球最值得点开的 3 条
2. 直接读到这些条目的大段正文 / 主要信息块
3. 再用压缩列表快速扫过剩余内容，决定是否展开原文

## Proposed output structure

### 1. 总览头部
包含：
- 本次覆盖的星球
- 每个星球抓取条数
- 是否来自 token / browser
- 说明是否为“最近可见流”而非严格今天

示例：
- 覆盖星球：学不完根本学不完、睡前消息的编辑们
- 数据模式：token / browser fallback
- 时间口径：最近可见更新（非严格今日）

### 2. 每个星球一个独立 section
按星球分块，而不是全局混排。

每个星球 section 内再分两层：

#### A. 精华 3 条（full-ish blocks）
每个星球固定放 3 条，按综合价值排序。

每条输出字段建议：
- 标题 / hook
- 作者（如有）
- 时间（如有）
- 为什么值得看（一行）
- 主体内容块（优先 300-800 字，超长截断）
- 原文链接

长文截断策略：
- 默认展示前 500-800 字
- 如果文本结构明显分段，优先保留前 2-4 段
- 截断后明确提示：`（下略，见原文）`

这部分的目标是：
> 用户不点进去，也已经拿到主要信息。

#### B. 其余更新（compact list）
剩余条目不展开全文，只保留：
- 标题
- 1-2 句摘要
- 推荐动作（立即看 / 稍后看 / 可跳过）
- URL

这样可以压缩长度，避免每个星球都变得过重。

### 3. 最后给一个跨星球速览
可选的尾部 section：
- 今日/本次最值得点开的 5 条
- 或“如果只有 5 分钟，优先看这些”

这样适合忙的时候快速消费。

## Ranking model
排序不只看“是否最新”，而是看“是否有信息密度”。

建议综合四类信号：

### A. 内容价值信号（最重要）
优先级提高：
- 原创分析 / 判断 / 框架
- 方法论 / 逻辑 / 规则变化
- 资源推荐 / 书单 / 教程 / 模板 / 工具
- 明确结论、明确建议、明确行动项
- 对热点事件的高质量解读

### B. 可替代性信号
优先级降低：
- 单纯转载新闻
- 没有新信息的短提醒
- 情绪化发言 / 闲聊
- 只有标题，没有正文信息密度

### C. 时效性信号
提高：
- 直播、开播、报名、截止
- 明显与当前市场/政策/热点强相关

### D. 完整度信号
提高：
- 能抓到较完整正文
- 能抓到作者、时间、清晰标题

如果是 browser 模式抓到的“外链池”，通常应该降低权重，除非附带了星主自己的评论或总结。

## Per-circle rendering rules

### 学不完根本学不完（偏长文/分析）
策略：
- 更适合给“长块正文 + 少量条目”
- 精华 3 条可以放更长（600-900 字）
- 重点提炼：框架、逻辑、建议、案例

### 睡前消息的编辑们（偏线索/外链池）
策略：
- 精华 3 条不一定是最长，而是“最有判断价值”的 3 条
- 如果主要是外链，应优先展示：
  - 星球内评论/导语
  - 外链标题
  - 该条属于什么主题簇（如中东局势、AI医疗、劳工议题）
- 其余条目更适合聚类摘要，而不是逐条长展开

## Recommended data model extension
在 normalized item 上增加几个字段：

```json
{
  "summary_mode": "full|compact",
  "topic_cluster": "政策/市场/教育/地缘/AI/资源",
  "detail_excerpt": "for full block body",
  "detail_truncated": true,
  "detail_chars": 680,
  "source_mode": "token|browser",
  "source_confidence": "high|medium|low"
}
```

用途：
- `summary_mode`：决定渲染成长块还是短列表
- `topic_cluster`：让“睡前消息”这类外链流可以聚类
- `detail_excerpt`：给精华区输出主体内容
- `source_confidence`：提醒用户这条是正文级抓取还是仅浏览器可见预览

## Selection algorithm (V1)

### Step 1. 分星球
按 `circle_name` 分组。

### Step 2. 每个星球内评分
建议评分维度：
- base priority: high / medium / low
- signal bonus: original-analysis, tool-release, deadline
- body length bonus: 有较完整正文加分
- source penalty: 纯外链、纯列表、仅标题减分

可以先做一个简单整数评分：
- high = +30
- medium = +15
- low = +0
- original-analysis = +20
- tool-release = +15
- deadline = +10
- 正文长度 > 280 = +10
- 仅外链无评论 = -10
- 标题过短/信息贫乏 = -8

### Step 3. 选 top 3 为 full blocks
- 每个星球选前三
- 如果高质量条目不足 3 条，就允许 medium 补位
- 如果全是弱条目，也仍然给 3 条，但在说明中标注“本星球本轮以线索流为主”

### Step 4. 剩余条目做 compact summary
- 每条 1-2 句
- URL 保留
- 可按 topic cluster 再压缩成 2-4 个主题簇

## Token mode vs Browser mode

### Token mode（理想）
优先用 token 模式，因为更容易拿到结构化数据与稳定字段。
目标：
- 拿更完整的正文
- 拿稳定时间
- 拿 author / comment / like 等补充信号

### Browser mode（现实 fallback）
browser 模式作为可用 fallback：
- 可优先抓“当前可见卡片正文”
- 对长文链接，必要时二跳打开 article 页面，抓取正文前几段
- 如果二跳成本太高，先保留卡片预览 + URL

建议分两级 browser 实现：
1. **Level 1**：只读列表页可见卡片
2. **Level 2**：对 top 3 条再进入详情页补抓正文

这样成本可控，而且最符合用户价值。

## MVP recommendation
先做一个两阶段 MVP：

### MVP-A（低风险，马上可做）
- 保持现有采集链路
- 新增新的 renderer：`render_stream_digest.py`（或扩展 `digest_updates.py`）
- 实现“每星球 top3 长块 + 其余短列表”
- browser 模式先用已有 preview 文本，不强求详情页补抓

优势：
- 交付快
- 风险低
- 先验证用户是否喜欢这种编排

### MVP-B（体验增强）
- 对每星球 top3，尝试补抓 article 详情页正文
- 对“睡前消息的编辑们”增加 topic cluster 聚类
- 对外链池做“议题摘要”而不是逐条平铺

## Risks
1. browser 页面字段不稳定，时间/作者可能缺失
2. 外链型星球会出现“链接很多，但正文很薄”
3. 如果所有星球都放 3 条 full blocks，整体输出可能很长
4. 详情页补抓会增加浏览器自动化复杂度和耗时

## Guardrails
- 不要假装“严格今天”
- 不要假装抓到了完整正文；应标注截断 / 预览 / fallback
- 不要把纯新闻转载和原创分析放同样权重
- 所有条目都保留 URL

## Concrete implementation proposal

### Option 1: extend existing renderer
直接扩展 `scripts/digest_updates.py`：
- 新增 `--layout stream`
- 新增 `--full-per-circle 3`
- 新增 `--full-max-chars 800`

优点：
- 文件少
- 迁移快

缺点：
- 现有日报 renderer 会变复杂

### Option 2: add a dedicated renderer (recommended)
新增：
- `scripts/render_stream_digest.py`

输入：normalized item JSON
输出：新的分星球信息流 markdown

优点：
- 与现有日报渲染器解耦
- 更方便快速迭代编排
- 不会把当前简单日报逻辑搞乱

建议采用 **Option 2**。

## First implementation checklist
1. 新增评分函数：为每个 item 生成 `stream_score`
2. 新增 `summary_mode` 判定：top3=full，其余=compact
3. 新增 renderer：分星球输出 full + compact
4. full block 支持长文本截断与“下略，见原文”
5. compact block 保留摘要 + URL
6. 在 README / SKILL.md 中把它描述为：
   - `日报` 仍保留
   - 新增 `信息流摘要` 作为更适合日常阅读的模式

## Recommendation
建议先落地：
- **分星球 top3 长块 + 其余短列表**
- **新增独立 renderer**
- **先不强求严格 today**
- **先不强依赖详情页补抓**

这样最快得到一个真正省筛选时间、且内容足够扎实的版本。
