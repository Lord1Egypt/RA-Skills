# 青龙面板 API 完整参考

官方文档：https://qinglong.online/api/

所有 API 基础路径：`http://<HOST>/api`
认证方式：`Authorization: Bearer <TOKEN>`
响应格式：`{"code": 200, "data": <结果>}`

---

## 认证

### 获取 Token
```
GET /open/auth/token?client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>
```
返回：`{"token": "xxx", "token_type": "Bearer", "expiration": 1234567890}`

> 注意：所有开放 API 接口的基础路径为 `/open`，获取 token 后在 Header 中携带 `Authorization: Bearer <token>`

---

## 定时任务 `/crons`

### 任务 CRUD

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| GET | `/crons` | 列出所有任务 | - |
| GET | `/crons/:id` | 获取单个任务 | - |
| GET | `/crons/detail` | 获取任务详情 | query: `?id=` |
| POST | `/crons` | 创建任务 | `{name, command, schedule, labels?}` |
| PUT | `/crons` | 更新任务 | `{id, name, command, schedule, ...}` |
| DELETE | `/crons` | 删除任务 | `[id1, id2, ...]` |

**创建任务请求体示例：**
```json
{
  "name": "签到任务",
  "command": "task jd_sign.js",
  "schedule": "30 0 * * *",
  "labels": ["签到"]
}
```

### 任务控制

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| PUT | `/crons/run` | 运行任务 | `[id1, id2, ...]` |
| PUT | `/crons/stop` | 停止任务 | `[id1, id2, ...]` |
| PUT | `/crons/enable` | 启用任务 | `[id1, id2, ...]` |
| PUT | `/crons/disable` | 禁用任务 | `[id1, id2, ...]` |
| PUT | `/crons/pin` | 置顶任务 | `[id1, id2, ...]` |
| PUT | `/crons/unpin` | 取消置顶 | `[id1, id2, ...]` |

