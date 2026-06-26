# Performance Max 与 Demand Gen 运营深度指南

> **所属 skill:** siluzan-tso
> **适用场景:** PMax 效果诊断、asset group 优化建议、PMax 与 Search 蚕食分析、Demand Gen 策略
> **最后更新:** 2026-04-01

**CLI PMax（Lead Gen / 非 Shopping）**：新建见 `assets/pmax-create-template.md`；上线后 `ad pmax-get` / `pmax-edit` / `pmax-assets-update` / `pmax-signals-*` / 报表见 `references/google-ads/pmax-api.md`。本指南侧重运营诊断。

---

---

## 1. PMax 运营原理

### 1.1 多渠道竞价机制

PMax 在单一广告系列中同时参与 Search、Shopping、Display、YouTube、Discover/Gmail、Maps 渠道的竞价。Google 实时竞价系统自动分配预算到预估转化价值最高的渠道。广告主**无法手动选择或排除渠道**。

### 1.2 核心架构概念

| 概念                            | 说明                                                                                    |
| ------------------------------- | --------------------------------------------------------------------------------------- |
| **Asset Group（素材组）**       | PMax 的广告单元，等同于广告组。每组包含文字、图片、视频等素材，Google 自动组合投放      |
| **Audience Signal（受众信号）** | 给 Google 算法的"建议"，**不是硬定向**。PMax 会以此为起点，但可自主扩展到信号之外的受众 |
| **Listing Group（产品分组）**   | 电商 PMax 中用于筛选 Feed 中哪些产品进入该素材组                                        |
| **Search Theme（搜索主题）**    | 2025 新增，提供关键词级别的搜索意图信号（每个素材组最多 25 个）                         |

### 1.3 PMax 与标准系列的优先级规则

- **PMax vs 标准购物：** PMax 优先级高于标准购物广告系列（同一产品时 PMax 优先竞价）
- **PMax vs Search：** 完全匹配（Exact Match）或词组匹配（Phrase Match）的 Search 关键词，若与搜索查询完全一致，则 Search 优先于 PMax。广泛匹配与 PMax 共同竞价，Ad Rank 高者获展示
- **实操含义：** 高价值关键词必须在 Search 中以 Exact Match 保护，否则 PMax 将接管该流量

### 1.4 2025 年关键更新

| 更新           | 影响                                                                 |
| -------------- | -------------------------------------------------------------------- |
| **渠道级报告** | 可查看 Search/Shopping/Display/Video/Discover 各渠道的花费与转化数据 |
| **否定关键词** | 每个 PMax 系列最多支持 10,000 个否定关键词（之前需联系 Google 代表） |
| **品牌排除**   | 通过品牌列表功能排除品牌词流量，减少与 Search 蚕食                   |
| **搜索主题**   | 每个素材组最多 25 个 search themes，引导搜索渠道投放方向             |
| **搜索词报告** | PMax 搜索词现在可查看（之前为黑盒），支持 CLI 拉取                   |

## 2. PMax 与 Search 蚕食诊断

> **这是 PMax 运营中最常见、影响最大的问题。**

### 2.1 典型症状

- PMax 上线后，原有 Search 系列的展示次数 / 点击 / 转化明显下降
- PMax 报告中品牌词占比过高（品牌花费 > PMax 总花费的 20%）
- 整体 CPA 未降低，但流量从 Search 转移到了 PMax

### 2.2 CLI 诊断流程

**第一步：对比 PMax 上线前后 Search 系列表现**

```bash
# 查看 PMax 上线前的 Search 表现（假设 PMax 于 3 月 1 日上线）
siluzan-tso google-analysis -a <CID> --sections campaigns --from 2026-01-01 --to 2026-02-28
# 查看 PMax 上线后的 Search 表现
siluzan-tso google-analysis -a <CID> --sections campaigns --from 2026-03-01 --to 2026-03-31
```

