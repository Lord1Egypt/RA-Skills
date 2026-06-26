# Common Verification Checklist for OpenClaw Upgrades

This document provides a catalog of common verification tests that can be referenced during post-upgrade audits. Not all tests apply to every upgrade—select based on identified risks.

## Pre-Upgrade Verification

Always run these before any upgrade:

### Core Health Checks
```bash
# 1. Check overall system health
cd $HOME/repo/apps/openclaw && pnpm openclaw doctor

# 2. Verify config validity
openclaw config validate

# 3. Create config-only backup (lightweight, ~16MB)
# Note: Backup CLI does not auto-cleanup. Manage retention manually.
openclaw backup create --only-config --verify

# Alternative: Full backup including sessions (~5GB)
# openclaw backup create --verify

# 4. Document current state
openclaw status > /tmp/pre-upgrade-status.txt
git -C $HOME/repo/apps/openclaw log -1 > /tmp/pre-upgrade-version.txt
```

#### Backup Management

**Important**: `openclaw backup create` does not auto-cleanup old backups. To avoid disk space issues:

**Option 1: Config-Only Backups (Recommended for Upgrade Guardian)**
```bash
# Only backup config (16MB vs 5GB for full backup)
openclaw backup create --only-config --verify
```

**Option 2: Manual Cleanup for Full Backups**
```bash
# Keep only last 7 backups (if using full backups)
ls -t ~/Backups/openclaw/*.tar.gz | tail -n +8 | xargs rm -f

# Or use find to delete backups older than 7 days
find ~/Backups/openclaw -name "*.tar.gz" -mtime +7 -delete
```

**Option 3: Dedicated Backup Directory**
```bash
# Create organized backup location
mkdir -p ~/Backups/openclaw
openclaw backup create --only-config --output ~/Backups/openclaw --verify
```

---

## Post-Upgrade Verification

### Category 1: Gateway & Service Health

#### 1.1 Gateway Startup
**Purpose**: Verify gateway starts without critical errors
```bash
# Check gateway is running
openclaw status

# Check logs for errors
openclaw gateway logs --tail 100 | grep -i error

# Verify no auth complaints
openclaw gateway logs --tail 100 | grep -i "auth\|token\|password"
```
**Pass criteria**: Gateway shows "healthy", no auth-related errors

#### 1.2 Config Loading
**Purpose**: Verify config is loaded successfully
```bash
# Check for config errors
openclaw gateway logs --tail 100 | grep -i "invalid config\|validation error"

# Verify agents loaded
openclaw config get agents.list | jq '.[].id'
```
**Pass criteria**: All expected agents are listed, no validation errors

---

### Category 2: Bot Functionality

#### 2.1 Telegram Bot Response
**Purpose**: Verify bot responds in group chats
```bash
# Manual test: Send message in group
# "@bot_name /status" or "@bot_name ping"

# Check logs for delivery
openclaw gateway logs --tail 50 | grep -i "telegram.*deliver"
```
**Pass criteria**: Bot responds within 10 seconds, no errors in logs

#### 2.2 Group Routing
**Purpose**: Verify messages route to correct agents
```bash
# Manual test: Send message in group with specific agent binding
# Check which agent session receives the message

# Verify session created
ls -lh ~/.openclaw/sessions/ | grep "{GROUP_ID}"
```
**Pass criteria**: Message routes to expected agent, session file created

#### 2.3 DM Functionality
**Purpose**: Verify DMs work if dmPolicy is enabled
```bash
# Manual test: Send DM to bot
# Check logs for pairing/routing

# Check for DM-specific errors
openclaw gateway logs --tail 50 | grep -i "dm.*pairing\|dm.*policy"
```
**Pass criteria**: DM accepted (if pairing configured) or correctly rejected

---

### Category 3: Model & Provider Tests

#### 3.1 Primary Model Invocation
**Purpose**: Verify primary model works
```bash
# Manual test via TUI or chat
# "Say hello" or simple prompt

# Check logs for model usage
openclaw gateway logs --tail 50 | grep -i "model\|provider"
```
**Pass criteria**: Response received, no provider errors

#### 3.2 Fallback Model Chain
**Purpose**: Verify fallback works if primary fails
```bash
# Simulate failure or trigger high-cost scenario
# Check logs for fallback attempts

openclaw gateway logs --tail 100 | grep -i "fallback\|failover"
```
**Pass criteria**: Fallback chain activates, response received

#### 3.3 Custom OpenAI-Compatible Providers
**Purpose**: Verify custom endpoints work
```bash
# Test provider specifically configured in models.providers
# e.g., google-antigravity, gemini-local

# Check for streaming errors
openclaw gateway logs --tail 100 | grep -i "streaming\|parse error"
```
**Pass criteria**: Streaming responses complete without mid-stream failure

---

### Category 4: Session & Memory

#### 4.1 Session Creation
**Purpose**: Verify sessions are created correctly
```bash
# Trigger a conversation
ls -lh ~/.openclaw/sessions/ | tail -5

# Verify session metadata
jq '.conversationLabel, .model.primary' ~/.openclaw/sessions/{SESSION_KEY}.json
```
**Pass criteria**: Session file created, metadata correct

