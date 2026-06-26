# 市场全景分析

对指定的 Amazon 类目市场进行全面深入的分析，帮助卖家评估市场吸引力、竞争强度和进入可行性。

## 使用方式

用户输入: `/market-analysis [类目关键词或类目节点ID]`

参数说明:
- 第1个参数: 类目名称、关键词或 nodeIdPath（必填）
- 可附加参数: 站点(默认US)、月份(默认最近)

## 执行步骤

### 第1步: 获取类目信息

调用 `product_node` 查找类目节点:

参数:
- marketplace: 用户指定站点
- keyword: 用户输入的类目关键词

获取 nodeIdPath 后，进入下一步。

### 第2步: 并行获取市场核心数据

> 以下两个工具均只需 nodeIdPath，无数据依赖，**必须并行调用**。

同时调用以下 2 个工具:

**1. `market_research`** - 市场整体数据:
- marketplace: 用户指定站点
- nodeIdPath: 第1步获取的节点路径
- month: 指定月份（可选）
- topNum: 10（头部商品数）
- size: 50

**2. `market_research_statistics`** - 市场深入统计:
- marketplace: 用户指定站点
- nodeIdPath: 节点路径
- topN: 10
- newProduct: 根据行业特性设置（默认6）

### 第3步: 并行多维度分布分析

并行调用以下工具，获取市场的多维度数据:

1. **market_price_distribution** - 价格区间分布
   - 分析不同价格带的商品数量、销量占比、平均销量效率
   - 识别有利润空间的定价带

2. **market_brand_concentration** - 品牌集中度
   - 头部品牌销量占比
   - 与同级类目对比的品牌垄断程度
   - 新品牌生存空间评估

3. **market_product_concentration** - 商品集中度
   - 头部商品销量占比
   - 市场竞争强度判断

4. **market_seller_concentration** - 卖家集中度
   - 头部卖家垄断程度
   - 市场进入壁垒评估

5. **market_rating_distribution** - 评分值分布
   - 市场整体质量水平
   - 产品优化空间判断

6. **market_ratings_count_distribution** - 评分数分布
   - 新品评论积累门槛
   - 进入难度评估

7. **market_listing_date_distribution** - 上架时间分布
   - 新品接受度
   - 市场更新迭代速度

8. **market_seller_country_distribution** - 卖家所属地分布
   - 中国卖家/本土卖家占比
   - 竞争格局分析

9. **market_seller_type_concentration** - 发货类型分布
   - FBA/FBM/Amazon自营占比
   - 配送策略建议

10. **market_ebc_distribution** - A+页面与视频分布
    - 内容配置与销量关系
    - Listing内容投入建议

11. **market_product_demand_trend** - 需求趋势
    - 页面浏览量、退货率、搜索购买比
    - 需求规模与转化效率

### 第4步: 生成市场分析报告

综合所有数据，输出完整的市场分析报告:

#### 一、市场概览
- 类目名称与层级路径
- 商品总数、品牌数、卖家数
- 月总销量、月总销售额
- 平均价格、平均评分

#### 二、市场吸引力评估 (1-10分)

| 维度 | 评分 | 说明 |
|------|------|------|
| 市场规模 | x/10 | 基于月销量/销售额 |
| 增长性 | x/10 | 基于需求趋势 |
| 利润空间 | x/10 | 基于平均毛利率和价格带 |
| 竞争强度 | x/10 | 基于集中度指标（反向计分）|
| 新品友好度 | x/10 | 基于新品占比和上架时间分布 |
| 进入门槛 | x/10 | 基于评分/评论门槛（反向计分）|
| **综合评分** | **x/10** | 加权平均 |

#### 三、竞争格局分析
- 头部商品集中度及趋势
- 头部品牌集中度及与同级类目对比
- 卖家类型分布（FBA/FBM/自营）及竞争策略
- 卖家所属地分布及中国卖家竞争压力

#### 四、价格与利润分析
- 各价格区间商品数量与销量占比
- 最佳定价带建议
- 利润空间评估

#### 五、新品进入评估
- 新品数量占比
- 新品平均销量表现
- 评论积累门槛分析
- A+/视频内容投入建议

#### 六、风险与机会
- 主要风险点
- 差异化切入方向
- 内容优化建议

#### 七、结论与建议
- 是否推荐进入该市场
- 推荐的进入策略（价格带、差异化方向）
- 预估投入产出周期

## 输出格式

使用 Markdown 表格、评分卡和结构化列表呈现。关键结论用加粗标注，风险用警告标识。
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`market_brand_concentration`](../../reference/market_brand_concentration.md)
- [`market_ebc_distribution`](../../reference/market_ebc_distribution.md)
- [`market_listing_date_distribution`](../../reference/market_listing_date_distribution.md)
- [`market_price_distribution`](../../reference/market_price_distribution.md)
- [`market_product_concentration`](../../reference/market_product_concentration.md)
- [`market_product_demand_trend`](../../reference/market_product_demand_trend.md)
- [`market_rating_distribution`](../../reference/market_rating_distribution.md)
- [`market_ratings_count_distribution`](../../reference/market_ratings_count_distribution.md)
- [`market_research`](../../reference/market_research.md)
- [`market_research_statistics`](../../reference/market_research_statistics.md)
- [`market_seller_concentration`](../../reference/market_seller_concentration.md)
- [`market_seller_country_distribution`](../../reference/market_seller_country_distribution.md)
- [`market_seller_type_concentration`](../../reference/market_seller_type_concentration.md)
- [`product_node`](../../reference/product_node.md)
