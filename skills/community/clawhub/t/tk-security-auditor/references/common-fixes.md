# Common Security Fix Commands

## SSH Hardening

### Disable root login
```bash
sudo sed -i 's/#*PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Disable password authentication
```bash
sudo sed -i 's/#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Set MaxAuthTries
```bash
sudo sed -i 's/#*MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### Change SSH port
```bash
sudo sed -i 's/#*Port .*/Port 2222/' /etc/ssh/sshd_config
sudo ufw allow 2222/tcp
sudo systemctl restart sshd
# Then: sudo ufw delete allow 22/tcp
```

## Firewall

### Enable UFW with default deny
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### Install and configure fail2ban
```bash
sudo apt install fail2ban -y
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo sed -i 's/bantime  = 10m/bantime  = 1h/' /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Rate limit SSH
```bash
sudo ufw limit ssh/tcp
```

## System Updates

### Enable automatic security updates (Ubuntu/Debian)
```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

### Check pending updates
```bash
sudo apt update && sudo apt list --upgradable 2>/dev/null | grep -i security
```

## File Permissions

### Find world-writable files
```bash
find / -type f -perm -o+w -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null
```

### Find SUID binaries
```bash
find / -type f -perm -4000 2>/dev/null
```

### Fix tmp permissions
```bash
sudo mount -o remount,noexec,nosuid /tmp
```

## SSL/TLS

### Check certificate expiry
```bash
echo | openssl s_client -connect domain.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Test SSL configuration
```bash
nmap --script ssl-enum-ciphers -p 443 domain.com
```

## Security Headers (Nginx)
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## Kernel Hardening (sysctl)
```bash
cat >> /etc/sysctl.d/99-hardening.conf << 'EOF'
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
kernel.randomize_va_space = 2
fs.suid_dumpable = 0
EOF
sudo sysctl --system
```
