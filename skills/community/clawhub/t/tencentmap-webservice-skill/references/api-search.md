# 搜索服务 API

## 地点搜索

根据关键词搜索地点（POI），支持周边搜索、城市/区域搜索和矩形范围搜索。

**接口**: `GET /ws/place/v1/search`

**请求参数**:
- `key` (必填): 开发密钥
- `keyword` (必填): 搜索关键词（最大96字节，仅支持单个关键词）
- `boundary` (必填): 搜索范围，支持三种格式：
  - **周边搜索**: `nearby(lat,lng,radius[,auto_extend])`
    - `radius` — 搜索半径（米，10~1000）
    - `auto_extend` — 可选，`0`=不自动扩大范围，`1`=自动扩大（默认，依次按1km/2km/5km直到全城）
  - **城市/区域搜索**: `region(city_name[,auto_extend][,lat,lng])`
    - `city_name` — 城市名称或 adcode
    - `auto_extend` — `0`=仅在当前城市，`1`=无结果自动扩大（默认），`2`=限制在当前区/县
    - `lat,lng` — 可选，传入坐标优先返回附近地点
  - **矩形范围搜索**: `rectangle(lat1,lng1,lat2,lng2)` — 左下角到右上角
- `filter` (可选): 筛选条件（如 `category=美食`，排除 `category<>商务楼宇`，筛选有电话 `tel<>null`）
- `orderby` (可选): `_distance` 按距离排序（仅针对周边搜索）
- `page_size` (可选): 每页条目数，最大20，默认10
- `page_index` (可选): 页码，从1开始
- `get_subpois` (可选): 是否返回子地点（出入口、停车场等），`0`=否（默认），`1`=是
- `added_fields` (可选): 附加字段，如 `category_code`（POI 分类编码）
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`

**请求示例**:

周边搜索（海淀区附近2km内酒店）:
```
GET /ws/place/v1/search?key=YOUR_KEY&keyword=酒店&boundary=nearby(39.984154,116.307490,1000)&orderby=_distance
```

城市搜索（北京市内酒店，优先显示某坐标附近）:
```
GET /ws/place/v1/search?key=YOUR_KEY&keyword=酒店&boundary=region(北京,0,39.984154,116.307490)
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "request_id": "xxx",
  "count": 10,
  "data": [
    {
      "id": "xxx",
      "title": "如家酒店",
      "address": "北京市海淀区...",
      "tel": "010-12345678",
      "category": "酒店宾馆:酒店宾馆",
      "type": 0,
      "location": {
        "lat": 39.984154,
        "lng": 116.30749
      },
      "_distance": 123.5,
      "ad_info": {
        "adcode": 110108,
        "province": "北京市",
        "city": "北京市",
        "district": "海淀区"
      }
    }
  ],
  "region": {
    "title": "中国"
  }
}
```

> **注意**：服务最多返回200条数据。`type` 字段：0=普通POI，1=公交站，2=地铁站，3=公交线路，4=行政区划。

> **多边形搜索**是独立接口 `GET /ws/place/v1/search_by_polygon`，使用 `polygon` 参数（而非 `boundary`），格式为 `polygon=lat1,lng1;lat2,lng2;...`。

---

## 沿途搜索

在路线规划结果的沿途搜索 POI，适用于"沿途加油站"、"途经服务区"等场景。

**使用方式**: 先调用路线规划接口获取路线 polyline（折线坐标串），再使用地点搜索接口配合 `boundary=along` 参数进行沿途搜索。

**接口**: `GET /ws/place/v1/search`

**请求参数**:
- `key` (必填): 开发密钥
- `keyword` (必填): 搜索关键词（如"加油站"、"服务区"）
- `boundary` (必填): `along(lat1,lng1;lat2,lng2;..., distance)` - 沿途搜索
  - 折线坐标串：从路线规划接口返回的 polyline 坐标点
  - distance：搜索偏移距离（米），沿线两侧搜索范围
- `page_size` (可选): 每页结果数
- `page_index` (可选): 页码

**请求示例**:
```
GET /ws/place/v1/search?key=YOUR_KEY&keyword=加油站&boundary=along(39.984154,116.307490;39.974154,116.317490;39.964154,116.327490, 2000)
```

**典型使用流程**:
1. 调用驾车路线规划接口获取路线
2. 从路线结果中提取 polyline 坐标串
3. 使用 `boundary=along(polyline, distance)` 搜索沿途 POI

---

## 关键词输入提示

搜索框自动补全建议，帮助用户快速输入。

**接口**: `GET /ws/place/v1/suggestion`

**请求参数**:
- `key` (必填): 开发密钥
- `keyword` (必填): 用户输入的关键词
- `region` (可选): 限制城市范围（如 "北京"）
- `region_fix` (可选): 是否严格限制城市，`0`=不限制（默认），`1`=仅限当前城市
- `location` (可选): 定位坐标（格式 `lat,lng`），搜索类别词时优先返回附近地点
- `policy` (可选): 检索策略
  - `0`（默认）— 常规策略
  - `1` — 收货地址/上门服务（提高小区/楼宇排序）
  - `10` — 出行场景（网约车）起点
  - `11` — 出行场景（网约车）终点
- `filter` (可选): 筛选条件（如 `category=大学,中学`，最多5个分类）
- `get_subpois` (可选): 是否返回子地点，`0`=否（默认），`1`=是
- `get_ad` (可选): 是否返回区划结果，`0`=否（默认），`1`=是
- `address_format` (可选): `short` — 返回不带行政区划的短地址
- `added_fields` (可选): 附加字段，如 `category_code`
- `page_size` (可选): 每页条数（1-20，需与 page_index 同时使用）
- `page_index` (可选): 页码，从1开始
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`

