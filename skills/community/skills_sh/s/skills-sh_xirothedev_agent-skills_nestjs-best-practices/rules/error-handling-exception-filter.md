---
title: Enable Global Exception Filter
impact: CRITICAL
section: 4
impactDescription: Prevents stack trace leaks in production
tags: security, error-handling, production, exceptions
---

## Enable Global Exception Filter

Default Express errors leak stack traces and database info to clients. Global filters catch all exceptions and return safe HTTP responses. **Hide internal errors from users.**

> **Hint**: Use global exception filters to standardize error responses, log errors properly, and prevent sensitive information leaks. Different responses for development vs production environments.

## Why Global Exception Filters Matter

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

### Basic Implementation

```typescript
// common/filters/all-exceptions.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
  Logger,
} from '@nestjs/common';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? exception.message
        : 'Internal server error';

    // ✅ Log the full error for debugging
    this.logger.error(
      `${request.method} ${request.url}`,
      exception instanceof Error ? exception.stack : exception,
    );

    // ✅ Return safe response to client
    response.status(status).json({
      statusCode: status,
      message,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}

// main.ts
import { AllExceptionsFilter } from './common/filters/all-exceptions.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Apply global filter
  app.useGlobalFilters(new AllExceptionsFilter());

  await app.listen(3000);
}
```

### Environment-Aware Exception Filter

```typescript
// common/filters/all-exceptions.filter.ts
import { ConfigService } from '@nestjs/config';

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  constructor(private configService: ConfigService) {}

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const isDevelopment = this.configService.get('NODE_ENV') === 'development';

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    // Build error response
    const errorResponse: any = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
    };

    // ✅ Development: show detailed info
    if (isDevelopment) {
      errorResponse.message =
        exception instanceof HttpException
          ? exception.message
          : exception instanceof Error
          ? exception.message
          : 'Unknown error';

      if (exception instanceof Error && exception.stack) {
        errorResponse.stack = exception.stack;
      }
    }
    // ✅ Production: hide details
    else {
      if (status >= 500) {
        errorResponse.message = 'Internal server error';
      } else {
        errorResponse.message =
          exception instanceof HttpException
            ? exception.message
            : 'An error occurred';
      }
    }

    // Log error
    this.logger.error(
      `${request.method} ${request.url} - Status: ${status}`,
      exception instanceof Error ? exception.stack : exception,
    );

    response.status(status).json(errorResponse);
  }
}

// main.ts - Use dependency injection
app.useGlobalFilters(new AllExceptionsFilter(app.get(ConfigService)));
```

## Custom Business Exceptions

Create domain-specific exceptions for better error handling:

```typescript
// common/exceptions/business.exception.ts
import { HttpException, HttpStatus } from '@nestjs/common';

export class BusinessException extends HttpException {
  constructor(message: string, status: HttpStatus = HttpStatus.BAD_REQUEST) {
    super(
      {
        statusCode: status,
        message,
        error: 'BUSINESS_ERROR',
      },
      status,
    );
  }
}

// common/exceptions/resource-not-found.exception.ts
export class ResourceNotFoundException extends BusinessException {
  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`, HttpStatus.NOT_FOUND);
  }
}

// common/exceptions/invalid-state.exception.ts
export class InvalidStateException extends BusinessException {
  constructor(message: string) {
    super(message, HttpStatus.CONFLICT);
  }
}

// Usage in services
@Injectable()
export class OrdersService {
  async cancelOrder(orderId: string) {
    const order = await this.findOne(orderId);

    if (order.status === OrderStatus.SHIPPED) {
      // ✅ Business logic error with clear message
      throw new InvalidStateException(
        'Cannot cancel order: already shipped',
      );
    }

    order.status = OrderStatus.CANCELLED;
    return this.repository.save(order);
  }

