# SSH Deploy Skill - 通用 SSH 远程部署工具

> ⚠️ **重要说明**：本文档为参考文档。完整、最新的文档请阅读英文主版本：[README.md](./README.md)

本技能提供通过 paramiko 管理任意 Linux 服务器的能力，专为国内网络环境优化。

## 核心功能

- ✅ **SSH 密钥/密码管理** - 安全存储和自动连接
- ✅ **远程命令执行** - 单机/批量并行/顺序执行
- ✅ **文件传输** - SCP 上传/下载
- ✅ **服务器清单管理** - 分组、标签、动态 SSH config
- ✅ **安装脚本模板** - Docker、MySQL、PostgreSQL、Nginx、Node.js、Redis、Python、Git
- ✅ **国内镜像源自动配置** - 阿里云、清华、中科大

## 快速开始

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/skills/ssh-deploy-skill
pip3 install paramiko
```

### 2. 配置服务器（三种方式）

**方式 A：使用 inventory.py（推荐）**

```bash
python3 scripts/inventory.py add web-01 \
  --host 192.168.1.101 \
  --user root \
  --ssh-key ~/.ssh/id_rsa \
  --groups production,web \
  --tags "阿里云"
```

**方式 B：编辑 `~/.ssh-deploy/inventory.json`**

```json
{
  "servers": {
    "web-01": {
      "host": "192.168.1.101",
      "user": "root",
      "ssh_key": "~/.ssh/id_rsa",
      "groups": ["web", "production"],
      "tags": ["阿里云"]
    }
  }
}
```

**方式 C：直接使用 `~/.ssh/config`（无需额外配置）**

```bash
# ~/.ssh/config
Host myserver
    HostName 1.2.3.4
    User root
    IdentityFile ~/.ssh/id_rsa

# 直接使用
python3 scripts/deploy.py exec myserver "uptime"
```

> SSH config 的服务器是动态只读的。如需分组/标签，用 `inventory.py add --from-ssh-config` 导入。

### 3. 执行部署

```bash
# 单台
python3 scripts/deploy.py exec web-01 "uptime"

# 按分组批量
python3 scripts/deploy.py exec group:production "docker ps"

# 按标签批量
python3 scripts/deploy.py exec tag:aliyun "systemctl status nginx"

# 顺序执行（大 batch）
python3 scripts/deploy.py exec group:large "apt upgrade -y" --sequential

# 使用模板
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"
cat templates/install_mysql.sh | python3 scripts/deploy.py exec db-01 "bash -s"  # MYSQL_ROOT_PASSWORD=xxx

# 文件传输
python3 scripts/deploy.py upload web-01 ./nginx.conf /etc/nginx/nginx.conf
python3 scripts/deploy.py download web-01 /var/log/app.log ./logs/
```

## 目标语法

在 `deploy.py` 中指定目标服务器：
- `server-name` - 具体服务器
- `group:分组名` - 所有该分组的服务器
- `tag:标签名` - 所有包含该标签的服务器
- `*` - 所有服务器

## 模板列表

| 模板 | 功能 | 国内镜像 | 环境变量 |
|------|------|----------|----------|
| `base_setup.sh` | 基础环境配置 | ✅ | - |
| `install_docker.sh` | Docker CE + 加速器 | ✅ | - |
| `install_mysql.sh` | MySQL 8.0 | ✅ | MYSQL_ROOT_PASSWORD |
| `install_postgresql.sh` | PostgreSQL 15 | ✅ | PG_VERSION |
| `install_nginx.sh` | Nginx | ❌ | - |
| `install_nodejs.sh` | Node.js | ✅（npm） | NODE_VERSION |
| `install_redis.sh` | Redis | ❌ | - |
| `install_python.sh` | Python | ✅（pip） | PYTHON_VERSION |
| `install_git.sh` | Git | ❌ | GIT_USER_NAME, GIT_USER_EMAIL |

## 完整文档结构

- **[README.md](./README.md)** ⭐ **英文主文档**（推荐阅读）
- **[README.zh-CN.md](./README.zh-CN.md)** 本文件（简化版，参考用）
- `references/best-practices.md` - 最佳实践详细指南
- `references/mirrors.md` - 国内镜像源配置详解
- `references/troubleshooting.md` - 故障排查完整手册

## 常用命令速查

```bash
# 清单管理
python3 scripts/inventory.py list                          # 列出所有
python3 scripts/inventory.py list --group production      # 按分组
python3 scripts/inventory.py add <name> [options]         # 添加

# 部署
python3 scripts/deploy.py exec <target> "<command>"       # 执行命令
python3 scripts/deploy.py upload <target> <local> <remote> # 上传
python3 scripts/deploy.py download <target> <remote> <local> # 下载

