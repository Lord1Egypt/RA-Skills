# SSH Server 技能

通过 SSH 远程连接和操作 Linux/Unix 服务器。

## 功能特性

- 🔐 密码/SSH 密钥认证
- 📡 远程命令执行
- 📊 系统状态监控
- 🐳 Docker 容器管理
- 📝 日志查看
- ⚙️ 服务管理

## 快速开始

### 1. 添加服务器配置

```bash
python D:\openClaw\openclaw\config\ssh_config.py add
```

按提示输入：
- 服务器名称（如 vps, ubuntu）
- 服务器 IP 地址
- 端口（默认 22）
- 用户名（root, ubuntu 等）
- 密码

### 2. 连接到服务器

```bash
python D:\openClaw\openclaw\config\ssh_config.py connect <服务器名称>
```

### 3. 使用 SSH 密钥登录（更安全）

```bash
# 生成本地 SSH 密钥
ssh-keygen -t ed25519

# 复制公钥到服务器
ssh-copy-id user@服务器IP
```

## 常用命令

### 系统状态
```bash
uptime
free -h
df -h
```

### 进程管理
```bash
ps aux
ps aux | grep nginx
```

### 服务管理
```bash
systemctl status nginx
sudo systemctl restart nginx
```

### Docker 操作
```bash
docker ps
docker logs container_name
docker exec -it container_name bash
```

### 日志查看
```bash
sudo journalctl -n 100
sudo journalctl -u nginx
```

## 管理命令

```bash
# 添加服务器
python config/ssh_config.py add

# 列出服务器
python config/ssh_config.py list

# 连接服务器
python config/ssh_config.py connect <名称>

# 删除服务器
python config/ssh_config.py delete <名称>
```

## 安全说明

- 🔐 密码本地加密存储，不会通过聊天传输
- 🔑 推荐使用 SSH 密钥认证
- ⚠️ 执行危险操作前会确认
