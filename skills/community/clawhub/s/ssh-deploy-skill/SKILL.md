---
name: ssh-deploy-skill
description: Universal SSH remote deployment tool - multi-server management, batch deployment, installation script templates with domestic mirror optimization. Supports remote installation of Git, Docker, MySQL, PostgreSQL, Nginx, Node.js, Redis, Python and more.
when: Use when you need to deploy Linux servers remotely, batch install software, or manage SSH connections (install Docker, configure databases, sync files across servers)
examples:
  - user: Install Docker on my server
    assistant: Use ssh-deploy to install Docker
  - user: Deploy environment on three servers at once
    assistant: Use ssh-deploy for batch deployment
  - user: Configure Aliyun mirrors on new server
    assistant: Use ssh-deploy to set up domestic mirrors
  - user: Upload config files to all backend servers
    assistant: Use ssh-deploy to upload files in batch
  - user: Run database migrations on all test servers
    assistant: Use ssh-deploy to execute batch commands
metadata:
  openclaw:
    emoji: 🚀
    requires:
      python: ">=3.8"
      bins: ["python3", "ssh", "scp"]
    install:
      - id: paramiko
        kind: pip
        package: paramiko
        label: Install paramiko (SSH library)
---

# SSH Deploy Skill

A universal SSH remote deployment tool for managing Linux servers with batch operations, file transfers, and templated software installations. Optimized for domestic network environments with built-in mirror configuration for Chinese mirrors (Aliyun, Tsinghua, etc.).

## Quick Start

### 1. Initial Setup

```bash
cd /root/.openclaw/workspace/skills/ssh-deploy-skill

# Auto setup (checks dependencies, creates config)
bash scripts/setup.sh

# Manual dependency install if auto fails
pip3 install --user paramiko
```

### 2. Configure Servers (Two Methods)

#### Method A: Use inventory.json (Traditional)

Edit `~/.ssh-deploy/inventory.json` or add servers via CLI:

```bash
python3 scripts/inventory.py add web-01 \
  --host 192.168.1.101 \
  --user root \
  --ssh-key ~/.ssh/id_rsa \
  --groups production,web \
  --tags "aliyun"
```

**Config location**: All server configurations are saved in `~/.ssh-deploy/inventory.json`.

#### Method B: Read Directly from ~/.ssh/config (New!)

If you already have Host entries in `~/.ssh/config`, use them **without any additional configuration**:

```bash
# ~/.ssh/config example
Host dy-c1
    HostName 101.126.92.30
    User root
    IdentityFile ~/.ssh/mypc_id_rsa
    Port 22

# Execute directly using host name
python3 scripts/deploy.py exec dy-c1 "ls -la /opt"
```

The tool automatically parses `Host`, `HostName`, `Port`, `User`, `IdentityFile` fields from your SSH config.

> **Note**: Servers loaded from SSH config are **read-only** and not saved to inventory. To add groups/tags, import them: `inventory.py add --from-ssh-config`.

### 3. Execute Remote Commands

```bash
# Single server
python3 scripts/deploy.py exec web-01 "uptime && df -h"

# Batch by group
python3 scripts/deploy.py exec group:production "docker ps"

# Batch by tag
python3 scripts/deploy.py exec tag:aliyun "systemctl status nginx"

# Sequential execution (avoid high load)
python3 scripts/deploy.py exec group:large "apt update" --sequential
```

### 4. File Transfers

```bash
# Upload file
python3 scripts/deploy.py upload web-01 ./nginx.conf /etc/nginx/nginx.conf

# Batch upload to all group servers
python3 scripts/deploy.py upload group:web ./config.json /opt/app/config.json

# Download file
python3 scripts/deploy.py download web-01 /var/log/nginx/access.log ./logs/
```

### 5. Use Templates for Software Installation

All templates in `templates/` come pre-configured with domestic mirrors.

```bash
# Install Docker (auto-configured with China mirrors)
cat templates/install_docker.sh | python3 scripts/deploy.py exec tag:docker "bash -s"

# Install MySQL (password via environment variable)
MYSQL_ROOT_PASSWORD=YourPass123 cat templates/install_mysql.sh | \
  python3 scripts/deploy.py exec db-01 "bash -s"

# Base setup (system updates + mirrors)
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:all "bash -s"
```

## 📦 Installation Script Templates

