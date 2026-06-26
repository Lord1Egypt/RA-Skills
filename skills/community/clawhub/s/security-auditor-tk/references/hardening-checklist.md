# Server Hardening Checklist

## SSH Hardening
- [ ] Disable root login (`PermitRootLogin no`)
- [ ] Disable password auth (`PasswordAuthentication no`)
- [ ] Use non-standard port (move off 22)
- [ ] Set MaxAuthTries to 3
- [ ] Set LoginGraceTime to 60
- [ ] Disable X11 forwarding
- [ ] Use Ed25519 or RSA 4096 keys only
- [ ] Set ClientAliveInterval 300, ClientAliveCountMax 2
- [ ] Restrict to specific users (AllowUsers)
- [ ] Enable login banner

## Firewall
- [ ] Enable UFW/iptables with default deny
- [ ] Only open required ports (SSH, HTTP/S, app-specific)
- [ ] Rate limit SSH connections
- [ ] Enable logging
- [ ] Install and configure fail2ban
- [ ] Block ICMP if not needed
- [ ] Review IPv6 rules (or disable if unused)

## System
- [ ] Enable automatic security updates
- [ ] Remove unnecessary packages
- [ ] Disable unused services
- [ ] Set proper permissions on /tmp (noexec,nosuid)
- [ ] Audit SUID/SGID binaries
- [ ] Remove world-writable files
- [ ] Configure core dump restrictions
- [ ] Set kernel hardening parameters (sysctl)
- [ ] Enable audit logging

## Users & Access
- [ ] Remove default/unused accounts
- [ ] Enforce strong password policy (if passwords used)
- [ ] Set proper umask (027 or 077)
- [ ] Review sudo access (principle of least privilege)
- [ ] Check for users with UID 0 (should only be root)
- [ ] Review authorized_keys files

## Web/SSL
- [ ] Valid SSL certificate (not self-signed in production)
- [ ] TLS 1.2+ only (disable SSLv3, TLS 1.0, TLS 1.1)
- [ ] Strong cipher suites only
- [ ] HSTS enabled with long max-age
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Server version headers hidden
- [ ] Directory listing disabled
