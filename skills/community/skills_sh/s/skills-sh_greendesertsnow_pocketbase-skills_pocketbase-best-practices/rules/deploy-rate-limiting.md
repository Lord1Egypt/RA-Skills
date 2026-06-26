---
title: Enable Rate Limiting for API Protection
impact: MEDIUM
impactDescription: Prevents abuse, brute-force attacks, and DoS
tags: production, security, rate-limiting, abuse-prevention
---

## Enable Rate Limiting for API Protection

PocketBase v0.23+ includes built-in rate limiting. Enable it to protect against brute-force attacks, API abuse, and excessive resource consumption.

> **v0.36.7 behavioral change:** the built-in limiter switched from a sliding-window to a **fixed-window** strategy. This is cheaper and more predictable, but it means a client can send `2 * maxRequests` in quick succession if they straddle the window boundary. Size your limits with that worst case in mind, and put Nginx/Caddy rate limiting in front of PocketBase for defense in depth (see examples below).

**Incorrect (no rate limiting):**

```bash
# Running without rate limiting
./pocketbase serve

# Vulnerable to:
# - Brute-force password attacks
# - API abuse and scraping
# - DoS from excessive requests
# - Account enumeration attempts
```

**Correct (enable rate limiting):**

```bash
# Enable via command line flag
./pocketbase serve --rateLimiter=true

# Or configure specific limits (requests per second per IP)
./pocketbase serve --rateLimiter=true --rateLimiterRPS=10
```

**Configure via Admin Dashboard:**

Navigate to Settings > Rate Limiter:
- **Enable rate limiter**: Toggle on
- **Max requests/second**: Default 10, adjust based on needs
- **Exempt endpoints**: Optionally whitelist certain paths

**Configure programmatically (Go/JS hooks):**

```javascript
// In pb_hooks/rate_limit.pb.js
routerAdd("GET", "/api/public/*", (e) => {
  // Custom rate limit for specific endpoints
}, $apis.rateLimit(100, "10s")); // 100 requests per 10 seconds

// Stricter limit for auth endpoints
routerAdd("POST", "/api/collections/users/auth-*", (e) => {
  // Auth endpoints need stricter limits
}, $apis.rateLimit(5, "1m")); // 5 attempts per minute
```

**Rate limiting with reverse proxy (additional layer):**

```nginx
# Nginx rate limiting (defense in depth)
http {
    # Define rate limit zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth:10m rate=1r/s;

    server {
        # General API rate limit
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://pocketbase;
        }

        # Strict limit for auth endpoints
        location /api/collections/users/auth {
            limit_req zone=auth burst=5 nodelay;
            proxy_pass http://pocketbase;
        }

        # Stricter limit for superuser auth
        location /api/collections/_superusers/auth {
            limit_req zone=auth burst=3 nodelay;
            proxy_pass http://pocketbase;
        }
    }
}
```

```caddyfile
# Caddy with rate limiting plugin
myapp.com {
    rate_limit {
        zone api {
            key {remote_host}
            events 100
            window 10s
        }
        zone auth {
            key {remote_host}
            events 5
            window 1m
        }
    }

    @auth path /api/collections/*/auth*
    handle @auth {
        rate_limit { zone auth }
        reverse_proxy 127.0.0.1:8090
    }

    handle {
        rate_limit { zone api }
        reverse_proxy 127.0.0.1:8090
    }
}
```

**Handle rate limit errors in client:**

```javascript
async function makeRequest(fn, retries = 0, maxRetries = 3) {
  try {
    return await fn();
  } catch (error) {
    if (error.status === 429 && retries < maxRetries) {
      // Rate limited - wait and retry with limit
      const retryAfter = error.response?.retryAfter || 60;
      console.log(`Rate limited. Retry ${retries + 1}/${maxRetries} after ${retryAfter}s`);

      // Show user-friendly message
      showMessage('Too many requests. Please wait a moment.');

      await sleep(retryAfter * 1000);
      return makeRequest(fn, retries + 1, maxRetries);
    }
    throw error;
  }
}

// Usage
const result = await makeRequest(() =>
  pb.collection('posts').getList(1, 20)
);
```

**Recommended limits by endpoint type:**

| Endpoint Type | Suggested Limit | Reason |
|--------------|-----------------|--------|
| Auth endpoints | 5-10/min | Prevent brute-force |
| Password reset | 3/hour | Prevent enumeration |
| Record creation | 30/min | Prevent spam |
| General API | 60-100/min | Normal usage |
| Public read | 100-200/min | Higher for reads |
| File uploads | 10/min | Resource-intensive |

**Monitoring rate limit hits:**

```javascript
// Check PocketBase logs for rate limit events
// Or set up alerting in your monitoring system

// Client-side tracking
pb.afterSend = function(response, data) {
  if (response.status === 429) {
    trackEvent('rate_limit_hit', {
      endpoint: response.url,
      timestamp: new Date()
    });
  }
  return data;
};
```

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)