**关注指标：** Search 系列的 impressions、conversions、conversion value 是否显著下降。

**第二步：搜索词重叠分析** `[CLI 可执行]`

```bash
# 拉取 PMax 搜索词
siluzan-tso google-analysis -a <CID> --sections search-terms
# 拉取 Search 系列关键词
siluzan-tso google-analysis -a <CID> --sections keywords
```

对比两者，找出重叠搜索词，尤其关注品牌词和高转化非品牌词。

**第三步：确认品牌词占比**
从搜索词报告中筛选包含品牌名的查询，计算其在 PMax 总花费中的占比。

### 2.3 解决方案矩阵

| 场景                        | 操作                                                                          |
| --------------------------- | ----------------------------------------------------------------------------- |
| PMax 品牌花费 > 20%         | `[UI 操作]` 在 PMax 设置品牌排除 + `[CLI/UI]` Search 中添加品牌词 Exact Match |
| 高价值非品牌词被 PMax 抢占  | `[CLI/UI]` Search 中以 Exact Match 添加这些关键词（Search Exact 优先于 PMax） |
| Search 广泛匹配与 PMax 竞争 | 将 Search 关键词收紧为 Exact/Phrase Match                                     |
| 整体蚕食严重                | `[UI 操作]` PMax 添加否定关键词排除已在 Search 中覆盖的高价值词               |

### 2.4 决策阈值

- **品牌花费占比 > 20%：** 必须设置品牌排除
- **Search 转化下降 > 30%（PMax 上线后）：** 需要紧急干预
- **PMax 搜索词与 Search 关键词重叠率 > 50%：** 需重新划分各系列职责

## 3. Asset Group 策略

### 3.1 分组原则

Asset Group 是 PMax 中素材与受众信号的组合单元。**推荐分组维度（按优先级）：** 产品类别/服务线 → 利润层级 → 受众画像 → 主题/季节。

### 3.2 何时拆分 vs 不拆分

**拆分：** 产品线差异大（素材/着陆页不同）、目标 ROAS/CPA 差异显著、受众信号明显不同。
**不拆分：** 预算不足（每个素材组建议最低 $50/天）、产品/受众高度相似、月转化 < 30。

### 3.3 电商场景

```
素材组 A: 高毛利产品（Custom Label = "high-margin"）→ tROAS 较激进
素材组 B: 中毛利产品（Custom Label = "mid-margin"）→ tROAS 中等
素材组 C: 清仓/低毛利（Custom Label = "clearance"）→ tROAS 保守或暂停
```

通过产品 Feed 的 custom labels 控制 listing group 分组。 `[UI 操作]`

### 3.4 Lead Gen 场景

```
素材组 A: 服务类型 1 → 着陆页 A + 该服务的受众信号
素材组 B: 服务类型 2 → 着陆页 B + 不同受众信号
素材组 C: 通用品牌认知 → 首页 + 广泛受众信号
```

**新建活动（CLI）**：方案 JSON 默认含 `campaignExtensions.leadForm`（潜在客户表单），与 callouts/snippets 一并由 `pmax-create` 挂载；字段见 `assets/pmax-create-template.md` § 方案生成。存量活动补挂见 `assets/pmax-lead-form-template.md`。

### 3.5 每个素材组的完整性要求

每个素材组必须包含**完整素材套件**：长标题 × 5、短标题 × 5、描述 × 5；横版图 (1.91:1) × 4+、方形图 (1:1) × 4+、竖版图 (4:5) × 2+；视频 × 1+（建议 3 个）；商家名称、Logo、最终网址、行动号召。

## 4. 素材（Asset）诊断与优化

### 4.1 素材表现标签

Google 为每个素材分配以下标签：

