# Best Practices for SSH Deploy

A practical guide to secure, reliable server deployments.

## 1. Inventory Organization

### ✅ Do

**Use groups for environments/roles**

```bash
python3 scripts/inventory.py add web-prod-01 \
  --host 1.2.3.101 \
  --groups production,web \
  --tags "aliyun,apac"
```

**Use tags for cloud/region filtering**

```bash
python3 scripts/deploy.py exec tag:aliyun "uptime"
python3 scripts/deploy.py exec tag:apac "docker ps"
```

**Consistent naming**

```
<env>-<service>-<number>
Examples: prod-web-01, staging-db-01
```

### ❌ Avoid

- Using IP addresses as server names
- Putting all servers in one group
- Mixing production and staging in same inventory

---

## 2. SSH Key Management

### ✅ Do

**Use keys, never passwords**

```json
{
  "web-01": {
    "user": "deploy",
    "ssh_key": "~/.ssh/id_rsa_prod"
  }
}
```

**Different keys per environment**

```
~/.ssh/
  id_rsa_prod
  id_rsa_staging
  id_rsa_personal
```

**Rotate keys periodically**

```bash
# Generate new key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_new

# Deploy new public key
cat ~/.ssh/id_rsa_new.pub | python3 scripts/deploy.py upload group:prod - ~/.ssh/authorized_keys
```

**Set correct permissions**

```bash
chmod 600 ~/.ssh/id_rsa*
```

### ❌ Avoid

- Storing passwords in `inventory.json`
- Using DSA keys (weak)
- Sharing keys across environments
- Leaving private keys unprotected

---

## 3. Command Execution

### ✅ Do

**Use template scripts**

`deploy.sh`:
```bash
#!/bin/bash
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:web "bash -s"
cat templates/install_docker.sh | python3 scripts/deploy.py exec group:web "bash -s"
```

**Control parallelism**

```bash
# 5 servers: parallel (default)
python3 scripts/deploy.py exec tag:small "docker pull nginx"

# 20+ servers: sequential
python3 scripts/deploy.py exec tag:large "apt upgrade -y" --sequential
```

**Pass parameters via environment**

```bash
export MYSQL_ROOT_PASSWORD="secret"
export NODE_VERSION="20"

cat templates/install_mysql.sh | python3 scripts/deploy.py exec db-01 "bash -s"
```

**Log everything**

```bash
python3 scripts/deploy.py exec group:prod "systemctl status nginx" > deploy-$(date +%Y%m%d-%H%M%S).log
```

**Check results**

```python
result = deployer.execute(server, "docker ps")
if not result.success:
    print(f"Failed on {server.name}: {result.error}")
```

### ❌ Avoid

- Hardcoding passwords in scripts
- Parallel execution on large batches (>15 servers)
- Ignoring exit codes
- Not validating single server before batch

---

## 4. File Transfers

### ✅ Do

**Validate on one server first**

```bash
python3 scripts/deploy.py upload web-test ./nginx.conf /etc/nginx/nginx.conf
# Verify it works...
python3 scripts/deploy.py upload group:web ./nginx.conf /etc/nginx/nginx.conf
```

**Backup before overwrite**

```bash
python3 scripts/deploy.py exec group:web "cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak.$(date +%Y%m%d)"
python3 scripts/deploy.py upload group:web ./nginx.conf /etc/nginx/nginx.conf
```

### ❌ Avoid

- Overwriting configs without backup
- Large transfers during peak hours
- Ignoring transfer failures
- Using deployment user for sensitive system files

---

## 5. Domestic Mirrors

### ✅ Do

**Configure base environment first**

```bash
cat templates/base_setup.sh | python3 scripts/deploy.py exec group:all "bash -s"
```

**Configure language-specific mirrors**

```bash
# Python
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# Node.js
npm config set registry https://registry.npmmirror.com
```

**Test connectivity**

```bash
python3 scripts/deploy.py exec group:prod "curl -I https://registry.npmmirror.com"
```

### ❌ Avoid

- Using default foreign mirrors in China
- Ignoring SSL certificate errors
- All traffic through proxy (performance bottleneck)

---

## 6. Security

### ✅ Do

**Use dedicated deploy user**

```bash
# Create user
python3 scripts/deploy.py exec web-01 "useradd -m -s /bin/bash deploy"

# Configure passwordless sudo for specific commands
echo "deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx" | \
  python3 scripts/deploy.py exec web-01 "tee -a /etc/sudoers.d/deploy"
```

**Harden SSH**

`/etc/ssh/sshd_config`:
```ini
PasswordAuthentication no
PermitRootLogin no
AllowUsers deploy
```

