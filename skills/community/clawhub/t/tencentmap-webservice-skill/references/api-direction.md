# 路线服务 API

## 驾车路线规划

计算驾车路线，支持途经点、实时路况、多种策略和偏好。

**接口**: `GET /ws/direction/v1/driving/`

**请求参数**:
- `key` (必填): 开发密钥
- `from` (必填): 起点坐标，格式 `纬度,经度`
- `to` (必填): 终点坐标，格式 `纬度,经度`
- `from_poi` (可选): 起点 POI ID（优先级高于 from 坐标）
- `to_poi` (可选): 终点 POI ID（优先级高于 to 坐标）
- `waypoints` (可选): 途经点，格式 `lat1,lng1;lat2,lng2`，最多30个
- `policy` (可选): 策略参数，支持策略与偏好混用（逗号分隔）
  - **策略（三选一）**:
    - `LEAST_TIME` — 时间最短（默认）
    - `PICKUP` — 网约车接乘客
    - `TRIP` — 网约车送乘客
  - **偏好（可多选）**:
    - `REAL_TRAFFIC` — 参考实时路况
    - `LEAST_FEE` — 少收费
    - `HIGHWAY_FIRST` — 高速优先
    - `AVOID_HIGHWAY` — 不走高速
    - `HIGHROAD_FIRST` — 大路优先
    - `NAV_POINT_FIRST` — 以地点出入口为终点
- `heading` (可选): 起点车头方向（0-360度），0为正北
- `speed` (可选): 起点速度（米/秒），默认3
- `accuracy` (可选): 定位精度（米），默认5
- `road_type` (可选): 起点道路类型，`0`=默认，`1`=桥上，`2`=桥下，`3`=主路，`4`=辅路
- `plate_number` (可选): 车牌号，用于限行避让
- `cartype` (可选): 车辆类型，`0`=普通汽车（默认），`1`=新能源
- `avoid_polygons` (可选): 避让区域，最多32个，格式 `lat,lng;lat,lng|lat,lng;lat,lng`
- `get_mp` (可选): 是否返回多方案，`0`=仅一条（默认），`1`=最多三条
- `get_speed` (可选): 是否返回路况速度，`0`=不返回（默认），`1`=返回
- `added_fields` (可选): 附加字段，如 `cities`（途经行政区划）
- `no_step` (可选): 不返回路线引导信息，`0`=返回（默认），`1`=不返回

**请求示例**:
```
GET /ws/direction/v1/driving/?key=YOUR_KEY&from=39.984154,116.307490&to=39.904989,116.405285&policy=LEAST_TIME,REAL_TRAFFIC
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "result": {
    "routes": [
      {
        "mode": "DRIVING",
        "distance": 18377,
        "duration": 37,
        "traffic_light_count": 19,
        "toll": 0,
        "tags": [],
        "polyline": [39.984094, 116.307958, 14, 112, ...],
        "steps": [
          {
            "instruction": "沿彩和坊路向东行驶123米",
            "road_name": "彩和坊路",
            "dir_desc": "东",
            "distance": 123,
            "act_desc": "左转",
            "accessorial_desc": "",
            "polyline_idx": [0, 5]
          }
        ],
        "taxi_fare": {
          "fare": 53
        },
        "restriction": {
          "status": 1
        }
      }
    ]
  }
}
```

> **重要**：
> - `duration` 单位为**分钟**（非秒）
> - `polyline` 是**压缩后的差分数组**，需解压：第一对值为原始坐标（小数形式如 39.984094, 116.307958），后续值为差分（整数，单位 10⁻⁶ 度），解压时 `coors[i] = coors[i-2] + coors[i]/1000000`
> - `polyline_idx` 是该 step 坐标在 polyline 中的索引范围 `[start, end]`

