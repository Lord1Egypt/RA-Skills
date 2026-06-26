# OpenClaw Status Monitor 安装指南

## 功能说明

定时将 OpenClaw Agent 状态同步到云端监控平台（https://openclaw-agent-monitor.vercel.app）。技能只上传 Agent ID 列表，离线判断和其他业务逻辑由监控平台处理。

## 安装步骤

### 方式一：从 GitHub 安装（推荐）

```bash
# 克隆到本地
cd ~/.openclaw/skills
git clone git@github.com:yahao333/openclaw-status-monitor.git
```

### 方式二：手动安装

1. 下载或复制 `openclaw-status-monitor` 目录到 `~/.openclaw/skills/`
2. 确保目录结构如下：
   ```
   ~/.openclaw/skills/openclaw-status-monitor/
   ├── SKILL.md
   ├── README.md
   ├── README_cn.md
   ├── INSTALL.md
   └── scripts/
       └── status_uploader.py
   ```

## 首次配置

### 1. 重启 OpenClaw

安装后需要重启 OpenClaw 使技能生效：
```bash
# 重启 openclaw 服务
openclaw gateway restart
```

### 2. 触发技能初始化

对 OpenClaw 说：
```
启用状态监控
```

或
```
开启监控同步
```

### 3. 配置 Token

首次使用会提示配置 Token：

1. 访问 https://openclaw-agent-monitor.vercel.app
2. 点击 **Sign In** 登录（支持 Google/GitHub 等）
3. 登录后在 **Settings** 页面生成 Agent Token
4. 将 Token 发送给 OpenClaw

### 4. 完成初始化

Token 配置成功后，会自动启动上传服务。

## 使用命令

| 命令 | 说明 |
|------|------|
| `同步状态` | 手动触发一次上传 |
| `启用状态监控` | 首次启用引导 |
| `查看状态监控` | 检查服务状态 |
| `停止状态监控` | 停止上传服务 |
| `每10分钟同步一次` | 修改同步间隔 |

## 上传脚本管理

脚本位置：`~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py`

| 命令 | 说明 |
|------|------|
| `python3 scripts/status_uploader.py start` | 启动上传服务（默认5分钟间隔） |
| `python3 scripts/status_uploader.py start --interval 10` | 启动并指定间隔（分钟） |
| `python3 scripts/status_uploader.py stop` | 停止上传服务 |
| `python3 scripts/status_uploader.py status` | 查看服务状态和当前间隔 |
| `python3 scripts/status_uploader.py set-interval 10` | 设置同步间隔（分钟） |
| `python3 scripts/status_uploader.py test` | 单次测试上传 |

**示例：**
```bash
# 启动时指定 10 分钟间隔
python3 scripts/status_uploader.py start --interval 10

# 修改间隔为 15 分钟
python3 scripts/status_uploader.py set-interval 15
```

## 上传间隔

- 默认：5 分钟
- 上传数据：Agent ID 数组，如 `[{id: "main"}, {id: "coding"}, ...]`

## 数据流程

```
OpenClaw Agent ──▶ Python 脚本 ──▶ Dashboard API
   (读取 ID)        (守护进程)      (存储 + 离线判断)
```

- 脚本每 5 分钟读取 `openclaw.json` 获取所有 Agent ID
- 上传格式：`[{id: "agentId"}, ...]`
- Dashboard 根据上传时间自动判断在线/离线（5分钟阈值）

## 配置文件

| 文件 | 说明 |
|------|------|
| `~/.openclaw/credentials/openclaw-status-monitor.json` | Token 和同步间隔配置 |
| `~/.openclaw/logs/status_uploader.log` | 服务运行日志 |
| `~/.openclaw/logs/status_uploader_error.log` | 错误日志 |
| `~/.openclaw/logs/status_uploader.pid` | 进程 PID |

**配置文件示例：**
```json
{
  "agentToken": "your-token-here",
  "monitorUrl": "https://openclaw-agent-monitor.vercel.app",
  "syncIntervalMinutes": 5
}
```

## 常见问题

### Q: 重启后技能不识别？
A: 确保 `.skill` 文件或目录在 `~/.openclaw/skills/` 下，重启 OpenClaw。

### Q: Token 验证失败？
A: Token 可能过期或无效，请重新在 Settings 页面生成新 Token。

### Q: 如何查看服务状态？
A: 对 OpenClaw 说"查看状态监控"，或运行 `python3 scripts/status_uploader.py status`。

### Q: 服务没在运行？
A: 运行 `python3 scripts/status_uploader.py start` 启动服务。

### Q: 如何停止服务？
A: 运行 `python3 scripts/status_uploader.py stop`，或对 OpenClaw 说"停止状态监控"。

## 卸载

```bash
# 停止上传服务
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py stop

# 删除技能目录
rm -rf ~/.openclaw/skills/openclaw-status-monitor

# 删除配置文件（可选）
rm -rf ~/.openclaw/credentials/openclaw-status-monitor.json
rm -rf ~/.openclaw/logs/status_uploader*
```
