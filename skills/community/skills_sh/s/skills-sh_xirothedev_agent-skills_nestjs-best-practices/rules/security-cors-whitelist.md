---
title: Enable CORS with Whitelist Origins Only
impact: CRITICAL
section: 1
impactDescription: Prevents unauthorized domain access
tags: security, cors, production, express
---

## Enable CORS with Whitelist Origins Only

Wildcard CORS (`*`) allows malicious sites to make requests to your API. Explicit origin whitelist prevents cross-site attacks. **Never use wildcard in production.**

**Incorrect (vulnerable CORS):**

```typescript
// main.ts
app.enableCors();  // Uses '*' - dangerous! 🚨
```

**Correct (secure CORS):**

```typescript
// main.ts
app.enableCors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://yourapp.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
});
```