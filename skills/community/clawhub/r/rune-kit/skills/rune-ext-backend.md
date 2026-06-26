# rune-ext-backend

> Rune L4 Skill | extension


# @rune/backend

> **RUNE COMPLIANCE**: Before ANY code response, you MUST:
> 1. Classify this request (CODE_CHANGE | QUESTION | DEBUG | REVIEW | EXPLORE)
> 2. Route through the correct Rune skill (see skill-router routing table)
> 3. Follow the skill's workflow — do NOT freelance or skip steps
> Violation: writing code without skill routing = incorrect behavior.

## Platform Constraints

- SHOULD: Monitor your context usage. If working on a long task, summarize progress before context fills up.
- MUST: Before summarizing/compacting context, save important decisions and progress to project files.
- SHOULD: Before ending, save architectural decisions and progress to .rune/ directory for future sessions.

## Purpose

Backend codebases accumulate structural debt across six areas: inconsistent API contracts (mixed naming, missing pagination, vague errors), insecure auth flows (token mismanagement, missing refresh rotation, weak RBAC), database anti-patterns (N+1 queries, missing indexes, unsafe migrations), ad-hoc middleware (duplicated validation, no request tracing, inconsistent error format), missing or naive caching (no invalidation strategy, cache stampede risk, unbounded memory growth), and synchronous processing of inherently async work (blocking request threads on email, PDF, image tasks). This pack addresses each systematically — detect the anti-pattern, emit the fix, verify the result. Skills are independent but compound: clean APIs need solid auth, solid auth needs safe queries, safe queries need proper middleware, and high-traffic APIs need caching and background jobs to stay responsive.

## Triggers

- Auto-trigger: when `routes/`, `controllers/`, `middleware/`, `*.resolver.ts`, `*.service.ts`, `queues/`, `workers/`, or server framework config detected
- `/rune api-patterns` — audit and fix API design
- `/rune auth-patterns` — audit and fix authentication flows
- `/rune database-patterns` — audit and fix database queries and schema
- `/rune middleware-patterns` — audit and fix middleware stack
- `/rune caching-patterns` — audit and implement caching strategy
- `/rune background-jobs` — identify async operations and implement job queues
- `/rune cli-generation` — generate production CLI for existing backend services
- `/rune async-pipeline` — build multi-stage async processing pipelines with waterfall fallback
- Called by `cook` (L1) when backend task is detected
- Called by `review` (L2) when API/backend code is under review

## Skills Included

| Skill | Model | Description |
|-------|-------|-------------|
| [api-patterns](skills/api-patterns.md) | sonnet | RESTful and GraphQL API design patterns — resource naming, pagination, filtering, error responses, versioning, rate limiting, OpenAPI generation. |
| [auth-patterns](skills/auth-patterns.md) | sonnet | Authentication and authorization patterns — JWT, OAuth 2.0 / OIDC, passkeys/WebAuthn, session management, RBAC, API key management, MFA flows. |
| [database-patterns](skills/database-patterns.md) | sonnet | Database design and query patterns — schema design, migrations, indexing strategies, N+1 prevention, soft deletes, read replicas, connection pooling, seeding. |
| [middleware-patterns](skills/middleware-patterns.md) | sonnet | Middleware architecture — request validation, error handling, logging, CORS, compression, graceful shutdown, health checks, request ID tracking. |
| [caching-patterns](skills/caching-patterns.md) | sonnet | Caching strategies — in-memory LRU, Redis distributed cache, CDN/edge cache, browser cache headers, invalidation, and stampede prevention. |
| [background-jobs](skills/background-jobs.md) | sonnet | Queue-based async processing — BullMQ (Node.js), job patterns, retry strategies, idempotency, dead letter queues, monitoring. |
| [cli-generation](skills/cli-generation.md) | sonnet | Generate production-grade CLI wrappers — command groups, dual output mode (human + JSON), stateful REPL, session management with undo/redo, installable packaging. |
| [async-pipeline](skills/async-pipeline.md) | sonnet | Multi-stage async processing pipelines with waterfall engine selection, progress streaming via SSE, concurrency control, and credit-based billing. |

## Tech Stack Support

| Framework | ORM | Auth Library | Queue | Cache |
|-----------|-----|-------------|-------|-------|
| Express 5 | Prisma | Passport / custom JWT | BullMQ | ioredis |
| Fastify 5 | Drizzle | @fastify/jwt | BullMQ | ioredis |
| Next.js 16 (Route Handlers) | Prisma | NextAuth v5 / Lucia | BullMQ | ioredis / Upstash |
| NestJS 11 | TypeORM / Prisma | @nestjs/passport | @nestjs/bull | @nestjs/cache-manager |
| FastAPI | SQLAlchemy | python-jose / authlib | Celery | redis-py |
| Django 5 | Django ORM | django-rest-framework | Celery | django-redis |

## Connections

```
Calls → docs-seeker (L3): lookup API documentation and framework guides
Calls → sentinel (L2): security audit on auth implementations
Calls → watchdog (L3): monitor queue depth and cache hit ratios
Calls → @rune/devops (L4): container and serverless deployment config for backend services
Called By ← cook (L1): when backend task detected
Called By ← review (L2): when API/backend code is being reviewed
Called By ← audit (L2): backend health dimension
Called By ← deploy (L2): pre-deploy readiness checks (health endpoints, graceful shutdown)
Called By ← @rune/saas (L4): SaaS services use backend API, auth, and caching patterns
Called By ← @rune/security (L4): security audits reference auth flows and middleware patterns
Called By ← @rune/mobile (L4): mobile backend integration patterns (auth, push server)
Inter-skill: cli-generation → api-patterns (CLI wraps existing API surface)
Inter-skill: async-pipeline → background-jobs (pipeline stages use job queue for execution)
Inter-skill: async-pipeline → caching-patterns (pipeline results cached by content hash)
```

## Sharp Edges

