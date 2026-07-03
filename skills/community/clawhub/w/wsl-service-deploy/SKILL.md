---
name: wsl-service-deploy
description: >-
  WSL Ubuntu 服务一键部署。通过 wsl.exe + su -c root + aptitude，无需 SSH 即可在 Windows 宿主机上安全、快速地安装和管理后端服务。
  覆盖 MySQL、Redis、Nginx、PostgreSQL、MongoDB 等任意 aptitude 可搜到的包。适用场景：WSL 运维、服务安装、环境搭建。
agent_created: true
---

# WSL Service Deploy

在 Windows 宿主机的 WSL Ubuntu 中，通过 `wsl.exe` 直接执行命令，使用 aptitude 包管理器安装和管理后端服务。

## 核心工作流

### 原则

1. **首选 `wsl.exe -e bash -c`** — 直接从 Windows 侧调用 WSL 命令，无需 SSH
2. **以 root 执行** — 使用 `echo '<root密码>' | su -c '<命令>' - root` 绕过 sudo 密码
3. **脚本先写再跑** — 将多步操作写入 `/tmp/` 脚本，一次性执行，通过 `/tmp/*.log` 查看结果
4. **用 aptitude 不用 apt** — aptitude 依赖处理更可靠

### 标准执行模式

```bash
# 第一步：在 WSL 中写入安装脚本
wsl.exe -e bash -c 'cat > /tmp/install_<service>.sh << "EOF"
#!/bin/bash
set -e
exec &> /tmp/install_<service>.log
echo "=== START $(date) ==="
# ... 安装步骤 ...
echo "=== END $(date) ==="
EOF
chmod +x /tmp/install_<service>.sh'

# 第二步：以 root 执行脚本（后台运行，避免超时）
wsl.exe -e bash -c "echo '<root密码>' | su -c 'bash /tmp/install_<service>.sh' - root" &

# 第三步：等待后检查日志（sleep 时间视包大小调整：Redis~10s，MySQL~30-60s）
sleep 10
wsl.exe -e bash -c 'tail -30 /tmp/install_<service>.log'
```

### 卸载服务

```bash
systemctl stop <service>
DEBIAN_FRONTEND=noninteractive aptitude purge -y <package-names>
rm -rf <data-directories>
aptitude purge -y ~c   # 清理残留配置
```

### 检查状态

```bash
wsl.exe -e bash -c 'systemctl status <service> --no-pager; ss -tlnp | grep <port>'
```

## 通用部署流程（适用于 aptitude search 找到的任何包）

当用户要求安装一个不在下方速查表中的服务时，按以下步骤自行推理：

1. **搜索包名** — `aptitude search <关键词> | head -20`
2. **确定包名** — 通常就是 `<服务名>` 或 `<服务名>-server`（如 `nginx`、`postgresql`）
3. **查端口和配置路径** — `aptitude show <包名> | grep -E "Homepage|Depends"`，或用 `dpkg -L <包名>` 安装后查看
4. **套用标准执行模式** — 写入 `/tmp/install_<service>.sh`，通过 `su -c` 执行
5. **安装后操作**：
   - `systemctl enable <service> && systemctl start <service>` — 自启 + 启动
   - 有配置文件则 `cp <config> <config>.bak` 备份后修改
   - 有默认认证则通过服务自带 CLI 设置密码
6. **验证** — 版本号 + 端口监听 + 功能测试

**示例**：用户说"装 Nginx"
→ 搜索 `nginx` → 包名 `nginx` → 写脚本安装 → `systemctl enable nginx` → 验证 `curl localhost`

## 服务速查表

### MySQL

- **包名**: `mysql-server`
- **数据目录**: `/var/lib/mysql`
- **配置目录**: `/etc/mysql`
- **root 密码**: 安装后通过 `ALTER USER` 设置
- **认证插件**: `mysql_native_password`
- **默认端口**: 3306 (MySQL), 33060 (X Protocol)
- **自启**: `systemctl enable mysql`

### Redis

- **包名**: `redis-server`
- **配置文件**: `/etc/redis/redis.conf`
- **关键配置**:
  - `requirepass <密码>` — 设置认证密码
  - `bind 0.0.0.0` — 允许外部连接
- **默认端口**: 6379
- **验证**: `redis-cli -a <密码> PING`
- **自启**: `systemctl enable redis-server`

## 通用规范

- 安装前先 `apt update`（镜像源已配置为阿里云）
- 安装前确认包未安装：`which <binary> || echo NOT_INSTALLED`
- 安装前清理残留锁文件：`rm -f /var/lib/dpkg/lock* /var/lib/apt/lists/lock /var/cache/apt/archives/lock`
- 有残留 dpkg 进程时先 `killall apt; killall dpkg; dpkg --configure -a`（需在 root 下执行）
- 修改配置文件前先备份：`cp <config> <config>.bak`
- 安装完成后必须验证：密码登录、版本号、端口监听

## 环境信息

详见 `references/wsl-commands.md`，关键参数：

| 项目 | 值 |
|------|-----|
| Ubuntu 版本 | 26.04 LTS (resolute) |
| 镜像源 | `https://mirrors.aliyun.com/ubuntu/` |
| Root 密码 | `123456` |
| 包管理器 | aptitude |

## 注意事项

- **WSL IP 动态变化**：SSH 方式不可靠，优先用 `wsl.exe` 直接调用
- **安全策略**：需要在 WorkBuddy 安全中心启用「系统级工具」策略
- **多层引号**：`wsl.exe -e bash -c` 中避免复杂嵌套引号，改用 heredoc 脚本
- **前台超时**：长时间操作（下载/安装）用后台执行 + 日志轮询
