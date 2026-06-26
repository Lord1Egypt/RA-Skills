---
name: sellersprite-skills
description: 卖家精灵 Amazon 选品 AI Skills 全集 —— 10 个综合分析工作流（/product-research、/market-analysis、/competitor-analysis 等）+ 17 个战术选品策略卡（新品爆发、ABA 高增长、低品牌垄断、变体拆解等），通过 38 个 MCP 数据工具完成从品类扫描到选品落地的全链路。适用于跨境电商卖家、Amazon 选品研究、运营优化与广告投放决策。
license: MIT-0
version: 0.1.17
---

# SellerSprite Skills 体系

> 本文件是 SellerSprite CLI 的技能元数据总览，用于向 AI 智能体说明全部 27 个 Skills 的名称、用途和调用方式。

---

## 技能体系总览

SellerSprite 提供 **27 个 AI Skills**，分为两层：

| 层级 | 数量 | 调用方式 | 定位 |
|------|------|----------|------|
| **综合分析** | 10 个 | `/命令` | 多步骤工作流，生成完整报告 |
| **战术选品** | 17 个 | 对话引用名称 | 单一策略，聚焦具体打法 |

---

## 一、综合分析 Skills（10 个）

通过 `/命令` 调用，由 Claude Code 直接执行多步骤分析流程。

| 命令 | 技能名称 | 用途 | 核心工具 |
|------|----------|------|----------|
| `/product-research` | 智能选品助手 | 按多维条件筛选潜力商品 | `product_research` + `product_node` |
| `/market-analysis` | 市场全景分析 | 对目标类目进行 11 维度全方位评估 | `market_research` + 统计工具集 |
| `/competitor-analysis` | 竞品深度拆解 | 对竞品 ASIN 进行 8 大维度全面拆解 | `asin_detail` + `traffic_keyword` |
| `/keyword-research` | 关键词选品研究 | 基于关键词的市场需求分析 | `keyword_research` + `keyword_miner` |
| `/listing-optimizer` | Listing 优化诊断 | 诊断 Listing 质量，发现关键词覆盖缺口 | `traffic_listing` + `keyword_order` |
| `/traffic-analysis` | 流量结构分析 | 拆解 ASIN 流量来源，分析自然/广告/推荐结构 | `traffic_source` + `traffic_keyword_stat` |
| `/opportunity-finder` | 蓝海机会挖掘 | 通过 ABA 趋势发现飙升/增长/潜力关键词 | `aba_research_trend` + `google_trend` |
| `/review-insights` | 买家评论洞察 | 深度分析买家评论，提炼痛点和改进方向 | `review` + NLP 分析 |
| `/pricing-strategy` | 定价策略分析 | 分析市场价格带分布，制定最优定价策略 | `market_price_distribution` |
| `/ad-optimizer` | 广告投放优化 | 基于关键词数据优化 PPC 广告策略 | `keyword_order` + `traffic_keyword` |

### 综合分析使用方式

```
用户: /market-analysis earbuds US
AI: [执行 4-5 步工作流，生成完整市场分析报告]
```

---

## 二、战术选品 Skills（17 个）

在对话中引用技能名称触发，由 AI 按卡片参数执行单一策略。

### 2.1 新品爆发型（2）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **新品快速爆发** | ⭐ | `product_research` | 上架 ≤2月、销量 ≥300、Review ≤100 | `tactical/new-product-burst.md` |
| **隐形爆款** | ⭐ | `product_research` | 上架 ≤3月、销量 ≥500、Review ≤50 | `tactical/hidden-bestseller.md` |

### 2.2 关键词趋势型（3）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **ABA 高增长趋势词** | ⭐⭐ | `keyword_research` | 近3月持续增长 + 点击不集中 | `tactical/aba-high-growth-trend.md` |
| **流量分散关键词** | ⭐⭐ | `keyword_miner` | 搜索 ≥5000 + 集中度 <50% | `tactical/low-monopoly-keyword.md` |
| **标题密度漏洞** | ⭐⭐⭐ | `keyword_miner` | 标题密度 ≤5 的长尾词 | `tactical/title-density-gap.md` |

### 2.3 产品缺陷型（2）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **热销低评分产品** | ⭐⭐ | `product_research` | 月销 ≥1000 + 评分 ≤4.2 | `tactical/hot-low-rating.md` |
| **评论语义分析** | ⭐⭐⭐ | `review` | 差评 NLP 聚类 → 改良指南 | `tactical/review-sentiment.md` |