- **Auth**: Never emit JWT without expiry; hard-cap access tokens at 15min, refresh at 7d.
- **Cache stampede**: Always emit Redis `SET NX` mutex lock on cache miss for hot keys.
- **Job idempotency**: Never use random UUID as job ID — use deterministic domain key (e.g., `email:welcome:${userId}`).
- **N+1**: Check ORM `lazy: true` defaults (Sequelize, TypeORM) — not caught by loop scan alone.
- **Migrations**: Every migration MUST include both `up()` and `down()` — flag any missing rollback.
- **LRU**: Always set `max` entries AND `ttl` — unbounded LRU grows to OOM.
- **CORS**: Flag `origin: '*'` in production configs; check `NODE_ENV` before emitting.
- **SSE**: Send heartbeat comment every 30s (`:\n\n`) to prevent proxy/LB 60s timeout drops.
- **Dead letters**: Emit alert on DLQ depth > 0 for critical queues; never silently drop failed jobs.
- **Credit math**: Always `Math.ceil()` final cost; use integer cents internally to avoid float drift.

## Done When

- API audit report emitted with naming violations, missing pagination, versioning strategy, and fix diffs
- Auth flow hardened: short-lived access tokens, httpOnly refresh cookies, proper hashing, OAuth/OIDC integration ready
- N+1 queries detected and replaced with eager loading; soft delete pattern applied; missing indexes migrated
- Middleware stack has: request ID, structured logging, global error handler, input validation, compression, graceful shutdown, health endpoints
- Caching strategy implemented: cacheable endpoints identified, cache layer selected, invalidation logic emitted alongside every write
- Async operations moved to background jobs: idempotency keys assigned, retry strategy configured, dead letter queue wired
- All emitted code uses project's existing framework and ORM (detected from package.json)
- CLI generated with dual output (human + JSON), REPL mode, session undo/redo, and installable package
- Async pipeline has waterfall engine selection, progress streaming via SSE, concurrency control, and credit billing
- Structured report emitted for each skill invoked

## Cost Profile

~14,000–28,000 tokens per full pack run (all 8 skills). Individual skill: ~2,000–5,000 tokens. Sonnet default for code generation and security audit. Use haiku for detection scans (Step 1 of each skill). Escalate to opus for architecture decisions on caching topology, pipeline design, or queue system selection in high-traffic systems.

# api-patterns

RESTful and GraphQL API design patterns — resource naming, pagination, filtering, error responses, versioning, rate limiting, OpenAPI generation.

#### Workflow

**Step 1 — Detect API surface**
Use Grep to find route definitions (`app.get`, `app.post`, `router.`, `@Get()`, `@Post()`, `@Query`, `@Mutation`). Read each route file to inventory: endpoint paths, HTTP methods, response shapes, error handling approach.

**Step 2 — Audit naming and structure**
Check each endpoint against REST conventions: plural nouns for collections (`/users` not `/getUsers`), nested resources for relationships (`/users/:id/posts`), query params for filtering (`?status=active`), consistent error envelope. Flag violations with specific fix for each.

**Step 3 — Add missing pagination and filtering**
For list endpoints returning unbounded arrays, emit cursor-based or offset pagination. For endpoints with no filtering, add query param parsing with Zod/Joi validation. Emit the middleware or decorator that enforces the pattern.

**Step 4 — API versioning strategy**
Choose versioning approach based on project context: URL path (`/v2/users`) for public APIs with long deprecation windows; `Accept-Version: 2` header for internal APIs needing cleaner URLs; query param (`?version=2`) for simple cases. Emit version routing middleware and a deprecation warning header (`Deprecation: true, Sunset: <date>`) on v1 routes. Document migration path in the route file as a comment.

**Step 5 — OpenAPI/Swagger and GraphQL patterns**
For REST: emit OpenAPI 3.1 schema from route definitions using tsoa decorators (TypeScript), Fastify's built-in JSON Schema (`schema: { body, querystring, response }`), or NestJS `@ApiProperty`. For GraphQL: if schema-first, validate resolvers match schema types; if code-first (NestJS), check `@ObjectType` / `@Field` decorators. Add DataLoader to any resolver with a per-request DB call to prevent N+1 at the GraphQL layer. Emit subscription pattern (WebSocket transport) for real-time fields.

#### Example

```typescript
// BEFORE: inconsistent naming, no pagination, bare error
app.get('/getUsers', async (req, res) => {
  const users = await db.query('SELECT * FROM users');
  res.json(users);
});

// AFTER: REST naming, cursor pagination, error envelope, Zod validation
const paginationSchema = z.object({
  query: z.object({
    cursor: z.string().optional(),
    limit: z.coerce.number().int().min(1).max(100).default(20),
    status: z.enum(['active', 'inactive']).optional(),
  }),
});

app.get('/users', validate(paginationSchema), async (req, res) => {
  const { cursor, limit, status } = req.query;
  const users = await userRepo.findMany({ cursor, limit: limit + 1, status });
  const hasNext = users.length > limit;
  res.json({
    data: users.slice(0, limit),
    pagination: { next_cursor: hasNext ? users[limit - 1].id : null, has_more: hasNext },
  });
});

// Rate limiting: sliding window with Redis (atomic, no race condition)
const rateLimitMiddleware = async (req, res, next) => {
  const key = `rl:${req.ip}:${Math.floor(Date.now() / 60_000)}`; // 1-minute window
  const multi = redis.multi();
  multi.incr(key);
  multi.expire(key, 60);
  const [count] = await multi.exec();
  if (count > 100) return res.status(429).json({ error: { code: 'RATE_LIMITED', message: 'Too many requests' } });
  res.setHeader('X-RateLimit-Remaining', 100 - count);
  next();
};

// Fastify: built-in schema validation + OpenAPI generation
fastify.get('/users/:id', {
  schema: {
    params: { type: 'object', properties: { id: { type: 'string', format: 'uuid' } }, required: ['id'] },
    response: { 200: UserSchema, 404: ErrorSchema },
  },
}, async (req, reply) => { /* handler */ });

// GraphQL: DataLoader prevents N+1 in resolvers
const userLoader = new DataLoader(async (userIds: string[]) => {
  const users = await prisma.user.findMany({ where: { id: { in: userIds } } });
  return userIds.map(id => users.find(u => u.id === id) ?? new Error(`User ${id} not found`));
});
// In resolver: return userLoader.load(post.authorId) — batches all loads per request
```

