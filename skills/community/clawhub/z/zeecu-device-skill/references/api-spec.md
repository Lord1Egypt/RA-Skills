# 极酷电动车查询 API 规格文档

## Base URL

```
https://cn-hangzhou-mgs-gw.cloud.alipay.com/mgw.htm
```

## 认证方式

- API Key 以 `sk_live_` 开头，通过请求体 `_requestBody` 中的 `apiKey` 字段传递
- 环境变量 `API_KEY` 或 `config.json` 中配置

## mPaaS MGS 网关请求格式

所有请求必须携带以下 Header：

| Header | 值 | 说明 |
|--------|-----|------|
| `Content-Type` | `application/json` | 请求体格式 |
| `workspaceId` | `prod` | 工作空间 |
| `AppId` | `ALIPUB3C84031111512` | 应用标识 |
| `Operation-Type` | 见各接口 | 操作类型，标识具体接口 |

**请求体格式**：mPaaS MGS 网关要求请求体为数组，业务参数包裹在 `_requestBody` 中：

```json
[
  {
    "_requestBody": {
      "业务参数key": "业务参数value"
    }
  }
]
```

## 通用响应格式

```json
{
  "success": true,
  "resultCode": "SUCCESS",
  "resultMessage": "处理成功",
  "data": { ... }
}
```

### 错误码

| resultCode | resultMessage | 说明 |
|------------|---------------|------|
| `API_KEY_INVALID` | API Key无效或已撤销 | API Key 不存在或已撤销 |
| `API_KEY_NOT_EXIST` | API Key不存在 | 用户未生成 API Key |
| `DEVICE_NOT_BOUND` | 用户未绑定车辆 | 用户没有绑定的车辆 |
| `DEVICE_NOT_BELONG_USER` | 车辆不属于该用户 | 查询的车辆不属于当前 API Key 绑定的用户 |
| `QUERY_TIME_RANGE_EXCEEDED` | 查询时间范围超过30天，请缩短查询时间范围 | 轨迹查询时间范围超限 |
| `QUERY_RESULT_LIMIT_EXCEEDED` | 查询结果超过100条，请缩短查询时间范围 | 轨迹查询结果数量超限 |

---

## 接口列表

### 1. 查询车辆列表

查询 API Key 绑定用户的所有车辆信息。

- **Method:** POST
- **Operation-Type:** `com.alipay.ekytsaas.skill.device.list`

**请求：**

```
POST /mgw.htm
Headers:
  Content-Type: application/json
  workspaceId: prod
  AppId: ALIPUB3C84031111512
  Operation-Type: com.alipay.ekytsaas.skill.device.list

Body:
[
  {
    "_requestBody": {
      "apiKey": "sk_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    }
  }
]
```

**响应：**

```json
{
  "success": true,
  "resultCode": "SUCCESS",
  "resultMessage": "处理成功",
  "data": [
    {
      "tuid": "T123456789",
      "deviceName": null,
      "model": "XX-200",
      "color": "珍珠白",
      "frameNo": "VIN123456789012345",
      "barCode": "1234567890123"
    }
  ]
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| tuid | String | 车辆中控号，唯一标识一辆车 |
| deviceName | String | 设备名称（可能为空） |
| model | String | 车型型号 |
| color | String | 车辆颜色 |
| frameNo | String | 车架号/VIN |
| barCode | String | 条码号（可能为空） |

---

### 2. 查询车辆实时数据

查询指定车辆的实时状态信息。

- **Method:** POST
- **Operation-Type:** `com.alipay.ekytsaas.skill.device.query`

**请求：**

```
POST /mgw.htm
Headers:
  Content-Type: application/json
  workspaceId: prod
  AppId: ALIPUB3C84031111512
  Operation-Type: com.alipay.ekytsaas.skill.device.query

