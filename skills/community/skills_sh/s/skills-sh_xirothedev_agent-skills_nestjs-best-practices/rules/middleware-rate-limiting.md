---
title: Implement Rate Limiting for All Routes
impact: CRITICAL
section: 12
impactDescription: Prevents DDoS and brute force attacks
tags: security, performance, ddos, throttling
---

## Implement Rate Limiting for All Routes

Unlimited requests per IP enable brute force attacks and DDoS. Global rate limiter throttles excessive requests. **Protect every endpoint from abuse.**

**Incorrect (no protection):**

```typescript
// main.ts - Unlimited requests 🚨
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
```

**Correct (rate limited):**

```typescript
// main.ts
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalGuards(new ThrottlerGuard());
  
  await app.listen(3000);
}

// app.module.ts
@Module({
  imports: [
    ThrottlerModule.forRoot([{
      ttl: 60,        // 60 seconds
      limit: 10,      // 10 requests per IP
    }]),
  ],
})
```