---

# async-pipeline

Multi-stage async processing pipelines with waterfall engine selection, progress streaming, and credit-based billing. Patterns for building services that process data through multiple fallback strategies with real-time status updates.

#### Workflow

**Step 1 — Design engine waterfall**
Multiple processing engines ranked by quality and cost:
```typescript
interface ProcessingEngine {
  name: string;
  quality: number;       // higher = preferred
  costMultiplier: number; // credit cost factor
  execute: (input: Input) => Promise<Result>;
  canHandle: (input: Input) => boolean;
}

// Engines race with staggered delays — first valid result wins
async function waterfallExecute(
  engines: ProcessingEngine[],
  input: Input,
  staggerDelayMs: number = 500
): Promise<{ result: Result; engine: string }> {
  const sorted = engines
    .filter(e => e.canHandle(input))
    .sort((a, b) => b.quality - a.quality);

  const controller = new AbortController();

  const races = sorted.map((engine, i) =>
    new Promise<{ result: Result; engine: string }>(async (resolve, reject) => {
      // Stagger start: engine 0 starts immediately, engine 1 after 500ms, etc.
      if (i > 0) await delay(i * staggerDelayMs);
      if (controller.signal.aborted) return reject(new Error('aborted'));

      try {
        const result = await engine.execute(input);
        if (isValid(result)) {
          controller.abort();  // cancel slower engines
          resolve({ result, engine: engine.name });
        } else {
          reject(new Error(`${engine.name}: invalid result`));
        }
      } catch (err) {
        reject(err);
      }
    })
  );

  return Promise.any(races);
}
```

**Step 2 — Implement transform pipeline**
Chain transforms that process data sequentially:
```typescript
type Transformer<T> = (data: T, context: PipelineContext) => Promise<T>;

async function runPipeline<T>(
  data: T,
  transformers: Transformer<T>[],
  onProgress: (stage: string, pct: number) => void
): Promise<T> {
  let current = data;
  for (let i = 0; i < transformers.length; i++) {
    onProgress(transformers[i].name, (i / transformers.length) * 100);
    current = await transformers[i](current, context);
  }
  onProgress('complete', 100);
  return current;
}
```

**Step 3 — Stream progress via SSE**
Real-time progress from worker to client:
```typescript
// Worker side: publish progress to Redis pub/sub
async function publishProgress(jobId: string, stage: string, pct: number) {
  await redis.publish(`job:${jobId}:progress`, JSON.stringify({ stage, pct, ts: Date.now() }));
}

// API side: SSE endpoint
app.get('/jobs/:id/progress', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const subscriber = redis.duplicate();
  await subscriber.subscribe(`job:${req.params.id}:progress`);

  subscriber.on('message', (_channel, message) => {
    res.write(`data: ${message}\n\n`);
  });

  req.on('close', () => subscriber.unsubscribe());
});
```

**Step 4 — Two-tier concurrency control**
```typescript
// Team-level: limit concurrent jobs per team
async function canEnqueue(teamId: string): Promise<boolean> {
  const active = await redis.zcard(`team:${teamId}:active`);
  const limit = await getTeamConcurrencyLimit(teamId);
  return active < limit;
}

// Job-level: track active jobs with TTL (auto-cleanup on crash)
async function markActive(teamId: string, jobId: string) {
  await redis.zadd(`team:${teamId}:active`, Date.now(), jobId);
  await redis.expire(`team:${teamId}:active`, 3600);  // 1h TTL safety net
}

async function markComplete(teamId: string, jobId: string) {
  await redis.zrem(`team:${teamId}:active`, jobId);
}
```

**Step 5 — Dynamic credit billing**
```typescript
interface CreditCost {
  base: number;
  engineMultiplier: number;   // stealth proxy = 4x
  formatMultiplier: number;   // JSON extraction = 5x
  extras: number;             // per-page for PDFs, per-territory for pricing
}

function calculateCredits(job: CompletedJob): number {
  let cost = job.cost.base;
  cost *= job.cost.engineMultiplier;
  cost *= job.cost.formatMultiplier;
  cost += job.cost.extras;
  return Math.ceil(cost);
}
```

**Step 6 — Dead letter queue with retry classification**
```typescript
interface FailedJob {
  id: string;
  error: string;
  errorCode: 'TRANSIENT' | 'PERMANENT' | 'TIMEOUT' | 'RATE_LIMITED';
  attempts: number;
  stageTiming: Record<string, number>;  // per-stage perf data
}

// Retry only transient failures; permanent goes to dead letter
function shouldRetry(job: FailedJob): boolean {
  if (job.errorCode === 'PERMANENT') return false;
  if (job.attempts >= 3) return false;
  return true;
}
```

#### Example

```typescript
// Complete async pipeline for document processing
const docPipeline = createPipeline({
  engines: [
    { name: 'native-parser', quality: 100, costMultiplier: 1, execute: nativeParse },
    { name: 'llm-extraction', quality: 80, costMultiplier: 5, execute: llmExtract },
    { name: 'ocr-fallback', quality: 50, costMultiplier: 3, execute: ocrExtract },
  ],
  transforms: [
    cleanHTML,
    extractMetadata,
    convertToMarkdown,
    generateSummary,
    indexForSearch,
  ],
  concurrency: { perTeam: 10, perJob: 3 },
  billing: { base: 1, jsonFormat: 5 },
  deadLetter: { maxRetries: 3, alertThreshold: 10 },
});

// Enqueue
const jobId = await docPipeline.enqueue(teamId, { url, format: 'json' });

// Stream progress
const progress = docPipeline.streamProgress(jobId);
for await (const update of progress) {
  console.log(`${update.stage}: ${update.pct}%`);
}
```

