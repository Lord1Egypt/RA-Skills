---
name: wecom-openclaw
description: Integrate WeChat Work (Enterprise WeChat) with OpenClaw for intelligent messaging. Enables receiving messages from WeChat Work, processing them with Claude AI, and sending async replies. Handles msg_signature verification, AES-256-CBC encryption/decryption, and secure token-based authentication. Use when setting up bidirectional WeChat Work ↔ OpenClaw communication.
---

# WeChat Work → OpenClaw Adapter

## Quick Start

```bash
# 1. Deploy
bash <skill_dir>/scripts/deploy.sh

# 2. Edit .env with your WeChat Work credentials
nano ~/wecom-adapter/.env

# 3. Start
cd ~/wecom-adapter && npm start

# 4. Expose publicly
cloudflared tunnel --url http://localhost:8090

# 5. Copy tunnel URL → WeChat Work admin → webhook URL
```

## Architecture

```
WeChat Work → HTTPS → Cloudflare Tunnel → Node.js Adapter (8090)
                                              ├─ Verify msg_signature (SHA1)
                                              ├─ Decrypt message (AES-256-CBC)
                                              ├─ Return "success" within 5s
                                              └─ Async: call OpenClaw → send reply via WeCom API
```

**Key**: Adapter returns `success` immediately, then sends AI reply asynchronously via WeChat Work's `message/send` API. This avoids the 5-second timeout.

## ⚠️ Critical Gotchas (Learned the Hard Way)

### 1. Parameter name is `msg_signature`, NOT `signature`

WeChat Work sends `?msg_signature=xxx`, not `?signature=xxx`. Reading `req.query.signature` will always be `undefined`.

### 2. Signature must include echostr/encrypt

**GET verification**: `SHA1(sort([token, timestamp, nonce, echostr]))`
**POST messages**: `SHA1(sort([token, timestamp, nonce, encrypt]))`

NOT `SHA1(sort([token, timestamp, nonce]))` — the encrypted payload MUST participate in the signature.

### 3. echostr must be DECRYPTED before returning

WeChat Work sends an AES-encrypted echostr. You must:
1. Verify msg_signature
2. AES-256-CBC decrypt the echostr
3. Strip PKCS#7 padding
4. Extract message from format: `16-byte random + 4-byte length (BE) + message + CorpID`
5. Return the **decrypted message** (not the raw echostr)

### 4. APP_SECRET ≠ EncodingAESKey

- **APP_SECRET** (应用密钥): Used to get `access_token` for sending messages
- **AGENT_SECRET / EncodingAESKey**: Used for AES encryption/decryption
- These are TWO DIFFERENT keys from the WeChat Work console

### 5. Express body parser must accept multiple Content-Types

WeChat Work may send XML as `text/xml`, `application/xml`, or other types:
```javascript
app.use(express.text({ type: ['application/xml', 'text/xml', 'text/plain', '*/*'] }));
```

### 6. Async reply pattern is mandatory

WeChat Work requires response within 5 seconds. AI responses take 5-30s. Solution:
1. Return `res.status(200).send('success')` immediately
2. Call OpenClaw asynchronously
3. Send reply via `POST /cgi-bin/message/send?access_token=xxx`

### 7. IP whitelist required for sending messages

WeChat Work API (`qyapi.weixin.qq.com`) requires your server's public IP in the app's trusted IP list. Error `60020` means IP not whitelisted.

### 8. Enterprise verification required

⚠️ **Unverified enterprises risk account suspension.** WeChat may ban accounts that use API automation without proper enterprise verification. Complete verification before production use.

### 9. Cloudflare quick tunnels are unstable

Quick (account-less) tunnels generate new URLs on restart and may disconnect unexpectedly. For production, use Named Tunnels ($7/mo) or a static IP.

## Environment Variables

```env
CORP_ID=ww...              # From WeChat Work admin
AGENT_ID=1000003           # Application agent ID
AGENT_SECRET=xxx           # EncodingAESKey (43-char Base64, for encryption)
APP_SECRET=xxx             # Application Secret (for access_token)
WEBHOOK_TOKEN=xxx          # Token configured in webhook settings
OPENCLAW_TOKEN=xxx         # OpenClaw gateway bearer token
OPENCLAW_BASE_URL=http://localhost:18789  # OpenClaw gateway URL
CLAUDE_MODEL=claude-haiku-4-5             # AI model
```

## Files

- `scripts/deploy.sh` — One-command deployment
- `scripts/index.js` — Production-ready adapter (all fixes applied)
- `references/setup-guide.md` — Step-by-step WeChat Work configuration
- `references/security-guide.md` — Security architecture and hardening

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `signature=undefined` | Using `req.query.signature` | Use `req.query.msg_signature` |
| Signature mismatch | echostr/encrypt not in calculation | Include 4th element in sort array |
| `-30065` error | Returning encrypted echostr | Decrypt before returning |
| `bad decrypt` | Wrong key or `setAutoPadding(true)` | Use `setAutoPadding(false)` + manual PKCS#7 |
| `body长度=undefined` | Body parser doesn't match Content-Type | Accept `*/*` in express.text() |
| `60020` IP error | Server IP not whitelisted | Add public IP in WeChat Work console |
| Timeout | 5s limit exceeded | Use async pattern: return success, send via API |
| Account banned | Unverified + automated messages | Verify enterprise first |
