# SSH Deploy Skill

> Universal SSH remote deployment tool optimized for domestic network environment

A Python paramiko-based SSH deployment tool for managing Linux servers with support for:
- Multi-server management and batch operations
- Remote command execution and file transfer (SCP)
- Installation script templates for common software (Docker, MySQL, PostgreSQL, Nginx, Node.js, Redis, Python, Git)
- Automated domestic mirror configuration (Aliyun, Tsinghua, USTC)
- Direct integration with `~/.ssh/config`
- Group and tag-based server targeting

## Quick Start

```bash
# 1. Navigate to the skill directory
cd /root/.openclaw/workspace/skills/ssh-deploy-skill

# 2. Install dependency
pip3 install paramiko

# 3. Add a server (three methods)

## Method A: Using inventory.py
python3 scripts/inventory.py add web-01 \
  --host 192.168.1.101 \
  --user root \
  --ssh-key ~/.ssh/id_rsa \
  --groups production,web

## Method B: Edit ~/.ssh-deploy/inventory.json manually
## Method C: Use existing ~/.ssh/config entries (no extra config needed!)

# 4. Execute commands
python3 scripts/deploy.py exec web-01 "uptime"

# 5. Batch operations by group/tag
python3 scripts/deploy.py exec group:production "docker ps"
python3 scripts/deploy.py exec tag:aliyun "systemctl status nginx"

# 6. File transfer
python3 scripts/deploy.py upload web-01 ./nginx.conf /etc/nginx/nginx.conf
python3 scripts/deploy.py download web-01 /var/log/app.log ./logs/

# 7. Use installation templates
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"
```

## Command Line Options

### `--strict` (Strict Host Key Verification)

Enable strict SSH host key checking for production environments:

```bash
python3 scripts/deploy.py --strict exec web-01 "uptime"
```

When `--strict` is used:
- Loads `~/.ssh/known_hosts`
- Rejects unknown or changed host keys
- First connection to a new server will fail; you must manually verify fingerprint first
- Prevents man-in-the-middle attacks

**Default**: `--strict` is OFF for convenience. Turn ON for production.

### `--config-dir`

Custom configuration directory (default: `~/.ssh-deploy`):

```bash
python3 scripts/deploy.py --config-dir /path/to/custom/config exec web-01 "uptime"
```

## Configuration Files

- `~/.ssh-deploy/inventory.json` - Server inventory (primary)
- `~/.ssh-deploy/config.json` - Reserved for future global settings (currently unused)

**Note**: `config.json` is a placeholder. It may be used in future versions for default timeout, mirror settings, or output formatting. You can safely ignore it for now.

## Features

### Server Inventory Management
- **Multiple input methods**: CLI (`inventory.py`), JSON file (`~/.ssh-deploy/inventory.json`), or direct `~/.ssh/config` reading
- **Grouping**: Organize servers by environment/role (production, staging, web, db)
- **Tagging**: Flexible labels for cloud provider, region, etc.
- **Target syntax**: `server-name`, `group:name`, `tag:name`, `*` (all servers)

### Remote Operations
- **Command execution**: Parallel by default, `--sequential` for controlled batches
- **File transfer**: Upload/download with progress tracking
- **Template system**: Pre-built shell scripts with domestic mirror optimization

### Domestic Network Optimization
- Automatic mirror configuration for apt/yum, npm, pip, Docker, Go, Maven
- Works out-of-the-box for China mainland
- Mirror fallback switching

## Project Structure

```
ssh-deploy-skill/
├── SKILL.md               # Skill definition
├── README.md              # This file (English - primary)
├── README.zh-CN.md        # Full Chinese documentation
├── scripts/
│   ├── inventory.py       # Server inventory management
│   ├── deploy.py          # Core deployment engine
│   └── templates.py       # Template utilities
├── templates/             # Installation script templates
│   ├── base_setup.sh      # Base environment + mirrors
│   ├── install_git.sh
│   ├── install_docker.sh
│   ├── install_mysql.sh
│   ├── install_postgresql.sh
│   ├── install_nginx.sh
│   ├── install_nodejs.sh
│   ├── install_redis.sh
│   └── install_python.sh
└── references/           # Detailed documentation references
    ├── best-practices.md
    ├── mirrors.md
    └── troubleshooting.md
```

## Usage Reference

### Server Management

```bash
# List all servers
python3 scripts/inventory.py list

# Filter by group
python3 scripts/inventory.py list --group production

# Filter by tag
python3 scripts/inventory.py list --tag "阿里云"

# Add server
python3 scripts/inventory.py add <name> \
  --host <ip> \
  --port <22> \
  --user <username> \
  --ssh-key <path> \
  --groups <group1,group2> \
  --tags <tag1,tag2> \
  --desc "description"
```

