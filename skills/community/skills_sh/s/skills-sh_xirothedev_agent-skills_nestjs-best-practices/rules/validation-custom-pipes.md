---
title: Create Custom Pipes for Query Parameter Transformation
impact: MEDIUM
section: 5
impactDescription: Ensures type safety and reduces boilerplate
tags: validation, pipes, transformation, type-safety
---

Query parameters are always strings by default. Custom pipes automatically transform and validate these values before they reach your controller, providing type safety and reducing boilerplate code. **Never manually parse query parameters in controllers.**

> **Hint**: NestJS pipes are executed before controllers. Use them to transform `?page=1` into `number: 1`, `?active=true` into `boolean: true`, and trim whitespace from strings automatically.

## For AI Agents

When implementing or reviewing query parameter handling, **always** follow these steps:

### Step 1: Check for Manual Type Conversion
**Pattern to check:** Look for `parseInt()`, `Number()`, `Boolean()`, or string operations in controllers.

```typescript
// ❌ WRONG - Manual conversion in controller
@Get('users')
async getUsers(@Query('page') page: string) {
  const pageNum = parseInt(page, 10);  // Manual conversion!
  const limit = 10;
  return this.usersService.findAll({ page: pageNum, limit });
}

// ✅ CORRECT - Custom pipe handles conversion
@Get('users')
async getUsers(
  @Query('page', ParseIntPipe) page: number,
  @Query('limit', new ParseIntPipe({ optional: true })) limit?: number,
) {
  return this.usersService.findAll({ page, limit: limit || 10 });
}
```

**If found:** Create custom pipes to handle the conversion.

### Step 2: Create Basic Transformation Pipes
**File:** `src/common/pipes/parse-int.pipe.ts`

```typescript
// ✅ REQUIRED: ParseIntPipe with optional support
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  constructor(private options?: { optional?: boolean }) {}

  transform(value: string, metadata: ArgumentMetadata): number {
    if (this.options?.optional && !value) {
      return undefined as any;
    }

    const isNumeric = ['string', 'number'].includes(typeof value) &&
      !isNaN(parseFloat(value)) &&
      isFinite(parseFloat(value));

    if (!isNumeric) {
      throw new BadRequestException(`Validation failed: "${value}" is not a number`);
    }

    return parseFloat(value);
  }
}
```

**File:** `src/common/pipes/trim.pipe.ts`

```typescript
// ✅ REQUIRED: TrimPipe for strings
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';

@Injectable()
export class TrimPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    if (typeof value === 'string') {
      return value.trim();
    }
    return value;
  }
}

// For arrays and objects
@Injectable()
export class DeepTrimPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    if (typeof value === 'string') {
      return value.trim();
    }
    if (Array.isArray(value)) {
      return value.map(item => this.transform(item, metadata));
    }
    if (value && typeof value === 'object') {
      return Object.keys(value).reduce((acc, key) => {
        acc[key] = this.transform(value[key], metadata);
        return acc;
      }, {} as any);
    }
    return value;
  }
}
```

**File:** `src/common/pipes/parse-boolean.pipe.ts`

```typescript
// ✅ REQUIRED: ParseBooleanPipe
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseBooleanPipe implements PipeTransform<string, boolean> {
  transform(value: string, metadata: ArgumentMetadata): boolean {
    if (value === 'true' || value === '1') {
      return true;
    }
    if (value === 'false' || value === '0') {
      return false;
    }
    throw new BadRequestException(
      `Validation failed: "${value}" is not a boolean. Use "true" or "false"`
    );
  }
}
```

### Step 3: Register Pipes Globally or Use Per-Parameter

```typescript
// ✅ OPTIONAL: Global trim pipe in main.ts
import { ValidationPipe } from '@nestjs/common';
import { TrimPipe } from './common/pipes/trim.pipe';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply trim globally to all body/query/param values
  app.useGlobalPipes(new ValidationPipe({
    transform: true,
    whitelist: true,
    transformOptions: {
      enableImplicitConversion: true,
    },
  }));

  await app.listen(3000);
}
```

### Step 4: Use Pipes in Controllers

```typescript
// ✅ CORRECT: Controller with pipes
@Controller('users')
export class UsersController {
  @Get()
  findAll(
    @Query('page', new ParseIntPipe({ optional: true })) page?: number,
    @Query('limit', new ParseIntPipe({ optional: true })) limit?: number,
    @Query('active', new ParseBooleanPipe({ optional: true })) active?: boolean,
    @Query('search', TrimPipe) search?: string,
  ) {
    return this.usersService.findAll({
      page: page || 1,
      limit: limit || 10,
      active,
      search,
    });
  }
}
```

