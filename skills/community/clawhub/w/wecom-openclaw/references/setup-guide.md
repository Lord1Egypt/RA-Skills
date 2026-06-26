# WeChat Work + OpenClaw Setup Guide

## Prerequisites

- Node.js 18+
- OpenClaw running locally (default port 18789)
- `cloudflared` CLI installed (`brew install cloudflare/cloudflare/cloudflared`)
- WeChat Work admin account with an enterprise (preferably verified)

## Step 1: Create WeChat Work Application

1. Login: https://work.weixin.qq.com
2. **应用管理** → **自建** → **创建应用**
3. Fill in app name, description, logo
4. Note your **AgentID**

## Step 2: Configure Webhook (Receive Messages)

1. In your app → **接收消息** → **设置API接收**
2. **URL**: Your public endpoint (e.g., `https://your-tunnel.trycloudflare.com/webhook`)
3. **Token**: Generate a random string (will be `WEBHOOK_TOKEN`)
4. **EncodingAESKey**: Click "随机获取" (will be `AGENT_SECRET`)
5. **DO NOT click save yet** — start your adapter first

## Step 3: Get Credentials

From WeChat Work admin console, collect:

| Item | Where to find | .env variable |
|------|--------------|---------------|
| CorpID | 我的企业 → 企业信息 → 企业ID | `CORP_ID` |
| AgentID | 应用管理 → 你的应用 → AgentId | `AGENT_ID` |
| Secret | 应用管理 → 你的应用 → Secret | `APP_SECRET` |
| Token | API接收 → Token | `WEBHOOK_TOKEN` |
| EncodingAESKey | API接收 → EncodingAESKey | `AGENT_SECRET` |

⚠️ **APP_SECRET and AGENT_SECRET are DIFFERENT keys!**
- APP_SECRET = Application Secret (for API access_token)
- AGENT_SECRET = EncodingAESKey (for message encryption)

## Step 4: Deploy Adapter

```bash
bash path/to/wecom-openclaw/scripts/deploy.sh
cd ~/wecom-adapter
nano .env  # Fill in all credentials
npm start
```

## Step 5: Expose Publicly

```bash
cloudflared tunnel --url http://localhost:8090
```

Copy the generated `https://xxx.trycloudflare.com` URL.

## Step 6: Add IP Whitelist

1. In WeChat Work admin → your app → **企业可信IP**
2. Add your server's public IP
3. Find your IP: `curl ifconfig.me`

## Step 7: Verify Webhook

1. Go back to Step 2's webhook settings
2. Enter URL: `https://xxx.trycloudflare.com/webhook`
3. Click **保存**
4. Should succeed if adapter is running correctly

## Step 8: Test

1. Open WeChat Work app on your phone
2. Find your application
3. Send a text message
4. You should receive an AI reply within 10-30 seconds

## Common Issues

### Error -30065 (callback address failed)

- Tunnel not running → restart cloudflared
- Wrong EncodingAESKey → verify AGENT_SECRET matches console
- Not decrypting echostr → adapter must decrypt and return plaintext

### Error 60020 (IP not allowed)

- Add your public IP to trusted IP list in WeChat Work console

### No reply received

- Check `~/wecom-adapter/logs/wecom-adapter.log`
- Verify OpenClaw is running: `curl http://localhost:18789/health`
- Verify OPENCLAW_TOKEN is correct

### Account suspended

- Complete enterprise verification before using API automation
- Avoid rapid testing with many API calls
- Contact WeChat Work support for appeal
