---
title: Lazy Load Non-Critical Modules
impact: HIGH
section: 13
impactDescription: Reduces startup time and memory usage
tags: performance, modules, lazy-loading, optimization
---

## Lazy Load Non-Critical Modules

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

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { CoreModule } from './core/core.module';
import { UsersModule } from './users/users.module';

@Module({
  imports: [
    CoreModule,      // ✅ Eager load - always needed
    UsersModule,     // ✅ Eager load - accessed immediately
  ],
})
export class AppModule {}

// Use lazy loading in routes or controllers
import { Controller, Get } from '@nestjs/common';
import { ModuleRef } from '@nestjs/core';

@Controller('admin')
export class AdminController {
  constructor(private moduleRef: ModuleRef) {}

  @Get('dashboard')
  async getDashboard() {
    // ✅ Lazy load AdminModule on first request
    const { AdminService } = await import('./admin/admin.module');
    const adminModule = await this.moduleRef.get(AdminModule);

    return adminModule.getDashboard();
  }
}
```

## Using ModuleLoader (NestJS 10+)

For NestJS 10+, use the built-in `ModuleLoader`:

```typescript
// app.module.ts
import { Module } from '@nestjs/common';
import { ModuleLoader } from '@nestjs/core';
import { join } from 'path';

@Module({
  imports: [
    CoreModule,
    UsersModule,
  ],
  providers: [
    {
      provide: 'LAZY_MODULES',
      useFactory: (moduleLoader: ModuleLoader) => ({
        async loadAdmin() {
          return moduleLoader.load(join(__dirname, './admin/admin.module.js'));
        },
        async loadAnalytics() {
          return moduleLoader.load(join(__dirname, './analytics/analytics.module.js'));
        },
      }),
      inject: [ModuleLoader],
    },
  ],
})
export class AppModule {}
```

## Alternative: Route-Based Lazy Loading

A more practical approach is lazy loading through routing:

```typescript
// app.controller.ts
import { Controller, Get, Res, Req } from '@nestjs/common';
import { createProxyMiddleware } from 'http-proxy-middleware';

@Controller()
export class AppController {
  @Get()
  index() {
    return 'Welcome to the API';
  }

  // Lazy-loaded admin routes
  @Get('admin*')
  async adminRoutes(@Req() req, @Res() res) {
    const { adminHandler } = await import('./lazy-handlers/admin.handler');
    return adminHandler(req, res);
  }

  // Lazy-loaded analytics routes
  @Get('analytics*')
  async analyticsRoutes(@Req() req, @Res() res) {
    const { analyticsHandler } = await import('./lazy-handlers/analytics.handler');
    return analyticsHandler(req, res);
  }
}
```

## Using Custom Lazy Module Decorator

Create a reusable lazy loading decorator:

```typescript
// common/decorators/lazy-module.decorator.ts
import { Module } from '@nestjs/common';

export function LazyModule(modulePath: string) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const module = await import(modulePath);
      return originalMethod.apply(this, [module, ...args]);
    };

    return descriptor;
  };
}

// Usage
@Controller('reports')
export class ReportsController {
  @Get()
  @LazyModule('../reports/reports.module')
  async getReports(reportsModule: any) {
    const { ReportsService } = reportsModule;
    return ReportsService.generateReport();
  }
}
```

## Lazy Loading with Fastify

Using Fastify's plugin system for lazy loading:

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { FastifyAdapter } from '@nestjs/platform-fastify';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(
    AppModule,
    new FastifyAdapter(),
  );

  // Register lazy-loaded plugins
  app.register(async function (fastify) {
    fastify.register(
      async function (instance) {
        const { adminRoutes } = await import('./admin/admin.routes');
        instance.register(adminRoutes, { prefix: '/admin' });
      },
      { prefix: '/api/v1' },
    );
  });

  await app.listen(3000);
}
```

## Dynamic Module Registration

```typescript
// common/services/module-loader.service.ts
import { Injectable, OnModuleInit, ModuleRef } from '@nestjs/core';
import { join } from 'path';

@Injectable()
export class ModuleLoaderService implements OnModuleInit {
  private loadedModules = new Map<string, any>();

  constructor(private moduleRef: ModuleRef) {}

  async onModuleInit() {
    // Preload critical modules if needed
    if (process.env.PRELOAD_ADMIN === 'true') {
      await this.loadModule('admin');
    }
  }

  async loadModule(moduleName: string) {
    if (this.loadedModules.has(moduleName)) {
      return this.loadedModules.get(moduleName);
    }

    const modulePath = join(__dirname, `./${moduleName}/${moduleName}.module`);
    const module = await import(modulePath);

    this.loadedModules.set(moduleName, module);
    return module;
  }

  getModule(moduleName: string) {
    return this.loadedModules.get(moduleName);
  }
}

// Usage in controllers
@Controller('admin')
export class AdminController {
  constructor(private moduleLoader: ModuleLoaderService) {}

  @Get('dashboard')
  async getDashboard() {
    const adminModule = await this.moduleLoader.loadModule('admin');
    return adminModule.AdminService.getDashboard();
  }
}
```

## Lazy Loading Configuration

Configure which modules to lazy load:

```typescript
// config/modules.config.ts
export interface LazyModuleConfig {
  name: string;
  path: string;
  preload?: boolean;
  priority?: number;
}

export const LAZY_MODULES: LazyModuleConfig[] = [
  {
    name: 'admin',
    path: './admin/admin.module',
    priority: 1,
    preload: process.env.NODE_ENV === 'development', // Preload in dev for faster HMR
  },
  {
    name: 'analytics',
    path: './analytics/analytics.module',
    priority: 2,
  },
  {
    name: 'reports',
    path: './reports/reports.module',
    priority: 3,
  },
  {
    name: 'integrations',
    path: './integrations/integrations.module',
    priority: 4,
  },
];

// app.module.ts
import { LAZY_MODULES } from './config/modules.config';

@Module({
  providers: [
    {
      provide: 'MODULE_LOADER',
      useFactory: () => {
        const loader = new Map();
        LAZY_MODULES.forEach(config => {
          if (config.preload) {
            // Preload specific modules
            import(config.path).then(m => loader.set(config.name, m));
          }
        });
        return loader;
      },
    },
  ],
})
export class AppModule {}
```

## Memory and Performance Benefits

### Before Lazy Loading

```bash
# Application startup
[AppModule] initialized
[UsersModule] initialized
[AdminModule] initialized      # 50MB
[AnalyticsModule] initialized  # 80MB
[ReportsModule] initialized    # 60MB
[IntegrationsModule] initialized # 70MB

Startup time: 2.5s
Memory usage: 310MB
```

### After Lazy Loading

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

## When NOT to Use Lazy Loading

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

## Summary: Lazy Loading Best Practices

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
