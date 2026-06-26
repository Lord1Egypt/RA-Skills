# WittIoT Weather Station – API Specification

## Base URL

```
https://wittiot.com
```

## Authentication

- **API Key**：请求头 `X-API-Key: witt_sk_xxxx`
- API Key 在 https://wittiot.com/index/apikey 创建
- 公开端点（Shortcode 查询）无需认证

---

## 1. 列出我的设备

- **Method:** GET
- **Path:** `/api/v1.Device/index`
- **Auth:** 必须
- **Response JSON (example):**

```json
{
  "code": 200,
  "msg": "ok",
  "data": [
    {
      "id": 1,
      "name": "Backyard Station",
      "model": "WS6900",
      "sn": "WS6900-000001",
      "online": true,
      "visibility": "public"
    },
    {
      "id": 2,
      "name": "Rooftop Station",
      "model": "WS3900",
      "sn": "WS3900-000002",
      "online": false,
      "visibility": "private"
    }
  ]
}
```

**Devices path:** `data`
**Device fields:** `id`, `name`, `model`, `sn`, `online`, `visibility`

---

## 2. 获取实时传感器数据

- **Method:** GET
- **Path:** `/api/v1.Realtime/index`
- **Auth:** 必须（如需访问私有设备）；`?scope=public` 时无需认证但设备须为公开
- **Params:**
  - `id` (int, required) — 设备 ID
  - `scope` (string, optional) — `public`：公开数据，不需要认证
- **Response JSON (example):**

```json
{
  "code": 200,
  "msg": "ok",
  "data": {
    "device_id": 1,
    "device_name": "Backyard Station",
    "online": true,
    "data": {
      "temperature": 23.5,
      "humidity": 68.2,
      "pressure": 1013.2,
      "light": 45.3,
      "wind_speed": 3.2,
      "wind_gust": 5.1,
      "wind_direction": 270,
      "rainfall": 0.0
    }
  }
}
```

**Data path:** `data.data`
**Online path:** `data.online`
**Device name path:** `data.device_name`

传感器字段说明：

| 字段 | 单位 | 说明 |
|------|------|------|
| `temperature` | °C | 温度 |
| `humidity` | %RH | 相对湿度 |
| `pressure` | hPa | 气压 |
| `light` | Klux | 光照强度 |
| `wind_speed` | m/s | 风速 |
| `wind_gust` | m/s | 阵风风速 |
| `wind_direction` | ° | 风向（0=北，90=东，180=南，270=西） |
| `rainfall` | mm | 降雨量 |

---

## 3. 获取历史数据

- **Method:** GET
- **Path:** `/api/v1.History/index`
- **Auth:** 必须
- **Params:**
  - `id` (int, required) — 设备 ID
  - `range` (string) — `24h` / `7d` / `30d`（默认 `24h`）
  - `type` (string) — `minute` / `daily` / `cmd`
- **Response JSON (example):**

```json
{
  "code": 200,
  "msg": "ok",
  "data": [
    {
      "timestamp": 1743000000,
      "temperature": 22.1,
      "humidity": 65.0,
      "pressure": 1012.8
    }
  ]
}
```

---

## 4. 通过短码查询设备信息（公开，无需认证）

- **Method:** GET
- **Path:** `/api/v1.Shortcode/read`
- **Auth:** 无需
- **Params:**
  - `code` (string, required) — 6字符短码（印在设备标签上）
- **Response JSON (example):**

```json
{
  "code": 200,
  "msg": "ok",
  "data": {
    "device": {
      "id": 1,
      "name": "Backyard Station",
      "model": "WS6900",
      "visibility": "public"
    },
    "online": true
  }
}
```

---

## 5. 通过短码获取公开实时数据（公开，无需认证）

- **Method:** GET
- **Path:** `/api/v1.Shortcode/data`
- **Auth:** 无需
- **Params:**
  - `code` (string, required) — 6字符短码
- **Response JSON (example):**

```json
{
  "code": 200,
  "msg": "ok",
  "data": {
    "online": true,
    "data": {
      "temperature": 23.5,
      "humidity": 68.2,
      "pressure": 1013.2,
      "wind_speed": 3.2,
      "rainfall": 0.0
    }
  }
}
```

---

## 错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 参数错误 |
| 401 | 未认证或 API Key 无效 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 409 | 冲突（如设备已绑定） |
