# Troubleshooting Guide

Quick solutions for common SSH Deploy issues.

## Quick Diagnostic Flow

```
Deployment Failed?
    │
    ├─ Network Issues?
    │   ├─ ping <host> → No response?
    │   │   └─ Server down or network unreachable
    │   ├─ telnet <host> 22 → Connection refused?
    │   │   └─ SSH not running or firewall blocking
    │
    ├─ Authentication Failed?
    │   ├─ Manual ssh test → Works?
    │   │   └─ Check ~/.ssh/id_rsa permissions (600)
    │   │   └─ Check server ~/.ssh/authorized_keys (600)
    │   │   └─ Check /etc/ssh/sshd_config
    │   │
    │   └─ Password error?
    │       └→ Configure NOPASSWD sudo or use root
    │
    ├─ Command Not Found?
    │   ├─ Use absolute path: /usr/bin/docker
    │   ├─ Source environment: source ~/.bashrc && <cmd>
    │   └─ Install software first (use templates)
    │
    ├─ Slow Downloads (China)?
    │   └─ Run base_setup.sh to configure mirrors
    │
    └─ See detailed solutions below
```

---

## Common Issues

### 1. Connection Refused or Timeout

**Error**: `[Errno 113] No route to host`, `Timeout`

**Checklist**:
```bash
# 1. Is server online?
ping 192.168.1.100

# 2. Is SSH port open?
telnet 192.168.1.100 22
# or
nc -zv 192.168.1.100 22

# 3. Is SSH running on server?
# (if you can access via other means)
systemctl status sshd

# 4. Check firewall
iptables -L -n
# or CentOS 7+
firewall-cmd --list-all

# 5. Cloud security group?
# Console → Security Groups → allow port 22
```

**Fix**:
```bash
# Start SSH
systemctl start sshd && systemctl enable sshd

# Open port (iptables)
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Open port (firewalld)
firewall-cmd --add-port=22/tcp --permanent
firewall-cmd --reload
```

---

### 2. Permission Denied (publickey)

**Error**: `Authentication failed`

**Checklist**:
```bash
# 1. Manual SSH test
ssh -i ~/.ssh/id_rsa root@192.168.1.100

# 2. Key file permissions
ls -la ~/.ssh/id_rsa*
# Should be: -rw------- (600)

chmod 600 ~/.ssh/id_rsa

# 3. Server authorized_keys permissions
# On server:
ls -la ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 4. SSH config on server
cat /etc/ssh/sshd_config | grep -E "(PubkeyAuthentication|AuthorizedKeysFile)"
# Should be:
# PubkeyAuthentication yes
# AuthorizedKeysFile .ssh/authorized_keys

# 5. SELinux (RHEL/CentOS)
getenforce
# If Enforcing:
restorecon -R -v ~/.ssh
```

**Fix**:
```bash
# Deploy public key
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.1.100

# Or manual:
cat ~/.ssh/id_rsa.pub | ssh root@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Restart SSH after changes
systemctl restart sshd
```

---

### 3. Command Not Found

**Error**: `exit code: 127`, `bash: docker: command not found`

**Fix**:
```bash
# Use absolute path
python3 scripts/deploy.py exec web-01 "/usr/bin/docker ps"

# Source environment first
python3 scripts/deploy.py exec web-01 "source ~/.bashrc && which docker"

# If software not installed, use template
cat templates/install_docker.sh | python3 scripts/deploy.py exec web-01 "bash -s"
```

---

### 4. Sudo Requires Password

**Error**: `sudo: a password is required`

**Solution A**: Use root user in inventory
```json
{
  "web-01": {
    "user": "root",
    "ssh_key": "~/.ssh/id_rsa"
  }
}
```

**Solution B**: Configure passwordless sudo
```bash
# On server (as root):
visudo
# Add:
deploy ALL=(ALL) NOPASSWD:ALL
```

Then use deploy user:
```json
{
  "web-01": {
    "user": "deploy",
    "ssh_key": "~/.ssh/id_rsa_deploy"
  }
}
```

---

### 5. Slow/Failed Downloads in China

**Error**: `Could not connect to archive.ubuntu.com`, timeouts

**Fix - Auto**:
```bash
# Configure all mirrors automatically
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:all "bash -s"
```

**Fix - Manual (Ubuntu)**:
```bash
python3 scripts/deploy.py exec web-01 "cat > /etc/apt/sources.list <<'EOF'
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
EOF"
python3 scripts/deploy.py exec web-01 "apt-get update"
```

