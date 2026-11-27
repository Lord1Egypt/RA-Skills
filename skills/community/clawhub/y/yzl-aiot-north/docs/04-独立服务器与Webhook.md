# 04 · 独立服务器与 Webhook

Bridge 的目标：把“平台北向接口”变成你应用能直接消费的稳定 HTTP/Webhook 数据源，而不必在每个业务服务里重复处理登录、分页、时间格式和平台字段。

---

## 1. 架构

```text
设备 ──南向──> AIoT 平台
                    │
          ┌─────────┴─────────┐
          │  REST 北向 API     │  （默认，已验证）
          │  north MQTT topic  │  （需要平台分配独立凭证）
          └─────────┬─────────┘
                    │
              NorthBridge
        ┌───────────┼────────────┐
        │           │            │
   内存最新值    事件队列      Webhook
        │           │            │
   GET /latest  GET /events   你的服务器
```

Bridge 是**有状态但可重启**的：内存只保留最近 `retainEvents` 条事件和每台设备最新值；历史数据请从平台 `/history` 查询或写入你自己的数据库。

---

## 2. 启动

### Python

```bash
export AIOT_TOKEN='...'
aiot-north bridge \
  --device AIOTSDK-0001 \
  --device WANCD2-0000001008 \
  --host 0.0.0.0 --port 8080 --interval 10 \
  --webhook https://app.example.com/aiot/events \
  --secret 'shared-secret'
```

### JavaScript

```bash
export AIOT_TOKEN='...'
node src/cli.js bridge \
  --device AIOTSDK-0001 \
  --port 8080 --interval 10 \
  --webhook https://app.example.com/aiot/events \
  --secret 'shared-secret'
```

`--discover`（Python）/ 不传 `--device`（JS）会自动拉取账号下设备列表；设备多时注意 API 频率限制。

### 有北向 MQTT 凭证时

Python：

```python
from aiot_north import NorthBridge, NorthMQTT
from aiot_north.bridge import BridgeConfig

mqtt = NorthMQTT(username="north-user", password="north-pass")
bridge = NorthBridge(client, BridgeConfig(port=8080), mqtt=mqtt)
bridge.start(block=True)
```

JavaScript：

```js
import { NorthBridge, NorthClient, NorthMQTT } from "aiot-north";

const mqtt = new NorthMQTT({ username: "north-user", password: "north-pass" });
const bridge = new NorthBridge(await NorthClient.fromEnv(), {
  port: 8080,
  mqtt,
});
await bridge.start();
```

没有凭证时 `mqtt` 留空，Bridge 自动 REST 轮询。

---

## 3. HTTP API

### `GET /health`

```json
{
  "ok": true,
  "uptime_sec": 120.5,
  "mode": "rest-poll",
  "devices": 2,
  "latest": 2,
  "events": 18,
  "last_poll": "2026-11-03T17:34:28+00:00",
  "error_count": 0,
  "error_last": null,
  "webhook": true
}
```

### `GET /devices`

返回 `{"items":[最新值...]}`。

### `GET /devices/{id}/latest`

单设备最新值；不存在返回 404。

### `GET /devices/{id}/history?limit=100`

内存内该设备最近事件。

### `GET /events?since=<seq>&limit=100`

增量事件：

```json
{
  "items": [
    {
      "seq": 18,
      "type": "telemetry",
      "received_at": "2026-11-03T17:34:28+00:00",
      "device_id": "AIOTSDK-0001",
      "deviceId": "AIOTSDK-0001",
      "values": {"temp": 25.5, "hum": 60},
      "online": false,
      "ts": "2026-11-04 01:30:16",
      "raw": {}
    }
  ]
}
```

客户端保存最后 `seq`，下次带 `since=<seq>` 即可断点续传（仅限 Bridge 内存保留范围）。

### `GET /metrics`

Prometheus 文本：

```text
aiot_bridge_devices 2
aiot_bridge_latest_devices 2
aiot_bridge_events_total 18
aiot_bridge_errors_total 0
```

### `POST /commands/{id}`

默认关闭。开启：

```bash
aiot-north bridge --device DEV-1 --allow-command
```

```bash
curl -X POST http://127.0.0.1:8080/commands/DEV-1 \
  -H 'Content-Type: application/json' \
  -d '{"cmd":"set","args":["sw","1"]}'
```

> 这是高权限接口。公网部署必须加鉴权/白名单；更推荐让业务后端直接调用 `NorthClient.send_command`。

---

## 4. Webhook

### 4.1 请求