| 标签         | 含义           | 操作                                   |
| ------------ | -------------- | -------------------------------------- |
| **Best**     | 表现最佳       | **不要替换**，可作为新素材的参考模板   |
| **Good**     | 表现良好       | 保留，持续观察                         |
| **Low**      | 表现不佳       | 安排替换（每次替换不超过总素材的 20%） |
| **Learning** | 数据积累中     | 至少等待 2 周再判断                    |
| **Pending**  | 审核中或无数据 | 检查是否有审核问题                     |

### 4.2 优化节奏

- **检查频率：** 每 2-4 周检查一次素材表现
- **替换规则：** 仅替换 Low 标签素材；每次替换比例 ≤ 20%，避免大幅波动触发重新学习
- **新素材上线：** 添加后至少观察 2 周再评判
- **季节性素材：** 提前 2 周上传，给足学习时间

### 4.3 文字素材

遵循 RSA 的六主题法则（详见 google-ads-creative-optimization.md）：核心价值主张、产品特性、社会证明、优惠促销、行动号召变体、品牌信任信号。每个主题至少 1 个标题变体。

### 4.4 图片素材规格

| 比例            | 尺寸           | 用途                            | 最低数量 |
| --------------- | -------------- | ------------------------------- | -------- |
| **1.91:1 横版** | 1200 × 628 px  | Display、Discover、Gmail        | 4        |
| **1:1 方形**    | 1200 × 1200 px | Discover、YouTube 信息流        | 4        |
| **4:5 竖版**    | 960 × 1200 px  | YouTube Shorts、移动端 Discover | 2        |

**要点：** 图片中文字面积 ≤ 20%，主体居中（自动裁剪安全区域），避免拼贴式设计。

### 4.5 视频素材

> **关键规则：必须上传至少 1 个视频。** 如果不上传，Google 将自动从图片生成低质量视频，表现通常很差。

推荐配置：横版 16:9（In-stream/Display）、竖版 9:16（Shorts/移动端）、方形 1:1（Discover/信息流）。时长 15-30 秒为主，可补充 6 秒 bumper。

### 4.6 自动创建素材（Auto-created Assets）

- **新账户 / 新系列：** 建议关闭。先用人工素材建立表现基线
- **成熟账户：** 可开启测试，但需监控自动生成的素材质量
- 设置路径：`[UI 操作]` 系列设置 → 自动创建的素材 → 开启/关闭

## 5. 渠道级分析（2025 新功能）

### 5.1 可见数据

2025 年起，PMax 报告可查看 Search、Shopping、Display、Video（YouTube）、Discover/Gmail 各渠道的花费、展示次数、点击、转化次数、转化价值。

### 5.2 诊断框架

| 渠道分布                                     | 信号                             | 建议操作                                                            |
| -------------------------------------------- | -------------------------------- | ------------------------------------------------------------------- |
| Display + YouTube 占预算 > 40%，转化率低     | PMax 在低漏斗效率渠道上花费过多  | `[UI]` 收紧受众信号、减少展示类素材数量、检查转化跟踪是否包含微转化 |
| Search + Shopping 占预算 > 80%               | PMax 几乎只跑搜索/购物           | 评估是否需要 PMax——标准 Search + Shopping 可能更可控                |
| 各渠道均衡且 ROAS 达标                       | 健康的 PMax 表现                 | 维持现状，逐步测试预算增加                                          |
| Discover 花费高但转化为 0                    | 信息流素材或着陆页不适配         | `[UI]` 优化信息流格式的图片素材，检查着陆页移动端体验               |
| Video 花费正常但 view-through 转化占比 > 60% | 视频带来的是辅助转化而非直接转化 | 不一定需要干预，但不应将此等同于直接转化效果                        |

### 5.3 渠道 × 表现行动矩阵

```
渠道表现好 + 花费占比高 → 维持，考虑增加该渠道对应素材
渠道表现好 + 花费占比低 → 增加对应素材数量和质量，吸引更多该渠道展示
渠道表现差 + 花费占比高 → 收紧受众信号，减少该渠道格式素材
渠道表现差 + 花费占比低 → 暂不干预，聚焦主力渠道
```

