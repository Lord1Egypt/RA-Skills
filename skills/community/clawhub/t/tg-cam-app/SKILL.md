---
name: tg-cam-app
description: 探鸽摄像头 Skill 服务。用于查询当前 Skill 已绑定设备、查看当前画面、查询事件、查看事件图片、确认设备状态和电量。当用户要查看可操作设备、看某个摄像头当前截图、查询某天或某时段发生了什么、查看最近事件或事件图片、确认在线状态、查询电量时使用。
metadata: {"openclaw":{"requires":{"env":["TIVS_CLI_ID","TIVS_API_KEY"]},"primaryEnv":"TIVS_API_KEY"}}
---

# Webcam App Skill

## 概述

这个 Skill 用于查询当前 Skill 已绑定摄像头的设备信息、当前画面、事件记录、事件图片、在线状态和电量，并在需要时完成拍照等操作。默认返回整理后的结论、摘要和图片，不直接回传长段原始接口响应。

- 可以做的事：查看设备列表、拍一张当前画面、查询事件、查看事件图片、确认在线状态、查询电量
- 典型触发：用户说“看看有哪些设备”“帮我看下门口摄像头现在画面”“今天发生了什么”“最近一次事件是什么”“这条事件的图片给我看看”“设备在线吗”“查下电量”
- 默认输出：整理后的结论、摘要和图片，不把长段原始 JSON 直接甩给用户

## 使用规则

### 基础规则

- 所有请求都使用 `https://skill.webcamapp.cc` 作为唯一 API Base URL。
- 环境变量：
  - `TIVS_CLI_ID`：摄像头 Skill 服务分配的 `cli_id`
  - `TIVS_API_KEY`：摄像头 Skill 服务分配的 `cli_api_key`
- 所有请求都带上以下请求头：

```http
X-Client-ID: $TIVS_CLI_ID
X-Api-Key: $TIVS_API_KEY
X-Skill-Version: 0.0.3
Content-Type: application/json
```

- 缺少 `TIVS_CLI_ID` 或 `TIVS_API_KEY` 时，提醒用户到摄像头 APP 内获取当前 Skill 的凭据，不要伪造请求
- 不要在聊天内容中回显 `TIVS_API_KEY` 的真实值
- 除非接口明确是 `GET` 且无请求体，否则默认按 JSON 请求发送
- 统一按 Header 方式调用

### 授权配置

如果会话中收到 `TIVS_CLI_ID` 和 `TIVS_API_KEY`，请将其写入 `openclaw.json`：

```json
{
  "skills": {
    "entries": {
      "tg-cam-app": {
        "env": {
          "TIVS_CLI_ID": "{TIVS_CLI_ID}",
          "TIVS_API_KEY": "{TIVS_API_KEY}"
        }
      }
    }
  }
}
```

### 结果读取

成功或失败都使用统一响应信封：

```json
{
  "requestId": "req_xxx",
  "code": "ok",
  "msg": "ok",
  "data": {}
}
```

- 读取结果时优先关注 `data`
- 只解释已经确认的字段，不要给未知字段强行编含义
- 默认把接口结果整理成用户能直接理解的答案，不输出长段原始 JSON

### 图片处理

- 图片 URL 可能带签名参数；需要访问时必须使用完整 URL，不要截断。
- 默认不要把原始图片 URL 直接发给用户；优先获取图片内容后再展示。

### 调用约束

- Query 参数统一使用 `snake_case`，例如 `device_id`、`start_time`、`event_id`
- 截图接口请求体使用 `camelCase`，字段名固定为 `deviceId`
- 响应字段通常是 `camelCase`，以实际返回为准
- 不要臆造不存在的接口路径，也不要把 `devices` 和 `device` 写混
- 如果用户按设备名、备注名或位置描述来操作，先查询设备列表确认目标设备
- `event_id` 必须使用系统已经返回过的值，不要自己拼
- 看到“实时画面”“拍一张”“截个图”时，将其理解为获取一张当前截图，不是实时视频流

## APP链接生成

### 实时视频

- 标题：`摄像头实时视频`
- 模板：`myapp://pages/live?deviceId={deviceId}`
- 已确认 `deviceId` 后，输出：`[摄像头实时视频](myapp://pages/live?deviceId={deviceId})`

### 回放视频

- 标题：`回放视频`
- 模板：`myapp://pages/replay?deviceId={deviceId}&startTime={unixTimestampSeconds}`
- 已确认 `deviceId` 和事件时间后，输出：`[回放视频](myapp://pages/replay?deviceId={deviceId}&startTime={unixTimestampSeconds})`
- `startTime` 单位固定为 Unix 秒时间戳

### 事件详情

- 标题：`事件详情`
- 模板：`myapp://pages/event-detail?id={eventId}`
- 已确认 `eventId` 后，输出：`[事件详情](myapp://pages/event-detail?id={eventId})`

