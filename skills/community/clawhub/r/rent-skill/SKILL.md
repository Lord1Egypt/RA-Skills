---
name: fliggy-rental-car
version: 1.0.0
description: 飞猪租车智能推荐助手。根据用户出行需求（人数、目的地、时间、品牌偏好）推荐最适合的租车车型，支持调用飞猪租车Mtop API查询实时库存。
author: ruji.mqq
tags: [飞猪, 租车, 交通, 车型推荐]
---

# 飞猪租车智能推荐助手

帮助用户快速找到最适合的租车车型。

## 工作流程

### 第1步：收集用户出行信息

通过交互式对话收集以下必需信息：

| 信息项 | 说明 | 示例 |
|--------|------|------|
| **目的地** | 取车城市（需要转换为城市编码） | 北京 → P_V1_487161 |
| **出行时间** | 取车日期和还车日期（时间戳毫秒） | 2026-04-10 10:00 |
| **出行人数** | 乘车人数（决定座位数需求） | 4人 → 推荐5座车 |
| **品牌偏好** | 可选，用户有偏好时收集 | 特斯拉、比亚迪 |

**收集策略**：
- 用户一次性提供完整信息 → 直接进入第2步
- 用户只提供部分信息 → 依次询问缺失项
- 品牌偏好为非必需项，如用户未提及可不收集

### 第2步：计算座位数需求

根据出行人数计算所需座位数：

```
座位数需求 = 出行人数
```

**常见映射关系**：
| 出行人数 | 推荐座位数 | 典型车型 |
|----------|-----------|----------|
| 1-4人 | 5座 | 轿车、SUV |
| 5-6人 | 7座 | 商务MPV |
| 7-8人 | 9座 | 商务车 |

### 第3步：调用 Mtop API 查询车型

使用飞猪租车 API 查询可用车型：

```bash
mtop.trip.tfrcs.rentcar.queryItems
```

**请求参数 (reqParams)**：
```json
{
  "bizType": "3",
  "subBizType": "31",
  "carUseDate": 1775268000000,
  "carReturnDate": 1775440800000,
  "departureAddressParams": "P_V1_487161",
  "destinationAddressParams": "P_V1_487161",
  "departureCityParams": "P_V1_487161",
  "destinationCityParams": "P_V1_487161",
  "driverAge": "30",
  "loadCount": 1,
  "sortType": 1,
  "utcOffset": -480,
  "pageNo": 1,
  "pageSize": 10,
  "contextId": "QGW3egY7f739fqOT2J0XDLBDWkirWE",
  "fpt": "ftuid(pv4i6iDe064813.2)hsts(1775216097018)",
  "searFilterTags": "[\"category_all\",\"fuelGroup_1\",\"seat_4\",\"brand_蔚来\"]",
  "isCredit": false,
  "isPickUpOnDoor": false,
  "userFlowParam": "{\"spmDetail\":\"181.20978741.filter_dialog_settings.complete\",\"clientReqTime\":\"2026-04-03 19:43:45.662\"}",
  "h5Version": "1.23.99"
}
```

**关键字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `carUseDate` | 取车时间戳（毫秒） | 1775268000000 |
| `carReturnDate` | 还车时间戳（毫秒） | 1775440800000 |
| `departureCityParams` | 出发城市编码 | P_V1_487161（北京） |
| `destinationCityParams` | 目的城市编码 | P_V1_487161 |
| `searFilterTags` | 筛选标签JSON数组 | 座位数、品牌、能源类型等 |
| `sortType` | 排序方式 | 1=综合排序, 5=总价低→高 |
| `pageSize` | 每页数量 | 10 |

**筛选标签 (searFilterTags) 格式**：
```json
[
  "category_all",           // 全部车型
  "fuelGroup_1",            // 能源类型: 1=汽油, 2=纯电动, 3=新能源混动
  "seat_4",                 // 座位数: seat_2/4/5/6/7
  "brand_蔚来",             // 品牌筛选
  "gear_自动",              // 挡位: 手动/自动
  "quick_39"                // 车龄: 39=6个月内新车
]
```

