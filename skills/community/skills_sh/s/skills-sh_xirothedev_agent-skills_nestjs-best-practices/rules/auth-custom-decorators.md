---
title: Use Custom Decorators for Type-Safe Request Data Access
impact: HIGH
impactDescription: Improves type safety and reduces boilerplate
section: 7
tags: auth, decorators, types, request, type-safety
---

Accessing request data directly through `@Req()` or `@Request()` decorators results in verbose, type-unsafe code. Custom decorators encapsulate request data extraction and provide full type safety with autocomplete support.

## For AI Agents

When implementing or reviewing request data access, **always** follow these steps:

### Step 1: Check for Manual Request Data Access
**Pattern to check:** Look for direct access to `req.user`, `req.headers`, type assertions, or manual data extraction.

```typescript
// ❌ WRONG - Manual extraction with type assertion
@Get()
findAll(@Req() req: Request) {
  const user = req.user as any; // ❌ Unsafe type assertion
  return this.tasksService.getTasks(user.id);
}

// ❌ WRONG - Verbose manual extraction
@Post()
create(@Req() req: Request, @Body() dto: CreateTaskDto) {
  const user = req.user as User;
  const token = req.headers.authorization?.replace('Bearer ', '');
  return this.tasksService.create(dto, user.id, token);
}

// ❌ WRONG - Repeated extraction logic
@Get('profile')
getProfile(@Req() req: Request) {
  const user = req.user as User;
  return { id: user.id, email: user.email, name: user.name };
}

@Get('stats')
getStats(@Req() req: Request) {
  const user = req.user as User;
  return this.statsService.getUserStats(user.id);
}
```

**If found:** Replace with custom decorators.

### Step 2: Create Custom User Decorator
**File:** `src/auth/decorators/get-user.decorator.ts`

```typescript
// ✅ REQUIRED: Custom decorator for type-safe user access
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

### Step 3: Create Decorator with Property Access
For accessing specific user properties:

```typescript
// ✅ OPTIONAL: Decorator with property selection
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    return data ? user?.[data] : user;
  },
);

// Usage:
// @GetUser()              → Returns full User object
// @GetUser('id')          → Returns user.id
// @GetUser('email')       → Returns user.email
```

### Step 4: Create Decorators for Other Request Data

```typescript
// ✅ OPTIONAL: Headers decorator
// src/common/decorators/headers.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const Headers = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const headers = request.headers;

    return data ? headers[data] : headers;
  },
);

// ✅ OPTIONAL: Bearer token decorator
// src/common/decorators/bearer-token.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const BearerToken = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      return null;
    }

    return authHeader.substring(7);
  },
);

// ✅ OPTIONAL: IP address decorator
// src/common/decorators/ip-address.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const IpAddress = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();

    // Check for forwarded IP (behind proxy)
    const forwarded = request.headers['x-forwarded-for'] as string;
    if (forwarded) {
      return forwarded.split(',')[0].trim();
    }

    return request.socket.remoteAddress;
  },
);
```

### Step 5: Use Decorators in Controllers

```typescript
// ✅ REQUIRED: Clean controller with decorators
// tasks/tasks.controller.ts
import { GetUser } from '../auth/decorators/get-user.decorator';
import { User } from '../users/entities/user.entity';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(@GetUser() user: User) {
    // ✅ Type-safe, full autocomplete
    return this.tasksService.getTasks(user.id);
  }

  @Post()
  create(
    @Body() dto: CreateTaskDto,
    @GetUser() user: User,
  ) {
    return this.tasksService.create(dto, user.id);
  }

  @Get('profile')
  getProfile(@GetUser() user: User) {
    // ✅ Type-safe, no assertion needed
    return {
      id: user.id,
      email: user.email,
      name: user.name,
    };
  }

  @Get('stats')
  getStats(@GetUser() user: User) {
    // ✅ Clean and consistent
    return this.statsService.getUserStats(user.id);
  }
}

// ✅ OPTIONAL: Using property selection
@Get('email')
getEmail(@GetUser('email') email: string) {
  return { email };
}

@Get('id')
getId(@GetUser('id') userId: string) {
  return this.service.findById(userId);
}

// ✅ OPTIONAL: Using token decorator
import { BearerToken } from '../common/decorators/bearer-token.decorator';

@Post('refresh')
refreshToken(@BearerToken() token: string) {
  return this.authService.refreshToken(token);
}

