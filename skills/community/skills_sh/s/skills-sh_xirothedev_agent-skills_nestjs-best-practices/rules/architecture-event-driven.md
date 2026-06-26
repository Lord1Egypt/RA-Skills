---
title: Use Event-Driven Architecture for Loose Coupling
impact: HIGH
section: 3
impactDescription: Reduces dependencies and enables scalability
tags: architecture, events, EventEmitter2, loose-coupling
---

Direct service-to-service coupling creates rigid dependencies that are hard to test and maintain. Event-driven architecture uses domain events to decouple modules, allowing them to communicate without knowing about each other. **Never inject services directly just to trigger side effects.**

> **Hint**: When a user registers, you need to send a welcome email, create a profile, and log an audit event. Instead of injecting `EmailService`, `ProfileService`, and `AuditService` into `UsersService`, emit a `UserRegistered` event and let each service handle it independently.

## For AI Agents

When implementing or reviewing cross-module communication, **always** follow these steps:

### Step 1: Check for Direct Service Injection
**Pattern to check:** Look for multiple service dependencies that trigger side effects.

```typescript
// ❌ WRONG - Tight coupling through direct injection
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private emailService: EmailService,      // ❌ Only for sending welcome email
    private profileService: ProfileService,   // ❌ Only for creating profile
    private auditService: AuditService,       // ❌ Only for logging
  ) {}

  async register(data: RegisterDto) {
    const user = await this.prisma.user.create({ data });

    // ❌ Directly calling other services
    await this.emailService.sendWelcome(user.email);
    await this.profileService.create(user.id);
    await this.auditService.log('USER_REGISTERED', user.id);

    return user;
  }
}

// ✅ CORRECT - Loose coupling through events
@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private eventEmitter: EventEmitter2,
  ) {}

  async register(data: RegisterDto) {
    const user = await this.prisma.user.create({ data });

    // ✅ Emit event - other services handle independently
    this.eventEmitter.emit('user.registered', { userId: user.id, email: user.email });

    return user;
  }
}
```

**If found:** Replace with event emission using EventEmitter2.

### Step 2: Install EventEmitter2
**Run in terminal:**

```bash
bun add @nestjs/event-emitter
```

### Step 3: Configure EventEmitter2 Module
**File:** `src/app.module.ts`

```typescript
// ✅ REQUIRED: Import EventEmitter2 module
import { Module } from '@nestjs/common';
import { EventEmitterModule } from '@nestjs/event-emitter';

@Module({
  imports: [
    EventEmitterModule.forRoot({
      wildcard: false,     // Set to true to use wildcard events
      delimiter: '.',      // Delimiter for wildcard events
      newListener: false,  // Show when a listener is added
      removeListener: false,
      maxListeners: 10,    // Maximum listeners per event
      verboseMemoryLeak: true,
      ignoreErrors: false,
    }),
    // ... other modules
  ],
})
export class AppModule {}
```

### Step 4: Define Domain Events
**File:** `src/users/events/user-registered.event.ts`

```typescript
// ✅ REQUIRED: Strongly typed event
export class UserRegisteredEvent {
  constructor(
    public readonly userId: string,
    public readonly email: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}
```

### Step 5: Emit Events in Services
**File:** `src/users/users.service.ts`

```typescript
// ✅ REQUIRED: Emit events
import { Injectable } from '@nestjs/common';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { UserRegisteredEvent } from './events/user-registered.event';

@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private eventEmitter: EventEmitter2,
  ) {}

  async register(data: RegisterDto) {
    const user = await this.prisma.user.create({ data });

    // ✅ Emit strongly typed event
    this.eventEmitter.emit(
      'user.registered',
      new UserRegisteredEvent(user.id, user.email)
    );

    return user;
  }
}
```

### Step 6: Create Event Listeners
**File:** `src/email/listeners/user.listener.ts`

```typescript
// ✅ REQUIRED: Event listener
import { OnEvent } from '@nestjs/event-emitter';
import { Injectable } from '@nestjs/common';
import { UserRegisteredEvent } from '../../users/events/user-registered.event';

@Injectable()
export class UserListener {
  constructor(private emailService: EmailService) {}

  @OnEvent('user.registered')
  async handleUserRegistered(event: UserRegisteredEvent) {
    await this.emailService.sendWelcomeEmail(event.email);
  }
}
```

**File:** `src/email/email.module.ts`

```typescript
// ✅ REQUIRED: Register listeners in module
import { Module } from '@nestjs/common';
import { EmailService } from './email.service';
import { UserListener } from './listeners/user.listener';

@Module({
  providers: [EmailService, UserListener],  // ✅ Register listener
  exports: [EmailService],
})
export class EmailModule {}
```

## Installation

