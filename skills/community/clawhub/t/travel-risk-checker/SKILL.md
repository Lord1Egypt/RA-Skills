---
name: travel-risk-checker
version: 0.1.0
description: 旅行交通风险检查助手，提供转机风险评估、延误酒店推荐、最后一公里交通检查三大核心功能
---

# 参数获取

获取以下参数：

- `$ARGUMENTS`: 用户原始输入
- `$ORDER_DATA`: 交通订单数据（如有）
- `$USER_LOCATION`: 用户当前位置（如有）

# 核心功能

基于用户输入或订单数据，提供以下三大核心服务：

## 1. 极限转机风险检查

**触发条件：** 用户输入航班信息或检测到联程航班订单

**检查内容：**
- 转机时间是否充足
- 是否需要重新托运行李
- 是否需要入境再出境
- 是否需要更换航站楼
- 机场平均转机耗时
- 赶不上概率评估

**输出格式：**
```
【转机风险评估】
转机机场：{机场名称}
航站楼：{T1 → T2}
转机时间：{用户时间}
平均耗时：{机场平均时间}
风险项：
  - 需重新安检 ✓
  - 需入境再出境 ✓
  - 航站楼不同 ✓
错过概率：{XX}%
建议：{改签/提前到达/快速通道}
```

**示例：**
```
【转机风险评估】
转机机场：香港国际机场 (HKG)
航站楼：T1 → T1
转机时间：1 小时 10 分钟
平均耗时：65 分钟
风险项：
  - 需重新安检 ✓
  - 需入境再出境 ✗
  - 航站楼不同 ✗
错过概率：35%
建议：建议改签至 2 小时以上转机时间，或购买快速安检服务
```

## 2. 航班延误酒店保命助手

**触发条件：** 检测到航班延误 > 2 小时 或 航班取消

**检查内容：**
- 预计到达时间
- 到达地酒店入住政策
- 24 小时前台酒店
- 机场附近酒店（15 分钟车程内）
- 凌晨 check-in 支持

**输出格式：**
```
【延误酒店推荐】
到达时间：{凌晨 HH:MM}
城市：{城市名称}
机场：{机场名称}

可入住酒店：
1. {酒店 A}
   - 距离：{X.X km / X 分钟车程}
   - 前台：24 小时
   - 服务：{机场接送/免费 shuttle}
   - 价格：{¥XXX 起}

2. {酒店 B}
   - 距离：{X.X km / X 分钟车程}
   - 前台：24 小时
   - 服务：{机场接送}
   - 价格：{¥XXX 起}

建议：立即预订，避免深夜无房
```

**示例：**
```
【延误酒店推荐】
到达时间：凌晨 1:40
城市：上海
机场：浦东国际机场 (PVG)

可入住酒店：
1. 机场大酒店
   - 距离：2.3 km / 5 分钟车程
   - 前台：24 小时
   - 服务：免费机场接送
   - 价格：¥458 起

2. 浦东机场宾馆
   - 距离：1.8 km / 4 分钟车程
   - 前台：24 小时
   - 服务：航站楼直达
   - 价格：¥528 起

建议：立即预订，避免深夜无房
```

## 3. 最后一公里交通失效提醒

**触发条件：** 检测到晚间到达交通订单（航班/高铁 22:00 后到达）

**检查内容：**
- 目的地城市地铁末班车时间
- 机场大巴运营时间
- 夜班公交路线
- 打车排队情况
- 替代交通方案

**输出格式：**
```
【交通失效预警】
到达时间：{HH:MM}
到达站点：{站点名称}
城市：{城市名称}

交通状态：
  - 地铁：{已停运/末班车 XX:XX}
  - 机场大巴：{已停运/末班车 XX:XX}
  - 夜班公交：{有/无}
  - 打车排队：{约 X 分钟}

建议：
  - 改为{推荐时间}前到达的车次
  - 或预订接站车（¥XXX 起）
  - 或提前预约网约车
```

**示例：**
```
【交通失效预警】
到达时间：23:10
到达站点：西安北站
城市：西安

交通状态：
  - 地铁：已停运（末班车 23:00）
  - 机场大巴：已停运（末班车 22:30）
  - 夜班公交：无
  - 打车排队：约 60 分钟

建议：
  - 改为 22:00 前到达的车次
  - 或预订接站车（¥120 起）
  - 或提前预约网约车
```

# MCP 集成

## MCP Server 配置

**所需 MCP Servers：**

```yaml
mcpServers:
  travel-data:
    command: npx
    args: ["-y", "@travel/mcp-server"]
    env:
      TRAVEL_API_KEY: "${TRAVEL_API_KEY}"
  
  hotel-booking:
    command: npx
    args: ["-y", "@hotel/mcp-server"]
    env:
      HOTEL_API_KEY: "${HOTEL_API_KEY}"
  
  city-transport:
    command: npx
    args: ["-y", "@city-transport/mcp-server"]
    env:
      TRANSPORT_API_KEY: "${TRANSPORT_API_KEY}"
```

## MCP 工具定义

