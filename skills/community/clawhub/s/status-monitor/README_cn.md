# OpenClaw 状态监控

**再也不用问"在吗？"。**

一个自动同步 OpenClaw Agent 状态到云端仪表盘的技能，让你一眼看清谁在线、他们在干什么——无需打断他们。

## 痛点

```
你：在吗？
Agent：在的。
你：最近在忙什么？
Agent：...
```

每次都要问。每次都打断。

你的 Agent 24 小时运行，但你不知道他们在干什么。

## 解决方案

一个实时仪表盘，展示：

- ✅ 哪些 Agent 在线
- 📊 实时活动状态
- 🔔 自动离线检测（5分钟阈值）

## 功能特性

- **无需问"在吗"** - 一眼看清状态，不打断 Agent 的工作节奏
- **自动离线检测** - Dashboard 自动标记 5 分钟无心跳的 Agent 为离线
- **定时同步** - 每 5 分钟通过后台脚本自动更新
- **实时更新** - Agent 上报时 SSE 通知
- **多 Agent 支持** - 所有 Agent，一个仪表盘
- **简单集成** - 只上传 Agent ID，所有业务逻辑由 Dashboard 处理

## 快速开始

详细安装说明请查看 [INSTALL.md](./INSTALL.md)。

**基本步骤：**
1. 安装到 OpenClaw skills 目录
2. 运行 `openclaw gateway restart`
3. 对 OpenClaw 说："启用状态监控"

然后访问 **https://openclaw-agent-monitor.vercel.app** 查看仪表盘。

## 工作原理

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  OpenClaw  │────▶│  上传脚本    │────▶│    仪表盘       │
│   Agents   │     │  (Python)    │     │  (查看在线状态) │
│   (ID列表)  │     │  守护进程    │     │  自动离线检测   │
└─────────────┘     └──────────────┘     └─────────────────┘
```

技能负责管理一个 Python 上传脚本。脚本只上传 Agent ID，业务逻辑由 Dashboard 处理：
- 存储 Agent 元数据（名称、问候语等）
- 计算在线/离线状态
- 生成问候语和展示

## 两种运行模式

### 模式一：Cron 定时同步（默认）

OpenClaw 内置 cron 定时执行，单次调用上传脚本：

```bash
# OpenClaw cron 定时调用（无 start 参数）
python3 scripts/status_uploader.py
```

### 模式二：守护进程模式

需要持续后台运行时，使用 `--fork` 启动真正的守护进程：

| 命令 | 说明 |
|------|------|
| `python3 scripts/status_uploader.py start --fork` | 启动守护进程 |
| `python3 scripts/status_uploader.py start --fork --interval 10` | 启动并指定间隔（分钟） |
| `python3 scripts/status_uploader.py stop` | 停止服务 |
| `python3 scripts/status_uploader.py status` | 查看服务状态 |
| `python3 scripts/status_uploader.py test` | 单次测试上传 |


## 相关文档

- [INSTALL.md](./INSTALL.md) - 详细安装指南
- [README.md](./README.md) - English introduction

## 相关项目

- [OpenClaw Agent Monitor](https://github.com/yahao333/openclaw-agent-monitor) - 监控仪表盘

## 开源协议

MIT
