## 场景三：POI 详细搜索

使用腾讯地图 Web 服务 API 通过 `query_place` 函数进行 POI 搜索，支持关键词搜索、城市限定、周边搜索等。

**前置条件：** 需要用户提供腾讯位置服务的 临时 API Key。

### 调用函数

`query_place(params)` — 位于 `skills/tmap-lbs-skills/index.js`

### 参数说明

| 参数       | 说明                         | 必填 | 示例                  |
| ---------- | ---------------------------- | ---- | --------------------- |
| `keywords` | 搜索关键词                   | 是   | `肯德基`              |
| `city`     | 城市名称（城市搜索时必填）   | 否   | `北京`                |
| `location` | 中心点坐标 "经度,纬度"       | 否   | `116.397428,39.90923` |
| `radius`   | 搜索半径(米)，周边搜索时必填 | 否   | `1000`                |
| `types`    | POI 分类筛选                 | 否   | `餐饮`                |
| `page`     | 页码，从 1 开始              | 否   | `1`                   |
| `offset`   | 每页数量（最大 20）          | 否   | `10`                  |

**注意：** `location` 使用 `经度,纬度` 格式（经度在前，纬度在后），函数内部会自动转换为腾讯地图所需的 `纬度,经度` 格式。

### 使用方法

**城市关键词搜索：**

```bash
node -e "const {query_place} = require('./skills/tmap-lbs-skills/index.js'); query_place({ keywords: '肯德基', city: '北京', page: 1, offset: 10 }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**周边搜索（指定坐标和半径）：**

```bash
node -e "const {query_place} = require('./skills/tmap-lbs-skills/index.js'); query_place({ keywords: '酒店', location: '116.397428,39.90923', radius: 1000, page: 1, offset: 10 }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**带分类筛选的搜索：**

```bash
node -e "const {query_place} = require('./skills/tmap-lbs-skills/index.js'); query_place({ keywords: '餐厅', city: '上海', types: '餐饮', page: 1, offset: 20 }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

### 返回数据格式

函数返回经过处理的结构化数据：

```json
{
  "status": "1",
  "count": 100,
  "pois": [
    {
      "name": "肯德基(王府井店)",
      "address": "北京市东城区王府井大街...",
      "type": "餐饮:快餐",
      "tel": "010-12345678",
      "location": "116.41,39.914",
      "distance": 500,
      "id": "..."
    }
  ],
  "_raw": { "...原始API响应..." }
}
```

### 返回字段说明

| 字段       | 说明                               |
| ---------- | ---------------------------------- |
| `status`   | 状态码，`"1"` 表示成功             |
| `count`    | 结果总数                           |
| `pois`     | POI 结果数组                       |
| `name`     | 地点名称                           |
| `address`  | 地址                               |
| `type`     | 分类                               |
| `tel`      | 电话                               |
| `location` | 坐标 `"经度,纬度"` 格式            |
| `distance` | 距中心点距离（周边搜索时），单位米 |
| `_raw`     | 原始 API 响应数据                  |

### 错误处理

- 函数返回 `null` 时表示请求失败，错误信息会输出到控制台
- 常见错误：Key 无效、配额不足、参数格式错误
