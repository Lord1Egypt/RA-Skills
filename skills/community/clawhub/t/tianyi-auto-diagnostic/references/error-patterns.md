# OpenClaw 错误模式参考

## 认证相关

### token_mismatch

```
Error: unauthorized: gateway token mismatch
gateway closed (1008): unauthorized: gateway token mismatch
```

**原因**: 客户端（扩展程序/CLI）提供的令牌与网关配置的 `gateway.auth.token` 不匹配

**解决步骤**:
1. 读取配置：`Get-Content ~\.openclaw\openclaw.json | ConvertFrom-Json | Select-Object -ExpandProperty gateway`
2. 确认 `gateway.auth.token` 的值
3. 在扩展程序选项中填入相同令牌
4. 如配置为空，添加令牌后重启网关

**相关命令**:
```powershell
# 设置令牌
$config = Get-Content ~\.openclaw\openclaw.json -Raw | ConvertFrom-Json
$config.gateway.auth.token = "your-token"
$config | ConvertTo-Json -Depth 10 | Set-Content ~\.openclaw\openclaw.json
openclaw gateway restart
```

---

## 连接相关

### ECONNREFUSED

```
Error: connect ECONNREFUSED 127.0.0.1:18792
Error: connect ECONNREFUSED 127.0.0.1:18789
```

**原因**: 目标服务未运行

**端口说明**:
- `18789`: Gateway 主端口（默认）
- `18792`: Browser Relay 端口（Gateway 端口 + 3）

**解决步骤**:
1. 检查网关：`openclaw gateway status`
2. 如未运行：`openclaw gateway start`
3. 检查配置：确认 `gateway.mode: local`

---

### WebSocket closed

```
WebSocket closed with code 1008
```

**原因**: 认证失败或协议不匹配

**解决**: 参考 token_mismatch

---

## 配置相关

### JSON5 parse failed

```
SyntaxError: JSON5: invalid character '，' at 179:20
JSON5 parse failed
```

**原因**: 配置文件包含非法字符（常见：中文逗号、未闭合引号）

**解决步骤**:
1. 自动修复：`openclaw doctor --fix`
2. 手动检查报错行号的标点符号
3. 用标准 JSON 格式替换

---

### Unrecognized key

```
gateway: Unrecognized key: "authToken"
```

**原因**: 使用了已废弃的配置字段

**解决**:
- 旧字段 `gateway.authToken` → 新字段 `gateway.auth.token`
- 运行 `openclaw doctor --fix` 自动迁移

---

## 端口相关

### Port already in use

```
Port 18789 is already in use.
- pid 22916: node.exe ... gateway --port 18789
```

**原因**: 网关进程重复启动

**解决步骤**:
1. 停止旧进程：`Stop-Process -Id 22916 -Force`
2. 或正常停止：`openclaw gateway stop`
3. 重新启动：`openclaw gateway start`

**预防**: 避免手动启动多个网关实例

---

## 扩展程序相关

### Extension not installed

```
Chrome extension is not installed.
Run: "openclaw browser extension install"
```

**解决步骤**:
```powershell
openclaw browser extension install
# 然后按提示在 Chrome 中加载扩展
```

### Extension badge shows "!"

**原因**: 扩展程序无法连接到 Relay 服务

**检查清单**:
- [ ] 网关是否运行：`openclaw gateway status`
- [ ] Relay 端口是否正确（Gateway 端口 + 3）
- [ ] 令牌是否匹配
- [ ] Chrome 是否允许本地连接

---

## 服务状态码

### Gateway 状态

| 状态 | 含义 | 操作 |
|------|------|------|
| `Listening: 127.0.0.1:18789` | 正常运行 | 无需操作 |
| `RPC probe: failed` | 认证失败 | 检查令牌 |
| `Service: Not found` | 未注册计划任务 | `openclaw gateway start` |
| `Port already in use` | 端口冲突 | 停止旧进程 |

### Browser 状态

| 状态 | 含义 | 操作 |
|------|------|------|
| `running: true` | 浏览器运行中 | 无需操作 |
| `running: false` + `profile: chrome` | 扩展模式（正常） | 无需操作 |
| `detectedBrowser: unknown` | 未检测到 Chrome | 安装 Chrome |

---

## 日志位置

- **当前日志**: `\tmp\openclaw\openclaw-YYYY-MM-DD.log`
- **配置文件**: `~\.openclaw\openclaw.json`
- **技能目录**: `D:\workspace\openclaw_ceo\skills`

## 快速诊断命令

```powershell
# 一键诊断
openclaw gateway status
openclaw browser status
Get-Content \tmp\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log -Tail 20

# 配置验证
openclaw doctor --fix

# 服务重启
openclaw gateway restart
```