```bash
python3 scripts/deploy.py exec web-01 "systemctl reload sshd"
```

**Protect sensitive data**

- Never store passwords in `inventory.json`
- Use environment variables or external vault
- Set file permissions: `chmod 640 config.json && chown root:appgroup`

### ❌ Avoid

- All operations as root
- Password authentication enabled
- Wide-open sudo rules (`ALL=(ALL) ALL` without NOPASSWD)
- Deploy user with unnecessary privileges

---

## 7. Monitoring & Rollback

### ✅ Do

**Maintain deployment logs**

```bash
# Structured logging
python3 scripts/deploy.py exec group:prod "systemctl status nginx" \
  > logs/deploy-$(date +%Y%m%d-%H%M%S)-prod.log
```

**Post-deployment verification**

```bash
cat install.sh | python3 scripts/deploy.py exec web-01 "bash -s" && \
python3 scripts/deploy.py exec web-01 "systemctl is-active nginx && curl -f http://localhost"
```

**Automated rollback**

```bash
rollback() {
  python3 scripts/deploy.py exec $1 "docker-compose rollback"
  python3 scripts/deploy.py exec $1 "docker-compose up -d"
}
```

### ❌ Avoid

- Deploying without health checks
- No backup before changes
- Ignoring single-server failures
- Manual rollback procedures (automate!)

---

## 8. CI/CD Integration

### ✅ Do

**Environment-based targeting**

```yaml
deploy:
  script:
    - export TARGET="group:${ENV}"
    - cat deploy.sh | python3 skills/ssh-deploy-skill/scripts/deploy.py exec "$TARGET" "bash -s"
```

**Phased rollouts**

```bash
# Phase 1: Canary
python3 scripts/deploy.py exec tag:canary "docker-compose up -d"
# Monitor...

# Phase 2: Full rollout
python3 scripts/deploy.py exec tag:production "docker-compose up -d"
```

**Automatic rollback on failure**

```bash
if ! python3 scripts/deploy.py exec group:prod "docker-compose up -d"; then
  echo "Deployment failed, rolling back..."
  python3 scripts/deploy.py exec group:prod "docker-compose rollback"
  exit 1
fi
```

### ❌ Avoid

- Hardcoded server IPs in CI config
- No rollback plan
- Full restart of all services simultaneously
- Storing secrets in CI variables (use vault instead)

---

## 9. Performance

### ✅ Do

**Batch appropriately**

| Batch Size | Recommendation |
|------------|----------------|
| 1-5 | Parallel (default) |
| 6-15 | Parallel (ok) |
| 16+ | Sequential (`--sequential`) |

**Reuse connections**

`SSHDeployer` caches connections. Ensure `deployer.close()` is called.

**Compress transfer (future)**

For large files, enable compression in paramiko config.

### ❌ Avoid

- 50+ parallel connections (can overwhelm SSH daemon)
- Opening/closing connections per command
- Transferring large files during business hours

---

## 10. Troubleshooting Checklist

1. **Network**: `ping <host>`, `telnet <host> 22`
2. **SSH**: `ssh -i ~/.ssh/id_rsa <user>@<host> "uptime"`
3. **Key permissions**: `chmod 600 ~/.ssh/id_rsa*`
4. **Authorized keys**: `cat ~/.ssh/authorized_keys` on server
5. **SSH config**: `PubkeyAuthentication yes`, `AuthorizedKeysFile .ssh/authorized_keys`
6. **Firewall**: `iptables -L` or `firewall-cmd --list-all`
7. **SELinux** (RHEL): `restorecon -R -v ~/.ssh`
8. **Disk space**: `df -h`
9. **Mirror connectivity**: `curl -I https://mirrors.aliyun.com`
10. **Logs**: `/var/log/auth.log` or `/var/log/secure`

See `docs/troubleshooting.md` for detailed solutions.

---

## Quick Reference

### Command Templates

```bash
# Add server
python3 scripts/inventory.py add <name> --host <ip> --groups <g1,g2> --tags <t1,t2>

# Execute
python3 scripts/deploy.py exec <target> "<command>" [--sequential]

# Upload/Download
python3 scripts/deploy.py upload <target> <local> <remote>
python3 scripts/deploy.py download <target> <remote> <local>

# Use template
cat templates/install_<软件>.sh | python3 scripts/deploy.py exec <target> "bash -s"
```

### Target Syntax

```
server-name        # Specific server
group:production   # All servers in 'production' group
tag:aliyun         # All servers with 'aliyun' tag
*                  # All servers
```

---

*Last updated: 2026-04-06*
