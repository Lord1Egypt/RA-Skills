---
name: rate-limit-validator
description: >
  Test whether an HTTP endpoint enforces rate limiting. Sends a
  burst of requests and checks for 429 responses, Retry-After, and
  X-RateLimit headers. Useful for validating gateway and API
  throttling before going to production.
metadata:
  openclaw:
    requires:
      bins:
        - curl
---
# Rate Limit Validator

Tests whether an HTTP endpoint actually enforces rate limiting.

Most rate-limit skills help you *add* rate limiting. This one helps
you *check* if it's working — or if it's missing entirely.

## What it checks

- Whether the server returns HTTP 429 under burst load
- Presence of `Retry-After` header
- Presence of `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers
- Response time degradation under sustained requests

## When to use it

- Before deploying an API or gateway to production
- After adding rate-limit middleware, to confirm it works
- When auditing a third-party service you depend on
- Validating threat model mitigations (e.g. T-IMPACT-002)

## Example prompts

- "Test if my gateway has rate limiting"
- "Validate rate limiting on http://localhost:18789"
- "Check if my API throttles requests"

## Test script

```bash
#!/bin/bash
TARGET="${1:-http://localhost:18789/}"
COUNT="${2:-50}"
TMP="/tmp/ratelimit-test-$$.txt"

echo "Target: $TARGET"
echo "Requests: $COUNT"
echo ""

for i in $(seq 1 $COUNT); do
  curl -s -o /dev/null -w "%{http_code}" "$TARGET" >> "$TMP"
  echo "" >> "$TMP"
done

TOTAL_200=$(grep -c '200' "$TMP" || echo 0)
TOTAL_429=$(grep -c '429' "$TMP" || echo 0)

echo "Allowed (200): $TOTAL_200"
echo "Throttled (429): $TOTAL_429"
echo ""

HEADERS=$(curl -sI "$TARGET")
echo "$HEADERS" | grep -qi "retry-after" && echo "Retry-After: present" || echo "Retry-After: missing"
echo "$HEADERS" | grep -qi "x-ratelimit" && echo "X-RateLimit: present" || echo "X-RateLimit: missing"

echo ""
if [ "$TOTAL_429" -gt 0 ]; then
  echo "Result: rate limiting is active ($TOTAL_429/$COUNT throttled)"
else
  echo "Result: no rate limiting detected ($TOTAL_200/$COUNT allowed through)"
fi

rm -f "$TMP"
```

## Notes

- Only sends GET requests, no payloads
- Meant for testing your own deployments, not for attacking others
- In OpenClaw's trust model, rate limiting is a hardening measure,
  not a security boundary (authenticated callers are trusted operators)

## References

- [OpenClaw threat model (T-IMPACT-002)](https://github.com/openclaw/trust)
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy)