---

# auth-patterns

Authentication and authorization patterns — JWT, OAuth 2.0 / OIDC, passkeys/WebAuthn, session management, RBAC, API key management, MFA flows.

#### Workflow

**Step 1 — Detect auth implementation**
Use Grep to find auth-related code: `jwt.sign`, `jwt.verify`, `bcrypt`, `passport`, `next-auth`, `lucia`, `cookie`, `session`, `Bearer`, `x-api-key`, `WebAuthn`, `passkey`. Read auth middleware and login/register handlers to understand the current approach.

**Step 2 — Audit security posture**
Check for: tokens stored in localStorage (XSS risk → use httpOnly cookies), missing refresh token rotation, JWT without expiry, password hashing without salt rounds check, missing CSRF protection on cookie-based auth, hardcoded secrets. Flag each with severity and specific fix.

**Step 3 — Emit secure auth flow**
Based on detected framework (Express, Fastify, Next.js, etc.), emit the corrected auth flow: access token (short-lived, 15min) + refresh token (httpOnly cookie, 7d, rotation on use), proper password hashing (bcrypt rounds ≥ 12), RBAC middleware with role hierarchy.

**Step 4 — OAuth 2.0 / OIDC integration**
Emit OAuth 2.0 authorization code flow with PKCE (required for public clients). Support Google, GitHub, or custom OIDC provider. Key points: validate `state` parameter to prevent CSRF, validate `id_token` signature and `aud`/`iss` claims, exchange code server-side (never client-side), store provider `sub` as stable user identifier. Use `openid-client` (Node.js) or `authlib` (Python) — never hand-roll token exchange.

**Step 5 — API key management and passkeys**
For API keys: generate with `crypto.randomBytes(32).toString('base64url')`, store hashed (`sha256` is sufficient — no need for bcrypt, keys are long), never store plaintext after initial display. Add scopes (read-only vs read-write), per-key rate limits, and rotation endpoint. For passkeys/WebAuthn: emit registration and authentication ceremonies using `@simplewebauthn/server`. WebAuthn is the correct long-term replacement for passwords — emit as opt-in upgrade path. Stateless vs stateful tradeoff: JWT = stateless, easy to scale horizontally, hard to revoke; sessions = stateful, easy to revoke, requires sticky sessions or shared store (Redis). Recommend JWT + token blacklist on logout for most cases; sessions for admin panels where immediate revocation matters.

#### Example

```typescript
// BEFORE: JWT in localStorage, no refresh, no expiry
const token = jwt.sign({ userId: user.id }, SECRET);
res.json({ token });

// AFTER: short-lived access + httpOnly refresh cookie with rotation
const accessToken = jwt.sign(
  { sub: user.id, role: user.role },
  ACCESS_SECRET,
  { expiresIn: '15m' }
);
const refreshToken = jwt.sign(
  { sub: user.id, jti: crypto.randomUUID() },
  REFRESH_SECRET,
  { expiresIn: '7d' }
);
await tokenStore.save(refreshToken, user.id); // rotation tracking — invalidate old on reuse

res.cookie('refresh_token', refreshToken, {
  httpOnly: true, secure: true, sameSite: 'strict',
  maxAge: 7 * 24 * 60 * 60 * 1000,
});
res.json({ access_token: accessToken, expires_in: 900 });

// API key management
const generateApiKey = async (userId: string, scopes: string[]): Promise<{ key: string; keyId: string }> => {
  const rawKey = `rk_${crypto.randomBytes(32).toString('base64url')}`;
  const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
  const keyId = crypto.randomUUID();
  await db.apiKey.create({ data: { id: keyId, userId, keyHash, scopes, createdAt: new Date() } });
  return { key: rawKey, keyId }; // rawKey shown ONCE — never stored plaintext
};

const authenticateApiKey = async (req, res, next) => {
  const raw = req.headers['x-api-key'];
  if (!raw) return next(); // fallback to JWT auth
  const hash = crypto.createHash('sha256').update(raw).digest('hex');
  const apiKey = await db.apiKey.findUnique({ where: { keyHash: hash } });
  if (!apiKey || apiKey.revokedAt) return res.status(401).json({ error: { code: 'INVALID_API_KEY' } });
  req.user = { id: apiKey.userId, scopes: apiKey.scopes };
  next();
};

// OAuth 2.0 with PKCE (using openid-client)
import { generators, Issuer } from 'openid-client';

const googleIssuer = await Issuer.discover('https://accounts.google.com');
const client = new googleIssuer.Client({ client_id: GOOGLE_CLIENT_ID, redirect_uris: [CALLBACK_URL], response_types: ['code'] });

app.get('/auth/google', (req, res) => {
  const codeVerifier = generators.codeVerifier();
  const codeChallenge = generators.codeChallenge(codeVerifier);
  const state = generators.state();
  req.session.codeVerifier = codeVerifier;
  req.session.state = state;
  res.redirect(client.authorizationUrl({ scope: 'openid email profile', code_challenge: codeChallenge, code_challenge_method: 'S256', state }));
});

app.get('/auth/google/callback', async (req, res) => {
  const params = client.callbackParams(req);
  const tokens = await client.callback(CALLBACK_URL, params, { code_verifier: req.session.codeVerifier, state: req.session.state });
  const claims = tokens.claims(); // validated: iss, aud, exp
  const user = await userRepo.upsertByProvider('google', claims.sub, claims.email);
  // issue internal JWT...
});
```

---

# background-jobs

Queue-based async processing — BullMQ (Node.js), job patterns, retry strategies, idempotency, dead letter queues, monitoring.

#### Workflow

**Step 1 — Identify async operations**
Scan route handlers and service functions for operations that: (a) take > 200ms (PDF generation, image resizing, report aggregation), (b) are non-user-facing (email sending, webhook delivery, analytics events), (c) can tolerate eventual consistency (data sync, cache warming, notification dispatch). Flag these as candidates for background jobs. Output a classification: fire-and-forget vs delayed vs scheduled (cron) vs fan-out.