  async findOne(orderId: string) {
    const order = await this.repository.findOne(orderId);

    if (!order) {
      // ✅ Resource not found error
      throw new ResourceNotFoundException('Order', orderId);
    }

    return order;
  }
}
```

## HTTP Exception Filter

Handle HTTP exceptions specifically:

```typescript
// common/filters/http-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  Logger,
} from '@nestjs/common';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(HttpExceptionFilter.name);

  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status = exception.getStatus();
    const exceptionResponse = exception.getResponse();

    const errorResponse: any = {
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
    };

    // Handle different exception response types
    if (typeof exceptionResponse === 'string') {
      errorResponse.message = exceptionResponse;
    } else if (typeof exceptionResponse === 'object') {
      errorResponse.message = (exceptionResponse as any).message;
      errorResponse.error = (exceptionResponse as any).error;

      // Include validation errors if present
      if ((exceptionResponse as any).message instanceof Array) {
        errorResponse.errors = (exceptionResponse as any).message;
      }
    }

    // Log 4xx and 5xx errors
    if (status >= 400) {
      this.logger.warn(
        `${request.method} ${request.url} - ${status}: ${JSON.stringify(errorResponse.message)}`,
      );
    }

    response.status(status).json(errorResponse);
  }
}
```

## Prisma Exception Filter

Handle database-specific errors safely:

```typescript
// common/filters/prisma-exception.filter.ts
import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { Prisma } from '@prisma/client';

@Catch(Prisma.PrismaClientKnownRequestError)
export class PrismaExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(PrismaExceptionFilter.name);

  catch(exception: Prisma.PrismaClientKnownRequestError, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let message = 'Database error occurred';

    // ✅ Map Prisma errors to safe messages
    switch (exception.code) {
      case 'P2002':
        status = HttpStatus.CONFLICT;
        message = 'A record with this value already exists';
        break;
      case 'P2025':
        status = HttpStatus.NOT_FOUND;
        message = 'Record not found';
        break;
      case 'P2003':
        status = HttpStatus.BAD_REQUEST;
        message = 'Related record not found';
        break;
      default:
        // Log unexpected errors with details
        this.logger.error(
          `Prisma error ${exception.code}: ${exception.message}`,
        );
        message = 'An error occurred while processing your request';
    }

    response.status(status).json({
      statusCode: status,
      message,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}
```

## Combining Multiple Filters

Use multiple filters for different exception types:

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Order matters - more specific filters first
  app.useGlobalFilters(
    new PrismaExceptionFilter(),      // Catch Prisma errors
    new HttpExceptionFilter(),         // Catch HTTP exceptions
    new AllExceptionsFilter(),         // Catch everything else
  );

  await app.listen(3000);
}
```

## Register Filters as Global Providers

Better approach using dependency injection:

```typescript
// main.ts
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ✅ Use APP_FILTER to enable DI
    app.get(PrismaExceptionFilter),
    app.get(HttpExceptionFilter),
    app.get(AllExceptionsFilter),
  );

  await app.listen(3000);
}

// Or in app.module.ts
import { APP_FILTER } from '@nestjs/core';

@Module({
  providers: [
    {
      provide: APP_FILTER,
      useClass: AllExceptionsFilter,
    },
    {
      provide: APP_FILTER,
      useClass: HttpExceptionFilter,
    },
  ],
})
export class AppModule {}
```

## Standardized Error Response Format

Define a consistent error response structure:

```typescript
// common/interfaces/error-response.interface.ts
export interface ErrorResponse {
  statusCode: number;
  message: string | string[];
  error?: string;
  timestamp: string;
  path: string;
  errors?: Record<string, string[]>;  // For validation errors
}

// common/filters/all-exceptions.filter.ts
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const errorResponse: ErrorResponse = {
      statusCode: status,
      message: this.getErrorMessage(exception),
      timestamp: new Date().toISOString(),
      path: request.url,
    };

    response.status(status).json(errorResponse);
  }

  private getErrorMessage(exception: unknown): string {
    if (exception instanceof HttpException) {
      const response = exception.getResponse();
      if (typeof response === 'string') {
        return response;
      }
      return (response as any).message || 'An error occurred';
    }
    if (exception instanceof Error) {
      return exception.message;
    }
    return 'Internal server error';
  }
}
```

## Exception Filter with Logging Service

Integrate with external logging services:

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

## Summary: Exception Filter Best Practices

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
