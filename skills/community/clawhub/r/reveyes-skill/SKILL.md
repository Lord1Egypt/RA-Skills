---
name: amazon-review-reveyes
version: "1.1.5"
author: reveyes
description: >
  使用 Reveyes API 批量抓取亚马逊商品评论，支持 20 个站点。
  输出完整评论数据（含所有字段），并由 AI 从跨境电商运营者视角深度分析差评，
  提供产品质量、物流包装、Listing 准确性、客服反馈、改善优先级等结构化分析报告。
  Use when: 用户提到抓评论、查差评、分析竞品口碑、给出 ASIN 编号需要评论数据或运营分析。
  NOT for: 分析已经抓好的本地评论文件，或查询亚马逊商品价格/销量。
tags:
  - amazon
  - ecommerce
  - review
  - scraping
  - cross-border
  - analysis
requires:
  env:
    - REVEYES_API_KEY
---

## When to Run

- 用户发送 ASIN 编号并要求抓取或分析评论
- 用户说「帮我看看这个竞品的差评」「分析一下这款产品的用户反馈」
- 用户要了解差评原因、改进产品或 Listing
- 用户要对比同一商品在多个亚马逊站点的口碑
- 用户要导出评论数据做运营分析

## Parameters

从用户消息中提取以下信息：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `asin` | 亚马逊 ASIN，10 位字母数字（必须） | — |
| `marketplace` | 站点代码，见下方列表 | `US` |
| `pages` | 抓取页数（1-10），1 页约 10 条评论 | `3` |
| `filter_star` | 星级筛选：`all_stars` `positive` `critical` `five_star` `four_star` `three_star` `two_star` `one_star` | `all_stars` |
| `filter_sort_by` | 排序：`recent`（最新）/ `helpful`（最有用） | `recent` |
| `filter_reviewer_type` | 评论者类型：`all_reviews` / `avp_only_reviews`（验证购买） | `all_reviews` |
| `filter_media_type` | 媒体筛选：`all_contents` / `media_reviews_only`（含图片/视频） | `all_contents` |
| `filter_variant` | 变体筛选：`all_formats` / 具体变体值 | `all_formats` |

**支持的站点代码（20 个）：**
`US` `CA` `MX` `UK` `DE` `FR` `IT` `ES` `NL` `SE` `PL` `BE` `IE` `JP` `IN` `SG` `AE` `SA` `AU` `BR`

## Workflow

1. **提取参数**：从用户消息中识别 ASIN（10 位）、站点代码、页数、星级筛选
   - 若用户只给 ASIN，其余使用默认值
   - 若用户说「差评」/ 「negative」→ 自动设置 `filter_star=critical`
   - 若用户说「好评」/ 「positive」→ 自动设置 `filter_star=positive`
   - 若用户说「带图评论」→ 设置 `filter_media_type=media_reviews_only`
   - 若用户说「真实买家」/ 「verified」→ 设置 `filter_reviewer_type=avp_only_reviews`

2. **执行抓取**：调用 `scripts/fetch.py`，传入参数
   ```
   python scripts/fetch.py <ASIN> <marketplace> <pages> <filter_star>
   ```

3. **等待完成**：脚本内部自动轮询（最多 5 分钟），完成后输出完整 JSON 结果

4. **展示结构化数据**：将 JSON 中所有字段完整呈现（见下方字段说明）

5. **AI 深度分析**：按照下方「AI 分析提示词」对数据进行跨境电商运营分析

6. **错误处理**：
   - `AUTH_ERROR` → 提示用户检查 `REVEYES_API_KEY` 环境变量
   - `NO_CREDITS` → 提示前往 https://www.reveyes.cn 充值
   - `BAD_PARAMS` → 提示检查 ASIN 格式或站点代码是否正确
   - `TIMEOUT` → 告知任务仍在运行，附上 task_id 供后续查询

## API 返回字段说明

脚本输出标准 JSON，包含以下所有字段：

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `task_id` | string | 本次抓取任务 ID |
| `asin` | string | 商品 ASIN |
| `marketplace` | string | 站点代码 |
| `filter_star` | string | 本次星级筛选条件 |
| `credits_used` | int | 本次实际消耗积分 |

