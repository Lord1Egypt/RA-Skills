# 聚合接口完整参考

> 所有请求头：`X-API-Key: $XHS_API_KEY`
> 所有响应都包含通用包装字段（见末尾）

---

## A — 获取可分析维度

```
GET /api/v1/aggregate/data-index
```

无请求体。

**响应关键字段：**

```json
{
  "categories": [
    { "name": "美妆", "code": "cat_001", "keywordCount": 32 }
  ],
  "keywords": ["黑头", "防晒霜", "..."]
}
```

**用途：** 每次分析前必须先调用，获取系统支持的类目/关键词列表，再将用户输入映射到具体维度。

---

## B — 热门笔记清单

```
POST /api/v1/aggregate/notes/discover
```

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | string | ✅ | 用户输入（类目名或关键词，如"美妆"、"黑头"） |
| `timeRange` | string | ❌ | 时间范围天数：`"7"` 或 `"30"`，默认 `"30"` |
| `minEngagement` | number | ❌ | 最低互动量门槛，默认0 |
| `noteType` | string | ❌ | `"image"`（图文）/ `"video"`（视频），不填=全部 |
| `isCommercial` | boolean | ❌ | `true`=仅商业投备 / `false`=仅自然内容 / 不填=全部 |
| `limit` | number | ❌ | 最多返回条数，默认20，上限50 |

**响应 `data` 字段（数组）：**

| 字段 | 说明 |
|------|------|
| `noteId` | 笔记ID |
| `title` | 标题 |
| `author` | 作者昵称 |
| `fansCount` / `fansCountLabel` | 作者粉丝数（原始值 / 中文标签如"12万"） |
| `type` | `image` / `video` / `unknown` |
| `engagement` / `engagementLabel` | 互动量（点赞+收藏+评论） |
| `reads` / `readsLabel` | 阅读量 |
| `isCommercial` | 是否商业合作笔记 |
| `promotedProduct` | 推广品牌名（商业笔记才有） |
| `topics` | 话题标签数组 |
| `publishTime` | 发布时间 |

---

## C — 内容格局分析

```
POST /api/v1/aggregate/notes/landscape
```

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | string | ✅ | 类目名或关键词 |
| `timeRange` | string | ❌ | `"7"` 或 `"30"`，默认 `"30"` |
| `minEngagement` | number | ❌ | 纳入分析的笔记互动量门槛 |
| `noteType` | string | ❌ | `"image"` / `"video"` |

**响应 `data` 字段：**

| 字段 | 说明 |
|------|------|
| `scope.totalMatched` | 分析基数（符合条件的笔记数） |
| `scope.filter` | 筛选条件描述 |
| `formatDistribution` | 图文/视频占比及平均互动量 |
| `commercialAnalysis.commercialRatio` | 商业笔记占比 |
| `commercialAnalysis.topProducts` | 推广频次最高的品牌 Top5 |
| `topTopics` | 热门话题 Top10（含热度指数） |
| `engagementTiers` | 互动层级分布（5k-1w / 1w-5w / 5w-20w / 20w+） |
| `marketContext.supplyDemandNote` | 供需判断文字（"供不应求"/"供过于求"等） |
| `brandPresence` | 笔记中出现最多的品牌词 Top5 |
| `contentAttributes` | 爆文标题高频属性词（如"成分党"、"平价"等） |
| `sampleNotes` | 图文/视频各3篇最高互动的代表性笔记 |

---

## D — 活跃博主清单

```
POST /api/v1/aggregate/authors/discover
```

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | string | ✅ | 类目名或关键词 |
| `timeRange` | string | ❌ | `"7"` 或 `"30"`，默认 `"30"` |
| `minNoteCount` | number | ❌ | 最低笔记数过滤，默认0 |
| `limit` | number | ❌ | 最多返回条数，默认20，上限50 |

**响应 `data` 字段：**

| 字段 | 说明 |
|------|------|
| `totalAuthors` | 活跃博主总数 |
| `tierDistribution` | 层级分布（头部/腰部/尾部/普通，含占比） |
| `authors[]` | 博主列表（见下） |
| `risingAuthors[]` | 近30天粉丝增长最快的博主 Top5 |

**`authors[]` 每项字段：**

| 字段 | 说明 |
|------|------|
| `nickname` | 昵称 |
| `fansCount` / `fansCountLabel` | 粉丝数 |
| `tier` | `头部` / `腰部` / `尾部` / `素人` |
| `noteCount` | 笔记数量 |
| `totalEngagement` / `totalEngagementLabel` | 总互动量 |
| `avgEngageRate` | 平均互动率 |
| `picturePrice` / `videoPrice` | 图文/视频报价（有则显示，如"¥3000"） |
| `contentTags` | 内容标签数组 |
| `location` | 所在地 |