#### 4.2 Session Reset
**Purpose**: Verify /reset command works
```bash
# Manual test: Send "/reset" in chat
# Verify new session starts

# Check for old session archival
ls -lh ~/.openclaw/sessions/*.archive
```
**Pass criteria**: New session starts, old session archived

#### 4.3 Memory/Compaction
**Purpose**: Verify compaction doesn't break sessions
```bash
# Trigger a long conversation (>100 turns)
# Check session file size

ls -lh ~/.openclaw/sessions/{SESSION_KEY}.json

# Verify no data loss
jq '.messages | length' ~/.openclaw/sessions/{SESSION_KEY}.json
```
**Pass criteria**: Session compacts without losing critical context

---

### Category 5: TUI & CLI

#### 5.1 TUI Session Isolation
**Purpose**: Verify `/new` creates independent sessions (v2026.3.7+)
```bash
# Open TUI: openclaw tui
# Run: /new
# Check session key in TUI header

# Verify session file
ls ~/.openclaw/sessions/tui-*
```
**Pass criteria**: `/new` creates `tui-<uuid>` session, not shared reset

#### 5.2 TUI `/reset` Behavior
**Purpose**: Verify `/reset` clears shared session
```bash
# In TUI: /reset
# Verify conversation cleared

# Check session reset timestamp
jq '.resetAt' ~/.openclaw/sessions/main.json
```
**Pass criteria**: Shared session cleared, resetAt updated

#### 5.3 CLI Commands
**Purpose**: Verify CLI commands work
```bash
# Test key commands
openclaw status
openclaw agents list
openclaw sessions list
```
**Pass criteria**: All commands return expected output

---

### Category 6: Cron & Automation

#### 6.1 Cron Job Execution
**Purpose**: Verify cron jobs run
```bash
# Check cron status
openclaw cron status

# Trigger manual run
openclaw cron run {JOB_NAME}

# Check logs
openclaw gateway logs --tail 50 | grep -i "cron.*run"
```
**Pass criteria**: Job executes, logs show completion

#### 6.2 Cron Async Behavior (v2026.3.7+)
**Purpose**: Verify cron.run returns enqueued response
```bash
# Run cron job manually
openclaw cron run {JOB_NAME}

# Verify response format
# Should return: { "ok": true, "enqueued": true, "runId": "..." }
```
**Pass criteria**: Returns enqueued response, job completes asynchronously

---

### Category 7: Browser & Media

#### 7.1 Browser CDP Connection
**Purpose**: Verify browser automation works
```bash
# Test browser tool (if configured)
# In agent chat: "Open https://example.com and take screenshot"

# Check logs for CDP errors
openclaw gateway logs --tail 50 | grep -i "cdp\|browser.*error"
```
**Pass criteria**: Browser tool executes, no CDP connection errors

#### 7.2 Media Uploads
**Purpose**: Verify media attachments work
```bash
# Send image/file to bot in chat
# Check logs for upload

openclaw gateway logs --tail 50 | grep -i "media.*upload\|attachment"
```
**Pass criteria**: Media processed, no upload errors

---

### Category 8: Security & Auth

#### 8.1 Gateway Auth Mode
**Purpose**: Verify gateway.auth.mode is respected
```bash
# Check auth mode in config
openclaw config get gateway.auth.mode

# Verify no auth errors
openclaw gateway logs --tail 50 | grep -i "auth.*mode\|ambiguous auth"
```
**Pass criteria**: Auth mode matches config, no ambiguity errors

#### 8.2 SecretRef Resolution
**Purpose**: Verify SecretRef-managed secrets work
```bash
# Check for SecretRef errors
openclaw gateway logs --tail 50 | grep -i "secretref\|unresolved secret"

# Test model with SecretRef API key
# "Say hello" using that model
```
**Pass criteria**: SecretRef resolves, model works

---

### Category 9: Routing & Delivery

#### 9.1 Duplicate Reply Suppression
**Purpose**: Verify no duplicate replies in groups
```bash
# Send message in group with bot
# Verify only one response

# Check logs for delivery dedupe
openclaw gateway logs --tail 50 | grep -i "dedupe\|duplicate.*suppress"
```
**Pass criteria**: Single response, no double-delivery

#### 9.2 Legacy Session Routing
**Purpose**: Verify legacy session keys still route
```bash
# If using custom session keys (agent:<id>:custom:<name>)
# Trigger message that routes to that session

# Check delivery logs
openclaw gateway logs --tail 50 | grep -i "route.*legacy"
```
**Pass criteria**: Routes correctly to legacy session

---

## Risk-Specific Tests

### For Gateway Auth Mode Breaking Change (v2026.3.7)
```bash
# Verify mode is set
openclaw config get gateway.auth.mode

# Should return "token" or "password", not null
```

### For TUI `/new` Behavior Change (v2026.3.7+)
```bash
# Test /new creates independent session
openclaw tui --agent {AGENT} --session test-new
# In TUI: /new
# Verify new session key (tui-<uuid>)
```

### For Streaming Compatibility (v2026.3.7+)
```bash
# Test long response from custom provider
# In chat: "Write a 500-word essay on..."
# Verify no mid-stream failure
```

