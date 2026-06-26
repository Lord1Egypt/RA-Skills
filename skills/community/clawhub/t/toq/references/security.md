# Security

## Connection modes

- **approval** (default): new agents need your permission. Recommended for most users.
- **open**: anyone can connect. Only for public-facing services.
- **allowlist**: only pre-approved agents can connect. Most restrictive.
- **dns-verified**: agents must have valid DNS records. Good for organizations.

Always default to approval mode. Never suggest open mode unless the user explicitly asks.

## Network security walkthrough

Present this to the user based on their network situation.

### Cloud server (public IP)

"Your agent is on a server with a public internet address. This means:

- Port 9009 is how other agents connect to you. You may need to open it in your cloud provider's firewall settings before other agents can reach you.
- Once port 9009 is open, anyone on the internet can try to connect. They cannot send you messages without your approval (that is what approval mode does), but they can knock on your door.
- Approval mode is your front door lock. Every new agent that tries to connect goes into a waiting list. You decide who gets in.
- If you only plan to talk to one or two specific agents, consider setting up firewall rules that only allow those IPs to connect on port 9009."

### Home network (behind router)

"Your agent is behind your home router. This is the safest setup:

- Agents on your same network can connect directly. No extra setup needed.
- Agents outside your network cannot reach you unless you set up port forwarding.
- If you do set up port forwarding, the same rules apply as a cloud server."

### OpenClaw exec tool interaction

This is the most important security consideration. When a remote agent sends a toq message, that message content reaches the AI. If exec is enabled without approval mode, the AI could be influenced by message content to run commands.

Mitigations:
1. Enable OpenClaw's exec approval mode so every command requires human confirmation
2. Use toq's approval or allowlist connection mode so only trusted agents can send messages
3. Both protections together provide defense in depth

Before creating any handler or notification that forwards messages into the conversation, check the connection mode with `toq status` and warn the user about these risks.

## DNS setup

To set up DNS discovery:
1. Add an A record pointing the domain to the server's public IP
2. Add a TXT record: `_toq._tcp.<domain>` with value `v=toq1; key=<public-key>; agent=<name>`
3. If using a non-default port, add `port=<port>` to the TXT record
4. Verify with `toq discover <domain>`

Before setting up DNS, make sure connection mode is approval or stricter. A DNS name makes the agent discoverable by anyone who knows the domain.

## Auto-start on reboot

On Linux with systemd:
```
cat > /tmp/toq.service << EOF
[Unit]
Description=toq protocol daemon
After=network.target

[Service]
Type=forking
User=$USER
ExecStart=$(which toq) up
ExecStop=$(which toq) down
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
sudo mv /tmp/toq.service /etc/systemd/system/toq.service
sudo systemctl daemon-reload
sudo systemctl enable toq
```

On macOS with launchd:
```
cat > ~/Library/LaunchAgents/com.toqprotocol.toq.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.toqprotocol.toq</string>
    <key>ProgramArguments</key><array><string>/usr/local/bin/toq</string><string>up</string></array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.toqprotocol.toq.plist
```
