# WHOOP Connect Setup Guide

## Why do I need a developer account?

WHOOP doesn't have a public API — you can't just pull your data with a simple request. To let your AI agent read your recovery, sleep, and workout data, you need to create a free "developer app" on WHOOP's platform. This gives you a pair of credentials (Client ID + Client Secret) that authorize the skill to access **your own data only**, using the industry-standard OAuth protocol.

- It's free and takes about 5 minutes
- You're only granting **read access** to your own account
- Your data is stored locally in `~/.whoop/whoop.db` — nothing is uploaded anywhere
- You can revoke access anytime from the WHOOP developer dashboard

## Step 1: Register as WHOOP Developer (5 minutes)

1. Go to https://developer.whoop.com
2. Sign in with your WHOOP account (the same one linked to your WHOOP band)
3. Click "Create Application"
4. Fill in:
   - **App Name**: anything you like (e.g. "My Health Bot")
   - **Description**: anything
   - **Redirect URI**: `http://localhost:3000/callback`
   - **Scopes**: select ALL read scopes (profile, body measurement, recovery, sleep, workout, cycle)
   - **Webhooks**: skip for now (can add later)
5. After creating, you'll see **Client ID** and **Client Secret** — save these

## Step 2: Set Environment Variables

Add to your shell profile or OpenClaw config:

```bash
export WHOOP_CLIENT_ID="your_client_id_here"
export WHOOP_CLIENT_SECRET="your_client_secret_here"
```

## Step 3: Authorize

The first time you use the skill, it will detect missing tokens and run the OAuth flow automatically. You'll see a URL — open it in your browser, authorize, and you're done. Tokens refresh automatically after that.

## That's it!

You can now ask things like "how's my recovery?" or "how did I sleep last night?"

---

## Optional: Webhook Setup (Advanced)

Webhooks let WHOOP push data to you in real-time (e.g. recovery ready notification as soon as you wake up). This requires a server with a public HTTPS endpoint.

### Requirements

- A server with a public IP
- A domain name with DNS you control
- nginx + certbot (or similar reverse proxy with SSL)

### Steps

1. **nginx config** — create a site that proxies `/whoop/webhook` to `localhost:9876`:

```nginx
server {
    listen 80;
    server_name your-domain.example.com;

    location /whoop/webhook {
        proxy_pass http://127.0.0.1:9876;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        proxy_pass http://127.0.0.1:9876;
    }
}
```

2. **SSL** — `certbot --nginx -d your-domain.example.com`

3. **Start webhook server** — run as a systemd service:

```ini
[Unit]
Description=WHOOP Webhook Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/whoop-connect/scripts
Environment=WHOOP_CLIENT_ID=your_id
Environment=WHOOP_CLIENT_SECRET=your_secret
ExecStart=/usr/bin/python3 webhook_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

4. **Register in WHOOP Dashboard** — go back to https://developer.whoop.com, edit your app, add the webhook URL (e.g. `https://your-domain.example.com/whoop/webhook`), select Model Version V2.

5. **Verify** — `curl https://your-domain.example.com/health` should return `{"status":"ok"}`

### Daily Sync (Recommended)

Even with webhooks, add a daily cron as safety net:

```bash
0 8 * * * cd /path/to/whoop-connect/scripts && WHOOP_CLIENT_ID=... WHOOP_CLIENT_SECRET=... python3 daily_sync.py >> /var/log/whoop-sync.log 2>&1
```