## 6. 搜索词与否定关键词管理

### 6.1 PMax 搜索词报告

2025 年更新后，PMax 搜索词报告已可查看。 `[CLI 可执行]`

```bash
siluzan-tso google-analysis -a <CID> --sections search-terms
```

**检查频率：** 每周一次（高花费账户可 2 次/周）。

### 6.2 否定关键词策略

PMax 现支持每个系列最多 **10,000 个否定关键词**。 `[UI 操作]`

**操作流程：**

1. `[CLI]` 拉取搜索词报告 → 导出
2. 筛选不相关搜索词（无转化 + 高花费 / 明显不相关）
3. `[UI]` 在 PMax 系列设置中添加为否定关键词
4. 筛选高转化搜索词 → `[CLI/UI]` 添加为 Search 系列的 Exact Match 关键词

### 6.3 品牌排除

> 品牌排除功能优于手动添加品牌否定关键词，因为它覆盖品牌词的所有变体。

- `[UI 操作]` 系列设置 → 品牌排除 → 选择品牌列表
- 品牌列表在账户级别管理，可跨系列共享
- 适用场景：品牌词已在 Search 系列中覆盖，PMax 无需重复竞价品牌流量

### 6.4 搜索词 → 关键词闭环

```
PMax 搜索词报告
    ├── 不相关词 → 添加为 PMax 否定关键词 [UI]
    ├── 品牌词 → 设置品牌排除 [UI] + Search Exact Match [CLI/UI]
    ├── 高转化非品牌词 → 添加为 Search Exact Match [CLI/UI]
    └── 长尾探索词（有转化潜力）→ 保留在 PMax 中继续观察
```

## 7. 受众信号优化

### 7.1 核心概念

**受众信号是建议，不是硬定向。** PMax 会以受众信号为起点进行学习，但算法有权扩展到信号之外的用户。信号越精准，冷启动越快、初期浪费越少。

### 7.2 信号类型及优先级

| 类型                              | 说明                                            | 推荐优先级                            |
| --------------------------------- | ----------------------------------------------- | ------------------------------------- |
| **Your Data（自有数据）**         | 再营销列表、Customer Match（客户邮箱/电话列表） | ★★★ 最高 — 已有转化意图的真实用户数据 |
| **Custom Segments（自定义细分）** | 基于搜索关键词、浏览过的网址、使用过的 App      | ★★★ 高 — 接近搜索意图的信号           |
| **In-Market（有购买意向）**       | Google 判定近期有购买意向的用户                 | ★★ 中 — 有效但较宽泛                  |
| **Affinity（兴趣相似）**          | 长期兴趣标签                                    | ★ 低 — 信号太宽，仅作为补充           |
| **Demographics（人口统计）**      | 年龄、性别、家庭收入                            | ★ 低 — 仅在明确需要排除时使用         |

### 7.3 最佳实践

- **启动期：** 强信号组合 — 再营销 + Customer Match + 高意图自定义细分
- **稳定期：** 逐步添加 In-Market 等较宽信号
- **弱信号风险：** 仅提供 Affinity → PMax 快速广泛探索 → 学习期大量预算浪费

### 7.4 信号组合逻辑

同一素材组内多个信号 = **OR 逻辑**（满足任一即可触达）。不同素材组之间 = 独立运作。

### 7.5 受众信号诊断 `[CLI 可执行]`

```bash
siluzan-tso google-analysis -a <CID> --sections audience
```

关注：各受众段 CPA 差异；信号受众 vs 自动扩展受众比例；扩展受众 CPA 远高于信号受众 → 信号不够强。

## 8. PMax 出价与预算

### 8.1 出价策略阶段

