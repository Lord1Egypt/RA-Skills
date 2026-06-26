---
title: Use Logger with Module Context for Debugging
impact: MEDIUM
impactDescription: Improves debugging with contextual log messages
section: 4
tags: logging, error-handling, debugging, logger, context
---

Using `console.log()` or generic loggers without context makes debugging difficult in production. NestJS's built-in Logger with module context prefixes each message with the source module, making it easy to trace where logs originate.

## For AI Agents

When implementing or reviewing logging, **always** follow these steps:

### Step 1: Check for Console Logging or Contextless Loggers
**Pattern to check:** Look for `console.log()`, `console.error()`, or Logger without context parameter.

```typescript
// ❌ WRONG - Console logging with no context
console.log('User created:', user);
console.error('Error:', error);

// ❌ WRONG - Logger without module context
@Injectable()
export class TasksService {
  private logger = new Logger(); // ❌ No context

  createTask(dto: CreateTaskDto) {
    this.logger.log('Creating task'); // ❌ No module prefix
  }
}

// ❌ WRONG - Generic context
@Injectable()
export class TasksService {
  private logger = new Logger('Service'); // ❌ Too generic
}
```

**If found:** Replace with contextual Logger.

### Step 2: Create Logger with Class Context

```typescript
// ✅ REQUIRED: Use class name as context
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class TasksService {
  // ✅ Logger with class name as context
  private readonly logger = new Logger(TasksService.name);

  createTask(dto: CreateTaskDto) {
    this.logger.log('Creating task');
    // Output: [TasksService] Creating task
  }
}
```

### Step 3: Use Appropriate Log Levels

```typescript
// ✅ REQUIRED: Use appropriate log levels
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  // ✅ LOG - General information
  findAll() {
    this.logger.log('Retrieving all tasks');
    return this.tasksRepository.findAll();
  }

  // ✅ VERBOSE - Detailed debugging (disabled by default)
  findAll(user: User, filters: GetTasksFilterDto) {
    this.logger.verbose(`User "${user.username}" retrieving tasks. Filters: ${JSON.stringify(filters)}`);
    return this.tasksRepository.findAll(filters, user);
  }

  // ✅ DEBUG - Debugging information
  async processData(data: any) {
    this.logger.debug('Processing data', { data });
    // ...
  }

  // ✅ WARN - Warning messages
  async updateTask(id: string, dto: UpdateTaskDto) {
    this.logger.warn(`Task ${id} is being updated`);
    // ...
  }

  // ✅ ERROR - Error messages
  async deleteTask(id: string) {
    this.logger.error(`Task ${id} not found`, id); // context can be any type
    throw new NotFoundException(`Task ${id} not found`);
  }

  // ✅ ERROR - With stack trace
  async processWithError() {
    try {
      // ...
    } catch (error) {
      this.logger.error('Processing failed', error.stack); // Pass stack trace
      throw error;
    }
  }
}
```

### Step 4: Log Important Events

```typescript
// ✅ REQUIRED: Log lifecycle events
import { Injectable, Logger, OnModuleInit, OnModuleDestroy } from '@nestjs/common';

@Injectable()
export class TasksService implements OnModuleInit, OnModuleDestroy {
  private readonly logger = new Logger(TasksService.name);

  onModuleInit() {
    this.logger.log('TasksService initialized');
  }

  onModuleDestroy() {
    this.logger.log('TasksService destroyed');
  }
}

// ✅ Log important business events
@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  async createTask(dto: CreateTaskDto, user: User) {
    this.logger.log(`Creating task "${dto.title}" for user "${user.email}"`);

    const task = await this.tasksRepository.create(dto, user);

    this.logger.log(`Task created with ID "${task.id}"`);
    return task;
  }

  async completeTask(id: string, user: User) {
    const task = await this.tasksRepository.findOne(id, user);

    this.logger.verbose(`User "${user.email}" marking task "${id}" as complete`);

    task.status = TaskStatus.DONE;
    await this.tasksRepository.save(task);

    this.logger.log(`Task "${id}" completed by user "${user.email}"`);
    return task;
  }
}
```

### Step 5: Log Request Details in Controllers

```typescript
// ✅ OPTIONAL: Log request details for debugging
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';
import { GetUser } from '../auth/decorators/get-user.decorator';
import { User } from '../users/entities/user.entity';

@Controller('tasks')
export class TasksController {
  private readonly logger = new Logger(TasksController.name);

  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto, @GetUser() user: User) {
    // ✅ Log user action with context
    this.logger.verbose(
      `User "${user.username}" retrieving tasks. Filters: ${JSON.stringify(filterDto)}`,
    );

    return this.tasksService.findAll(filterDto, user);
  }

  @Post()
  create(@Body() dto: CreateTaskDto, @GetUser() user: User) {
    // ✅ Log creation attempt
    this.logger.log(`User "${user.username}" creating task "${dto.title}"`);

    return this.tasksService.create(dto, user);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @GetUser() user: User) {
    this.logger.verbose(`User "${user.username}" retrieving task "${id}"`);

    return this.tasksService.findOne(id, user);
  }
}
```