## 调用指南

### 快速路由

| 用户意图 | 优先调用 | 前置动作 | 回答重点 |
|------|------|------|------|
| 查看设备列表或指定设备 | `GET /api/v1/skill/devices` | 无 | 设备清单或指定设备信息 |
| 按设备名找目标设备 | `GET /api/v1/skill/devices` | 用结果确认 `deviceId` | 设备匹配结果 |
| 看某个设备当前画面 | `POST /api/v1/skill/device/snapshot` | 先确认 `deviceId` | 截图和简短说明 |
| 查某天或某时段事件 | `GET /api/v1/skill/device/events` | 先确认 `device_id`，再补时间范围 | 事件列表或摘要 |
| 看最近一个事件 | `GET /api/v1/skill/device/events/latest` | 先确认 `device_id` | 单条事件摘要和图片 |
| 看某条事件图片 | `GET /api/v1/skill/device/events/image` | 需要已有 `event_id` | 图片和简短事件信息 |
| 查设备在线状态 | `GET /api/v1/skill/device/online` | 先确认 `device_id` | 是否在线 |
| 查设备电量 | `GET /api/v1/skill/device/battery` | 先确认 `device_id` | 电量结果 |

### 通用流程

1. 设备不明确时，先查设备列表，不要直接猜 `deviceId`。
2. 命中多个设备时，先向用户澄清，不要替用户随意选择。
3. 用户说“今天”“昨天”“最近一段时间”时，先换成明确的日期或时间范围，再发请求。
4. 事件类查询默认返回整理后的摘要；用户明确要列表时，再按时间顺序列出重点事件。
5. 图片可用时优先展示图片，同时补一句简短说明；图片不可用时，明确说明并保留事件摘要。
6. 结果为空时直接说明“当前没有查到”，不要臆造原因或补不存在的数据。

### 常见场景

以下示例用于帮助快速选路。

- 用户想看当前有哪些设备：
  1. 调用 `GET /api/v1/skill/devices`
  2. 整理成可读的设备清单，优先给出设备名、设备 ID、是否在线等关键信息

- 用户想看某个设备当前画面：
  1. 先确认 `deviceId`
  2. 调用 `POST /api/v1/skill/device/snapshot`
  3. 返回截图结果和简短说明
  4. 按“APP链接生成 > 实时视频”规则，追加实时视频链接

- 用户想知道今天发生了什么：
  1. 先确认 `device_id`
  2. 将“今天”换成明确时间范围
  3. 调用 `GET /api/v1/skill/device/events`
  4. 按时间整理事件，并给出简短总结
  5. 生成事件列表时，同时按“APP链接生成 > 事件详情”规则为每条事件附上事件详情链接

- 用户想看下午有没有快递来：
  1. 先确认 `device_id`
  2. 将“下午”换成明确时间范围
  3. 调用 `GET /api/v1/skill/device/events`
  4. 优先关注 `body`、`ai_summary`，先看 `detailDescription`，需要时再查看事件图片
  5. 生成事件列表时，同时按“APP链接生成 > 事件详情”规则为每条事件附上事件详情链接

- 用户想看最近一个事件：
  1. 先确认 `device_id`
  2. 调用 `GET /api/v1/skill/device/events/latest`
  3. 返回事件摘要；有图片时一并展示
  4. 用户想播放该事件视频时，按“APP链接生成 > 回放视频”规则追加回放视频链接；其中 `startTime` 使用事件时间的 Unix 秒时间戳
  5. 需要事件详情时，按“APP链接生成 > 事件详情”规则追加事件详情链接

- 用户想播放一个事件视频：
  1. 先确认对应事件，至少拿到 `deviceId` 和事件时间 `time`
  2. 按“APP链接生成 > 回放视频”规则生成回放视频链接

- 用户想查询设备电量：
  1. 先确认 `device_id`
  2. 调用 `GET /api/v1/skill/device/battery`
  3. 直接解释电量结果，不输出原始结构

- 用户想看多个设备某一天发生了什么：
  1. 先调用 `GET /api/v1/skill/devices` 确认目标设备，并解析出多个 `device_id`
  2. 将目标日期换成明确时间范围
  3. 对每个设备分别调用 `GET /api/v1/skill/device/events`
  4. 先按设备整理事件，再给出跨设备总结

- 用户想看某个设备最近几天发生了什么：
  1. 先确认 `device_id`
  2. 将“最近几天”换成明确日期范围，总跨度不要超过 7 天
  3. 按单日时间范围多次调用 `GET /api/v1/skill/device/events`
  4. 先按日期总结，再给出跨天结论

## 接口说明

### 1. 查询设备列表

```http
GET /api/v1/skill/devices
```

- 用途：查询当前 Skill 可操作的设备；传入 `device_id` 时返回指定设备信息
- Query：
  - `device_id`：可选；传入后仅返回该设备，不存在或无权限时 `items` 为空