| 阶段       | 策略                                             | 时间            | 条件                              |
| ---------- | ------------------------------------------------ | --------------- | --------------------------------- |
| **冷启动** | Max Conversions（不设目标）                      | 2-4 周          | 新系列或数据不足时                |
| **过渡**   | Max Conversions + tCPA 或 Max Conv Value + tROAS | 设定后观察 2 周 | 积累 30+ 转化后                   |
| **稳态**   | tCPA 或 tROAS                                    | 持续优化        | 月转化 30+（tCPA）或 50+（tROAS） |

### 8.2 转化量阈值

- **tCPA 最低要求：** 近 30 天 30+ 转化
- **tROAS 最低要求：** 近 30 天 50+ 转化
- **数据不足时：** 使用 Max Conversions 不设目标，或合并多个低量系列

### 8.3 预算规则

- **推荐最低日预算：** $50-100（取决于行业 CPA），绝对最低 $30
- **每个素材组隐含预算：** 3 个素材组 → 系列预算至少 $150/天
- **规则：** 日预算 ≥ 目标 CPA × 3

### 8.4 预算扩展

每次增加 15-20%，间隔 1 周。不要一次性翻倍（触发重新学习）。缩减同理，每次 ≤ 20%。

### 8.5 PMax + Search 预算交互

PMax 和 Search 应各自独立预算，**不要从 Search 挪预算给 PMax**。共享预算（Shared Budget）不建议用于 PMax + Search 组合。PMax 上线后 Search 表现下降通常是流量蚕食而非预算问题（参见第 2 章）。

## 9. Demand Gen 系列战术

### 9.1 什么是 Demand Gen

Demand Gen 是 Discovery 广告系列的升级版，覆盖 YouTube（In-stream + Shorts + In-feed）、Discover、Gmail 版位。

### 9.2 适用场景

中漏斗拓新（Lookalike 触达相似人群）、新品发布（视觉冲击力强）、品牌认知 + 转化意图（比展示更接近转化，比 Search 更靠上游）。

### 9.3 素材要求

| 格式     | 规格                                 | 说明            |
| -------- | ------------------------------------ | --------------- |
| 图片广告 | 1:1 (1200×1200) + 1.91:1 (1200×628)  | 必须            |
| 视频广告 | 横版 16:9 + 竖版 9:16                | 强烈建议        |
| 轮播广告 | 2-10 张卡片，每张含图片 + 标题 + URL | 电商/多产品推荐 |
| Logo     | 1:1 (1200×1200)                      | 必须            |

### 9.4 受众选项

与 PMax 不同，Demand Gen 的受众是**硬定向**（不会自动扩展到受众之外）：

- **Lookalike 细分：** 基于 Customer Match 或网站访客列表生成相似受众（窄/均衡/宽）
- **Custom Segments：** 基于搜索关键词或浏览 URL
- **In-Market / Affinity：** Google 标准受众
- **Your Data：** 再营销、Customer Match

### 9.5 出价策略

| 目标     | 出价策略                          | 适用场景                           |
| -------- | --------------------------------- | ---------------------------------- |
| 转化     | Maximize Conversions / tCPA       | 有明确转化目标和转化数据           |
| 点击     | Maximize Clicks                   | 品牌认知、流量导入、无足够转化数据 |
| 转化价值 | Maximize Conversion Value / tROAS | 电商，不同产品价值差异大           |

### 9.6 Demand Gen vs PMax

| 维度      | Demand Gen                 | PMax                           |
| --------- | -------------------------- | ------------------------------ |
| 版位      | YouTube + Discover + Gmail | 全渠道（含 Search + Shopping） |
| 受众      | 硬定向                     | 信号式（可扩展）               |
| 素材控制  | 高（可预览每种格式）       | 低（Google 自动组合）          |
| 搜索/购物 | 不包含                     | 包含                           |
| 适合阶段  | 中上漏斗（创造需求）       | 中下漏斗（捕获需求）           |

### 9.7 Demand Gen + PMax 协同

**理想模型：** Demand Gen 上游创造需求 → PMax / Search 下游捕获转化。Demand Gen 的直接转化数据可能偏低，需关注辅助转化报告。