### 任务日志

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/crons/:id/log` | 获取最新日志 |
| GET | `/crons/:id/logs` | 获取全部日志记录 |

### 任务标签

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| POST | `/crons/labels` | 添加标签 | `{ids: [...], labels: [...]}` |
| DELETE | `/crons/labels` | 删除标签 | `{ids: [...], labels: [...]}` |

### 视图管理

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| GET | `/crons/views` | 获取所有视图 | - |
| POST | `/crons/views` | 创建视图 | `{name, sorts?, filters?}` |
| PUT | `/crons/views` | 更新视图 | `{id, name, ...}` |
| DELETE | `/crons/views` | 删除视图 | `[id1, id2, ...]` |
| PUT | `/crons/views/move` | 移动视图 | `{id, fromIndex, toIndex}` |
| PUT | `/crons/views/enable` | 启用视图 | `[id1, id2, ...]` |
| PUT | `/crons/views/disable` | 禁用视图 | `[id1, id2, ...]` |

---

## 环境变量 `/envs`

| 方法 | 路径 | 说明 | 请求参数/体 |
|------|------|------|------------|
| GET | `/envs` | 获取变量列表 | query: `?searchValue=关键词` |
| GET | `/envs/:id` | 获取单个变量 | - |
| POST | `/envs` | 新增变量 | `[{name, value, remarks?}]` |
| PUT | `/envs` | 更新变量 | `{id, name, value, remarks?}` |
| DELETE | `/envs` | 删除变量 | `[id1, id2, ...]` |
| PUT | `/envs/enable` | 启用变量 | `[id1, id2, ...]` |
| PUT | `/envs/disable` | 禁用变量 | `[id1, id2, ...]` |
| PUT | `/envs/name` | 批量重命名 | `{ids: [...], name: "新名称"}` |
| PUT | `/envs/:id/move` | 移动变量排序 | `{fromIndex, toIndex}` |
| POST | `/envs/upload` | 从文件导入 | multipart/form-data (JSON文件) |

**新增变量示例（支持批量）：**
```json
[
  {"name": "JD_COOKIE", "value": "pt_key=xxx;pt_pin=yyy;", "remarks": "京东Cookie"},
  {"name": "BARK_KEY", "value": "your_bark_key", "remarks": "Bark推送"}
]
```

**变量命名规则：** 必须以字母或下划线开头，只能包含字母、数字和下划线。

---

## 订阅管理 `/subscriptions`

| 方法 | 路径 | 说明 | 请求参数/体 |
|------|------|------|------------|
| GET | `/subscriptions` | 获取订阅列表 | query: `?searchValue=&ids=` |
| POST | `/subscriptions` | 创建订阅 | 见下方示例 |
| PUT | `/subscriptions/run` | 运行订阅 | `[id1, id2, ...]` |
| PUT | `/subscriptions/stop` | 停止订阅 | `[id1, id2, ...]` |
| PUT | `/subscriptions/enable` | 启用订阅 | `[id1, id2, ...]` |
| PUT | `/subscriptions/disable` | 禁用订阅 | `[id1, id2, ...]` |
| GET | `/subscriptions/:id/log` | 最新日志 | - |
| GET | `/subscriptions/:id/logs` | 全部日志 | - |
| PUT | `/subscriptions/status` | 更新状态 | `{ids, status, pid?, log_path?}` |

**创建订阅示例（Git订阅）：**
```json
{
  "name": "订阅名称",
  "type": 0,
  "url": "https://github.com/user/repo",
  "branch": "main",
  "schedule": "0 0 * * *",
  "whitelist": "jd_",
  "blacklist": "test",
  "dependenceFile": "",
  "autoAddCron": true,
  "autoDelCron": false
}
```

**订阅类型 `type`：** `0`=公开仓库, `1`=私有仓库, `2`=单文件

---

## 脚本管理 `/scripts`

| 方法 | 路径 | 说明 | 请求参数/体 |
|------|------|------|------------|
| GET | `/scripts` | 获取脚本列表 | query: `?path=目录` |
| GET | `/scripts/detail` | 获取脚本内容 | query: `?filename=&path=` |
| POST | `/scripts` | 上传/创建脚本 | `{filename, content, path?}` 或 multipart |
| PUT | `/scripts` | 更新脚本内容 | `{filename, content, path?}` |
| DELETE | `/scripts` | 删除脚本 | `{filename, path?}` |
| POST | `/scripts/download` | 下载脚本 | `{filename, path?}` |
| PUT | `/scripts/run` | 运行脚本 | `{filename, path?}` |
| PUT | `/scripts/stop` | 停止脚本 | `{filename?, pid?}` |
| PUT | `/scripts/rename` | 重命名脚本 | `{filename, newFilename, path?}` |

---

## 依赖管理 `/dependencies`

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| GET | `/dependencies` | 获取依赖列表 | query: `?searchValue=&type=` |
| GET | `/dependencies/:id` | 获取单个依赖 | - |
| POST | `/dependencies` | 新增依赖 | `{name, type, remark?}` |
| PUT | `/dependencies` | 更新依赖 | `{id, name, type, remark?}` |
| DELETE | `/dependencies` | 删除依赖 | `[id1, id2, ...]` |
| DELETE | `/dependencies/force` | 强制删除 | `[id1, id2, ...]` |
| PUT | `/dependencies/reinstall` | 重新安装 | `[id1, id2, ...]` |
| PUT | `/dependencies/cancel` | 取消安装 | `[id1, id2, ...]` |

**依赖类型 `type`：** `0`=NodeJS, `1`=Python3, `2`=Linux

---

## 配置文件 `/configs`

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| GET | `/configs` | 获取配置文件列表 | - |
| GET | `/configs/detail` | 获取配置内容 | query: `?filename=` |
| PUT | `/configs` | 更新配置内容 | `{filename, content}` |
| GET | `/configs/:name` | 获取指定配置 | - |

---

## 系统设置 `/system`

### 系统信息与配置

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| GET | `/system` | 系统状态和版本信息 | - |
| GET | `/system/config` | 获取系统配置 | - |
| PUT | `/system/config/log-remove-frequency` | 设置日志清理频率 | `{frequency: <天数>}` |
| PUT | `/system/config/cron-concurrency` | 设置任务并发数 | `{concurrency: <数量>}` |
| PUT | `/system/config/dependence-proxy` | 设置依赖代理 | `{proxy: "http://..."}` |
| PUT | `/system/config/node-mirror` | 设置Node镜像 | `{url: "https://..."}` |
| PUT | `/system/config/python-mirror` | 设置Python镜像 | `{url: "https://..."}` |
| PUT | `/system/config/linux-mirror` | 设置Linux镜像 | `{url: "https://..."}` |

### 系统操作

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| PUT | `/system/update-check` | 检查更新 | - |
| PUT | `/system/update` | 执行更新 | - |
| PUT | `/system/reload` | 重载系统 | `{type?: ""}` |
| PUT | `/system/notify` | 发送通知 | `{title, content}` |
| PUT | `/system/command-run` | 执行Shell命令 | `{command: "ls -la"}` |
| PUT | `/system/command-stop` | 停止命令 | `{command?, pid?}` |

### 日志

| 方法 | 路径 | 说明 | 请求参数 |
|------|------|------|---------|
| GET | `/system/log` | 获取系统日志 | query: `?time=&type=` |
| DELETE | `/system/log` | 删除系统日志 | - |

### 数据导入导出

| 方法 | 路径 | 说明 |
|------|------|------|
| PUT | `/system/data/export` | 导出系统数据 |
| PUT | `/system/data/import` | 导入系统数据（multipart/form-data） |

**通知支持渠道（21+）：** Telegram、企业微信、钉钉、飞书、Bark、Gotify、邮件、Server酱、PushPlus、微信推送、自定义Webhook 等。

---

## 错误码说明

| code | 含义 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | Token 无效或过期，需重新获取 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## curl 完整示例合集

### 获取Token并保存
```bash
TOKEN=$(curl -s "http://192.168.1.100:5700/api/user/login?client_id=xxx&client_secret=yyy" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['token'])")
```

### 批量查看任务状态（格式化输出）
```bash
curl -s -H "Authorization: Bearer $TOKEN" "http://192.168.1.100:5700/api/crons" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
for c in data.get('data', data) if isinstance(data, dict) else data:
    status = ['空闲','运行中','停止'][c.get('status',0)] if c.get('status',0) < 3 else '未知'
    print(f\"ID:{c['id']:4d} | {status:4s} | {c.get('schedule',''):15s} | {c.get('name','')}\")
"
```

### 搜索并运行指定名称任务
```bash
# 搜索任务ID
IDS=$(curl -s -H "Authorization: Bearer $TOKEN" "http://<HOST>/api/crons" | python3 -c "
import sys, json
data = json.load(sys.stdin)['data']
tasks = data.get('data', data) if isinstance(data, dict) else data
ids = [str(t['id']) for t in tasks if '签到' in t.get('name','')]
print(json.dumps([int(i) for i in ids]))
")
# 运行
curl -s -X PUT -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d "$IDS" "http://<HOST>/api/crons/run"
```
