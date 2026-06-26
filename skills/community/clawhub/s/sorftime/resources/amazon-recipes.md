> 公共参考见 [`_common.md`](./_common.md)：CLI 调用模板、Domain 表、错误码、返回结构、限流约束。
> 各接口详细参数见对应 resources 文件。本文档只提供多接口编排的 CLI 命令链配方。

# Amazon 多接口编排配方

**用途**：展示 `sorftime-cli` 比 `sorftime-agent-x`（MCP 预设工具）灵活的核心场景——任意 endpoint 组合、批量脚本、自定义工作流。

**阅读前提**：已熟悉各接口的单独用法（参见 amazon-category.md / amazon-product.md / amazon-keyword.md / amazon-monitoring-*.md）。

---

## 配方 1：选品配方（CategoryRequest → ProductSearch → KeywordExtends → ProductReviewsQuery）

**场景**：从目标类目出发，筛选潜力产品，验证关键词流量，检查评论 sentiment。

**为什么 MCP 做不到**：MCP 预设工具通常只封装单接口调用，无法把 CategoryRequest 的 ASIN 列表自动喂给 ProductQuery 做二次过滤，更无法把过滤后的 ASIN 再串进 KeywordExtends 和 ReviewsQuery。

```bash
# Step 1: 获取类目 Best Seller Top 100（当前数据）
# 从 CategoryTree 拿到 nodeId，例如 3743561 = Kitchen & Dining
sorftime api CategoryRequest '{"nodeId": "3743561"}' --domain 1

# Step 2: 用 ProductQuery 多条件组合过滤
# 条件：类目=3743561，月销量 100-1000，星级 4+，FBA 发货
sorftime api ProductSearch '{"nodeid": "3743561", "MonthSaleVolumeRangeMin":100,"MonthSaleVolumeRangeMax":1000,"StarRangeMin":4,"ShippingType":"FBA", "page": 1}' --domain 1

# Step 3: 对候选产品的核心关键词做延伸词拓展
# 假设 Step 2 筛出的产品标题含 "power bank"
sorftime api KeywordExtends '{"keyword": "power bank", "pageIndex": 1, "pageSize": 50}' --domain 1

# Step 4: 查看候选 ASIN 的近期评论 sentiment
# 先采集最近评论（mode=1=most recent，star=11=积极评论）
sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "mode": 1, "star": "11", "onlyPurchase": 0, "page": 3}' --domain 1
# 再查消极评论（star=10=1-3星）
sorftime api ProductReviewsCollection '{"asin": "B0CVM8TXHP", "mode": 1, "star": "10", "onlyPurchase": 0, "page": 3}' --domain 1

# Step 5: 读取已采集的评论内容
sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "star": 11, "querystartdt": "2026-03-01"}' --domain 1
sorftime api ProductReviewsQuery '{"asin": "B0CVM8TXHP", "star": 10, "querystartdt": "2026-03-01"}' --domain 1
```

## 配方 2：竞品深挖配方（ProductRequest batch → AsinSalesVolume → ASINRequestKeywordv2 → ProductReviewsCollection）

**场景**：一次性对 5-10 个竞品 ASIN 做全景扫描——基础信息、子体销量历史、反查关键词、评论 sentiment。

**为什么 MCP 做不到**：MCP 的 `ProductRequest` 工具即使支持多 ASIN，也不会自动触发后续的 `AsinSalesVolume`、`ASINRequestKeywordv2`、`ProductReviewsCollection` 四连调；而 CLI 里一条 for 循环就能串完。

```bash
# 定义竞品 ASIN 列表
COMPETITORS="B0CVM8TXHP,B0XXXXXXX,B0YYYYYYY,B0ZZZZZZZZ,B0AAAAAAAA"

# Step 1: 批量查基础信息（最多 10 个 ASIN，1 次请求）
sorftime api ProductRequest '{"asin": "'"$COMPETITORS"'", "trend": 1}' --domain 1

# Step 2: 逐个查子体销量历史（循环，每个 ASIN 1 次请求）
for asin in $(echo $COMPETITORS | tr ',' ' '); do
  sorftime api AsinSalesVolume '{"asin": "'"$asin"'", "queryDate": "2026-01-01", "queryEndDate": "2026-03-31"}' --domain 1
done

# Step 3: 逐个反查关键词（循环，每个 ASIN 1 次请求）
for asin in $(echo $COMPETITORS | tr ',' ' '); do
  sorftime api ASINRequestKeywordv2 '{"asin": "'"$asin"'", "pageSize": 100}' --domain 1
done

# Step 4: 逐个采集最近评论（循环，每个 ASIN 消耗积分）
for asin in $(echo $COMPETITORS | tr ',' ' '); do
  sorftime api ProductReviewsCollection '{"asin": "'"$asin"'", "mode": 1, "star": "1,2,3,4,5", "onlyPurchase": 0, "page": 5}' --domain 1
done

# Step 5: 等 5-10 分钟后，批量查询评论采集状态
for asin in $(echo $COMPETITORS | tr ',' ' '); do
  sorftime api ProductReviewsCollectionStatusQuery '{"asin": "'"$asin"'", "update": 24}' --domain 1
done

# Step 6: 读取已完成采集的评论内容
for asin in $(echo $COMPETITORS | tr ',' ' '); do
  sorftime api ProductReviewsQuery '{"asin": "'"$asin"'", "querystartdt": "2026-04-01"}' --domain 1
done
```