### Step 6: Handle Errors with Context

```typescript
// ✅ REQUIRED: Log errors with context
import { Injectable, Logger, NotFoundException } from '@nestjs/common';

@Injectable()
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  async findOne(id: string, user: User): Promise<Task> {
    try {
      const task = await this.tasksRepository.findOne(id, user);

      if (!task) {
        // ✅ Log error with context before throwing
        this.logger.warn(`Task "${id}" not found for user "${user.id}"`);
        throw new NotFoundException(`Task "${id}" not found`);
      }

      return task;
    } catch (error) {
      // ✅ Log unexpected errors
      if (error instanceof NotFoundException) {
        throw error;
      }

      this.logger.error(
        `Failed to retrieve task "${id}"`,
        error.stack, // Stack trace for debugging
      );
      throw error;
    }
  }

  async updateTask(id: string, dto: UpdateTaskDto, user: User): Promise<Task> {
    try {
      const task = await this.findOne(id, user);

      this.logger.log(`Updating task "${id}" with data: ${JSON.stringify(dto)}`);

      Object.assign(task, dto);
      return this.tasksRepository.save(task);
    } catch (error) {
      this.logger.error(
        `Failed to update task "${id}"`,
        error.stack,
      );
      throw error;
    }
  }
}
```

### Step 7: Create Custom Logger Service (Optional)

```typescript
// ✅ OPTIONAL: Custom logger for consistent formatting
// common/logging/logger.service.ts
import { Injectable, LoggerService, Scope } from '@nestjs/common';
import { v4 as uuidv4 } from 'uuid';

@Injectable({ scope: Scope.TRANSIENT })
export class AppLogger implements LoggerService {
  private context: string;
  private requestId: string;

  setContext(context: string) {
    this.context = context;
  }

  setRequestId(requestId: string) {
    this.requestId = requestId;
  }

  log(message: any, ...optionalParams: any[]) {
    this.printMessage(message, 'LOG', optionalParams);
  }

  error(message: any, ...optionalParams: any[]) {
    this.printMessage(message, 'ERROR', optionalParams);
  }

  warn(message: any, ...optionalParams: any[]) {
    this.printMessage(message, 'WARN', optionalParams);
  }

  debug(message: any, ...optionalParams: any[]) {
    this.printMessage(message, 'DEBUG', optionalParams);
  }

  verbose(message: any, ...optionalParams: any[]) {
    this.printMessage(message, 'VERBOSE', optionalParams);
  }

  private printMessage(message: any, level: string, optionalParams: any[]) {
    const timestamp = new Date().toISOString();
    const requestId = this.requestId ? ` [${this.requestId}]` : '';
    const context = this.context ? ` [${this.context}]` : '';

    console.log(
      `[${timestamp}]${requestId}${context} [${level}] ${message}`,
      ...optionalParams,
    );
  }
}

// ✅ Use custom logger
// tasks/tasks.service.ts
import { Injectable } from '@nestjs/common';
import { AppLogger } from '../../common/logging/logger.service';

@Injectable()
export class TasksService {
  private readonly logger = new AppLogger();
  private readonly context = TasksService.name;

  constructor() {
    this.logger.setContext(this.context);
  }

  findAll() {
    this.logger.log('Retrieving all tasks');
    return this.tasksRepository.findAll();
  }
}
```

## Installation

```bash
# No packages needed - Logger is built-in to NestJS
# Just import from @nestjs/common
```

**Incorrect:**

```typescript
// tasks/tasks.service.ts - Console logging 🚨
import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksService {
  constructor(private tasksRepository: TasksRepository) {}

  // ❌ Console.log - no context, no levels
  async createTask(dto: CreateTaskDto, user: User) {
    console.log('Creating task'); // ❌ No module context
    const task = await this.tasksRepository.create(dto, user);
    console.log('Task created:', task); // ❌ No structure
    return task;
  }

  // ❌ Console.error for errors
  async deleteTask(id: string) {
    try {
      return await this.tasksRepository.delete(id);
    } catch (error) {
      console.error('Error deleting task:', error); // ❌ No context
      throw error;
    }
  }

  // ❌ No logging at all
  async updateTask(id: string, dto: UpdateTaskDto) {
    return this.tasksRepository.update(id, dto); // ❌ Silent operation
  }
}

// tasks/tasks.controller.ts - No logging 🚨
import { Controller, Get, Post, Body } from '@nestjs/common';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto) {
    // ❌ No logging - hard to debug in production
    return this.tasksService.findAll(filterDto);
  }

  @Post()
  create(@Body() dto: CreateTaskDto) {
    // ❌ No audit trail
    return this.tasksService.create(dto);
  }
}
```

**Correct:**

