---
name: zworker
description: 控制zworker AI自动化任务应用，支持任务管理、定时计划控制、用户信息同步和消息通知转发。当用户提到“zworker”关键词时使用此技能，例如：同步用户信息、获取任务列表、执行任务、管理定时计划、获取并发送通知等。技能通过HTTP接口与本地运行的zworker应用（localhost:18803）通信。
---

# Zworker 技能

## 概述

zworker 是一个AI自动化任务的Electron应用，本技能提供与zworker应用交互的完整能力，包括：

- **同步用户信息**：将OpenClaw的channel和userid同步到zworker
- **消息通知处理**：获取zworker的通知并转发到指定用户
- **任务管理**：获取、执行zworker任务
- **定时计划管理**：获取、启用、关闭zworker的定时计划

所有操作通过zworker暴露的HTTP接口（http://localhost:18803）完成。

## 快速开始

### 前置条件
1. zworker应用正在运行，HTTP服务监听在 http://localhost:18803
2. OpenClaw环境已配置好message工具，能够向各channel发送消息

## 核心功能

### 1. 同步用户信息至zworker
**触发语句**：`帮我调用zworker技能，同步用户信息至zworker`、`帮我同步用户信息至zworker`

**工作流程**：
1. 读取当前OpenClaw的openclaw.json文件中的channels字段，获取当前可用的channel以及该channel的userid，把数据平铺得到 `[{channel: 'xxx', userid: 'xxx'}, ...]`，作为下一步的users参数
2. 调用 `POST /control/setClawUserInfo` 接口，把user信息同步到zworker，参数格式为 `{ users: [{channel: '', userid: ''}, ...] }`
3. 调用 `POST /control/setClawUserInfo` 接口同步到zworker
4. 输出同步结果

**输出**：
- 成功：`已成功同步用户信息至zworker，请返回zworker继续操作。`
- 失败：`用户信息同步失败` + 原因

### 2. 获取zworker消息并发送给指定用户
**触发语句**：`帮我调用zworker技能，发送zworker的消息通知`、`帮我获取并发送zworker的消息通知`

**工作流程**：
1. 调用 `GET /control/getClawMessage` 接口，`clawType` 参数必须传入，且固定传入 `QClaw`，
2. 解析返回的 `{channel: 'xxx', userid: 'xxx', message: 'xxx'}`
3. 如果channel和message非空，使用message工具将消息发送到指定channel和userid
   - 如果userid为空，发送到该channel的默认绑定用户或最近聊天的用户
4. 输出发送的消息内容或错误信息

**输出**：
- 成功：输出message字段内容
- 失败：`zworker消息获取/发送失败` + 原因

### 3. 获取zworker任务列表
**触发语句**：`帮我调用zworker技能，获取zworker的任务列表`、`帮我获取zworker的任务列表`、`获取下一页zworker任务数据`、`查找名称为[xxx]的zworker任务`

**工作流程**：
1. 解析用户请求中的任务名称过滤条件和分页参数
2. 调用 `GET /control/getTaskList` 接口，传入 `name`、`pageNumber`、`limit` 参数
3. 默认：`pageNumber=1`、`limit=24`
4. 以列表形式输出任务ID和任务名称
5. 如果还有下一页数据，提示可获取更多数据

**输出格式**：
```
- 任务A（任务ID：1）
- 任务B（任务ID：2）
...
当前仅返回前24条任务数，如果需要获取更多可以继续跟我说，比如：获取下一页数据
```

### 4. 执行zworker任务
**触发语句**：`帮我调用zworker技能，执行id为[12312]的zworker任务`、`帮我执行id为[12312]的zworker任务`、`帮我执行名称为[xxx自动化执行]的zworker任务`

**工作流程**：
1. 解析用户请求中的任务ID或名称
2. 调用 `POST /control/runTask` 接口，传入 `id` 或 `name` 参数
3. 检查返回的 `success` 字段

**输出**：
- 成功：`已成功触发任务执行`
- 失败：`触发任务执行失败` + 原因

### 5. 获取zworker定时计划列表
**触发语句**：`帮我调用zworker技能，获取定时计划列表`、`帮我获取zworker的定时计划列表`、`查找名称为[xxx]的zworker计划`

**工作流程**：
1. 解析用户请求中的计划名称过滤条件和分页参数
2. 调用 `GET /control/getScheduleList` 接口，传入 `name`、`pageNumber`、`limit` 参数
3. 默认：`pageNumber=1`、`limit=24`
4. 以列表形式输出计划ID、计划名称、状态（已启动/未启动）
5. 如果还有下一页数据，提示可获取更多数据

**输出格式**：
```
- 计划A（计划ID：1，状态：已启动）
- 计划B（计划ID：2，状态：未启动）
...
当前仅返回前24条计划数，如果需要获取更多可以继续跟我说，比如：获取下一页数据
```

### 6. 启动zworker定时计划
**触发语句**：`帮我调用zworker技能，启用id为[12321]的定时计划`、`帮我启用id为[12321]的zworker定时计划`、`帮我启动名称为[xxx]的计划`

**工作流程**：
1. 解析用户请求中的计划ID或名称
2. 调用 `POST /control/setSchedule` 接口，传入 `enable=1` 和 `id` 或 `name` 参数
3. 检查返回的 `success` 字段

**输出**：
- 成功：`已成功启动定时计划`
- 失败：`定时计划启动失败` + 原因

### 7. 关闭zworker定时计划
**触发语句**：`帮我调用zworker技能，关闭id为[12321]的定时计划`、`帮我关闭id为[12321]的zworker定时计划`、`帮我关闭名称为[xxx]的计划`

**工作流程**：
1. 解析用户请求中的计划ID或名称
2. 调用 `POST /control/setSchedule` 接口，传入 `enable=0` 和 `id` 或 `name` 参数
3. 检查返回的 `success` 字段

**输出**：
- 成功：`已成功关闭定时计划`
- 失败：`定时计划关闭失败` + 原因

## 技术细节

### HTTP接口基础
- **基础URL**：`http://localhost:18803`
- **认证**：当前无需认证（本地网络）
- **超时**：建议设置5秒超时
- **错误处理**：检查HTTP状态码和返回的 `success` 字段

### 接口规范
详细接口定义见 [references/api_endpoints.md](references/api_endpoints.md)

### 脚本使用
本技能提供以下Python脚本，位于 `scripts/` 目录：

1. **`zworker_api.py`** - 通用HTTP客户端，封装所有接口调用
2. **`sync_users.py`** - 同步用户信息到zworker
3. **`fetch_notifications.py`** - 获取并发送zworker消息通知
4. **`list_tasks.py`** - 获取任务列表（支持分页和过滤）
5. **`run_task.py`** - 执行任务（按ID或名称）
6. **`list_schedules.py`** - 获取定时计划列表（支持分页和过滤）
7. **`enable_schedule.py`** - 启用定时计划
8. **`disable_schedule.py`** - 关闭定时计划

### 配置与存储
- **用户列表**：通过OpenClaw的 cli、gateway 等工具获取当前channel和userid

## 故障排除

1. **连接失败**：检查zworker应用是否运行，端口18803是否可访问
2. **认证错误**：当前无需认证，未来可能需要API密钥
3. **消息发送失败**：检查目标channel是否配置正确，userid是否存在

## 注意事项

1. 用户信息同步应在channel配置变更后执行
2. 消息通知功能依赖cron任务定期执行，也可手动触发
3. 所有HTTP接口为本地调用，确保网络环境安全
