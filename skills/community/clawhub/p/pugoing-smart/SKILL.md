---
name: pugoing-smart
description: 提供 Pugoing 中控平台的常用 API 调用能力，用于查询区域、主机、设备，以及通过自然语言控制设备。
---

# Pugoing Smart

这个目录提供一个通用调用脚本，目标是让 Agent 用尽量少的上下文完成对 Pugoing 平台的常见调用。

环境变量示例：

```bash
export PUGOING_BASE_URL="http://127.0.0.1:8080"
export PUGOING_API_KEY="xq_agent_xxx"
export PUGOING_TIMEOUT="30"
```

说明：

- `PUGOING_API_KEY` 必选，格式通常是 `xq_agent_xxx`
- `PUGOING_BASE_URL` 可选，默认是 `http://127.0.0.1:8080`, 一般是局域网地址
- `PUGOING_TIMEOUT` 可选，单位秒，默认 `30`

脚本会自动处理读环境变量和鉴权. 调用方只需要专注于传入正确的JSON即可.

## 通用调用对象

推荐传一个 JSON 对象给 `client.py`：

```json
{
  "path": "/api/xq_host/list",
  "method": "GET"
}
```

字段说明：

- `path`: 相对路径，推荐写法
- `url`: 也支持完整 URL；如果同时给了 `url`，优先使用 `url`
- `method`: `GET` 或 `POST`
- `params`: 查询参数
- `data`: JSON body
- `headers`: 额外请求头
- `timeout`: 单次请求超时秒数

## 输入方式

`client.py` 支持两种输入方式：

### 1. 传 JSON 文件

```bash
python client.py examples/list_hosts.json
```

### 2. 从 stdin 读 JSON

```bash
echo '{"path":"/api/xq_host/list","method":"GET"}' | python client.py -
```

## 常见能力

### 1. 查区域和主机

调用：

- `/api/host_area/list`

示例：

```bash
python client.py examples/list_areas_and_hosts.json
```

### 2. 查主机列表

调用：

- `/api/xq_host/list`

示例：

```bash
python client.py examples/list_hosts.json
```

### 3. 查某台主机下的设备

调用：

- `/api/device/sync?host_ip=...`

示例：

```bash
python client.py examples/list_host_devices.json
```

### 4. 用自然语言控制设备

调用：

- `/api/device/control/voice`

推荐只传：

- `host_ip`
- `dvcm`

示例：

```bash
python client.py examples/control_device_by_dvcm.json
```

请求体示例：

```json
{
  "host_ip": "192.168.1.88",
  "dvcm": "打开客厅灯"
}
```

### 5. 兜底走内置 AI

调用：

- `/api/ai/chat`

建议：

- 平台级查询或跨主机场景时，`host_ip` 传 `"global"`
- 单主机设备控制或上下文理解时，`host_ip` 传实际主机 IP

示例：

```bash
python client.py examples/ai_fallback.json
```