**Step 2 — Choose queue system**
Node.js: BullMQ (Redis-backed, TypeScript-native, built-in retry/delay/priority/rate-limiting — recommended). Python: Celery + Redis/RabbitMQ broker (mature, distributed workers, beat scheduler for cron). For very simple use cases (single server, low volume): `node-cron` + in-process worker. Avoid in-process queues in production — they die with the process and lose jobs.

**Step 3 — Implement job with retry strategy**
Emit job producer (enqueue) and worker (processor) as separate files. Retry strategy: exponential backoff with jitter (`attempts: 5, backoff: { type: 'exponential', delay: 1000 }`). Idempotency: every job MUST have an idempotency key — use a deterministic ID from the operation (e.g., `email:welcome:${userId}` not a random UUID). This ensures duplicate enqueues (from retries, double-clicks) process exactly once. Dead letter queue: after max retries, move job to a `{queue-name}:failed` queue for inspection and manual replay — never silently drop.

**Step 4 — Add monitoring and alerting**
BullMQ Board or Bull Dashboard for visual queue monitoring. Emit metrics: queue depth (jobs waiting), processing rate (jobs/sec), failure rate (failed/total). Alert when: queue depth > threshold (workers not keeping up), failure rate > 5% (systematic error in processor), job age > expected TTL (stuck job). Use BullMQ events (`queue.on('failed', ...)`) to push metrics to Prometheus or Datadog.

**Step 5 — Handle dead letters**
Emit dead letter inspection endpoint: list failed jobs with error reason, retry count, and last error. Emit replay endpoint: re-enqueue a specific failed job with a fresh retry budget. Purge endpoint: clear dead letter queue after investigation. Add alerting on dead letter queue depth > 0 for critical job types (payment processing, compliance logging).

#### Example

```typescript
// BullMQ setup with TypeScript — producer + worker
import { Queue, Worker, Job } from 'bullmq';

const connection = { host: REDIS_HOST, port: 6379 };

// Job type definitions
interface EmailJob { to: string; template: string; data: Record<string, unknown> }
interface PdfJob { reportId: string; userId: string; format: 'pdf' | 'xlsx' }

// Producers
export const emailQueue = new Queue<EmailJob>('email', { connection });
export const pdfQueue = new Queue<PdfJob>('pdf', { connection });

// Enqueue with idempotency key (jobId = idempotent identifier)
export const sendWelcomeEmail = (userId: string, email: string) =>
  emailQueue.add('welcome', { to: email, template: 'welcome', data: { userId } }, {
    jobId: `email:welcome:${userId}`, // prevents duplicate welcome emails
    attempts: 3,
    backoff: { type: 'exponential', delay: 2_000 },
    removeOnComplete: { count: 1000 }, // keep last 1000 completed for audit
    removeOnFail: false, // keep all failed for dead letter review
  });

// Scheduled/delayed job
export const sendReminderEmail = (userId: string, delayMs: number) =>
  emailQueue.add('reminder', { to: userId, template: 'reminder', data: {} }, {
    delay: delayMs,
    attempts: 5,
    backoff: { type: 'exponential', delay: 5_000 },
  });

// Worker processor with error handling
const emailWorker = new Worker<EmailJob>('email', async (job: Job<EmailJob>) => {
  const { to, template, data } = job.data;
  // Validate job data — serialized payload may be stale
  if (!to || !template) throw new Error(`Invalid job payload: ${JSON.stringify(job.data)}`);
  await emailService.send({ to, template, data });
  // Return value is stored in job.returnvalue for audit
  return { sentAt: new Date().toISOString() };
}, {
  connection,
  concurrency: 10,           // process up to 10 emails in parallel
  limiter: { max: 100, duration: 60_000 }, // rate limit: 100/min
});

emailWorker.on('failed', async (job, err) => {
  logger.error({ jobId: job?.id, queue: 'email', error: err.message, attempts: job?.attemptsMade });
  if (job?.attemptsMade >= job?.opts.attempts!) {
    // max retries exhausted → alert
    await alerting.notify(`Dead letter: email job ${job.id} failed after ${job.attemptsMade} attempts`);
  }
});

// Fan-out pattern: one job enqueues many children
const fanOutNotification = async (eventId: string, userIds: string[]) => {
  const jobs = userIds.map(userId => ({
    name: 'notify',
    data: { userId, eventId },
    opts: {
      jobId: `notify:${eventId}:${userId}`,
      attempts: 3,
      backoff: { type: 'exponential', delay: 1_000 },
    },
  }));
  await notificationQueue.addBulk(jobs);
};

// Dead letter inspection API
app.get('/admin/jobs/failed', authenticate, authorize('admin'), async (req, res) => {
  const failed = await emailQueue.getFailed(0, 50);
  res.json({ count: failed.length, jobs: failed.map(j => ({ id: j.id, data: j.data, reason: j.failedReason, attempts: j.attemptsMade })) });
});

app.post('/admin/jobs/:id/retry', authenticate, authorize('admin'), async (req, res) => {
  const job = await emailQueue.getJob(req.params.id);
  if (!job) return res.status(404).json({ error: { code: 'NOT_FOUND' } });
  await job.retry();
  res.json({ status: 'retried' });
});

// Celery equivalent (Python) — minimal pattern
# tasks.py
from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)
app.conf.task_acks_late = True  # at-least-once delivery
app.conf.task_reject_on_worker_lost = True  # requeue on worker crash
logger = get_task_logger(__name__)

@app.task(bind=True, max_retries=5, default_retry_delay=60)
def send_email(self, to: str, template: str, data: dict) -> dict:
    try:
        result = email_service.send(to=to, template=template, data=data)
        return {'sent_at': result.timestamp.isoformat()}
    except TransientError as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)
    except PermanentError as exc:
        logger.error(f"Permanent failure for {to}: {exc}")
        raise  # no retry — goes to dead letter
```

---

# caching-patterns

Caching strategies for backend applications — in-memory LRU, Redis distributed cache, CDN/edge cache, browser cache headers, invalidation, and stampede prevention.

