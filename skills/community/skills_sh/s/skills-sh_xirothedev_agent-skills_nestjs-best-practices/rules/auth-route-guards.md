---
title: Use Guards for Route Protection
impact: CRITICAL
section: 7
impactDescription: Enforces authentication/authorization per route
tags: security, guards, auth, authorization
---

Unprotected routes expose sensitive data. Guards run before controllers and can short-circuit requests. **Protect endpoints explicitly.**

> **Hint**: Guards determine whether a request will be handled by the controller or not. Use them for authentication (who are you?) and authorization (what can you do?). Always use global guards with public route decorators for default-deny security.

## For AI Agents

When implementing or reviewing security, **always** follow these steps:

### Step 1: Set Up Global Authentication Guard
**Files to create/modify:**
- `src/auth/guards/jwt-auth.guard.ts`
- `src/auth/guards/jwt-auth.guard.spec.ts`
- `src/auth/decorators/public.decorator.ts`
- `src/app.module.ts` (for APP_GUARD)

```typescript
// ✅ REQUIRED: Global JWT Guard
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(
    private jwtService: JwtService,
    private reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()],
    );

    if (isPublic) return true;

    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);

    if (!token) return false;

    try {
      const payload = this.jwtService.verify(token);
      request['user'] = payload;
    } catch {
      return false;
    }

    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
```

### Step 2: Create @Public() Decorator
**File:** `src/auth/decorators/public.decorator.ts`

```typescript
// ✅ REQUIRED: For marking public routes
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

### Step 3: Register Guard Globally
**File:** `src/app.module.ts`

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

### Step 4: Check All Controllers Have Proper Protection
**Pattern to check:**

```typescript
// ❌ WRONG - No protection
@Controller('users')
export class UsersController {
  @Get()
  findAll() { }  // Anyone can access!
}

// ❌ WRONG - Manual check in controller
@Controller('users')
export class UsersController {
  @Get()
  findAll(@Req() req) {
    if (!req.user) throw new UnauthorizedException();  // Too late!
  }
}

// ✅ CORRECT - Protected by global guard
@Controller('users')
export class UsersController {
  @Get()
  findAll() { }  // Protected by JwtAuthGuard
}

// ✅ CORRECT - Explicitly public
@Controller('auth')
export class AuthController {
  @Post('login')
  @Public()  // ✅ Marked as public
  login() { }
}
```

## Quick Reference Checklist

Use this checklist when reviewing or creating endpoints:

- [ ] Global authentication guard registered in `app.module.ts`
- [ ] `@Public()` decorator exists for public routes
- [ ] Controllers don't use `any` type for `@Req()` user
- [ ] Admin routes have `@Roles('admin')` guard
- [ ] Resource owner checks implemented (users can only access their own data)
- [ ] Rate limiting applied to auth endpoints
- [ ] Guards use `Reflector` to check metadata

## Guard Execution Order

```
Request → Middleware → Guards → Interceptors → Pipes → Controller
                              ↑
                         Short-circuit here
```

## Installation

```bash
bun add @nestjs/jwt @nestjs/passport passport passport-jwt
bun add -D @types/passport-jwt
```

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
// auth/guards/jwt-auth.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(
    private jwtService: JwtService,
    private reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    const isPublic = this.reflector.getAllAndOverride<boolean>(
      'isPublic',
      [context.getHandler(), context.getClass()],
    );

    if (isPublic) return true;  // ✅ Skip for public routes

    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);

    if (!token) return false;

    try {
      const payload = this.jwtService.verify(token);
      request['user'] = payload;  // Attach user to request
    } catch {
      return false;
    }

    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}

// auth/decorators/public.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);

// app.module.ts - Global guard registration
import { APP_GUARD } from '@nestjs/core';

@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: JwtAuthGuard,  // ✅ All routes protected by default
    },
  ],
})
export class AppModule {}

// auth/auth.controller.ts - Public routes
@Controller('auth')
export class AuthController {
  @Post('login')
  @Public()  // ✅ Explicitly mark as public
  async login(@Body() loginDto: LoginDto) {
    return this.authService.login(loginDto);
  }

  @Post('register')
  @Public()  // ✅ Explicitly mark as public
  async register(@Body() registerDto: RegisterDto) {
    return this.authService.register(registerDto);
  }
}

// users/users.controller.ts - Protected by default
@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    // ✅ Protected by global guard - no @UseGuards needed
    return this.usersService.findAll();
  }

  @Get('profile')
  getProfile(@Req() request: Request) {
    // ✅ User attached by guard
    return request['user'];
  }
}
```

