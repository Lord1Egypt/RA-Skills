---
name: v2ray-proxy
description: V2Ray代理管理 - 自动开关代理、根据网络状况自动配置系统代理 / V2Ray Proxy Management - Auto start/stop proxy based on network conditions
---

# V2Ray 代理管理 / V2Ray Proxy Management

管理 V2Ray 代理的自动开关，根据网络状况自动配置系统代理。

Manage V2Ray proxy auto start/stop and system proxy configuration based on network conditions.

## 功能 / Features

- 🚀 启动/停止 V2Ray / Start/Stop V2Ray
- 🌐 自动配置/清除系统代理 / Auto configure/clear system proxy
- 🔄 自动模式（根据网络状况自动开关）/ Auto mode (auto switch based on network)
- 📊 状态查看和连接测试 / Status check and connection test

## 配置 / Configuration

- V2Ray位置 / Location: `/media/felix/d/v2rayN-linux-64/`
- 代理端口 / Proxy port: `10808`

## 使用 / Usage

```bash
# 开启代理 / Enable proxy
./scripts/v2ray-proxy.sh on

# 关闭代理 / Disable proxy  
./scripts/v2ray-proxy.sh off

# 自动模式 / Auto mode
./scripts/v2ray-proxy.sh auto

# 查看状态 / Check status
./scripts/v2ray-proxy.sh status
```