// ✅ OPTIONAL: Using IP address decorator
import { IpAddress } from '../common/decorators/ip-address.decorator';

@Post('login')
login(@Body() dto: LoginDto, @IpAddress() ip: string) {
  return this.authService.login(dto, ip);
}
```

### Step 6: Create Typed Decorator for User Entity

```typescript
// ✅ OPTIONAL: Fully typed decorator
// src/auth/decorators/get-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { User } from '../../users/entities/user.entity';

export type UserData = User;

export const GetUser = createParamDecorator(
  (data: keyof UserData | undefined, ctx: ExecutionContext): UserData | UserData[ keyof UserData ] => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user as UserData;

    return data ? user?.[data] : user;
  },
);

// Usage with full type safety:
// @GetUser()        → User
// @GetUser('id')    → string (type of user.id)
// @GetUser('email') → string (type of user.email)
```

## Installation

```bash
# No packages needed - custom decorators are built-in NestJS feature
```

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
// tasks/tasks.controller.ts - Clean and type-safe ✅
import { Controller, Get, Post, Patch, Param, Body } from '@nestjs/common';
import { TasksService } from './tasks.service';
import { GetUser } from '../auth/decorators/get-user.decorator';
import { User } from '../users/entities/user.entity';

@Controller('tasks')
export class TasksController {
  constructor(private tasksService: TasksService) {}

  // ✅ Type-safe, clean
  @Get()
  findAll(@GetUser() user: User) {
    // Full autocomplete, type safety
    return this.tasksService.getTasks(user.id);
  }

  // ✅ No repeated extraction
  @Get(':id')
  findOne(@Param('id') id: string, @GetUser() user: User) {
    return this.tasksService.findOne(id, user.id);
  }

  // ✅ Clean and consistent
  @Post()
  create(@Body() dto: CreateTaskDto, @GetUser() user: User) {
    return this.tasksService.create(dto, user.id);
  }

  // ✅ Full autocomplete support
  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() dto: UpdateTaskDto,
    @GetUser() user: User,
  ) {
    // TypeScript knows user.id exists
    return this.tasksService.update(id, dto, user.id);
  }

  // ✅ Property-specific decorator
  @Get('stats')
  getStats(@GetUser('id') userId: string) {
    return this.statsService.getUserStats(userId);
  }
}

// auth/decorators/get-user.decorator.ts - Basic implementation ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);

// auth/decorators/get-user.decorator.ts - With property selection ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    return data ? user?.[data] : user;
  },
);

// auth/decorators/get-user.decorator.ts - Fully typed ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { User } from '../../users/entities/user.entity';

export type UserData = User;

export const GetUser = createParamDecorator(
  (data: keyof UserData | undefined, ctx: ExecutionContext): UserData | UserData[keyof UserData] => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user as UserData;

    return data ? user?.[data] : user;
  },
);

// common/decorators/bearer-token.decorator.ts ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const BearerToken = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const authHeader = request.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
      return null;
    }

    return authHeader.substring(7);
  },
);

// common/decorators/ip-address.decorator.ts ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const IpAddress = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();

    // Check for forwarded IP (behind proxy/load balancer)
    const forwarded = request.headers['x-forwarded-for'] as string;
    if (forwarded) {
      return forwarded.split(',')[0].trim();
    }

    return request.socket.remoteAddress;
  },
);

// common/decorators/user-agent.decorator.ts ✅
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const UserAgent = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.headers['user-agent'] || '';
  },
);
```

## Advanced: Decorator Composition

```typescript
// ✅ Combine multiple decorators
// auth/decorators/auth-metadata.decorator.ts
import { applyDecorators, createParamDecorator, ExecutionContext } from '@nestjs/common';

export const GetUser = createParamDecorator(
  (data: string | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    return data ? user?.[data] : user;
  },
);

export const AuthMetadata = () =>
  applyDecorators(
    // Combines user, IP, and user agent in one decorator
    GetUser(),
  );

// Usage
@Post('audit')
auditAction(
  @AuthMetadata() metadata: { user: User; ip: string; userAgent: string },
) {
  return this.auditService.log({
    user: metadata.user.id,
    ip: metadata.ip,
    userAgent: metadata.userAgent,
  });
}
```

## Testing Custom Decorators

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

## Best Practices Summary

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