### summary（汇总统计）

| 字段 | 类型 | 说明 |
|------|------|------|
| `total_reviews` | int | 抓取到的评论总数 |
| `average_rating` | float | 平均评分（1-5） |
| `rating_distribution` | object | 各星级数量，key 为 "5"~"1" |
| `verified_purchase_count` | int | 验证购买评论数 |
| `has_image_count` | int | 含图片的评论数 |
| `has_video_count` | int | 含视频的评论数 |
| `negative_count` | int | 差评数（1-2 星） |
| `negative_rate` | float | 差评率（%） |

### items_summary（ASIN 子任务明细）

| 字段 | 类型 | 说明 |
|------|------|------|
| `asin` | string | ASIN |
| `marketplace` | string | 站点 |
| `status` | string | 子任务状态：pending / running / done / failed |
| `pages` | int | 请求页数 |
| `actual_pages` | int | 实际抓取页数 |
| `review_count` | int | 本 ASIN 实际抓到的评论数 |

### negative_reviews / all_reviews（评论列表，每条评论完整字段）

| 字段 | 类型 | 说明 |
|------|------|------|
| `review_id` | string | 亚马逊评论唯一 ID |
| `asin` | string | 所属 ASIN |
| `marketplace` | string | 所属站点 |
| `rating` | int | 星级（1-5） |
| `title` | string | 评论标题 |
| `review_date` | string | 评论日期（亚马逊原始格式） |
| `review_content` | string | 评论正文（完整） |
| `user_name` | string | 评论者昵称 |
| `profile_url` | string | 评论者主页 URL |
| `verified_purchase` | bool | 是否验证购买 |
| `helpful_votes` | int | 有用投票数 |
| `product_variant` | string | 购买的产品变体（颜色/尺寸等） |
| `images` | array | 评论附带图片列表 |
| `videos` | array | 评论附带视频列表 |
| `page` | int | 来自第几页 |

## AI 分析提示词

收到 JSON 数据后，按以下提示词进行分析输出：

---

你是一位资深亚马逊跨境电商卖家顾问，专注于帮助卖家通过评论数据改善产品、优化 Listing、提升 BSR 排名和转化率。

请基于以下评论数据，**以卖家运营者身份**给出可直接执行的行动建议报告。报告语言简洁、结论先行，每条建议必须说明"做什么"和"怎么做"。

**分析维度（必须逐一覆盖）：**

### 一、核心运营指标速览
- 评论总数、平均评分、差评率（1-2 星占比）
- 验证购买占比 — 判断评论真实性，低于 70% 需关注刷评风险
- 含图/视频评论数 — 高质量 UGC 可用于 A+ / 品牌故事素材
- 评分分布直方图（ASCII 格式）
- **一句话风险判断**：当前评分是否危及 Listing 流量（低于 4.0 需标注 ⚠️）

### 二、差评根因诊断与卖家对策

从 `negative_reviews` 逐条归因，每类必须给出**卖家具体对策**（不止描述问题）：

1. **产品本身缺陷**（材质/耐用性/做工）
   - 出现次数 + 代表性引用（原文）
   - 卖家对策：→ 向供应商提出具体改良要求 / 更换原材料型号 / 升级 QC 抽检比例

2. **功能与预期不符**（性能/兼容性/操作）
   - 出现次数 + 代表性引用（原文）
   - 卖家对策：→ 在 Bullet Points 中明确标注适用范围和限制条件 / 在包装内增加快速上手卡片

3. **Listing 描述与实物不符**（颜色/尺寸/材质偏差）
   - 出现次数 + 代表性引用（原文）
   - 卖家对策：→ 修正主图/副图/尺寸对比图 / 在标题或 Bullet 中加精准规格描述 / 更新 A+ 对比展示模块

4. **包装与物流问题**（破损/包装简陋/发货延迟）
   - 出现次数 + 代表性引用（原文）
   - 卖家对策：→ 升级内衬缓冲材料 / 添加易碎品标签 / 核查 FBA 入库包装规范是否达标

