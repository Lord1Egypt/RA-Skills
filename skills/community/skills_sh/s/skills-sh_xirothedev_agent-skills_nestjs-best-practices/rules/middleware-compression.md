---
title: Enable Compression Middleware for Responses
impact: HIGH
section: 12
impactDescription: Reduces bandwidth usage and improves performance
tags: performance, compression, express, gzip
---

## Enable Compression Middleware for Responses

Uncompressed responses waste bandwidth and slow down page loads. Compression middleware (gzip/brotli) reduces response size by 70-90%. **Always enable compression in production.**

**Incorrect (no compression):**

```typescript
// main.ts - Large responses 🚨
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
```

**Correct (compressed responses):**

```typescript
// main.ts
import * as compression from 'compression';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(compression());  // Gzip/brotli compression ✅
  await app.listen(3000);
}
```

Reference: [Nestjs Compression Document](https://docs.nestjs.com/techniques/compression)