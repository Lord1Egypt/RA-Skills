# IPLoop Support API

Everything a bot needs to self-service: diagnose issues, check status, get help.

Base URL: `https://api.iploop.io/api/v1`

---

## 1. System Status

### Gateway Health (no auth)
```bash
curl -s https://gateway.iploop.io:9443/health
```
```json
{
  "status": "healthy",
  "connected_nodes": 9,600+,
  "device_types": {"android": 8100, "windows": 1500},
  "service": "node-registration"
}
```

### Network Stats (no auth)
```bash
curl -s https://gateway.iploop.io:9443/stats
```
```json
{
  "total_nodes": 9,600+,
  "active_nodes": 9,600+,
  "device_types": {"android": 8100, "windows": 1500},
  "total_bandwidth_mb": 0
}
```

### Customer API Health (no auth)
```bash
curl -s https://api.iploop.io/api/v1/health
```

---

## 2. Account Diagnostics (auth required)

### Check Your Plan & Usage
```bash
curl -s https://api.iploop.io/api/v1/usage -H "Authorization: Bearer $TOKEN"
```
```json
{
  "plan": {"name": "Starter", "includedGb": 5, "gbBalance": 5, "gbUsed": 0},
  "stats": {"totalRequests": 0, "successfulRequests": 0}
}
```

### Full Dashboard Summary
```bash
curl -s https://api.iploop.io/api/v1/dashboard/summary -H "Authorization: Bearer $TOKEN"
```
```json
{
  "user": {"firstName": "John", "email": "john@example.com", "role": "customer"},
  "plan": {"name": "Starter", "includedGb": 5},
  "usage": {"requests": 0, "gb": "0.00", "successRate": "100.0"},
  "activeKeys": 1,
  "activeWebhooks": 0
}
```

### List API Keys
```bash
curl -s https://api.iploop.io/api/v1/api-keys -H "Authorization: Bearer $TOKEN"
```

---

## 3. Proxy Diagnostics

### Quick Proxy Test
```bash
curl -x "http://iploop:YOUR_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip
# → {"origin": "71.204.49.146"}  (real residential IP)
```

### Check Your Proxy Config
```bash
curl -s https://api.iploop.io/api/v1/proxy/config -H "Authorization: Bearer $TOKEN"
```

### Available Countries
```bash
curl -s https://api.iploop.io/api/v1/nodes/countries -H "Authorization: Bearer $TOKEN"
```

### IP Check
```bash
curl -s https://iploop.io/ip
# → {"ip": "your.ip.here", "timestamp": "..."}
```

### IP + Geolocation
```bash
curl -s https://iploop.io/location
# → {"ip": "...", "location": {"country": "US", "city": "New York", ...}}
```

---

## 4. Earnings & Rewards

### Check Balance
```bash
curl -s https://api.iploop.io/api/v1/earn/balance -H "Authorization: Bearer $TOKEN"
```
```json
{"balance": 8.30, "totalEarned": 12.50, "pending": 0}
```

### Earning Stats
```bash
curl -s https://api.iploop.io/api/v1/earn/stats -H "Authorization: Bearer $TOKEN"
```
```json
{
  "totalEarned": 12.50,
  "balance": 8.30,
  "totalDevices": 2,
  "onlineDevices": 1,
  "earningRate": 0.10
}
```

### List Devices
```bash
curl -s https://api.iploop.io/api/v1/earn/devices -H "Authorization: Bearer $TOKEN"
```

### Register Device
```bash
curl -X POST https://api.iploop.io/api/v1/earn/devices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Server", "deviceType": "linux"}'
```

### Cash Out (min $10)
```bash
curl -X POST https://api.iploop.io/api/v1/earn/cashout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "method": "paypal", "destination": "you@paypal.com"}'
```

---

## 5. Pricing (no auth)
```bash
curl -s https://api.iploop.io/api/v1/billing
```
Returns all plans: Starter ($4.99/GB), Professional ($3.99/GB), Business ($2.99/GB), Enterprise.

---

## 6. Common Error Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 407 | Invalid API key | Check key format: `iploop:YOUR_KEY@proxy.iploop.io:8880` |
| 403 | Site blocked | Enable stealth: `IPLoop(api_key=KEY, stealth=True)` |
| 429 | Rate limited | Slow down or upgrade plan |
| Timeout | Slow proxy | Try different country: `-country-US` |
| Empty response | Anti-bot | Use Python SDK with `stealth=True` |

---

## 7. Bot Quick Start

```bash
# 1. Register
TOKEN=$(curl -s -X POST https://api.iploop.io/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"bot@example.com","password":"Pass123!","firstName":"Bot","lastName":"Agent"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# 2. Check status
curl -s https://gateway.iploop.io:9443/health

# 3. Test proxy
curl -x "http://iploop:YOUR_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip

# 4. Check usage
curl -s https://api.iploop.io/api/v1/usage -H "Authorization: Bearer $TOKEN"

# 5. Start earning
curl -X POST https://api.iploop.io/api/v1/earn/devices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Node","deviceType":"linux"}'

# 6. Monitor balance
curl -s https://api.iploop.io/api/v1/earn/balance -H "Authorization: Bearer $TOKEN"
```

---

## Support Contacts
- Email: partners@iploop.io
- Website: https://iploop.io/contact.html
- Docs: https://proxyclaw.ai/docs.html
