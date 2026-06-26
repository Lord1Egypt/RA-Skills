# 蓝海机会挖掘

通过 ABA 数据和关键词趋势分析，系统发现 Amazon 市场中正在上升、增长或被低估的关键词和产品机会。

## 使用方式

用户输入: `/opportunity-finder [关键词或类目]`

参数说明:
- 第1个参数: 关键词、类目或留空查看全局趋势（必填）
- 可附加参数: 站点(默认US)、搜索模式(热门/异动/增长/飙升/潜力/长尾)

## 执行步骤

### 第1步: 确认分析参数

向用户确认:
- **目标站点**: 默认 US
- **搜索模式**: 默认全部扫描
  - 热门市场: 高搜索量关键词
  - 异动市场: 排名变化异常
  - 持续增长市场: 稳步上升
  - 快速飙升市场: 短期爆发
  - 潜力市场: 低竞争高需求
  - 长尾市场: 精准细分需求
- **类目范围**: 全类目或指定类目

### 第2步: ABA 周度趋势扫描

调用 `aba_research_weekly` 进行周度趋势扫描:

根据用户选择的搜索模式，分别查询:

**模式1 - 快速飙升市场** (快速发现短期爆发):
- marketplace: 用户指定站点
- searchModel: 4
- includeKeywords: 用户关键词（可选）
- order: 按 `searches` 降序（aba_research_weekly 响应字段为 keyword/searches/clicks/ctr/cvShareRate/rank，可用其中之一作为 field）
- size: 40

**模式2 - 持续增长市场** (发现稳定增长):
- marketplace: 用户指定站点
- searchModel: 3
- includeKeywords: 用户关键词（可选）
- order: 按 `searches` 降序
- size: 15

**模式3 - 潜力市场** (低竞争高需求):
- marketplace: 用户指定站点
- searchModel: 5
- includeKeywords: 用户关键词（可选）
- order: 按 `searches` 降序
- size: 15

### 第3步: ABA 月度趋势验证

调用 `aba_research_monthly` 进行月度趋势验证:

参数同上，但按月维度获取数据，验证短期趋势是否在月度上也成立。

### 第4步: 关键词市场深度评估

对筛选出的 TOP 10 机会关键词，**并行调用** `keyword_research` 和 `keyword_research_trends`（这些工具不支持批量查询，必须并行调用以节省等待时间）评估市场可行性:

参数（每个关键词）:

**`keyword_research`** - 市场全景快照:
- marketplace: 用户指定站点
- keywords: 机会关键词

**`keyword_research_trends`** - 关键词搜索趋势:
- marketplace: 用户指定站点
- keyword: 机会关键词

获取: 月搜索量、购买量、商品数、供需比、PPC竞价等完整数据，以及关键词的历史搜索趋势。

### 第5步: Google 趋势与 ABA 趋势交叉验证

对 TOP 5 关键词，**并行调用** `google_trend` 和 `aba_research_trend` 验证:

**`google_trend`** - 外部趋势:
- marketplace: 用户指定站点
- keyword: 机会关键词
- googleProp: "shoppingCart"
- monthly: true

**`aba_research_trend`** - ABA 趋势分析:
- marketplace: 用户指定站点
- keyword: 机会关键词

获取: Google Shopping 搜索趋势 + ABA 排名历史趋势，确认是否为 Amazon 站内短期波动还是外部真实需求增长。

### 第6步: 市场可行性验证

对最有潜力的 TOP 3 方向，**并行调用** `market_research` 验证:

参数:
- marketplace: 用户指定站点
- departmentKeyword: 机会关键词

获取: 类目市场规模、竞争度、新品表现等。

### 第7步: 生成机会挖掘报告

#### 一、机会扫描概览

| 搜索模式 | 发现关键词数 | 高潜力词数 |
|----------|-------------|-----------|
| 快速飙升 | xx | xx |
| 持续增长 | xx | xx |
| 潜力市场 | xx | xx |

#### 二、飙升关键词 (短期爆发机会)

| 关键词 | 周搜索量 | 增长率 | 商品数 | 供需比 | 点击集中度 | 机会评分 |
|--------|---------|--------|--------|--------|-----------|---------|
| word1  | xxx     | +xx%   | xx     | xx     | xx%       | ★★★★★  |
| word2  | xxx     | +xx%   | xx     | xx     | xx%       | ★★★★☆  |

#### 三、持续增长关键词 (长期布局机会)

| 关键词 | 月搜索量 | 近3月增长率 | 同比增长率 | 商品数 | PPC竞价 | 机会评分 |
|--------|---------|------------|-----------|--------|---------|---------|
| word3  | xxx     | +xx%       | +xx%      | xx     | $x.xx   | ★★★★★  |

#### 四、潜力关键词 (蓝海市场)

| 关键词 | 月搜索量 | 购买率 | 商品数 | 供需比 | SPR | 机会评分 |
|--------|---------|--------|--------|--------|-----|---------|
| word4  | xxx     | xx%    | xx     | xx     | xx  | ★★★★★  |

#### 五、趋势交叉验证

| 关键词 | ABA周度 | ABA月度 | ABA趋势 | Google趋势 | 一致性 | 可信度 |
|--------|---------|---------|---------|-----------|--------|--------|
| word1  | 飙升    | 上升    | 上升    | 上升      | 高     | 高     |
| word2  | 增长    | 平稳    | 平稳    | 平稳      | 中     | 中     |

#### 六、TOP 3 机会详细分析

每个机会方向包含:
- 关键词/市场需求分析
- 竞争强度评估
- 新品进入可行性
- 预估利润空间
- 建议进入策略

#### 七、机会优先级排序

| 优先级 | 机会方向 | 类型 | 预估投入 | 预估回报 | 时间窗口 |
|--------|---------|------|---------|---------|---------|
| 1      | xxx     | 飙升 | $xxx    | $xxx/月 | 紧急    |
| 2      | xxx     | 增长 | $xxx    | $xxx/月 | 1-3月   |
| 3      | xxx     | 蓝海 | $xxx    | $xxx/月 | 3-6月   |

#### 八、行动建议
- 需要立即抓住的时间敏感型机会
- 值得长期布局的增长型机会
- 低竞争适合新品测试的蓝海机会
- 风险提示和注意事项

## 输出格式

使用 Markdown 表格、星级评分呈现。时间敏感型机会用紧急标识，长期机会用推荐标识。
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`aba_research_monthly`](../../reference/aba_research_monthly.md)
- [`aba_research_trend`](../../reference/aba_research_trend.md)
- [`aba_research_weekly`](../../reference/aba_research_weekly.md)
- [`google_trend`](../../reference/google_trend.md)
- [`keyword_research`](../../reference/keyword_research.md)
- [`keyword_research_trends`](../../reference/keyword_research_trends.md)
- [`market_research`](../../reference/market_research.md)