**输出归档建议**：

```bash
OUTDIR="./competitor-$(date +%Y%m%d)"
mkdir -p "$OUTDIR"
# 每个步骤的结果重定向到 $OUTDIR/ 下的文件
# 最后用 jq 统一提取 price / sales / ratings / brand 做对比表
```

**批量提取对比字段**：

```bash
# 从 ProductRequest 结果中提取关键指标
jq '{asin: .data.asin, title: .data.title, price: .data.price, monthlySales: .data.monthlySales, ratings: .data.ratings, brand: .data.brand}' base.json

# 从 AsinSalesVolume 中提取最新月销量
jq '.data | last | {date: .[0], sales: .[1]}' sales.json

# 从 ASINRequestKeywordv2 中提取 Top 10 关键词
jq '.data[:10] | map({keyword: .keyword, share: .ShowShare})' keywords.json
```

**CLI 优势**：`for` 循环 + 变量替换是 shell 原生能力，不需要等 MCP server 暴露一个"竞品深挖"的复合工具；ASIN 列表、时间范围、page 数全部可参数化。

---

## 配方 3：监控部署配方（KeywordBatchSubscription + period config + schedule detail extraction）

**场景**：给 3 个核心关键词注册排名监控，限定工作时段，然后验证部署结果并提取一次监控详情。

**为什么 MCP 做不到**：MCP 的监控工具通常只封装"注册"或"查询"单动作，不会把"注册 → 查任务列表 → 查批次 → 提取详情"连成一条可复现的部署流水线。

```bash
# Step 1: 注册 3 个关键词的监控任务
# 条件：PC 浏览器模式，纽约邮编，监控前 3 页
# 时段：周一至周五，9-12 点和 13-16 点（时段 3、4），每个时段执行 1 次（频率 1）
sorftime api KeywordBatchSubscription '{"keyword": ["power bank", "portable charger", "external battery"], "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|3,4|1"}' --domain 1
# 返回示例：["power bank:12345", "portable charger:12346", ...]

# Step 2: 查询全部有效监控任务，确认注册成功
sorftime api KeywordTasks '{"pageIndex": 1, "pageSize": 50}' --domain 1

# Step 3: 查询某个任务的全部执行批次（用 Step 1 返回的 taskId）
TASK_ID=12345
sorftime api KeywordBatchScheduleList '{"TaskId": '"$TASK_ID"'}' --domain 1
# 返回示例：["202604270930:batch001:1:202604270935", ...]

# Step 4: 提取最近一次批次的详细数据（用 Step 3 返回的 ScheduelId）
SCHEDULE_ID=batch001
sorftime api KeywordBatchScheduleDetail '{"ScheduelId": "'"$SCHEDULE_ID"'"}' --domain 1
# 返回：该次监控前 3 页所有 ASIN 的曝光类型、排名、价格、卖家等字段

# Step 5（可选）：修改任务设置，比如改为每小时监控
sorftime api KeywordBatchTaskUpdate '{"taskId": '"$TASK_ID"', "update": 0, "mode": 0, "area": "10041", "page": 3, "period": "1,2,3,4,5|3,4|2"}' --domain 1
```

**period 表达式速查**：

```
格式：<每周哪几日>|<每天哪些时段>|<监控频率>

每周哪几日：1-7（逗号分割，1=周一，7=周日）
每天哪些时段：1-6（每个时段 4 小时，北京时区）
  1: 1-4点,  2: 5-8点,  3: 9-12点
  4: 13-16点, 5: 17-20点, 6: 21-0点
监控频率：
  1:  时段内任意时刻一次
  2:  时段内每小时 1 次
  3:  时段内每 2 小时 1 次
  11-14: 时段内第 1-4 个时间刻度执行
  31: 时段内单数小时执行，共 2 次
  32: 时段内双数小时执行，共 2 次
```

**CLI 优势**：`TASK_ID` 和 `SCHEDULE_ID` 可以写进环境变量或 `.env` 文件，整个流程可以封装成一个 `deploy-monitor.sh` 脚本，一键部署 + 验证。MCP 没有这种"把上一步输出作为下一步输入"的脚本化能力。

---

## 配方 4：趋势追踪配方（CategoryTrend trendIndex 0-39 → time series stitching）

