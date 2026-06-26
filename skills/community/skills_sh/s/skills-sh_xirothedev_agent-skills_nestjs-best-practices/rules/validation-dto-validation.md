---
title: Validate All Inputs with DTOs and ValidationPipe
impact: CRITICAL
impactDescription: Prevents invalid data and injection attacks
section: 5
tags: validation, security, dto, class-validator
---

## Validate All Inputs with DTOs and ValidationPipe

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

```typescript
// main.ts - Global ValidationPipe
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,              // Strip properties not in DTO
    forbidNonWhitelisted: true,   // Throw error if extra properties
    transform: true,              // Convert plain objects to DTO instances
    transformOptions: {
      enableImplicitConversion: true,
    },
    disableErrorMessages: false,  // Show detailed validation errors
  }));

  await app.listen(3000);
}

// dto/create-user.dto.ts - Full validation
import { IsEmail, IsString, MinLength, IsOptional, IsInt, Matches } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateUserDto {
  @IsEmail({}, { message: 'Invalid email format' })
  email: string;

  @IsString()
  @MinLength(8, { message: 'Password must be at least 8 characters' })
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase, and number'
  })
  password: string;

  @IsOptional()
  @IsString()
  @MinLength(2)
  name?: string;

  @IsOptional()
  @IsInt()
  @Min(18)
  @Max(120)
  age?: number;
}

// users.controller.ts - Type-safe
@Post()
create(@Body() createUserDto: CreateUserDto) {
  // DTO is automatically validated before reaching here
  return this.usersService.create(createUserDto);
}
```

## ValidationPipe Options Reference

| Option | What It Does | Always Use? |
|--------|--------------|------------|
| `whitelist: true` | Removes properties not in DTO | ✅ Yes |
| `forbidNonWhitelisted: true` | Throws error if extra properties sent | ✅ Yes (security) |
| `transform: true` | Converts plain objects to DTO instances | ✅ Yes (type safety) |
| `disableErrorMessages: false` | Shows detailed validation errors | ✅ Yes (debugging) |
| `transformOptions.enableImplicitConversion: true` | Auto-converts strings to types | ✅ Yes (convenience) |

## Common Validation Decorators

```typescript
import {
  // String validation
  IsEmail, IsString, IsUrl, IsUUID, IsPhoneNumber,
  MinLength, MaxLength, Matches,

  // Number validation
  IsInt, IsFloat, IsPositive, IsNegative,
  Min, Max, IsNumber,

  // Type validation
  IsBoolean, IsDate, IsArray, IsObject,

  // Conditional
  IsOptional, IsEmpty,

  // Enum & Sets
  IsEnum, IsIn, IsNotIn,

  // Array validation
  ArrayNotEmpty, ArrayMinSize, ArrayMaxSize,

  // Nested validation
  ValidateNested,
} from 'class-validator';

import { Type, Expose } from 'class-transformer';
```

> **Note:** For query parameter validation with filter DTOs, see `validation-filter-dtos.md`.

## Custom Validators

For business-specific validation rules:

```typescript
// decorators/is-strong-password.decorator.ts
import {
  registerDecorator,
  ValidationOptions,
  ValidatorConstraint,
  ValidatorConstraintInterface,
} from 'class-validator';

@ValidatorConstraint({ name: 'isStrongPassword', async: false })
export class IsStrongPasswordConstraint implements ValidatorConstraintInterface {
  validate(password: string) {
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongPasswordRegex.test(password);
  }

  defaultMessage() {
    return 'Password must contain at least 8 characters, including uppercase, lowercase, number, and special character';
  }
}

export function IsStrongPassword(validationOptions?: ValidationOptions) {
  return function (object: Object, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName: propertyName,
      options: validationOptions,
      constraints: [],
      validator: IsStrongPasswordConstraint,
    });
  };
}

// dto/create-user.dto.ts
export class CreateUserDto {
  @IsStrongPassword()
  password: string;
}
```

## Nested DTOs

```typescript
// dto/create-order.dto.ts
import { ValidateNested, IsArray, ArrayMinSize } from 'class-validator';
import { Type } from 'class-transformer';

export class OrderItemDto {
  @IsString()
  productId: string;

  @IsInt()
  @Min(1)
  quantity: number;
}

export class CreateOrderDto {
  @ValidateNested()
  @Type(() => AddressDto)
  shippingAddress: AddressDto;

  @IsArray()
  @ArrayMinSize(1)
  @ValidateNested({ each: true })
  @Type(() => OrderItemDto)
  items: OrderItemDto[];
}
```

## Expected Validation Error Response

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

**Sources:**
- [NestJS Validation Documentation](https://docs.nestjs.com/techniques/validation)
- [class-validator Documentation](https://github.com/typestack/class-validator)
- [class-transformer Documentation](https://github.com/typestack/class-transformer)
