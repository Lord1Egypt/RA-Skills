# SSH Remote Skill - SSH 远程服务器管理

> SSH 远程服务器管理工具，支持多服务器连接管理、命令执行、文件传输、系统监控、服务管理、日志分析、安全检查等功能，适用于 Linux/Unix 服务器运维。

---

## 📦 功能特性

| 功能模块 | 描述 |
|----------|------|
| 🔌 **连接管理** | 多服务器配置、连接测试、连接池管理 |
| 💻 **命令执行** | 远程命令执行、脚本运行、批量操作 |
| 📤 **文件上传** | 单文件/目录上传、进度显示、预设模板 |
| 📥 **文件下载** | 单文件/目录下载、文件列表、断点续传 |
| 📊 **系统监控** | CPU/内存/磁盘/网络/进程监控 |
| ⚙️ **服务管理** | systemctl 服务管理、日志查看 |
| 📋 **日志分析** | 系统/应用日志查看、搜索、分析 |
| 🔒 **安全检查** | 安全扫描、漏洞检查、加固建议 |

---

## 🔧 安装

### 1. 安装依赖

```bash
cd ~/.openclaw/skills/ssh-remote
npm install
```

### 2. 配置服务器

复制示例配置文件并修改：

```bash
cp configs/servers.json.example configs/servers.json
```

编辑 `configs/servers.json`:

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

---

## ⚙️ 配置方式

### 方式 A：配置文件（推荐）

```json
{
  "servers": [
    {
      "name": "服务器别名",
      "host": "服务器 IP 或域名",
      "port": 22,
      "username": "SSH 用户名",
      "password": "SSH 密码（或使用私钥）",
      "privateKeyPath": "~/.ssh/id_rsa",
      "passphrase": "私钥密码（如有）"
    }
  ]
}
```

### 方式 B：环境变量

```bash
export SSH_NAME="production"
export SSH_HOST="YOUR_SERVER_IP"
export SSH_PORT="22"
export SSH_USERNAME="YOUR_USERNAME"
export SSH_PASSWORD="YOUR_PASSWORD"
# 或使用私钥
export SSH_PRIVATE_KEY="~/.ssh/id_rsa"
```

---

## 💡 使用示例

### 1. 连接管理

```
用户：ssh 连接测试
AI: 🔌 服务器连接状态：
   ✅ production (192.168.1.100) - 延迟 25ms
```

### 2. 执行命令

```
用户：ssh 执行 production uptime
AI: 📋 执行结果：
   12:30:00 up 15 days,  2:30,  1 user,  load average: 0.50, 0.45, 0.40
```

### 3. 文件传输

```
用户：ssh 上传 production ./app.js /var/www/app.js
AI: ✅ 文件上传成功！
   本地：./app.js (2.5KB)
   远程：/var/www/app.js
```

### 4. 系统监控

```
用户：ssh 监控 production
AI: 📊 服务器监控 (production):
   🖥️ CPU: 4 核心，使用率 25%
   💾 内存：8GB (4GB/8GB 50%)
   💿 磁盘：50GB (20GB/50GB 40%)
```

---

## 📖 API 参考

### 连接管理 (connect.js)

| 方法 | 描述 |
|------|------|
| `listServers()` | 列出所有服务器 |
| `testServer(name)` | 测试单个服务器连接 |
| `testAllServers()` | 测试所有服务器 |
| `addServer(config)` | 添加服务器配置 |
| `removeServer(name)` | 删除服务器配置 |

### 命令执行 (exec.js)

| 方法 | 描述 |
|------|------|
| `execCommand(server, cmd)` | 执行单个命令 |
| `execCommands(server, cmds)` | 执行多个命令 |
| `getSystemOverview(server)` | 获取系统概览 |
| `execOnMultiple(servers, cmd)` | 批量执行 |

### 文件传输 (upload.js / download.js)

| 方法 | 描述 |
|------|------|
| `upload(server, local, remote)` | 上传文件 |
| `uploadDirectory(server, local, remote)` | 上传目录 |
| `download(server, remote, local)` | 下载文件 |
| `listRemoteFiles(server, path)` | 列出远程文件 |

### 系统监控 (monitor.js)

| 方法 | 描述 |
|------|------|
| `getCPUInfo(server)` | CPU 信息 |
| `getMemoryInfo(server)` | 内存信息 |
| `getDiskInfo(server)` | 磁盘信息 |
| `getSystemOverview(server)` | 系统概览 |
| `getSystemAlerts(server)` | 系统告警 |

### 服务管理 (service.js)

| 方法 | 描述 |
|------|------|
| `listServices(server)` | 列出服务 |
| `getServiceStatus(server, name)` | 服务状态 |
| `startService(server, name)` | 启动服务 |
| `stopService(server, name)` | 停止服务 |
| `restartService(server, name)` | 重启服务 |

### 日志管理 (log.js)

| 方法 | 描述 |
|------|------|
| `viewSystemLog(server)` | 系统日志 |
| `viewNginxLog(server)` | Nginx 日志 |
| `searchLog(server, file, pattern)` | 搜索日志 |
| `getLogSummary(server)` | 日志摘要 |

### 安全检查 (security.js)

| 方法 | 描述 |
|------|------|
| `checkSSHSecurity(server)` | SSH 安全检查 |
| `checkFirewall(server)` | 防火墙检查 |
| `generateSecurityReport(server)` | 安全报告 |
| `getSecurityRecommendations(server)` | 加固建议 |

---

## 🔍 触发词

| 功能 | 触发词 |
|------|--------|
| 连接 | "ssh 连接", "ssh connect", "ssh 登录" |
| 执行 | "ssh 执行", "ssh exec", "远程命令" |
| 上传 | "ssh 上传", "ssh upload" |
| 下载 | "ssh 下载", "ssh download" |
| 监控 | "ssh 监控", "ssh monitor", "服务器状态" |
| 服务 | "ssh 服务", "ssh service", "systemctl" |
| 日志 | "ssh 日志", "ssh log", "查看日志" |
| 安全 | "ssh 安全", "ssh security", "安全检查" |

---

## ⚠️ 注意事项

1. **凭证安全**：妥善保管 SSH 密码和私钥，不要提交到代码仓库
2. **权限控制**：确保 SSH 用户有足够权限
3. **连接池**：避免创建过多并发连接
4. **命令安全**：避免执行危险命令（如 `rm -rf /`）
5. **生产环境**：生产环境操作前请备份

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| ssh2 文档 | https://github.com/mscdex/ssh2 |
| OpenSSH 配置 | https://www.openssh.com/manual.html |
| Linux 系统管理 | https://linux.die.net |

---

## 📄 License

MIT

---

*创建时间：2026-02-26*
