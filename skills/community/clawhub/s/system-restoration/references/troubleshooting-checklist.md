# System Restoration Troubleshooting Checklist

## Pre-Restoration Investigation

### ☐ 1. Identify What's Broken
- [ ] Check #manager-nudges - Missing morning pulse or live alerts?
- [ ] Check #margin-alerts - Missing zero revenue alerts?  
- [ ] Check #material-intel-systems - Missing material reports?
- [ ] Ask: When did it last work? What changed?

### ☐ 2. Check System Status
```bash
# LaunchD services
launchctl list | grep ranger

# Running processes  
ps aux | grep -E "(pulse|margin|nudge|keel)" | grep -v grep

# Cron jobs
cron list

# Recent logs
ls -la /tmp/*pulse* /tmp/*margin* /tmp/*nudge*
```

### ☐ 3. Locate Code Files
- [ ] Check `/Users/stephendobbins/.config/ranger/scripts/`
- [ ] Check `/Users/stephendobbins/.config/ranger/materials/`
- [ ] Check `/Users/stephendobbins/.openclaw/workspace/`
- [ ] Look for `.bak` backup files

## System-by-System Restoration

### Zero Revenue Alerts

#### ☐ Investigation
- [ ] Script exists: `/Users/stephendobbins/.config/ranger/scripts/margin_alerts.py`
- [ ] LaunchD plist: `/Users/stephendobbins/Library/LaunchAgents/com.ranger.margin-alerts.plist`
- [ ] Service status: `launchctl list | grep margin-alerts`

#### ☐ Restoration Steps
- [ ] Test script: `cd /Users/stephendobbins/.config/ranger/scripts && python3 margin_alerts.py`
- [ ] Load service: `launchctl load ~/Library/LaunchAgents/com.ranger.margin-alerts.plist`
- [ ] Verify posting: Check #margin-alerts for test alerts
- [ ] Check logs: `tail /tmp/margin_alerts.log`

#### ☐ Success Criteria
- [ ] Service shows as loaded: `launchctl list | grep margin-alerts`
- [ ] Finds zero-revenue jobs
- [ ] Posts alerts to #margin-alerts (C0A5L7MG60P)

---

### Morning Pulse

#### ☐ Investigation  
- [ ] Script exists: `/Users/stephendobbins/.config/ranger/scripts/pulse_os_full.py`
- [ ] Backup exists: `pulse_os_full.py.bak`
- [ ] LaunchD plist: `/Users/stephendobbins/Library/LaunchAgents/com.ranger.morning-pulse.plist`
- [ ] Service status: `launchctl list | grep morning-pulse`

#### ☐ Data Source Check
- [ ] **CRITICAL:** Check if API returns real or test data
- [ ] Test API calls vs browser automation
- [ ] Look for terminated employees in data (indicates test data)

#### ☐ Restoration Steps
- [ ] Restore backup: `cp pulse_os_full.py.bak pulse_os_full.py`
- [ ] Fix data sources: Add browser automation imports
- [ ] Load service: `launchctl load ~/Library/LaunchAgents/com.ranger.morning-pulse.plist`
- [ ] Test: `python3 pulse_os_full.py pulse`
- [ ] Verify sections: Low margin, stale estimates, revenue leaks, driver incidents

#### ☐ Success Criteria
- [ ] Service loaded and scheduled for 6:35 AM CT
- [ ] Posts to #manager-nudges (C0A5V9JL2KV)
- [ ] Contains all 4 sections from Feb 19 format
- [ ] Data is current (not test data with terminated employees)

---

### Live Nudges

#### ☐ Investigation
- [ ] Function exists: `grep -n "def run_nudges" pulse_os_full.py`
- [ ] Function is on lines 548-617
- [ ] No existing LaunchD service (needs creation)

#### ☐ Service Creation
- [ ] Create plist: Use `scripts/create-live-nudges-service.py` 
- [ ] Load service: `launchctl load ~/Library/LaunchAgents/com.ranger.live-nudges.plist`
- [ ] Test function: `python3 pulse_os_full.py nudges`

#### ☐ Success Criteria
- [ ] Service runs every 15 minutes
- [ ] Posts 🚗 dispatched / 📍 arrived / ✅ completed alerts
- [ ] Posts to #manager-nudges

---

### Material Truth Report

#### ☐ Investigation
- [ ] Script exists: `/Users/stephendobbins/.config/ranger/materials/reconciliation_report.py`
- [ ] No existing cron job (needs creation)

#### ☐ Restoration Steps
- [ ] Test script: `python3 reconciliation_report.py --no-email`
- [ ] Create cron job for 7:00 AM CT daily
- [ ] Verify channel posting

#### ☐ Success Criteria  
- [ ] Daily execution at 7:00 AM CT
- [ ] Posts "Ranger Materials Intelligence" report
- [ ] Posts to #material-intel-systems (C0A5L7RB5EK)

## Post-Restoration Verification

### ☐ Service Status Check
```bash
# All LaunchD services loaded
launchctl list | grep ranger
# Should show:
# - com.ranger.morning-pulse  
# - com.ranger.margin-alerts
# - com.ranger.live-nudges

# All cron jobs active
cron list
# Should show Material Truth Report
```

### ☐ Channel Activity Check  
- [ ] #manager-nudges - Morning pulse + live nudges
- [ ] #margin-alerts - Zero revenue alerts
- [ ] #material-intel-systems - Daily material reports

### ☐ Log Monitoring (First 24 Hours)
- [ ] Monitor `/tmp/morning_pulse.log`
- [ ] Monitor `/tmp/margin_alerts.log`  
- [ ] Monitor `/tmp/live_nudges.log`
- [ ] Check for errors in `.err` files

## Common Failure Patterns & Solutions

### ServiceTitan API Returns Wrong Data
**Symptoms:** Reports show terminated employees, unrealistic job counts
**Solution:** Switch to browser automation data sources

### LaunchD Services Not Loading
**Symptoms:** `launchctl list` doesn't show service
**Solution:** Check plist syntax, file permissions, reload service

### Scripts Run But Don't Post to Slack
**Symptoms:** Logs show success but no channel messages
**Solution:** Check Slack token, channel IDs, network connectivity

### Data Source Import Errors
**Symptoms:** `ModuleNotFoundError` or import failures  
**Solution:** Check Python path, install missing modules, verify file locations

## Emergency Rollback

If restoration causes issues:

1. **Stop all services:**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.ranger.*.plist
   ```

2. **Remove cron jobs:**
   ```bash
   cron list  # Note job IDs
   cron remove <job-id>
   ```

3. **Kill processes:**
   ```bash  
   pkill -f "pulse_os_full.py"
   pkill -f "margin_alerts.py"
   ```

4. **Restore from known-good state or contact Stephen**