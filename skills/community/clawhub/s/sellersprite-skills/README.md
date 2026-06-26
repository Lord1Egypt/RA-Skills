# 卖家精灵 Skills 索引

> 共 27 个 Skills，覆盖从品类扫描到产品开发的全链路选品流程。
> 每个 Skill 是一个独立的、可被 AI 直接执行的"数据技能卡"。

---

## 全局参数默认值

> 以下参数适用于所有 MCP 工具调用，未显式指定时使用默认值。

| 参数 | 默认值  | 说明 |
|------|------|------|
| `marketplace` | `US` | 目标站点（US/JP/UK/DE/FR/IT/ES/CA/IN） |
| `matchType` | `2`  | 关键词匹配方式：`1`=词组匹配，`2`=模糊匹配，`3`=精准匹配（默认 `2`） |
| `size` | `50` | 每页返回条数（默认：50，最大：100） |

调用时显式传值可覆盖默认值，例如 `matchType: 3` 切换为精准匹配以收窄搜索范围。

---

## 一、综合分析（10 个）

> 多步骤工作流，编排多个工具生成完整报告。Claude Code 通过 `/命令` 调用，其他客户端对话中引用名称触发。

| Skill | 核心场景 | 一句话说明 |
|-------|---------|-----------|
| [智能选品助手](comprehensive/product-research.md) | 选品阶段 | 按多维条件筛选潜力商品，评估进入可行性 |
| [市场全景分析](comprehensive/market-analysis.md) | 市场调研 | 对目标类目进行 11 个维度的全方位评估 |
| [竞品深度拆解](comprehensive/competitor-analysis.md) | 竞品分析 | 对竞品 ASIN 进行 8 大维度的全面拆解 |
| [关键词选品研究](comprehensive/keyword-research.md) | 选品+关键词 | 基于关键词的市场需求分析 |
| [Listing 优化诊断](comprehensive/listing-optimizer.md) | 运营优化 | 诊断 Listing 质量，发现关键词覆盖缺口 |
| [流量结构分析](comprehensive/traffic-analysis.md) | 流量分析 | 拆解 ASIN 流量来源，分析自然/广告/推荐结构 |
| [蓝海机会挖掘](comprehensive/opportunity-finder.md) | 机会发现 | 通过 ABA 趋势发现飙升/增长/潜力关键词 |
| [买家评论洞察](comprehensive/review-insights.md) | 产品优化 | 深度分析买家评论，提炼痛点和改进方向 |
| [定价策略分析](comprehensive/pricing-strategy.md) | 定价决策 | 分析市场价格带分布，制定最优定价策略 |
| [广告投放优化](comprehensive/ad-optimizer.md) | 广告投放 | 基于关键词数据优化 PPC 广告策略 |

## 二、战术选品（17 个）

> 单一策略，聚焦一个具体打法，带精确参数配置。对话中引用名称触发。

### 新品爆发型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [新品快速爆发](tactical/new-product-burst.md) | `product_research` | 上架<=2月、销量>=300、Review<=100 |
| [隐形爆款](tactical/hidden-bestseller.md) | `product_research` | 上架<=3月、销量>=500、Review<=50 |

### 关键词趋势型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [ABA高增长趋势词](tactical/aba-high-growth-trend.md) | `keyword_research` | 近3月持续增长+点击不集中 |
| [流量分散关键词](tactical/low-monopoly-keyword.md) | `keyword_miner` | 搜索>=5000+集中度<50% |
| [标题密度漏洞](tactical/title-density-gap.md) | `keyword_miner` | 标题密度<=5的长尾词 |

### 产品缺陷型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [热销低评分产品](tactical/hot-low-rating.md) | `product_research` | 月销>=1000+评分<=4.2 |
| [评论语义分析](tactical/review-sentiment.md) | `review` | 差评NLP聚类 -> 改良指南 |

### 类目结构型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [低品牌垄断类目](tactical/low-brand-monopoly.md) | `market_research` | 品牌集中度<45% |
| [高新品占比市场](tactical/high-new-product-ratio.md) | `market_research` | 新品占比>5%+新品仍出单 |
| [高毛利轻小品](tactical/high-margin-lightweight.md) | `product_research` | FBA<=$4+毛利>=50% |

### 流量防伪型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [自然流量反查](tactical/natural-traffic-audit.md) | `traffic_source` | 自然流量占比>60% |
| [变体拆解模型](tactical/variant-gap-analysis.md) | `asin_detail` | 找未被覆盖的变体缺口 |

### 机会捕捉型

| Skill | 核心工具 | 一句话逻辑 |
|-------|---------|-----------|
| [本土溢价降维](tactical/local-premium-disruption.md) | `product_research` | 美国卖家+高价+高销 |
| [FBM拦截](tactical/fbm-intercept.md) | `product_research` | FBM发货+月销>=300 |
| [低质量Listing高销量](tactical/poor-listing-winner.md) | `product_research` | LQS<=60+月销>=400 |
| [高客单长尾](tactical/high-ticket-long-tail.md) | `keyword_miner` | 均价>=$80+搜索量适中 |
| [季节前置爆破](tactical/seasonal-prepositioning.md) | `keyword_miner` | 历史同期环比增长>100% |

---

## 推荐组合链路

```
品类扫描 -> 低品牌垄断 / 高新品占比（找蓝海类目）
    |
关键词挖掘 -> ABA增长词 / 流量分散词 / 标题密度漏洞（找增长词+机会词）
    |
竞品锁定 -> 新品爆发 / 隐形爆款 / 热销低评分（找目标竞品）
    |
竞品验真 -> 自然流量反查（流量防伪）
    |
痛点提炼 -> 评论语义分析（评论分析）
    |
产品开发 -> 变体拆解 + 高毛利轻小（利润验证）
```
