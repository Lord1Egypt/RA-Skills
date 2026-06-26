# Security Guide

## Threat Model

The adapter sits between WeChat Work (internet-facing) and OpenClaw (local-only). Key risks:

1. **Spoofed messages** — Attacker sends fake webhook calls
2. **Data leakage** — Sensitive info exposed in AI replies
3. **Token theft** — Credentials leaked in logs or responses
4. **Replay attacks** — Resubmitting captured requests

## Built-in Protections

### Signature Verification

Every request is verified using `msg_signature`:
- GET: `SHA1(sort([token, timestamp, nonce, echostr]))`
- POST: `SHA1(sort([token, timestamp, nonce, encrypt]))`

Only WeChat Work servers can produce valid signatures.

### AES-256-CBC Encryption

All messages encrypted with EncodingAESKey. Format:
```
16-byte random | 4-byte msg length (BE) | message | CorpID
```

Padding: PKCS#7 (manual, `setAutoPadding(false)`)

### Token Caching

Access tokens cached with 5-minute safety margin to minimize API calls.

## Recommended Hardening

### 1. Response Content Filtering

Add a filter to prevent leaking sensitive data in AI replies:

```javascript
function filterSensitiveContent(text) {
  // Remove anything that looks like a password, key, or token
  return text
    .replace(/[A-Za-z0-9+/=]{32,}/g, '[REDACTED]')
    .replace(/sk-[a-zA-Z0-9-]+/g, '[REDACTED]')
    .replace(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/g, '[REDACTED_IP]');
}
```

### 2. Rate Limiting

```javascript
const rateLimit = {};
const MAX_PER_MINUTE = 10;

function checkRateLimit(userId) {
  const now = Date.now();
  const key = userId;
  if (!rateLimit[key]) rateLimit[key] = [];
  rateLimit[key] = rateLimit[key].filter(t => now - t < 60000);
  if (rateLimit[key].length >= MAX_PER_MINUTE) return false;
  rateLimit[key].push(now);
  return true;
}
```

### 3. Message Deduplication

WeChat Work retries failed messages. Deduplicate by MsgId:

```javascript
const processedMsgs = new Set();

function isDuplicate(msgId) {
  if (processedMsgs.has(msgId)) return true;
  processedMsgs.add(msgId);
  setTimeout(() => processedMsgs.delete(msgId), 300000); // 5min TTL
  return false;
}
```

### 4. Log Sanitization

Never log full tokens or secrets. The adapter already truncates sensitive values.

### 5. Network Isolation

- OpenClaw gateway binds to `localhost:18789` (not exposed)
- Adapter binds to `localhost:8090` (only Cloudflare Tunnel accesses it)
- No direct internet exposure of either service

## Environment Security

- Store `.env` with `chmod 600`
- Never commit `.env` to version control
- Rotate WEBHOOK_TOKEN periodically
- Monitor `logs/wecom-adapter.log` for anomalies
