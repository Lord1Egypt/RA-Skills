# OpenClaw Heartbeat 配置示例

## 配置项说明

| 字段 | 说明 | 示例值 |
|------|------|--------|
| every | 触发间隔 | "6h" (每6小时) |
| target | 目标消息 | "last" (回复最近一条) |
| directPolicy | 直接发送策略 | "allow" (允许直接发送) |
| lightContext | 轻量上下文 | true |
| activeHours | 活跃时段 | 09:00 - 22:00 (Asia/Shanghai) |

## 完整配置

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "6h",
        "target": "last",
        "directPolicy": "allow",
        "lightContext": true,
        "activeHours": {
          "start": "09:00",
          "end": "22:00",
          "timezone": "Asia/Shanghai"
        },
        "prompt": "Read HEARTBEAT.md if it exists in the workspace and follow it strictly. Use the say-hi-to-me skill if available. This run is only for a social proactive greeting. If no greeting should be sent, respond exactly HEARTBEAT_OK."
      }
    }
  }
}
```

> 注意：prompt 字段会根据用户配置的 proactive 设置自动生成，可参考 `HEARTBEAT.md`。
