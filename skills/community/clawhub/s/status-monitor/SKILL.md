---
name: openclaw-status-monitor
description: Manages OpenClaw Agent status upload scripts, periodically syncing agent online status to the cloud monitoring platform
author: yanghao
version: 4.0.0
metadata:
  openclaw:
    categories: [system, monitor]
    tags: [openclaw, status, sync, monitor]
    user-invocable: true
---

## Script Location

```
~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py
```

## Two Running Modes

### Mode 1: Cron Scheduled Sync (Default)

OpenClaw's built-in cron executes the script periodically:

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py
```

**Trigger phrases**: say "sync status", "restart sync" or "同步状态", "重启同步状态" — OpenClaw will trigger execution on schedule.

### Mode 2: Daemon Mode

Use `--fork` to start a real background daemon:

| Command | Description |
|---------|-------------|
| `python3 scripts/status_uploader.py start --fork` | Start daemon |
| `python3 scripts/status_uploader.py start --fork --interval 10` | Start with custom interval (minutes) |
| `python3 scripts/status_uploader.py stop` | Stop service |
| `python3 scripts/status_uploader.py status` | Check service status |
| `python3 scripts/status_uploader.py set-interval <minutes>` | Set sync interval |
| `python3 scripts/status_uploader.py test` | Single test upload |

**Examples:**
```bash
# Start daemon
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork

# Start with 10-minute interval
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 10
```

## Trigger Conditions

Triggers when any of the following conditions are met:

1. **First-time initialization**: say "enable status monitor", "setup status-monitor" or "启用状态监控", "开启监控同步", "配置 status-monitor"
2. **Manual trigger**: say "sync status", "sync status-monitor", "upload status" or "同步状态", "同步 status-monitor", "上传状态" → single execution
3. **Scheduled sync**: OpenClaw cron triggers → single execution
4. **Check status**: say "check status monitor", "monitor status", "check upload service" or "查看状态监控", "状态监控状态", "检查上传服务"
5. **Stop service**: say "stop status monitor", "stop upload service" or "停止状态监控", "停止上传服务"
6. **Change interval**: say "sync every 10 minutes", "change to 15 minutes" or "每10分钟同步一次", "改成15分钟"
7. **Daemon mode**: say "start status monitor", "start daemon", "run in background" or "启动状态监控", "启动守护进程", "后台运行" → execute `start --fork`

**Additional triggers**: say "start status-monitor service", "restart status-monitor service" or "启动status-monitor服务", "重启status-monitor服务".

## Initialization Flow (Must Execute on First Use)

### Step 1: Check Token Configuration

When the skill runs, first check for the token in these locations:

1. Environment variable `MONITOR_PLATFORM_TOKEN`
2. File `~/.openclaw/credentials/openclaw-status-monitor.json`

### Step 2: Handling Missing Token

If no token is found, guide the user to register/login:

1. **Prompt the user**:
   ```
   No monitoring token found. Let me help you set up...

   Please choose a sign-in method:
   1. Existing user: visit https://openclaw-agent-monitor.vercel.app and click Sign In
   2. New user: visit https://openclaw-agent-monitor.vercel.app and click Sign Up

   After signing in:
   - Go to the Settings page
   - Generate and copy your Agent Token
   - Send me the generated token
   ```

2. **Wait for user to reply with token**

3. **Save the token**:
   - Create directory `~/.openclaw/credentials/`
   - Save to `~/.openclaw/credentials/openclaw-status-monitor.json`:
     ```json
     {
       "agentToken": "user-provided-token",
       "createdAt": "2026-03-29T10:00:00.000Z",
       "monitorUrl": "https://openclaw-agent-monitor.vercel.app"
     }
     ```

4. **Validate the token**

### Step 3: After Successful Token Validation

```
✅ Token configured successfully!

Starting upload service...
- Running initial sync test...
- ✅ Service started successfully!

Monitor platform: https://openclaw-agent-monitor.vercel.app
Upload interval: 5 minutes

Start command:
python3 scripts/status_uploader.py start --fork

Management commands:
- Say "sync status" to manually trigger an upload
- Say "check status monitor" to check service status
- Say "stop status monitor" to stop the service
- Say "restart status monitor" to restart the service
```

## Core Functions: Managing the Upload Script

### 1. Check if Script Exists

```bash
if [ -f ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py ]; then
  echo "Script exists"
else
  echo "Script not found"
fi
```

### 2. Start Service (Recommended)

```bash
# Start daemon with --fork (recommended)
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 10
```

### 3. Set Sync Interval

```bash
# Method 1: specify at startup
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py start --fork --interval 15

# Method 2: use set-interval command
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py set-interval 15
```

### 4. Stop Service

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py stop
```

### 5. Check Service Status

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py status
```

### 6. View Error Logs

```
~/.openclaw/logs/status_uploader_error.log
~/.openclaw/logs/status_uploader.log
```

```bash
# View recent errors
tail -50 ~/.openclaw/logs/status_uploader_error.log

