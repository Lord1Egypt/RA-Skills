---
name: openclaw-watchdog
description: "Keep OpenClaw gateway alive: heartbeat monitoring, auto-restart, crash alerts, memory warning, uptime report."
metadata:
  openclaw:
    requires:
      bins: ["systemctl", "curl", "ss"]
    install:
      - id: "init"
        kind: "shell"
        label: "Create watchdog directory"
        run: "mkdir -p /root/.openclaw/workspace/scripts"
---

# OpenClaw Watchdog

自动监控 OpenClaw Gateway 的运行状态，掉线自动重启，异常实时通知。

## 使用方式

### 一键运行监控

```
帮我启动 openclaw-watchdog
```

### 查看运行状态

```
watchdog status
```

### 停止监控

```
watchdog stop
```

### 自定义端口启动

```
帮我启动 openclaw-watchdog，端口 18789
```

## 功能

| 功能 | 说明 |
|------|------|
| 心跳检测 | 每 2 分钟检查 gateway 进程和端口 |
| 自动重启 | 检测到掉线自动 systemctl restart |
| 异常通知 | 通过当前聊天渠道发送掉线/恢复通知 |
| 内存预警 | 内存使用超过 80% 时预警 |
| 运行日报 | 每天生成 uptime 和异常统计报告 |
| 端口可配 | 支持自定义监控端口，默认 18789 |

## 实现说明

### 配置参数

用户可自定义以下参数（直接告诉 Agent 即可）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 端口 | Gateway 监听端口 | 18789 |
| 间隔 | 心跳检测间隔 | 2 分钟 |
| 内存阈值 | 内存预警线 | 80% |

### 检测逻辑

1. 检查 `systemctl is-active openclaw-gateway`
2. 检查配置的端口是否在监听（默认 18789）
3. 检查内存使用率
4. 如果前两项任何一项异常 → 触发重启流程
5. 重启后等待 10 秒再次验证
6. 如果依然不正常 → 发送紧急通知

### 通知内容

掉线通知:
```
⚠️ OpenClaw Watchdog 警报
时间: {时间}
异常: {具体异常内容}
已自动重启: 是/否
当前状态: {当前状态}
```

日报:
```
📊 OpenClaw 运行日报
日期: {日期}
总运行时间: {uptime}
重启次数: {次数}
内存峰值: {峰值}
异常事件: {列表}
```

## 脚本文件

监控脚本位于: `/root/.openclaw/workspace/scripts/watchdog.sh`

## 注意事项

- 需要 systemd 权限（root 用户）
- 心跳间隔默认 2 分钟，可在启动命令中自定义
- 日报发送时间默认早上 9 点
- 端口号可在启动时指定，不指定则用默认 18789