**场景**：对同一个 nodeId，连续查询 40 个 trendIndex，把近 2 年的销量、垄断、新品占比等时间序列拼成一张完整的市场趋势表。

**为什么 MCP 做不到**：MCP 不会提供一个"查询全部 40 个趋势指标"的工具，因为那会消耗 80 次 request（40 × 2），远超单次调用的合理范围；而 CLI 可以用循环逐个拉取，再本地拼接。

```bash
NODE_ID="3743561"

# Step 1: 定义需要追踪的核心指标索引
# 0=销量, 3=平均售价, 6=1个月新品占比, 28=前3 Listing垄断, 34=前10品牌垄断
INDICES="0 3 6 28 34"

# Step 2: 循环查询，每个指标 2 次 request
for idx in $INDICES; do
  echo "=== trendIndex: $idx ==="
  sorftime api CategoryTrend '{"nodeId": "'"$NODE_ID"'", "trendIndex": '"$idx"'}' --domain 1 > "trend_${idx}.json"
  sleep 0.3  # 控制 QPS，避免 429
done

# Step 3: 本地拼接（用 jq 把多个 JSON 的 data 字段合并）
# 假设每个 trend_${idx}.json 的 data 字段是 [202010,1000,202011,1010,...]
jq -s 'map(.data) | {nodeId: "'"$NODE_ID"'", trends: .}' trend_*.json > "${NODE_ID}_trends.json"

# Step 4: 如需全部 40 个指标，直接循环 0-39
for idx in $(seq 0 39); do
  sorftime api CategoryTrend '{"nodeId": "'"$NODE_ID"'", "trendIndex": '"$idx"'}' --domain 1 > "trend_${idx}.json"
  sleep 0.3
done
```

**关键指标索引速查**：

| 索引 | 含义 | 分析用途 |
|------|------|---------|
| 0 | 销量趋势 | 判断类目整体涨跌 |
| 3 | 平均售价趋势 | 价格带是否下移 |
| 6 | 1个月新品占比 | 新品进入难度 |
| 28 | 前3 Listing垄断 | 头部集中度 |
| 34 | 前10品牌垄断 | 品牌竞争格局 |
| 9 | 亚马逊自营占比 | 自营挤压程度 |
| 12 | 平均单次产品利润 | 利润空间变化 |

**CLI 优势**：这是一个"脚本模式"，不是单个 API call。你可以只选 5 个核心指标快速扫描，也可以拉满 40 个指标做深度分析；中间结果落盘为 `.json`，随时用 `jq` 做二次加工。MCP 的 preset tool 无法提供这种"按需选择指标子集 + 本地持久化 + 离线拼接"的灵活性。

---

## 配方 5：跨平台对比配方（Amazon ProductRequest + Shopee CategoryRequest + Walmart ProductRequest）

**场景**：同一产品概念（如 "water bottle"）在 Amazon、Shopee、Walmart 三个平台的表现对比。

**为什么 MCP 做不到**：MCP server 通常是平台隔离的——`sorftime-agent-amazon`、`sorftime-agent-shopee`、`sorftime-agent-walmart` 是三个独立工具集，没有一个 preset tool 能同时接受 `domain=1`、`domain=201`、`domain=21` 并返回三平台对比结果。CLI 只需改 `--domain` 参数即可任意跨平台编排。

```bash
# ========================================
# Amazon 美国站（domain=1）
# ========================================
# 先查类目 Best Seller，拿到 ASIN 列表
sorftime api CategoryRequest '{"nodeId": "3743561"}' --domain 1

# 查具体产品详情（ASIN 来自上一步输出）
sorftime api ProductRequest '{"asin": "B0CVM8TXHP", "trend": 1}' --domain 1

# 反查关键词
sorftime api ASINRequestKeywordv2 '{"asin": "B0CVM8TXHP", "pageSize": 50}' --domain 1

# ========================================
# Shopee 越南站（domain=201）
# ========================================
# Shopee 用 productId 而非 ASIN；CategoryRequest 返回 productId
sorftime api CategoryRequest '{"nodeId": "11035813"}' --domain 201

# 查产品详情
sorftime api ProductRequest '{"productId": "21584486278"}' --domain 201

# 查店铺信息（Shopee 专属接口）
sorftime api ShopRequest '{"shopId": "123456"}' --domain 201

# ========================================
# Walmart 美国站（domain=21）
# ========================================
# Walmart 用 nodePath 而非 nodeId
sorftime api CategoryRequest '{"nodePath": "4044_623679_1032619_5842891_9823303"}' --domain 21

# 查产品详情（Walmart 用 productId）
sorftime api ProductRequest '{"productId": "3319869184"}' --domain 21

# 查子体销量历史
sorftime api ProductSalesVolume '{"productId": "3319869184", "queryDate": "2026-01-01", "queryEndDate": "2026-03-31"}' --domain 21

# ========================================
# 三平台 domain 速查
# ========================================
# Amazon US  -> --domain 1
# Shopee VN  -> --domain 201
# Walmart US -> --domain 21
```