### Command Execution

```bash
# Single server
python3 scripts/deploy.py exec <target> "<command>"

# Batch (parallel by default)
python3 scripts/deploy.py exec group:web "docker ps"

# Sequential (large batches)
python3 scripts/deploy.py exec group:large "apt upgrade -y" --sequential

# With environment variables
export MYSQL_ROOT_PASSWORD="secret"
cat templates/install_mysql.sh | python3 scripts/deploy.py exec db-01 "bash -s"
```

### File Operations

```bash
# Upload
python3 scripts/deploy.py upload <target> <local_path> <remote_path>

# Download
python3 scripts/deploy.py download <target> <remote_path> <local_path_or_dir>
```

### Templates

All templates in `templates/` are ready-to-use with domestic mirrors:

| Template | Software | Env Vars |
|----------|----------|----------|
| `base_setup.sh` | Base system + mirrors | - |
| `install_docker.sh` | Docker CE + mirrors | - |
| `install_mysql.sh` | MySQL 8.0 | `MYSQL_ROOT_PASSWORD` |
| `install_postgresql.sh` | PostgreSQL 15 | `PG_VERSION` |
| `install_nginx.sh` | Nginx | - |
| `install_nodejs.sh` | Node.js | `NODE_VERSION` (default: 20) |
| `install_redis.sh` | Redis | - |
| `install_python.sh` | Python | `PYTHON_VERSION` (default: 3.10) |
| `install_git.sh` | Git | `GIT_USER_NAME`, `GIT_USER_EMAIL` |

## Configuration

### SSH Config Integration (Recommended)

If you already use `~/.ssh/config`, no additional configuration needed:

```ssh-config
# ~/.ssh/config
Host myserver
    HostName 1.2.3.4
    User deploy
    IdentityFile ~/.ssh/id_rsa_myserver
    Port 22
```

Then use directly:
```bash
python3 scripts/deploy.py exec myserver "uptime"
```

**Note**: SSH config hosts are read-only (dynamic). To add groups/tags, import to inventory:
```bash
python3 scripts/inventory.py add myserver --from-ssh-config
```

### Manual Inventory

Edit `~/.ssh-deploy/inventory.json`:

```json
{
  "servers": {
    "web-prod-01": {
      "host": "1.2.3.101",
      "port": 22,
      "user": "deploy",
      "ssh_key": "~/.ssh/id_rsa_prod",
      "groups": ["web", "production"],
      "tags": ["aliyun", "east-china"]
    }
  }
}
```

## Domestic Mirror Configuration

The skill automatically configures mirrors for:

- **apt (Ubuntu/Debian)**: `mirrors.aliyun.com`
- **yum (CentOS/RHEL)**: `mirrors.aliyun.com`
- **npm**: `registry.npmmirror.com` (Taobao)
- **pip**: `mirrors.aliyun.com/pypi/simple`
- **Docker**: USTC, NetEase, Baidu mirrors
- **Go modules**: `goproxy.cn`
- **Maven**: Aliyun repository

For manual configuration details, see `references/mirrors.md`.

## Best Practices

### Security

#### SSH Key Authentication
- Use SSH keys, disable password authentication
- Create dedicated deployment users (not root)
- Set key permissions to `600`
- Configure `PermitRootLogin no` and `PasswordAuthentication no` in `/etc/ssh/sshd_config`

#### Strict Host Key Verification (--strict)

By default, the tool automatically accepts new host keys (convenient for initial setup). For production environments, enable strict mode:

```bash
python3 scripts/deploy.py --strict exec web-01 "uptime"
```

Strict mode behavior:
- Loads `~/.ssh/known_hosts`
- Rejects unknown or changed host keys
- First connection to a new server will fail with `BadHostKeyException`
- You must manually confirm the fingerprint once: `ssh root@server`

**When to use strict mode**:
- Production environments
- Multi-tenant or untrusted networks
- Compliance requirements (audit trails)

**When to skip**:
- Initial server provisioning (auto-accept, then switch to strict)
- Isolated lab environments
- Ephemeral test servers

#### Password Authentication Warning

The tool detects if any server in your inventory uses password authentication (stored in plaintext in `inventory.json`). A warning will be displayed:

```
⚠️  检测到以下服务器使用密码认证（不推荐）：web-old, db-test
   建议：使用 SSH 密钥认证，避免明文存储密码。
   参考：https://docs.openclaw.ai/security/ssh-keys
```

**Recommendation**: Always use SSH key authentication. Remove `password` fields from `inventory.json` and migrate to key-based auth.

### Operations
- Test on one server before batch operations
- Backup configurations before overwriting
- Use `--sequential` for 20+ servers
- Always check exit codes and outputs
- Maintain deployment logs