#### Workflow

**Step 1 — Identify cacheable endpoints**
Scan routes for: (a) read-heavy endpoints called frequently with the same inputs (user profile, product catalog, config lookups), (b) expensive computations (aggregations, report generation), (c) external API calls that are rate-limited or slow. Flag endpoints that mutate state as NOT cacheable at the response level (cache the data layer instead). Output a cacheable/non-cacheable classification per endpoint.

**Step 2 — Select cache layer**
Choose layer based on access pattern: in-memory (node-cache, LRU-cache) for single-process data with sub-millisecond access and low cardinality; Redis for distributed cache shared across multiple server instances or processes; CDN (Cloudflare, Fastly) for public, user-agnostic responses (marketing pages, public API responses); browser cache (`Cache-Control` headers) for static assets and safe GET responses. Hybrid: in-memory L1 + Redis L2 for hot-path data that justifies two-layer lookup.

**Step 3 — Implement cache pattern**
Cache-aside (most common): application checks cache first, on miss fetches from DB, writes to cache. Write-through: write to cache and DB together on every write (cache always warm, higher write latency). Write-behind (write-back): write to cache immediately, flush to DB asynchronously (lowest write latency, risk of data loss on crash). Read-through: cache sits in front of DB, handles miss transparently (simpler app code, less control). For most web APIs: cache-aside for reads + TTL-based expiry is the correct default.

**Step 4 — Add invalidation strategy**
TTL-based: set appropriate TTL per data type (user session: match auth token TTL; product catalog: 5–15min; config: 1hr). Event-driven: on mutation, publish event to Redis pub/sub, cache subscribers delete affected keys. Versioned keys: `cache:user:v3:{id}` — bump version in config to invalidate all users atomically. Tag-based: associate keys with tags (`tag:user:123`), delete all keys for a tag on mutation. Stale-while-revalidate: serve stale data immediately, refresh in background — valid for data where slight staleness is acceptable (leaderboards, stats). Emit invalidation hook alongside every write operation.

**Step 5 — Monitor hit/miss ratio**
Instrument cache calls to emit metrics: hit count, miss count, eviction count, cache size. Redis provides `INFO stats` — parse `keyspace_hits` and `keyspace_misses`. Target hit ratio > 80% for hot-path caches; < 50% indicates wrong key granularity or TTL too short. Alert on sudden hit ratio drop (invalidation bug) or memory > 80% of `maxmemory` (eviction risk).

#### Example

```typescript
// Redis cache-aside middleware for Express/Fastify
import { Redis } from 'ioredis';
const redis = new Redis(REDIS_URL);

const cacheMiddleware = (ttlSeconds: number, keyFn?: (req) => string) =>
  async (req, res, next) => {
    const key = keyFn ? keyFn(req) : `cache:${req.method}:${req.originalUrl}`;
    const cached = await redis.get(key);
    if (cached) {
      res.setHeader('X-Cache', 'HIT');
      return res.json(JSON.parse(cached));
    }
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      // Only cache successful responses
      if (res.statusCode < 400) redis.setex(key, ttlSeconds, JSON.stringify(data));
      res.setHeader('X-Cache', 'MISS');
      return originalJson(data);
    };
    next();
  };

// Usage: cache product list for 5 minutes
app.get('/products', cacheMiddleware(300), async (req, res) => { /* handler */ });

// Cache stampede prevention: mutex lock on cache miss
const getWithLock = async <T>(key: string, fetchFn: () => Promise<T>, ttl: number): Promise<T> => {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:${key}`;
  const lock = await redis.set(lockKey, '1', 'EX', 10, 'NX'); // 10s lock
  if (!lock) {
    // Another process is fetching — wait briefly and retry
    await new Promise(r => setTimeout(r, 100));
    return getWithLock(key, fetchFn, ttl); // retry (max ~10 cycles within 10s lock)
  }

  try {
    const data = await fetchFn();
    await redis.setex(key, ttl, JSON.stringify(data));
    return data;
  } finally {
    await redis.del(lockKey);
  }
};

// Event-driven invalidation with Redis pub/sub
const invalidateOnMutation = async (userId: string) => {
  await redis.del(`cache:user:${userId}`);
  await redis.publish('cache:invalidate', JSON.stringify({ type: 'user', id: userId }));
};

// Cache-Control headers for browser/CDN caching
app.get('/products', (req, res) => {
  res.setHeader('Cache-Control', 'public, max-age=300, stale-while-revalidate=60');
  // ^ CDN caches 5min, serves stale for extra 60s while revalidating in background
  res.json(products);
});

app.get('/user/profile', authenticate, (req, res) => {
  res.setHeader('Cache-Control', 'private, max-age=60'); // user-specific, browser only
  res.json(profile);
});

// In-memory LRU cache for single-process hot data
import LRU from 'lru-cache';
const configCache = new LRU<string, unknown>({ max: 500, ttl: 60_000 }); // 500 entries, 1min TTL

const getConfig = async (key: string) => {
  if (configCache.has(key)) return configCache.get(key);
  const value = await db.config.findUnique({ where: { key } });
  configCache.set(key, value);
  return value;
};
```

---

# cli-generation

Generate production-grade CLI wrappers for backend services — command groups, dual output mode (human + JSON), stateful REPL, session management with undo/redo, and pip/npm-installable packaging.

#### Workflow

**Step 1 — Analyze backend service surface**
Map existing API endpoints, service methods, or data models to CLI command groups:
```typescript
interface CLICommandGroup {
  name: string;          // e.g., 'users', 'orders', 'config'
  source: string;        // API route file or service class
  commands: CLICommand[];
}