5. **售后与客服问题**（退换货/响应速度）
   - 出现次数 + 代表性引用（原文）
   - 卖家对策：→ 优化 Buyer-Seller Message 自动回复模板 / 包装内附售后服务卡（含联系方式和常见问题解答）

6. **其他问题**
   - 出现次数 + 代表性引用 + 卖家建议对策

### 三、高权重差评处理优先级（helpful_votes Top 5）

这些差评对潜在买家转化影响最大，须优先处理：

逐条列出：
- 星级 / helpful_votes 数 / 是否验证购买 / 所购变体
- 评论标题 + 正文关键句（100 字内，保留原文）
- **卖家应对**：① 是否可通过 Comment 公开回复澄清？② 是否需改动产品/Listing？③ 是否需主动联系买家补救？

### 四、Listing 优化行动清单

基于差评和好评数据，给出各模块**直接可用的改写建议**：

- **标题**：需补充哪些关键属性（给出修改示例）
- **五点 Bullet Points**：哪几点需增加/修正，直接给出改写文案
- **主图/副图**：缺少哪些展示角度（尺寸对比图 / 使用场景图 / 细节放大图）
- **A+ 内容**：差评中哪些常见误解可通过 A+ 图文模块主动消除
- **Search Terms / PPC 关键词**：从评论中提取买家自然语言，列出可补充进 Search Terms 的词，以及应加入 PPC 否定词的词

### 五、SKU / 变体策略建议

如有多个 `product_variant`：
- 各变体的好评率与投诉率对比
- 明确指出：哪些变体**加大推广**、哪些**列为改良重点**、哪些**考虑下架**
- 是否存在新变体机会（买家在评论中提到希望有但目前没有的款式/颜色/尺寸）

### 六、竞品差异化打法（适用于分析竞品 ASIN）

如本次抓取的是竞品 ASIN：
- **竞品核心弱点**：买家投诉最多的 2-3 个问题 → 我方产品需针对性优化并在 Listing 中主动对比
- **买家最在意的属性**：从评论中提炼竞品买家真正关心的核心诉求
- **我方 Listing 差异化打法**：在标题/Bullet/A+ 中如何具体体现"我们解决了竞品的 XX 问题"（给出文案示例）
- **PPC 拦截机会**：哪些竞品相关词值得投放广告

---

**输出规范：**
- 每条建议必须**可直接执行**，避免空话（错误示例："提升质量" → 正确示例："要求供应商将外壳材质从 ABS 升级为 PC+ABS 合金，并在 QC 环节增加跌落测试"）
- 涉及 Listing 文案改动时，**直接给出改写示例**，而非仅指出问题
- 引用评论保留原文语言，可附中文说明
- 以 Markdown 格式输出，可直接复制到运营 SOP 文档

## Output Format

收到脚本 JSON 输出后，AI 依次输出：

```
📦 ASIN: {asin}  |  站点: {marketplace}  |  筛选: {filter_star}
本次消耗积分: {credits_used}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 数据概览
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
评论总数: {total_reviews}  |  平均评分: {average_rating}★  |  差评率: {negative_rate}%
验证购买: {verified_purchase_count} 条  |  含图: {has_image_count} 条  |  含视频: {has_video_count} 条

评分分布：
  ★★★★★  {5星数} 条 ({占比}%)  ██████
  ★★★★☆  {4星数} 条 ({占比}%)  ████
  ★★★☆☆  {3星数} 条 ({占比}%)  ██
  ★★☆☆☆  {2星数} 条 ({占比}%)  █
  ★☆☆☆☆  {1星数} 条 ({占比}%)  ███

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
� 差评问题分类
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 产品质量问题（N 条）
   - "Title of review" → 关键问题描述
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  高影响差评 Top 5（按有用票数）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ★☆ [{helpful_votes} 人觉得有用] [已验证购买]
   "{title}"
   {review_content 前100字}...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 好评亮点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠 运营改善建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[高] ...
[中] ...
[低] ...
```
