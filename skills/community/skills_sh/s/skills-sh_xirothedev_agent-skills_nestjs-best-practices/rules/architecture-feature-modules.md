---
title: Organize Code by Feature Modules
impact: HIGH
section: 3
impactDescription: Improves scalability and maintainability
tags: architecture, modules, structure, scalability
---

## Organize Code by Feature Modules

Flat controller/service structure becomes unmaintainable at scale. NestJS modules enforce separation of concerns by feature. **One module per business domain.**

> **Hint**: Use feature modules to encapsulate related controllers, services, and providers. Each module should be independently testable and reusable across the application.

**Incorrect:**

```
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

```
src/
  users/
    users.module.ts
    users.controller.ts
    users.service.ts
    dto/
      create-user.dto.ts
      update-user.dto.ts
  auth/
    auth.module.ts
    auth.controller.ts
    auth.service.ts
    strategies/
      local.strategy.ts
      jwt.strategy.ts
    guards/
      jwt-auth.guard.ts
  products/
    products.module.ts
    products.controller.ts
    products.service.ts
    entities/
      product.entity.ts
```

## Module Configuration Example

```typescript
// users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { DatabaseModule } from '../database/database.module';

@Module({
  imports: [DatabaseModule],  // Import dependencies
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],    // Export for other modules
})
export class UsersModule {}
```

## Shared Modules

Services can be shared across multiple modules by exporting them:

```typescript
// database/database.module.ts
@Module({
  providers: [DatabaseService],
  exports: [DatabaseService],  // Make available to other modules
})
export class DatabaseModule {}

// users/users.module.ts
@Module({
  imports: [DatabaseModule],  // Import to use DatabaseService
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}

// users/users.service.ts
@Injectable()
export class UsersService {
  constructor(private databaseService: DatabaseService) {}  // Injected!
}
```

## Global Modules

Use `@Global()` for modules that should be available everywhere without importing:

```typescript
import { Global, Module } from '@nestjs/common';

@Global()  // Available everywhere without importing
@Module({
  providers: [ConfigService],
  exports: [ConfigService],
})
export class ConfigModule {}

// Any module can now use ConfigService without importing ConfigModule
@Module({
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

> **Warning**: Use global modules sparingly. Only use for truly universal services like logging, configuration, or utilities.

## Dynamic Modules

Create configurable modules with `register()` or `forRoot()` patterns:

```typescript
// database/database.module.ts
import { Module, DynamicModule } from '@nestjs/common';
import { DatabaseService } from './database.service';

export interface DatabaseModuleOptions {
  host: string;
  port: number;
  username: string;
  password: string;
}

@Module({})
export class DatabaseModule {
  static register(options: DatabaseModuleOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        {
          provide: 'DATABASE_OPTIONS',
          useValue: options,
        },
        DatabaseService,
      ],
      exports: [DatabaseService],
    };
  }

  static forRoot(options: DatabaseModuleOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        {
          provide: 'DATABASE_OPTIONS',
          useValue: options,
        },
        DatabaseService,
      ],
      exports: [DatabaseModule],
      global: true,  // Make available globally
    };
  }
}

// Usage in app.module.ts
@Module({
  imports: [
    DatabaseModule.register({
      host: 'localhost',
      port: 5432,
      username: 'user',
      password: 'pass',
    }),
  ],
})
export class AppModule {}
```

## Module Dependencies and Imports

Modules must explicitly declare their dependencies:

```typescript
// orders/orders.module.ts
@Module({
  imports: [
    UsersModule,    // Need UsersService for user validation
    ProductsModule, // Need ProductsService for inventory check
    PaymentsModule, // Need PaymentsService for processing
  ],
  controllers: [OrdersController],
  providers: [OrdersService],
})
export class OrdersModule {}
```

## Complete Feature Module Structure

Best practice structure for a feature module:

```
users/
  dto/
    create-user.dto.ts
    update-user.dto.ts
    user-response.dto.ts
  entities/
    user.entity.ts
  users.module.ts
  users.controller.ts
  users.service.ts
  users.spec.ts
  users.controller.spec.ts
```

### Example: Complete Users Module

```typescript
// users/dto/create-user.dto.ts
import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;

  @IsString()
  name: string;
}

// users/entities/user.entity.ts
export class User {
  id: string;
  email: string;
  password: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

// users/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { User } from './entities/user.entity';

@Injectable()
export class UsersService {
  private users: User[] = [];

  create(createUserDto: CreateUserDto): User {
    const user: User = {
      id: crypto.randomUUID(),
      ...createUserDto,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.users.push(user);
    return user;
  }

  findAll(): User[] {
    return this.users;
  }

  findOne(id: string): User {
    const user = this.users.find(u => u.id === id);
    if (!user) {
      throw new NotFoundException(`User ${id} not found`);
    }
    return user;
  }
}

// users/users.controller.ts
import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  create(@Body() createUserDto: CreateUserDto) {
    return this.usersService.create(createUserDto);
  }

  @Get()
  findAll() {
    return this.usersService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.usersService.findOne(id);
  }
}

// users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

## Module Best Practices

| Practice | Description | Why |
|----------|-------------|-----|
| One module per feature | Each business domain gets its own module | Clear separation of concerns |
| Export only what's needed | Only export services meant for external use | Prevents tight coupling |
| Use DTOs in each module | Keep data transfer objects with the module | Encapsulates validation logic |
| Avoid circular dependencies | Don't have Module A import Module B if B imports A | Prevents initialization issues |
| Use barrel exports | Export from `index.ts` for clean imports | Better developer experience |

### Barrel Export Pattern

```typescript
// users/index.ts
export * from './users.module';
export * from './users.service';
export * from './dto/create-user.dto';
export * from './dto/update-user.dto';

// Import from other modules
import { UsersModule, UsersService, CreateUserDto } from '@/users';
```

## Testing Modules

Test modules in isolation:

```typescript
// users/users.module.spec.ts
import { Test } from '@nestjs/testing';
import { UsersModule } from './users.module';
import { UsersService } from './users.service';

describe('UsersModule', () => {
  it('should compile the module', async () => {
    const module = await Test.createTestingModule({
      imports: [UsersModule],
    }).compile();

    expect(module).toBeDefined();
    expect(module.get(UsersService)).toBeInstanceOf(UsersService);
  });
});
```

## Module Communication Patterns

### Direct Import (Tight Coupling)

```typescript
@Module({
  imports: [UsersModule],  // Direct dependency
  providers: [OrdersService],
})
export class OrdersModule {}
```

### Event-Based (Loose Coupling)

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

**Sources:**
- [Modules | NestJS - Official Documentation](https://docs.nestjs.com/modules)
- [Dynamic Modules | NestJS](https://docs.nestjs.com/fundamentals/dynamic-modules)
- [Custom Providers | NestJS](https://docs.nestjs.com/providers#custom-providers)
- [EventEmitter2 | NestJS Recipe](https://docs.nestjs.com/techniques/events)