**Alternative mirrors**:
- Aliyun: `mirrors.aliyun.com`
- Tsinghua: `mirrors.tuna.tsinghua.edu.cn`
- USTC: `mirrors.ustc.edu.cn`

---

### 6. Host Key Verification Failed

**Error**: `Host key verification failed.`

**Cause**: Server SSH fingerprint changed (reinstalled OS or MITM attack)

**Fix**:
```bash
# Remove old key from known_hosts
sed -i '/192.168.1.100/d' ~/.ssh/known_hosts

# Or manually edit
vim ~/.ssh/known_hosts
# Remove the line with 192.168.1.100

# Reconnect (will prompt to accept new key)
ssh root@192.168.1.100
```

---

### 7. File Transfer Permission Denied

**Error**: `[Errno 13] Permission denied: '/etc/nginx/nginx.conf'`

**Fix**:
```bash
# Option 1: Upload to temp, then move with sudo
python3 scripts/deploy.py upload web-01 ./nginx.conf /tmp/nginx.conf
python3 scripts/deploy.py exec web-01 "mv /tmp/nginx.conf /etc/nginx/nginx.conf"

# Option 2: Use root user
# (update inventory.json user to "root")

# Option 3: Grant write permission to deploy user
python3 scripts/deploy.py exec web-01 "chmod 644 /etc/nginx"
# (not recommended for sensitive files)
```

---

### 8. No Space Left on Device

**Error**: `IOError: [Errno 28] No space left on device`

**Fix**:
```bash
# Check disk space
python3 scripts/deploy.py exec web-01 "df -h"

# Check inode usage
python3 scripts/deploy.py exec web-01 "df -i"

# Clean Docker
python3 scripts/deploy.py exec web-01 "docker system prune -af"

# Clean apt cache
python3 scripts/deploy.py exec web-01 "apt-get clean"

# Clean yum cache
python3 scripts/deploy.py exec web-01 "yum clean all"
```

---

### 9. Address Already in Use

**Error**: `EADDRINUSE: address already in use :::80`

**Fix**:
```bash
# Find process using port
python3 scripts/deploy.py exec web-01 "lsof -i :80"

# Kill process (if safe)
python3 scripts/deploy.py exec web-01 "kill <PID>"

# Or change your app to use different port
```

---

### 10. Module Not Found: paramiko

**Error**: `ImportError: No module named 'paramiko'`

**Fix**:
```bash
pip3 install paramiko
# or
pip3 install --user paramiko
```

---

### 11. Execution Timeout

**Error**: `timed out`

**Causes**: Slow server, network latency, long-running command

**Fix**:
```python
# Increase timeout in deploy.py (if needed)
deployer = SSHDeployer(timeout=120)
```

Or break command into smaller steps.

---

## Debug Mode

Enable verbose logging:

```bash
export LOG_LEVEL=DEBUG
python3 scripts/deploy.py exec web-01 "uptime"
```

Or edit `scripts/deploy.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

---

## System Information Scripts

Run these to gather diagnostic info:

```bash
# Server overview
python3 scripts/deploy.py exec "*" "hostname && uname -a && cat /etc/os-release"

# SSH configuration
python3 scripts/deploy.py exec "*" "which ssh && ssh -V"

# Network
python3 scripts/deploy.py exec "*" "ip addr show && route -n"

# Resources
python3 scripts/deploy.py exec "*" "free -m && df -h"

# Firewall
python3 scripts/deploy.py exec "*" "iptables -L -n || firewall-cmd --list-all"

# Docker
python3 scripts/deploy.py exec "*" "docker version || echo 'Docker not installed'"
```

---

## Still Stuck?

Check:
1. [README.md](../README.md) - Full usage guide
2. [best-practices.md](./best-practices.md) - Operational guidance
3. [mirrors.md](./mirrors.md) - Network/mirror issues

**Report issues** with:
- Complete error output
- Results of diagnostic scripts above
- `inventory.json` (sanitized)
- OS details of affected servers
- Steps to reproduce

---

## Emergency Recovery

If deployment broke your service:

1. **Manual SSH** to server
2. **Restart service**: `systemctl restart <service>`
3. **Rollback config**: `cp /etc/app/config.conf.bak /etc/app/config.conf`
4. **Check logs**: `journalctl -u <service> -n 100`, `tail -f /var/log/app/error.log`
5. **Monitor**: Verify before proceeding

---

*Last updated: 2026-04-06*
