# Security Best Practices for Remote Terminal Access

Guidelines for secure remote server management.

## Authentication

### SSH Keys (Recommended)

**Generate strong keys:**

```bash
# Ed25519 (recommended, modern)
ssh-keygen -t ed25519 -C "your-email@example.com"

# RSA with 4096 bits (if Ed25519 not supported)
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

**Protect your keys:**

```bash
# Strong passphrase (use a password manager)
ssh-keygen -p -f ~/.ssh/id_ed25519

# Correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/config
```

**Add to SSH agent:**

```bash
# Start agent if not running
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# macOS: store in keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### Password Authentication

- **Avoid if possible** - Use SSH keys instead
- If required, use `sshpass` only in trusted environments
- Never store passwords in plain text files
- Use environment variables or secure vaults for automation

## Server-Side Security

### Disable Root Login

```bash
# /etc/ssh/sshd_config
PermitRootLogin no
```

### Disable Password Authentication

```bash
# /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
```

### Limit Users

```bash
# /etc/ssh/sshd_config
AllowUsers admin deploy@192.168.1.0/24
```

### Change Default Port

```bash
# /etc/ssh/sshd_config
Port 2222
```

### Use Fail2Ban

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

### Configure Firewall

```bash
# UFW (Ubuntu/Debian)
sudo ufw default deny incoming
sudo ufw allow from 192.168.1.0/24 to any port 22
sudo ufw enable

# iptables
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j DROP
```

## Connection Security

### Verify Host Keys

- First connection: verify the fingerprint
- Use `StrictHostKeyChecking yes` (default)
- Periodically verify known hosts: `ssh-keygen -F hostname`

### Use Known Hosts

```bash
# Check known hosts
cat ~/.ssh/known_hosts

# Remove old/compromised key
ssh-keygen -R hostname
```

### Jump Hosts (Bastion)

- Route all internal access through a bastion
- Monitor bastion access logs
- Apply strict security on bastion

```bash
# ~/.ssh/config
Host internal-*
    ProxyJump bastion.example.com
```

### VPN Access

- Connect to VPN before accessing internal servers
- Never expose SSH directly to the internet
- Use WireGuard or OpenVPN for VPN

## Command Execution Safety

### Dangerous Commands

**Always confirm before executing:**

- `rm -rf` with broad paths
- `shutdown`, `reboot`, `poweroff`
- `dd` operations
- `mkfs`, `fdisk`, `parted`
- `iptables -F`, `ufw disable`
- `DROP DATABASE`, `TRUNCATE TABLE`
- Any command with `sudo` on production

### Least Privilege

- Use dedicated service accounts
- Limit sudo to specific commands
- Use role-based access control (RBAC)

```bash
# /etc/sudoers
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
deploy ALL=(ALL) NOPASSWD: /usr/bin/docker restart *
```

### Audit Trail

- Log all executed commands
- Store logs securely
- Regularly review logs

```bash
# Enable command logging
export PROMPT_COMMAND='history -a; logger -t ssh_cmd "$(history 1)"'
```

## Session Security

### Timeouts

```bash
# Client-side (~/.ssh/config)
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Server-side (/etc/ssh/sshd_config)
ClientAliveInterval 300
ClientAliveCountMax 2
```

### Session Locking

For long sessions, use `screen` or `tmux`:

```bash
# Install
sudo apt install screen

# Start session
screen -S work

# Detach: Ctrl+A, D
# Reattach: screen -r work
# Lock: Ctrl+A, X
```

### Close Idle Sessions

```bash
# In ~/.bashrc or ~/.zshrc
TMOUT=3600  # Auto-logout after 1 hour idle
```

## Automated Access

### Service Accounts

- Create dedicated service accounts
- Use limited SSH keys (command restrictions)
- Log and monitor all automated access

```bash
# Generate key for automation
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N "" -C "deploy@ci"

# Add to authorized_keys with restrictions
command="/path/to/script.sh",no-port-forwarding,no-agent-forwarding ssh-ed25519 AAAA...
```

### CI/CD Security

- Use secrets management (Vault, AWS Secrets Manager)
- Rotate keys regularly
- Audit automation access separately

## Monitoring and Alerts

### Log Monitoring

```bash
# Monitor SSH logins
sudo tail -f /var/log/auth.log | grep sshd

# Failed login attempts
sudo grep "Failed password" /var/log/auth.log

# Successful logins
sudo grep "Accepted" /var/log/auth.log
```

### Alerting

Set up alerts for:
- Multiple failed login attempts
- Root login attempts
- Logins outside business hours
- Logins from unexpected IPs

## Incident Response

### Compromised Key

1. Immediately remove from authorized_keys
2. Generate new key with new passphrase
3. Audit all servers for unauthorized access
4. Check command history
5. Update all credentials

### Unauthorized Access

1. Terminate session: `pkill -u username`
2. Lock account: `usermod -L username`
3. Investigate source IP
4. Review logs
5. Report and document

## Checklist

### Before First Connection

- [ ] Generate SSH key with strong passphrase
- [ ] Add public key to server authorized_keys
- [ ] Verify host key fingerprint
- [ ] Configure SSH config with aliases
- [ ] Set correct file permissions

### Regular Maintenance

- [ ] Rotate SSH keys annually
- [ ] Audit authorized_keys
- [ ] Review access logs
- [ ] Update SSH config for new servers
- [ ] Test backup access methods

### Production Servers

- [ ] Disable root login
- [ ] Disable password authentication
- [ ] Configure firewall rules
- [ ] Set up fail2ban
- [ ] Configure logging
- [ ] Set up monitoring alerts