## 10. AI Max for Search 协同

### 10.1 AI Max 功能概览

AI Max for Search 是 Google 在 Search 系列中集成的 AI 优化功能包：更广泛的匹配（类似强制广泛匹配）、文字定制（AI 改写标题/描述）、最终网址扩展（自动选择最相关着陆页）、兴趣地点定位（向对目标地区感兴趣但不在该地区的用户展示）。

### 10.2 何时启用 / 不启用

**启用条件：** 月转化 50+、网站页面丰富架构清晰、非敏感行业、已有稳定 Search 基线。
**不启用：** 单一着陆页/产品、合规敏感行业（医疗/金融/法律）、网站内容单薄、新账户无历史数据。

### 10.3 防护措施

- `[UI 操作]` **品牌设置（Brand Settings）：** 控制 AI 如何使用品牌名称
- `[UI 操作]` **网址排除（URL Exclusions）：** 排除不想作为着陆页的页面（如博客、关于我们）
- `[UI 操作]` **网址规则（URL Rules）：** 限定 AI 只能在特定目录下选择着陆页

### 10.4 与 PMax 的交互

AI Max 让 Search 获得类似 PMax 的自动扩展能力。Search 搜索词范围变宽，可能与 PMax 更多重叠。需**每周检查两者搜索词报告**。AI Max 开启后 PMax 表现下降 → 可能是 Search 抢回了之前被 PMax 覆盖的查询。监控命令：

```bash
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso google-analysis -a <CID> --sections campaigns
```

## 11. AI Overview 中的广告

### 11.1 背景

AI Overview（AI 生成的搜索摘要）自 2025 年从约 3% 覆盖扩展到约 40% 的搜索结果页。广告可出现在 AI 摘要中。

### 11.2 关键特性

- 无法单独定向或排除
- 启用自动化功能（广泛匹配、AI Max、PMax）的系列更易被选中
- 广告需同时匹配用户查询和 AI 生成的回答上下文

### 11.3 对 PMax 的影响

PMax 搜索渠道天然适配 AI Overview（自动化程度高）。AI Overview 偏向信息型/探索型查询，PMax 可能在更早期用户旅程触达用户。

### 11.4 策略调整

- **关键词覆盖扩展：** 不仅覆盖交易型查询，也覆盖信息型/研究型查询
- **Search Themes 利用：** 在 PMax 素材组中添加信息型搜索主题，引导算法竞争 AI Overview 展示位
- **素材适配：** 广告文案需同时适用于直接搜索和 AI 摘要上下文——强调信息价值而非单纯促销
- **着陆页优化：** AI Overview 用户处于研究阶段，着陆页应提供教育性内容而非仅有转化入口

## 12. 常见问题诊断

### PMax 问题诊断速查表

| 症状                          | 可能原因                                                     | 诊断方法                                                                         | 解决方案                                                                              |
| ----------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **学习期卡住（>2 周无进展）** | 预算不足；转化量太少；素材不完整                             | 检查日预算是否 ≥ tCPA × 3；检查素材完整度                                        | 增加预算至 $50+/天；补全所有素材类型（尤其视频）；临时切换为 Max Conversions 不设目标 |
| **高花费低转化**              | 渠道分布不佳；受众信号太宽；转化跟踪有误                     | `campaigns` 查渠道分布；`audience` 查受众表现；`conversion-actions` 检查转化设置 | 收紧受众信号；检查是否有微转化干扰；验证转化跟踪代码                                  |
| **与 Search 蚕食**            | PMax 竞价品牌词或高价值非品牌词                              | `search-terms` 对比分析（详见第 2 章）                                           | `[UI]` 品牌排除 + `[CLI/UI]` Search Exact Match 保护                                  |
| **素材组不展示**              | 素材不足；素材与受众/着陆页关联度低；预算分散                | `ads` 查看素材状态                                                               | 补全素材至每种格式最低数量；合并低量素材组；增加系列预算                              |
| **CPA 突然飙升**              | 竞争加剧；转化延迟；素材疲劳；季节因素                       | 对比近 7 天 vs 前 7 天各指标                                                     | 等待 3-5 天观察是否恢复；更新素材；检查竞争对手动态                                   |
| **ROAS 远低于目标**           | tROAS 设置过高导致展示不足；产品 Feed 问题；着陆页转化率下降 | `campaigns` 查展示量趋势；`final-urls` 查着陆页数据                              | 降低 tROAS 目标 10-15%；优化产品 Feed 数据质量；检查着陆页                            |
| **展示量突然归零**            | 系列暂停/预算耗尽；审核拒绝；账户问题                        | `ad campaigns -a <CID> --json-out ./snap` 查系列状态                             | 检查系列启用状态和预算；查看审核状态；联系 Google 支持                                |

