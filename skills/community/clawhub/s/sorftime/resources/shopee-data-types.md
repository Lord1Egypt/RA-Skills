# Shopee 数据类型定义

> 所有 Shopee 接口的 `data` 字段类型定义。各接口文档仅说明 `data` 字段的类型，具体字段见本文档。
> 所有接口统一外层返回结构：`requestLeft`、`requestConsumed`、`requestCount`、`code`、`message`、`data`。

---

## CategoryTreeObject

类目树节点。CategoryTree 接口返回此对象的数组。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 类目ID |
| parentId | Integer | 父级类目ID，为0表示第一级 |
| nodeid | String | 类目nodeid（用于后续查询） |
| name | String | 类目名称 |
| cnName | String | 类目中文名称 |
| url | String | 类目URL地址 |

---

## CategoryObject

类目市场对象。CategoryRequest 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| Subcategory | Boolean | 是否为细分类目 |
| products | [ProductSummeryObject](#productsummeryobject) Array | 类目下产品列表 |

---

## ProductSummeryObject

产品摘要对象。ProductRequest 接口返回的 `data` 字段。CategoryRequest 接口返回的 `products` 数组元素。

| 字段 | 类型 | 说明 |
|------|------|------|
| title | String | 产品名称 |
| photo | String Array | 产品主图URL数组 |
| productId | String | 产品ID |
| updateTime | String | 数据更新时间 |
| salesCount | Integer | 近30日销量 |
| salesAmount | Number | 近30日销售额 |
| salesCalcTime | String | 计算产品销量的时间 |
| saleIsCorrection | Boolean | 是否做了销量校准（true表示已校准） |
| hisSalesCount | Integer | 累计销量 |
| shopId | String | 卖家店铺ID |
| shopName | String | 卖家店铺名称 |
| shopLocation | String | 店铺来源城市 |
| shopLocType | String | 店铺类型：本土店或跨境店 |
| shopType | String | 店铺类型：普通店、优选店、旗舰店 |
| price | Number | 产品销售价 |
| listPrice | Number | 划线价 |
| discount | Number | 折扣率（如46.00表示降价46%） |
| brand | String | 产品品牌 |
| brandId | String | 品牌ID |
| ratings | Number | 评分星级（如4.8） |
| ratingCount | Integer | 评论数量 |
| saleTime | String | 产品上线时间 |
| couponStr | String | 优惠券信息 |
| ratingDetail | String | 星级组成JSON数组：[1星数量,2星数量,3星数量,4星数量,5星数量] |
| bsrCategory | String | 所属细分类目JSON数组：[["类目名称","NodeId","排名"],...] |

---

## ProductTrendObject

产品历史趋势对象。ProductTrend 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | String | 产品ID |
| saleCountTrend | String | 按日统计的近30日销量趋势数组 |
| saleTotalCountTrend | String | 累计销量趋势数组 |
| priceTrend | String | 价格趋势数组（仅在价格变化时记录） |
| reviewCountTrend | String | 按月统计评论数量趋势数组 |
| starTrend | String | 按月统计星级趋势数组 |

**趋势数据格式说明**：

- 数组格式：`["20231001","775","20231002","765",...]`
- 偶数下标为日期/月份，奇数下标为对应数据值
- 价格趋势：仅在价格变化时记录，最后一个数据为截止日期
  - 例如：`["20241001","19.99","20241102","18.99","20250402","18.99"]`
- 星级趋势：450表示4.5星

---

## ShopObject

店铺对象。ShopRequest 接口返回的 `data` 字段。

| 字段 | 类型 | 说明 |
|------|------|------|
| shopId | String | 店铺ID |
| shopName | String | 店铺名称 |
| shopLocation | String | 店铺来源地 |
| shopImage | String | 店铺主图链接 |
| shopType | String | 店铺类型：普通店、优选店、旗舰店 |
| saleDate | String | 开店日期（例：2020-09-20） |
| shopStar | Integer | 店铺星级（例：4.50表示4.5星） |
| shopRating | Integer Array | 店铺评论数JSON数组：[好评价数,中性评价数,差评价数] |
| top500ProductCount | Integer | 店铺卖进top500的产品数 |
| top500SalesCount | Integer | 店铺卖进top500产品月销量 |
| top500salesAmount | Number | 店铺卖进top500产品月销额 |
| top500Products | String | 店铺卖进top500产品ID清单JSON数组（最多500个） |

---
