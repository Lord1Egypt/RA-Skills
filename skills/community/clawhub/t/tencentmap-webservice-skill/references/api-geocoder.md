# 地址服务 API

## 地址解析（地址 → 坐标）

将文字地址转换为坐标（地理编码），同时提供结构化的省市区地址信息。

**接口**: `GET /ws/geocoder/v1/`

**请求参数**:
- `key` (必填): 开发密钥
- `address` (必填): 地址（建议包含城市名以提高准确率，需 URL 编码）
- `region` (可选): 指定城市，提高准确性
- `policy` (可选): 解析策略
  - `0`（默认）— 标准策略，地址中须包含城市
  - `1` — 宽松策略，允许地址中缺失城市（准确性可能受影响）
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`
- `callback` (可选): JSONP 回调函数名

**请求示例**:
```
GET /ws/geocoder/v1/?key=YOUR_KEY&address=北京市海淀区彩和坊路海淀西大街74号
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "request_id": "xxx",
  "result": {
    "title": "海淀西大街74号",
    "location": {
      "lng": 116.307015,
      "lat": 39.982915
    },
    "ad_info": {
      "adcode": "110108"
    },
    "address_components": {
      "province": "北京市",
      "city": "北京市",
      "district": "海淀区",
      "street": "彩和坊路",
      "street_number": ""
    },
    "similarity": 0.99,
    "deviation": 1000,
    "reliability": 7,
    "level": 9
  }
}
```

**响应字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 解析到的地址标题 |
| location | object | 解析到的坐标（GCJ-02 坐标系） |
| address_components | object | 地址部件（province/city/district/street/street_number） |
| ad_info.adcode | string | 行政区划代码 |
| similarity | number | 地址与输入的相似度（0-1） |
| deviation | number | 可能的偏移距离（米） |
| reliability | number | 可信度参考（1-10），≥7 较为准确 |
| level | number | 解析精度级别，≥9 表示精确到门址/POI |

**level 取值说明**: 0=无法判别, 1=城市, 2=区县, 3=乡镇, 7=道路, 9=门址, 10=小区大厦, 11=POI点

---

## 逆地址解析（坐标 → 地址）

将坐标转换为文字地址（逆地理编码），支持获取行政区划、周边地标和 POI 列表。

**接口**: `GET /ws/geocoder/v1/`

**请求参数**:
- `key` (必填): 开发密钥
- `location` (必填): 坐标（GCJ-02），格式 `纬度,经度`（注意顺序）
- `get_poi` (可选): 是否返回周边 POI，`0`=否（默认），`1`=是
- `poi_options` (可选): POI 控制参数，多个用英文分号 `;` 分隔
  - `address_format=short` - 返回短地址
  - `radius=5000` - 搜索半径（米，1-5000）
  - `policy=1/2/3/4/5` - 场景策略：
    - `1`（默认）- 地标+主要道路+近距离 POI
    - `2` - 到家场景（精确到楼栋）
    - `3` - 出行场景（过滤不易到达 POI）
    - `4` - 社交签到
    - `5` - 位置共享
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`

**请求示例**:
```
GET /ws/geocoder/v1/?key=YOUR_KEY&location=39.984154,116.307490&get_poi=1&poi_options=address_format=short;radius=5000;policy=2
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "request_id": "xxx",
  "result": {
    "location": {
      "lat": 39.984154,
      "lng": 116.30749
    },
    "address": "北京市海淀区彩和坊路",
    "formatted_addresses": {
      "recommend": "海淀区中关村中国技术交易大厦(彩和坊路西)",
      "rough": "海淀区中关村中国技术交易大厦(彩和坊路西)",
      "standard_address": "北京市海淀区北四环西路66号"
    },
    "address_component": {
      "nation": "中国",
      "province": "北京市",
      "city": "北京市",
      "district": "海淀区",
      "street": "彩和坊路",
      "street_number": ""
    },
    "ad_info": {
      "nation_code": "156",
      "adcode": "110108",
      "city_code": "110100",
      "name": "北京市海淀区",
      "location": { "lat": 39.959912, "lng": 116.298056 }
    },
    "address_reference": {
      "famous_area": { "id": "xxx", "title": "中关村", "location": {...}, "_distance": 0, "_dir_desc": "内" },
      "business_area": { "id": "xxx", "title": "中关村", "location": {...}, "_distance": 0, "_dir_desc": "内" },
      "town": { "id": "110108012", "title": "海淀街道", "location": {...}, "_distance": 0, "_dir_desc": "内" },
      "landmark_l2": { "id": "xxx", "title": "中国技术交易大厦", "location": {...}, "_distance": 0, "_dir_desc": "内" },
      "street": { "id": "xxx", "title": "彩和坊路", "location": {...}, "_distance": 44.4, "_dir_desc": "西" },
      "crossroad": { "id": "xxx", "title": "彩和坊路/海淀北一街(路口)", "location": {...}, "_distance": 61.5, "_dir_desc": "西" }
    },
    "poi_count": 10,
    "pois": [
      {
        "id": "xxx",
        "title": "中国技术交易大厦",
        "address": "北四环西路66号",
        "category": "房产小区:商务楼宇",
        "location": { "lat": 39.984105, "lng": 116.307499 },
        "ad_info": { "adcode": "110108", "province": "北京市", "city": "北京市", "district": "海淀区" },
        "_distance": 0,
        "_dir_desc": "内"
      }
    ]
  }
}
```