```typescript
// tasks/tasks.service.ts - Contextual logging ✅
import { Injectable, Logger } from '@nestjs/common';

@Injectable()
export class TasksService {
  // ✅ Logger with class context
  private readonly logger = new Logger(TasksService.name);

  constructor(private tasksRepository: TasksRepository) {}

  // ✅ Log important operations
  async createTask(dto: CreateTaskDto, user: User) {
    this.logger.log(`Creating task "${dto.title}" for user "${user.email}"`);

    const task = await this.tasksRepository.create(dto, user);

    this.logger.log(`Task created with ID "${task.id}"`);
    return task;
  }

  // ✅ Log errors with context
  async deleteTask(id: string, user: User) {
    this.logger.log(`User "${user.email}" deleting task "${id}"`);

    try {
      await this.tasksRepository.delete(id, user);
      this.logger.log(`Task "${id}" deleted`);
    } catch (error) {
      this.logger.error(
        `Failed to delete task "${id}"`,
        error.stack,
      );
      throw error;
    }
  }

  // ✅ Verbose logging for debugging
  async getTasks(filterDto: GetTasksFilterDto, user: User) {
    this.logger.verbose(
      `User "${user.email}" retrieving tasks with filters: ${JSON.stringify(filterDto)}`,
    );
    return this.tasksRepository.findAll(filterDto, user);
  }

  // ✅ Warning for edge cases
  async updateTask(id: string, dto: UpdateTaskDto, user: User) {
    const task = await this.tasksRepository.findOne(id, user);

    if (task.status !== dto.status) {
      this.logger.warn(`Task "${id}" status changing from "${task.status}" to "${dto.status}"`);
    }

    Object.assign(task, dto);
    const updated = await this.tasksRepository.save(task);

    this.logger.log(`Task "${id}" updated`);
    return updated;
  }
}

// tasks/tasks.controller.ts - Request logging ✅
import { Controller, Get, Post, Body, Query } from '@nestjs/common';
import { GetUser } from '../auth/decorators/get-user.decorator';
import { User } from '../users/entities/user.entity';

@Controller('tasks')
export class TasksController {
  private readonly logger = new Logger(TasksController.name);

  constructor(private tasksService: TasksService) {}

  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto, @GetUser() user: User) {
    // ✅ Log request with user context
    this.logger.verbose(
      `User "${user.username}" fetching tasks. Filters: ${JSON.stringify(filterDto)}`,
    );
    return this.tasksService.getTasks(filterDto, user);
  }

  @Post()
  create(@Body() dto: CreateTaskDto, @GetUser() user: User) {
    // ✅ Log creation
    this.logger.log(`User "${user.username}" creating task "${dto.title}"`);
    return this.tasksService.createTask(dto, user);
  }

  @Get(':id')
  findOne(@Param('id') id: string, @GetUser() user: User) {
    // ✅ Log access
    this.logger.verbose(`User "${user.username}" fetching task "${id}"`);
    return this.tasksService.findOne(id, user);
  }
}

// main.ts - Configure log level ✅
async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    // ✅ Set log level based on environment
    logger: process.env.NODE_ENV === 'production'
      ? ['log', 'error', 'warn']
      : ['log', 'error', 'warn', 'debug', 'verbose'],
  });

  await app.listen(3000);
}
```

## Advanced: Request ID Logging

```typescript
// ✅ Add request ID to all logs in a request
// common/middleware/request-id.middleware.ts
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class RequestIdMiddleware implements NestMiddleware {
  private logger = new Logger(RequestIdMiddleware.name);

  use(req: Request, res: Response, next: NextFunction) {
    const id = uuidv4();
    req['id'] = id;

    // ✅ Add request ID to response header
    res.setHeader('X-Request-ID', id);

    this.logger.verbose(`[${id}] ${req.method} ${req.url}`);

    next();
  }
}

// tasks/tasks.service.ts - Use request ID ✅
import { Injectable, Logger, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.REQUEST })
export class TasksService {
  private readonly logger = new Logger(TasksService.name);

  constructor(@Inject(REQUEST) private request: Request) {
    // ✅ Use request ID in logs
    const requestId = request['id'];
    if (requestId) {
      this.logger.setContext(`[${requestId}] ${TasksService.name}`);
    }
  }

  findAll() {
    this.logger.log('Retrieving all tasks');
    // Output: [abc-123] [TasksService] Retrieving all tasks
    return this.tasksRepository.findAll();
  }
}
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use `Logger(Class.name)` | Context prefix in every log message |
| Log at appropriate levels | Control verbosity by environment |
| Log important business events | Audit trail for debugging |
| Log errors with stack traces | Easier debugging in production |
| Use verbose for debugging | Disabled by default, enabled when needed |
| Log user actions | Security audit trail |

**Sources:**
- [NestJS Logger Documentation](https://docs.nestjs.com/techniques/logger)
- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application

**See also:** `error-handling-structured-logging.md` for Winston/structured logging in production.