# 使用模板
cat templates/install_<软件>.sh | python3 scripts/deploy.py exec <target> "bash -s"
```

## 安全建议

### SSH 密钥认证
- **使用 SSH 密钥**，禁用密码登录
- **创建专用部署用户**，不使用 root 执行日常操作
- **配置免密码 sudo**（仅限必要命令）
- **不在 inventory.json 中存储密码**，优先使用密钥
- **密钥文件权限 600**，服务器端 `authorized_keys` 权限 600
- **SSH 服务配置**：`PermitRootLogin no`, `PasswordAuthentication no`

### 严格主机密钥验证（--strict）

默认情况下，工具自动接受新主机密钥（类似 `ssh -o StrictHostKeyChecking=no`），方便首次连接。生产环境建议启用严格模式：

```bash
python3 scripts/deploy.py --strict exec web-01 "uptime"
```

严格模式行为：
- 加载 `~/.ssh/known_hosts`
- 拒绝未知或已更改的主机密钥
- 首次连接新服务器会失败（`BadHostKeyException`）
- 必须手动确认指纹：`ssh root@server` 一次

**使用严格模式**：
- 生产环境
- 多租户或不信任网络
- 合规审计要求

**不使用严格模式**：
- 初始服务器配置阶段
- 隔离的测试环境
- 临时测试服务器

### 密码认证警告

工具会检测 inventory 中是否使用密码认证（明文存储在 `inventory.json`），并显示警告：

```
⚠️  检测到以下服务器使用密码认证（不推荐）：web-old, db-test
   建议：使用 SSH 密钥认证，避免明文存储密码。
   参考：https://docs.openclaw.ai/security/ssh-keys
```

**强烈建议**：始终使用 SSH 密钥认证，从 `inventory.json` 中删除 `password` 字段。

## 故障排查

### 1. 连接失败

```bash
ping <host>
telnet <host> 22
ssh -i ~/.ssh/id_rsa <user>@<host> "uptime"
```

常见原因：
- 服务器未开机或网络不通
- SSH 服务未启动：`systemctl start sshd`
- 防火墙/安全组未开放 22 端口

### 2. 认证失败

```bash
chmod 600 ~/.ssh/id_rsa*
# 检查服务器：ls -la ~/.ssh/authorized_keys (权限 600)
```

### 3. 命令找不到

```bash
# 使用绝对路径或 source 环境
python3 scripts/deploy.py exec <server> "source ~/.bashrc && <command>"
```

### 4. 国内下载慢

```bash
# 配置国内镜像
cat templates/base_setup.sh | python3 scripts/deploy.py exec <target> "bash -s"
```

### 5. sudo 需要密码

- 方案 A：使用 root 用户
- 方案 B：配置 `/etc/sudoers` 添加 `deploy ALL=(ALL) NOPASSWD:ALL`

完整故障排查指南：`references/troubleshooting.md`

## 示例场景

### 全新服务器初始化

```bash
# 1. 添加服务器
python3 scripts/inventory.py add web-01 \
  --host 1.2.3.101 \
  --groups web,production \
  --tags "aliyun"

# 2. 基础环境配置（镜像源）
cat templates/base_setup.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# 3. 安装 Docker
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# 4. 上传配置
python3 scripts/deploy.py upload web-01 ./nginx.conf /etc/nginx/nginx.conf

# 5. 启动服务
python3 scripts/deploy.py exec web-01 "docker-compose up -d"
```

### 批量部署多台服务器

```bash
# 批量添加到同一分组
for i in 1 2 3; do
  python3 scripts/inventory.py add web-$i \
    --host 1.2.3.10$i \
    --groups web \
    --tags "production"
done

# 批量安装
cat templates/install_docker.sh | python3 scripts/deploy.py exec group:web "bash -s"
python3 scripts/deploy.py upload group:web ./app-config.json /opt/app/config.json
```

### 灰度发布

```bash
# 第一阶段：灰度组
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:"canary" "bash -s"

# 检查监控...

# 第二阶段：全量
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:production "bash -s"
```

### 巡检

```bash
# 批量收集状态
python3 scripts/deploy.py exec "*" "uptime" > uptime-$(date +%F).log
python3 scripts/deploy.py exec "*" "df -h" > disk-$(date +%F).log
python3 scripts/deploy.py exec "*" "docker ps" > containers-$(date +%F).log
```

## 集成 CI/CD

### GitLab CI 示例

```yaml
stages:
  - deploy

deploy_production:
  stage: deploy
  script:
    - pip3 install paramiko
    - export TARGET="group:production"
    - cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "$TARGET" "bash -s"
  only:
    - main
```

### GitHub Actions 示例

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install paramiko
        run: pip3 install paramiko
      - name: Deploy
        run: |
          cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "group:staging" "bash -s"
```

## 主要变更（相比旧版本）

- ✅ **新增 SSH config 直接读取** - 无需额外配置即可使用 `~/.ssh/config` 中的 Host
- ✅ **更好的分组/标签系统** - 灵活的服务器筛选
- ✅ **国内镜像全面优化** - 系统、npm、pip、Docker、Go、Maven
- ✅ **安装模板化** - 一键安装常见软件
- ✅ **更简洁的接口** - 单命令完成操作
- 🔒 **严格主机密钥验证** - `--strict` 选项，生产环境安全加固
- ⚠️ **密码认证警告** - 自动检测并警告密码使用
- 🧵 **线程安全** - 修复多线程环境下的竞态条件

## 获取帮助

- 阅读英文主文档：`README.md`
- 查看最佳实践：`references/best-practices.md`
- 故障排查：`references/troubleshooting.md`
- 镜像配置：`references/mirrors.md`

## 贡献与协议

MIT License。欢迎提交 Issue 和 PR。
