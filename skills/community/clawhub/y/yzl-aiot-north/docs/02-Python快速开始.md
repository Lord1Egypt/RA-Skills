# 02 · Python 快速开始

要求 Python >= 3.8，REST 部分只用标准库；MQTT 需要可选 `paho-mqtt`。

---

## 1. 安装

```bash
cd aiot-north/python
python -m pip install -e .
```

或者不安装，临时指定源码路径：

```bash
export PYTHONPATH=src
python -m aiot_north --help
```

---

## 2. 配置

推荐用环境变量：

```bash
export AIOT_BASE_URL='https://aiot.yzlkj.com'
export AIOT_TOKEN='...'          # JWT，优先
# 或
export AIOT_ACCOUNT='用户名'
export AIOT_PASSWORD='密码'
# 或
export AIOT_API_KEY='ak_...'
```

- `AIOT_TOKEN` 存在时直接使用，不登录。
- 只有 `AIOT_ACCOUNT/PASSWORD` 时，`from_env()` 自动登录。
- `AIOT_API_KEY` 单独使用时可能只能看到空数据（平台账号差异），先用 `/open/account` 验证。
- 可选 `AIOT_TIMEOUT`（秒，默认 10）。

---

## 3. 客户端

```python
from aiot_north import NorthClient

client = NorthClient.from_env()
# 或显式：
# client = NorthClient(base_url="https://aiot.yzlkj.com", token="...")
# client.login("账号", "密码")
```

### 3.1 设备与数据

```python
devices = client.devices.list(max_results=20)
print(devices["total"])

device = client.devices.get("AIOTSDK-0001")          # 默认脱敏 password/bindCode
device = client.devices.get("AIOTSDK-0001", include_secrets=True)

telemetry = client.devices.telemetry("AIOTSDK-0001")
history = client.devices.history(
    "AIOTSDK-0001",
    keys=["temp", "hum"],
    start="2026-11-01 00:00:00",
    end="2026-11-04 23:59:59",
    limit=1000,
)
aggregate = client.devices.aggregate(
    "AIOTSDK-0001",
    keys=["temp"],
    start="2026-10-01 00:00:00",
    end="2026-11-04 23:59:59",
    bucket="1d",
)
```

### 3.2 指令

```python
result = client.devices.command("AIOTSDK-0001", "set", ["sw", "1"])
print(result["commandId"], result["status"])

# 显式完整 args 也可以：
client.devices.command("AIOTSDK-0001", "set", ["AIOTSDK-0001", "sw", "1"])

status = client.commands.list(device_id="AIOTSDK-0001", page_size=10)
```

### 3.3 告警 / 型号 / 账号

```python
alarms = client.alarms.list(status="active", page_size=20)
products = client.products.list()
ports = client.gateway_ports()
account = client.account()
```

### 3.4 归一化

```python
from aiot_north import normalize_telemetry, parse_device_payload

record = normalize_telemetry(telemetry)
print(record["deviceId"], record["values"], record["online"])

# MQTT payload 也可以单独解析：
mqtt_record = parse_device_payload(
    '{"ter":"DEV-1","data":[{"func":"facs","args":["temp","25.5"]}]}',
    topic="north/P1/DEV-1/data",
)
print(mqtt_record["values"])   # {"temp": 25.5}
```

---

## 4. 错误处理

```python
from aiot_north import AiotAuthError, AiotRateLimitError, AiotAPIError, AiotNetworkError

try:
    data = client.devices.telemetry("DEV-1")
except AiotAuthError:
    client.login()          # 使用保存的账号密码
except AiotRateLimitError:
    time.sleep(10)
except AiotAPIError as exc:
    print(exc.code, exc.message, exc.status)
except AiotNetworkError as exc:
    print("network:", exc)
```

- `AiotAuthError`：401/403，token 过期或权限不足。
- `AiotRateLimitError`：429；退避后重试。
- `AiotAPIError`：其他业务错误，含 `code/status/payload`。
- `AiotNetworkError`：DNS/连接/超时。
- `AiotProtocolError`：返回不是合法 JSON 信封。

SDK 默认对 429/5xx 重试 2 次，指数退避。

---

## 5. CLI

```bash
aiot-north whoami
aiot-north account
aiot-north devices --limit 10 --filter 温室
aiot-north telemetry AIOTSDK-0001
aiot-north history AIOTSDK-0001 --keys temp,hum --limit 50
aiot-north command AIOTSDK-0001 set sw 1
aiot-north commands --device AIOTSDK-0001 --page-size 10
aiot-north alarms --status active
aiot-north products
aiot-north ports
aiot-north bridge --device AIOTSDK-0001 --port 8080 --interval 5
aiot-north watch --device AIOTSDK-0001 --interval 5
```

凭证可通过环境变量或 `--token/--account/--password/--api-key` 传入。密码缺省时会提示输入。

---

## 6. MQTT（可选）

```bash
python -m pip install -e ".[mqtt]"
```

```python
from aiot_north.mqtt import NorthMQTT

def on_data(record):
    print(record["deviceId"], record["values"])

client = NorthMQTT(
    host="ciot.yzlkj.com",
    port=1883,
    username="平台分配的北向用户名",
    password="平台分配的北向密码",
    on_data=on_data,
)
client.start()       # 异步重连；或 client.run_forever()
# ...
client.stop()
```

> 北向 MQTT 凭证不是每个账号都有；没有就使用 Bridge 的 REST 轮询。详见 [01-北向接口说明.md](01-北向接口说明.md) 第 4 节。

---

## 7. 独立服务器

见 [04-独立服务器与Webhook.md](04-独立服务器与Webhook.md)，或直接：

```bash
aiot-north bridge --device AIOTSDK-0001 --port 8080
```

---

## 8. 测试

```bash
cd python
python -m unittest discover -s tests -v
```

测试覆盖：URL/查询参数、认证头、错误映射、指令参数、历史查询、载荷归一化、Bridge HTTP 端点。