**请求示例**:
```
GET /ws/place/v1/suggestion?key=YOUR_KEY&keyword=北京大&region=北京&region_fix=1&policy=0
```

**响应格式**:
```json
{
  "status": 0,
  "count": 10,
  "data": [
    {
      "id": "xxx",
      "title": "北京大学",
      "address": "北京市海淀区颐和园路5号",
      "category": "教育学校:大学",
      "type": 0,
      "location": {
        "lat": 39.998877,
        "lng": 116.316833
      },
      "adcode": 110108,
      "province": "北京市",
      "city": "北京市",
      "district": "海淀区",
      "_distance": 5230.5
    }
  ]
}
```

> `_distance` 仅在传入 `location` 参数时返回。`type` 字段：0=普通POI，1=公交站，2=地铁站，3=公交线路，4=行政区划。本服务最多返回100条结果。

---

## 行政区划

提供中国省、市、区/县、乡镇/街道行政区划数据查询，包含三个子接口。

### 获取全部行政区划列表

**接口**: `GET /ws/district/v1/list`

**请求参数**:
- `key` (必填): 开发密钥
- `struct_type` (可选): `1` — 以省市区实际归属嵌套返回（树状结构）

获取全国省/市/区三级列表。

### 获取下级行政区划

**接口**: `GET /ws/district/v1/getchildren`

**请求参数**:
- `key` (必填): 开发密钥
- `id` (可选): 父级行政区划 ID（adcode），缺省时返回省级列表
- `get_polygon` (可选): 返回行政区划轮廓
  - `0`（默认）— 不返回
  - `1` — 固定3km抽稀粒度
  - `2` — 支持多种抽稀粒度（需配合 max_offset）
  - `3` — 获取乡镇/街道（四级）轮廓边界（需联系商务开通）
- `max_offset` (可选): 轮廓抽稀精度（仅 get_polygon=2 时生效），单位米，可选值: 100/500/1000/3000

**请求示例**:
```
GET /ws/district/v1/getchildren?key=YOUR_KEY&id=110000
```

### 行政区划搜索

**接口**: `GET /ws/district/v1/search`

**请求参数**:
- `key` (必填): 开发密钥
- `keyword` (必填): 搜索关键词（如 "北京"、"海淀区"），也支持 adcode（如 `130681`，多个逗号分隔）
- `get_polygon` (可选): 返回行政区划轮廓（同上，仅 keyword 为单个 adcode 时生效）
- `max_offset` (可选): 轮廓抽稀精度

**请求示例**:
```
GET /ws/district/v1/search?key=YOUR_KEY&keyword=北京
```

### 行政区划响应格式

```json
{
  "status": 0,
  "data_version": "20251119",
  "result": [
    [
      {
        "id": "110000",
        "fullname": "北京市",
        "name": "北京",
        "location": {
          "lat": 39.904989,
          "lng": 116.405285
        },
        "pinyin": ["bei", "jing"],
        "cidx": [0, 15]
      }
    ]
  ]
}
```

**字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 行政区划编码（adcode） |
| fullname | string | 行政区划全称 |
| name | string | 简称 |
| location | object | 行政区划中心坐标 |
| pinyin | array | 拼音数组 |
| cidx | array | 子级行政区划在下一级数组中的索引范围 `[起始, 结束]`。无子级时不返回 |
| polygon | array | 轮廓数据（仅 get_polygon≥1 时返回），每项为一个多边形坐标数组 |
