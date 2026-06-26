# LaunchAgent notes for tbot

## Why LaunchAgent

- Runs in user context (no root required).
- Good fit for OpenClaw host setups where agent runs as a user account.
- Starts at login and can be started immediately with `launchctl bootstrap`.

## Common operations

```bash
# Load/start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.tbot.plist

# Restart
launchctl kickstart -k gui/$(id -u)/com.openclaw.tbot

# Stop/unload
launchctl bootout gui/$(id -u)/com.openclaw.tbot

# Inspect status
launchctl print gui/$(id -u)/com.openclaw.tbot
```

## Caveats

- LaunchAgent requires a logged-in user session.
- For boot-before-login behavior, use LaunchDaemon (root-owned), which requires sudo/root setup.
