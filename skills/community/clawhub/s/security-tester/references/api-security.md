# API Security Testing

Reference: OWASP API Security Top 10 (2023) - https://owasp.org/API-Security/

## OWASP API Security Top 10 (2023)

| # | Risk | Test Focus |
|---|------|-----------|
| API1 | Broken Object Level Authorization | IDOR on every endpoint |
| API2 | Broken Authentication | Token handling, session management |
| API3 | Broken Object Property Level Authorization | Mass assignment, excessive data exposure |
| API4 | Unrestricted Resource Consumption | Rate limiting, pagination limits |
| API5 | Broken Function Level Authorization | Admin endpoints with user tokens |
| API6 | Unrestricted Access to Sensitive Business Flows | Bot abuse, business logic bypass |
| API7 | Server Side Request Forgery | URL parameters, webhook URLs |
| API8 | Security Misconfiguration | CORS, error handling, TLS |
| API9 | Improper Inventory Management | Shadow APIs, deprecated endpoints |
| API10 | Unsafe Consumption of APIs | Third-party API trust, validation |

## API3: Mass Assignment Testing

```bash
# Try adding extra fields in request
curl -X PUT "$URL/api/users/me" \
  -H "Content-Type: application/json" \
  -d '{"name":"test", "role":"admin", "isVerified":true, "balance":999999}'
# Verify: role, isVerified, balance should NOT be changed
```

## API4: Rate Limiting & Resource Consumption

```bash
# Test missing pagination limits
curl "$URL/api/items?page=1&per_page=999999"
# Should enforce max per_page

# Test missing rate limits
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code}\n" "$URL/api/expensive-endpoint"
done | sort | uniq -c
# Should see 429 responses

# Test large payload
python3 -c "print('{\"data\":\"' + 'A'*10000000 + '\"}')" | \
  curl -X POST -d @- -H "Content-Type: application/json" "$URL/api/upload"
# Should return 413 Payload Too Large
```

## API7: SSRF Testing

```bash
# Test URL parameters for SSRF
SSRF_PAYLOADS=(
  "http://127.0.0.1:80"
  "http://localhost:22"
  "http://169.254.169.254/latest/meta-data/"  # AWS metadata
  "http://[::1]:80"
  "http://0x7f000001"
)

for payload in "${SSRF_PAYLOADS[@]}"; do
  echo "Testing: $payload"
  curl -s -o /dev/null -w "%{http_code} %{time_total}s" \
    "$URL/api/fetch?url=$payload"
  echo
done
```

## JWT Security Testing

```bash
# Decode JWT (without verification)
echo "$JWT" | python3 -c "
import sys, base64, json
token = sys.stdin.read().strip()
parts = token.split('.')
header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
print('Header:', json.dumps(header, indent=2))
print('Payload:', json.dumps(payload, indent=2))
"

# Test: alg=none attack
# 1. Change header to {"alg":"none","typ":"JWT"}
# 2. Remove signature
# 3. Send modified token

# Test: weak secret
# Use tools like jwt-cracker or hashcat against HS256 tokens

# Check: token expiry
# Verify exp claim is present and reasonable (not 10 years)
# Verify token is rejected after expiry
```

## GraphQL Security

```bash
# Introspection query (should be disabled in production)
curl -X POST "$URL/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name fields { name } } } }"}'

# Batch query attack (DoS)
curl -X POST "$URL/graphql" \
  -H "Content-Type: application/json" \
  -d '[{"query":"{ users { id name } }"},{"query":"{ users { id name } }"},...]'

# Nested query attack (resource exhaustion)
# { user { friends { friends { friends { ... } } } } }
```