interface CLICommand {
  name: string;          // e.g., 'list', 'create', 'delete'
  sourceMethod: string;  // e.g., 'UserService.findAll'
  params: CLIParam[];
  mutating: boolean;     // true = needs confirmation/undo support
}
```

**Step 2 — Design dual output mode**
Every command MUST support both human-readable and machine-readable output:
```typescript
// Human mode (default): tables, colors, formatted text
function formatHuman(data: any, format: 'table' | 'list' | 'detail'): string {
  if (format === 'table') return formatTable(data, { borders: true, colors: true });
  if (format === 'list') return data.map((d: any) => `  • ${d.name}`).join('\n');
  return JSON.stringify(data, null, 2);
}

// JSON mode (--json flag): structured output for piping/scripting
function formatJSON(data: any): string {
  return JSON.stringify(data, null, 2);
}

// Error output follows same dual pattern
function formatError(error: Error, jsonMode: boolean): string {
  if (jsonMode) return JSON.stringify({ error: error.message, type: error.constructor.name });
  return chalk.red(`Error: ${error.message}`);
}
```

**Step 3 — Implement session with undo/redo**
For mutating operations, maintain session state:
```typescript
interface CLISession {
  id: string;
  history: SessionSnapshot[];
  undoStack: SessionSnapshot[];   // max 50
  redoStack: SessionSnapshot[];
  modified: boolean;
}

function snapshot(session: CLISession, action: string): CLISession {
  return {
    ...session,
    undoStack: [...session.undoStack.slice(-49), { action, state: deepCopy(session) }],
    redoStack: [],  // new action clears redo
    modified: true,
  };
}
```

**Step 4 — Build REPL mode**
CLI enters REPL when invoked without subcommand:
```typescript
// Click (Python) — invoke_without_command=True enters REPL
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        start_repl(ctx)

// Commander (Node.js) — detect no args
if (process.argv.length <= 2) {
  startREPL({ history: '~/.myapp_history', prompt: 'myapp> ' });
}
```

REPL features: command history (file-persisted), auto-suggest from history, tab completion, colored prompt, help command, status bar showing connection state.

**Step 5 — Package for distribution**
```bash
# Python: PEP 420 namespace packages for independent installability
# pyproject.toml or setup.py
entry_points = {
    'console_scripts': ['myapp = myapp.cli:main'],
}

# Node.js: bin field in package.json
{
  "bin": { "myapp": "./bin/cli.js" },
  "files": ["bin/", "lib/"]
}
```

**Step 6 — Verify installation**
After packaging: install locally (`pip install -e .` or `npm link`), verify binary on PATH (`which myapp`), run `myapp --version`, test `myapp --json` mode, and verify REPL launch.

#### Example

```python
# Generated CLI structure for a backend service
# myapp/
# ├── cli.py          ← Click entry point + REPL
# ├── commands/
# │   ├── users.py    ← User CRUD commands
# │   ├── orders.py   ← Order management
# │   └── config.py   ← Config operations
# ├── core/
# │   ├── session.py  ← Session + undo/redo
# │   └── client.py   ← API client wrapper
# └── utils/
#     ├── output.py   ← Dual output (human + JSON)
#     └── repl.py     ← REPL with prompt-toolkit

# Usage:
# myapp users list                    → human-readable table
# myapp users list --json             → JSON output for piping
# myapp users create --name "Alice"   → creates user, snapshots for undo
# myapp                               → enters REPL mode
```

---

# database-patterns

Database design and query patterns — schema design, migrations, indexing strategies, N+1 prevention, soft deletes, read replicas, connection pooling, seeding.

#### Workflow

**Step 1 — Detect ORM and query patterns**
Use Grep to find ORM usage (`prisma.`, `knex(`, `sequelize.`, `typeorm`, `drizzle`, `mongoose.`, `db.query`) and raw SQL strings. Read schema files (`schema.prisma`, `migrations/`, `models/`) to understand the data model.

**Step 2 — Detect N+1 and missing indexes**
Scan for loops containing database calls (a query inside `for`, `map`, `forEach` → N+1). Check foreign key columns for missing indexes. Identify queries with `WHERE` clauses on unindexed columns. Flag each with the specific query and fix.

**Step 3 — Emit optimized queries**
For N+1: emit eager loading (`include`, `populate`, `JOIN`). For missing indexes: emit migration files. For unsafe raw SQL: emit parameterized version. For connection pooling: check pool config and recommend sizing based on max connections.

**Step 4 — Soft delete and query scoping**
Emit soft delete pattern: add `deleted_at TIMESTAMPTZ` column, update all `findMany`/`findUnique` calls to include `WHERE deleted_at IS NULL`. Cascade consideration: soft-delete parent should soft-delete children (emit trigger or application-level cascade). For Prisma: emit a custom extension that injects the filter automatically. Warn about index bloat from soft-deleted rows — add partial index `WHERE deleted_at IS NULL` to keep index lean.

**Step 5 — Read replicas, connection pooling, and seeding**
Read replicas: emit query routing — writes to primary, reads to replica. Handle replication lag: do not read from replica immediately after write in the same request (use primary for the read-after-write). For Prisma: emit `$extends` with read/write client split. Connection pooling deep dive: PgBouncer in transaction mode for serverless (each query gets a connection); Prisma's built-in pool for long-running servers. Pool sizing formula: `connections = (core_count * 2) + effective_spindle_count`. Seeding: emit factory functions using `@faker-js/faker` — deterministic seeds via `faker.seed(42)` for reproducible test data.

#### Example

```typescript
// BEFORE: N+1 — one query per post to get author
const posts = await prisma.post.findMany();
for (const post of posts) {
  post.author = await prisma.user.findUnique({ where: { id: post.authorId } });
}

// AFTER: eager loading, single query with JOIN
const posts = await prisma.post.findMany({
  include: { author: { select: { id: true, name: true, avatar: true } } },
});

// Migration: missing indexes + soft delete column
-- Migration: add_indexes_and_soft_delete_to_posts
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_posts_active ON posts(author_id, created_at DESC) WHERE deleted_at IS NULL;

// Prisma soft delete extension (auto-scopes all queries)
const softDelete = Prisma.defineExtension({
  name: 'softDelete',
  query: {
    $allModels: {
      async findMany({ model, operation, args, query }) {
        args.where = { ...args.where, deletedAt: null };
        return query(args);
      },
      async delete({ model, args, query }) {
        return (query as any)({ ...args, data: { deletedAt: new Date() } } as any);
      },
    },
  },
});
const prisma = new PrismaClient().$extends(softDelete);

// Read replica routing with Prisma
const primaryClient = new PrismaClient({ datasources: { db: { url: PRIMARY_URL } } });
const replicaClient = new PrismaClient({ datasources: { db: { url: REPLICA_URL } } });
const db = { write: primaryClient, read: replicaClient };
// Usage: db.write.user.create(...) vs db.read.user.findMany(...)

// Factory seeding
import { faker } from '@faker-js/faker';
faker.seed(42); // reproducible

const createUserFactory = (overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  createdAt: faker.date.past(),
  ...overrides,
});