### CI/CD
```yaml
# Example: GitLab CI
deploy_production:
  script:
    - pip3 install paramiko
    - export TARGET="group:production"
    - cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "$TARGET" "bash -s"
```

For comprehensive best practices, see `references/best-practices.md`.

## Troubleshooting

### Common Issues

| Symptom | Solution |
|---------|----------|
| `Connection refused` | Check server status, SSH service, firewall, security group |
| `Permission denied (publickey)` | Verify key in `~/.ssh/authorized_keys`, key permissions `600` |
| `Command not found` | Use absolute path or `source ~/.bashrc && <command>` |
| `sudo: a password is required` | Configure NOPASSWD sudo or use root user |
| Slow downloads in China | Run `base_setup.sh` to configure domestic mirrors |
| `Host key verification failed` | Remove old key from `~/.ssh/known_hosts` |
| `No space left on device` | `df -h`, clean Docker/apt cache |

### Debug Steps

```bash
# 1. Network test
ping <host>
telnet <host> 22

# 2. Manual SSH test
ssh -i ~/.ssh/id_rsa <user>@<host> "uptime"

# 3. Check server info
python3 scripts/deploy.py exec <target> "uname -a && cat /etc/os-release"

# 4. Enable debug logging
export LOG_LEVEL=DEBUG
python3 scripts/deploy.py exec <target> "command"
```

For complete troubleshooting guide, see `references/troubleshooting.md`.

## Examples

### Scenario 1: New Server Initialization

```bash
# Add to inventory
python3 scripts/inventory.py add web-01 \
  --host 1.2.3.101 \
  --groups web,production \
  --tags "aliyun"

# Base setup (mirrors, tools)
cat templates/base_setup.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# Install Docker
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"

# Upload config
python3 scripts/deploy.py upload web-01 ./app-config.json /opt/app/config.json

# Start app
python3 scripts/deploy.py exec web-01 "docker-compose up -d"
```

### Scenario 2: Batch Deployment

```bash
# Add multiple servers to same group
for i in 1 2 3; do
  python3 scripts/inventory.py add web-$i \
    --host 1.2.3.10$i \
    --groups web \
    --tags "production"
done

# Deploy to all group members in parallel
cat templates/install_docker.sh | python3 scripts/deploy.py exec group:web "bash -s"

# Upload config to all at once
python3 scripts/deploy.py upload group:web ./nginx.conf /etc/nginx/nginx.conf

# Restart services sequentially (avoid thundering herd)
python3 scripts/deploy.py exec group:web "systemctl restart nginx" --sequential
```

### Scenario 3: Gray Rollout

```bash
# Phase 1: Canary group
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:"canary" "bash -s"

# Monitor metrics...

# Phase 2: Full rollout
cat deploy-v2.sh | python3 scripts/deploy.py exec tag:production "bash -s"
```

### Scenario 4:巡检 (Health Check)

```bash
# Collect status from all servers
python3 scripts/deploy.py exec "*" "uptime" > uptime-$(date +%F).log
python3 scripts/deploy.py exec "*" "df -h" > disk-$(date +%F).log
python3 scripts/deploy.py exec "*" "docker ps --format 'table {{.Names}}\t{{.Status}}'" > containers-$(date +%F).log
```

## Python API

```python
from inventory import Inventory
from deploy import SSHDeployer

# Load inventory
inv = Inventory()
server = inv.get_server("web-prod-01")

# Create deployer (with strict mode for production)
deployer = SSHDeployer(strict_host_key=True)

# Execute command
result = deployer.execute(server, "docker ps")
print(f"Success: {result.success}, Output: {result.output}")

# Upload file
res = deployer.upload_file(server, "./local.conf", "/etc/conf.d/local.conf")

# Batch execute
servers = inv.get_servers_by_group("production")
results = deployer.execute_batch(servers, "systemctl status nginx", sequential=False)

# Always close connections (or use context manager)
deployer.close()
```

**Recommended: Context Manager** (auto cleanup)

```python
with SSHDeployer(strict_host_key=True) as deployer:
    result = deployer.execute(server, "uptime")
    # Connections automatically closed on exit
```

## Requirements

- Python 3.8+
- `paramiko` package (`pip3 install paramiko`)
- System bins: `python3`, `ssh`, `scp`
- Target servers: Any Linux distribution (Ubuntu, Debian, CentOS, RHEL, Alpine, etc.)

## License

MIT

## Chinese Documentation

For detailed Chinese documentation including comprehensive examples, see:
- `README.zh-CN.md` - Full Chinese manual
- `references/best-practices.md` - 最佳实践
- `references/mirrors.md` - 国内镜像源配置详解
- `references/troubleshooting.md` - 故障排查完整手册
