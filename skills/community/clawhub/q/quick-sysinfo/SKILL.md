---
name: quick-sysinfo
description: 快速查询本机系统信息和OpenClaw配置。包括CPU、内存、磁盘、网络、环境配置、硬件资源占用、Docker容器、OpenClaw配置/频道/插件/服务状态。当用户询问"系统状态"、"CPU使用率"、"内存占用"、"磁盘空间"、"网络信息"、"硬件配置"、"进程状态"、"Docker状态"、"系统负载"、"配置信息"、"OpenClaw状态"时使用此技能。
security_note: "OpenClaw 配置中的敏感字段（api_key、token、secret、password 等）会被自动脱敏显示为 [REDACTED]，不会暴露凭证。脚本所有配置读取均通过统一的脱敏函数处理。"
---

# Quick System Info

## 触发词

系统状态、系统概览、CPU、内存、磁盘、网络、硬件配置、进程状态、Docker状态、系统负载、OpenClaw配置

## 执行方式

```bash
bash scripts/sysinfo.sh [模块]
```

## 模块列表

| 参数 | 功能 |
|------|------|
| `all` (默认) | 系统概览 + OpenClaw 状态 |
| `cpu` | CPU 详细信息和使用率 |
| `mem` | 内存和 Swap 详情 |
| `disk` | 磁盘使用和 IO 统计 |
| `net` | 网络接口和连接数 |
| `env` | 系统环境（OS/内核/软件版本） |
| `load` | 系统负载和 Top 进程 |
| `proc` | 进程统计和服务状态 |
| `gpu` | GPU 信息（NVIDIA/AMD/Intel） |
| `docker` | Docker 容器状态和资源 |
| `openclaw` | OpenClaw 配置（脱敏后）、频道、插件、服务状态 |

## 模块选择

- 用户说"状态"/"概览"/"怎么样" → `all`
- 用户说"CPU" → `cpu`
- 用户说"内存" → `mem`
- 用户说"磁盘" → `disk`
- 用户说"网络" → `net`
- 用户说"配置" → `openclaw`
- 用户说"进程"/"服务" → `proc`
- 多个问题同时问 → 多次调用，合并结果

## 安全说明

所有配置读取均通过统一的脱敏函数处理：
- 匹配字段名：`api_key`、`token`、`secret`、`password` 等 → 显示为 `[REDACTED]`
- 递归扫描：配置各 section 中任意层级匹配即脱敏
- 模型名展示：只取 `provider/model-name` 的 model 部分，凭证部分自动剥离
- 不依赖 inline Python 字符串拼接读取配置，统一走脱敏函数
