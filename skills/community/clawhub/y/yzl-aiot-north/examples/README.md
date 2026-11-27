# 北向示例（Python / Node.js）

两个语言、各两个场景：

| 文件 | 场景 |
|---|---|
| `python/quickstart.py` | 设备列表 → 最新值 → 历史 |
| `python/bridge_webhook.py` | 起只读 Bridge，把变更推到 Webhook |
| `js/quickstart.mjs` | 同上（Node.js ESM） |
| `js/bridge_webhook.mjs` | 同上（Node.js ESM） |

## 准备

1. **客户端库**：技能自带 `lib/`，无需安装。
   - Python：`sys.path.insert(0, "../lib")`（示例已处理）
   - Node：直接 `import "../lib/north_client.mjs"`（示例已处理）
2. **认证**（三选一）：
   - `AIOT_TOKEN`（JWT）
   - `AIOT_ACCOUNT` + `AIOT_PASSWORD`
   - `AIOT_API_KEY`
3. **平台地址**：默认 `https://aiot.yzlkj.com`，可用 `AIOT_BASE_URL` 覆盖。

## 运行

```bash
# Python
python python/quickstart.py
set AIOT_WEBHOOK_URL=https://app.example.com/aiot/events
python python/bridge_webhook.py DEV-1

# Node
node js/quickstart.mjs
node js/bridge_webhook.mjs DEV-1
```

## 注意

- **限频**：用户配额 = 基础配额 + 设备数 × 每台追加（次/秒）；写接口（POST/PUT/DELETE）按 3 倍计；超限 429。
  轮询多台设备时把 `interval` 调大，或改走北向 MQTT / Bridge 事件。
- **下发指令**是写接口：先确认设备固件支持，再调用 `client.devices.command(...)`。
- 不要把 token / 密码写进示例；Webhook secret 用环境变量，并校验 `X-AIoT-Signature`。