> **注意**：逆地址解析的地址部件字段名是 `address_component`（单数），与地址解析的 `address_components`（复数）不同。

**逆地址解析核心字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| address | string | 标准格式化地址（行政区划+道路） |
| formatted_addresses.recommend | string | 推荐的描述性地址（结合知名地标） |
| formatted_addresses.rough | string | 粗略位置描述 |
| formatted_addresses.standard_address | string | 标准地址（含门牌号） |
| address_component | object | 地址部件（nation/province/city/district/street/street_number） |
| ad_info.adcode | string | 行政区划代码 |
| ad_info.city_code | string | 城市代码 |
| address_reference | object | 地址参考信息（famous_area/business_area/town/landmark_l2/street/crossroad 等） |
| poi_count | number | 返回的 POI 数量 |
| pois[].id | string | POI 唯一标识 |
| pois[].ad_info | object | POI 所属行政区划（adcode/province/city/district） |
| pois[]._distance | number | 距输入坐标的直线距离（米） |
| pois[]._dir_desc | string | 相对方位描述（东/南/内等） |

---

## 智能地址解析

从非结构化文本中提取地址信息并解析为结构化数据和坐标。适用于从快递单、聊天记录等非标准文本中提取地址，同时自动识别姓名和手机号。

> **注意**：此接口为高级版服务，需企业认证后通过工单申请开通。

**接口**: `GET /ws/geocoder/v1/`（与地址解析相同的接口，通过 `smart_address` 参数触发智能解析）

**请求参数**:
- `key` (必填): 开发密钥
- `smart_address` (必填): 非结构化地址文本（如 "张三 13800138000 北京市海淀区中关村大街1号"）
- `region` (可选): 指定城市，提高准确性
- `policy` (可选): 解析策略，`0`=标准（默认），`1`=宽松
- `added_fields` (可选): 附加字段，逗号分隔
  - `split_address` — 旧版地址切分结果
  - `split_address_v2` — 新版地址切分结果
  - `town` — 乡镇/街道名称
  - `town_code` — 乡镇/街道代码
- `output` (可选): 返回格式，`json`（默认）/ `jsonp`

**请求示例**:
```
GET /ws/geocoder/v1/?key=YOUR_KEY&smart_address=张三13800138000北京市海淀区中关村大街1号
```

**响应格式**:
```json
{
  "status": 0,
  "message": "query ok",
  "request_id": "xxx",
  "result": {
    "location": {
      "lat": 39.984154,
      "lng": 116.30749
    },
    "address_components": {
      "province": "北京市",
      "city": "北京市",
      "district": "海淀区",
      "street": "中关村大街",
      "street_number": "1号"
    },
    "ad_info": {
      "adcode": "110108"
    },
    "formatted_address": "北京市海淀区中关村大街1号",
    "analysis_address": "北京市海淀区中关村大街1号",
    "short_address": "中关村大街1号",
    "person_name": "张三",
    "tel": "13800138000",
    "reliability": 7,
    "level": 9
  }
}
```

**智能解析特有字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| formatted_address | string | 格式化后的地址 |
| analysis_address | string | 补全省市区后的完整地址 |
| short_address | string | 短地址（不含省市区划） |
| person_name | string | 提取的姓名 |
| tel | string | 提取的电话号码 |
| reliability | number | 可信度参考（1-10） |
| level | number | 解析精度级别 |
