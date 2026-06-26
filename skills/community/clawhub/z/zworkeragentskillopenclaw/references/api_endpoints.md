# Zworker HTTP API 接口文档

**基础URL**: `http://localhost:18803`

所有接口均返回JSON格式响应。成功时通常包含 `success: true` 字段，失败时包含 `success: false` 和 `message` 字段说明错误原因。

---

## 任务管理

### 获取任务列表
- **方法**: GET
- **端点**: `/control/getTaskList`
- **参数**:
  - `name` (可选): 任务名称模糊匹配
  - `pageNumber` (可选): 页码，从1开始
  - `limit` (可选): 每页数量
- **响应格式**:
```json
{
  "success": true,
  "tasks": [
    {"id": 1, "name": "任务名称1"},
    {"id": 2, "name": "任务名称2"}
  ],
  "pageNumber": 1,
  "limit": 24,
  "total": 2
}
```
- **说明**: `tasks` 是当前分页的任务列表，`total` 是满足条件的任务总数。

### 执行任务
- **方法**: POST
- **端点**: `/control/runTask`
- **参数**:
  - `id` (可选): 任务ID，与 `name` 至少提供一个
  - `name` (可选): 任务名称，与 `id` 至少提供一个
- **响应格式**:
```json
// 成功
{"success": true}
// 失败
{"success": false, "message": "错误原因"}
```

---

## 定时计划管理

### 获取定时计划列表
- **方法**: GET
- **端点**: `/control/getScheduleList`
- **参数**:
  - `name` (可选): 计划名称模糊匹配
  - `pageNumber` (可选): 页码，从1开始
  - `limit` (可选): 每页数量
- **响应格式**:
```json
{
  "success": true,
  "schedules": [
    {"id": 1, "name": "计划名称1", "status": "已启动"},
    {"id": 2, "name": "计划名称2", "status": "未启动"}
  ],
  "pageNumber": 1,
  "limit": 24,
  "total": 2
}
```
- **说明**: `schedules` 是当前分页的计划列表，`total` 是满足条件的计划总数。

### 启动/关闭定时计划
- **方法**: POST
- **端点**: `/control/setSchedule`
- **参数**:
  - `enable` (必需): `1` 表示启动，`0` 表示关闭
  - `id` (可选): 计划ID，与 `name` 至少提供一个
  - `name` (可选): 计划名称，与 `id` 至少提供一个
- **响应格式**:
```json
// 成功
{"success": true}
// 失败
{"success": false, "message": "错误原因"}
```

---

## 消息通知

### 获取通知信息
- **方法**: GET
- **端点**: `/control/getClawMessage`
- **参数**:
  - `clawType` (必需): claw类型，如 `OpenClaw`、`QClaw`、`EasyClaw`、`AutoClaw` 等
- **响应格式**:
```json
{
  "success": true,
  "channel": "channel_name",
  "userid": "user_id",
  "message": "消息内容"
}
```
- **说明**:
  - `channel`: 目标channel名称，为空表示无效消息
  - `userid`: 目标用户ID，可为空（表示发送给该channel的默认用户）
  - `message`: 消息内容，为空表示无效消息

---

## 系统配置

### 同步用户信息
- **方法**: POST
- **端点**: `/control/setClawUserInfo`
- **参数** (JSON Body):
```json
{
  "users": [
    {"channel": "channel1", "userid": "user1"},
    {"channel": "channel2", "userid": "user2"}
  ]
}
```
- **响应格式**:
```json
// 成功
{"success": true}
// 失败
{"success": false, message: "错误原因"}
```

### 传输Cron ID
- **方法**: POST
- **端点**: `/control/setClawCronId`
- **参数** (JSON Body):
  - `cronId` (必需): cron_job_id
  - `clawType` (必需): claw类型，如 `OpenClaw`、`QClaw`、`EasyClaw`、`AutoClaw` 等
- **响应格式**:
```json
// 成功
{"success": true}
// 失败
{"success": false, message: "错误原因"}
```

---

## 使用示例

### cURL 示例

**获取任务列表**:
```bash
curl "http://localhost:18803/control/getTaskList?pageNumber=1&limit=24"
```

**执行任务**:
```bash
curl -X POST "http://localhost:18803/control/runTask" \
  -H "Content-Type: application/json" \
  -d '{"id": 123}'
```

**获取通知**:
```bash
curl "http://localhost:18803/control/getClawMessage?clawType=OpenClaw"
```

**同步用户信息**:
```bash
curl -X POST "http://localhost:18803/control/setClawUserInfo" \
  -H "Content-Type: application/json" \
  -d '{"users": [{"channel": "webchat", "userid": "user123"}]}'
```

---

## 错误处理

- **400 Bad Request**: 参数错误或缺失
- **500 Internal Server Error**: 服务器内部错误
- **响应中的 `success` 字段**: 始终检查此字段，`false` 表示业务逻辑失败

## 注意事项

1. 所有接口均为本地调用，无需认证（当前版本）
2. 确保zworker应用正在运行且监听端口18803
3. 异步操作（如任务执行）可能立即返回成功，但实际执行需要时间
4. 分页参数 `pageNumber` 从1开始，`limit` 建议不超过48