## Installation

```bash
# Pipes are built-in to NestJS - no extra packages needed
bun add @nestjs/common
```

## Quick Reference Checklist

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
// common/pipes/parse-int.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  constructor(private options?: { optional?: boolean; minValue?: number; maxValue?: number }) {}

  transform(value: string, metadata: ArgumentMetadata): number {
    // Handle optional empty values
    if (this.options?.optional && (value === undefined || value === null || value === '')) {
      return undefined as any;
    }

    const parsed = parseInt(value, 10);

    if (isNaN(parsed)) {
      throw new BadRequestException(
        `Validation failed: "${metadata.data}" must be a valid integer`
      );
    }

    // Range validation
    if (this.options?.minValue !== undefined && parsed < this.options.minValue) {
      throw new BadRequestException(
        `Validation failed: "${metadata.data}" must be at least ${this.options.minValue}`
      );
    }

    if (this.options?.maxValue !== undefined && parsed > this.options.maxValue) {
      throw new BadRequestException(
        `Validation failed: "${metadata.data}" must be at most ${this.options.maxValue}`
      );
    }

    return parsed;
  }
}

// common/pipes/parse-float.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseFloatPipe implements PipeTransform<string, number> {
  constructor(private options?: { optional?: boolean; min?: number; max?: number }) {}

  transform(value: string, metadata: ArgumentMetadata): number {
    if (this.options?.optional && !value) {
      return undefined as any;
    }

    const parsed = parseFloat(value);

    if (isNaN(parsed)) {
      throw new BadRequestException(`Validation failed: "${metadata.data}" must be a valid number`);
    }

    if (this.options?.min !== undefined && parsed < this.options.min) {
      throw new BadRequestException(`Validation failed: "${metadata.data}" must be at least ${this.options.min}`);
    }

    if (this.options?.max !== undefined && parsed > this.options.max) {
      throw new BadRequestException(`Validation failed: "${metadata.data}" must be at most ${this.options.max}`);
    }

    return parsed;
  }
}

// common/pipes/parse-boolean.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseBooleanPipe implements PipeTransform<string, boolean> {
  constructor(private options?: { optional?: boolean }) {}

  transform(value: string, metadata: ArgumentMetadata): boolean {
    if (this.options?.optional && !value) {
      return undefined as any;
    }

    const normalized = value.toLowerCase().trim();

    if (['true', '1', 'yes'].includes(normalized)) {
      return true;
    }

    if (['false', '0', 'no'].includes(normalized)) {
      return false;
    }

    throw new BadRequestException(
      `Validation failed: "${metadata.data}" must be a boolean (true/false, yes/no, 1/0)`
    );
  }
}

// common/pipes/trim.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';

@Injectable()
export class TrimPipe implements PipeTransform<string, string> {
  transform(value: string, metadata: ArgumentMetadata): string {
    if (typeof value !== 'string') {
      return value;
    }
    return value.trim();
  }
}

// common/pipes/default-value.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata } from '@nestjs/common';

@Injectable()
export class DefaultValuePipe<T = any> implements PipeTransform<T, T> {
  constructor(private readonly defaultValue: T) {}

  transform(value: T, metadata: ArgumentMetadata): T {
    return value === undefined || value === null || value === ''
      ? this.defaultValue
      : value;
  }
}

