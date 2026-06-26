---
title: Implement Proper Logging Strategy
impact: HIGH
section: 4
impactDescription: Enables debugging, monitoring, and audit trails
tags: logging, monitoring, debugging, production
---

## Implement Proper Logging Strategy

> **Note:** For NestJS Logger with module context patterns, see `error-handling-logger-context.md`. This rule focuses on Winston and structured JSON logging for production environments.

Console.log lacks structure, levels, and persistence. NestJS Logger with Winston provides structured JSON logs for production monitoring. **Log all errors, warnings, and business events.**

**Incorrect (console.log debugging):**

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

**Correct (structured logging):**

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