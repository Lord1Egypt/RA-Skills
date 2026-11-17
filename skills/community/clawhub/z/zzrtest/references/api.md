# DEV 测试环境日志系统 API 参考

## 基础信息

- **API 网关**：`https://devtool.flightroutes24.com`（与生产相同）
- **环境标识**：请求 Header `profile: DEV`（生产为 `PROD`）

### 必需 Header

```
profile:    DEV
gray:       zzr
user:       {账号}_dev-{token}     # 测试环境账号名带 _dev 后缀
webVersion: 1.0.0
Content-Type: application/json
```

### 与生产 curl 对比

| 字段 | 生产 | 测试（DEV） |
|------|------|-------------|
| `profile` | `PROD` | `DEV` |
| `user` | `zhaorong.zhou-{token}` | `zhaorong.zhou_dev-{token}` |
| `gray` | `zzr` | `zzr` |
| 服务示例 | `order` | `account_deve`、`export_zzr` |
| SSE connectId | `{账号}-{executeId}` | `{账号}_dev-{executeId}` |

---

## 浏览器流程（find-log 页面）

### 1. 发起搜索

```
POST /sse/searchLog
```

**请求体示例：**
```json
{
  "text": "\"关键词\"",
  "option": "",
  "pipelineHandle": "",
  "startDate": "2026-07-01 17:35:43",
  "endDate": null,
  "service": ["account_deve"],
  "executeId": "cd080108-2914-4060-8f99-af7a0e15b984",
  "executeTime": "2026-07-02 14:43:52",
  "concurrentSearch": true,
  "sshToken": "你的账号-你的token"
}
```

### 2. SSE 拉取结果

```
GET /sse/connectLogEmitter?executeId={账号}_dev-{executeId}
Accept: text/event-stream
```

---

## Agent 脚本流程（dev_log.py）

脚本使用 **同步封装接口**，无需手动连接 SSE：

```
POST /sse/syncSearchLog
```

Header 与 body 字段同上；若 `~/.DEV_SKILL/dev-find-log/config.json` 配置了 `sshToken`，会自动写入 body。

其他接口：

| 接口 | 说明 |
|------|------|
| `GET /ssh/searchService` | 获取 DEV 环境可搜服务列表 |
| `GET /sse/downloadLog?executeId=&service=&server=` | 下载命中日志文件 |

下载保存路径：`~/.DEV_SKILL/dev-find-log/{executeId}/{service}-{server}.log`

---

## 配置文件（可选）

路径：`~/.DEV_SKILL/dev-find-log/config.json`

```json
{
  "profile": "DEV",
  "user": "你的账号_dev-你的token",
  "sshToken": "你的账号-你的token",
  "gray": "zzr",
  "webVersion": "1.0.0"
}
```

未配置时使用内置 Agent 账号 `dev-agentskill`。

---

## 时间戳解析规则

从 traceId / requestId 自动解析时间（脚本内置）：

- **长格式**（末尾 ≥13 位毫秒）：取前 13 位 epoch → CST
- **短格式**（字母/下划线 + 12 位 YYMMDDHHmmss）：直接解析为 CST

---

## 服务匹配规则

```python
def match_service(user_input: str, service: dict) -> bool:
    keywords = user_input.lower().split()
    haystack = " ".join([
        service.get("label", ""),
        service.get("value", ""),
        service.get("keyWord", ""),
    ]).lower()
    return all(k in haystack for k in keywords)
```

测试环境服务名常带 `_deve` / `_deva` / `_devb` 等后缀，匹配时注意使用 devtool 返回的完整 value。
