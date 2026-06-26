---
name: server-watchdog
description: Monitor remote servers via SSH — check service health (PM2, systemd, Docker), database status (MongoDB, MySQL, PostgreSQL), disk space, memory, and auto-restart crashed services. Sends alerts via messaging. Use when asked to check server status, monitor services, restart crashed processes, or set up server health checks.
---

# Server Watchdog

Monitor and auto-heal remote servers via SSH. Check services, databases, disk, memory — restart what's down, alert what's wrong.

## Prerequisites

- SSH access to target server (password or key-based)
- `expect` available locally (for password-based SSH)
- Target server runs PM2, systemd, or Docker for service management

## Quick Reference

### Check PM2 services
```bash
ssh user@host "pm2 list"
ssh user@host "pm2 logs --lines 20 --nostream"
```

### Check MongoDB
```bash
# Windows
ssh user@host "net start | findstr MongoDB"
ssh user@host "powershell -Command \"(Test-NetConnection -ComputerName 127.0.0.1 -Port 27017).TcpTestSucceeded\""

# Linux
ssh user@host "systemctl status mongod"
ssh user@host "mongosh --eval 'db.runCommand({ping:1})' --quiet"
```

### Check disk & memory
```bash
# Linux
ssh user@host "df -h && free -h"

# Windows
ssh user@host "powershell -Command \"Get-PSDrive -PSProvider FileSystem | Select Root,Used,Free; \$os=Get-CimInstance Win32_OperatingSystem; Write-Output ('RAM: '+[math]::Round((\$os.TotalVisibleMemorySize-\$os.FreePhysicalMemory)/1MB,1)+'GB / '+[math]::Round(\$os.TotalVisibleMemorySize/1MB,1)+'GB')\""
```

## Workflow

1. **Diagnose** — SSH in, check service status, logs, disk, memory
2. **Identify** — Parse logs for errors, crashes, OOM, or unclean shutdowns
3. **Fix** — Restart crashed services (`pm2 restart`, `net start`, `systemctl restart`)
4. **Verify** — Confirm service is back up and responding
5. **Alert** — Notify user via messaging with summary

## Crash Analysis

When a service is down, check these in order:

1. **Service logs** — `pm2 logs`, `journalctl -u service`, Windows Event Log
2. **Application logs** — Check log files at configured paths
3. **System events** — OOM killer, unexpected shutdowns, disk full
4. **Database logs** — MongoDB: check `mongod.log` for Fatal (`"s":"F"`) entries

### MongoDB crash patterns
```
"s":"F" — Fatal error (crash)
"Unhandled exception" — Internal bug (often FTDC related)
"Detected unclean shutdown" — Process killed without graceful shutdown
"WiredTiger error" — Storage engine corruption
```

## Auto-Heal Recipes

### PM2 service restart
```bash
pm2 restart <service-name>
pm2 save  # persist across reboots
```

### MongoDB (Windows)
```bash
net stop MongoDB
timeout /t 5
net start MongoDB
```

### MongoDB (Linux)
```bash
sudo systemctl restart mongod
```

### Deploy watchdog service
For persistent monitoring, deploy the included watchdog script:
1. Copy `scripts/mongodb-watchdog.js` to target server
2. Install: `npm init -y && npm install mongodb`
3. Start: `pm2 start mongodb-watchdog.js --name mongodb-watchdog`
4. Save: `pm2 save`

## SSH with password (via expect)

When key-based auth isn't available:
```bash
expect -c 'set timeout 20
spawn ssh -o StrictHostKeyChecking=no user@host "COMMAND"
expect {
    "password:" { send "PASSWORD\r"; exp_continue }
    eof
}
'
```

## Alert Template

```
🚨 Server Alert — [hostname]

⏰ Time: [timestamp]
❌ Issue: [service] is DOWN
📋 Cause: [crash reason from logs]
🔄 Action: Auto-restarted [service]
✅ Status: [service] is back online

📊 System Health:
• Memory: X GB / Y GB
• Disk: Z% used
• Services: N/N online
```
