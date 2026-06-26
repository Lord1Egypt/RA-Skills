---
title: Cache Frequently Used Data with Redis
impact: HIGH
section: 2
impactDescription: Dramatically reduces database load and improves response times
tags: performance, caching, redis, scalability
---

## Cache Frequently Used Data with Redis

Every database query increases latency and costs. Redis caching stores hot data in memory for sub-millisecond access. **Cache read-heavy endpoints and expensive computations.**

**Incorrect (database every request):**

```typescript
// users.service.ts - DB hit every time 🚨
async getUserProfile(id: string) {
  return this.prisma.user.findUnique({
    where: { id },
    include: { posts: true, followers: true }
  });
}
```

**Correct (Redis cached):**

```typescript
// cache.service.ts
@Injectable()
export class CacheService {
  constructor(private redis: Redis) {}
  
  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }
  
  async set(key: string, data: any, ttl = 300) {
    await this.redis.setex(key, ttl, JSON.stringify(data));
  }
}

// users.service.ts
async getUserProfile(id: string) {
  const cacheKey = `user:${id}:profile`;
  let profile = await this.cacheService.get(cacheKey);
  
  if (!profile) {
    profile = await this.prisma.user.findUnique({
      where: { id },
      include: { posts: true, followers: true }
    });
    await this.cacheService.set(cacheKey, profile, 300);  // 5min ✅
  }
  
  return profile;
}
```