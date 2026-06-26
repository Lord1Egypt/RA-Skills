---
title: Use Response Transformation Interceptor for Serialization
impact: MEDIUM
impactDescription: Prevents sensitive data leaks and ensures consistent response format
section: 14
tags: interceptors, serialization, class-transformer, response, security
---

Returning entity objects directly from controllers can leak sensitive data (passwords, internal fields) and results in inconsistent response formats. A global transformation interceptor with `class-transformer` ensures all responses are serialized consistently and sensitive data is excluded.

## For AI Agents

When implementing or reviewing response handling, **always** follow these steps:

### Step 1: Check for Direct Entity Returns
**Pattern to check:** Look for controllers returning entity objects, repositories, or database results directly.

```typescript
// ❌ WRONG - Returns entity with password
@Get(':id')
findOne(@Param('id') id: string) {
  return this.usersService.findOne(id); // ❌ Returns User with password!
}

// ❌ WRONG - Returns repository result
@Get()
findAll() {
  return this.usersService.findAll(); // ❌ Returns raw entities
}

// ❌ WRONG - Manual exclusion in each method
@Get(':id')
findOne(@Param('id') id: string) {
  const user = await this.usersService.findOne(id);
  // ❌ Repeated, error-prone manual exclusion
  const { password, ...result } = user;
  return result;
}
```

**If found:** Implement TransformInterceptor.

### Step 2: Create TransformInterceptor
**File:** `src/common/interceptors/transform.interceptor.ts`

```typescript
// ✅ REQUIRED: Global response transformation
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { map, Observable } from 'rxjs';
import { classToPlain, instanceToPlain } from 'class-transformer';

@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => {
        // Transform response data using class-transformer
        // This respects @Exclude() and other class-transformer decorators
        return instanceToPlain(data);
      }),
    );
  }
}
```

### Step 3: Register Globally
**File:** `src/main.ts`

```typescript
// ✅ REQUIRED: Register interceptor globally
import { TransformInterceptor } from './common/interceptors/transform.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ✅ Apply to all routes
  app.useGlobalInterceptors(new TransformInterceptor());

  await app.listen(3000);
}
bootstrap();
```

### Step 4: Use @Exclude() on Sensitive Fields

```typescript
// ✅ REQUIRED: Exclude sensitive fields
// users/entities/user.entity.ts
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
import { Exclude } from 'class-transformer';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  email: string;

  @Column()
  name: string;

  // ✅ Automatically excluded from all responses
  @Exclude()
  @Column()
  password: string;

  @Exclude()
  @Column({ name: 'internal_notes' })
  internalNotes: string;
}
```

### Step 5: Use @Expose() for Computed Fields

```typescript
// ✅ OPTIONAL: Virtual/computed properties
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
import { Exclude, Expose } from 'class-transformer';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  firstName: string;

  @Column()
  lastName: string;

  // ✅ Virtual property - not in database
  @Expose()
  get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  // ✅ Conditional exposure
  @Expose({ groups: ['admin'] })
  @Column({ default: false })
  isAdmin: boolean;
}
```

### Step 6: Use Groups for Role-Based Responses

```typescript
// ✅ OPTIONAL: Different response for different roles
import { Exclude, Expose } from 'class-transformer';

@Entity('users')
export class User {
  @Expose({ groups: ['public', 'admin'] })
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Expose({ groups: ['public', 'admin'] })
  @Column()
  email: string;

  @Expose({ groups: ['admin'] })
  @Column()
  phoneNumber: string;

  @Exclude({ groups: ['public', 'admin'] })
  @Column()
  password: string;
}

// In controller/service
import { instanceToPlain } from 'class-transformer';

return instanceToPlain(user, { groups: ['public'] });
```

### Step 7: Configure Serialization Options

```typescript
// ✅ OPTIONAL: Advanced interceptor with options
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { map, Observable } from 'rxjs';
import { instanceToPlain, ClassTransformOptions } from 'class-transformer';

@Injectable()
export class TransformInterceptor implements NestInterceptor {
  private readonly options: ClassTransformOptions;

  constructor(options: ClassTransformOptions = {}) {
    this.options = {
      excludePrefixes: ['_'],  // Exclude properties starting with _
      ...options,
    };
  }

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => instanceToPlain(data, this.options)),
    );
  }
}

// Usage with custom options
app.useGlobalInterceptors(
  new TransformInterceptor({
    groups: ['public'],
    version: '1.0',
  }),
);
```

## Installation

```bash
# Install class-transformer
bun add class-transformer
# or
npm install class-transformer

# For TypeORM entities (optional)
bun add typeorm
# or
npm install typeorm
```

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
// users/users.controller.ts - Clean and secure ✅
import { Controller, Get, Param } from '@nestjs/common';
import { UsersService } from './users.service';

