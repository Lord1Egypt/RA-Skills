# Self-Heal Watchdog 配置参考

## 环境变量

所有脚本使用以下环境变量（有合理默认值）：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_HOME` | `~/.openclaw` | OpenClaw 根目录 |
| `GATEWAY_URL` | `http://localhost:18789` | Gateway 地址 |
| `HEALTH_ENDPOINT` | `/health` | 健康检查端点 |
| `FAIL_THRESHOLD` | `2` | 连续失败多少次触发 failover |
| `HEALTH_TIMEOUT` | `10` | 健康检查超时（秒） |
| `DRY_RUN` | `0` | 设为 1 启用干运行模式 |

## 健康检查端点

- **端点:** `GET http://localhost:18789/health`
- **正常响应:** `{"ok":true,"status":"live"}`
- **超时判定:** 超过 10 秒无响应视为失败

## 状态文件格式

`~/.openclaw/watchdog-state.json`:

```json
{
  "current_model": "openrouter/hunter-alpha",
  "original_model": "openrouter/healer-alpha",
  "fail_count": 0,
  "last_check": "2026-03-16T11:00:00-07:00",
  "last_failover": null,
  "config_backups": 3,
  "failed_models": []
}
```

| 字段 | 说明 |
|------|------|
| `current_model` | 当前使用的模型 |
| `original_model` | 初始模型（failover 前） |
| `fail_count` | 连续失败计数 |
| `last_check` | 最后一次检查时间 |
| `last_failover` | 最后一次切换时间 |
| `config_backups` | 备份文件数量 |
| `failed_models` | 已失败的模型列表（避免切回） |

## 模型切换规则

1. 读取当前模型 → 找到下一个可用模型（跳过 `failed_models`）
2. 更新 `openclaw.json` 中 `agents.defaults.model.primary`
3. 重启 gateway
4. 记录到 `failed_models` 避免循环

## 日志轮转

- 最大行数: 1000 行
- 自动在每次写入时检查并裁剪
- 日志路径: `~/.openclaw/watchdog/watchdog.log`

## Scheduler (launchd)

macOS 使用 launchd 而非 cron：

- **Plist:** `~/Library/LaunchAgents/com.openclaw.watchdog.plist`
- **间隔:** 每 60 秒
- **Label:** `com.openclaw.watchdog`

管理命令：
```bash
# 查看状态
launchctl list | grep openclaw.watchdog

# 手动卸载
launchctl unload ~/Library/LaunchAgents/com.openclaw.watchdog.plist

# 手动加载
launchctl load ~/Library/LaunchAgents/com.openclaw.watchdog.plist
```
