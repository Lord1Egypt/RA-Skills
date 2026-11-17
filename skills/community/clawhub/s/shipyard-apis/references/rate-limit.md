# Rate limits and caching with Upstash Redis

Every Shipyard app already has `src/lib/rate-limit.mjs`: an in-memory limiter. It lives in one server instance's memory, so on Vercel (many instances) it is a brake, not a guarantee. Upstash Redis makes the limit shared across instances and adds a cache. Wiring Upstash into a Shipyard app is **new, untested in production**.

## When to add it

- An app route calls a paid API (AI, search, voice) and the app is public.
- Sign-up, password reset or contact forms get abuse.
- The same expensive answer is asked for again and again (cache it).

## Setup

1. The student makes a free Redis database at console.upstash.com (region close to the Vercel region) and pastes `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` with `secrets-init.mjs`. Check with `secrets-check.mjs --live` (one PING).
2. `app-keys.mjs <appDir> UPSTASH_REDIS_REST_URL UPSTASH_REDIS_REST_TOKEN`, then `npm install @upstash/ratelimit @upstash/redis`.
3. `src/lib/limit.ts`: `Redis.fromEnv()` and `new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(20, '1 m'), prefix: '<app-slug>' })`. Key by user id when signed in, else by IP. Answer `429` with `Retry-After`.
4. Keep `rate-limit.mjs` as the fallback when the Upstash variables are missing or Redis is down, so the app never stops working because of the limiter.
5. Cache: `redis.set(key, value, { ex: 3600 })` / `redis.get(key)` with keys made from a hash of the input; never cache answers that contain one user's private data under a shared key.

Free plan limits change; check the Upstash pricing page and tell the student roughly how many requests a day the app can make before paying.
