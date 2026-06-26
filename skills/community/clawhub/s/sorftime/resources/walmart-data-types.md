# Walmart 数据类型定义

> 所有 Walmart 接口的 `data` 字段类型定义。各接口文档仅说明 `data` 字段的类型，具体字段见本文档。
> 所有接口统一外层返回结构：`requestLeft`、`requestConsumed`、`requestCount`、`code`、`message`、`data`。

---

## CategoryTreeObject

类目树节点。CategoryTree 接口返回此对象的数组。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 类目ID |
| parentId | Integer | 父级类目ID，为0表示第一级 |
| nodeid | String | 类目nodeid |
| name | String | 类目名称 |
| cnName | String | 类目中文名称 |
| url | String | 类目URL地址 |

---

## ProductSummeryObject

产品摘要对象。CategoryRequest、ProductRequest、KeywordSearchResults、ProductSearchFromName 接口返回的 `data` 字段或其数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| title | String | 产品名称 |
| photo | String Array | 产品主图URL数组 |
| listingSalesVolumeOfMonth | Integer | 链接预估月销量（不区分子体），评估产品销量时建议使用此值 |
| listingSalesOfMonth | Integer | 链接预估月销售额，单位为当地货币最小单位（如美国站为美分） |
| productId | String | 产品ID |
| parentProductId | String | 父级产品ID |
| price | Integer | 产品销售价，单位为当地货币最小单位（如1999表示$19.99） |
| brand | String | 产品品牌 |
| seller | String | 采集时的卖家 |
| shipedby | String | 采集时的发货方式 |
| wfsFee | Integer | 如果物流方式为FBA，此产品的FBA费用，单位为当地货币最小单位 |
| attribute | String Array | 产品属性：["属性1","值1","属性2","值2",...] |
| firstReviewsDate | String | 首个评论日期（yyyy-MM-dd） |
| reviewsCount | Integer | 评论数量 |
| ratings | Number | 评分星级（如4.8） |
| nodePath | String Array | 产品所属类目节点，格式：["类目节点名称","类目节点","排名时间","排名",...] |
| label | String Array | 产品标志（如pickup、savewith、bestsell等） |
| popularPick | Integer | Popular Pick标志，存在时为1 |
| clearance | Integer | Clearance标志，存在时为1 |
| reducedPrice | Integer | Reduced Price标志，存在时为1 |
| rollback | Integer | Rollback标志，存在时为1 |
| flashDeal | Integer | Flash Deal标志，存在时为1 |
| size | String Array | 外包装尺寸：["最长边","第二长边","最短边"]，单位cm |
| weight | Integer | 产品重量，单位g |
| variants | String Array | 子体信息JSON数组，每项包含 VariantId、Url、Property、PriceUpdate、DetailUpdate |
| numberOfStar | String Array | 各星级评论数量：["星级","评论数","星级","评论数",...] |

---

## ProductTrendObject

产品历史趋势对象。ProductTrendRequest 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | String | 产品ID |
| listingSalesVolumeOfMonth | Integer | 链接预估月销量 |
| listingSalesOfMonth | Integer | 链接预估月销售额（当地货币最小单位） |
| listingSalesVolumeOfMonthTrend | String Array | 月销量历史趋势数组，偶数下标为日期，奇数下标为销量 |
| listingSalesOfMonthTrend | String Array | 月销额历史趋势数组（当地货币最小单位） |
| priceTrend | String Array | 价格趋势数组（当地货币最小单位） |
| reviewsTrend | String Array | 评论数量趋势数组 |
| starTrend | String Array | 星级趋势数组（450表示4.5星） |
| rankTrend | String[][] | 各类目中的排名趋势，每行格式：["类目节点名称","类目节点","日期","排名","日期","排名",...] |

---

## ProductKeywordItemObject

产品反查关键词对象。ProductRequestKeyword 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| ShowShare | Number | 在此产品的反查关键词中，此词贡献的流量占比 |
| recentlyPosition | String | 最近一次曝光位，格式："1,2/18"表示第1页第2位，共18个位置 |
| organicPosition | String | 最近一次自然曝光位 |
| adPosition | String | 最近一次广告曝光位 |
| keyword | [KeywordSummeryObject](#keywordsummeryobject) | 关键词详情 |

---

## KeywordSummeryObject

关键词摘要对象。KeywordQuery、KeywordSearchResults、KeywordRequest、KeywordSearchFromName、KeywordExtends 接口返回的 `data` 字段或其数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | String | 关键词 |
| keywordCNName | String | 关键词中文名称 |
| images | String Array | 某次搜索结果前10个产品图片，仅用以快速识别关键词 |
| update | String | 该词最新更新时间 |
| rank | Integer | 周搜索排名 |
| searchVolume | Integer | 近30天搜索量 |
| productCount | Integer | 竞品数量，关键词搜索页沃尔玛提示的竞品数量 |
| searchFirstPageAvgPrice | Integer | 首页自然位产品平均价格（当地货币最小单位，如1999表示$19.99） |
| searchFirstPageAvgReviews | Number | 首页自然位产品平均评论数 |
| searchFirstPageAvgStar | Number | 首页自然位产品平均星级（如4.5） |

---

## KeywordQueryPatternObject

关键词查询模式对象。KeywordQuery 接口的 `pattern` 参数。

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | String | 查询的关键词 |
| rankCondition | String Array | 周排名筛选条件：[最小值,最大值]，如["1","5000"] |
| searchVolumeCondition | String Array | 近30日搜索量筛选条件：[最小值,最大值]，如["10000"] |

---

## ProductListItemObject

产品列表项对象。ProductListObject 中的 products 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| title | String | 产品名称 |
| photo | String | 产品主图URL（JSON Array格式） |
| listingSalesVolumeOfMonth | Integer | 链接预估月销量（不区分子体） |
| listingSalesOfMonth | Integer | 链接预估月销售额（当地货币最小单位） |
| productId | String | 产品ID |
| parentProductId | String | 父级产品ID |
| price | Integer | 产品销售价（当地货币最小单位） |
| brand | String | 产品品牌 |
| seller | String | 采集时的卖家 |
| reviewsCount | Integer | 评论数量 |
| ratings | String | 评分星级（如4.8） |
| nodePath | String Array | 产品所属类目节点 |

---

## ProductListObject

分页产品列表对象。

| 字段 | 类型 | 说明 |
|------|------|------|
| page | Integer | 当前页码 |
| pageCount | Integer | 共有多少页 |
| products | String | 产品列表，JSON Array 格式，元素为 [ProductListItemObject](#productlistitemobject) |
