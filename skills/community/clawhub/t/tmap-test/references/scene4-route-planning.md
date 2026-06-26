## 场景四：路径规划

使用腾讯地图 Web 服务 API 通过路径规划函数规划不同出行方式的路线。支持步行、驾车、骑行（自行车）、电动车、公交等多种出行方式。

**前置条件：** 需要用户在 OpenClaw 配置页面设置腾讯位置服务临时 API Key，同时不要提供给任何人。

### 调用函数

所有函数位于 `skills/tmap-lbs-skills/index.js`

| 出行方式       | 函数名        |
| -------------- | ------------- |
| 步行           | `walk_path`   |
| 驾车           | `drive_path`  |
| 骑行（自行车） | `cycle_path`  |
| 电动车         | `ecycle_path` |
| 公交           | `bus_path`    |

### 通用参数

| 参数          | 说明                 | 必填 | 示例                   |
| ------------- | -------------------- | ---- | ---------------------- |
| `origin`      | 起点坐标 "经度,纬度" | 是   | `116.397428,39.90923`  |
| `destination` | 终点坐标 "经度,纬度" | 是   | `116.427281,39.903719` |

**坐标格式：** 参数使用 `经度,纬度` 格式（经度在前），函数内部会自动转换为腾讯地图所需的 `纬度,经度` 格式。

### 使用方法

**步行路线：**

```bash
node -e "const {walk_path} = require('./skills/tmap-lbs-skills/index.js'); walk_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**驾车路线：**

```bash
node -e "const {drive_path} = require('./skills/tmap-lbs-skills/index.js'); drive_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**驾车路线（带途经点和策略）：**

```bash
node -e "const {drive_path} = require('./skills/tmap-lbs-skills/index.js'); drive_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719', waypoints: '116.410000,39.910000', policy: 'LEAST_TIME' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**骑行路线（自行车）：**

```bash
node -e "const {cycle_path} = require('./skills/tmap-lbs-skills/index.js'); cycle_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**电动车路线：**

```bash
node -e "const {ecycle_path} = require('./skills/tmap-lbs-skills/index.js'); ecycle_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**公交路线：**

```bash
node -e "const {bus_path} = require('./skills/tmap-lbs-skills/index.js'); bus_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

**公交路线（带策略）：**

```bash
node -e "const {bus_path} = require('./skills/tmap-lbs-skills/index.js'); bus_path({ origin: '116.397428,39.90923', destination: '116.427281,39.903719', policy: 'LEAST_TRANSFER' }).then(r => console.log(JSON.stringify(r, null, 2)))"
```

### 驾车专有参数

| 参数           | 说明                                    | 示例                        |
| -------------- | --------------------------------------- | --------------------------- |
| `waypoints`    | 途经点坐标 "经度,纬度"，多个用 `;` 分隔 | `116.41,39.91;116.42,39.92` |
| `policy`       | 驾车策略                                | `LEAST_TIME`                |
| `plate_number` | 车牌号，用于避开限行                    | `京A12345`                  |

**驾车策略（policy）：**

- `LEAST_TIME` — 时间最短（默认）
- `LEAST_FEE` — 少收费
- `AVOID_HIGHWAY` — 不走高速
- `HIGHWAY_FIRST` — 高速优先

### 公交专有参数

| 参数             | 说明                    | 示例         |
| ---------------- | ----------------------- | ------------ |
| `policy`         | 公交策略                | `LEAST_TIME` |
| `departure_time` | 出发时间（Unix 时间戳） | `1700000000` |

**公交策略（policy）：**

- `LEAST_TIME` — 时间短（默认）
- `LEAST_TRANSFER` — 少换乘
- `LEAST_WALKING` — 少步行
- `RECOMMEND` — 推荐策略

### 返回数据说明

**步行 / 骑行 / 电动车 / 驾车返回：**

```json
{
  "status": "1",
  "route": {
    "paths": [
      {
        "distance": 3200,
        "duration": 40,
        "steps": [...]
      }
    ]
  },
  "_raw": { "...原始API响应..." }
}
```

**公交返回：**

```json
{
  "status": "1",
  "route": {
    "transits": [
      {
        "duration": 35,
        "distance": 5000,
        "bounds": "...",
        "steps": [...]
      }
    ]
  },
  "_raw": { "...原始API响应..." }
}
```

| 字段                  | 说明                     |
| --------------------- | ------------------------ |
| `status`              | 状态码，`"1"` 表示成功   |
| `distance`            | 路线总距离，单位：米     |
| `duration`            | 预计耗时，单位：分钟     |
| `toll`                | 过路费（驾车），单位：元 |
| `traffic_light_count` | 红绿灯数量（驾车）       |
| `steps`               | 详细步骤数组             |
| `_raw`                | 原始 API 响应数据        |

### 错误处理

- 函数返回 `null` 时表示请求失败，错误信息会输出到控制台
- 常见错误：Key 无效、配额不足、坐标格式错误、起终点太近或太远