**响应结构 (resData)**：
```json
{
  "api": "mtop.trip.tfrcs.rentcar.queryItems",
  "data": {
    "globalData": {
      "carSize": 22,
      "contextId": "QGW3egY7f739fqOT2J0XDLBDWkirWE",
      "departureAddress": "北京大兴国际机场",
      "destinationAddress": "北京大兴国际机场",
      "filters": { /* 筛选器配置 */ }
    },
    "items": [
      {
        "carModelId": "xxx",
        "carModelName": "比亚迪秦PLUS",
        "brandName": "比亚迪",
        "seatCount": 5,
        "carType": "新能源",
        "price": {
          "single": 208,          // 日租金
          "finalSummary": 854     // 总价
        },
        "imageUrl": "https://...",
        "jumpKey": "ota_key_xxx",  // OTA页面跳转key
        "providerInfo": {
          "name": "神州租车",
          "score": 4.9
        }
      }
    ]
  }
}
```

### 第4步：筛选和排序车型

根据以下规则筛选：

1. **座位数匹配**：优先精确匹配，其次向上兼容（如需要5座，5/7/9座都可）
2. **品牌偏好**：如有品牌偏好，优先展示该品牌车型
3. **库存可用**：确保查询时间段内有库存
4. **排序规则**：
   - 默认按价格从低到高
   - 如有品牌偏好，该品牌车型置顶

### 第5步：展示推荐结果

在对话框中以 Markdown 表格形式展示 Top 3-5 车型：

```markdown
## 🚗 为您推荐的车型

### Top 1: {车型名称} ⭐ 最匹配
- **品牌**: {brandName}
- **座位数**: {seatCount}座
- **日租金**: ¥{price.single}/天
- **预估总价**: ¥{price.finalSummary}
- **商家**: {providerInfo.name} ({providerInfo.score}分)
- [选择商家预订]({otaLink})

### Top 2: {车型名称}
...
```

**展示要素**：
- 车型图片（如有）
- 品牌、车系名称
- 座位数
- 日租金价格 / 预估总价
- 商家名称和评分
- 特色标签（新能源、豪华型等）
- 直达 OTA 页面的链接

### 第6步：处理用户后续操作

用户可能的后续需求：

| 用户操作 | Skill 响应 |
|----------|-----------|
| 点击 OTA 链接 | 打开商家选择页面 |
| 询问某车型详情 | 展示更详细的车型信息 |
| 调整筛选条件 | 重新执行第3-5步 |
| 确认租车 | 提供预订指引 |

## Mtop API 规范

### API: mtop.trip.tfrcs.rentcar.queryItems

**用途**：查询租车车型列表

**调用方式**：
```bash
mtop.trip.tfrcs.rentcar.queryItems --data '{
  "bizType": "3",
  "subBizType": "31",
  "carUseDate": {timestamp_ms},
  "carReturnDate": {timestamp_ms},
  "departureCityParams": "{city_code}",
  "destinationCityParams": "{city_code}",
  "searFilterTags": "[{filters}]",
  "pageSize": 10
}'
```

### 城市编码映射

常见城市编码（需根据实际系统获取完整映射）：

| 城市 | 编码 |
|------|------|
| 北京 | P_V1_487161 |
| 上海 | P_V1_xxx |
| 广州 | P_V1_xxx |
| 深圳 | P_V1_xxx |
| 成都 | P_V1_xxx |
| 杭州 | P_V1_xxx |

### 筛选标签对照表

**能源类型 (fuelGroup)**：
- `fuelGroup_1` - 汽油
- `fuelGroup_2` - 纯电动
- `fuelGroup_3` - 新能源混动

**座位数 (seat)**：
- `seat_2` - 2座
- `seat_4` - 4座
- `seat_5` - 5座
- `seat_6` - 6座
- `seat_7` - 7座

**品牌 (brand)**：
- `brand_特斯拉`, `brand_比亚迪`, `brand_蔚来`, `brand_理想`
- `brand_宝马`, `brand_奔驰`, `brand_奥迪`
- `brand_丰田`, `brand_本田`, `brand_大众`
- ...（详见 data.js 完整列表）