| Template | Software | China Mirror | Env Vars |
|----------|----------|--------------|----------|
| `base_setup.sh` | Base environment | ✅ | - |
| `install_git.sh` | Git | ❌ | GIT_USER_NAME, GIT_USER_EMAIL |
| `install_docker.sh` | Docker CE +加速器 | ✅ | - |
| `install_mysql.sh` | MySQL 8.0 | ✅ | MYSQL_ROOT_PASSWORD |
| `install_postgresql.sh` | PostgreSQL 15 | ✅ | PG_VERSION |
| `install_nginx.sh` | Nginx | ❌ | - |
| `install_nodejs.sh` | Node.js | ✅ (npm) | NODE_VERSION |
| `install_redis.sh` | Redis | ❌ | - |
| `install_python.sh` | Python | ✅ (pip) | PYTHON_VERSION |

> **Note**: All added server configs are saved to `~/.ssh-deploy/inventory.json`.

## 🎯 Core Features

### Server Inventory Management (`inventory.py`)

```bash
# List all servers
python3 scripts/inventory.py list

# Filter by group
python3 scripts/inventory.py list --group production

# Filter by tag
python3 scripts/inventory.py list --tag aliyun

# Add server
python3 scripts/inventory.py add SERVER_NAME \
  --host IP_OR_HOSTNAME \
  --port 22 \
  --user USERNAME \
  --ssh-key PATH_TO_KEY \
  --groups GROUP1,GROUP2 \
  --tags TAG1,TAG2 \
  --desc "description"
```

**Target Syntax** (used in `deploy.py`):
- `server-name` - Specific server
- `group:groupname` - All servers in that group
- `tag:tagname` - All servers with that tag
- `*` - All servers

### Remote Command Execution (`deploy.py`)

```bash
# Parallel batch (default)
python3 scripts/deploy.py exec group:web "docker pull nginx"

# Sequential (large batches or to avoid overload)
python3 scripts/deploy.py exec group:large "apt upgrade -y" --sequential

# Use environment variables
export MYSQL_VERSION="8.0"
cat templates/install_mysql.sh | python3 scripts/deploy.py exec db-01 "bash -s"
```

### File Operations

```bash
# Upload (single)
python3 scripts/deploy.py upload web-01 ./local.conf /etc/app/conf.d/conf.conf

# Batch upload
python3 scripts/deploy.py upload group:web ./nginx.conf /etc/nginx/nginx.conf

# Download
python3 scripts/deploy.py download web-01 /var/log/app.log ./logs/
```

## 🌏 Domestic Network Optimization

### Mirror Configuration

This skill uses **Aliyun mirrors by default** and configures:

- **Ubuntu/Debian** → `mirrors.aliyun.com`
- **CentOS/RHEL** → `mirrors.aliyun.com`
- **npm** → `registry.npmmirror.com` (Taobao)
- **pip** → `mirrors.aliyun.com/pypi/simple`
- **Docker** → USTC, NetEase, Baidu mirrors
- **Go** → `goproxy.cn`
- **Maven** → Aliyun repository

Detailed config: `references/mirrors.md`

### One-Click Mirror Setup

```bash
# Configure system mirrors on all servers
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:all "bash -s"

# Manual Docker mirror config (if needed)
cat <<'EOF' | python3 scripts/deploy.py exec group:all "bash -s"
cat > /etc/docker/daemon.json <<DOCKER
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ]
}
DOCKER
systemctl restart docker
EOF
```

## 🔒 Security Best Practices

1. **SSH Key Management**
   - Use key auth, disable passwords
   - Key permissions: `chmod 600 ~/.ssh/id_rsa`
   - Different keys for different environments

2. **Least Privilege**
   - Create dedicated deploy users (not root)
   - Configure passwordless sudo (only necessary commands)
   - Server `sshd_config`: `PermitRootLogin no`, `PasswordAuthentication no`

3. **Sensitive Data**
   - Never store passwords in `inventory.json`
   - Use environment variables for passwords (e.g., `MYSQL_ROOT_PASSWORD`)
   - Config file permissions `640`, owner `root:appgroup`

4. **Audit**
   - Keep all deployment logs
   - Record command, server, time, result

Full security guide: `references/best-practices.md`

## 🐛 Troubleshooting

### Quick Diagnostics