# View service logs
tail -50 ~/.openclaw/logs/status_uploader.log
```

**Log rotation**: log files auto-rotate when exceeding 10MB, format: `status_uploader.20260329_183500.log`

### 7. Manually Trigger One Upload

```bash
python3 ~/.openclaw/skills/openclaw-status-monitor/scripts/status_uploader.py test
```

### Upload Logic (Simplified)

The script only reads all agent IDs from `openclaw.json` and uploads them — **it does not perform any offline detection**.

Offline detection is handled by the monitoring platform (openclaw-agent-monitor):
- The platform automatically updates `lastActiveTimestamp` based on upload time
- If no upload is received for 5+ minutes, the platform automatically marks the agent as offline

## Storage Configuration

### Token Storage Location

`~/.openclaw/credentials/openclaw-status-monitor.json`:

```json
{
  "agentToken": "e2d3262f-b626-4850-af11-5f2cb1c0dcad",
  "createdAt": "2026-01-26T10:00:00.000Z",
  "monitorUrl": "https://openclaw-agent-monitor.vercel.app",
  "syncIntervalMinutes": 5
}
```

## Log Locations

- Service log: `~/.openclaw/logs/status_uploader.log`
- Error log: `~/.openclaw/logs/status_uploader_error.log`
- PID file: `~/.openclaw/logs/status_uploader.pid`
- Token config: `~/.openclaw/credentials/openclaw-status-monitor.json`

## Error Handling

### 1. Missing Token

**During initialization**:
```
❌ No monitoring token detected

Please complete these steps first:

1. Visit https://openclaw-agent-monitor.vercel.app
2. Click Sign In / Sign Up to log in or register
3. After logging in, generate an Agent Token on the Settings page
4. Send me the token

Example: My token is abc123-def456...
```

### 2. Script Not Found

```
❌ Upload script not found

Please reinstall the skill or contact the developer.
```

### 3. Service Start Failed

Check the error log:
```
cat ~/.openclaw/logs/status_uploader_error.log
```

Common errors:
- Token not configured
- Network connection failed
- Port already in use

### 4. Invalid Token

```
❌ Token validation failed

Your token may have expired or is invalid.

Please obtain a new token:
1. Log in to https://openclaw-agent-monitor.vercel.app
2. Go to the Settings page
3. Click Generate to create a new Token
4. Send me the new token
```

## Example Conversations

### First-time Enable

**User:** 启用状态监控 / enable status monitor
**Agent:**
Checking monitoring configuration...

❌ No Agent Token detected

Please complete these steps first:

1. Visit https://openclaw-agent-monitor.vercel.app
2. Click **Sign In** (supports Google/GitHub, etc.)
3. After logging in, generate an Agent Token on the **Settings** page
4. Send me the token

---

**User:** 我的 Token 是 e2d3262f-b626-4850-af11-5f2cb1c0dcad / My token is e2d3262f-b626-4850-af11-5f2cb1c0dcad
**Agent:**
Validating token...

✅ Token validated successfully!

Starting upload service...
- Running initial sync test...
- ✅ Service started successfully!

---

✅ **Status monitor enabled!**

- Monitor platform: https://openclaw-agent-monitor.vercel.app
- Upload interval: 5 minutes
- Service status: running

Management commands:
- Say "sync status" / "同步状态" to manually trigger an upload
- Say "check status monitor" / "查看状态监控" to check service status
- Say "stop status monitor" / "停止状态监控" to stop the service

### Check Service Status

**User:** 查看状态监控 / check status monitor
**Agent:**
Checking upload service status...

✅ Service is running
   PID: 12345
   Sync interval: 5 minutes
   Log file: ~/.openclaw/logs/status_uploader.log

Recent logs:
```
2026-03-29 10:30:01 - INFO - Upload success: ['main', 'coding']
2026-03-29 10:35:02 - INFO - Upload success: ['main', 'coding']
```

Error log: none

### Stop Service

**User:** 停止状态监控 / stop status monitor
**Agent:**
Stopping upload service...

✅ Service stopped

To restart, say "start status monitor" / "启动状态监控".

### Manual Sync

**User:** 同步状态 / sync status
**Agent:**
Executing manual upload...

Online agents: ['main', 'coding']
Upload result: ✅ Success

### Restart Service

**User:** 重启状态监控 / restart status monitor
**Agent:**
Restarting upload service...

✅ Service restarted, PID: 67890

### Check Errors

**User:** 查看状态监控错误日志 / check status monitor error log
**Agent:**
Checking error logs...

Recent errors:
```
2026-03-29 09:15:03 - HTTP 401: Unauthorized
2026-03-29 09:20:01 - Network: [Errno 8] nodename nor servname provided
```

Suggestion: Check if the token is correct, or check your network connection.
