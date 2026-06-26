---
title: Use Send Hooks for Request Customization
impact: MEDIUM
impactDescription: Custom headers, logging, response transformation
tags: sdk, hooks, middleware, headers, logging
---

## Use Send Hooks for Request Customization

The SDK provides `beforeSend` and `afterSend` hooks for intercepting and modifying requests and responses globally.

**Incorrect (repeating logic in every request):**

```javascript
// Adding headers to every request manually
const posts = await pb.collection('posts').getList(1, 20, {
  headers: { 'X-Custom-Header': 'value' }
});

const users = await pb.collection('users').getList(1, 20, {
  headers: { 'X-Custom-Header': 'value' }  // Repeated!
});

// Logging each request manually
console.log('Fetching posts...');
const posts = await pb.collection('posts').getList();
console.log('Done');
```

**Correct (using send hooks):**

```javascript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://127.0.0.1:8090');

// beforeSend - modify requests before they're sent
pb.beforeSend = function(url, options) {
  // Add custom headers to all requests
  options.headers = Object.assign({}, options.headers, {
    'X-Custom-Header': 'value',
    'X-Request-ID': crypto.randomUUID()
  });

  // Log outgoing requests
  console.log(`[${options.method}] ${url}`);

  // Must return { url, options }
  return { url, options };
};

// afterSend - process responses
pb.afterSend = function(response, data) {
  // Log response status
  console.log(`Response: ${response.status}`);

  // Transform or extend response data
  if (data && typeof data === 'object') {
    data._fetchedAt = new Date().toISOString();
  }

  // Return the (possibly modified) data
  return data;
};

// All requests now automatically have headers and logging
const posts = await pb.collection('posts').getList();
const users = await pb.collection('users').getList();
```

**Practical examples:**

```javascript
// Request timing / performance monitoring
let requestStart;
pb.beforeSend = function(url, options) {
  requestStart = performance.now();
  return { url, options };
};

pb.afterSend = function(response, data) {
  const duration = performance.now() - requestStart;
  console.log(`${response.url}: ${duration.toFixed(2)}ms`);

  // Send to analytics
  trackApiPerformance(response.url, duration);

  return data;
};

// Add auth token from different source
pb.beforeSend = function(url, options) {
  const externalToken = getTokenFromExternalAuth();
  if (externalToken) {
    options.headers = Object.assign({}, options.headers, {
      'X-External-Auth': externalToken
    });
  }
  return { url, options };
};

// Handle specific response codes globally
pb.afterSend = function(response, data) {
  if (response.status === 401) {
    // Token expired - trigger re-auth
    handleAuthExpired();
  }

  if (response.status === 503) {
    // Service unavailable - show maintenance message
    showMaintenanceMode();
  }

  return data;
};

// Retry failed requests (simplified example)
const originalSend = pb.send.bind(pb);
pb.send = async function(path, options) {
  try {
    return await originalSend(path, options);
  } catch (error) {
    if (error.status === 429) {  // Rate limited
      await sleep(1000);
      return originalSend(path, options);  // Retry once
    }
    throw error;
  }
};

// Add request correlation for debugging
let requestId = 0;
pb.beforeSend = function(url, options) {
  requestId++;
  const correlationId = `req-${Date.now()}-${requestId}`;

  options.headers = Object.assign({}, options.headers, {
    'X-Correlation-ID': correlationId
  });

  console.log(`[${correlationId}] Starting: ${url}`);
  return { url, options };
};

pb.afterSend = function(response, data) {
  console.log(`Complete: ${response.status}`);
  return data;
};
```

**Hook signatures:**

```typescript
// beforeSend
beforeSend?: (
  url: string,
  options: SendOptions
) => { url: string; options: SendOptions } | Promise<{ url: string; options: SendOptions }>;

// afterSend
afterSend?: (
  response: Response,
  data: any
) => any | Promise<any>;
```

**Use cases:**
- Add custom headers (API keys, correlation IDs)
- Request/response logging
- Performance monitoring
- Global error handling
- Response transformation
- Authentication middleware

Reference: [PocketBase Send Hooks](https://github.com/pocketbase/js-sdk#send-hooks)
