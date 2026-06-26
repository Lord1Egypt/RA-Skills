# 智能选品助手

根据卖家的选品需求，系统性筛选和分析 Amazon 商品，从数据维度评估产品潜力，辅助选品决策。

## 使用方式

用户输入: `/product-research [关键词/类目]`

参数说明:
- 第1个参数: 关键词或类目名称（必填）
- 可附加参数: 站点(默认US)、价格区间、月销量范围、评分范围等

## 执行步骤

### 第1步: 确认选品条件

向用户确认以下选品筛选条件（如用户未指定则使用推荐默认值）:
- **目标站点**: 默认 US
- **价格区间**: 默认 $15-$50
- **月销量下限**: 默认 300
- **最高评分数**: 默认 500
- **最低评分值**: 默认 4.0
- **毛利率下限**: 默认 20%
- **商品重量上限**: 默认 500g
- **关键词匹配方式**: 默认模糊匹配

### 第2步: 查找类目节点

调用 `product_node` 工具，根据用户输入的关键词查找对应的 Amazon 类目节点路径，获取 nodeIdPath。

参数:
- marketplace: 用户指定的站点
- keyword: 用户输入的关键词

### 第3步: 商品筛选

调用 `product_research` 工具，按条件筛选商品。

参数设置:
- marketplace: 用户指定的站点
- keyword: 用户输入的关键词
- nodeIdPath: 第2步获取的类目路径（可选）
- minPrice / maxPrice: 价格区间
- minUnits: 月销量下限
- maxRatings: 最高评分数
- minRating: 最低评分值
- minProfit: 毛利率下限
- maxWeights: 重量上限
- matchType: 匹配方式（integer，1=词组匹配，2=模糊匹配，3=精准匹配，默认 2）
- order: 按 `units`（月销量）降序排列
- size: 20
- page: 1

### 第4步: 市场可行性验证

对筛选结果中的 TOP 3-5 商品，**并行调用**以下工具（这些工具不支持批量查询，必须并行调用）:

1. **asin_detail** - 获取商品完整详情（品牌、卖家、变体、配送方式等）— 为每个 ASIN 单独调用，所有调用并行执行
2. **asin_prediction** - 获取近14个月销量趋势，判断增长性 — 为每个 ASIN 单独调用，所有调用并行执行
3. **market_research_statistics** - 验证类目整体市场机会 — 与所有 ASIN 级别调用并行执行
4. **google_trend** - 验证关键词搜索趋势 — 与所有 ASIN 级别调用并行执行（可选）

> **并行策略**: 假设筛选出 N 个商品（N=3~5），则本轮共发起 2N+1~2N+2 个并行调用（N 个 asin_detail + N 个 asin_prediction + 1 个 market_research_statistics + 0~1 个 google_trend），切勿串行逐个调用。

### 第5步: 生成选品报告

综合所有数据，输出结构化选品报告，包含以下内容:

#### 一、筛选概览
- 搜索关键词、类目、站点
- 符合条件的商品总数
- 市场整体规模（月销量/销售额）

#### 二、潜力商品推荐 (TOP 5)
每个商品包含:
- ASIN、标题、品牌
- 价格、月销量、月销售额
- 评分值、评分数
- BSR排名（大类/小类）
- 毛利率、FBA费用
- 上架时间
- 变体数量
- 卖家类型（FBA/FBM/Amazon自营）

#### 三、趋势分析
- TOP商品近14个月销量趋势（增长/稳定/衰退）
- 类目整体需求趋势
- Google Trends 验证（如第4步已调用则直接引用结果）

#### 四、风险评估
- 商品集中度风险（头部垄断程度）
- 品牌集中度风险
- 新品进入难度（评分门槛、评论门槛）
- 价格竞争激烈程度

#### 五、选品建议
- 是否推荐进入该细分市场
- 推荐的价格区间和差异化方向
- 预估投入和回报周期
- 需要注意的风险点

## 输出格式

使用 Markdown 表格和结构化列表呈现数据，关键指标用加粗标注。评分和趋势用直观的符号表示。
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`asin_detail`](../../reference/asin_detail.md)
- [`asin_prediction`](../../reference/asin_prediction.md)
- [`google_trend`](../../reference/google_trend.md)
- [`market_research_statistics`](../../reference/market_research_statistics.md)
- [`product_node`](../../reference/product_node.md)
- [`product_research`](../../reference/product_research.md)
