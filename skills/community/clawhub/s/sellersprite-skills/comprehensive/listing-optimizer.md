# Listing 优化诊断

对指定的 Amazon 商品 Listing 进行全面诊断，从关键词覆盖、流量结构、评论反馈等维度给出优化建议。

## 使用方式

用户输入: `/listing-optimizer [ASIN]`

参数说明:
- 第1个参数: 商品 ASIN（必填）
- 可附加参数: 站点(默认US)、对比竞品ASIN（可选）

## 执行步骤

### 第1步: 获取 Listing 完整信息

调用 `asin_detail` 获取商品详情:

参数:
- marketplace: 用户指定站点
- asin: 目标ASIN

获取: 标题、五点描述、类目、Listing质量分、价格、评分、变体、标识等。

### 第2步: 关键词与流量批量分析（并行调用）

以下三个调用均基于目标 ASIN，无数据依赖，**并行执行**:

**2a.** 调用 `traffic_keyword_stat` 获取流量结构概览:

参数:
- marketplace: 用户指定站点
- asin: 目标ASIN
- month: 历史月份 yyyyMM（可选，不传默认近30天）

获取: 自然搜索词、广告词、推荐词数量分布。

**2b.** 调用 `traffic_keyword` 获取具体流量词:

参数:
- marketplace: 用户指定站点
- asin: 目标ASIN
- order: 按 trafficPercentage 降序
- size: 10

获取: 当前已获取流量的关键词列表、搜索量、排名、流量占比等。

**2c.** 调用 `keyword_order` 进行关键词反查:

参数:
- marketplace: 用户指定站点
- asins: [目标ASIN]
- reverseType: "M"
- date: 当月，格式 yyyyMM（如 "202605"）。reverseType="M" 时用 yyyyMM 格式；reverseType="W" 时用 yyyyMMdd 格式（当周周六）

获取: 该 ASIN 参与曝光与转化的关键词完整列表，识别转化优质词和流失词。

### 第3步: 关键词拓展与评论反馈（并行调用）

以下两个调用无数据依赖，**并行执行**:

**3a.** 调用 `traffic_extend` 挖掘更多潜在关键词:

参数:
- marketplace: 用户指定站点
- asinList: [目标ASIN]
- queryType: 2
- minSearches: 1000
- size: 10

获取: 竞品有流量但本商品未覆盖的关键词机会。

**3b.** 调用 `review` 获取评论数据:

参数:
- marketplace: 用户指定站点
- asin: 目标ASIN
- categoryId: 可选；如需提升类目相关性，可先调用 `asin_prediction` 取 `asinDetail.categoryId`（asin_detail 响应中无此字段）
- size: 10

### 第4步: 竞品 Listing 对比（可选，并行调用）

如果用户提供了对比竞品 ASIN，以下两个调用**并行执行**:

**4a.** 调用 `competitor_lookup` 获取竞品数据:

参数:
- marketplace: 用户指定站点
- asins: [竞品ASIN列表]

**4b.** 调用 `traffic_keyword` 获取竞品流量关键词（每个竞品 ASIN 并行调用）:

参数:
- marketplace: 用户指定站点
- asin: 单个竞品ASIN
- order: 按 trafficPercentage 降序
- size: 10

获取所有竞品的流量关键词，用于对比关键词覆盖差异。

### 第5步: 生成 Listing 优化报告

#### 一、Listing 质量诊断

| 诊断项 | 当前状态 | 评分 | 优化建议 |
|--------|---------|------|---------|
| 标题质量 | xxx | x/10 | xxx |
| 五点描述 | xxx | x/10 | xxx |
| 关键词覆盖 | xxx | x/10 | xxx |
| 流量结构 | xxx | x/10 | xxx |
| A+页面 | 有/无 | x/10 | xxx |
| 主图视频 | 有/无 | x/10 | xxx |
| 评分表现 | x.x星 | x/10 | xxx |
| Listing质量分 | xx/100 | - | - |
| **综合评分** | - | **x/10** | - |

#### 二、关键词覆盖分析

**已覆盖核心关键词** (当前有流量的关键词):
| 关键词 | 月搜索量 | 自然排名 | 广告排名 | 流量占比 | 状态 |
|--------|---------|---------|---------|---------|------|
| word1  | xxx     | #x      | #x      | xx%     | 优质 |
| word2  | xxx     | #x      | -       | xx%     | 稳定 |

**缺失关键词** (竞品有流量但本商品未覆盖):
| 关键词 | 月搜索量 | 购买率 | PPC竞价 | 优先级 |
|--------|---------|--------|---------|--------|
| word3  | xxx     | xx%    | $x.xx   | 高     |
| word4  | xxx     | xx%    | $x.xx   | 中     |

**转化流失关键词** (有曝光但转化差):
| 关键词 | 搜索量 | 状态 | 建议 |
|--------|--------|------|------|
| word5  | xxx    | 流失 | 优化/否词 |

#### 三、标题优化建议
- 当前标题分析（长度、关键词密度、可读性）
- 推荐优化标题（融入高价值缺失关键词）
- 关键词布局位置建议

#### 四、五点描述优化建议
- 当前五点描述评估
- 基于评论反馈的卖点提炼
- 推荐优化的五点描述框架

#### 五、流量结构优化建议
- 自然流量提升策略
- 广告投放关键词建议
- 推荐流量获取建议（AC/ER/4星）

#### 六、竞品对比（如提供）
- 关键词覆盖差异
- 流量结构对比
- 可借鉴的优化方向

#### 七、优先级行动清单

| 优先级 | 优化动作 | 预期效果 | 工具支持 |
|--------|---------|---------|---------|
| P0 | xxx | xxx | xxx |
| P1 | xxx | xxx | xxx |
| P2 | xxx | xxx | xxx |

## 输出格式

使用 Markdown 表格呈现，优先级用 P0/P1/P2 标注。核心建议用加粗标注。
---

## 参考文档

本 Skill 涉及的 API 详细参数说明：

- [`asin_detail`](../../reference/asin_detail.md)
- [`competitor_lookup`](../../reference/competitor_lookup.md)
- [`keyword_order`](../../reference/keyword_order.md)
- [`review`](../../reference/review.md)
- [`traffic_extend`](../../reference/traffic_extend.md)
- [`traffic_keyword`](../../reference/traffic_keyword.md)
- [`traffic_keyword_stat`](../../reference/traffic_keyword_stat.md)
