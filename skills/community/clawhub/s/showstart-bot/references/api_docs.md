# Showstart Skill API 文档

## 基础信息

- **API地址**: https://skill.showstart.com/

## 频率限制

- **1秒最多1次请求**
- **10分钟最多60次请求**
- 超过限制返回错误码 `100003`

## 接口列表

### 1. 查询演出详情

**接口**: `/?id={activityId}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| --- | ------ | -- | ---- |
| id | number | 是 | 演出ID |

**示例**:
```
GET /?id=135591
```

**返回示例**:
```json
{
  "success": true,
  "result": {
    "activityId": 135591,
    "title": "演出名称",
    "city": "北京",
    "cityId": "10",
    "siteName": "场地名称",
    "showTime": "2026.03.24 周一 20:00",
    "price": "¥180起",
    "styles": ["流行", "摇滚"],
    "showTypeTagName": "音乐节",
    "showTypeTagId": 1387,
    "poster": "/img/xxx.jpg",
    "minPrice": 1800000,
    "maxPrice": 5800000,
    "wishCount": 1234,
    "performers": [...],
    "sessions": [...]
  }
}
```

### 2. 关键字搜索

**接口**: `/?keyword={keyword}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| ------- | ------ | -- | ----- |
| keyword | string | 是 | 搜索关键字 |

**说明**: 独立参数，不能与其他搜索参数组合

**示例**:
```
GET /?keyword=周云蓬
```

### 3. 城市搜索（支持模糊搜索）

**接口**: `/?city={cityName}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| ---- | ------ | -- | --------------- |
| city | string | 是 | 城市名称(中文)，支持模糊匹配 |

**说明**:
- 支持模糊搜索，如搜索"京"可匹配"北京"、"南京"
- 可与category、style参数组合使用(&关系)

**示例**:
```
GET /?city=北京
GET /?city=京
GET /?city=北京&category=音乐节
```

### 4. 分类搜索（支持模糊搜索）

**接口**: `/?category={categoryName}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| -------- | ------ | -- | --------------- |
| category | string | 是 | 分类名称(中文)，支持模糊匹配 |

**常用分类**: 音乐节、演唱会、话剧、音乐剧、展览、脱口秀等

**说明**:
- 支持模糊搜索，如搜索"音乐"可匹配"音乐节"、"音乐剧"、"音乐会"等
- 可与city、style参数组合使用(&关系)

**示例**:
```
GET /?category=音乐节
GET /?category=音乐
GET /?city=上海&category=演唱会
```

### 5. 风格搜索（支持模糊搜索）

**接口**: `/?style={styleName}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| ----- | ------ | -- | --------------- |
| style | string | 是 | 风格名称(中文)，支持模糊匹配 |

**常用风格**: 摇滚、流行、民谣、电子、爵士、嘻哈等

**说明**:
- 支持模糊搜索，如搜索"摇"可匹配"摇滚"
- 可与city、category参数组合使用(&关系)

**示例**:
```
GET /?style=摇滚
GET /?style=摇
GET /?city=北京&style=民谣
```

### 6. 艺人/场地名搜索（支持模糊搜索）

**接口**: `/?name={name}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| ---- | ------ | -- | -------------- |
| name | string | 是 | 艺人名或场地名，支持模糊匹配 |

**说明**: 独立参数，不能与其他搜索参数组合

**示例**:
```
GET /?name=周云蓬
```

### 7. 经纬度搜索(附近演出)

**接口**: `/?loc={longitude},{latitude}`

**参数**:

| 参数名 | 类型 | 必填 | 说明 |
| --- | ------ | -- | ----- |
| loc | string | 是 | 经度,纬度 |

**说明**: 独立参数，不能与其他搜索参数组合。返回结果按距离排序

**示例**:
```
GET /?loc=116.3956,39.9299
```

## 组合搜索规则

### 可组合参数

- city + category
- city + style
- category + style
- city + category + style

### 独立参数(不可组合)

- keyword
- name
- loc

### 必须提供参数

至少提供一个搜索参数，否则返回错误

## 分页参数

| 参数名 | 类型 | 默认值 | 最大值 | 说明 |
| -------- | ------ | --- | --- | ---- |
| pageNo | number | 1 | - | 页码 |
| pageSize | number | 100 | 100 | 每页数量 |

**示例**:
```
GET /?city=北京&pageNo=1&pageSize=20
```

## 缓存机制

- 所有搜索结果缓存 **1小时**
- 相同请求会命中缓存，响应更快

## 返回格式

### 成功响应

```json
{
  "success": true,
  "result": {
    "total": 100,
    "pageNo": 1,
    "pageSize": 100,
    "list": [
      {
        "activityId": 135591,
        "title": "演出名称",
        "city": "北京",
        "showTime": "2026.03.24 周一 20:00",
        "price": "¥180起",
        ...
      }
    ]
  }
}
```

### 错误响应

```json
{
  "success": false,
  "state": "100002",
  "msg": "missing search parameter"
}
```

### 错误码说明

| 错误码 | 说明 |
| ------ | ------ |
| 100001 | 资源不存在 |
| 100002 | 缺少必要参数 |
| 100003 | 频率限制超限 |

## Python API 使用示例

```python
from showstart_api import get_activity, search_city, search_keyword

# 查询演出详情
activity = get_activity(135591)

# 城市搜索
results = search_city("北京", category="音乐节")

# 关键字搜索
results = search_keyword("周云蓬")
```

## CLI 使用示例

```bash
# 查询演出详情
python showstart_api.py activity 135591

# 城市搜索
python showstart_api.py city 北京

# 分类搜索
python showstart_api.py category 音乐节

# 风格搜索
python showstart_api.py style 摇滚

# 关键字搜索
python showstart_api.py keyword 周云蓬
```