## Role-Based Authorization

```typescript
// auth/guards/roles.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>(
      'roles',
      context.getHandler(),
    );

    if (!requiredRoles) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}

// auth/decorators/roles.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// admin/admin.controller.ts
@Controller('admin')
@UseGuards(RolesGuard)  // ✅ Apply to controller
export class AdminController {
  @Get()
  @Roles('admin')  // ✅ Admins only
  getDashboard() {
    return this.adminService.getDashboard();
  }

  @Delete('users/:id')
  @Roles('admin')  // ✅ Only admins can delete
  deleteUser(@Param('id') id: string) {
    return this.adminService.deleteUser(id);
  }
}
```

## Resource Owner Guard

```typescript
// auth/guards/owner.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';

@Injectable()
export class OwnerGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const { user, params } = context.switchToHttp().getRequest();

    // Admin can access everything
    if (user.roles?.includes('admin')) return true;

    // Users can only access their own resources
    return user.id === params.userId || user.id === params.id;
  }
}

// orders/orders.controller.ts
@Controller('orders')
export class OrdersController {
  @Get('my-orders')
  @UseGuards(OwnerGuard)  // ✅ Resource owner check
  getMyOrders(@Req() request: Request) {
    return this.ordersService.findByUserId(request['user'].id);
  }

  @Patch(':id')
  @UseGuards(OwnerGuard)  // ✅ Users can only update their own orders
  update(@Param('id') id: string, @Body() dto: UpdateOrderDto) {
    return this.ordersService.update(id, dto);
  }
}
```

## Permission-Based Authorization

```typescript
// auth/decorators/require-permissions.decorator.ts
export const REQUIRE_PERMISSIONS_KEY = 'requirePermissions';
export const RequirePermissions = (...permissions: string[]) =>
  SetMetadata(REQUIRE_PERMISSIONS_KEY, permissions);

// auth/guards/permissions.guard.ts
@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.get<string[]>(
      REQUIRE_PERMISSIONS_KEY,
      context.getHandler(),
    );

    if (!requiredPermissions) return true;

    const { user } = context.switchToHttp().getRequest();
    return requiredPermissions.every((p) => user.permissions?.includes(p));
  }
}

// products/products.controller.ts
@Controller('products')
@UseGuards(PermissionsGuard)
export class ProductsController {
  @Post()
  @RequirePermissions('product:create')  // ✅ Requires specific permission
  create(@Body() dto: CreateProductDto) {
    return this.productsService.create(dto);
  }

  @Delete(':id')
  @RequirePermissions('product:delete')  // ✅ Requires specific permission
  remove(@Param('id') id: string) {
    return this.productsService.remove(id);
  }
}
```

## API Key Guard (Service-to-Service)

```typescript
// auth/guards/api-key.guard.ts
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(private configService: ConfigService) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    const validApiKeys = this.configService.get<string>('API_KEYS')?.split(',') || [];
    return validApiKeys.includes(apiKey);
  }
}

// webhook/webhook.controller.ts
@Controller('webhook')
@UseGuards(ApiKeyGuard)  // ✅ Requires valid API key
export class WebhookController {
  @Post('stripe')
  handleStripeWebhook(@Body() payload: any) {
    return this.webhookService.handleStripeEvent(payload);
  }
}
```

## Rate Limiting Auth Endpoints

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

## Summary: Guard Best Practices

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