- 返回要点：
  - `data.items[].deviceId`：设备ID
  - `data.items[].deviceName`：设备名称
  - `data.items[].isOwner`：设备归属；`true` 为本人设备，`false` 为共享设备
  - `data.items[].connectWay`：联网方式
  - `data.items[].extend.bindTime`：绑定时间
- 注意：如果用户按设备名操作，先用这一步确认目标设备；查电量前可先看 `data.items[].attrs.power` 是否有 `battery`

### 2. 查询设备在线状态

```http
GET /api/v1/skill/device/online
```

- 用途：判断设备当前是否在线、是否可用
- Query：
  - `device_id`：必填
- 返回要点：
  - `data.deviceId`
  - `data.isOnline`
- 注意：按接口实际返回直接解释即可

### 3. 查询设备当前画面

```http
POST /api/v1/skill/device/snapshot
```

- 用途：查询设备当前截图，适合“拍一张”“看当前画面”“帮我截个图”

请求体示例：

```json
{
  "deviceId": "678A7QP6Q5WD"
}
```

- Body：
  - `deviceId`：必填
- 返回要点：
  - `data.deviceId`
  - `data.status`
  - `data.imageUrl`
- 注意：
  - 请求体字段必须写成 `deviceId`
  - 这是截图，不是实时视频流
  - 该接口不是直接读取现成图片，而是由服务器先给设备下发截图指令，再等待设备上传图片，通常会有约 3 秒等待时间
  - 截图会产生一定存储和流量成本，不要频繁调用

### 4. 查询设备某天或某时间段事件

```http
GET /api/v1/skill/device/events
```

- 用途：查询某一天或某个时间段内发生了什么，也可按标签过滤
- Query：
  - `device_id`：必填
  - `start_time`：可选，Unix 秒时间戳
  - `end_time`：可选，Unix 秒时间戳
  - `tag`：可选，可重复传多个
  - `limit`：可选，整数，需大于等于 `0`
  - `offset`：可选，整数，需大于等于 `0`
- 返回要点：
  - `data.items[].id`
  - `data.items[].tag`
  - `data.items[].time`
  - `data.items[].deviceId`
  - `data.items[].detailDescription`
- `tag` 说明：
  - `tag` 是事件的分类标识，用于表示事件所属分类；`tag` / `tags` 都可用于筛选，重复传多个值表示同时关注多个分类
  - 常见 tag 示例：`motion`（移动）、`sound`（声音）、`body`（人形）、`pet`（宠物）、`livestock`（家畜）、`fire`（火焰）、`guard`（看守异常）、`image_abnormal`（画面异常）、`car`（发现车辆）、`ai_summary`（AI 文字摘要）
  - 实际支持哪些 tag，以接口返回结果为准
- 使用建议：
  - 可结合 `tag` 筛选，并优先阅读 `data.items[].detailDescription`
  - 需要事件图片时，再用返回的 `id` 作为 `event_id` 调用 `GET /api/v1/skill/device/events/image`查询
- 注意：
  - 未传 `start_time` 和 `end_time` 时，默认查询设备时区当天的事件
  - 查时间范围时，建议同时传 `start_time` 和 `end_time`，且需满足 `start_time < end_time`
  - `limit` 和 `offset` 不能是负数

### 5. 查询设备最近一个事件

```http
GET /api/v1/skill/device/events/latest
```

- 用途：查看设备最近一次发生了什么
- Query：
  - `device_id`：必填
  - `start_time`：可选，Unix 秒时间戳
  - `end_time`：可选，Unix 秒时间戳
- 返回要点：
  - `data.id`
  - `data.tag`
  - `data.time`
  - `data.deviceId`
  - `data.detailDescription`
  - `data.imageUrl`
- 注意：这是单条事件，不是事件列表

### 6. 查询设备事件图片

```http
GET /api/v1/skill/device/events/image
```

- 用途：查看某条事件对应的图片
- Query：
  - `event_id`：必填
- 返回要点：
  - `data.id`
  - `data.tag`
  - `data.time`
  - `data.deviceId`
  - `data.imageUrl`
- 注意：`event_id` 请使用系统已经返回过的事件 ID，不要自己拼，例如 `/api/v1/skill/device/events` 返回结果中的 `id`

### 7. 查询设备电量

```http
GET /api/v1/skill/device/battery
```

- 用途：查看设备电量
- Query：
  - `device_id`：必填
- 返回要点：
  - `data.deviceId`
  - `data.batteryPercent`：电量百分比，值为 `0-100`
  - `data.isCharging`：是否正在充电
- 注意：仅当设备 `attrs.power` 有 `battery` 时，才可查询电量；若没有 `battery`，直接说明该设备不支持电量查询

### 补充规则

- 缺少 `deviceId`、`device_id` 或 `event_id` 时，先提示用户补充，或先走上游查询步骤
