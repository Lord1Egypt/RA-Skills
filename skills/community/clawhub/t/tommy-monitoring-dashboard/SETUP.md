# Live Monitoring Dashboard - Setup Guide

## Quick Test

Test the dashboard formatting:
```bash
cd ~/.openclaw/workspace/skills/live-monitoring-dashboard
node scripts/production-monitor.js once
```

## Integration with OpenClaw

To actually post to Discord, the dashboard needs to run within an OpenClaw session where it has access to the message tool.

### Method 1: Manual Testing from OpenClaw Session

From within an OpenClaw session, you can test the integration:

```javascript
// Run the monitoring dashboard
exec('cd ~/.openclaw/workspace/skills/live-monitoring-dashboard && node scripts/production-monitor.js once')
```

### Method 2: Cron Job Integration (Recommended)

Create a cron job to run the dashboard automatically:

```bash
# Add this cron job to run every 30 seconds
openclaw cron add --name "Live Dashboard Update" --schedule "*/30 * * * * *" --isolated --payload '{"kind": "systemEvent", "text": "exec(\"cd ~/.openclaw/workspace/skills/live-monitoring-dashboard && node scripts/production-monitor.js once\")"}'
```

### Method 3: Full Discord Integration

For actual Discord posting, modify the production monitor to use OpenClaw's message tool:

```javascript
// Within OpenClaw session context:
const dashboardContent = formatDashboardMessage(data);

// Post new message (first time)
message({
    action: 'send',
    target: 'user:311529658695024640',
    message: dashboardContent
});

// Update existing message (subsequent updates)  
message({
    action: 'edit',
    messageId: 'stored_message_id',
    message: dashboardContent
});
```

## ✅ Slice 2 Complete - Discord Integration

The skill now includes **live Discord integration** with automatic updates!

### What's Live:
- **Real-time Discord dashboard** (updates every 30 seconds)
- **Persistent message editing** (no spam, just live updates)
- **Automatic cron job** for continuous monitoring
- **State management** with message ID persistence

### Files Created (Slice 2):
```
└── scripts/
    ├── discord-integration.js     # Discord posting logic
    ├── dashboard-updater.js       # Update mechanism
    └── discord-post.js           # Generated script
```

### Configuration:
- **State file:** `config/live-state.json` (message ID, update tracking)
- **Cron job ID:** `30e374a6-1b35-4d9a-ac35-066ac8e38cc2`
- **Update interval:** 30 seconds

## Files Created

```
live-monitoring-dashboard/
├── SKILL.md                           # Skill documentation
├── package.json                       # Skill metadata
├── install.sh                         # Installation script
├── scripts/
│   ├── monitor.js                     # Core monitoring logic
│   ├── integration.js                 # OpenClaw CLI integration
│   ├── production-monitor.js          # Production monitoring version
│   └── session-runner.js              # OpenClaw session integration
├── config/
│   └── default.json                   # Default configuration
└── SETUP.md                           # This file
```

## Configuration

Edit `config/default.json` to customize:

```json
{
  "channelName": "#tommy-monitoring",
  "updateInterval": 30000,
  "userId": "311529658695024640",
  "features": {
    "subagentTracking": true,
    "cronMonitoring": true, 
    "systemHealth": false
  }
}
```

## Testing the Complete Flow

1. **Install the skill:**
   ```bash
   cd ~/.openclaw/workspace/skills/live-monitoring-dashboard
   ./install.sh
   ```

2. **Test message formatting:**
   ```bash
   node scripts/monitor.js test
   ```

3. **Test with real data:**
   ```bash
   node scripts/production-monitor.js once
   ```

4. **Integration test:**
   ```bash
   node scripts/integration.js
   ```

## Ready for ClawHub Publication

This skill is now ready to be published to ClawHub as a complete, working monitoring solution. The vertical slice approach means users get immediate value from Slice 1 while we continue developing additional features.