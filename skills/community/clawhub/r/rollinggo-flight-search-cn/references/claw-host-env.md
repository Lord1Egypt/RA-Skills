# Claw Host Environment Reference

本技能需要进程可见的 `ROLLINGGO_API_KEY`。如果宿主环境在多次运行之间丢失该变量，请优先使用宿主配置注入，而不是依赖 shell export。

**本技能的 key：** `rollinggo-searchflight`

## OpenClaw-family 配置

按你的环境选择注入层级，优先使用 per-skill 配置。

### Per-skill（推荐）

```json
{
  "skills": {
    "entries": {
      "rollinggo-searchflight": {
        "env": { "ROLLINGGO_API_KEY": "YOUR_KEY" }
      }
    }
  }
}
```

### Host-wide（多个技能共用同一个 key 时）

```json
{ "env": { "ROLLINGGO_API_KEY": "YOUR_KEY" } }
```

或者写入宿主的 `.env` 文件：`~/.openclaw/.env`（macOS/Linux）或 `%USERPROFILE%\.openclaw\.env`（Windows）。  
覆盖路径：`OPENCLAW_HOME`、`OPENCLAW_STATE_DIR`、`OPENCLAW_CONFIG_PATH`。

### Shell import fallback

```json
{ "env": { "shellEnv": { "enabled": true, "timeoutMs": 15000 } } }
```

仅在 key 已存在于登录 shell 中，但子进程拿不到时使用。

## Sandbox

宿主侧 env **不会自动传入** sandbox 进程。请把 `ROLLINGGO_API_KEY` 直接注入 sandbox，例如 `agents.defaults.sandbox.docker.env` 或等价配置。
