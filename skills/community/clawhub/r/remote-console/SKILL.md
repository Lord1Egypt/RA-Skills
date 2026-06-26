---
name: remote-console
description: |
  通过手机/浏览器远程访问主机上的 Claude Code 或其他 CLI 工具。使用此技能来启动、停止和管理远程开发环境。

  **必须触发此技能的场景**：
  - 用户提到"远程控制台"、"远程终端"、"远程开发"、"ttyd"、"SSH 隧道"
  - 用户想用手机/平板访问电脑上的开发环境
  - 用户提到"移动端编程"、"手机写代码"、"远程编码"
  - 用户要添加/删除/查看项目路径
  - 用户要添加/设置/查看命令配置
  - 用户要关闭或停止远程控制台
  - 用户询问如何在外出时继续编程

  **不要触发**：普通 SSH 连接、服务器部署、日志查看等非远程控制台任务。
---

# 远程控制台 Skill

通过 ttyd + SSH 隧道，在手机浏览器中访问主机上的 Claude Code。

## ⚠️ 重要：优先使用 Python 脚本

**所有操作必须通过 Python 脚本执行，禁止直接拼接 Shell 命令！**

脚本目录：`./scripts/`（与 SKILL.md 同目录）

### 前置依赖

```bash
pip install psutil
```

---

## 快速命令

### 启动远程控制台

```bash
python ./scripts/start_console.py <项目名>
python ./scripts/start_console.py <项目名> -c <命令名>
python ./scripts/start_console.py --path /path/to/project
```

### 停止远程控制台

```bash
python ./scripts/stop_console.py
```

### 检查状态

```bash
python ./scripts/check_tunnel.py
python ./scripts/check_tunnel.py --json
```

### 验证配置

```bash
python ./scripts/validate_config.py
```

---

## 用户操作指南

### 1. 启动远程控制台

**触发**: "打开 {项目名} 的远程控制台"

**执行**:
```bash
python ./scripts/start_console.py {项目名}
```

**返回格式**:
```
✅ 远程控制台已启动

📁 项目：{项目名称}
🔗 访问地址：http://{host}:{port}
📂 工作目录：{project.path}
🚀 启动命令：{command}
```

### 2. 停止远程控制台

**触发**: "关闭远程控制台" / "停止远程终端"

**执行**:
```bash
python ./scripts/stop_console.py
```

### 3. 检查状态

**触发**: "远程控制台状态" / "检查隧道"

**执行**:
```bash
python ./scripts/check_tunnel.py
```

### 4. 验证配置

**触发**: "验证远程控制台配置"

**执行**:
```bash
python ./scripts/validate_config.py
```

### 5. 项目管理

**查看所有项目**:
```bash
python ./scripts/start_console.py
```

---

## 配置文件

配置文件：`./config.json`（与 SKILL.md 同目录）

```json
{
  "servers": {
    "default": {
      "name": "my-server",
      "host": "your-server.com",
      "port": 2222,
      "user": "your-username",
      "ssh_alias": "ssh-config-alias"
    }
  },
  "ttyd": {
    "port": 7681,
    "path": "ttyd",
    "options": "-W -t fontSize=16"
  },
  "defaults": {
    "command": "claude",
    "server": "default"
  },
  "commands": {
    "claude": "claude",
    "claude-bypass": "claude --dangerously-skip-permissions",
    "codex": "codex"
  },
  "projects": {
    "项目名": {
      "path": "/path/to/project",
      "command": "claude-bypass"
    }
  }
}
```

---

## 预定义命令

| 名称 | 实际命令 | 说明 |
|------|---------|------|
| claude | `claude` | 标准 Claude Code |
| claude-bypass | `claude --dangerously-skip-permissions` | ⚠️ 跳过权限检查 |
| codex | `codex` | OpenAI Codex |
| cursor | `cursor-agent` | Cursor Agent |

---

## ⚠️ 安全警告

### claude-bypass 命令风险

`claude-bypass` 使用 `--dangerously-skip-permissions` 标志，会**跳过所有权限检查**。

**仅在以下情况使用**：
- ✅ 完全信任的私有网络环境
- ✅ 个人非敏感项目
- ✅ 你了解并接受所有操作将自动执行

**绝不使用于**：
- ❌ 生产环境或敏感数据处理
- ❌ 公共或共享网络
- ❌ 不确定安全性的项目

---

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 链接无法访问 | 运行 `check_tunnel.py` 检查隧道状态 |
| 配置错误 | 运行 `validate_config.py` 验证配置 |
| 端口被占用 | 运行 `stop_console.py` 先停止再启动 |

---

## 架构

```
手机浏览器 → 服务器:{port} → SSH 隧道 → 主机 ttyd → Shell + Claude Code
```

---

## 首次使用检查清单

1. **安装依赖**: `pip install psutil`
2. **配置文件**: 修改 `config.json` 中的服务器信息
3. **SSH 密钥**: 确保免密登录 `ssh {ssh_alias} echo test`
4. **ttyd 安装**: Windows `scoop install ttyd`，Linux `sudo apt install ttyd`
5. **服务器配置**: `GatewayPorts yes` 和 `AllowTcpForwarding yes`
6. **验证**: 运行 `python ./scripts/validate_config.py`