## 13. CLI 诊断流程

> 以下所有命令均通过 `siluzan-tso` CLI 执行。PMax/Demand Gen 系列的**创建和编辑需在 Google Ads UI 中完成**，CLI 仅用于数据分析和 Search 系列操作。

### 13.1 每周 PMax 健康检查

```bash
siluzan-tso google-analysis -a <CID> --sections overview            # 系列状态和整体花费
siluzan-tso google-analysis -a <CID> --sections campaigns           # PMax 花费、转化、CPA/ROAS
siluzan-tso google-analysis -a <CID> --sections search-terms        # 不相关查询和品牌词渗透
siluzan-tso google-analysis -a <CID> --sections ads                 # 识别 Low 标签素材
siluzan-tso google-analysis -a <CID> --sections conversion-actions  # 转化 action 正常运行
```

**关注：** CPA 是否在目标 ±15% 内；新出现的不相关搜索词；Low 标签素材；转化跟踪异常。

### 13.2 PMax vs Search 蚕食分析

```bash
# 对比 PMax 上线前后系列数据
siluzan-tso google-analysis -a <CID> --sections campaigns --from <BEFORE_START> --to <BEFORE_END>
siluzan-tso google-analysis -a <CID> --sections campaigns --from <AFTER_START> --to <AFTER_END>
# 搜索词重叠
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso google-analysis -a <CID> --sections keywords
# 设备维度交叉（蚕食是否集中在某设备）
siluzan-tso google-analysis -a <CID> --sections devices
```

**判断：** Search impressions 下降 > 20% + 搜索词重叠率高 → 蚕食确认。品牌搜索词花费 > 20% → 需品牌排除。详见第 2 章。

### 13.3 素材表现审查

```bash
siluzan-tso google-analysis -a <CID> --sections ads        # 素材级表现
siluzan-tso google-analysis -a <CID> --sections final-urls  # 着陆页表现
```

标记 Low 素材 → 准备替换 `[UI]`；分析 Best 素材共性 → 指导新素材方向；检查着陆页转化率异常。

### 13.4 渠道分布分析

```bash
siluzan-tso google-analysis -a <CID> --sections campaigns   # 渠道分布（2025+）
siluzan-tso google-analysis -a <CID> --sections audience     # 受众 × 渠道交叉
siluzan-tso google-analysis -a <CID> --sections geographic   # 地理维度
siluzan-tso google-analysis -a <CID> --sections devices      # 设备维度
```

**决策：** 确认渠道花费占比（参照第 5 章）→ 交叉受众数据判断低效渠道原因 → 地理/设备维度排查异常。

---

> **提示：** 本指南中标注 `[CLI 可执行]` 的操作可通过 siluzan-tso 完成；标注 `[UI 操作]` 的操作需在 Google Ads 界面中执行。AI 的角色是分析数据、诊断问题、给出建议——PMax/Demand Gen 的创建与设置变更由用户在 UI 中执行，或由 AI 协助执行 Search 系列侧的调整。