```bash
# 1. Network test
ping <host>
telnet <host> 22

# 2. Manual SSH test
ssh -i ~/.ssh/id_rsa root@<host> "uptime"

# 3. View connection details
python3 scripts/deploy.py exec <server> "uptime" 2>&1

# 4. Verify key permissions
ls -la ~/.ssh/id_rsa*
```

### Common Issues

| Symptom | Solution |
|---------|----------|
| Connection refused/timeout | Check server status, SSH service, firewall/security group |
| Permission denied (publickey) | Check public key in server's `~/.ssh/authorized_keys`, key perms 600 |
| sudo: a password is required | Configure passwordless sudo or use root user |
| Command not found | Use absolute path or ensure PATH includes command |
| Slow downloads in China | Run `base_setup.sh` to configure mirrors, see `docs/mirrors.md` |

Detailed troubleshooting: `references/troubleshooting.md`

## 📊 Batch Operations Examples

### Scenario 1: New Server Initialization

```bash
# 1. Add server to inventory
python3 scripts/inventory.py add web-01 --host 1.2.3.101 --groups web --tags production

# 2. Base setup (mirrors, tools)
cat templates/base_setup.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# 3. Install core software
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"
cat templates/install_nginx.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# 4. Upload app config
python3 scripts/deploy.py upload web-01 ./app-config.json /opt/app/config.json

# 5. Start application
python3 scripts/deploy.py exec web-01 "docker-compose up -d"
```

### Scenario 2: Rolling Updates Across Multiple Servers

```bash
# Canary release: update first batch
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:"canary" "bash -s"

# Check monitoring metrics...

# Full rollout
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:production "bash -s"
```

### Scenario 3: Configuration Sync

```bash
# Sync config file to all Web servers
python3 scripts/deploy.py upload group:web ./nginx.conf /etc/nginx/nginx.conf

# Batch restart
python3 scripts/deploy.py exec group:web "nginx -t && systemctl reload nginx"
```

### Scenario 4: Health Checks & Monitoring

```bash
# Collect status from all servers
python3 scripts/deploy.py exec "*" "uptime" > uptime-$(date +%F).log

python3 scripts/deploy.py exec "*" "df -h" > disk-$(date +%F).log

python3 scripts/deploy.py exec "*" "docker ps --format 'table {{.Names}}\t{{.Status}}'" > containers-$(date +%F).log
```

## 🔄 CI/CD Integration

### GitLab CI Example

```yaml
stages:
  - deploy

deploy_production:
  stage: deploy
  script:
    - pip3 install --user paramiko
    - export TARGET="group:production"
    - cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "$TARGET" "bash -s"
  only:
    - main
```

### GitHub Actions Example

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install paramiko
        run: pip3 install paramiko
      - name: Deploy to servers
        run: |
          cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "group:staging" "bash -s"
```

## 🛠️ Developer Guide

### Adding New Installation Templates

1. Create `.sh` file in `templates/`
2. Use `#!/bin/bash` and `set -e`
3. Detect OS type and adapt (see existing templates)
4. Use env vars for parameters, never hardcode secrets
5. Add domestic mirror config where applicable

### Custom Script Structure

```bash
#!/bin/bash
set -e

echo "===== Installing XXX ====="

# 1. Detect OS
if [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/redhat-release ]; then
    OS="redhat"
else
    echo "Unsupported OS"
    exit 1
fi

# 2. Configure domestic mirrors (if needed)
# ...

# 3. Install software
if [ "$OS" = "debian" ]; then
    apt-get update
    apt-get install -y xxx
elif [ "$OS" = "redhat" ]; then
    yum install -y xxx
fi

# 4. Start service
systemctl start xxx
systemctl enable xxx

echo "XXX installation complete!"
```

### Using Python API Directly

```python
from inventory import Inventory, Server
from deploy import SSHDeployer

# Load inventory
inv = Inventory()
server = inv.get_server("web-01")

# Create deployer
deployer = SSHDeployer()

# Execute command
result = deployer.execute(server, "docker ps")
print(result.success, result.output)

# Upload file
res = deployer.upload_file(server, "./local.conf", "/etc/conf.d/local.conf")

deployer.close()
```

## 📚 Additional Documentation

Detailed documentation (some in Chinese):
- `README.md` - Complete usage guide with API reference
- `README.zh-CN.md` - Full Chinese manual
- `references/mirrors.md` - Domestic mirror configuration details
- `references/best-practices.md` - Best practices and code examples
- `references/troubleshooting.md` - Complete troubleshooting handbook

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License