### For Cron Async Change (v2026.3.7+)
```bash
# Test cron.run returns enqueued
openclaw cron run {JOB_NAME}
# Verify response has "enqueued": true
```

---

## Quick Reference: Essential Tests

For most upgrades, these 5 tests cover 80% of risks:

1. ✅ Gateway starts: `openclaw status`
2. ✅ Bot responds in group: `@bot /status`
3. ✅ Model works: "Say hello"
4. ✅ No auth errors: Check logs for "auth"
5. ✅ Session works: Verify session file created

If all 5 pass, the upgrade is likely successful. Use additional tests for specific risks.

---

## Automation Script

You can bundle these into a shell script:

```bash
#!/bin/bash
# post-upgrade-check.sh

echo "🔍 Running post-upgrade checks..."

# Gateway health
echo "1️⃣ Checking gateway status..."
openclaw status || exit 1

# Config validation
echo "2️⃣ Validating config..."
openclaw config validate || exit 1

# Logs check
echo "3️⃣ Checking for errors..."
ERRORS=$(openclaw gateway logs --tail 100 | grep -i error | wc -l)
if [ "$ERRORS" -gt 0 ]; then
  echo "⚠️  Found $ERRORS error(s) in logs"
  openclaw gateway logs --tail 100 | grep -i error
fi

echo "✅ Basic checks complete. Manual tests:"
echo "  - Send @bot /status in group"
echo "  - Test model invocation"
echo "  - Verify session creation"
```

Make it executable: `chmod +x post-upgrade-check.sh`

---

## Extended Monitoring (Post-Upgrade)

### Setup monitoring before leaving upgrade unattended

**Option 1: Quick Verification (5 minutes, recommended for most cases)**
```bash
# Run immediate checks after upgrade
for i in {1..10}; do
    echo "Check #$i - $(date)"
    pgrep -f "gateway" && echo "✅ Gateway OK" || echo "⚠️  Gateway down!"
    openclaw logs --since 1m 2>&1 | grep -qiE "error|streaming" && echo "⚠️  Issues found" || echo "✅ No issues"
    sleep 30
done
```

**Option 2: Extended Monitoring (24 hours, automated)**
```bash
# Create monitoring script
cat > ~/openclaw-upgrade-monitor.sh <<'SCRIPT'
#!/bin/bash
LOG_FILE="$HOME/openclaw-upgrade-monitor.log"
echo "=== Monitoring started at $(date) ===" >> "$LOG_FILE"

# Check every 30 minutes for 24 hours (48 checks)
for i in {1..48}; do
    echo "Check #$i - $(date)" >> "$LOG_FILE"
    
    # Gateway status
    pgrep -f "gateway" >/dev/null && echo "✅ Gateway OK" >> "$LOG_FILE" || echo "⚠️  Gateway down!" >> "$LOG_FILE"
    
    # Error check
    ERROR_COUNT=$(openclaw logs --since 10m 2>&1 | grep -ci "error" || echo "0")
    echo "Errors (last 10m): $ERROR_COUNT" >> "$LOG_FILE"
    
    # Streaming check
    openclaw logs --since 10m 2>&1 | grep -qiE "parse error|streaming" && echo "⚠️  Streaming issues" >> "$LOG_FILE" || echo "✅ Streaming OK" >> "$LOG_FILE"
    
    echo "" >> "$LOG_FILE"
    [ $i -lt 48 ] && sleep 1800  # 30 minutes
done
echo "=== Monitoring complete at $(date) ===" >> "$LOG_FILE"
SCRIPT

chmod +x ~/openclaw-upgrade-monitor.sh

# Run in background
nohup bash ~/openclaw-upgrade-monitor.sh &

# Check results anytime
tail -f ~/openclaw-upgrade-monitor.log
```

**Option 3: One-Shot Validation (recommended)**
```bash
# Verify immediately after upgrade, then manually check back in 24h
echo "=== Post-Upgrade Check - $(date) ===" > ~/post-upgrade-check.txt
openclaw status >> ~/post-upgrade-check.txt
openclaw logs --since 5m 2>&1 | grep -iE "error|streaming" >> ~/post-upgrade-check.txt 2>&1 || echo "No issues" >> ~/post-upgrade-check.txt

# Check back in 24 hours manually:
# openclaw logs --since 24h | grep -iE "error|streaming"
```

### What to Monitor

| Indicator | Command | Alert Threshold |
|-----------|---------|-----------------|
| Gateway crashes | `pgrep -f "gateway"` | Process not running |
| Parse errors | `grep -c "parse error" logs` | Any occurrence |
| Streaming errors | `grep -c "streaming" logs` | Any occurrence |
| Auth errors | `grep -c "auth.*error" logs` | Any occurrence |
| Session failures | `grep -c "session.*fail" logs` | > 5 per hour |

### Summary

- **Most users**: Use Option 1 (quick 5-min check) or Option 3 (one-shot + manual follow-up)
- **Production systems**: Use Option 2 (24h automated monitoring)
- **All options**: Check logs for `parse error`, `streaming`, `auth` keywords
