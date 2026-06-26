---
name: system-restoration
description: Restore Advantage HPE operational intelligence systems. Use when systems are down, missing alerts, broken scheduling, or data source issues. Covers LaunchD services, cron jobs, API fixes, and service restoration for zero revenue alerts, morning pulse, live nudges, and material truth reports.
---

# System Restoration

Comprehensive guide for restoring Advantage HPE's operational intelligence systems when they fail or go down.

## Investigation Workflow

### 1. System Status Assessment

Before fixing anything, map out what's broken:

**Core Intelligence Systems:**
1. **Zero Revenue Alerts** → #margin-alerts (Every 30 min)
2. **Morning Pulse** → #manager-nudges (Daily 6:35 AM)  
3. **Live Nudges** → #manager-nudges (Every 15 min)
4. **Material Truth Report** → #material-intel-systems (Daily 7:00 AM)
5. **Friend-Zone Reformatter** → #live-ops (ServiceTitan email alerts)

**Investigation Commands:**
```bash
# Check LaunchD services
launchctl list | grep ranger

# Check cron jobs  
cron list

# Check running processes
ps aux | grep -E "(keel|pulse|margin|nudge)" | grep -v grep

# Find system code
find /Users/stephendobbins/.config/ranger -name "*.py" | grep -E "(pulse|margin|nudge)"
find /Users/stephendobbins/.openclaw/workspace -name "*.py" | grep -E "(zero|revenue)"
```

### 2. Locate Code & Determine Failure Cause

**Common Locations:**
- `/Users/stephendobbins/.config/ranger/scripts/` - Main operational scripts
- `/Users/stephendobbins/.config/ranger/materials/` - Material intelligence  
- `/Users/stephendobbins/.openclaw/workspace/` - Recent scripts & fixes
- `/Users/stephendobbins/Library/LaunchAgents/` - LaunchD service definitions

**Common Failure Patterns:**
- **LaunchD services unloaded** - Emergency shutdown or system restart
- **Data source broken** - ServiceTitan API returning wrong data
- **Scheduling missing** - Functions exist but no cron/LaunchD trigger
- **Script errors** - Import failures, credential issues

## System-Specific Restoration

### Zero Revenue Alerts

**Script:** `/Users/stephendobbins/.config/ranger/scripts/margin_alerts.py`
**Channel:** #margin-alerts (C0A5L7MG60P)
**Schedule:** Every 30 minutes

**Restoration Steps:**
1. Verify script exists and posts to Slack
2. Load LaunchD service: `launchctl load /Users/stephendobbins/Library/LaunchAgents/com.ranger.margin-alerts.plist`
3. Test manually: `cd /Users/stephendobbins/.config/ranger/scripts && python3 margin_alerts.py`
4. Check logs: `tail /tmp/margin_alerts.log`

### Morning Pulse

**Script:** `/Users/stephendobbins/.config/ranger/scripts/pulse_os_full.py`
**Channel:** #manager-nudges (C0A5V9JL2KV)
**Schedule:** Daily 6:35 AM CT

**Restoration Steps:**
1. **If broken API data:** Check for `.bak` backup with working data sources
2. **Restore backup:** `cp pulse_os_full.py.bak pulse_os_full.py`
3. **Fix data sources:** Replace API calls with browser automation (see references/browser-data-sources.md)
4. Load LaunchD service: `launchctl load /Users/stephendobbins/Library/LaunchAgents/com.ranger.morning-pulse.plist`
5. Test: `python3 pulse_os_full.py pulse`

### Live Nudges  

**Script:** `/Users/stephendobbins/.config/ranger/scripts/pulse_os_full.py nudges`
**Channel:** #manager-nudges
**Schedule:** Every 15 minutes

**Function:** `run_nudges()` on line 548-617
**Features:** 🚗 dispatched / 📍 arrived / ✅ completed alerts

**Restoration Steps:**
1. Verify function exists: `grep -n "def run_nudges" pulse_os_full.py`
2. Create LaunchD service (see scripts/create-live-nudges-service.py)
3. Load service: `launchctl load /Users/stephendobbins/Library/LaunchAgents/com.ranger.live-nudges.plist`
4. Test: `python3 pulse_os_full.py nudges`

### Material Truth Report

**Script:** `/Users/stephendobbins/.config/ranger/materials/reconciliation_report.py`
**Channel:** #material-intel-systems (C0A5L7RB5EK)  
**Schedule:** Daily 7:00 AM CT

**Restoration Steps:**
1. Test script: `cd /Users/stephendobbins/.config/ranger/materials && python3 reconciliation_report.py --no-email`
2. Create cron job with 7:00 AM schedule
3. Verify channel posting

## Data Source Repair

### ServiceTitan API vs UI Data

**Problem:** ServiceTitan API often returns test/historical data instead of real operational data.

**Solution:** Replace API calls with browser automation:

1. **Create browser data source module** (see scripts/browser_data_sources.py)
2. **Import in main script:** Replace parse functions with browser equivalents  
3. **Preserve output format** - Same sections, different data source

**Browser Data Functions:**
- `get_browser_low_margin_jobs()` 
- `get_browser_stale_estimates()`
- `get_browser_revenue_leaks()`
- `get_browser_driver_incidents()`

### KEEL System Issues

**Script:** `/Users/stephendobbins/.config/ranger/keel/keel_slack_bot.py`

**Safe restart for field tech DM only:**
1. **Disable operational intelligence:** Set `OPERATIONAL_INTELLIGENCE_ENABLED = False`
2. **Restart process:** `cd /Users/stephendobbins/.config/ranger/keel && python3 keel_slack_bot.py &`
3. **Verify running:** `ps aux | grep keel_slack_bot`

## Service Management Commands

### LaunchD Services
```bash
# List services
launchctl list | grep ranger

# Load service  
launchctl load /Users/stephendobbins/Library/LaunchAgents/com.ranger.<service>.plist

# Unload service
launchctl unload /Users/stephendobbins/Library/LaunchAgents/com.ranger.<service>.plist

# Start service immediately
launchctl start com.ranger.<service>

# Check service logs
tail /tmp/<service>.log
tail /tmp/<service>.err
```

### Cron Jobs (OpenClaw)
```bash
# List jobs
cron list

# Add job  
cron add <job-definition>

# Remove job
cron remove <job-id>
```

## Emergency Shutdown Recovery

When systems are emergency-stopped due to bad data:

1. **Investigate root cause** - Usually ServiceTitan API data issues
2. **Fix data sources** - Switch to browser automation or correct API endpoints  
3. **Test manually** - Verify data accuracy before re-enabling
4. **Restore services** - Load LaunchD services and cron jobs
5. **Monitor initially** - Check logs and channel posts for accuracy

## Resources

### scripts/
- `create-live-nudges-service.py` - Generate LaunchD plist for live nudges
- `browser_data_sources.py` - Browser automation replacement for broken APIs

### references/  
- `launchd-service-templates.md` - LaunchD plist templates for different schedules
- `channel-ids.md` - Slack channel IDs for all operational intelligence channels
- `troubleshooting-checklist.md` - Step-by-step debugging guide