---

## E — 单博主深度档案

```
GET /api/v1/aggregate/authors/{authorId}
```

`authorId` 来自接口D响应中博主的ID（通过昵称在D的结果里定位，再用系统内部ID查询）。

**响应字段（无通用包装，直接返回）：**

`basic` — 基本信息：

| 字段 | 说明 |
|------|------|
| `nickname` | 昵称 |
| `gender` / `location` | 性别 / 地区 |
| `fansCount` / `fansCountLabel` | 粉丝数 |
| `fansGrowth30d` / `fansGrowth30dLabel` | 近30天粉丝增量 |
| `contentTags` | 内容标签 |
| `picturePrice` / `videoPrice` | 图文/视频报价 |
| `avgReadNum` / `avgEngageNum` | 均次阅读 / 互动 |
| `engageRate` | 互动率 |

`content` — 内容表现：

| 字段 | 说明 |
|------|------|
| `totalNotes` | 总笔记数 |
| `totalExposure` / `totalReads` / `totalInteractions` | 总曝光 / 总阅读 / 总互动 |
| `topNotes[]` | 历史最高互动笔记 Top5（含标题/互动数/发布时间） |

`fans` — 粉丝画像：

| 字段 | 说明 |
|------|------|
| `ageDistribution` | 年龄分布数组（age + ratio） |
| `genderDistribution` | 性别分布 |
| `interestTopics` | 兴趣标签 |
| `locationDistribution` | 地域分布 |

> `fans` 可能为 null，表示该博主粉丝画像数据暂无。

---

## F — 博主层级 ROI 对比

```
POST /api/v1/aggregate/authors/compare
```

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | string | ✅ | 类目名或关键词（确定行业背景） |
| `timeRange` | string | ❌ | `"7"` 或 `"30"`，默认 `"30"` |

**响应 `data` 字段：**

| 字段 | 说明 |
|------|------|
| `tiers[]` | 各层级对比数据（见下） |
| `recommendation` | 综合投放建议（文字） |

**`tiers[]` 每项字段：**

| 字段 | 说明 |
|------|------|
| `label` | 层级名称（头部/腰部/尾部/普通博主） |
| `fansRange` | 粉丝量区间（如"10w-100w"） |
| `authorCount` | 该层级博主数量 |
| `avgFans` / `avgFansLabel` | 平均粉丝数 |
| `avgPicturePrice` / `avgVideoPrice` | 平均报价 |
| `avgEngageRate` | 平均互动率 |
| `estimatedRoi` | ROI估算（每百元约X次互动） |
| `roiNote` | ROI文字说明 |

---

## G — 品牌市场格局

```
POST /api/v1/aggregate/brand/market
```

**注意：此接口只支持类目名（如"手机"、"美妆"），不支持关键词。**

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `input` | string | ✅ | 类目名（需来自A接口列表） |
| `timeRange` | string | ❌ | `"7"` 或 `"30"`，默认 `"30"` |
| `rankBy` | string | ❌ | 排名维度：`searchNum`（搜索）/ `readNum`（阅读）/ `noteNum`（笔记数），默认 `searchNum` |
| `entityType` | string | ❌ | `brand`（品牌）/ `spu`（产品款式），默认 `brand` |

**响应 `data` 字段：**

`competition` — 品牌竞争格局：

| 字段 | 说明 |
|------|------|
| `totalBrands` | 参与竞争的品牌总数 |
| `topBrands[]` | 前10品牌（含品牌名/声量份额/笔记数/阅读数） |
| `concentrationNote` | 集中度判断（"高度集中"/"较分散"等） |

`ranking` — 品牌/SPU排名：

| 字段 | 说明 |
|------|------|
| `entityType` | 实体类型（品牌/产品） |
| `rankBy` | 排名维度 |
| `items[]` | 排名列表（含排名/名称/搜索量/阅读量/笔记数/是否峰值期） |

`marketOpportunity` — 市场供需：

| 字段 | 说明 |
|------|------|
| `searchNumLabel` | 搜索量 |
| `noteNumLabel` | 内容量 |
| `supplyDemandNote` | 供需关系文字判断 |

---

## 通用响应包装（A/E除外）

所有 POST 接口的响应都包含以下字段：

```json
{
  "_coverage": {
    "coverageNote": "数据覆盖近30天，基于已爬取样本，不代表全网"
  },
  "_dataGaps": ["话题分布数据不足", "..."],
  "data": { ... }
}
```

| 字段 | 说明 |
|------|------|
| `_coverage.coverageNote` | 数据范围声明，**输出时必须引用** |
| `_dataGaps` | 哪些维度数据不足，数组非空时需告知用户局限性 |
| `data` | 实际业务数据 |