```http
POST /aiot/events HTTP/1.1
Content-Type: application/json
X-AIoT-Event: telemetry
X-AIoT-Signature: sha256=<hex>
```

Body：

```json
{
  "seq": 18,
  "type": "telemetry",
  "received_at": "2026-11-03T17:34:28+00:00",
  "device_id": "AIOTSDK-0001",
  "deviceId": "AIOTSDK-0001",
  "values": {"temp": 25.5, "hum": 60},
  "online": false,
  "ts": "2026-11-04 01:30:16",
  "raw": {}
}
```

- 只在新数据/在线状态变化时触发；不会每个轮询周期重复。
- 失败重试 3 次（0.5s / 1s / 2s 退避）。
- 返回 2xx 视为成功。

### 4.2 Python 校验

```python
import hashlib, hmac

def verify(secret: str, body: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)

# Flask / FastAPI 里拿到原始 body
@app.post("/aiot/events")
async def events(request: Request):
    body = await request.body()
    if not verify(SECRET, body, request.headers.get("X-AIoT-Signature", "")):
        raise HTTPException(401, "bad signature")
    event = json.loads(body)
    ...
```

### 4.3 Node 校验

```js
import crypto from "node:crypto";

function verify(secret, body, signature) {
  const expected = "sha256=" + crypto.createHmac("sha256", secret).update(body).digest("hex");
  const a = Buffer.from(signature);
  const b = Buffer.from(expected);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

app.post("/aiot/events", express.raw({ type: "application/json" }), (req, res) => {
  if (!verify(process.env.AIOT_WEBHOOK_SECRET, req.body, req.get("X-AIoT-Signature") || "")) {
    return res.status(401).send("bad signature");
  }
  const event = JSON.parse(req.body.toString("utf8"));
  res.status(204).end();
});
```

> 必须使用**原始 body** 计算 HMAC，不能先 `JSON.parse` 再 `JSON.stringify`（空格/键顺序会变）。

### 4.4 幂等

Webhook 可能重试，业务侧用 `(deviceId, ts, seq)` 或自己的事件 ID 去重；`seq` 只在单次 Bridge 进程内递增，重启会从 1 开始。

---

## 5. 部署

### systemd

```ini
[Unit]
Description=AIoT northbound bridge
After=network-online.target
Wants=network-online.target

[Service]
WorkingDirectory=/opt/aiot-north
EnvironmentFile=/etc/aiot-north.env
ExecStart=/opt/aiot-north/.venv/bin/aiot-north bridge \
  --device AIOTSDK-0001 --host 127.0.0.1 --port 8080 --interval 10
Restart=always
RestartSec=3
User=aiot

[Install]
WantedBy=multi-user.target
```

`/etc/aiot-north.env`：

```text
AIOT_BASE_URL=https://aiot.yzlkj.com
AIOT_TOKEN=...
AIOT_WEBHOOK_URL=https://app.example.com/aiot/events
AIOT_WEBHOOK_SECRET=...
```

### Nginx 反向代理

```nginx
location /aiot/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    # 在这里加 auth_request / IP 白名单 / TLS
}
```

### Docker（示例）

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY python /app/python
RUN pip install --no-cache-dir -e /app/python
ENV AIOT_BASE_URL=https://aiot.yzlkj.com
EXPOSE 8080
CMD ["aiot-north", "bridge", "--discover", "--host", "0.0.0.0", "--port", "8080", "--interval", "10"]
```

---

## 6. 扩展到自己的应用

三种常见接法：

1. **前端/小程序** → 调你的业务后端 → 业务后端调 Bridge `/latest`、`/events`；不要把 JWT 放前端。
2. **独立服务器** → Bridge Webhook 推到你的 `/aiot/events`，你落库/告警/转发。
3. **数据管道** → Bridge `/events` 增量拉取，写入 Kafka/MQ/时序库；用 `seq` 断点。

如果设备量大或需要毫秒级实时：

- 向平台申请北向 MQTT 独立凭证，用 `NorthMQTT` 直接订阅；
- 或让平台把 `north/.../data` 桥接到你的 MQTT/Kafka；
- 不要用 5 秒轮询几千台设备（会触发限流）。

---

## 7. 安全清单

- Bridge 默认只读；`--allow-command` 是高权限开关。
- 公网必须 TLS + 鉴权（mTLS/Token/网关）。
- Webhook 密钥放环境变量；校验签名；使用常量时间比较。
- 日志不要打印 `Authorization`、API Key、设备 `password`。
- `retainEvents` 不是持久化；重启会丢内存事件，重要数据落库。
