# Security Dashboard

Real-time security monitoring dashboard for OpenClaw and Linux server infrastructure. Monitors 7 critical security areas with automated 4x daily checks and instant alerts for issues like inactive firewalls, fail2ban problems, and public exposure.

![Security Dashboard Screenshot](images/dashboard-screenshot.jpg)

## Overview

The Security Dashboard provides comprehensive monitoring for your OpenClaw deployment and Linux infrastructure. It tracks gateway security, network configuration, public exposure, system updates, SSH access, certificates, and resource usage - all in a clean, real-time web interface.

**Key Features:**
- 🔒 7 security monitoring sections
- 🚨 Automated critical alerts (firewall, fail2ban, SSH)
- 📊 Real-time metrics updated every 5 seconds  
- 🤖 4x daily automated checks via cron
- 🌐 Localhost-only binding (secure by default)
- 📱 Mobile-friendly dark UI

## Quick Start

```bash
./scripts/install.sh
```

Access via SSH port forwarding:
```bash
ssh -L 18791:localhost:18791 root@YOUR_SERVER_IP
```

Then visit: http://localhost:18791

## Features

- ✅ OpenClaw gateway monitoring
- ✅ Network security metrics
- ✅ Public exposure analysis
- ✅ System security checks
- ✅ SSH & fail2ban status
- ✅ Real-time alerts
- ✅ Resource monitoring

## Documentation

See [SKILL.md](SKILL.md) for full documentation.

## Quick Commands

```bash
# Service management
sudo systemctl status security-dashboard
sudo systemctl restart security-dashboard

# View logs
sudo journalctl -u security-dashboard -f

# Get metrics via API
curl http://localhost:18791/api/security | jq
```

## Security

- **Default binding:** 127.0.0.1 (localhost only)
- **Port:** 18791
- **Access:** SSH port forwarding or Tailscale required

## Requirements

- Node.js v18+
- OpenClaw installed
- systemd

## Author

Created by Brian Christner / @idomyowntricks.
