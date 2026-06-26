# 车辆控制协议

## 目录

- [协议概述](#协议概述)
- [指令格式](#指令格式)
- [基础控制指令](#基础控制指令)
- [方向控制指令](#方向控制指令)
- [状态查询指令](#状态查询指令)
- [响应格式](#响应格式)
- [错误码定义](#错误码定义)

## 协议概述

本协议定义了语音车辆控制技能与车辆控制系统之间的通信规范。所有指令采用 JSON 格式，通过标准 API 接口传输。

**基础 URL**：`/api/v1/vehicle`

**通用 Header**：
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer {token}",
  "X-Language": "zh-CN|en-US|..."
}
```

## 指令格式

### 控制指令

```json
{
  "command": "vehicle_control",
  "request_id": "uuid-v4",
  "timestamp": "ISO8601",
  "action": "string",
  "target": "string",
  "parameters": {}
}
```

### 查询指令

```json
{
  "command": "status_query",
  "request_id": "uuid-v4",
  "timestamp": "ISO8601",
  "items": ["string"]
}
```

### 场景指令

```json
{
  "command": "scenario_execute",
  "request_id": "uuid-v4",
  "timestamp": "ISO8601",
  "scenario": "string",
  "options": {}
}
```

## 基础控制指令

### 引擎控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| engine_start | 启动引擎 | all | - |
| engine_stop | 熄火 | all | - |
| engine_status | 引擎状态 | all | - |

### 车门控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| door_lock | 锁门 | all/driver/passenger/rear_left/rear_right/trunk |
| door_unlock | 解锁 | all/driver/passenger/rear_left/rear_right/trunk | - |

### 车窗控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| window_open | 开车窗 | all/driver/passenger/rear_left/rear_right/sunroof | position: open/vent/auto |
| window_close | 关车窗 | all/driver/passenger/rear_left/rear_right/sunroof | - |
| window_set | 设置开度 | all/driver/passenger/rear_left/rear_right/sunroof | level: 0-100 |

### 空调控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| climate_on | 开启空调 | all/front/rear | mode: auto/cool/heat/defrost |
| climate_off | 关闭空调 | all/front/rear | - |
| climate_set | 设置温度 | all/front/rear | temperature: 16-30, unit: C/F |
| climate_fan_set | 设置风速 | all/front/rear | speed: 0-7, direction: face/feet/face_feet/defrost |

### 座椅控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| seat_heat | 座椅加热 | driver/passenger/rear_left/rear_right | level: 0-3 |
| seat_ventilate | 座椅通风 | driver/passenger/rear_left/rear_right | level: 0-3 |
| seat_position_set | 座椅位置 | driver/passenger/rear_left/rear_right | position: {foreaft, height, recline} |

### 后视镜控制

| action | 描述 | target | parameters |
|--------|------|--------|------------|
| mirror_fold | 后视镜折叠 | left/right/both | - |
| mirror_unfold | 后视镜展开 | left/right/both | - |
| mirror_adjust | 后视镜调节 | left/right | direction: up/down/left/right |

## 方向控制指令

### 转向灯控制

| action | 描述 | parameters |
|--------|------|------------|
| turn_signal_left | 左转向灯 | duration: 秒数（默认3） |
| turn_signal_right | 右转向灯 | duration: 秒数（默认3） |
| turn_signal_hazard | 双闪警示灯 | enable: true/false |

### 喇叭控制

| action | 描述 | parameters |
|--------|------|------------|
| horn | 鸣笛 | pattern: short/long/long_short |

### 大灯控制

| action | 描述 | parameters |
|--------|------|------------|
| headlight | 大灯 | mode: off/auto/low_beam/high_beam |
| fog_light | 雾灯 | mode: off/on/front/rear/both |

## 状态查询指令

### 查询项目

| items 值 | 描述 | 返回格式 |
|----------|------|----------|
| fuel_level | 油量 | {value: number, unit: "L"\|"%"} |
| battery_level | 电量 | {value: number, unit: "%"} |
| tire_pressure | 胎压 | {front_left, front_right, rear_left, rear_right, unit: "bar"\|"psi"} |
| door_status | 车门状态 | {driver, passenger, rear_left, rear_right, trunk, trunkglass: "open"\|"closed"\|"ajar"} |
| window_status | 车窗状态 | {driver, passenger, rear_left, rear_right, sunroof: "open"\|"closed"\|"vent", level: 0-100} |
| climate_status | 空调状态 | {on: boolean, temperature, fan_speed, mode} |
| engine_status | 引擎状态 | {running: boolean, rpm, temperature} |
| position | 车辆位置 | {latitude, longitude, address, heading} |
| mileage | 总里程 | {value: number, unit: "km"\|"mi"} |
| speed | 当前时速 | {value: number, unit: "km/h"\|"mph"} |

### 批量查询

```json
{
  "command": "status_query",
  "items": ["fuel_level", "battery_level", "tire_pressure", "door_status"]
}
```

## 响应格式

### 成功响应

```json
{
  "status": "success",
  "request_id": "uuid-v4",
  "timestamp": "ISO8601",
  "data": {}
}
```

### 查询响应

```json
{
  "status": "success",
  "request_id": "uuid-v4",
  "timestamp": "ISO8601",
  "data": {
    "battery_level": {"value": 82, "unit": "%"},
    "fuel_level": {"value": 45, "unit": "L"},
    "tire_pressure": {
      "front_left": 2.3,
      "front_right": 2.3,
      "rear_left": 2.2,
      "rear_right": 2.2,
      "unit": "bar"
    }
  }
}
```

### 批量操作响应

```json
{
  "status": "partial_success",
  "request_id": "uuid-v4",
  "results": [
    {"action": "window_open", "target": "driver", "status": "success"},
    {"action": "window_open", "target": "passenger", "status": "success"},
    {"action": "window_open", "target": "sunroof", "status": "failed", "error": "obstacle_detected"}
  ]
}
```

## 错误码定义

| error_code | 描述 | 说明 |
|------------|------|------|
| vehicle_offline | 车辆离线 | 车辆未联网或信号不佳 |
| command_rejected | 命令被拒 | 车辆拒绝执行（如行驶中） |
| auth_expired | 认证过期 | 需要重新登录 |
| invalid_target | 无效目标 | 指定的 target 不存在 |
| obstacle_detected | 障碍物检测 | 车窗/天窗有障碍物 |
| low_battery | 电量过低 | 无法执行启动等操作 |
| engine_running | 引擎运行中 | 部分操作需熄火后执行 |
| safety_locked | 安全锁定 | 多次错误后临时锁定 |
| network_error | 网络错误 | 请求超时或连接失败 |
| unknown_error | 未知错误 | 其他未分类错误 |