### 工具 1：flight_transit_risk_check

**用途：** 检查航班转机风险

**参数：**
```json
{
  "type": "object",
  "properties": {
    "flight_no_1": {"type": "string", "description": "第一程航班号"},
    "flight_no_2": {"type": "string", "description": "第二程航班号"},
    "transit_airport": {"type": "string", "description": "转机机场代码"},
    "transit_time_minutes": {"type": "integer", "description": "转机时间（分钟）"},
    "terminal_1": {"type": "string", "description": "第一程航站楼"},
    "terminal_2": {"type": "string", "description": "第二程航站楼"}
  },
  "required": ["flight_no_1", "flight_no_2", "transit_airport", "transit_time_minutes"]
}
```

**返回示例：**
```json
{
  "risk_level": "HIGH",
  "transit_airport": "HKG",
  "terminals": "T1 → T1",
  "avg_transit_time": 65,
  "user_time": 70,
  "miss_probability": 0.35,
  "risk_items": ["security_recheck", "immigration_required"],
  "suggestions": ["建议改签至 2 小时以上转机时间", "购买快速安检服务"]
}
```

### 工具 2：delay_hotel_recommend

**用途：** 推荐延误时可入住的酒店

**参数：**
```json
{
  "type": "object",
  "properties": {
    "airport_code": {"type": "string", "description": "机场代码"},
    "arrival_time": {"type": "string", "description": "预计到达时间 (ISO 8601)"},
    "max_distance_km": {"type": "number", "description": "最大距离（公里）", "default": 10},
    "require_24h_reception": {"type": "boolean", "description": "是否要求 24 小时前台", "default": true},
    "require_airport_shuttle": {"type": "boolean", "description": "是否要求机场接送", "default": true}
  },
  "required": ["airport_code", "arrival_time"]
}
```

**返回示例：**
```json
{
  "hotels": [
    {
      "name": "机场大酒店",
      "distance_km": 2.3,
      "drive_time_minutes": 5,
      "reception_24h": true,
      "airport_shuttle": true,
      "price_from": 458,
      "available_rooms": 3
    }
  ]
}
```

### 工具 3：last_mile_transport_check

**用途：** 检查最后一公里交通可用性

**参数：**
```json
{
  "type": "object",
  "properties": {
    "station_name": {"type": "string", "description": "到达站点名称"},
    "station_type": {"type": "string", "enum": ["airport", "train_station"], "description": "站点类型"},
    "arrival_time": {"type": "string", "description": "预计到达时间 (ISO 8601)"},
    "city_code": {"type": "string", "description": "城市代码"}
  },
  "required": ["station_name", "station_type", "arrival_time", "city_code"]
}
```

**返回示例：**
```json
{
  "metro_status": "CLOSED",
  "metro_last_train": "23:00",
  "airport_bus_status": "CLOSED",
  "airport_bus_last": "22:30",
  "night_bus_available": false,
  "taxi_queue_time": 60,
  "alternatives": [
    {"type": "prebook_car", "price_from": 120},
    {"type": "ride_hailing", "estimated_time": 15}
  ]
}
```

## 数据源接入

**必须结合以下数据：**

| 数据类型 | 用途 | 触发条件 | MCP 工具 |
|----------|------|----------|----------|
| 交通订单 | 获取航班/车次信息 | 用户授权访问订单 | `travel-data.get_order` |
| 目的地城市 | 查询当地交通政策 | 订单中包含目的地 | `city-transport.get_city_info` |
| 到达时间 | 判断是否深夜到达 | 订单中包含时间 | `travel-data.get_order` |
| 实时延误 | 检测航班延误状态 | 航班起飞前 2 小时 | `travel-data.get_flight_status` |
| 酒店数据 | 推荐可入住酒店 | 延误 > 2 小时 | `hotel-booking.search_hotels` |
| 交通时刻表 | 检查末班车时间 | 到达时间 > 22:00 | `city-transport.get_schedule` |

## 自动触发规则

**规则 1：转机风险检查**
```
IF 订单类型 == "联程航班"
   AND 转机时间 < 90 分钟
THEN 触发转机风险评估
```

**规则 2：延误酒店推荐**
```
IF 航班状态 == "延误"
   AND 延误时间 > 120 分钟
   AND 到达时间 > 23:00
THEN 触发酒店推荐
```

**规则 3：最后一公里检查**
```
IF 到达时间 > 22:00
   AND 交通方式 IN ["高铁", "飞机"]
THEN 触发交通失效检查
```

## 输出渠道

- **订单详情页**：在订单确认前展示风险提示
- **推送通知**：航班延误时主动推送
- **短信/邮件**：深夜到达前发送交通提醒
- **App 首页**：行程卡片展示风险状态

# 风险等级定义

## 转机风险等级

**错过概率计算公式：**
```
miss_probability = base_risk × terminal_factor × immigration_factor × security_factor × time_factor

其中：
- base_risk = 0.1（基础风险）
- terminal_factor = 1.5（同航站楼）或 2.5（不同航站楼）
- immigration_factor = 1.0（无需入境）或 2.0（需入境）
- security_factor = 1.0（无需安检）或 1.5（需安检）
- time_factor = min(2.0, (90 - user_time_minutes) / 30)
```

