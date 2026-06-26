# StockToday Skill 安装使用指南

> StockToday Skill v1.3.10 — 提供 **241** 个 A股/港股/美股/基金/期货数据接口
> ClawHub slug: `stocktoday` · 版本: `1.3.10`

---

## 1. 前置依赖

- **Node.js ≥ 18** ([下载](https://nodejs.org))
- **npx** (Node 自带)
- **StockToday TOKEN** (从 [stocktoday.cn](https://stocktoday.cn) 申请)

验证:
```bash
node -v   # 应 ≥ v18
npx -v    # 应 ≥ 9
```

---

## 2. 一键安装 (ClawHub CLI)

```bash
# 安装最新版
npx clawhub install stocktoday

# 安装指定版本
npx clawhub install stocktoday --version 1.3.4

# 安装到当前目录 (覆盖式)
npx clawhub install stocktoday --force
```

默认安装路径:
- **Windows**: `%USERPROFILE%\skills\stocktoday\`
- **macOS/Linux**: `~/skills/stocktoday/`

---

## 3. 配置 Token

**方式 A: 环境变量 (推荐)**
```bash
# Windows (PowerShell)
$env:STOCKTODAY_TOKEN = "your_token_here"

# macOS/Linux
export STOCKTODAY_TOKEN="your_token_here"
```

**方式 B: 在智能体的 MCP 配置里设 env**
```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["~/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

---

## 4. 各智能体集成

### 4.1 Claude Code (CLI)

**配置文件**: `~/.claude/mcp.json` (用户级) 或 `.mcp.json` (项目级)

```bash
# 1) 安装
npx clawhub install stocktoday

# 2) 编辑配置
# Windows: notepad $env:USERPROFILE\.claude\mcp.json
# macOS/Linux: nano ~/.claude/mcp.json
```

```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["${USERPROFILE}/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

> **注意**: Claude Code 路径分隔符 — Windows 用 `${USERPROFILE}`, Mac/Linux 用 `~`

**验证**:
```bash
claude mcp list
# 应输出: stocktoday: node ~/skills/stocktoday/dist/index.js - ✓ Connected
```

---

### 4.2 Claude Desktop

**配置文件路径**:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["C:/Users/<你>/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

**重启 Claude Desktop** 让配置生效。

---

### 4.3 Cursor

**配置文件**: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["~/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

**重启 Cursor** → Settings → MCP → 应看到 stocktoday 已连接。

---

### 4.4 Cline (VS Code 扩展)

**配置文件**:
- Windows: `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

```json
{
  "mcpServers": {
    "stocktoday": {
      "command": "node",
      "args": ["~/skills/stocktoday/dist/index.js"],
      "env": {
        "STOCKTODAY_TOKEN": "your_token_here"
      }
    }
  }
}
```

---

### 4.5 其他 MCP 兼容智能体

任何支持 MCP 协议的智能体都能用, 只需配置:
1. **command**: `node`
2. **args**: `[<安装路径>/dist/index.js]`
3. **env**: `{ "STOCKTODAY_TOKEN": "<你的token>" }`

---

## 5. 升级 / 卸载

```bash
# 升级到最新
npx clawhub update stocktoday

# 升级到指定版本
npx clawhub update stocktoday --version 1.3.5

# 卸载
npx clawhub uninstall stocktoday
```

升级后**不需要**改 MCP 配置, 智能体重启即可生效。

---

## 6. 验证安装

启动智能体后, 试试这些对话:

```
你: 帮我查一下茅台的今天日线
```

```
你: 我这个 token 什么时候到期?
```

```
你: 我能不能查 stk_factor_pro?
```

LLM 应该会调 `daily` / `token_info` 等 tool 返数据。如果失败, 检查:
1. `STOCKTODAY_TOKEN` 是否正确
2. 网络是否能访问 `https://tushare.citydata.club/`
3. Token 积分是否用完 (返 `code:1 msg:请求超限`)

---

## 7. 高级配置 (env vars)

| 环境变量 | 默认 | 说明 |
|---|---|---|
| `STOCKTODAY_TOKEN` | (无) | **必填**, 你的 API token |
| `STOCKTODAY_URL` | `https://tushare.citydata.club/` | 自定义后端地址 |
| `STOCKTODAY_BACKUP_URL1` | `http://111.229.164.2:8083/` | 备用 gateway 1 |
| `STOCKTODAY_BACKUP_URL2` | `http://124.223.112.152:6331/` | 备用 gateway 2 |
| `STOCKTODAY_BACKUP_URL3` | `http://110.42.211.9:9900/` | 备用 gateway 3 |
| `STOCKTODAY_RATE_PER_MIN` | `60` | 每分钟每 token 上限 |
| `STOCKTODAY_MAX_CONCURRENT` | `5` | 全局最大并发 |
| `STOCKTODAY_MAX_RETRIES` | `3` | 单次重试次数 |
| `STOCKTODAY_TOKEN_CACHE_TTL_MS` | `86400000` (24h) | token 缓存 TTL |

---

## 8. 故障排查

| 症状 | 原因 | 解决 |
|---|---|---|
| LLM 调工具返 `code:1 TOKEN无效` | token 错/失效/被封 | 检查 token 有效性 |
| 调工具超时 | 网络问题 / gateway 全挂 | 检查 `tushare.citydata.club` 通不通 |
| 频繁返 `请求超限20000次` | token 当日额度用完 | 明日 0 点重置, 或换 token |
| 智能体里看不到 stocktoday skill | MCP 配置没生效 | 重启智能体, 检查 JSON 路径 |
| Windows 上 ClawHub 检查失败 (EINVAL) | `shell:true` 警告 | 已修, 不影响功能 |

---

## 9. 反馈

- ClawHub: `stocktoday` skill 页面 (publish id `k977hyqhvh194s5qtmk6d5145s88pe3p`)
- 项目目录: `D:\office\stocktoday-skill\`
- SKILL 介绍: `<安装路径>/SKILL.md`
