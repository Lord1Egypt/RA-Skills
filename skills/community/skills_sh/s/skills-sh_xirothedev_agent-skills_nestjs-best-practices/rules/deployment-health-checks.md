---
title: Implement Health Check Endpoints
impact: HIGH
section: 11
impactDescription: Enables monitoring and automatic restarts
tags: monitoring, health, production, reliability
---

## Implement Health Check Endpoints

No health checks prevent container orchestrators from detecting failures. Dedicated endpoints verify database, cache, and service connectivity. **Production apps must expose health status.**

**Incorrect (no monitoring):**

```typescript
// No health endpoint - can't detect failures 🚨
```

**Correct (comprehensive health checks):**

```typescript
// health.controller.ts
@Controller('health')
export class HealthController {
  constructor(
    @Inject(PrismaService) private prisma: PrismaService,
    @Inject(CacheService) private cache: CacheService,
  ) {}

  @Get()
  async checkHealth() {
    // Database check
    await this.prisma.$queryRaw`SELECT 1`;
    
    // Cache check
    await this.cache.get('health-check');
    
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: { database: 'ok', cache: 'ok' }
    };
  }
}

// main.ts
app.setGlobalPrefix('api');
app.use('/api/health', healthRouter);
```