**路线方案字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| mode | string | 交通方式（DRIVING） |
| tags | array | 方案标签（RECOMMEND/LEAST_TIME/LEAST_FEE/HIGHWAY_FIRST等），可能为空数组 |
| distance | number | 总距离（米） |
| duration | number | 预估时间（**分钟**，含路况） |
| traffic_light_count | number | 途经红绿灯个数 |
| toll | number | 收费金额（元） |
| polyline | array | 压缩坐标点串（需解压） |
| steps | array | 路线引导步骤 |
| steps[].accessorial_desc | string | 辅助描述信息 |
| taxi_fare | object | 预估打车费 |
| restriction | object | 限行信息（status: 0=不限行, 1=限行） |

---

## 步行路线规划

**接口**: `GET /ws/direction/v1/walking/`

**请求参数**:
- `key` (必填): 开发密钥
- `from` (必填): 起点坐标，格式 `纬度,经度`
- `to` (必填): 终点坐标，格式 `纬度,经度`

**响应格式**: 同驾车路线规划，包含 `routes[].distance`（米）、`duration`（分钟）、`direction`（总体方向）、`polyline`（压缩格式）、`steps[]`（含 `type`/`road_class` 字段），但无 `taxi_fare`、`restriction`、`traffic_light_count`、`toll` 等驾车特有字段。

---

## 骑行路线规划

**接口**: `GET /ws/direction/v1/bicycling/`

**请求参数**:
- `key` (必填): 开发密钥
- `from` (必填): 起点坐标，格式 `纬度,经度`
- `to` (必填): 终点坐标，格式 `纬度,经度`

**响应格式**: 同步行路线规划，包含 `routes[].distance`（米）、`duration`（分钟）、`polyline`、`steps[]`。

---

## 电动车路线规划

**接口**: `GET /ws/direction/v1/ebicycling/`

**请求参数**:
- `key` (必填): 开发密钥
- `from` (必填): 起点坐标，格式 `纬度,经度`
- `to` (必填): 终点坐标，格式 `纬度,经度`

**响应格式**: 同步行路线规划，包含 `routes[].distance`（米）、`duration`（分钟）、`polyline`、`steps[]`。

---

## 公交路线规划

**接口**: `GET /ws/direction/v1/transit/`

**请求参数**:
- `key` (必填): 开发密钥
- `from` (必填): 起点坐标，格式 `纬度,经度`
- `to` (必填): 终点坐标，格式 `纬度,经度`
- `policy` (可选): 路线策略
  - `LEAST_TIME` — 时间短（默认）
  - `LEAST_TRANSFER` — 少换乘
  - `LEAST_WALKING` — 少步行
  - `LEAST_PRICE` — 低价格

---

## 批量距离计算（距离矩阵）

批量计算多个起点到多个终点的路面距离和时间。

**接口**: `GET /ws/distance/v1/matrix`

> 也支持 POST 请求（`Content-Type: application/json`）。

**请求参数**:
- `key` (必填): 开发密钥
- `mode` (必填): 计算方式
  - `driving` — 驾车（支持实时 ETA）
  - `walking` — 步行
  - `bicycling` — 骑行
- `from` (必填): 起点坐标串，格式 `lat1,lng1;lat2,lng2`
- `to` (必填): 终点坐标串，格式 `lat1,lng1;lat2,lng2`

> **坐标限制**：一对多计算 ≤200个，多对多 from×to ≤625 且单侧 ≤50个。
> 驾车模式下 from 支持扩展参数：`lat,lng,header,roadtype,speed,accuracy,timestamp`。

**请求示例**:
```
GET /ws/distance/v1/matrix?key=YOUR_KEY&mode=driving&from=39.984154,116.307490&to=39.904989,116.405285;39.912345,116.387654
```

**响应格式**:
```json
{
  "status": 0,
  "message": "Success",
  "result": {
    "rows": [
      {
        "elements": [
          {"distance": 18169, "duration": 2221},
          {"distance": 16665, "duration": 2833}
        ]
      }
    ]
  }
}
```

**距离矩阵字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| distance | number | 起点到终点的距离（米） |
| duration | number | 预估时间（**秒**，含路况） |
| status | number | 本对起终点计算状态（4=附近无路，此时 distance 为直线距离） |

> **注意**：距离矩阵的 `duration` 单位是**秒**，而路线规划的 `duration` 单位是**分钟**，两者不同。
