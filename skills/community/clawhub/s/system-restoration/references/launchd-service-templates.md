# LaunchD Service Templates

## Daily Schedule Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ranger.SERVICENAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Frameworks/Python.framework/Versions/3.12/bin/python3</string>
        <string>/path/to/script.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/stephendobbins/.config/ranger/scripts</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>6</integer>
        <key>Minute</key>
        <integer>35</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/SERVICENAME.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/SERVICENAME.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

## Interval Schedule Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ranger.SERVICENAME</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Library/Frameworks/Python.framework/Versions/3.12/bin/python3</string>
        <string>/path/to/script.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/stephendobbins/.config/ranger/scripts</string>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>/tmp/SERVICENAME.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/SERVICENAME.err</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

## Service Configuration

### Existing Services

| Service | File | Schedule | Purpose |
|---------|------|----------|---------|
| com.ranger.morning-pulse | com.ranger.morning-pulse.plist | Daily 6:35 AM | Morning pulse |
| com.ranger.margin-alerts | com.ranger.margin-alerts.plist | Every 30 min (1800s) | Zero revenue alerts |
| com.ranger.live-nudges | com.ranger.live-nudges.plist | Every 15 min (900s) | Live dispatch alerts |

### Schedule Types

**StartCalendarInterval** - Daily at specific time:
```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>6</integer>
    <key>Minute</key>
    <integer>35</integer>
</dict>
```

**StartInterval** - Recurring interval in seconds:
```xml
<key>StartInterval</key>
<integer>1800</integer>  <!-- 30 minutes -->
```

Common intervals:
- 15 minutes: 900
- 30 minutes: 1800  
- 1 hour: 3600
- 4 hours: 14400

## Service Management

```bash
# Load service (enable and start)
launchctl load ~/Library/LaunchAgents/com.ranger.SERVICENAME.plist

# Unload service (disable and stop)  
launchctl unload ~/Library/LaunchAgents/com.ranger.SERVICENAME.plist

# Start service immediately (one-time)
launchctl start com.ranger.SERVICENAME

# Check if service is loaded
launchctl list | grep ranger

# View logs
tail -f /tmp/SERVICENAME.log
tail -f /tmp/SERVICENAME.err
```