// users.controller.ts - Clean with pipes ✅
@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get()
  findAll(
    @Query('page', new ParseIntPipe({ optional: true, minValue: 1 })) page?: number,
    @Query('limit', new ParseIntPipe({ optional: true, minValue: 1, maxValue: 100 })) limit?: number,
    @Query('active', new ParseBooleanPipe({ optional: true })) active?: boolean,
    @Query('search', TrimPipe) search?: string,
    @Query('sortBy', new DefaultValuePipe('createdAt')) sortBy?: string,
    @Query('order', new DefaultValuePipe('DESC')) order?: 'ASC' | 'DESC',
  ) {
    return this.usersService.findAll({
      page: page || 1,
      limit: limit || 10,
      active,
      search,
      sortBy,
      order,
    });
  }

  @Get(':id')
  findOne(
    @Param('id', ParseIntPipe) id: number,
  ) {
    return this.usersService.findOne(id);
  }
}
```

## Pipe Composition and Chaining

### Combining Multiple Pipes

```typescript
// Apply multiple pipes to a single parameter
@Get('products')
async getProducts(
  @Query('price', ParseFloatPipe, new DefaultValuePipe(0)) minPrice: number,
  @Query('rating', ParseIntPipe, new DefaultValuePipe(0)) minRating: number,
) {
  return this.productsService.findFiltered({ minPrice, minRating });
}
```

### Custom Validation Pipe

```typescript
// common/pipes/enum.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class EnumPipe<T = any> implements PipeTransform<string, T> {
  constructor(private readonly enumObject: Record<string, T>) {}

  transform(value: string, metadata: ArgumentMetadata): T {
    const enumValues = Object.values(this.enumObject);

    if (enumValues.includes(value as T)) {
      return value as T;
    }

    throw new BadRequestException(
      `Validation failed: "${metadata.data}" must be one of: ${enumValues.join(', ')}`
    );
  }
}

// Usage
enum SortOrder {
  ASC = 'ASC',
  DESC = 'DESC',
}

enum SortField {
  NAME = 'name',
  CREATED_AT = 'createdAt',
  UPDATED_AT = 'updatedAt',
}

@Get('users')
async getUsers(
  @Query('order', new EnumPipe(SortOrder)) order: SortOrder,
  @Query('sortBy', new EnumPipe(SortField)) sortBy: SortField,
) {
  return this.usersService.findAll({ order, sortBy });
}
```

## Error Handling in Pipes

### Custom Error Messages

```typescript
// common/pipes/parse-uuid.pipe.ts ✅
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseUuidPipe implements PipeTransform<string, string> {
  constructor(private options?: { optional?: boolean; version?: 4 | 7 }) {}

  transform(value: string, metadata: ArgumentMetadata): string {
    if (this.options?.optional && !value) {
      return undefined as any;
    }

    const uuidRegex = this.options?.version === 7
      ? /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
      : /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

    if (!uuidRegex.test(value)) {
      throw new BadRequestException(
        `Validation failed: "${metadata.data}" must be a valid UUID${this.options?.version ? ` v${this.options.version}` : ''}`
      );
    }

    return value;
  }
}
```

### Formatting Error Response

```typescript
// common/exceptions/validation.exception.ts ✅
import { BadRequestException } from '@nestjs/common';

export class ValidationException extends BadRequestException {
  constructor(field: string, message: string, value?: any) {
    super({
      statusCode: 400,
      message: 'Validation failed',
      errors: [
        {
          field,
          message,
          value,
        },
      ],
    });
  }
}

// Use in pipe
@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  transform(value: string, metadata: ArgumentMetadata): number {
    const parsed = parseInt(value, 10);

    if (isNaN(parsed)) {
      throw new ValidationException(
        metadata.data,
        'Must be a valid integer',
        value
      );
    }

    return parsed;
  }
}
```

## Global Pipe Registration

### Registering Pipes Application-Wide

```typescript
// main.ts ✅
import { ValidationPipe, Logger } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { TrimPipe } from './common/pipes/trim.pipe';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Global validation pipe with all best practices
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,              // Strip properties not in DTO
    forbidNonWhitelisted: true,   // Throw error if extra properties
    transform: true,              // Convert plain objects to DTO instances
    transformOptions: {
      enableImplicitConversion: true,  // Auto-convert primitives
    },
    disableErrorMessages: false,  // Show detailed errors in development
    exceptionFactory: (errors) => {
      // Custom error format
      return new BadRequestException({
        statusCode: 400,
        message: 'Validation failed',
        errors: errors.map(error => ({
          field: error.property,
          constraints: error.constraints,
          value: error.value,
        })),
      });
    },
  }));

  await app.listen(3000);
}
bootstrap();
```

### Module-Level Pipe Registration

```typescript
// users.module.ts ✅
import { Module } from '@nestjs/common';
import { USERS_SERVICES } from './users.providers';
import { ParseIntPipe } from '../common/pipes/parse-int.pipe';

@Module({
  providers: [
    ...USERS_SERVICES,
    ParseIntPipe,  // Register pipe for use in this module
  ],
  exports: [ParseIntPipe],  // Export if other modules need it
})
export class UsersModule {}
```

## Testing Custom Pipes

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

## Best Practices Summary

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