```bash
bun add @nestjs/event-emitter
```

## Quick Reference Checklist

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
// users/users.service.ts - Event-driven ✅
import { Injectable } from '@nestjs/common';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class UsersService {
  constructor(
    private prisma: PrismaService,
    private eventEmitter: EventEmitter2,
  ) {}

  async register(data: RegisterDto) {
    const user = await this.prisma.user.create({ data });

    // ✅ Emit event - decoupled from side effects
    this.eventEmitter.emit('user.registered', new UserRegisteredEvent(
      user.id,
      user.email,
      user.name,
    ));

    return user;
  }

  async deleteUser(userId: string) {
    await this.prisma.user.delete({ where: { id: userId } });

    // ✅ Emit event - other modules handle cleanup
    this.eventEmitter.emit('user.deleted', new UserDeletedEvent(userId));
  }
}

// users/events/user-registered.event.ts ✅
export class UserRegisteredEvent {
  constructor(
    public readonly userId: string,
    public readonly email: string,
    public readonly name: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

// users/events/user-deleted.event.ts ✅
export class UserDeletedEvent {
  constructor(
    public readonly userId: string,
    public readonly timestamp: Date = new Date(),
  ) {}
}

// email/listeners/user.listener.ts ✅
import { OnEvent } from '@nestjs/event-emitter';
import { Injectable } from '@nestjs/common';
import { UserRegisteredEvent } from '../../users/events/user-registered.event';

@Injectable()
export class EmailListener {
  constructor(private emailService: EmailService) {}

  @OnEvent('user.registered')
  async handleUserRegistered(event: UserRegisteredEvent) {
    await this.emailService.sendVerificationEmail(event.email);
  }
}

// notification/listeners/user.listener.ts ✅
import { OnEvent } from '@nestjs/event-emitter';
import { Injectable } from '@nestjs/common';
import { UserRegisteredEvent, UserDeletedEvent } from '../../users/events/user-events';

@Injectable()
export class NotificationListener {
  constructor(private notificationService: NotificationService) {}

  @OnEvent('user.registered')
  async handleUserRegistered(event: UserRegisteredEvent) {
    await this.notificationService.sendPushNotification(
      event.userId,
      `Welcome ${event.name}!`,
    );
  }

  @OnEvent('user.deleted')
  async handleUserDeleted(event: UserDeletedEvent) {
    await this.notificationService.clearAllNotifications(event.userId);
  }
}

// audit/listeners/user.listener.ts ✅
import { OnEvent } from '@nestjs/event-emitter';
import { Injectable } from '@nestjs/common';
import { UserRegisteredEvent, UserDeletedEvent } from '../../users/events/user-events';

@Injectable()
export class AuditListener {
  constructor(private auditService: AuditService) {}

  @OnEvent('user.registered')
  async handleUserRegistered(event: UserRegisteredEvent) {
    await this.auditService.log({
      action: 'USER_REGISTERED',
      userId: event.userId,
      timestamp: event.timestamp,
    });
  }

  @OnEvent('user.deleted')
  async handleUserDeleted(event: UserDeletedEvent) {
    await this.auditService.log({
      action: 'USER_DELETED',
      userId: event.userId,
      timestamp: event.timestamp,
    });
  }
}

// app.module.ts ✅
import { Module } from '@nestjs/common';
import { EventEmitterModule } from '@nestjs/event-emitter';

@Module({
  imports: [
    EventEmitterModule.forRoot({
      wildcard: false,
      delimiter: '.',
      maxListeners: 20,
      verboseMemoryLeak: true,
    }),
    UsersModule,
    EmailModule,     // Contains EmailListener
    NotificationModule,  // Contains NotificationListener
    AuditModule,     // Contains AuditListener
  ],
})
export class AppModule {}
```

## Advanced Event Patterns

### Async Event Handling

```typescript
// Event listeners are async by default
@Injectable()
export class EmailListener {
  @OnEvent('user.registered', { async: true })
  async handleUserRegistered(event: UserRegisteredEvent) {
    // This runs asynchronously, doesn't block the response
    await this.emailService.sendVerificationEmail(event.email);
  }
}
```

### Wildcard Events

```typescript
// Configure wildcard in app.module.ts
EventEmitterModule.forRoot({
  wildcard: true,
  delimiter: '.',
})

// Listen to all user events
@Injectable()
export class AnalyticsListener {
  @OnEvent('user.*')
  handleAnyUserEvent(eventName: string, payload: any) {
    // eventName: 'user.registered', 'user.deleted', etc.
    this.analyticsService.track(eventName, payload);
  }
}

// Listen to all events
@Injectable()
export class LoggingListener {
  @OnEvent('*')
  logAllEvents(eventName: string, payload: any) {
    this.logger.log(`Event: ${eventName}`, payload);
  }
}
```

### Event Priorities

```typescript
// Listeners can specify priority (higher = earlier execution)
@Injectable()
export class ValidationListener {
  @OnEvent('order.created', { priority: 10 })  // Runs first
  async validateOrder(event: OrderCreatedEvent) {
    // Validate before processing
  }
}

@Injectable()
export class InventoryListener {
  @OnEvent('order.created', { priority: 5 })  // Runs second
  async reserveInventory(event: OrderCreatedEvent) {
    // Reserve inventory
  }
}

@Injectable()
export class NotificationListener {
  @OnEvent('order.created', { priority: 1 })  // Runs last
  async notifyCustomer(event: OrderCreatedEvent) {
    // Send confirmation
  }
}
```

### Error Handling in Listeners

```typescript
@Injectable()
export class EmailListener {
  @OnEvent('user.registered')
  async handleUserRegistered(event: UserRegisteredEvent) {
    try {
      await this.emailService.sendVerificationEmail(event.email);
    } catch (error) {
      // Log error but don't throw - other listeners should still execute
      this.logger.error(`Failed to send email to ${event.email}`, error);

      // Optionally emit an error event
      this.eventEmitter.emit('email.failed', {
        userId: event.userId,
        error: error.message,
      });
    }
  }
}
```

## Saga Pattern for Complex Workflows

```typescript
// events/order.events.ts
export class OrderCreatedEvent {
  constructor(public readonly orderId: string, public readonly userId: string) {}
}

export class PaymentCompletedEvent {
  constructor(public readonly orderId: string, public readonly amount: number) {}
}

export class InventoryReservedEvent {
  constructor(public readonly orderId: string, public readonly items: OrderItem[]) {}
}

export class OrderCompletedEvent {
  constructor(public readonly orderId: string) {}
}

// orders/saga/order-saga.ts ✅
import { Injectable } from '@nestjs/common';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { OrderCreatedEvent, PaymentCompletedEvent, InventoryReservedEvent } from '../events/order.events';

@Injectable()
export class OrderSaga {
  constructor(private eventEmitter: EventEmitter2) {}

  @OnEvent('order.created')
  async handleOrderCreated(event: OrderCreatedEvent) {
    // Step 1: Process payment
    const paymentResult = await this.paymentService.charge(event.orderId);

    if (paymentResult.success) {
      // Emit payment completed event
      this.eventEmitter.emit('payment.completed', new PaymentCompletedEvent(
        event.orderId,
        paymentResult.amount,
      ));
    } else {
      // Emit payment failed event
      this.eventEmitter.emit('payment.failed', { orderId: event.orderId });
    }
  }

  @OnEvent('payment.completed')
  async handlePaymentCompleted(event: PaymentCompletedEvent) {
    // Step 2: Reserve inventory
    const inventoryResult = await this.inventoryService.reserve(event.orderId);

    if (inventoryResult.success) {
      this.eventEmitter.emit('inventory.reserved', new InventoryReservedEvent(
        event.orderId,
        inventoryResult.items,
      ));
    } else {
      // Refund payment
      await this.paymentService.refund(event.orderId);
      this.eventEmitter.emit('order.failed', { orderId: event.orderId });
    }
  }

  @OnEvent('inventory.reserved')
  async handleInventoryReserved(event: InventoryReservedEvent) {
    // Step 3: Complete order
    await this.orderService.markAsCompleted(event.orderId);
    this.eventEmitter.emit('order.completed', new OrderCompletedEvent(event.orderId));
  }
}
```

## Event Versioning and Backwards Compatibility

```typescript
// events/user.events.v2.ts
export class UserRegisteredEventV2 {
  constructor(
    public readonly userId: string,
    public readonly email: string,
    public readonly metadata: UserMetadata,  // New field
  ) {}

  // Static method for backwards compatibility
  static fromV1(v1Event: UserRegisteredEvent): UserRegisteredEventV2 {
    return new UserRegisteredEventV2(
      v1Event.userId,
      v1Event.email,
      { source: 'migration', version: '1->2' },
    );
  }
}

// Listen to both versions during migration
@Injectable()
export class EmailListener {
  @OnEvent('user.registered.v1')
  async handleV1(event: UserRegisteredEvent) {
    const v2Event = UserRegisteredEventV2.fromV1(event);
    await this.processUserRegistration(v2Event);
  }

  @OnEvent('user.registered.v2')
  async handleV2(event: UserRegisteredEventV2) {
    await this.processUserRegistration(event);
  }

  private async processUserRegistration(event: UserRegisteredEventV2) {
    await this.emailService.sendWelcomeEmail(event.email);
  }
}
```

## Testing Event-Driven Architecture

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

## Best Practices Summary

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
