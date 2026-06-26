# Step 08 — Channel Integration

## Goal
Connect the agent to the surfaces where staff and customers will actually interact with it.
Different roles suit different channels. Test each connection before proceeding.

---

## Channel Selection Guide

| Channel | Best For | Setup Complexity | Who Uses It |
|---------|---------|-----------------|------------|
| 企业微信 (WeCom) | Staff-facing roles | ⭐⭐ Medium | Employees |
| 微信公众号 | Customer-facing, broad reach | ⭐⭐ Medium | Customers |
| 微信小程序 | Customer-facing, richer UI | ⭐⭐⭐ Complex | Customers |
| 飞书 (Lark) | Staff-facing, tech-forward teams | ⭐⭐ Medium | Employees |
| Web Kiosk UI | In-store self-service screen | ⭐ Simple | Customers |
| WhatsApp | International/cross-border stores | ⭐⭐ Medium | Customers |
| SMS / IVR | Offline backup, elderly users | ⭐⭐⭐ Complex | Customers |

---

## Setup Guides

### 企业微信 (WeCom) Bot
**Use when:** Agent serves internal staff (stock manager, training, manager assistant)

Setup steps:
1. Log into WeCom Admin Console → App Management → Create Internal App
2. Enable messaging permissions
3. Note: `AgentId`, `Secret`, `CorpId`
4. Set Webhook URL to your OpenClaw gateway endpoint
5. In OpenClaw config, set `channel: wecom` with the 3 credentials above
6. Send test message: `/ping`

Required fields:
```
corp_id: "ww..."
agent_id: "100..."
agent_secret: "..."
```

---

### 微信公众号 (WeChat Official Account)
**Use when:** Agent serves customers, store has existing WeChat followers

Setup steps:
1. Log into mp.weixin.qq.com → Basic Configuration
2. Enable Developer Mode
3. Note: `AppID`, `AppSecret`
4. Set server URL to OpenClaw gateway endpoint
5. Set Token (any string, must match OpenClaw config)
6. Verify server (WeChat will send a GET challenge)
7. Enable message encryption (recommended)

Required fields:
```
appid: "wx..."
app_secret: "..."
token: "..."
encoding_aes_key: "..." (optional but recommended)
```

---

### 微信小程序 (WeChat Mini Program)
**Use when:** Rich customer-facing UI needed (product browsing, image-based queries)

Requires a developer or technical team to integrate the Mini Program with OpenClaw API.
Provide them the API endpoint and auth token after completing Step 09.

**For non-technical users:** Use WeChat Official Account instead.

---

### 飞书 (Lark) Bot
**Use when:** Company uses Lark for internal comms

Setup steps:
1. Open Lark Developer Console → Create App → Bot
2. Enable "Receive messages" permissions
3. Note: `App ID`, `App Secret`
4. Set Event Callback URL to OpenClaw gateway endpoint
5. Verify endpoint
6. Publish app to your workspace

Required fields:
```
app_id: "cli_..."
app_secret: "..."
verification_token: "..."
```

---

### Web Kiosk UI
**Use when:** In-store self-service screen or iPad at counter

Setup steps:
1. OpenClaw generates a unique Web Chat URL for this agent
2. Open that URL in the browser on the kiosk device
3. Set browser to full-screen / kiosk mode
4. (Optional) Add store logo and custom welcome screen via OpenClaw webchat config

Required fields:
```
kiosk_title: "欢迎光临 [门店名]"
kiosk_welcome: "您好！我是[名字]，有什么可以帮您？"
```

No API keys needed. Simplest setup.

---

### WhatsApp
**Use when:** Cross-border stores or international customer base

Requires WhatsApp Business API (via Meta Business Suite or third-party BSP like 360Dialog, Twilio).
Follow OpenClaw's WhatsApp configuration guide.

---

## Multi-Channel Configuration

A single agent can serve multiple channels simultaneously.
Each channel can have a slightly different opening message and UI, but shares the same:
- Knowledge base
- Skills configuration
- Persona (name/tone)
- Escalation routing

**Recommended multi-channel setup for typical retail:**
- **Customers:** WeChat Official Account (primary) + Web Kiosk (in-store)
- **Staff:** WeCom Bot (primary)
- **Manager:** WeCom private channel or dedicated agent

---

## Output Format

```json
{
  "channels": [
    {
      "channel_id": "wecom",
      "status": "connected",
      "audience": "staff",
      "test_passed": true,
      "credentials_env": "WECOM_CORP_ID, WECOM_AGENT_ID, WECOM_SECRET"
    },
    {
      "channel_id": "wechat_mp",
      "status": "connected",
      "audience": "customers",
      "test_passed": true,
      "credentials_env": "WECHAT_APPID, WECHAT_SECRET, WECHAT_TOKEN"
    }
  ]
}
```

Save as `channels_config` in agent memory.
Never log or save raw credential values — use env var references only.

Proceed to Step 09.
