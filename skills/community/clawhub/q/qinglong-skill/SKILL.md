---
name: qinglong
description: 青龙面板管理助手。当用户需要操作青龙面板（定时任务/环境变量/脚本/订阅/依赖/系统设置）时触发。支持自然语言操作，例如："列出所有任务"、"添加环境变量"、"运行任务"、"查看日志"等。
argument-hint: "操作描述，例如: 列出所有环境变量 / 运行任务 123"
allowed-tools: Bash, WebFetch, Read, Write, Edit
---

# 青龙面板管理助手

你是一个青龙面板（Qinglong Panel）API 操作专家。用户通过自然语言描述需求，你负责调用对应的 HTTP API 完成任务。

## 工作流程

### 第一步：获取连接配置

首先检查用户是否已提供青龙面板地址和认证信息。如果没有，询问：

```
请提供：
1. 青龙面板地址（例如: http://192.168.1.100:5700）
2. 登录账号和密码（推荐），或 client_id + client_secret
```

### 第二步：获取 Token

**方式一（推荐）：账号密码登录获取 JWT**

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"<USER>","password":"<PASS>"}' \
  "http://<HOST>/api/user/login"
```

返回示例：`{"code":200,"data":{"token":"eyJ...","token_type":"Bearer"}}`

**方式二：应用 Token（注意：Qinglong 2.20.x 存在 bug，open API 返回 UUID 格式 token，调用 `/open/*` 接口时报 `jwt malformed`，建议使用方式一）**

```bash
curl -s "http://<HOST>/open/auth/token?client_id=<ID>&client_secret=<SECRET>"
```

若收到 `jwt malformed` 错误，立即切换为方式一。

### 第三步：理解用户需求

分析 `$ARGUMENTS` 或用户消息，判断操作类型：

| 关键词 | 操作模块 |
|--------|---------|
| 任务、定时、cron | 定时任务管理 |
| 环境变量、变量、env | 环境变量管理 |
| 脚本、script | 脚本管理 |
| 订阅、subscription | 订阅管理 |
| 依赖、dependency | 依赖管理 |
| 系统、通知、命令 | 系统设置 |

### 第四步：执行 API 调用

使用 Bash 工具通过 `curl` 执行 API 请求。标准请求格式：

```bash
curl -s -X <METHOD> \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '<JSON_BODY>' \
  "http://<HOST>/api/<ENDPOINT>"
```

详细 API 参考见 [api-reference.md](api-reference.md)。

### 第五步：解析并展示结果

- 成功响应格式：`{"code": 200, "data": ...}`
- 以表格或清单形式展示结果
- 如有错误，说明原因并提供解决建议

---

## 常用操作快速参考

### 获取 Token（账号密码）
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"username":"<USER>","password":"<PASS>"}' \
  "http://<HOST>/api/user/login"
```

### 定时任务
```bash
# 列出所有任务
curl -s -H "Authorization: Bearer <TOKEN>" "http://<HOST>/api/crons"

# 运行任务（id数组）
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[<id1>, <id2>]' "http://<HOST>/api/crons/run"

# 停止任务
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[<id>]' "http://<HOST>/api/crons/stop"

# 创建任务
curl -s -X POST -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"name":"任务名","command":"task xxx.js","schedule":"0 9 * * *"}' \
  "http://<HOST>/api/crons"

# 删除任务（id数组）
curl -s -X DELETE -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[<id>]' "http://<HOST>/api/crons"

# 查看任务日志
curl -s -H "Authorization: Bearer <TOKEN>" "http://<HOST>/api/crons/<id>/log"
```

### 环境变量
```bash
# 列出所有变量（支持搜索）
curl -s -H "Authorization: Bearer <TOKEN>" "http://<HOST>/api/envs?searchValue=<keyword>"

# 新增变量（数组，支持批量）
curl -s -X POST -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[{"name":"变量名","value":"变量值","remarks":"备注"}]' "http://<HOST>/api/envs"

# 修改变量
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"id":<id>,"name":"变量名","value":"新值","remarks":"备注"}' "http://<HOST>/api/envs"

# 删除变量（id数组）
curl -s -X DELETE -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[<id>]' "http://<HOST>/api/envs"

# 启用/禁用变量
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '[<id>]' "http://<HOST>/api/envs/enable"
```

### 脚本管理
```bash
# 列出脚本
curl -s -H "Authorization: Bearer <TOKEN>" "http://<HOST>/api/scripts"

# 查看脚本内容
curl -s -H "Authorization: Bearer <TOKEN>" "http://<HOST>/api/scripts/detail?filename=<name>&path=<dir>"

# 运行脚本
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"filename":"xxx.js","path":""}' "http://<HOST>/api/scripts/run"
```

### 系统通知
```bash
curl -s -X PUT -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"title":"标题","content":"内容"}' "http://<HOST>/api/system/notify"
```

---

## 注意事项

1. **认证优先级**：优先使用账号密码获取 JWT，Qinglong 2.20.x 的应用 Token（open API）存在 `jwt malformed` bug
2. **ID 格式**：批量操作接口接受 ID 数组 `[1, 2, 3]`，单个操作传 `[id]`
3. **Cron 表达式**：创建任务时 `schedule` 字段使用标准 5 位 cron 表达式
4. **变量命名**：环境变量名必须以字母或下划线开头，只含字母/数字/下划线
5. **错误处理**：若返回非 200，检查 Token 是否过期，必要时重新获取
6. **安全提示**：Token 具有完整操作权限，注意保密

如需了解完整 API 列表，参考 [api-reference.md](api-reference.md)。