Body:
[
  {
    "_requestBody": {
      "apiKey": "sk_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
      "tuid": "T123456789"
    }
  }
]
```

**响应：**

```json
{
  "success": true,
  "resultCode": "SUCCESS",
  "resultMessage": "处理成功",
  "data": {
    "tuid": "T123456789",
    "location": "120.123456,30.123456",
    "locationAddress": "浙江省杭州市西湖区xxx路xxx号",
    "runningStatus": "在线",
    "speed": "0",
    "powerStatus": "OFF",
    "rsrp": "-75",
    "locss": "12",
    "totalMileage": 1234.5,
    "lastLocationTime": "1713849600000",
    "batteryLevel": "85",
    "enduranceMileage": "45.2"
  }
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| tuid | String | 车辆中控号 |
| location | String | 经纬度，格式：`经度,纬度` |
| locationAddress | String | 位置地址描述 |
| runningStatus | String | 在线状态（在线/离线） |
| speed | String | 当前速度（km/h） |
| powerStatus | String | 电源状态（ON/OFF） |
| rsrp | String | 信号强度（dBm） |
| locss | String | 定位卫星数 |
| totalMileage | Double | 总里程（km） |
| lastLocationTime | String | 最后定位时间（时间戳毫秒） |
| batteryLevel | String | 当前电量百分比（如 "85"），Skynet渠道可能为null |
| enduranceMileage | String | 续航里程（km），Skynet渠道可能为null |

---

### 3. 查询历史轨迹

查询指定车辆在某一时间段内的骑行行程列表。

- **Method:** POST
- **Operation-Type:** `com.alipay.ekytsaas.skill.device.tripList`

**请求：**

```
POST /mgw.htm
Headers:
  Content-Type: application/json
  workspaceId: prod
  AppId: ALIPUB3C84031111512
  Operation-Type: com.alipay.ekytsaas.skill.device.tripList

Body:
[
  {
    "_requestBody": {
      "apiKey": "sk_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
      "tuid": "T123456789",
      "startTime": 1713849600000,
      "endTime": 1714454400000
    }
  }
]
```

**请求参数：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| apiKey | String | 是 | API Key |
| tuid | String | 是 | 车辆中控号 |
| startTime | Long | 是 | 查询开始时间（毫秒时间戳） |
| endTime | Long | 是 | 查询结束时间（毫秒时间戳） |

**约束：**
- 时间范围不得超过 30 天
- 查询结果最多返回 100 条行程
- API 按天查询最佳：传入每天的起始时间（当天 00:00:00.000 毫秒时间戳）作为 `startTime`
- 默认查询最近 7 天轨迹，按天拆分后并发请求

**响应：**

```json
{
  "success": true,
  "resultCode": "SUCCESS",
  "resultMessage": "处理成功",
  "data": {
    "trips": [
      {
        "tripId": "trip_7cb1cc64f0d949d8bcb969370884fe6e",
        "startTime": 1782208290452,
        "endTime": 1782208298492,
        "mileage": "50.0",
        "durationValue": "0.1",
        "durationUnit": "min",
        "avgSpeed": "30.0",
        "maxSpeed": "30.0",
        "firstAddress": "上海市黄浦区南京东路街道延安高架路凯迪拉克·上海音乐厅",
        "lastAddress": "上海市黄浦区外滩街道河南中路南京商务楼"
      }
    ],
    "totalCount": 1
  }
}
```

**行程字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| tripId | String | 行程ID |
| startTime | Long | 行程开始时间（毫秒时间戳） |
| endTime | Long | 行程结束时间（毫秒时间戳） |
| mileage | String | 行程里程（km，如 "50.0" 表示 50 公里） |
| durationValue | String | 行程时长数值（如 "0.1"） |
| durationUnit | String | 行程时长单位（如 "min"、"h"） |
| avgSpeed | String | 平均速度（km/h） |
| maxSpeed | String | 最高速度（km/h） |
| firstAddress | String | 起始地址 |
| lastAddress | String | 结束地址 |
