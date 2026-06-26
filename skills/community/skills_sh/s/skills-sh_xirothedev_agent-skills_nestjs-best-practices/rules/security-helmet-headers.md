---
title: Use Helmet Middleware for Security Headers
impact: CRITICAL
impactDescription: Protects against XSS, clickjacking, and other web attacks
section: 1
tags: security, express, helmet, production
---

## Use Helmet Middleware for Security Headers

NestJS with Express adapter exposes HTTP headers that can be exploited by attackers. Helmet automatically sets security headers like X-XSS-Protection, X-Frame-Options, and Content-Security-Policy. **Always enable it in production.**

> **Hint**: Apply `helmet` as global middleware **before** other calls to `app.use()` or route definitions. Middleware order matters - routes defined before helmet will not have security headers applied.

### Installation

**Express (default adapter):**
```bash
bun add helmet
```

**Fastify adapter:**
```bash
bun add @fastify/helmet
```

### Usage

**Incorrect (vulnerable headers):**

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Define routes before helmet - insecure!
  app.route('/api', ...);

  app.use(helmet());
  await app.listen(3000);
}
```

**Correct (Express):**

```typescript
// main.ts
import helmet from 'helmet';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply helmet FIRST, before routes and other middleware
  app.use(helmet());

  // Now define routes
  app.route('/api', ...);

  await app.listen(3000);
}
```

**Correct (Fastify):**

```typescript
// main.ts
import helmet from '@fastify/helmet';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Fastify uses register() instead of use()
  await app.register(helmet);

  await app.listen(3000);
}
```

### Apollo/GraphQL CSP Configuration

When using `@apollo/server` (4.x) with Apollo Sandbox, default CSP may cause issues. Configure as follows:

**Express with Apollo:**
```typescript
app.use(helmet({
  crossOriginEmbedderPolicy: false,
  contentSecurityPolicy: {
    directives: {
      imgSrc: [`'self'`, 'data:', 'apollo-server-landing-page.cdn.apollographql.com'],
      scriptSrc: [`'self'`, `https: 'unsafe-inline'`],
      manifestSrc: [`'self'`, 'apollo-server-landing-page.cdn.apollographql.com'],
      frameSrc: [`'self'`, 'sandbox.embed.apollographql.com'],
    },
  },
}));
```

**Fastify with Apollo:**
```typescript
await app.register(helmet, {
  contentSecurityPolicy: {
    directives: {
      defaultSrc: [`'self'`, 'unpkg.com'],
      styleSrc: [
        `'self'`,
        `'unsafe-inline'`,
        'cdn.jsdelivr.net',
        'fonts.googleapis.com',
        'unpkg.com',
      ],
      fontSrc: [`'self'`, 'fonts.gstatic.com', 'data:'],
      imgSrc: [`'self'`, 'data:', 'cdn.jsdelivr.net'],
      scriptSrc: [
        `'self'`,
        `https: 'unsafe-inline'`,
        'cdn.jsdelivr.net',
        `'unsafe-eval'`,
      ],
    },
  },
});

// Or disable CSP entirely if not needed:
await app.register(helmet, {
  contentSecurityPolicy: false,
});
```

Reference: [Helmet NestJS Documentation](https://docs.nestjs.com/security/helmet)