await prisma.user.createMany({ data: Array.from({ length: 50 }, () => createUserFactory()) });
```

---

# middleware-patterns

Middleware architecture — request validation, error handling, logging, CORS, compression, graceful shutdown, health checks, request ID tracking.

#### Workflow

**Step 1 — Audit middleware stack**
Read the main server file (app.ts, server.ts, index.ts) to inventory all middleware in registration order. Check for: missing request ID generation, missing structured logging, inconsistent error responses, missing input validation, CORS misconfiguration (`*` in production).

**Step 2 — Detect error handling gaps**
Use Grep to find `catch` blocks, error middleware signatures (`err, req, res, next`), and unhandled promise rejections. Check if errors return consistent format (same envelope for 400, 401, 403, 404, 500). Flag any that leak stack traces or internal details in production.

**Step 3 — Emit middleware improvements**
For each gap, emit the middleware function: request ID (`X-Request-Id` header, UUID per request), structured JSON logger (request method, path, status, duration, request ID), global error handler with consistent envelope, Zod-based request validation middleware.

**Step 4 — Compression strategy**
Emit response compression middleware. Use `brotli` for static assets and pre-compressible responses (better ratio than gzip, supported by all modern clients). Use `gzip` as fallback for older clients. Conditional compression: skip for already-compressed content types (`image/*`, `video/*`, `application/zip`) — compressing these wastes CPU. In Express: use `compression` package with a `filter` function. In Fastify: `@fastify/compress` with `encodings: ['br', 'gzip']`. Minimum size threshold: do not compress responses < 1KB (overhead exceeds benefit).

**Step 5 — Graceful shutdown and health checks**
Graceful shutdown: on `SIGTERM`/`SIGINT`, stop accepting new connections, wait for in-flight requests to complete (timeout 30s), then close DB pools and exit. Emit the shutdown handler for Express (`server.close()`), Fastify (`fastify.close()`), and worker processes. Health check endpoints: `/health/live` (liveness — is the process alive? return 200 always unless process is broken), `/health/ready` (readiness — can it serve traffic? check DB connection, Redis connection, return 503 if dependencies are down). In Kubernetes: map liveness to `livenessProbe`, readiness to `readinessProbe`. Do NOT check external third-party APIs in readiness — only your own dependencies.

#### Example

```typescript
// Request ID middleware
const requestId = (req, res, next) => {
  req.id = req.headers['x-request-id'] || crypto.randomUUID();
  res.setHeader('X-Request-Id', req.id);
  next();
};

// Structured error handler — consistent envelope, no stack leak
const errorHandler = (err, req, res, _next) => {
  const status = err.status || 500;
  const message = status < 500 ? err.message : 'Internal server error';
  logger.error({ err, requestId: req.id, path: req.path });
  res.status(status).json({
    error: { code: err.code || 'INTERNAL_ERROR', message },
    request_id: req.id,
  });
};

// Zod validation middleware
const validate = (schema: z.ZodSchema) => (req, res, next) => {
  const result = schema.safeParse({ body: req.body, query: req.query, params: req.params });
  if (!result.success) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: 'Invalid request', details: result.error.flatten() } });
  }
  Object.assign(req, result.data);
  next();
};

// Compression with conditional skip (Express)
import compression from 'compression';
app.use(compression({
  filter: (req, res) => {
    const contentType = res.getHeader('Content-Type') as string || '';
    if (/image|video|audio|zip|gz|br/.test(contentType)) return false;
    return compression.filter(req, res);
  },
  threshold: 1024, // skip responses < 1KB
}));

// Graceful shutdown
const gracefulShutdown = async (signal: string) => {
  console.log(`Received ${signal}, shutting down gracefully...`);
  server.close(async () => {
    try {
      await prisma.$disconnect();
      await redis.quit();
      console.log('All connections closed. Exiting.');
      process.exit(0);
    } catch (err) {
      console.error('Error during shutdown:', err);
      process.exit(1);
    }
  });
  // Force exit after 30s if still not done
  setTimeout(() => { console.error('Forced shutdown after timeout'); process.exit(1); }, 30_000);
};
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Health check endpoints
app.get('/health/live', (req, res) => res.json({ status: 'ok' }));

app.get('/health/ready', async (req, res) => {
  const checks = await Promise.allSettled([
    prisma.$queryRaw`SELECT 1`,   // DB check
    redis.ping(),                  // Redis check
  ]);
  const results = { db: checks[0].status, redis: checks[1].status };
  const allHealthy = checks.every(c => c.status === 'fulfilled');
  res.status(allHealthy ? 200 : 503).json({ status: allHealthy ? 'ready' : 'degraded', checks: results });
});
```

---
> **Rune Skill Mesh** — 64 skills, 203 connections + 40 signals, 14 extension packs
> [Landing Page](https://rune-kit.github.io/rune) · [Source](https://github.com/rune-kit/rune) (MIT)
> **Rune Pro** ($49 lifetime) — product, sales, data-science, support packs → [rune-kit/rune-pro](https://github.com/rune-kit/rune-pro)
> **Rune Business** ($149 lifetime) — finance, legal, HR, enterprise-search packs → [rune-kit/rune-business](https://github.com/rune-kit/rune-business)