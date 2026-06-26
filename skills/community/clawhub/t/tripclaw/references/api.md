# TripClaw API 参考

## 基础信息

- **Base URL**: `https://api.tripclaws.com`
- **认证方式**: API Key (Header)
- **Content-Type**: `application/json`

## 认证

所有请求需要在 Header 中携带 API Key：

```
Authorization: Bearer <YOUR_API_KEY>
```

## 端点

### 导入行程

**POST** `/v1/trips/import`

导入一个新的自驾行程到用户账户。

#### 请求体

```json
{
  "name": "云南自驾之旅",
  "description": "从昆明出发，途经大理、丽江，最后抵达香格里拉",
  "startDate": "2024-01-15",
  "endDate": "2024-01-22",
  "travelers": 2,
  "waypoints": [
    {
      "order": 1,
      "name": "昆明",
      "type": "start",
      "location": {
        "address": "昆明市，云南省",
        "coordinates": {
          "lat": 25.0389,
          "lng": 102.7183
        }
      },
      "arrivalDate": "2024-01-15",
      "stay": {
        "accommodation": "昆明云上四季酒店",
        "nights": 1,
        "bookingUrl": "https://example.com/booking/123"
      }
    },
    {
      "order": 2,
      "name": "大理",
      "type": "waypoint",
      "location": {
        "address": "大理古城，大理白族自治州",
        "coordinates": {
          "lat": 25.6872,
          "lng": 100.1815
        }
      },
      "arrivalDate": "2024-01-16",
      "stay": {
        "accommodation": "大理古城客栈",
        "nights": 2,
        "bookingUrl": null
      }
    },
    {
      "order": 3,
      "name": "丽江",
      "type": "waypoint",
      "location": {
        "address": "丽江古城，丽江市",
        "coordinates": {
          "lat": 26.8721,
          "lng": 100.2255
        }
      },
      "arrivalDate": "2024-01-18",
      "stay": {
        "accommodation": "丽江束河古镇民宿",
        "nights": 2,
        "bookingUrl": null
      }
    },
    {
      "order": 4,
      "name": "香格里拉",
      "type": "destination",
      "location": {
        "address": "香格里拉市，迪庆藏族自治州",
        "coordinates": {
          "lat": 27.8186,
          "lng": 99.7035
        }
      },
      "arrivalDate": "2024-01-20",
      "stay": {
        "accommodation": "香格里拉松赞林卡酒店",
        "nights": 2,
        "bookingUrl": null
      }
    }
  ],
  "activities": [
    {
      "date": "2024-01-16",
      "name": "洱海骑行",
      "description": "环洱海骑行，欣赏苍山洱海美景",
      "location": {
        "address": "洱海环湖路，大理市",
        "coordinates": {
          "lat": 25.7125,
          "lng": 100.1652
        }
      },
      "duration": "3小时",
      "cost": 150
    },
    {
      "date": "2024-01-17",
      "name": "大理古城游览",
      "description": "漫步大理古城，体验白族文化",
      "location": {
        "address": "大理古城，大理市",
        "coordinates": {
          "lat": 25.6872,
          "lng": 100.1815
        }
      },
      "duration": "4小时",
      "cost": 0
    },
    {
      "date": "2024-01-19",
      "name": "玉龙雪山",
      "description": "乘坐索道登上玉龙雪山，欣赏雪山美景",
      "location": {
        "address": "玉龙雪山景区，丽江市",
        "coordinates": {
          "lat": 27.1041,
          "lng": 100.1825
        }
      },
      "duration": "全天",
      "cost": 450
    },
    {
      "date": "2024-01-21",
      "name": "普达措国家公园",
      "description": "游览高原湖泊和原始森林",
      "location": {
        "address": "普达措国家公园，香格里拉市",
        "coordinates": {
          "lat": 27.8456,
          "lng": 99.9512
        }
      },
      "duration": "全天",
      "cost": 258
    }
  ],
  "budget": {
    "total": 15000,
    "currency": "CNY"
  }
}
```

#### 成功响应 (201)

```json
{
  "success": true,
  "data": {
    "tripId": "trip_abc123xyz",
    "name": "云南自驾之旅",
    "importedAt": "2024-01-10T15:30:00Z",
    "waypointCount": 4,
    "activityCount": 4,
    "deepLink": "tripclaw://trip/trip_abc123xyz",
    "shareUrl": "https://tripclaw.com/trip/trip_abc123xyz"
  }
}
```

#### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": " waypoints 数组不能为空",
    "details": [
      {
        "field": "waypoints",
        "message": "至少需要一个途经点"
      }
    ]
  }
}
```

### 获取行程列表

**GET** `/v1/trips`

获取当前用户的所有行程。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认 1 |
| limit | int | 每页数量，默认 20，最大 100 |
| status | string | 筛选状态：planning/ongoing/completed |

#### 成功响应 (200)

```json
{
  "success": true,
  "data": {
    "trips": [
      {
        "tripId": "trip_abc123",
        "name": "云南自驾之旅",
        "startDate": "2024-01-15",
        "endDate": "2024-01-22",
        "status": "planning",
        "waypointCount": 4
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 1,
      "totalPages": 1
    }
  }
}
```

### 获取行程详情

**GET** `/v1/trips/{tripId}`

获取指定行程的完整信息。

#### 成功响应 (200)

返回完整的行程对象，包含所有 waypoints 和 activities。

### 更新行程

**PATCH** `/v1/trips/{tripId}`

部分更新行程信息。

#### 请求体

只需传入要更新的字段：

```json
{
  "name": "云南深度自驾游",
  "budget": {
    "total": 18000,
    "currency": "CNY"
  }
}
```

### 删除行程

**DELETE** `/v1/trips/{tripId}`

删除指定行程。

#### 成功响应 (200)

```json
{
  "success": true,
  "message": "行程已删除"
}
```

## 错误码说明

| HTTP 状态码 | 错误码 | 说明 |
|------------|--------|------|
| 400 | VALIDATION_ERROR | 请求数据格式错误 |
| 401 | UNAUTHORIZED | API Key 无效或过期 |
| 403 | FORBIDDEN | 无权限访问该资源 |
| 404 | NOT_FOUND | 资源不存在 |
| 409 | CONFLICT | 资源冲突（如重复导入） |
| 429 | RATE_LIMITED | 请求过于频繁 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

## 请求限制

- 每分钟最多 60 次请求
- 每天最多 1000 次请求
- 单次导入的 waypoints 最多 50 个
- 单次导入的 activities 最多 100 个

## Webhook（可选）

TripClaw 支持通过 Webhook 推送行程变更通知。可在 TripClaw 应用设置中配置。