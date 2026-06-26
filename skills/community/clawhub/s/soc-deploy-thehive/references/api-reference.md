# API Reference: TheHive + Cortex

## TheHive (port 9000)

### Authentication
```bash
# Login (returns THEHIVE-SESSION cookie)
curl -s -D - -X POST http://<host>:9000/api/v1/login \
  -H 'Content-Type: application/json' \
  -d '{"user":"admin@thehive.local","password":"secret"}'

# With API key (preferred for automation)
curl -s http://<host>:9000/api/v1/user/current \
  -H 'Authorization: Bearer <API_KEY>'
```

### Password Management
```bash
# Change password (CORRECT endpoint)
printf '{"currentPassword":"old","password":"new"}' | \
curl -s -X POST "http://<host>:9000/api/v1/user/<login>/password/change" \
  -H "Cookie: THEHIVE-SESSION=<session>" \
  -H 'Content-Type: application/json' -d @-
```

### API Key
```bash
# Generate/renew API key
curl -s -X POST "http://<host>:9000/api/v1/user/<login>/key/renew" \
  -H "Cookie: THEHIVE-SESSION=<session>"
# Returns plain text key
```

### Status
```bash
curl -s http://<host>:9000/api/status
```

## Cortex (port 9001)

### First-Time Setup
```bash
# DB migration (idempotent)
curl -s -X POST http://<host>:9001/api/maintenance/migrate \
  -H 'Content-Type: application/json'

# Create superadmin (NO AUTH, only works when zero users)
printf '{"login":"admin","name":"Admin","password":"pass","roles":["superadmin"]}' | \
curl -s -X POST http://<host>:9001/api/user \
  -H 'Content-Type: application/json' -d @-
```

### Authentication
```bash
# Login (returns CORTEX_SESSION cookie)
printf '{"user":"admin","password":"pass"}' | \
curl -s -D - -X POST http://<host>:9001/api/login \
  -H 'Content-Type: application/json' -d @-

# Get CSRF token (make GET with session, capture CORTEX-XSRF-TOKEN cookie)
curl -s -D - http://<host>:9001/api/user/admin \
  -H "Cookie: CORTEX_SESSION=<session>"
```

### Organization Management (all need CSRF)
```bash
# Create org
curl -s -X POST http://<host>:9001/api/organization \
  -H "Cookie: CORTEX_SESSION=<s>; CORTEX-XSRF-TOKEN=<csrf>" \
  -H "X-CORTEX-XSRF-TOKEN: <csrf>" \
  -H 'Content-Type: application/json' \
  -d '{"name":"SOC","description":"SOC org","status":"Active"}'

# Create org admin
printf '{"name":"Admin","roles":["read","analyze","orgadmin"],"organization":"SOC","login":"soc-admin"}' | \
curl -s -X POST http://<host>:9001/api/user \
  -H "Cookie: CORTEX_SESSION=<s>; CORTEX-XSRF-TOKEN=<csrf>" \
  -H "X-CORTEX-XSRF-TOKEN: <csrf>" \
  -H 'Content-Type: application/json' -d @-
```

### API Keys (need CSRF)
```bash
curl -s -X POST http://<host>:9001/api/user/<login>/key/renew \
  -H "Cookie: CORTEX_SESSION=<s>; CORTEX-XSRF-TOKEN=<csrf>" \
  -H "X-CORTEX-XSRF-TOKEN: <csrf>"
# Returns plain text key
```

### Status
```bash
curl -s http://<host>:9001/api/status
```
