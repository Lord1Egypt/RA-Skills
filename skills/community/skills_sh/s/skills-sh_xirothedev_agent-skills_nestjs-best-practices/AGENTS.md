# NestJS Best Practices

**Version 1.0.0**  
Xiro - The Terminal Labs Engineering  
January 2026

> **Note:**  
> This document is mainly for agents and LLMs to follow when maintaining,  
> generating, or refactoring NestJS codebases. Humans  
> may also find it useful, but guidance here is optimized for automation  
> and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive performance optimization guide for NestJS with expressjs platform applications, designed for AI agents and LLMs. Contains 40+ rules across 8 categories, prioritized by impact from critical (eliminating waterfalls, reducing bundle size) to incremental (advanced patterns). Each rule includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and specific impact metrics to guide automated refactoring and code generation.

---

## Table of Contents

1. [Section 1](#1-section-1) — **CRITICAL**
   - 1.1 [Enable CORS with Whitelist Origins Only](#11-enable-cors-with-whitelist-origins-only)
   - 1.2 [Regular Dependency Security Audits](#12-regular-dependency-security-audits)
   - 1.3 [Use Helmet Middleware for Security Headers](#13-use-helmet-middleware-for-security-headers)
2. [Section 2](#2-section-2) — **HIGH**
   - 2.1 [Cache Frequently Used Data with Redis](#21-cache-frequently-used-data-with-redis)
3. [Section 3](#3-section-3) — **MEDIUM**
   - 3.1 [Keep Functions Short and Single Purpose](#31-keep-functions-short-and-single-purpose)
   - 3.2 [Organize Code by Feature Modules](#32-organize-code-by-feature-modules)
   - 3.3 [Remove Unused Code and Dependencies](#33-remove-unused-code-and-dependencies)
   - 3.4 [Single Responsibility - Separate Controller and Service](#34-single-responsibility---separate-controller-and-service)
   - 3.5 [Use Consistent Naming Conventions](#35-use-consistent-naming-conventions)
   - 3.6 [Use Enum Classes for Type-Safe Values](#36-use-enum-classes-for-type-safe-values)
   - 3.7 [Use Event-Driven Architecture for Loose Coupling](#37-use-event-driven-architecture-for-loose-coupling)
4. [Section 4](#4-section-4) — **CRITICAL**
   - 4.1 [Enable Global Exception Filter](#41-enable-global-exception-filter)
   - 4.2 [Implement Proper Logging Strategy](#42-implement-proper-logging-strategy)
   - 4.3 [Use Logger with Module Context for Debugging](#43-use-logger-with-module-context-for-debugging)
5. [Section 5](#5-section-5) — **MEDIUM**
   - 5.1 [Create Custom Pipes for Query Parameter Transformation](#51-create-custom-pipes-for-query-parameter-transformation)
   - 5.2 [Use Filter DTOs for Query Parameter Validation](#52-use-filter-dtos-for-query-parameter-validation)
   - 5.3 [Validate All Inputs with DTOs and ValidationPipe](#53-validate-all-inputs-with-dtos-and-validationpipe)
6. [Section 6](#6-section-6) — **CRITICAL**
   - 6.1 [Use Custom Repository Pattern for Database Logic Encapsulation](#61-use-custom-repository-pattern-for-database-logic-encapsulation)
   - 6.2 [Use Parameterized Queries to Prevent SQL Injection](#62-use-parameterized-queries-to-prevent-sql-injection)
7. [Section 7](#7-section-7) — **HIGH**
   - 7.1 [Use Bun's Built-in Crypto for Secure Password Hashing](#71-use-buns-built-in-crypto-for-secure-password-hashing)
   - 7.2 [Use Custom Decorators for Type-Safe Request Data Access](#72-use-custom-decorators-for-type-safe-request-data-access)
   - 7.3 [Use Guards for Route Protection](#73-use-guards-for-route-protection)
8. [Section 8](#8-section-8) — **HIGH**
   - 8.1 [Generate Swagger/OpenAPI Documentation](#81-generate-swaggeropenapi-documentation)
   - 8.2 [Use Cursor-Based Pagination for Large Datasets](#82-use-cursor-based-pagination-for-large-datasets)
9. [Section 9](#9-section-9) — **CRITICAL**
   - 9.1 [Never Hardcode Secrets - Use Environment Variables](#91-never-hardcode-secrets---use-environment-variables)
10. [Section 10](#10-section-10) — **MEDIUM**
   - 10.1 [Write Comprehensive Unit Tests](#101-write-comprehensive-unit-tests)
11. [Section 11](#11-section-11) — **HIGH**
   - 11.1 [Implement Health Check Endpoints](#111-implement-health-check-endpoints)
12. [Section 12](#12-section-12) — **HIGH**
   - 12.1 [Enable Compression Middleware for Responses](#121-enable-compression-middleware-for-responses)
   - 12.2 [Implement Rate Limiting for All Routes](#122-implement-rate-limiting-for-all-routes)
13. [Section 13](#13-section-13) — **HIGH**
   - 13.1 [Lazy Load Non-Critical Modules](#131-lazy-load-non-critical-modules)
   - 13.2 [Use @nestjs/schedule for Cron Jobs and Scheduled Tasks](#132-use-nestjsschedule-for-cron-jobs-and-scheduled-tasks)
14. [Section 14](#14-section-14) — **MEDIUM**
   - 14.1 [Use Response Transformation Interceptor for Serialization](#141-use-response-transformation-interceptor-for-serialization)

---

## 1. Section 1

**Impact: CRITICAL**

### 1.1 Enable CORS with Whitelist Origins Only

**Impact: CRITICAL (Prevents unauthorized domain access)**

Wildcard CORS (`*`) allows malicious sites to make requests to your API. Explicit origin whitelist prevents cross-site attacks. **Never use wildcard in production.**

**Incorrect: vulnerable CORS**

```typescript
// main.ts
app.enableCors();  // Uses '*' - dangerous! 🚨
```

**Correct: secure CORS**

```typescript
// main.ts
app.enableCors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://yourapp.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
});
```

### 1.2 Regular Dependency Security Audits

**Impact: CRITICAL (Prevents exploitation of known vulnerabilities in packages)**

Outdated dependencies contain known vulnerabilities that attackers exploit. Automated scanning with npm audit, bun audit, and Snyk catches issues before production. **Never deploy without clean dependency audit.**

**Incorrect: vulnerable deps**

```json
// package.json - outdated packages 🚨
{
  "dependencies": {
    "lodash": "^4.17.20",  // CVE-2021-23337
    "express": "^4.17.1"    // Multiple CVEs
  }
}
```

**Correct: automated security**

```bash
# Pre-commit / CI checks
bun run audit:check
npm audit --audit-level high
bun pm audit           # Bun's audit check
snyk test --severity-threshold=high
```

**Workflow:**

- `npm audit` or `bun pm audit` weekly in CI/CD

- `npm audit fix` auto-updates patches

- Snyk/Dependabot for vulnerability alerts

- Pin major versions, auto-patch minors

### 1.3 Use Helmet Middleware for Security Headers

**Impact: CRITICAL (Protects against XSS, clickjacking, and other web attacks)**

NestJS with Express adapter exposes HTTP headers that can be exploited by attackers. Helmet automatically sets security headers like X-XSS-Protection, X-Frame-Options, and Content-Security-Policy. **Always enable it in production.**

> **Hint**: Apply `helmet` as global middleware **before** other calls to `app.use()` or route definitions. Middleware order matters - routes defined before helmet will not have security headers applied.

**Express: default adapter**

```bash
bun add helmet
```

**Fastify adapter:**

```bash
bun add @fastify/helmet
```

**Incorrect: vulnerable headers**

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

**Correct: Express**

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

**Correct: Fastify**

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

Reference: [https://docs.nestjs.com/security/helmet](https://docs.nestjs.com/security/helmet)

---

## 2. Section 2

**Impact: HIGH**

### 2.1 Cache Frequently Used Data with Redis

**Impact: HIGH (Dramatically reduces database load and improves response times)**

Every database query increases latency and costs. Redis caching stores hot data in memory for sub-millisecond access. **Cache read-heavy endpoints and expensive computations.**

**Incorrect: database every request**

```typescript
// users.service.ts - DB hit every time 🚨
async getUserProfile(id: string) {
  return this.prisma.user.findUnique({
    where: { id },
    include: { posts: true, followers: true }
  });
}
```

**Correct: Redis cached**

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

---

## 3. Section 3

**Impact: MEDIUM**

### 3.1 Keep Functions Short and Single Purpose

**Impact: MEDIUM (Improves testability and reduces bugs)**

Long functions with multiple responsibilities are hard to test, debug, and maintain. Short functions (<20 lines) with one clear purpose are easier to understand. **Extract logic into focused helper functions.**

**Incorrect: god function**

```typescript
@Post()
async createUser(@Body() data: any) {
  // 3 responsibilities mixed 🚨
  const hashedPassword = await bcrypt.hash(data.password, 10);
  const user = await this.prisma.user.create({ data: {...data, password: hashedPassword} });
  const token = jwt.sign({ id: user.id }, process.env.JWT_SECRET);
  await this.sendWelcomeEmail(user.email);
  return { user, token };
}
```

**Correct: single responsibility**

```typescript
@Post()
async createUser(@Body() data: CreateUserDto) {
  const hashedPassword = await this.hashPassword(data.password);
  const user = await this.usersRepository.create({ ...data, password: hashedPassword });
  const token = this.generateToken(user.id);
  await this.emailService.sendWelcome(user.email);
  return { user, token };  // ✅ Orchestration only
}

private async hashPassword(password: string) {
  return bcrypt.hash(password, 10);
}
```

### 3.2 Organize Code by Feature Modules

**Impact: HIGH (Improves scalability and maintainability)**

Flat controller/service structure becomes unmaintainable at scale. NestJS modules enforce separation of concerns by feature. **One module per business domain.**

> **Hint**: Use feature modules to encapsulate related controllers, services, and providers. Each module should be independently testable and reusable across the application.

**Incorrect:**

```typescript
src/
  users.controller.ts
  users.service.ts
  auth.controller.ts
  auth.service.ts
  products.controller.ts  // Chaos!
  products.service.ts
  orders.controller.ts
  orders.service.ts
```

**Correct:**

```typescript
// orders/orders.service.ts
import { EventEmitter2 } from '@nestjs/event-emitter';

@Injectable()
export class OrdersService {
  constructor(private eventEmitter: EventEmitter2) {}

  async createOrder(order: CreateOrderDto) {
    const newOrder = await this.save(order);

    // Emit event, don't directly call other services
    this.eventEmitter.emit('order.created', { orderId: newOrder.id });

    return newOrder;
  }
}

// email/email.service.ts
import { OnEvent } from '@nestjs/event-emitter';

@Injectable()
export class EmailService {
  @OnEvent('order.created')
  async sendOrderConfirmation(payload: { orderId: string }) {
    await this.sendEmail({
      to: 'customer@example.com',
      subject: 'Order Confirmation',
      body: `Order ${payload.orderId} received`,
    });
  }
}
```

Services can be shared across multiple modules by exporting them:

Use `@Global()` for modules that should be available everywhere without importing:

> **Warning**: Use global modules sparingly. Only use for truly universal services like logging, configuration, or utilities.

Create configurable modules with `register()` or `forRoot()` patterns:

Modules must explicitly declare their dependencies:

Best practice structure for a feature module:

| Practice | Description | Why |

|----------|-------------|-----|

| One module per feature | Each business domain gets its own module | Clear separation of concerns |

| Export only what's needed | Only export services meant for external use | Prevents tight coupling |

| Use DTOs in each module | Keep data transfer objects with the module | Encapsulates validation logic |

| Avoid circular dependencies | Don't have Module A import Module B if B imports A | Prevents initialization issues |

| Use barrel exports | Export from `index.ts` for clean imports | Better developer experience |

Test modules in isolation:

**Sources:**

- [Modules | NestJS - Official Documentation](https://docs.nestjs.com/modules)

- [Dynamic Modules | NestJS](https://docs.nestjs.com/fundamentals/dynamic-modules)

- [Custom Providers | NestJS](https://docs.nestjs.com/providers#custom-providers)

- [EventEmitter2 | NestJS Recipe](https://docs.nestjs.com/techniques/events)

### 3.3 Remove Unused Code and Dependencies

**Impact: MEDIUM (Reduces bundle size and maintenance burden)**

Dead code bloats the project and confuses developers. Unused dependencies increase attack surface. Regular cleanup keeps codebase lean. **No unused imports, functions, or packages.**

**Incorrect: code rot**

```json
// package.json - Unused deps
{
  "dependencies": {
    "lodash": "^4.17.20",     // Never imported
    "moment": "^2.29.4",      // Replaced by date-fns
    "axios": "^1.0.0"         // Switched to fetch
  }
}
```

**Correct: clean codebase**

```json
// package.json - Clean ✅
{
  "scripts": {
    "cleanup": "bun pm prune && bun pm cache rm && bun run lint:fix",
    "depcheck": "depcheck && ts-unused-exports tsconfig.json"
  }
}
```

### 3.4 Single Responsibility - Separate Controller and Service

**Impact: HIGH (Makes testing and maintenance easier)**

| Controllers (HTTP Layer) | Services (Business Layer) |

|--------------------------|---------------------------|

| Parse request bodies | Execute business logic |

| Validate with DTOs | Perform calculations |

| Return HTTP status codes | Transform data |

| Handle routing | Manage transactions |

| Set headers/cookies | Call external APIs |

| Upload/download files | Enforce business rules |

**Incorrect:**

```typescript
@Controller('orders')
export class OrdersController {
  constructor(private repository: OrdersRepository) {}

  @Post()
  async createOrder(@Body() data: any) {
    // 🚨 Validation logic
    if (!data.email || !this.isValidEmail(data.email)) {
      throw new BadRequestException('Invalid email');
    }

    // 🚨 Business logic - checking inventory
    const product = await this.repository.getProduct(data.productId);
    if (product.stock < data.quantity) {
      throw new BadRequestException('Insufficient stock');
    }

    // 🚨 Business logic - calculating discount
    let discount = 0;
    if (data.quantity > 10) {
      discount = 0.1;
    } else if (data.quantity > 5) {
      discount = 0.05;
    }

    // 🚨 Business logic - calculating total
    const subtotal = product.price * data.quantity;
    const total = subtotal * (1 - discount);

    // 🚨 Data access logic
    const order = await this.repository.save({
      productId: data.productId,
      quantity: data.quantity,
      total,
    });

    // 🚨 External service call
    await this.emailService.sendConfirmation(data.email, order.id);

    return order;
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

**Problems:**

- Cannot test business logic without HTTP context

- Cannot reuse business logic in other contexts (CLI, GraphQL, WebSocket)

- Difficult to mock dependencies for testing

- Changes to business logic require HTTP layer changes

**Correct:**

```typescript
┌─────────────────────────────────────────────────────┐
│                   Controller Layer                   │
│  - Parse HTTP requests                               │
│  - Validate with DTOs                                │
│  - Set status codes and headers                      │
│  - Delegate to services                              │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                    Service Layer                     │
│  - Execute business logic                            │
│  - Enforce business rules                            │
│  - Coordinate multiple repositories                  │
│  - Emit domain events                                │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                  Repository Layer                    │
│  - Data access                                       │
│  - Database queries                                  │
│  - Entity persistence                                │
└─────────────────────────────────────────────────────┘
```

Controllers SHOULD handle HTTP-specific details:

**Sources:**

- [Controllers | NestJS - Official Documentation](https://docs.nestjs.com/controllers)

- [Providers | NestJS - Official Documentation](https://docs.nestjs.com/providers)

- [Single Responsibility Principle | Wikipedia](https://en.wikipedia.org/wiki/Single-responsibility_principle)

- [Clean Architecture | Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### 3.5 Use Consistent Naming Conventions

**Impact: MEDIUM (Improves code readability and maintainability)**

Inconsistent naming confuses developers and breaks tooling. NestJS follows specific conventions for maximum clarity. **Standardize all filenames, classes, and methods.**

**Incorrect: mixed conventions**

```typescript
userController.ts      // camelCase file
UserService.ts         // PascalCase file  
getuserById()          // mixed case method
Userservice            // missing suffix
```

**Correct: NestJS conventions**

```typescript
users.controller.ts    // kebab-case file
users.service.ts       // kebab-case file
UsersController        // PascalCase class
UsersService           // PascalCase class
findUserById()         // camelCase method ✅
getUserProfile()       // camelCase method ✅
```

### 3.6 Use Enum Classes for Type-Safe Values

**Impact: MEDIUM (Prevents typos and improves autocomplete)**

When implementing or reviewing constant values, **always** follow these steps:

**Pattern to check:** Look for string literals assigned to variables, compared in conditionals, or used as status/type values.

**If found:** Replace with enums.

**File:** `tasks/task-status.enum.ts`

**File:** `tasks/task.entity.ts`

**File:** `tasks/dto/create-task.dto.ts`

**Incorrect:**

```typescript
// tasks/tasks.service.ts - String literals 🚨
import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksService {
  // ❌ String parameter - any value accepted
  async updateStatus(id: string, status: string) {
    const task = await this.repo.findOne(id);
    task.status = status; // ❌ No type safety
    return this.repo.save(task);
  }

  // ❌ Typo-prone comparisons
  async getOpenTasks() {
    // If you type 'opne' instead of 'open', no error!
    return this.repo.find({ where: { status: 'opne' } });
  }

  // ❌ Magic strings throughout code
  async completeTask(id: string) {
    const task = await this.repo.findOne(id);
    task.status = 'done'; // ❌ What if other code uses 'DONE'?
    return this.repo.save(task);
  }

  // ❌ Inconsistent values
  async createTask(title: string) {
    // Is it 'open', 'Open', or 'OPEN'?
    const task = this.repo.create({ title, status: 'OPEN' });
    return this.repo.save(task);
  }
}

// tasks/dto/create-task.dto.ts 🚨
export class CreateTaskDto {
  title: string;

  // ❌ No validation of allowed values
  status?: string;
}

// tasks/task.entity.ts 🚨
import { Entity, Column } from 'typeorm';

@Entity()
export class Task {
  @Column({
    type: 'varchar', // ❌ No enum type constraint
  })
  status: string; // ❌ Any string can be stored
}
```

**Correct:**

```typescript
// ✅ Alternative: String union types (for simple cases)
// tasks/task-status.type.ts
export type TaskStatus = 'OPEN' | 'IN_PROGRESS' | 'DONE';

// Still type-safe, but no enum object at runtime
const status: TaskStatus = 'OPEN'; // ✅ Valid
const invalid: TaskStatus = 'INVALID'; // ❌ Compile error

// You can still get all values (requires manual array)
export const TASK_STATUSES: TaskStatus[] = ['OPEN', 'IN_PROGRESS', 'DONE'];
```

| Practice | Why |

|----------|-----|

| Use enums for constant values | Type-safe, autocomplete support |

| Define enums in separate files | Reusable across the application |

| Use enum type in entities | Database-level constraint |

| Add @IsEnum() in DTOs | Validation for API inputs |

| Use consistent casing | Avoids confusion (OPEN vs open vs Open) |

| Create enum utilities | Helper functions for common operations |

**Sources:**

- [TypeScript Enums Documentation](https://www.typescriptlang.org/docs/handbook/enums.html)

- [NestJS Validation with Enums](https://docs.nestjs.com/techniques/validation)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

### 3.7 Use Event-Driven Architecture for Loose Coupling

**Impact: HIGH (Reduces dependencies and enables scalability)**

When implementing or reviewing cross-module communication, **always** follow these steps:

**Pattern to check:** Look for multiple service dependencies that trigger side effects.

**If found:** Replace with event emission using EventEmitter2.

**Run in terminal:**

```bash
bun add @nestjs/event-emitter
```

**File:** `src/app.module.ts`

**File:** `src/users/events/user-registered.event.ts`

**File:** `src/users/users.service.ts`

**File:** `src/email/listeners/user.listener.ts`

**File:** `src/email/email.module.ts`

Use this checklist when reviewing or creating cross-module communication:

- [ ] Services don't inject other services just for side effects

- [ ] EventEmitter2 is configured in `app.module.ts`

- [ ] Events are defined as separate classes with types

- [ ] Events are emitted using `eventEmitter.emit()`

- [ ] Event listeners use `@OnEvent()` decorator

- [ ] Listeners are registered in their respective modules

- [ ] Event names use consistent naming convention (e.g., `module.action`)

**Incorrect:**

```typescript
// users.service.ts - Tight coupling 🚨
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private emailService: EmailService,      // ❌ Direct dependency
    private notificationService: NotificationService,  // ❌ Direct dependency
    private profileService: ProfileService,   // ❌ Direct dependency
    private auditService: AuditService,       // ❌ Direct dependency
    private analyticsService: AnalyticsService,  // ❌ Direct dependency
  ) {}

  async register(data: RegisterDto) {
    const user = await this.prisma.user.create({ data });

    // ❌ Five dependencies just for side effects!
    await this.emailService.sendVerification(user.email);
    await this.notificationService.sendPush(user.id, 'Welcome!');
    await this.profileService.createDefault(user.id);
    await this.auditService.log('USER_REGISTERED', { userId: user.id });
    await this.analyticsService.track('user_registered', { userId: user.id });

    // ❌ Hard to test - need to mock all 5 services
    // ❌ Hard to maintain - adding new feature requires modifying UsersService
    // ❌ Errors cascade - if email fails, everything fails
    // ❌ Hard to scale - all side effects are synchronous
  }

  async deleteUser(userId: string) {
    await this.prisma.user.delete({ where: { id: userId } });

    // ❌ Direct calls everywhere
    await this.notificationService.clearUserNotifications(userId);
    await this.profileService.delete(userId);
    await this.analyticsService.deleteUserData(userId);
  }
}
```

**Correct:**

```typescript
// users.service.spec.ts ✅
import { EventEmitter2 } from '@nestjs/event-emitter';

describe('UsersService', () => {
  let service: UsersService;
  let eventEmitter: EventEmitter2;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: PrismaService,
          useValue: { user: { create: jest.fn() } },
        },
        {
          provide: EventEmitter2,
          useValue: { emit: jest.fn() },
        },
      ],
    }).compile();

    service = module.get(UsersService);
    eventEmitter = module.get(EventEmitter2);
  });

  it('should emit user.registered event on registration', async () => {
    const mockUser = { id: '1', email: 'test@example.com' };
    jest.spyOn(service['prisma'].user, 'create').mockResolvedValue(mockUser);

    await service.register({ email: 'test@example.com' });

    expect(eventEmitter.emit).toHaveBeenCalledWith(
      'user.registered',
      expect.any(UserRegisteredEvent)
    );
  });
});
```

| Practice | Why |

|----------|-----|

| Use events for cross-module communication | Loose coupling, easier to test |

| Define event classes | Type safety, self-documenting |

| Use consistent naming | `module.action` pattern (e.g., `user.registered`) |

| Handle errors in listeners | Don't let one listener fail all |

| Use async listeners | Don't block main operation |

| Version events | Maintain backwards compatibility |

| Use sagas for workflows | Complex multi-step operations |

**Sources:**

- [EventEmitter2 | NestJS - Official Documentation](https://docs.nestjs.com/techniques/events)

- [Event-Driven Architecture | Martin Fowler](https://martinfowler.com/articles/201701-event-driven.html)

- [Saga Pattern | Microservices.io](https://microservices.io/patterns/data/saga.html)

---

## 4. Section 4

**Impact: CRITICAL**

### 4.1 Enable Global Exception Filter

**Impact: CRITICAL (Prevents stack trace leaks in production)**

Default Express errors leak stack traces and database info to clients. Global filters catch all exceptions and return safe HTTP responses. **Hide internal errors from users.**

> **Hint**: Use global exception filters to standardize error responses, log errors properly, and prevent sensitive information leaks. Different responses for development vs production environments.

**Without global filters:**

```json
// 🚨 Production response - LEAKS sensitive info!
{
  "statusCode": 500,
  "message": "select * from users where id = $1 - relation \"users\" does not exist",
  "stack": "Error: relation \"users\" does not exist\n    at Connection.parseE (/app/node_modules/pg/lib/connection.js:539:11)\n    at /app/src/users/users.service.ts:42:15\n    at processTicksAndRejections (internal/process/task_queues.js:95:5)"
}
```

**With global filters:**

```json
// ✅ Production response - Safe!
{
  "statusCode": 500,
  "message": "Internal server error",
  "error": "INTERNAL_SERVER_ERROR",
  "timestamp": "2026-01-20T12:34:56.789Z",
  "path": "/api/users/123"
}
```

**Incorrect:**

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}

// Service throws raw errors
@Injectable()
export class UsersService {
  async findOne(id: string) {
    const user = await this.repository.findOne(id);
    if (!user) {
      // 🚨 Throws raw Error - leaks database info
      throw new Error(`User ${id} not found in database`);
    }
    return user;
  }
}
```

**Correct:**

```typescript
// common/filters/all-exceptions.filter.ts
import { LoggerService } from '../services/logger.service';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  constructor(
    private configService: ConfigService,
    private loggerService: LoggerService,
  ) {}

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getResponse();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    // ✅ Log to external service (Sentry, DataDog, etc.)
    this.loggerService.logError({
      status,
      path: request.url,
      method: request.method,
      exception,
      userId: request.user?.id,
      correlationId: request.headers['x-correlation-id'],
    });

    const errorResponse = this.buildErrorResponse(exception, request);
    response.status(status).json(errorResponse);
  }
}
```

Create domain-specific exceptions for better error handling:

Handle HTTP exceptions specifically:

Handle database-specific errors safely:

Use multiple filters for different exception types:

Better approach using dependency injection:

Define a consistent error response structure:

Integrate with external logging services:

| Practice | Description |

|----------|-------------|

| Hide stack traces in production | Never expose internal implementation details |

| Log everything | Always log errors server-side for debugging |

| Use environment-aware responses | Show details in dev, hide in prod |

| Create custom exceptions | Use domain-specific exceptions for business logic |

| Standardize error format | Consistent response structure across all endpoints |

| Handle database errors | Map DB errors to safe HTTP responses |

| Use correlation IDs | Track requests through distributed systems |

**Sources:**

- [Exception Filters | NestJS - Official Documentation](https://docs.nestjs.com/exception-filters)

- [Built-in HTTP exceptions | NestJS](https://docs.nestjs.com/exception-filters#built-in-http-exceptions)

- [Exceptions | NestJS](https://docs.nestjs.com/throw-exceptions)

- [Error Handling Best Practices | OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

### 4.2 Implement Proper Logging Strategy

**Impact: HIGH (Enables debugging, monitoring, and audit trails)**

> **Note:** For NestJS Logger with module context patterns, see `error-handling-logger-context.md`. This rule focuses on Winston and structured JSON logging for production environments.

Console.log lacks structure, levels, and persistence. NestJS Logger with Winston provides structured JSON logs for production monitoring. **Log all errors, warnings, and business events.**

**Incorrect: console.log debugging**

```typescript
// users.service.ts - No structure 🚨
console.log('Creating user:', data);
try {
  const user = await this.prisma.user.create({ data });
  console.log('User created:', user.id);
} catch (error) {
  console.error('User creation failed:', error);
}
```

**Correct: structured logging**

```typescript
// logger.service.ts
import { LoggerService } from '@nestjs/common';
import * as winston from 'winston';

@Injectable()
export class WinstonLogger implements LoggerService {
  private logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
      winston.format.timestamp(),
      winston.format.json()
    ),
    transports: [
      new winston.transports.Console(),
      new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    ],
  });
}

// users.service.ts
import { Logger } from '@nestjs/common';

@Injectable()
export class UsersService {
  private readonly logger = new Logger(UsersService.name);

  async createUser(data: CreateUserDto) {
    this.logger.log(`Creating user for email: ${data.email}`, 'UsersService');
    
    try {
      const user = await this.prisma.user.create({ data });
      this.logger.log(`User created successfully: ${user.id}`);
      return user;
    } catch (error) {
      this.logger.error(`Failed to create user ${data.email}: ${error.message}`, error.stack);
      throw error;
    }
  }
}
```

### 4.3 Use Logger with Module Context for Debugging

**Impact: MEDIUM (Improves debugging with contextual log messages)**

When implementing or reviewing logging, **always** follow these steps:

**Pattern to check:** Look for `console.log()`, `console.error()`, or Logger without context parameter.

**If found:** Replace with contextual Logger.

**Incorrect:**

```typescript
// tasks/tasks.service.ts - Console logging 🚨
import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksService {
  constructor(private tasksRepository: TasksRepository) {}

  // ❌ Console.log - no context, no levels
  async createTask(dto: CreateTaskDto, user: User) {
    console.log('Creating task'); // ❌ No module context
    const task = await this.tasksRepository.create(dto, user);
    console.log('Task created:', task); // ❌ No structure
    return task;
  }

  // ❌ Console.error for errors
  async deleteTask(id: string) {
    try {
      return await this.tasksRepository.delete(id);
    } catch (error) {
      console.error('Error deleting task:', error); // ❌ No context
      throw error;
    }
  }

  // ❌ No logging at all
  async updateTask(id: string, dto: UpdateTaskDto) {
    return this.tasksRepository.update(id, dto); // ❌ Silent operation
  }
}

// tasks/tasks.controller.ts - No logging 🚨
import { Controller, Get, Post, Body } from '@nestjs/common';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto) {
    // ❌ No logging - hard to debug in production
    return this.tasksService.findAll(filterDto);
  }

  @Post()
  create(@Body() dto: CreateTaskDto) {
    // ❌ No audit trail
    return this.tasksService.create(dto);
  }
}
```

**Correct:**

```typescript
// ✅ Add request ID to all logs in a request
// common/middleware/request-id.middleware.ts
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  private logger = new Logger(RequestIdMiddleware.name);

  use(req: Request, res: Response, next: NextFunction) {
    const id = uuidv4();
    req['id'] = id;

    // ✅ Add request ID to response header
    res.setHeader('X-Request-ID', id);

    this.logger.verbose(`[${id}] ${req.method} ${req.url}`);

    next();
  }
}

// tasks/tasks.service.ts - Use request ID ✅
import { Injectable, Logger, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.REQUEST })
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  constructor(@Inject(REQUEST) private request: Request) {
    // ✅ Use request ID in logs
    const requestId = request['id'];
    if (requestId) {
      this.logger.setContext(`[${requestId}] ${TasksService.name}`);
    }
  }

  findAll() {
    this.logger.log('Retrieving all tasks');
    // Output: [abc-123] [TasksService] Retrieving all tasks
    return this.tasksRepository.findAll();
  }
}
```

| Practice | Why |

|----------|-----|

| Use `Logger(Class.name)` | Context prefix in every log message |

| Log at appropriate levels | Control verbosity by environment |

| Log important business events | Audit trail for debugging |

| Log errors with stack traces | Easier debugging in production |

| Use verbose for debugging | Disabled by default, enabled when needed |

| Log user actions | Security audit trail |

**Sources:**

- [NestJS Logger Documentation](https://docs.nestjs.com/techniques/logger)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

**See also:** `error-handling-structured-logging.md` for Winston/structured logging in production.

---

## 5. Section 5

**Impact: MEDIUM**

### 5.1 Create Custom Pipes for Query Parameter Transformation

**Impact: MEDIUM (Ensures type safety and reduces boilerplate)**

When implementing or reviewing query parameter handling, **always** follow these steps:

**Pattern to check:** Look for `parseInt()`, `Number()`, `Boolean()`, or string operations in controllers.

**If found:** Create custom pipes to handle the conversion.

**File:** `src/common/pipes/parse-int.pipe.ts`

**File:** `src/common/pipes/trim.pipe.ts`

**File:** `src/common/pipes/parse-boolean.pipe.ts`

Use this checklist when reviewing or creating query parameter handling:

- [ ] No manual `parseInt()` or `Number()` in controllers

- [ ] No manual `toLowerCase()` or `trim()` in controllers

- [ ] All numeric query params use `ParseIntPipe` or `ParseFloatPipe`

- [ ] All boolean query params use `ParseBooleanPipe`

- [ ] All string params use `TrimPipe` if whitespace matters

- [ ] Optional params use `optional: true` pipe option

- [ ] Error messages from pipes are user-friendly

**Incorrect:**

```typescript
// users.controller.ts - Manual type conversion 🚨
@Controller('users')
export class UsersController {
  @Get()
  async findAll(@Query() query: any) {
    // ❌ Manual parsing - error-prone
    const page = parseInt(query.page as string, 10) || 1;
    const limit = parseInt(query.limit as string, 10) || 10;

    // ❌ Manual boolean conversion
    const active = query.active === 'true' || query.active === '1';

    // ❌ Manual trimming
    const search = query.search ? (query.search as string).trim() : undefined;

    // ❌ No validation - NaN possible
    if (isNaN(page) || isNaN(limit)) {
      throw new BadRequestException('Invalid page or limit');
    }

    return this.usersService.findAll({ page, limit, active, search });
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    // ❌ Manual integer conversion
    const userId = parseInt(id, 10);
    if (isNaN(userId)) {
      throw new BadRequestException('Invalid user ID');
    }
    return this.usersService.findOne(userId);
  }
}
```

**Correct:**

```typescript
// common/pipes/parse-int.pipe.spec.ts ✅
import { ParseIntPipe } from './parse-int.pipe';
import { BadRequestException } from '@nestjs/common';

describe('ParseIntPipe', () => {
  let pipe: ParseIntPipe;

  beforeEach(() => {
    pipe = new ParseIntPipe();
  });

  it('should parse valid integer string', () => {
    const result = pipe.transform('42', { type: 'query', data: 'page' } as any);
    expect(result).toBe(42);
  });

  it('should throw for invalid string', () => {
    expect(() => pipe.transform('abc', { type: 'query', data: 'page' } as any))
      .toThrow(BadRequestException);
  });

  it('should return undefined for optional empty value', () => {
    const optionalPipe = new ParseIntPipe({ optional: true });
    const result = optionalPipe.transform('', { type: 'query', data: 'page' } as any);
    expect(result).toBeUndefined();
  });

  it('should enforce min value', () => {
    const pipeWithMin = new ParseIntPipe({ minValue: 1 });
    expect(() => pipeWithMin.transform('0', { type: 'query', data: 'page' } as any))
      .toThrow(BadRequestException);
  });

  it('should enforce max value', () => {
    const pipeWithMax = new ParseIntPipe({ maxValue: 100 });
    expect(() => pipeWithMax.transform('101', { type: 'query', data: 'page' } as any))
      .toThrow(BadRequestException);
  });
});
```

| Practice | Why |

|----------|-----|

| Use pipes for conversion | Consistent transformation, reusable |

| Make pipes reusable | Add optional/min/max options |

| Return user-friendly errors | Help API consumers fix their requests |

| Use `DefaultValuePipe` | Set sensible defaults |

| Combine pipes | Chain multiple transformations |

| Test pipes independently | Ensure reliability |

**Sources:**

- [Pipes | NestJS - Official Documentation](https://docs.nestjs.com/pipes)

- [Custom Pipes | NestJS Documentation](https://docs.nestjs.com/techniques/validation)

- [Query String Params | MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams)

### 5.2 Use Filter DTOs for Query Parameter Validation

**Impact: HIGH (Validates and type-checks query parameters)**

When implementing or reviewing query parameter handling, **always** follow these steps:

**Pattern to check:** Look for `@Query()` decorators with parameter names, manual string parsing, or optional chaining.

**If found:** Replace with filter DTO.

**File:** `tasks/dto/get-tasks-filter.dto.ts`

**Incorrect:**

```typescript
// tasks/tasks.controller.ts - Individual parameters 🚨
import { Controller, Get, Query } from '@nestjs/common';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(
    @Query('status') status: string,        // ❌ No validation
    @Query('search') search: string,        // ❌ No validation
    @Query('page') page: string,            // ❌ String, not number
    @Query('limit') limit: string,          // ❌ String, not number
  ) {
    // ❌ Manual type conversion
    const pageNum = parseInt(page) || 1;
    const limitNum = parseInt(limit) || 10;

    // ❌ No type safety - status could be "INVALID"
    return this.tasksService.getTasks(status, search, pageNum, limitNum);
  }

  @Get()
  findAll(@Query() query: any) {
    // ❌ No type safety at all
    const status = query.status as string;
    const page = parseInt(query.page) || 1;
    const limit = parseInt(query.limit) || 10;
    const search = query.search;

    return this.tasksService.getTasks(status, search, page, limit);
  }
}

// tasks/tasks.service.ts 🚨
@Injectable()
export class TasksService {
  // ❌ Too many parameters, no type safety
  async getTasks(
    status: string | undefined,
    search: string | undefined,
    page: number,
    limit: number,
  ) {
    // ❌ What values are valid for status? No hints.
    const query = this.repo.createQueryBuilder('task');

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    query.skip((page - 1) * limit).take(limit);

    return query.getMany();
  }
}
```

**Correct:**

```typescript
// ✅ Different validation for different scenarios
// tasks/dto/get-tasks-filter.dto.ts
import { ValidateIf } from 'class-validator';

export class GetTasksFilterDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  // ✅ Only validate if search is present
  @IsOptional()
  @IsString()
  @MinLength(3, { message: 'Search must be at least 3 characters' })
  search?: string;

  // ✅ Validate 'from' only if 'to' is also present
  @IsOptional()
  @ValidateIf((o) => o.to !== undefined)
  @IsDate()
  from?: Date;

  @IsOptional()
  @ValidateIf((o) => o.from !== undefined)
  @IsDate()
  to?: Date;
}
```

| Practice | Why |

|----------|-----|

| Use filter DTOs | Single validated parameter |

| Add @Type() decorator | Auto-transform strings to numbers/dates |

| Use @IsOptional() | Parameters are optional by default |

| Add default values | Cleaner code with default pagination |

| Create reusable base DTOs | DRY principle for common filters |

| Extend base DTOs | Composable filter combinations |

**Sources:**

- [NestJS Query Parameters Documentation](https://docs.nestjs.com/controllers#query-parameters)

- [class-validator Documentation](https://github.com/typestack/class-validator)

- [class-transformer Documentation](https://github.com/typestack/class-transformer)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

### 5.3 Validate All Inputs with DTOs and ValidationPipe

**Impact: CRITICAL (Prevents invalid data and injection attacks)**

Unvalidated inputs lead to runtime errors, SQL injection, and security vulnerabilities. Global ValidationPipe ensures every DTO is validated before reaching controllers. **Never trust client data.**

**Incorrect:**

```typescript
// main.ts - Missing ValidationPipe
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);  // No global pipe!
}

// users.controller.ts - No validation
@Post()
create(@Body() createUserDto: any) {
  // Any data can be passed - vulnerable!
  return this.usersService.create(createUserDto);
}

// dto/create-user.dto.ts - No decorators
export class CreateUserDto {
  email: string;      // No validation
  password: string;   // No validation
  age: number;        // No validation
}
```

**Correct:**

```json
{
  "statusCode": 400,
  "message": [
    "email must be an email",
    "password must be longer than or equal to 8 characters",
    "password must contain uppercase, lowercase, and number",
    "age must not be less than 18"
  ],
  "error": "Bad Request"
}
```

| Option | What It Does | Always Use? |

|--------|--------------|------------|

| `whitelist: true` | Removes properties not in DTO | ✅ Yes |

| `forbidNonWhitelisted: true` | Throws error if extra properties sent | ✅ Yes (security) |

| `transform: true` | Converts plain objects to DTO instances | ✅ Yes (type safety) |

| `disableErrorMessages: false` | Shows detailed validation errors | ✅ Yes (debugging) |

| `transformOptions.enableImplicitConversion: true` | Auto-converts strings to types | ✅ Yes (convenience) |

> **Note:** For query parameter validation with filter DTOs, see `validation-filter-dtos.md`.

For business-specific validation rules:

**Sources:**

- [NestJS Validation Documentation](https://docs.nestjs.com/techniques/validation)

- [class-validator Documentation](https://github.com/typestack/class-validator)

- [class-transformer Documentation](https://github.com/typestack/class-transformer)

---

## 6. Section 6

**Impact: CRITICAL**

### 6.1 Use Custom Repository Pattern for Database Logic Encapsulation

**Impact: HIGH (Separates concerns and improves testability)**

When implementing or reviewing database operations, **always** follow these steps:

**Pattern to check:** Look for `@InjectRepository()`, query builders, or database methods (find, save, update, delete) in service files.

**If found:** Extract to custom repository.

**File:** `tasks/tasks.repository.ts`

**File:** `tasks/tasks.module.ts`

**File:** `tasks/tasks.service.ts`

**Incorrect:**

```typescript
// tasks/tasks.service.ts - Database logic in service 🚨
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Task } from './task.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';

@Injectable()
export class TasksService {
  constructor(
    @InjectRepository(Task) // ❌ Direct repository injection
    private repo: Repository<Task>
  ) {}

  async getTasks(filterDto: GetTasksFilterDto, user: User) {
    const { status, search } = filterDto;

    // ❌ Database query logic in service
    const query = this.repo.createQueryBuilder('task');
    query.where({ user });

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    return await query.getMany();
  }

  async findOne(id: string, user: User) {
    // ❌ Repeated query logic
    return this.repo.findOne({ where: { id, user } });
  }

  async create(dto: CreateTaskDto, user: User) {
    // ❌ Mixed business and data logic
    const task = this.repo.create({ ...dto, user });
    return this.repo.save(task);
  }

  async findOverdue(user: User) {
    // ❌ Complex query in service - hard to test
    return this.repo
      .createQueryBuilder('task')
      .where('task.user = :user', { user })
      .andWhere('task.dueDate < :now', { now: new Date() })
      .andWhere('task.status != :status', { status: TaskStatus.DONE })
      .getMany();
  }
}
```

**Correct:**

```typescript
// For TypeORM >= 0.3, @EntityRepository() decorator is deprecated
// Use dataSource-based approach:

// tasks/repositories/tasks.repository.ts ✅
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, Repository } from 'typeorm';
import { Task } from '../entities/task.entity';

@Injectable()
export class TasksRepository {
  private get repo(): Repository<Task> {
    return this.dataSource.getRepository(Task);
  }

  constructor(@InjectDataSource() private dataSource: DataSource) {}

  async getTasks(user: User): Promise<Task[]> {
    return this.repo.find({ where: { user } });
  }

  async findOne(id: string, user: User): Promise<Task> {
    const task = await this.repo.findOne({ where: { id, user } });
    if (!task) {
      throw new NotFoundException();
    }
    return task;
  }
}

// Or use the new TypeOrmEx decorator approach:
// common/decorators/typeorm-ex.decorator.ts ✅
import { DataSource } from 'typeorm';
import { TYPEORM_EX_DATA_SOURCE } from './typeorm-ex.constants';

export const TypeormExRepository = <T>(entity: Type<any>) =>
  InjectDataSource(TYPEORM_EX_DATA_SOURCE);

// tasks/repositories/tasks.repository.ts
@Injectable()
export class TasksRepository {
  constructor(
    @TypeormExRepository(Task)
    private dataSource: DataSource,
  ) {
    // Use dataSource.getRepository(Task)
  }
}
```

| Practice | Why |

|----------|-----|

| Create custom repositories | Separates data access from business logic |

| Extend TypeORM Repository | Reuse base CRUD methods |

| Put complex queries in repository | Single responsibility, easier testing |

| Keep services clean | Focus on business rules only |

| Inject repository into service | Proper dependency injection |

| Test repositories independently | Isolated data layer testing |

**Sources:**

- [TypeORM Custom Repositories](https://typeorm.io/#/custom-repository)

- [NestJS TypeORM Documentation](https://docs.nestjs.com/techniques/database)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

### 6.2 Use Parameterized Queries to Prevent SQL Injection

**Impact: CRITICAL (Eliminates SQL injection vulnerabilities)**

When implementing or reviewing database queries, **always** follow these steps:

**Pattern to check:** Look for `$queryRaw`, `$executeRaw`, or `sql` template tag usage.

**If found:** Replace with Prisma v7 `sql` template tag or typed queries.

**File:** Any service using Prisma

**Prisma v7 transaction pattern:**

```bash
bun add @prisma/client @prisma/adapter-pg
bun add -D prisma
```

**File:** `src/database/prisma.service.ts` or similar

Use this checklist when reviewing or creating database queries:

- [ ] No string concatenation in SQL queries

- [ ] All `$queryRaw` uses template literals with variables

- [ ] All `$executeRaw` uses template literals with variables

- [ ] Prisma v7 `sql` template tag imported when needed

- [ ] Transactions use async callback pattern

- [ ] Client extensions use `$extends()` method

- [ ] User input never interpolated directly into SQL

**Incorrect:**

```typescript
// users.service.ts - DANGEROUS 🚨

import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  // ❌ String concatenation - SQL INJECTION
  async findByName(name: string) {
    const query = `SELECT * FROM users WHERE name = '${name}'`;
    return this.prisma.$queryRawUnsafe(query);
  }

  // ❌ Template literal concatenation - VULNERABLE
  async findByEmailAndPassword(email: string, password: string) {
    const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
    return this.prisma.$executeRawUnsafe(query);
  }

  // ❌ Direct interpolation - VULNERABLE
  async searchUsers(searchTerm: string) {
    return this.prisma.$queryRaw(
      `SELECT * FROM users WHERE name LIKE '%${searchTerm}%'`
    );
  }

  // ❌ Old Prisma syntax (pre-v7)
  async oldTransactionPattern(userData: any, postData: any) {
    return this.prisma.$transaction([
      this.prisma.user.create({ data: userData }),
      this.prisma.post.create({ data: postData }),
    ]);
  }
}
```

**Correct:**

```typescript
// Extended client with custom methods
const prisma = new PrismaClient().$extends({
  model: {
    user: {
      async findByEmail(email: string) {
        return prisma.user.findUnique({ where: { email } });
      },
      async findActive() {
        return prisma.user.findMany({ where: { status: 'ACTIVE' } });
      },
    },
    order: {
      async calculateTotal(orderId: string) {
        const items = await prisma.orderItem.findMany({
          where: { orderId },
        });
        return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    },
  },
});

// Usage
const user = await prisma.user.findByEmail('user@example.com');
const total = await prisma.order.calculateTotal('order-123');
```

| Practice | Why |

|----------|-----|

| Use typed queries | Type-safe, auto-parameterized |

| Avoid raw queries when possible | Prisma handles security automatically |

| Use `sql` template tag | Auto-parameterizes variables |

| Never concatenate strings | Prevents SQL injection |

| Use interactive transactions | Better error handling in v7 |

| Use client extensions | Reusable query patterns |

**Sources:**

- [Prisma v7 Release Notes](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)

- [Raw Database Queries | Prisma Documentation](https://www.prisma.io/docs/orm/prisma-client/queries/raw-database-access)

- [Transactions | Prisma Documentation](https://www.prisma.io/docs/orm/prisma-client/transactions)

- [SQL Injection | OWASP](https://owasp.org/www-community/attacks/SQL_Injection)

---

## 7. Section 7

**Impact: HIGH**

### 7.1 Use Bun's Built-in Crypto for Secure Password Hashing

**Impact: CRITICAL (Prevents password leak breaches)**

When implementing or reviewing password handling, **always** follow these steps:

**Pattern to check:** Look for passwords being stored directly or hashed with weak algorithms.

**If found:** Replace with Bun's `Crypto.password.hash()`.

**File:** `src/auth/password.service.ts`

**File:** `src/auth/dto/register.dto.ts`

Use this checklist when reviewing or creating password handling:

- [ ] Passwords are never stored in plain text

- [ ] Passwords are hashed with `Bun.password.hash()`

- [ ] Passwords are verified with `Bun.password.verify()`

- [ ] Passwords have minimum length requirement (12+ characters)

- [ ] Passwords require mixed case, numbers, special characters

- [ ] Database column for hashed password is `TEXT` or `VARCHAR(255)`

- [ ] Error messages don't reveal if user exists

**Incorrect:**

```typescript
// auth/auth.service.ts - Insecure 🚨
import { Injectable } from '@nestjs/common';
import { createHash, randomBytes } from 'crypto';

@Injectable()
export class AuthService {
  // ❌ Plain text storage
  async register(email: string, password: string) {
    return this.prisma.user.create({
      data: { email, password },  // ❌ Stored as-is!
    });
  }

  // ❌ Fast hash (SHA256, MD5) - crackable with GPUs
  async hashPassword(password: string) {
    return createHash('sha256').update(password).digest('hex');
  }

  // ❌ Manual salt - still vulnerable to GPU cracking
  async hashWithSalt(password: string) {
    const salt = randomBytes(16).toString('hex');
    const hash = createHash('sha512')
      .update(password + salt)
      .digest('hex');
    return `${salt}:${hash}`;
  }

  // ❌ Timing-sensitive string comparison
  async verifyPassword(password: string, hash: string) {
    const [salt, originalHash] = hash.split(':');
    const computedHash = createHash('sha512')
      .update(password + salt)
      .digest('hex');
    return computedHash === originalHash;  // ❌ Timing attack vulnerable
  }

  // ❌ Weak password requirements
  @MinLength(6)  // ❌ Too short!
  password: string;
}
```

**Correct:**

```typescript
// ✅ Recommended for new applications
async hash(password: string) {
  return Bun.password.hash(password);  // Uses argon2id by default
}

// Or explicitly
async hash(password: string) {
  return Bun.password.hash(password, {
    algorithm: 'argon2id',
    memoryCost: 16,  // MB of memory (higher = more GPU-resistant)
    timeCost: 2,     // Number of iterations
  });
}
```

Bun's password hashing supports both algorithms at runtime. The algorithm choice is stored in the hash prefix, so `verify()` auto-detects which algorithm was used.

**Use argon2id when:**

```typescript
// ✅ For legacy compatibility or cross-platform needs
async hash(password: string) {
  return Bun.password.hash(password, {
    algorithm: 'bcrypt',
    cost: 12,  // Work factor (2^12 iterations)
  });
}
```

- Starting a new application (recommended default)

- Maximum security against GPU/ASIC attacks is required

- Memory-hard hashing is acceptable

- Compliance requirements mandate modern algorithms

**Use bcrypt when:**

```typescript
// auth/auth.service.ts ✅
@Injectable()
export class AuthService {
  async login(dto: LoginDto) {
    const user = await this.prisma.user.findUnique({
      where: { email: dto.email },
    });

    const isValid = user
      ? await this.passwordService.verify(dto.password, user.password)
      : false;

    // ✅ Log failed attempts (but not passwords!)
    if (!isValid) {
      await this.auditService.log({
        event: 'LOGIN_FAILED',
        email: dto.email,
        ip: dto.ip,
        userAgent: dto.userAgent,
      });
    }

    // ... rest of logic
  }
}
```

- Migrating from existing bcrypt hashes

- Need compatibility with older systems/libraries

- Memory constraints prevent argon2 usage

- Regulatory requirements specifically mandate bcrypt

Bun stores the algorithm in the hash prefix, enabling seamless migration:

| Practice | Why |

|----------|-----|

| Use `Bun.password.hash()` | Argon2/bcrypt with runtime algorithm selection |

| Use `Bun.password.verify()` | Auto-detects algorithm, timing-safe comparison |

| Prefer argon2 for new apps | Memory-hard, GPU-resistant, modern standard |

| Use bcrypt for compatibility | Legacy systems, cross-platform needs |

| Configure algorithm at runtime | Environment-specific, flexible migration |

| Enforce strong passwords | Prevents brute force attacks |

| Generic error messages | Prevents user enumeration |

| Never log passwords | Logs can be compromised |

| Rehash on algorithm upgrade | Seamless migration between algorithms |

| Rate limit auth endpoints | Prevents brute force attacks |

**Sources:**

- [Bun Crypto Documentation](https://bun.sh/docs/api/crypto)

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

- [Argon2 RFC](https://datatracker.ietf.org/doc/html/rfc9106)

### 7.2 Use Custom Decorators for Type-Safe Request Data Access

**Impact: HIGH (Improves type safety and reduces boilerplate)**

When implementing or reviewing request data access, **always** follow these steps:

**Pattern to check:** Look for direct access to `req.user`, `req.headers`, type assertions, or manual data extraction.

**If found:** Replace with custom decorators.

**File:** `src/auth/decorators/get-user.decorator.ts`

For accessing specific user properties:

**Incorrect:**

```typescript
// tasks/tasks.controller.ts - Verbose and unsafe 🚨
import { Controller, Get, Req, Request } from '@nestjs/common';
import { TasksService } from './tasks.service';

@Controller('tasks')
export class TasksController {
  constructor(private tasksService: TasksService) {}

  // ❌ Manual extraction with type assertion
  @Get()
  findAll(@Req() req: Request) {
    const user = req.user as any; // ❌ Type assertion unsafe
    return this.tasksService.getTasks(user.id);
  }

  // ❌ Verbose, repeated extraction logic
  @Get(':id')
  findOne(@Param('id') id: string, @Req() req: Request) {
    const user = req.user as User; // ❌ Repeated in every method
    return this.tasksService.findOne(id, user.id);
  }

  // ❌ Type assertion everywhere
  @Post()
  create(@Body() dto: CreateTaskDto, @Req() req: Request) {
    const user = req.user as User;
    return this.tasksService.create(dto, user.id);
  }

  // ❌ No autocomplete, no type safety
  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateTaskDto,
    @Req() req: Request,
  ) {
    const user = req.user as User;
    // Does user.id exist? TypeScript doesn't know
    return this.tasksService.update(id, dto, user.id);
  }
}
```

**Correct:**

```typescript
// auth/decorators/get-user.decorator.spec.ts ✅
import { GetUser } from './get-user.decorator';
import { ExecutionContext } from '@nestjs/common';

describe('GetUser Decorator', () => {
  it('should extract user from request', () => {
    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => ({
          user: { id: '123', email: 'test@example.com' },
        }),
      }),
    } as unknown as ExecutionContext;

    const result = GetUser(null, mockContext);

    expect(result).toEqual({ id: '123', email: 'test@example.com' });
  });

  it('should extract specific property from user', () => {
    const mockContext = {
      switchToHttp: () => ({
        getRequest: () => ({
          user: { id: '123', email: 'test@example.com' },
        }),
      }),
    } as unknown as ExecutionContext;

    const result = GetUser('email', mockContext);

    expect(result).toBe('test@example.com');
  });
});
```

| Practice | Why |

|----------|-----|

| Use `@GetUser()` decorator | Type-safe user access with autocomplete |

| Create decorators for repeated extractions | Eliminates boilerplate code |

| Use property selection for single fields | Cleaner code when only one field needed |

| Create decorators for headers, IP, tokens | Consistent request data access |

| Type your decorators with User entity | Full TypeScript support |

| Test decorators independently | Ensures reliable extraction |

**Sources:**

- [NestJS Custom Decorators Documentation](https://docs.nestjs.com/custom-decorators)

- [NestJS Execution Context Documentation](https://docs.nestjs.com/fundamentals/execution-context)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

### 7.3 Use Guards for Route Protection

**Impact: CRITICAL (Enforces authentication/authorization per route)**

When implementing or reviewing security, **always** follow these steps:

**Files to create/modify:**

```typescript
// ✅ REQUIRED: Global guard registration
import { APP_GUARD } from '@nestjs/core';

@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: JwtAuthGuard,  // ✅ Global authentication
    },
  ],
})
export class AppModule {}
```

- `src/auth/guards/jwt-auth.guard.ts`

- `src/auth/guards/jwt-auth.guard.spec.ts`

- `src/auth/decorators/public.decorator.ts`

- `src/app.module.ts` (for APP_GUARD)

**File:** `src/auth/decorators/public.decorator.ts`

**File:** `src/app.module.ts`

**Pattern to check:**

```bash
bun add @nestjs/jwt @nestjs/passport passport passport-jwt
bun add -D @types/passport-jwt
```

Use this checklist when reviewing or creating endpoints:

- [ ] Global authentication guard registered in `app.module.ts`

- [ ] `@Public()` decorator exists for public routes

- [ ] Controllers don't use `any` type for `@Req()` user

- [ ] Admin routes have `@Roles('admin')` guard

- [ ] Resource owner checks implemented (users can only access their own data)

- [ ] Rate limiting applied to auth endpoints

- [ ] Guards use `Reflector` to check metadata

**Incorrect:**

```typescript
// users.controller.ts - All routes exposed 🚨
@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    return this.usersService.findAll();  // 🚨 Publicly accessible!
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);  // 🚨 Anyone can view any user!
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.usersService.remove(id);  // 🚨 Anyone can delete users!
  }
}
```

**Correct:**

```typescript
// First install: bun add @nestjs/throttler

// app.module.ts
import { ThrottlerModule } from '@nestjs/throttler';

@Module({
  imports: [
    ThrottlerModule.forRoot([{
      ttl: 60000,      // 1 minute
      limit: 5,        // 5 requests per minute
    }]),
  ],
})
export class AppModule {}

// auth/auth.controller.ts
import { Throttle } from '@nestjs/throttler';

@Controller('auth')
export class AuthController {
  @Post('login')
  @Throttle({ default: { limit: 5, ttl: 60000 } })  // ✅ Stricter for login
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }

  @Post('register')
  @Throttle({ default: { limit: 3, ttl: 3600000 } })  // ✅ 3 per hour
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }
}
```

| Practice | Description |

|----------|-------------|

| Use global guards | Default-deny security with explicit public routes |

| Separate auth from authorization | Different guards for authentication vs authorization |

| Use decorators | Custom decorators improve code readability |

| Check resource ownership | Users can only access their own resources |

| Combine guards | Chain multiple guards for comprehensive security |

| Rate limit auth endpoints | Prevent brute force attacks |

**Sources:**

- [Guards | NestJS - Official Documentation](https://docs.nestjs.com/guards)

- [Authentication | NestJS - Official Documentation](https://docs.nestjs.com/security/authentication)

- [Authorization | NestJS - Official Documentation](https://docs.nestjs.com/security/authorization)

- [Throttler | NestJS Documentation](https://docs.nestjs.com/security/rate-limiting)

---

## 8. Section 8

**Impact: HIGH**

### 8.1 Generate Swagger/OpenAPI Documentation

**Impact: MEDIUM (Enables automatic API documentation and client generation)**

Undocumented APIs force clients to guess endpoints and payloads. NestJS Swagger module auto-generates interactive OpenAPI docs from controllers. **All public APIs must be self-documenting.**

**Incorrect: no documentation**

```typescript
// users.controller.ts - Clients must guess schema 🚨
@Controller('users')
export class UsersController {
  @Post()
  create(@Body() data: any) {
    return this.usersService.create(data);
  }
}
```

**Correct: auto-generated docs**

```typescript
// main.ts
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  const config = new DocumentBuilder()
    .setTitle('Users API')
    .setDescription('User management endpoints')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
    
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);  // ✅ Interactive docs
  
  await app.listen(3000);
}

// users.controller.ts
@ApiTags('users')
@ApiBearerAuth()
@Controller('users')
export class UsersController {
  @Post()
  @ApiOperation({ summary: 'Create new user' })
  @ApiResponse({ status: 201, description: 'User created', type: UserDto })
  @ApiResponse({ status: 400, description: 'Invalid input' })
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }
}
```

### 8.2 Use Cursor-Based Pagination for Large Datasets

**Impact: HIGH (10-100x faster than offset for large datasets)**

When implementing or reviewing pagination, **always** follow these steps:

**Pattern to check:** Look for `skip`/`take` or `offset`/`limit` parameters.

**If found:** Replace offset pagination with cursor pagination.

**File:** `src/common/dto/pagination.dto.ts`

**File:** `src/users/users.service.ts`

**File:** `src/users/interfaces/paginated-result.interface.ts`

Use this checklist when reviewing or creating paginated endpoints:

- [ ] Pagination uses cursor-based approach (not offset/skip)

- [ ] Cursor is based on indexed column (usually `id` or `createdAt`)

- [ ] Response includes `hasNextPage`/`hasPreviousPage` flags

- [ ] Response includes `startCursor`/`endCursor` for navigation

- [ ] Fetches one extra item to determine if there's a next page

- [ ] Handles edge cases (first page, last page, empty results)

- [ ] Cursor is safely encoded/decoded (base64url recommended)

**Incorrect:**

```typescript
// dto/get-users.dto.ts - Offset pagination 🚨
export class GetUsersDto {
  @IsInt()
  @Min(1)
  page: number = 1;

  @IsInt()
  @Min(1)
  @Max(100)
  limit: number = 20;
}

// users.controller.ts - Offset based 🚨
@Controller('users')
export class UsersController {
  @Get()
  async findAll(@Query() dto: GetUsersDto) {
    return this.usersService.findAll(dto);
  }
}

// users.service.ts - OFFSET scans all rows 🚨
@Injectable()
export class UsersService {
  async findAll(dto: GetUsersDto) {
    const { page, limit } = dto;
    const skip = (page - 1) * limit;

    // Page 1000: scans 19,980 rows just to return 20!
    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        skip,  // ❌ Scans and discards rows
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.user.count(),
    ]);

    return {
      data: users,
      meta: {
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit),
      },
    };
  }
}

/* Performance issues:
 * Page 1:    ~1ms    (scans 0 rows)
 * Page 10:   ~5ms    (scans 180 rows)
 * Page 100:  ~50ms   (scans 1,980 rows)
 * Page 1000: ~500ms  (scans 19,980 rows)
 * Page 10000: ~5000ms (scans 199,980 rows)
 */
```

**Correct:**

```tsx
// components/UserInfiniteScroll.tsx
import { useEffect, useRef } from 'react';
import { useUsers } from '../hooks/useUsers';

export function UserInfiniteScroll() {
  const { users, hasNextPage, loadNext } = useUsers();
  const observerRef = useRef<IntersectionObserver>();

  const lastUserRef = (node: HTMLLIElement) => {
    if (observerRef.current) observerRef.current.disconnect();

    observerRef.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasNextPage) {
        loadNext();
      }
    });

    if (node) observerRef.current.observe(node);
  };

  return (
    <ul>
      {users.map((user, index) => (
        <li
          key={user.id}
          ref={index === users.length - 1 ? lastUserRef : undefined}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

| Aspect | Offset Pagination | Cursor Pagination |

|--------|------------------|-------------------|

| **Performance** | Degrades with page number | Consistent |

| **Deep pages** | Very slow (scans rows) | Same speed as page 1 |

| **Page jumping** | Easy (go to page 100) | Not supported |

| **Real-time updates** | Shows duplicate/missing items | Handles new items well |

| **Implementation** | Simple | More complex |

| **Use case** | Small datasets, admin panels | Infinite scroll, feeds |

**Use Cursor Pagination When:**

- Large datasets (>10,000 rows)

- Infinite scroll UI

- Real-time data feeds

- Mobile apps (better performance)

- Social media-style pagination

**Use Offset Pagination When:**

- Small datasets (<1,000 rows)

- Need page jumping (direct page access)

- Admin panels with pagination controls

- Static data that doesn't change often

**Sources:**

- [Pagination | Prisma Documentation](https://www.prisma.io/docs/concepts/components/prisma-client/pagination)

- [Relay Cursor Connections Specification](https://relay.dev/graphql/connections.htm)

- [PostgreSQL Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)

---

## 9. Section 9

**Impact: CRITICAL**

### 9.1 Never Hardcode Secrets - Use Environment Variables

**Impact: CRITICAL (Prevents credential leaks in source control)**

Hardcoded credentials in source code get committed to git and exposed publicly. The `@nestjs/config` package provides a secure way to manage configuration through environment variables. **Secrets belong in environment only.**

**Incorrect:**

```typescript
// database.module.ts
TypeOrmModule.forRoot({
  url: 'postgres://user:password@localhost/db',  // 🚨 Exposed!
  ssl: {
    cert: process.env.DB_CERT,  // Still vulnerable if cert is committed
  },
})

// auth.service.ts
@Injectable()
export class AuthService {
  private readonly jwtSecret = 'my-super-secret-key-12345';  // 🚨 Exposed!
  private readonly apiKey = 'sk_test_abc123xyz';  // 🚨 Exposed!
}

// payment.controller.ts
const stripe = require('stripe')('sk_test_51ABC...');  // 🚨 Exposed!
```

**Correct:**

```typescript
// For production, ignore .env files and use process.env only
ConfigModule.forRoot({
  isGlobal: true,
  ignoreEnvFile: process.env.NODE_ENV === 'production',
  validationSchema: productionValidationSchema,
})
```

Use Joi or Zod to validate environment variables at startup:

Use `registerAs` for type-safe, grouped configuration:

Always provide a `.env.example` file to document required variables:

**Sources:**

- [Configuration | NestJS - Official Documentation](https://docs.nestjs.com/techniques/configuration)

- [Managing Environment Variables in NestJS with ConfigModule | Medium](https://medium.com/@hashirmughal1000/managing-environment-variables-in-nestjs-with-configmodule-5b0742efb69c)

- [Managing Configuration and Environment Variables in NestJS | dev.to](https://dev.to/vishnucprasad/managing-configuration-and-environment-variables-in-nestjs-28ni)

- [NestJS Environment Configuration Using Zod | Medium](https://medium.com/@rotemdoar17/nestjs-environment-configuration-using-zod-92e3decca5ca)

---

## 10. Section 10

**Impact: MEDIUM**

### 10.1 Write Comprehensive Unit Tests

**Impact: MEDIUM (Catches bugs early and enables safe refactoring)**

Untested code leads to regressions and production bugs. NestJS + Jest provides full testing support for controllers, services, and repositories. **Aim for 80%+ coverage on business logic.**

**Incorrect: no tests**

```typescript
// users.service.ts - No tests 🚨
@Injectable()
export class UsersService {
  async createUser(data: CreateUserDto) {
    return this.prisma.user.create({ data });
  }
}
```

**Correct: full test suite**

```typescript
// users.service.spec.ts
describe('UsersService', () => {
  let service: UsersService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [UsersService, { provide: PrismaService, useValue: mockPrisma }],
    }).compile();
    service = module.get(UsersService);
  });

  it('should create user successfully', async () => {
    const dto: CreateUserDto = { email: 'test@example.com', name: 'Test' };
    const mockUser = { id: '1', ...dto };

    jest.spyOn(prisma.user, 'create').mockResolvedValue(mockUser);

    const result = await service.createUser(dto);
    expect(result).toEqual(mockUser);
    expect(prisma.user.create).toHaveBeenCalledWith(expect.any(Object));
  });
});
```

---

## 11. Section 11

**Impact: HIGH**

### 11.1 Implement Health Check Endpoints

**Impact: HIGH (Enables monitoring and automatic restarts)**

No health checks prevent container orchestrators from detecting failures. Dedicated endpoints verify database, cache, and service connectivity. **Production apps must expose health status.**

**Incorrect: no monitoring**

```typescript
// No health endpoint - can't detect failures 🚨
```

**Correct: comprehensive health checks**

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

---

## 12. Section 12

**Impact: HIGH**

### 12.1 Enable Compression Middleware for Responses

**Impact: HIGH (Reduces bandwidth usage and improves performance)**

Uncompressed responses waste bandwidth and slow down page loads. Compression middleware (gzip/brotli) reduces response size by 70-90%. **Always enable compression in production.**

**Incorrect: no compression**

```typescript
// main.ts - Large responses 🚨
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
```

**Correct: compressed responses**

```typescript
// main.ts
import * as compression from 'compression';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(compression());  // Gzip/brotli compression ✅
  await app.listen(3000);
}
```

Reference: [https://docs.nestjs.com/techniques/compression](https://docs.nestjs.com/techniques/compression)

### 12.2 Implement Rate Limiting for All Routes

**Impact: CRITICAL (Prevents DDoS and brute force attacks)**

Unlimited requests per IP enable brute force attacks and DDoS. Global rate limiter throttles excessive requests. **Protect every endpoint from abuse.**

**Incorrect: no protection**

```typescript
// main.ts - Unlimited requests 🚨
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
```

**Correct: rate limited**

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

---

## 13. Section 13

**Impact: HIGH**

### 13.1 Lazy Load Non-Critical Modules

**Impact: HIGH (Reduces startup time and memory usage)**

All modules load at startup, wasting memory on unused features. Lazy loading defers module initialization until the first request to that module. **Load only what's needed, when it's needed.**

**Incorrect:**

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { UsersModule } from './users/users.module';
import { AdminModule } from './admin/admin.module';
import { AnalyticsModule } from './analytics/analytics.module';
import { ReportsModule } from './reports/reports.module';

@Module({
  imports: [
    CoreModule,
    UsersModule,
    AdminModule,      // 🚨 Always loads at startup
    AnalyticsModule,  // 🚨 Always loads at startup
    ReportsModule,    // 🚨 Always loads at startup
  ],
})
export class AppModule {}
```

**Correct:**

```bash
# Application startup
[AppModule] initialized
[UsersModule] initialized

Startup time: 0.5s
Memory usage: 100MB

# After first admin request
[AdminModule] loaded
Memory usage: 150MB (+50MB)

# After first analytics request
[AnalyticsModule] loaded
Memory usage: 230MB (+80MB)
```

For NestJS 10+, use the built-in `ModuleLoader`:

A more practical approach is lazy loading through routing:

Create a reusable lazy loading decorator:

Using Fastify's plugin system for lazy loading:

Configure which modules to lazy load:

❌ **Don't lazy load:**

- Authentication/Authorization modules (needed immediately)

- Public API routes (accessed by most users)

- Core business logic (used throughout the app)

- Frequently accessed features (would cause repeated loading)

✅ **DO lazy load:**

- Admin panels (accessed by few users, infrequently)

- Analytics dashboards (not accessed on every request)

- Report generators (heavy, infrequently used)

- Integration modules (external service integrations)

- Background job processors (only run periodically)

| Practice | Description |

|----------|-------------|

| Measure before optimizing | Profile startup time and memory usage first |

| Lazy load infrequently used modules | Admin, analytics, reports, integrations |

| Keep critical modules eager | Auth, core API, public routes |

| Preload in development | Faster hot module replacement during development |

| Monitor memory usage | Track actual memory savings in production |

| Consider serverless | Lazy loading is crucial for cold start optimization |

**Sources:**

- [Modules | NestJS - Official Documentation](https://docs.nestjs.com/modules)

- [Dynamic Modules | NestJS](https://docs.nestjs.com/fundamentals/dynamic-modules)

- [Performance Optimization | NestJS](https://docs.nestjs.com/techniques/performance)

- [Serverless NestJS | NestJS Blog](https://trilon.io/blog/serverless-nestjs)

### 13.2 Use @nestjs/schedule for Cron Jobs and Scheduled Tasks

**Impact: MEDIUM (Ensures reliable periodic task execution)**

Scheduled tasks like cleanup jobs, data synchronization, and periodic reports need reliable execution. The `@nestjs/schedule` module provides decorators for cron jobs, intervals, and timeouts with proper NestJS lifecycle management. **Never use raw `setInterval` or external cron schedulers.**

**Incorrect:**

```typescript
// cleanup.service.ts - Raw timers 🚨
import { Injectable, OnModuleDestroy } from '@nestjs/common';

@Injectable()
export class CleanupService implements OnModuleDestroy {
  private intervals: NodeJS.Timeout[] = [];

  constructor() {
    // ❌ Raw interval - no NestJS lifecycle
    const interval1 = setInterval(() => {
      this.cleanupExpiredSessions().catch(console.error);
    }, 60000);  // Every minute

    // ❌ Another raw interval
    const interval2 = setInterval(() => {
      this.deleteOldLogs().catch(console.error);
    }, 3600000);  // Every hour

    // ❌ Manual interval tracking
    this.intervals.push(interval1, interval2);
  }

  // ❌ Manual cleanup required
  onModuleDestroy() {
    this.intervals.forEach(clearInterval);
  }

  // ❌ No error handling in callbacks
  async cleanupExpiredSessions() {
    await this.prisma.session.deleteMany({
      where: { expiresAt: { lt: new Date() } },
    });
  }

  async deleteOldLogs() {
    await this.prisma.log.deleteMany({
      where: { createdAt: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } },
    });
  }
}

// subscription.service.ts - Manual tracking 🚨
@Injectable()
export class SubscriptionService {
  private checkInterval: NodeJS.Timeout;

  constructor(private prisma: PrismaService) {
    // ❌ Manually start interval
    this.startCheckingExpiringSubscriptions();
  }

  private startCheckingExpiringSubscriptions() {
    this.checkInterval = setInterval(async () => {
      try {
        await this.checkExpiringSubscriptions();
      } catch (error) {
        console.error('Subscription check failed:', error);
        // ❌ No structured logging
      }
    }, 24 * 60 * 60 * 1000);  // Daily
  }

  private async checkExpiringSubscriptions() {
    // Business logic
  }
}
```

**Correct:**

```typescript
// tasks/scheduled-tasks.service.spec.ts ✅
import { Test, TestingModule } from '@nestjs/testing';
import { ScheduledTasksService } from './scheduled-tasks.service';
import { SchedulerRegistry } from '@nestjs/schedule';

describe('ScheduledTasksService', () => {
  let service: ScheduledTasksService;
  let schedulerRegistry: SchedulerRegistry;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ScheduledTasksService,
        {
          provide: PrismaService,
          useValue: { session: { deleteMany: jest.fn() } },
        },
        {
          provide: SchedulerRegistry,
          useValue: {
            addCronJob: jest.fn(),
            getCronJob: jest.fn(),
            deleteCronJob: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<ScheduledTasksService>(ScheduledTasksService);
    schedulerRegistry = module.get<SchedulerRegistry>(SchedulerRegistry);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should cleanup expired sessions', async () => {
    const deleteMany = jest.fn().mockResolvedValue({ count: 5 });
    service['prisma'].session.deleteMany = deleteMany;

    await service.cleanupExpiredSessions();

    expect(deleteMany).toHaveBeenCalledWith({
      where: { expiresAt: { lt: expect.any(Date) } },
    });
  });

  it('should handle errors gracefully', async () => {
    const loggerSpy = jest.spyOn(service['logger'], 'error');
    jest.spyOn(service['prisma'].session, 'deleteMany').mockRejectedValue(
      new Error('Database error')
    );

    await service.cleanupExpiredSessions();

    expect(loggerSpy).toHaveBeenCalled();
  });
});
```

| Practice | Why |

|----------|-----|

| Use `@nestjs/schedule` decorators | Proper NestJS lifecycle management |

| Use `CronExpression` enum | Readable, less error-prone |

| Always handle errors | Prevent cascading failures |

| Prevent overlapping executions | Avoid resource exhaustion |

| Log task execution | Monitor and debug issues |

| Use `@Interval()` for simple frequencies | More readable than cron |

| Use `@Timeout()` for startup tasks | One-time initialization |

**Sources:**

- [Task Scheduling | NestJS - Official Documentation](https://docs.nestjs.com/techniques/task-scheduling)

- [Cron Expression Format | crontab.guru](https://crontab.guru/)

- [Cron Documentation | npm](https://www.npmjs.com/package/cron)

---

## 14. Section 14

**Impact: MEDIUM**

### 14.1 Use Response Transformation Interceptor for Serialization

**Impact: MEDIUM (Prevents sensitive data leaks and ensures consistent response format)**

When implementing or reviewing response handling, **always** follow these steps:

**Pattern to check:** Look for controllers returning entity objects, repositories, or database results directly.

**If found:** Implement TransformInterceptor.

**File:** `src/common/interceptors/transform.interceptor.ts`

**File:** `src/main.ts`

**Incorrect:**

```typescript
// users/users.controller.ts - Leaks sensitive data 🚨
import { Controller, Get, Param } from '@nestjs/common';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  // ❌ Returns entity with password field
  @Get(':id')
  async findOne(@Param('id') id: string) {
    const user = await this.usersService.findOne(id);
    // Response includes: { id, email, name, password, internalNotes }
    // Password is exposed!
    return user;
  }

  // ❌ Returns raw repository data
  @Get()
  async findAll() {
    // Returns all users with all fields
    return this.usersService.findAll();
  }

  // ❌ Manual exclusion - verbose and error-prone
  @Get('public/:id')
  async findPublic(@Param('id') id: string) {
    const user = await this.usersService.findOne(id);
    // ❌ Must remember to exclude in every method
    const { password, internalNotes, ...publicUser } = user;
    return publicUser;
  }
}

// users/entities/user.entity.ts - No exclusion decorators 🚨
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  email: string;

  @Column()
  password: string;  // ❌ Will be included in all responses

  @Column({ name: 'internal_notes' })
  internalNotes: string;  // ❌ Leaked to clients
}
```

**Correct:**

```typescript
// ✅ Interceptor that handles arrays, pagination, etc.
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { map, Observable } from 'rxjs';
import { instanceToPlain } from 'class-transformer';

@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => {
        // Handle Pagination
        if (data?.data !== undefined && data?.meta !== undefined) {
          return {
            ...data,
            data: instanceToPlain(data.data),
          };
        }

        // Handle Arrays
        if (Array.isArray(data)) {
          return data.map((item) => instanceToPlain(item));
        }

        // Handle single objects
        return instanceToPlain(data);
      }),
    );
  }
}
```

| Practice | Why |

|----------|-----|

| Use `@Exclude()` on sensitive fields | Automatically excluded from all responses |

| Register TransformInterceptor globally | Consistent serialization across all routes |

| Use `@Expose()` for virtual properties | Add computed fields to responses |

| Use groups for role-based responses | Different data for different user types |

| Never return raw entities | Prevents accidental data leaks |

| Handle pagination responses | Transform paginated data correctly |

**Sources:**

- [NestJS Interceptors Documentation](https://docs.nestjs.com/interceptors)

- [class-transformer Documentation](https://github.com/typestack/class-transformer)

- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

---

## References

1. [https://docs.nestjs.com/](https://docs.nestjs.com/)
2. [https://expressjs.com/](https://expressjs.com/)
