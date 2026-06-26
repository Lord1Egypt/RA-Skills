---
name: ssh-remote-skill
description: SSH 远程服务器管理工具。支持多服务器连接管理、命令执行、文件传输、系统监控、服务管理、日志分析、安全检查等功能，适用于 Linux/Unix 服务器运维。
---

# SSH 远程服务器管理

> SSH 远程服务器管理工具，支持多服务器连接管理、命令执行、文件传输、系统监控、服务管理、日志分析、安全检查等功能，适用于 Linux/Unix 服务器运维。

## 功能特性

| 功能模块 | 描述 |
|----------|------|
| 🔌 **连接管理** | 多服务器配置、连接测试、连接池管理 |
| 💻 **命令执行** | 远程命令执行、脚本运行、批量操作 |
| 📤 **文件上传** | 单文件/目录上传、进度显示 |
| 📥 **文件下载** | 单文件/目录下载、文件列表 |
| 📊 **系统监控** | CPU/内存/磁盘/网络/进程监控 |
| ⚙️ **服务管理** | systemctl 服务管理、日志查看 |
| 📋 **日志分析** | 系统/应用日志查看、搜索、分析 |
| 🔒 **安全检查** | 安全扫描、漏洞检查、加固建议 |

## 安装

```bash
npm install
```

## 配置

创建配置文件 `configs/servers.json`:

```json
{
  "servers": [
    {
      "name": "production",
      "host": "YOUR_SERVER_IP",
      "port": 22,
      "username": "YOUR_USERNAME",
      "privateKeyPath": "~/.ssh/id_rsa"
    }
  ]
}
```

## 使用示例

### 连接测试
```
用户：ssh 连接测试
AI: 🔌 服务器连接状态：
   ✅ production - 延迟 25ms
```

### 执行命令
```
用户：ssh 执行 production uptime
AI: 📋 执行结果：
   12:30:00 up 15 days, load average: 0.50
```

### 文件传输
```
用户：ssh 上传 production ./app.js /var/www/
AI: ✅ 文件上传成功！
```

### 系统监控
```
用户：ssh 监控 production
AI: 📊 CPU: 25% | 内存: 50% | 磁盘: 40%
```

## 触发词

- `ssh 连接` - 连接管理
- `ssh 执行` - 执行远程命令
- `ssh 上传` - 上传文件
- `ssh 下载` - 下载文件
- `ssh 监控` - 系统监控
- `ssh 服务` - 服务管理
- `ssh 日志` - 日志查看
- `ssh 安全` - 安全检查

## 依赖

- Node.js >= 18.0.0
- ssh2 ^1.15.0

## License

MIT