@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  // ✅ Clean - interceptor handles serialization
  @Get(':id')
  async findOne(@Param('id') id: string) {
    // Response excludes password automatically
    return this.usersService.findOne(id);
  }

  // ✅ Consistent across all endpoints
  @Get()
  async findAll() {
    // All users returned without sensitive fields
    return this.usersService.findAll();
  }

  // ✅ No manual exclusion needed
  @Get('profile')
  async getProfile(@GetUser() user: User) {
    // Password automatically excluded
    return user;
  }
}

// users/entities/user.entity.ts - Proper decorators ✅
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
import { Exclude, Expose } from 'class-transformer';

@Entity('users')
export class User {
  @Expose()
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Expose()
  @Column()
  email: string;

  @Expose()
  @Column()
  name: string;

  // ✅ Automatically excluded from all responses
  @Exclude()
  @Column()
  password: string;

  // ✅ Exclude internal fields
  @Exclude()
  @Column({ name: 'internal_notes' })
  internalNotes: string;

  // ✅ Virtual property
  @Expose()
  get initials(): string {
    return this.firstName
      ? this.firstName[0] + this.lastName[0]
      : this.email[0];
  }
}

// common/interceptors/transform.interceptor.ts ✅
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { map, Observable } from 'rxjs';
import { instanceToPlain } from 'class-transformer';

@Injectable()
export class TransformInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => {
        // Respects @Exclude, @Expose, and other decorators
        return instanceToPlain(data);
      }),
    );
  }
}

// main.ts - Global registration ✅
import { TransformInterceptor } from './common/interceptors/transform.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ✅ Apply to all routes
  app.useGlobalInterceptors(new TransformInterceptor());

  await app.listen(3000);
}
```

## Advanced: Serialization Groups

```typescript
// ✅ Role-based response filtering
// users/entities/user.entity.ts
import { Exclude, Expose } from 'class-transformer';
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('users')
export class User {
  @Expose({ groups: ['basic', 'full', 'admin'] })
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Expose({ groups: ['basic', 'full', 'admin'] })
  @Column()
  email: string;

  @Expose({ groups: ['full', 'admin'] })
  @Column()
  phoneNumber: string;

  @Expose({ groups: ['admin'] })
  @Column()
  lastLoginAt: Date;

  @Exclude()
  @Column()
  password: string;
}

// users/users.controller.ts ✅
import { instanceToPlain } from 'class-transformer';

@Controller('users')
export class UsersController {
  @Get('public/:id')
  async findPublic(@Param('id') id: string) {
    const user = await this.usersService.findOne(id);
    // Only basic fields
    return instanceToPlain(user, { groups: ['basic'] });
  }

  @Get(':id')
  @UseGuards(JwtAuthGuard)
  async findOne(@Param('id') id: string, @GetUser() currentUser: User) {
    const user = await this.usersService.findOne(id);

    // Full profile for own account
    if (user.id === currentUser.id) {
      return instanceToPlain(user, { groups: ['full'] });
    }

    // Basic for other users
    return instanceToPlain(user, { groups: ['basic'] });
  }

  @Get('admin/:id')
  @UseGuards(AdminGuard)
  async adminFindOne(@Param('id') id: string) {
    const user = await this.usersService.findOne(id);
    // All fields for admin
    return instanceToPlain(user, { groups: ['admin'] });
  }
}
```

## Advanced: Custom Serialization

```typescript
// ✅ Custom interceptor for response wrapper
// common/interceptors/wrap-response.interceptor.ts
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { map, Observable } from 'rxjs';
import { instanceToPlain } from 'class-transformer';

export interface Response<T> {
  success: boolean;
  data: T;
  timestamp: string;
}

@Injectable()
export class WrapResponseInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<any>> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data: instanceToPlain(data),
        timestamp: new Date().toISOString(),
      })),
    );
  }
}

// main.ts - Combine interceptors ✅
import { TransformInterceptor } from './common/interceptors/transform.interceptor';
import { WrapResponseInterceptor } from './common/interceptors/wrap-response.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ✅ Order matters - wrap runs first, then transform
  app.useGlobalInterceptors(
    new WrapResponseInterceptor(),
    new TransformInterceptor(),
  );

  await app.listen(3000);
}

// Response format:
// {
//   "success": true,
//   "data": { "id": "123", "email": "user@example.com" },
//   "timestamp": "2026-01-20T12:00:00.000Z"
// }
```

## Advanced: Handle Different Response Types

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

## Best Practices Summary

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