**车辆配置 (quick)**：
- `quick_18` - 倒车雷达
- `quick_26` - 倒车影像
- `quick_39` - 6个月内新车
- `quick_40` - 满油/满电取车
- `quick_41` - 不限里程

## OTA 页面链接拼接

### 基础 URL
```
https://outfliggys.m.taobao.com/app/trip/rx-vehicle-ota/pages/home
```

### 参数拼接
```javascript
const params = {
  // 基础参数
  contextId: mainState?.renderReqParams?.contextId,
  otaKey: encodeURIComponent(item?.jumpKey),
  searFilterTags: JSON.stringify(searFilterTags),
  fpt: resultFpt,
  
  // 页面配置
  __webview_options__: 'allowsBounceVertical=NO&transparentTitle=always&titlePenetrate=YES&showOptionMenu=NO&readTitle=NO',
  enableTitleBar: 'YES',
  _use_stream: 1,
  
  // 车型信息
  category: metricExt?.category || '',
  carName: metricExt?.carName || '',
  fuelTypeGroup: metricExt?.fuelTypeGroup || '',
  formCity: metricExt?.formCity || '',
  
  // 其他参数
  linkedId: urlParams?.linkedId,
  originModifyOrderId: urlParams?.originModifyOrderId,
  exParams: encodeURIComponent(JSON.stringify({ ext: urlParams.ext, source: urlParams.source })),
  pageUniqueId_url: globalBizArgs?.pageUniqueId,
};
```

### 完整链接示例
```
https://outfliggys.m.taobao.com/app/trip/rx-vehicle-ota/pages/home
  ?otaKey=xxx
  &contextId=xxx
  &searFilterTags=xxx
  &fpt=xxx
  &enableTitleBar=YES
  &_use_stream=1
```

## 车型展示模板

### 对话框展示格式

```markdown
## 🚗 {城市} 租车推荐
**{取车日期} - {还车日期}** | {出行人数}人出行

---

### 🥇 {车型1名称} ⭐ 最匹配
![车型图片]({imageUrl})

| 项目 | 内容 |
|------|------|
| 品牌 | {brandName} |
| 座位 | {seatCount}座 |
| 类型 | {carType} |
| 日租金 | **¥{price.single}/天** |
| 预估总价 | ¥{price.finalSummary} |
| 商家 | {providerInfo.name} ⭐{providerInfo.score} |

**特色**: {featureDescription}

👉 [选择商家预订]({otaLink})

---

### 🥈 {车型2名称}
...
```

## 特殊情况处理

### 无可用车型
如果查询结果为空：
1. 提示用户调整时间或目的地
2. 建议扩大座位数筛选范围
3. 推荐邻近城市取车

### 库存不足
如果目标车型库存紧张：
1. 提示"该车型库存紧张，建议尽快预订"
2. 推荐相似替代车型

### 品牌偏好无结果
如果用户指定的品牌在当地无库存：
1. 告知该品牌暂无可用车辆
2. 推荐同档次其他品牌车型

## 示例对话

**用户**: 我想租车，4个人去北京，4月10号到15号

**Skill**:
> 收到！为您查询北京 4月10日-15日的租车车型。
>
> 出行信息确认：
> - 目的地：北京
> - 时间：2026-04-10 至 2026-04-15
> - 人数：4人 → 推荐5座车
>
> 是否有品牌偏好？（如特斯拉、比亚迪等，无偏好可直接查询）

**用户**: 没有偏好

**Skill**:
> 正在查询可用车型...
>
> ## 🚗 北京租车推荐
> ...（展示车型列表）

## 注意事项

1. **价格显示**：API 返回的 `price.single` 为日租金，`price.finalSummary` 为预估总价（含手续费、车辆保障费等）
2. **时间格式**：API 使用毫秒时间戳，需将用户输入的日期转换为时间戳
3. **城市编码**：需要将用户输入的城市名转换为对应的城市编码
4. **OTA 链接**：确保链接可正常跳转至飞猪租车 OTA 详情页
5. **库存实时性**：提示用户价格库存实时变动，以实际下单为准
6. **筛选标签**：`searFilterTags` 为 JSON 数组字符串，需正确转义