**三平台参数差异对照**：

| 维度 | Amazon | Shopee | Walmart |
|------|--------|--------|---------|
| Domain | 1 | 201 | 21 |
| 类目标识 | `nodeId` | `nodeId` | `nodePath` |
| 产品标识 | `asin` | `productId` | `productId` |
| 店铺标识 | 无（sellerName/sellerId） | `shopId` | 无（seller 字段） |
| 销量字段 | `monthlySales` | `salesCount` | `listingSalesVolumeOfMonth` |
| 子体销量接口 | `AsinSalesVolume` | 无 | `ProductSalesVolume` |
| 反查关键词 | `ASINRequestKeywordv2` | 无 | `ProductRequestKeyword` |
| 店铺查询 | 无 | `ShopRequest` | 无 |

**批量跨平台采集脚本**：

```bash
#!/bin/bash
# cross-platform.sh — 三平台同类产品批量采集
AMZ_NODE="3743561"
SHOPEE_NODE="11035813"
WALMART_PATH="4044_623679_1032619_5842891_9823303"
OUTDIR="./cross-platform-$(date +%Y%m%d)"
mkdir -p "$OUTDIR"

sorftime api CategoryRequest '{"nodeId": "'"$AMZ_NODE"'"}' --domain 1 > "$OUTDIR/amz.json"
sorftime api CategoryRequest '{"nodeId": "'"$SHOPEE_NODE"'"}' --domain 201 > "$OUTDIR/shopee.json"
sorftime api CategoryRequest '{"nodePath": "'"$WALMART_PATH"'"}' --domain 21 > "$OUTDIR/walmart.json"

# 统一提取：title, price, sales, ratings, brand
jq '{platform:"amazon", title:.data[0].title, price:.data[0].price, sales:.data[0].monthlySales, ratings:.data[0].ratings, brand:.data[0].brand}' "$OUTDIR/amz.json" > "$OUTDIR/amz_summary.json"
jq '{platform:"shopee", title:.data.products[0].title, price:.data.products[0].price, sales:.data.products[0].salesCount, ratings:.data.products[0].ratings, brand:.data.products[0].brand}' "$OUTDIR/shopee.json" > "$OUTDIR/shopee_summary.json"
jq '{platform:"walmart", title:.data[0].title, price:.data[0].price, sales:.data[0].listingSalesVolumeOfMonth, ratings:.data[0].ratings, brand:.data[0].brand}' "$OUTDIR/walmart.json" > "$OUTDIR/walmart_summary.json"

jq -s '.' "$OUTDIR"/*_summary.json > "$OUTDIR/comparison.json"
echo "对比结果: $OUTDIR/comparison.json"
```

**CLI 优势**：
- **参数差异透明**：Amazon 用 `nodeId` + `asin`，Shopee 用 `nodeId` + `productId` + `shopId`，Walmart 用 `nodePath` + `productId`——CLI 让你直接面对这些差异，精确控制每个平台的入参；MCP 的 preset tool 会隐藏这些细节，导致跨平台时参数对不上。
- **任意组合**：你可以只对比 Amazon + Walmart，也可以把 Shopee 的 8 个站点全部扫一遍；MCP 的 preset tool 不会为你预先封装这种"任意 N 平台 M 接口"的组合。
- **统一输出格式**：三平台结果都是 JSON，可以用同一个 `jq` 脚本做字段提取和对比报表。

---

## 总结：CLI vs MCP 灵活性对照

| 能力 | sorftime-cli | sorftime-agent-x（MCP） |
|------|-------------|------------------------|
| 单接口调用 | ✅ | ✅ |
| 多接口自由组合 | ✅ 任意 endpoint 拼接 | ❌ 只能调预设工具 |
| 上一接口输出 → 下一接口输入 | ✅ shell 变量 / jq / 文件 | ❌ 无管道能力 |
| 循环 / 批量 / 条件分支 | ✅ for / while / if | ❌ 无脚本能力 |
| 跨平台（Amazon/Shopee/Walmart）编排 | ✅ 改 `--domain` 即可 | ❌ 平台隔离 |
| 中间结果落盘 / 二次加工 | ✅ 本地 JSON + jq | ❌ 只能内存流转 |
| 自定义时间范围 / 分页 / 过滤 | ✅ 全参数暴露 | ⚠️ 部分参数被工具封装隐藏 |

**一句话**：MCP 适合"问一句、答一句"的交互式查询；CLI 适合"写脚本、跑流水线、出报表"的工程化工作流。两者互补，但复杂分析场景 CLI 不可替代。