### 2.4 类目结构型（3）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **低品牌垄断类目** | ⭐⭐ | `market_research` | 品牌集中度 <45% | `tactical/low-brand-monopoly.md` |
| **高新品占比市场** | ⭐⭐ | `market_research` | 新品占比 >5% + 新品仍出单 | `tactical/high-new-product-ratio.md` |
| **高毛利轻小品** | ⭐⭐ | `product_research` | FBA ≤$4 + 毛利 ≥50% | `tactical/high-margin-lightweight.md` |

### 2.5 流量防伪型（2）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **自然流量反查** | ⭐⭐⭐ | `traffic_source` | 自然流量占比 >60% | `tactical/natural-traffic-audit.md` |
| **变体拆解模型** | ⭐⭐⭐ | `asin_detail` | 找未被覆盖的变体缺口 | `tactical/variant-gap-analysis.md` |

### 2.6 机会捕捉型（5）

| 技能名称 | 难度 | 核心工具 | 一句话逻辑 | 文件 |
|----------|------|----------|-----------|------|
| **本土溢价降维** | ⭐⭐ | `product_research` | 美国卖家 + 高价 + 高销 | `tactical/local-premium-disruption.md` |
| **FBM 拦截** | ⭐ | `product_research` | FBM 发货 + 月销 ≥300 | `tactical/fbm-intercept.md` |
| **低质量 Listing 高销量** | ⭐⭐ | `product_research` | LQS ≤60 + 月销 ≥400 | `tactical/poor-listing-winner.md` |
| **高客单长尾** | ⭐⭐⭐ | `keyword_miner` | 均价 ≥$80 + 搜索量适中 | `tactical/high-ticket-long-tail.md` |
| **季节前置爆破** | ⭐⭐⭐⭐ | `keyword_miner` | 历史同期环比增长 >100% | `tactical/seasonal-prepositioning.md` |

### 战术选品使用方式

```
用户: 帮我找一下最近上架的爆款新品
AI: [识别到"新品快速爆发"技能，按卡片参数执行筛选]
```

---

## 三、全局参数

以下参数适用于所有工具调用：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `marketplace` | `US` | 目标站点：US/JP/UK/DE/FR/IT/ES/CA/IN |
| `matchType` | `2` | 关键词匹配：1=词组 2=模糊 3=精准（默认 2） |
| `size` | `50` | 每页返回条数（默认 50，最大 100） |

---

## 四、推荐组合链路

```
品类扫描 -> 低品牌垄断 / 高新品占比
    |
关键词挖掘 -> ABA增长词 / 流量分散词 / 标题密度漏洞
    |
竞品锁定 -> 新品爆发 / 隐形爆款 / 热销低评分
    |
竞品验真 -> 自然流量反查
    |
痛点提炼 -> 评论语义分析
    |
产品开发 -> 变体拆解 + 高毛利轻小
```

---

## 五、文件结构

```
skills/
  SKILL.md                          # 本文件：技能总览元数据
  README.md                         # Skill 索引（27 个 Skill 的详细列表）
  agent-instructions.md             # 项目概述 + 38 个 MCP 工具清单，作为 AI 客户端的 CLAUDE.md/AGENTS.md 写入
  comprehensive/                    # 综合分析 Skills（10 个）
    product-research.md
    market-analysis.md
    competitor-analysis.md
    keyword-research.md
    listing-optimizer.md
    traffic-analysis.md
    opportunity-finder.md
    review-insights.md
    pricing-strategy.md
    ad-optimizer.md
  tactical/                         # 战术选品 Skills（17 个）
    new-product-burst.md / hidden-bestseller.md
    aba-high-growth-trend.md / low-monopoly-keyword.md / title-density-gap.md
    hot-low-rating.md / review-sentiment.md
    low-brand-monopoly.md / high-new-product-ratio.md / high-margin-lightweight.md
    natural-traffic-audit.md / variant-gap-analysis.md
    local-premium-disruption.md / fbm-intercept.md / poor-listing-winner.md
    high-ticket-long-tail.md / seasonal-prepositioning.md
```

---

## 六、工具前缀说明

当通过 MCP 客户端（如 Claude Code、Cursor）调用工具时，使用完整工具名：

```
mcp__sellersprite__<tool_name>
```

例如：`mcp__sellersprite__asin_detail`、`mcp__sellersprite__product_research`

完整工具清单见 `agent-instructions.md`。
