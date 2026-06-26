# IPLoop API Reference

Base URL: `https://api.iploop.io/api/v1`

All authenticated endpoints require: `Authorization: Bearer <JWT_TOKEN>`

---

## Auth

### POST /auth/register
```bash
curl -X POST https://api.iploop.io/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "Pass123!", "firstName": "John", "lastName": "Doe", "company": "Acme"}'
```
Returns: `{ "user": {...}, "token": "eyJ..." }`

### POST /auth/login
```bash
curl -X POST https://api.iploop.io/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "Pass123!"}'
```
Returns: `{ "token": "eyJ..." }`

---

## Earn (Node Rewards) 💰

### GET /earn/stats
Earning overview — balance, devices, earnings rate.

```json
{
  "totalEarned": 12.50,
  "balance": 8.30,
  "pendingWithdrawal": 0,
  "totalWithdrawn": 4.20,
  "totalDevices": 2,
  "onlineDevices": 1,
  "bandwidthShared": 0,
  "earningRate": 0.10
}
```

### GET /earn/balance
Quick balance check.

```json
{
  "balance": 8.30,
  "totalEarned": 12.50,
  "pending": 0
}
```

### GET /earn/devices
List your registered devices.

```json
{
  "devices": [
    {
      "id": "uuid",
      "name": "My Linux Server",
      "type": "linux",
      "status": "online",
      "country": "US",
      "city": "New York",
      "bandwidthShared": 1073741824,
      "earned": 3.50,
      "lastSeen": "2026-03-10T11:00:00Z"
    }
  ],
  "total": 1
}
```

### POST /earn/devices
Register a new earning device.

```bash
curl -X POST https://api.iploop.io/api/v1/earn/devices \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Server", "deviceType": "linux"}'
```

### DELETE /earn/devices/:id
Remove a device.

### GET /earn/cashout/history
Withdrawal history.

### POST /earn/cashout
Request withdrawal (min $10).

```bash
curl -X POST https://api.iploop.io/api/v1/earn/cashout \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 10, "method": "paypal", "destination": "you@paypal.com"}'
```

---

## Usage & Billing

### GET /usage
Plan info, bandwidth balance, request stats.

```json
{
  "plan": {"name": "Starter", "includedGb": 5, "gbBalance": 5, "gbUsed": 0},
  "stats": {"totalRequests": 0, "successfulRequests": 0}
}
```

### GET /billing
Pricing plans (no auth required).

### GET /dashboard/summary
Full dashboard: user, plan, usage, keys, webhooks.

### GET /api-keys
List your API keys.

---

## Nodes & Network

### GET /nodes
List available proxy nodes (with country/city filters).

### GET /nodes/stats
Network-wide statistics.

### GET /nodes/countries
Available countries with node counts.

---

## Proxy

### GET /proxy/config
Your current proxy configuration.

### Proxy Endpoint
```bash
curl -x "http://iploop:API_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip
```

Options: `country-XX`, `city-NAME`, `session-ID`, `sesstype-sticky`

---

## Gateway Health

```bash
curl https://gateway.iploop.io:9443/health
# → {"connected_nodes": 23000+, "status": "healthy"}
```

---

## Bot Quick Start

```bash
# 1. Register
TOKEN=$(curl -s -X POST https://api.iploop.io/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"bot@example.com","password":"BotPass1!","firstName":"Bot","lastName":"Agent"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# 2. Register earning device
curl -X POST https://api.iploop.io/api/v1/earn/devices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Node","deviceType":"linux"}'

# 3. Check balance
curl -s https://api.iploop.io/api/v1/earn/balance \
  -H "Authorization: Bearer $TOKEN"

# 4. Use proxy
curl -x "http://iploop:API_KEY-country-US@proxy.iploop.io:8880" https://httpbin.org/ip

# 5. Cash out (when balance >= $10)
curl -X POST https://api.iploop.io/api/v1/earn/cashout \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":10,"method":"paypal","destination":"bot@example.com"}'
```
