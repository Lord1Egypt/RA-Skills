# Amazon 数据类型定义

> 所有 Amazon 接口的 `data` 字段类型定义。各接口文档仅说明 `data` 字段的类型，具体字段见本文档。
> 所有接口统一外层返回结构：`requestLeft`、`requestConsumed`、`requestCount`、`code`、`message`、`data`。

---

## CategoryTreeObject

类目树节点。CategoryTree 接口返回此对象的数组。

| 字段 | 类型 | 说明 |
|------|------|------|
| Id | Integer | 类目ID |
| ParentId | Integer | 父类目ID，0=一级类目 |
| NodeId | String | 平台原生类目ID（用于后续查询） |
| Name | String | 类目英文名称 |
| CNName | String | 类目中文名称 |
| URL | String | 类目对应平台页面地址 |

---

## CategoryObject

类目Best Seller对象。CategoryRequest 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| products | [ProductSummeryObject](#productsummeryobject) Array | Best Seller榜单产品列表 |

---

## ProductListObject

产品列表对象。CategoryProducts、ProductSearch 等接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| page | Integer | 当前页码 |
| pageCount | Integer | 共有多少页 |
| products | [ProductSummeryObject](#productsummeryobject) Array | 产品列表 |

---

## ProductSummeryObject

产品摘要对象。所有返回产品列表的接口均使用此结构。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | String | 产品ASIN |
| parentAsin | String / null | 父ASIN，无子体时为null |
| title | String | 产品名称 |
| brand | String | 品牌 |
| price | Integer | 销售价（未扣除coupon），当地货币最小单位 |
| listPrice | Integer | 原价（划线价），当地货币最小单位 |
| coupon | Integer | >0为固定金额抵扣，<0为百分比折扣（如-10=10%），当地货币最小单位 |
| salesPrice | Integer | 实际销售价（扣除coupon后），当地货币最小单位 |
| ratings | Number | 星级 |
| ratingsCount | Integer | 评论数 |
| listingSalesVolumeOfMonth | Integer | 预估月销量，-1表示无法预估 |
| listingSalesVolumeOfDaily | Integer | 日销量，-1表示无法预估 |
| listingSalesOfMonth | Integer | 预估月销售额，当地货币最小单位 |
| onlineDate | String | 上架日期，格式 yyyy-MM-dd |
| onlineDays | Integer | 上架天数 |
| variationASINCount | Integer | 子体数量 |
| sellerCount | Integer | 卖家数量 |
| isFBA | Boolean | buybox卖家是否使用FBA |
| hasVideo | Boolean | 是否有主图视频 |
| APlus | Boolean | 是否有A+页面 |
| hasBrandStore | Boolean | 是否有品牌旗舰店 |
| photo | String Array | 主图URL列表 |
| EBCPhoto | String Array | A+页面图片 |
| buyboxSeller | String | buybox卖家名称 |
| buyboxSellerId | String | buybox卖家ID |
| buyboxSellerAddress | String | buybox卖家国籍（国家二字码，如CN/US/GB） |
| category | String Array | 所属大类：[名称, nodeId] |
| bsrCategory | String Array | 所属细分类目：[["名称","NodeId","排名"]] |
| rank | Integer | 大类排名 |
| size | String Array | 外包装尺寸：[最长边, 第二长边, 最短边] |
| weight | Integer | 重量（单位：g） |
| profit | Integer | 毛利，当地货币最小单位 |
| profitRate | Number | 毛利率（百分比，如25.83表示25.83%） |
| fbaFee | Integer | FBA费用，当地货币最小单位 |
| fbaDetetail | String Array | FBA费用组成：[配送费, "1-9月:仓储费", "10-12月:仓储费"] |
| platformFee | Integer | 平台佣金，当地货币最小单位 |
| shipCost | Integer | FBM配送费，当地货币最小单位 |
| DealType | String | 促销标签 |
| StoreName | String | 店铺名称 |
| variationASIN | String Array | 子体ASIN列表 |
| refreshAsin | String | 刷新跳转目标ASIN，无跳转时为空 |
| ExtraSavings | Object Array | 关联促销内容：[{"Asin":"...", "Text":"..."}] |

---

## ProductObject

产品详情对象。ProductRequest 接口返回的 `data` 字段，在 [ProductSummeryObject](#productsummeryobject) 基础上增加以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| Description | String | 五点描述 |
| ProductBadge | String Array | 产品标志，如 ["Amazon Choice", "Best Seller", "New Release"] |
| updateDate | String | 当前ASIN更新时间 |
| AsinSalesCount | Integer | 亚马逊公布的ASIN月销量，近7个自然日有公布则返回最新值，否则为0 |
| OffSale | Integer | 是否不可售，1=不可售，0=可售 |
| attribute | String Array | 子体属性：[["子体asin","属性名","属性值",...]] |
| shipsFrom | String | 发货方名称 |
| feature | String Array | 产品特性及星级：["FromAsin","Easy to clean:4.6","Easy to use:4.4"] |
| productInfo | String Array | Product Information描述：["Manufacturer","Amazon Basics","Country of Origin","China"] |
| property | String Array | 属性列表：["FromAsin","Brand:Toshiba","Color:Black"] |
| oneStartRatings | Number | 1星ratings占比（%） |
| twoStartRatings | Number | 2星ratings占比（%） |
| threeStartRatings | Number | 3星ratings占比（%） |
| fourStartRatings | Number | 4星ratings占比（%） |
| fiveStartRatings | Number | 5星ratings占比（%） |
| bsrCategory | String Array | 细分类目增加"最后一次上榜时间"：[["名称","NodeId","排名","yyyyMMdd"]] |

**趋势字段**（当 `trend != 2` 时返回）：

| 字段 | 类型 | 说明 |
|------|------|------|
| listingSalesVolumeOfDailyTrend | Integer Array | 日销量趋势：[yyyyMMdd,销量,...]，-1表示无预计销量 |
| listingSalesOfDailyTrend | Integer Array | 日销售额趋势：[yyyyMMdd,销售额,...]，当地货币最小单位 |
| listingSalesVolumeOfMonthTrend | Integer Array | 月销量趋势：[yyyyMM,销量,...] |
| listingSalesOfMonthTrend | Integer Array | 月销售额趋势：[yyyyMM,销售额,...]，当地货币最小单位 |
| RankTrend | String Array | 大类排名变化：["日期","大类NodeId:大类排名",...] |
| BsrRankTrend | String | 小类排名历史JSON：[{"nodeid":"xxx","rank":["日期","排名",...]}] |
| DealTrend | Integer Array | Deal状态：[yyyyMMdd,1/0,...]，1=有Deal，0=无Deal |
| priceTrend | Integer Array | 销售价格趋势：[yyyyMMdd,价格,...]，当地货币最小单位 |
| listPriceTrend | Integer Array | 原价（划线价）趋势：[yyyyMMdd,价格,...] |
| couponTrend | Integer Array | coupon趋势：[yyyyMMdd,值,...]，>0为金额，<0为百分比，-1为无coupon |

---

## AsinSalesVolumeObject

ASIN官方公布子体销量。AsinSalesVolume 接口返回的 `data` 字段。

二维 String/Integer 数组，每行格式：`[日期, 销量, 销量类型]`

| 列 | 类型 | 说明 |
|----|------|------|
| [0] | String | 记录日期，格式 yyyy-MM-dd |
| [1] | Integer | 销量记录 |
| [2] | Integer | 1=周销量，2=月销量 |

---

## ProductVariationHistoryObject

产品子体变化历史。ProductVariationHistory 接口返回的 `data` 字段。

二维 String 数组，每行格式：`[记录时间, ParentASIN, 子体ASIN1, 子体ASIN2, ...]`

---

## ReviewsObject

产品评论。ProductReviewsQuery 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| reviewsLink | String | 评论详情链接 |
| consumerName | String | 评论人昵称 |
| consumerURL | String | 评论人主页链接 |
| consumerBadge | String Array | 评论人标志，如 ["Top 10 Reviewer"] |
| star | Number | 给予的评分星级 |
| title | String | 评论标题 |
| ReviewedCountry | String | 留评国籍/地区 |
| reviewsDate | String | 评论时间 |
| isVP | Boolean | 是否为 Verified Purchase 评论 |
| asin | String | 评论指向的变体ASIN，无变体时为空 |
| asinProperty | String | 评论指向的变体属性，如 "Color: Black" |
| helpful | Integer | 认为此评论有用的人数 |
| content | String | 评论原文 |
| resource | String | 评论图片URL，多图用 \|\| 分割 |
| videos | String | 评论视频链接 |
| itemIndex | String | 数据序号，如 "156/5000" |

---

## KeywordSummeryObject

关键词摘要对象。KeywordQuery、KeywordExtends、CategoryRequestKeyword 等接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | String | 关键词 |
| keywordCNName | String | 关键词中文名称 |
| Images | String Array | 搜索结果前10个产品图片 |
| ImagesFromAsin | String Array | 图片来源ASIN（顺序与Images一致） |
| update | String | 最新更新ABA排名时间（周词有效，月词为空） |
| rank | Integer | 周搜索排名 |
| Department | String Array | 相关类目nodeid：["17659096011","289937"] |
| searchVolume | Integer | 近30天搜索量 |
| searchVolumeTrend | String Array | 搜索量趋势：[yyyyMM,搜索量,...] |
| searchRankTrend | String | 搜索排名趋势：[yyyyMM,排名,...] |
| ClickOf90D | Integer | 近90日点击量（仅美国站，未公布=-1） |
| SalesVolumeOf90D | Integer | 近90日购买量 |
| wordCount | Integer | 单词数量 |
| searchConversionRateD90 | Number | 近90天搜索转化比（仅美国站） |
| ClickConversionRateD90 | Number | 近90天点击转化比（仅美国站） |
| searchConversionRate | Number | 过去360天搜索转化比（如18.44表示18.44%） |
| ProductCount | Integer | 竞品数量（搜索页亚马逊提示的竞品数） |
| rankChangeOfWeekly | Number | 较上一周排名变化（负数=下降） |
| cpc | Integer | CPC精准竞价，当地货币最小单位 |
| cpcRange | String | CPC竞价范围：最小值,最大值 |
| searchVolumeGrowthRateTrend | Number Array | 近3/6/12个月搜索量复合增长率：[3月,6月,12月] |
| shareClickRate | Number | 前3产品点击份额占比（%） |
| shareConversionRate | Number | 前3产品转化份额占比（%） |
| top3asin | String Array | 点击最多的前3个ASIN：["asin,点击份额,转化份额"] |
| top3Brand | String Array | 点击最高的前3个品牌 |
| top3Category | String Array | 点击最高的前3个类目名称 |
| season | String | 旺季 |

---

## KeywordObject

关键词详情。KeywordRequest 接口返回的 `data` 字段，在 [KeywordSummeryObject](#keywordsummeryobject) 基础上增加以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| salesVolumeOf90d | Integer | 近90天购买量 |
| searchVolumeGrowthTrend | String Array | 未来12个月搜索量增长趋势：[yyyyMM,增幅,...]，9612表示增长96.12% |
| cpcTrend | String Array | CPC精准竞价历史：[yyyyMM,cpc,最小值,最大值,...] |
| searchResultOfFP | String Array | 首页产品数据报告（见下方说明） |
| searchResultOfFPTrend | String Array | 首页产品历史趋势（见下方说明） |
| associatedWithCategory | String Array | 相关联细分类目nodeid |
| associatedWithCategoryDetail | String Array | 相关联细分类目top100数据：[[nodeid,名称,月销量,均价,均评价,...]] |

**searchResultOfFP 数组下标说明**：
0=产品数量，1=自然位数量，2=广告位数量，3=自然位非Top100占比，
4=自然位评价数低于100/300/500占比，5=广告位评价数低于100/300/500占比，
6=无星级数量，7=平均星级，8=平均评价数，
9=coupon数量/占比（如"2/588"），10=被跟卖数量/占比，11=30日最低价数量/占比

**searchResultOfFPTrend 数组格式**：[yyyyMM,平均星级,平均评价数,平均价格,无星级数量,...]

---

## ASINKeywordItemObject

ASIN反查关键词项。ASINRequestKeywordv2 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| keyword | [KeywordSummeryObject](#keywordsummeryobject) | 关键词详情 |
| ShowType | String | 曝光形式 |
| ShowShare | Number | 此词在该ASIN反查关键词中贡献的流量占比 |
| PositionType | String Array | 曝光位置形式，如 ["自然流量","平台推荐"] |
| SearchPosition | String | 自然曝光位 |
| searchPositionDate | String | 最近自然曝光时间，格式 yyyy-MM-dd HH:mm |
| AdPosition | String | 广告曝光位 |
| AdPositionDate | String | 最近广告曝光时间，格式 yyyy-MM-dd HH:mm |

---

## KeywordProductRankingObject

关键词搜索结果产品排名。KeywordProductRanking、ASINKeywordRanking 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| page | String | 分页信息，如 "1/100" |
| records | Array | 排名记录列表 |

**records 数组元素**：

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | String | 产品ASIN |
| keyword | String | 关键词 |
| page | String | 曝光在第几页 |
| position | String | 页面位置，如 "1/68" |
| positionType | String | 0=自然曝光，1=广告曝光 |
| positionName | String | 0=自然位，1=SP广告，2=品牌广告，3=视频广告 |
| adID | String | 广告组ID，非广告时为空 |
| campaignID | String | 广告活动ID（2025-03月起有效），非广告时为空 |
| recordDate | String | 记录时间，格式 yyyy-MM-dd HH:mm（UTC+8北京时间） |

---

## KeywordSearchResultItem

关键词搜索结果产品趋势项。KeywordSearchResultTrend 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| RecordDate | String | 记录时间，格式 yyyy-MM-dd |
| Top100SalesVolume | Integer | 前3页产品销量前100的月销量之和 |
| Top100Sales | Integer | 前3页产品销量前100的月销售额之和，当地货币最小单位 |
| ProductCount | Integer | 竞品数量（基于搜索结果展示的竞品数） |
| BrandCount | Integer | 前100产品的品牌数量 |
| SellerCount | Integer | 前100产品的卖家数量 |
| AvgStar | Integer | 前100产品的平均星级 |
| AvgPrice | Integer | 前100产品的平均价格，当地货币最小单位 |
| AvgRatings | Integer | 前100产品的平均评价数量 |
| NoRatingProductCount | Integer | 无星级产品数量 |

---

## KeywordTaskObject

关键词监控任务。KeywordTasks 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| taskId | String | 任务Id |
| status | Integer | 1=正常，2=暂停 |
| createDate | String | 任务创建日期 |
| keyword | String | 监控的关键词 |
| mode | Integer | 0=电脑浏览器，1=手机浏览器 |
| area | String | 使用的监控地区邮编 |
| page | Integer | 监控前N页（1,3,5,7） |
| period | String | 监控频率表达式 |

---

## KeywordBatchScheduleObject

关键词监控执行批次。KeywordBatchScheduleList 接口返回的 `data` 数组元素。

格式字符串：`<执行时间yyyyMMddHHmm>:<批次Id>:<状态>:<完成时间>`

| 段 | 说明 |
|----|------|
| 执行时间 | 格式 yyyyMMddHHmm |
| 批次Id | 批次唯一标识 |
| 状态 | 0=执行中，1=执行完成 |
| 完成时间 | 完成时的yyyyMMddHHmm，未完成时为"--" |

---

## KeywordBatchScheduleDetailObject

关键词监控批次详细数据。KeywordBatchScheduleDetail 接口返回的 `data` 数组元素。

CSV格式字符串，每行包含以下字段：

| 序号 | 字段 | 说明 |
|------|------|------|
| 1 | asin | 产品ASIN |
| 2 | 主图链接 | 主图URL |
| 3 | 产品标题 | 产品标题 |
| 4 | 曝光类型 | 0=自然曝光，1=广告曝光 |
| 5 | 标志 | AC/BS/Deal/Lowest |
| 6 | 曝光排名 | 第x页，第y/z位 |
| 7 | 曝光位置 | 品牌广告/视频广告/... |
| 8 | coupon | coupon信息 |
| 9 | 星级 | 星级 |
| 10 | 评价数量 | 评价数 |
| 11 | 销售价 | 当地货币最小单位 |
| 12 | 跟卖数量 | 跟卖数 |
| 13 | sellerName | 卖家名称（来自Sorftime库） |
| 14 | sellerId | 卖家ID（来自Sorftime库） |
| 15 | shipsFrom | 发货方（来自Sorftime库） |
| 16 | 配送费 | 配送费 |
| 17 | 品牌 | 品牌名 |
| 18 | 变体数 | 子体数（来自Sorftime库） |
| 19 | prime标志 | Prime标志 |
| 20 | scheduleId | 批次任务Id |

---

## BestSellerListItemObject

榜单监控数据项。BestSellerListDataCollect 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | String | 产品ASIN |
| parentAsin | String / null | 父ASIN，无子体时为null |
| title | String | 产品名称 |
| brand | String | 品牌 |
| price | Integer | 销售价，当地货币最小单位 |
| onlineDate | String | 上架日期，格式 yyyy-MM-dd |
| ratings | Number | 星级 |
| ratingsCount | Integer | 评论数 |
| listingSalesVolumeOfMonth | Integer | 预估月销量，-1表示无法预估 |
| listingSalesOfMonth | Integer | 预估月销售额，当地货币最小单位 |
| photo | String Array | 主图URL列表 |
| bsrCategory | String Array | 所属细分类目：[["名称","NodeId","排名"]] |
| Category | String Array | 所属大类：[["名称","NodeId","排名"]] |

---

## ProductSellerTaskObject

跟卖监控任务。ProductSellerTasks 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| taskId | String | 任务Id |
| status | Integer | 1=正常，2=暂停 |
| createDate | String | 任务创建日期 |
| asin | String | 监控的ASIN |
| period | String | 监控频率表达式 |

---

## ProductSellerScheduleDetailObject

跟卖监控执行结果。ProductSellerTaskScheduleDetail 接口返回的 `data` 数组元素。

CSV格式字符串：`<采集时间>,<asin>,<卖家名称>,<卖家ID>,<是否buybox>,<发货方式>,<类型>,<售价>,<库存>,<是否限购>`

| 序号 | 字段 | 说明 |
|------|------|------|
| 1 | 采集时间 | 采集时间 |
| 2 | asin | 产品ASIN |
| 3 | 卖家名称 | 卖家名称 |
| 4 | 卖家ID | 卖家SellerId |
| 5 | 是否buybox | 1=是，0=否 |
| 6 | 发货方式 | FBA/FBM |
| 7 | 类型 | New/Used等 |
| 8 | 售价 | 当地货币最小单位 |
| 9 | 库存 | 启用checkstock时返回库存数，否则返回-1 |
| 10 | 是否限购 | 1=限购，0=不限 |

---

## SimilarProductObject

图搜相似产品。SimilarProductRealtimeRequestCollection 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | String | 产品ASIN |
| brand | String | 品牌名 |
| star | Number | 星级 |
| ratings | Integer | 评论数 |
| price | Integer | 价格，当地货币最小单位 |
| listPrice | Integer | 划线价，当地货币最小单位 |

---

## CoinQueryObject

积分余额查询。CoinQuery 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| coin | Integer | 当前积分余额 |

---

## RequestStreamObject

请求流水查询。RequestStream 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| purchase | String Array (二维) | 购买记录：每行 `[日期, 购买金额, 剩余请求数, 过期时间]` |
| consume | String Array (二维) | 消耗记录：每行 `[月份, 消耗请求数]` |

---

## AsinSummaryObject

ASIN订阅数据摘要。ASINSubscriptionCollection 接口返回的 `data` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | String | 产品ASIN |
| parentAsin | String | 父ASIN |
| title | String | 产品名称 |
| brand | String | 品牌 |
| price | Integer | 销售价，当地货币最小单位 |
| ratings | Number | 星级 |
| ratingsCount | Integer | 评论数 |
| listingSalesVolumeOfMonth | Integer | 预估月销量 |
| photo | String Array | 主图URL列表 |
| bsrCategory | String Array | 所属细分类目 |
| category | String Array | 所属大类 |

---