| 等级 | 转机时间 | 错过概率 | 建议 |
|------|----------|----------|------|
| 🟢 安全 | > 120 分钟 | < 5% | 正常转机 |
| 🟡 注意 | 90-120 分钟 | 5-15% | 建议快速通道 |
| 🟠 风险 | 60-90 分钟 | 15-35% | 建议改签 |
| 🔴 高危 | < 60 分钟 | > 35% | 强烈建议改签 |

**机场平均转机耗时参考数据：**
```
数据来源：IATA Airport Connection Times

国内转国内：45-60 分钟
国内转国际：60-90 分钟
国际转国际：60-75 分钟
国际转国内：75-120 分钟

重点机场参考：
- 香港 (HKG): 65 分钟
- 东京成田 (NRT): 90 分钟
- 首尔仁川 (ICN): 60 分钟
- 新加坡 (SIN): 55 分钟
- 曼谷 (BKK): 75 分钟
- 吉隆坡 (KUL): 70 分钟
```

## 深夜到达风险等级

| 等级 | 到达时间 | 交通状态 | 建议 |
|------|----------|----------|------|
| 🟢 安全 | < 22:00 | 公共交通正常 | 正常出行 |
| 🟡 注意 | 22:00-23:00 | 部分交通停运 | 建议预约车 |
| 🟠 风险 | 23:00-01:00 | 公共交通停运 | 必须预约车 |
| 🔴 高危 | > 01:00 | 仅出租车可用 | 提前安排住宿 |

**交通可用性判断规则：**
```
IF arrival_time < metro_last_train THEN metro_available = true
ELSE metro_available = false

IF arrival_time < bus_last THEN bus_available = true
ELSE bus_available = false

IF metro_available OR bus_available THEN risk_level = LOW
ELSE IF taxi_queue_time < 30 THEN risk_level = MEDIUM
ELSE risk_level = HIGH
```

# 用户体验优化

## 提示语风格

- **简洁明了**：直接说明问题和解决方案
- **数据支撑**：使用具体数字（时间、概率、距离）
- **行动导向**：提供明确的下一步建议
- **语气友好**：避免制造焦虑，强调"有帮助"

## 交互设计

- **风险可视化**：使用颜色标识风险等级
- **一键操作**：提供"改签"、"预订酒店"、"预约车"快捷入口
- **对比展示**：显示当前方案 vs 推荐方案
- **倒计时提醒**：关键时间节点前主动提醒

# 数据更新频率

| 数据类型 | 更新频率 | 来源 | 缓存策略 |
|----------|----------|------|----------|
| 航班状态 | 实时（5 分钟） | 航司 API / 飞常准 | 不缓存，实时查询 |
| 地铁时刻 | 每日 00:00 | 城市交通数据 | 缓存 24 小时 |
| 酒店房态 | 实时（15 分钟） | 酒店 API / 携程 | 缓存 15 分钟 |
| 打车排队 | 实时（10 分钟） | 网约车 API | 缓存 10 分钟 |
| 机场转机时间 | 每周 | IATA / 机场官方 | 缓存 7 天 |
| 天气数据 | 每小时 | 气象局 API | 缓存 1 小时 |

**降级策略：**
```
IF 实时数据不可用 THEN
  使用缓存数据（如果在有效期内）
ELSE IF 缓存数据过期 THEN
  使用历史平均值
  提示用户"数据可能不准确，建议手动确认"
ELSE
  使用默认安全值
  提示用户"暂时无法获取数据，建议预留更多时间"
```

# 错误处理

**数据不可用时：**
```
抱歉，暂时无法获取{数据名称}
建议您：
1. 联系{相关机构}确认
2. 预留更多缓冲时间
3. 购买可退改签产品
```

**API 调用失败处理：**

| 错误类型 | 处理策略 | 用户提示 |
|----------|----------|----------|
| 超时 | 重试 2 次，使用缓存 | "数据加载中，显示的是最近的数据" |
| 认证失败 | 告警，使用默认值 | "部分功能暂时不可用" |
| 数据为空 | 使用历史平均 | "基于历史数据估算" |
| 服务不可用 | 降级到离线模式 | "已切换到离线模式，建议手动确认" |

**降级策略优先级：**
```
1. 实时 API 数据（首选）
2. 缓存数据（15 分钟内）
3. 历史平均值（同时间段）
4. 行业默认值（安全保守估计）
5. 提示用户手动输入
```

**日志记录：**
```javascript
{
  "timestamp": "2026-04-01T12:00:00Z",
  "user_id": "xxx",
  "check_type": "transit_risk",
  "data_source": "realtime",
  "fallback_used": false,
  "response_time_ms": 234,
  "risk_level": "HIGH"
}
```

# 隐私保护

- 订单数据仅用于风险评估
- 不存储用户行程历史
- 不向第三方分享位置信息
- 用户可随时关闭风险检查功能
