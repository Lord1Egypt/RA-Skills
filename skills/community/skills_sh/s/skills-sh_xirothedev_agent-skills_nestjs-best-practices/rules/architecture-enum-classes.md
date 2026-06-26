---
title: Use Enum Classes for Type-Safe Values
impact: MEDIUM
impactDescription: Prevents typos and improves autocomplete
section: 3
tags: architecture, enums, types, type-safety, autocomplete
---

Using string literals for status values, types, or constants leads to typos, no autocomplete support, and runtime errors. TypeScript enums provide type-safe values with compile-time checking and full IDE autocomplete support.

## For AI Agents

When implementing or reviewing constant values, **always** follow these steps:

### Step 1: Check for String Literals
**Pattern to check:** Look for string literals assigned to variables, compared in conditionals, or used as status/type values.

```typescript
// ❌ WRONG - String literals with no type safety
async updateStatus(id: string, status: string) {
  const task = await this.repo.findOne(id);
  task.status = status; // ❌ Any string allowed, typos possible
  return this.repo.save(task);
}

// ❌ WRONG - Typo-prone comparisons
if (task.status === 'opne') { // ❌ Typo! Should be 'open'
  // ...
}

// ❌ WRONG - No autocomplete
function createTask(status: string) {
  // What values are valid? No hints.
}

// ❌ WRONG - Inconsistent casing
task.status = 'OPEN';
task.status = 'open';
task.status = 'Open';
```

**If found:** Replace with enums.

### Step 2: Create Enum File
**File:** `tasks/task-status.enum.ts`

```typescript
// ✅ REQUIRED: Define enum with valid values
export enum TaskStatus {
  OPEN = 'OPEN',
  IN_PROGRESS = 'IN_PROGRESS',
  DONE = 'DONE',
}

// Alternative: PascalCase values
export enum TaskStatus {
  OPEN = 'Open',
  IN_PROGRESS = 'In Progress',
  DONE = 'Done',
}

// Alternative: Numeric values (not recommended for APIs)
export enum TaskStatus {
  OPEN = 0,
  IN_PROGRESS = 1,
  DONE = 2,
}
```

### Step 3: Use Enum in Entity
**File:** `tasks/task.entity.ts`

```typescript
// ✅ REQUIRED: Use enum type in entity
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
import { TaskStatus } from './task-status.enum';

@Entity()
export class Task {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  title: string;

  @Column({
    type: 'enum',
    enum: TaskStatus,
    default: TaskStatus.OPEN,
  })
  status: TaskStatus;
}
```

### Step 4: Use Enum in DTOs
**File:** `tasks/dto/create-task.dto.ts`

```typescript
// ✅ REQUIRED: Validate enum values in DTOs
import { IsEnum, IsOptional, IsString, MinLength } from 'class-validator';
import { TaskStatus } from '../task-status.enum';

export class CreateTaskDto {
  @IsString()
  @MinLength(3)
  title: string;

  @IsOptional()
  @IsEnum(TaskStatus, {
    message: `Status must be one of: ${Object.values(TaskStatus).join(', ')}`,
  })
  status?: TaskStatus;
}

// ✅ OPTIONAL: Update DTO with enum
export class UpdateTaskStatusDto {
  @IsEnum(TaskStatus, {
    message: `Status must be one of: ${Object.values(TaskStatus).join(', ')}`,
  })
  status: TaskStatus;
}
```

### Step 5: Use Enum in Service and Controller

```typescript
// ✅ REQUIRED: Use enum in business logic
// tasks/tasks.service.ts
import { TaskStatus } from './task-status.enum';

@Injectable()
export class TasksService {
  async updateStatus(id: string, status: TaskStatus) {
    // ✅ Type-safe, autocomplete works
    const task = await this.repo.findOne(id);
    task.status = status;
    return this.repo.save(task);
  }

  async getOpenTasks() {
    // ✅ Compile-time checking
    return this.repo.find({ where: { status: TaskStatus.OPEN } });
  }

  async completeTask(id: string) {
    const task = await this.repo.findOne(id);
    // ✅ Autocomplete shows OPEN, IN_PROGRESS, DONE
    task.status = TaskStatus.DONE;
    return this.repo.save(task);
  }
}

// tasks/tasks.controller.ts
@Controller('tasks')
export class TasksController {
  @Patch(':id/status')
  updateStatus(
    @Param('id') id: string,
    @Body() dto: UpdateTaskStatusDto,
  ) {
    // ✅ dto.status is typed as TaskStatus
    return this.tasksService.updateStatus(id, dto.status);
  }
}
```

### Step 6: Create Enums for Other Constants

```typescript
// ✅ OPTIONAL: Enums for other constant values
// users/user-role.enum.ts
export enum UserRole {
  ADMIN = 'ADMIN',
  USER = 'USER',
  GUEST = 'GUEST',
}

// common/enums/log-level.enum.ts
export enum LogLevel {
  DEBUG = 'debug',
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
}

// orders/order-status.enum.ts
export enum OrderStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
}

// payments/payment-method.enum.ts
export enum PaymentMethod {
  CREDIT_CARD = 'credit_card',
  DEBIT_CARD = 'debit_card',
  PAYPAL = 'paypal',
  BANK_TRANSFER = 'bank_transfer',
}
```

### Step 7: Use Enum in Validation and Guards

```typescript
// ✅ OPTIONAL: Enum-based guards
// guards/admin.guard.ts
import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { UserRole } from '../users/user-role.enum';

@Injectable()
export class AdminGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    // ✅ Type-safe comparison
    return user?.role === UserRole.ADMIN;
  }
}

// ✅ OPTIONAL: Enum validation helper
// common/utils/enum-utils.ts
export function isValidEnumValue<T>(
  enumObj: T,
  value: string,
): value is T[keyof T] {
  return Object.values(enumObj).includes(value as any);
}

// Usage
if (isValidEnumValue(TaskStatus, 'OPEN')) {
  // TypeScript knows value is valid
}
```

## Installation

```bash
# No packages needed - enums are built-in TypeScript feature
# Just ensure tsconfig.json has:
{
  "compilerOptions": {
    "strict": true
  }
}
```

**Incorrect:**

```typescript
// tasks/tasks.service.ts - String literals 🚨
import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksService {
  // ❌ String parameter - any value accepted
  async updateStatus(id: string, status: string) {
    const task = await this.repo.findOne(id);
    task.status = status; // ❌ No type safety
    return this.repo.save(task);
  }

  // ❌ Typo-prone comparisons
  async getOpenTasks() {
    // If you type 'opne' instead of 'open', no error!
    return this.repo.find({ where: { status: 'opne' } });
  }

  // ❌ Magic strings throughout code
  async completeTask(id: string) {
    const task = await this.repo.findOne(id);
    task.status = 'done'; // ❌ What if other code uses 'DONE'?
    return this.repo.save(task);
  }

  // ❌ Inconsistent values
  async createTask(title: string) {
    // Is it 'open', 'Open', or 'OPEN'?
    const task = this.repo.create({ title, status: 'OPEN' });
    return this.repo.save(task);
  }
}

// tasks/dto/create-task.dto.ts 🚨
export class CreateTaskDto {
  title: string;

  // ❌ No validation of allowed values
  status?: string;
}

// tasks/task.entity.ts 🚨
import { Entity, Column } from 'typeorm';

@Entity()
export class Task {
  @Column({
    type: 'varchar', // ❌ No enum type constraint
  })
  status: string; // ❌ Any string can be stored
}
```

**Correct:**

```typescript
// tasks/task-status.enum.ts - Type-safe enum ✅
export enum TaskStatus {
  OPEN = 'OPEN',
  IN_PROGRESS = 'IN_PROGRESS',
  DONE = 'DONE',
}

// tasks/task.entity.ts - Enum in entity ✅
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';
import { TaskStatus } from './task-status.enum';

@Entity()
export class Task {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  title: string;

  @Column({
    type: 'enum',
    enum: TaskStatus,
    default: TaskStatus.OPEN,
  })
  status: TaskStatus; // ✅ Type-safe
}

// tasks/dto/create-task.dto.ts - Enum validation ✅
import { IsEnum, IsOptional, IsString, MinLength } from 'class-validator';
import { TaskStatus } from '../task-status.enum';

export class CreateTaskDto {
  @IsString()
  @MinLength(3)
  title: string;

  @IsOptional()
  @IsEnum(TaskStatus, {
    message: `Status must be one of: ${Object.values(TaskStatus).join(', ')}`,
  })
  status?: TaskStatus; // ✅ Enum type with validation
}

// tasks/dto/update-task-status.dto.ts ✅
import { IsEnum } from 'class-validator';
import { TaskStatus } from '../task-status.enum';

export class UpdateTaskStatusDto {
  @IsEnum(TaskStatus, {
    message: `Status must be one of: ${Object.values(TaskStatus).join(', ')}`,
  })
  status: TaskStatus;
}

// tasks/tasks.service.ts - Enum in business logic ✅
import { Injectable } from '@nestjs/common';
import { TaskStatus } from './task-status.enum';

@Injectable()
export class TasksService {
  constructor(private tasksRepository: TasksRepository) {}

  // ✅ Type-safe parameter
  async updateStatus(id: string, status: TaskStatus) {
    const task = await this.tasksRepository.findOne(id);
    task.status = status;
    return this.tasksRepository.save(task);
  }

  // ✅ Compile-time checking, autocomplete
  async getTasksByStatus(status: TaskStatus) {
    return this.tasksRepository.find({ where: { status } });
  }

  // ✅ No typos possible
  async getOpenTasks() {
    return this.tasksRepository.find({
      where: { status: TaskStatus.OPEN },
    });
  }

  // ✅ Consistent values
  async completeTask(id: string) {
    const task = await this.tasksRepository.findOne(id);
    task.status = TaskStatus.DONE;
    return this.tasksRepository.save(task);
  }

  // ✅ Type-safe status transitions
  async startTask(id: string) {
    const task = await this.tasksRepository.findOne(id);

    // ✅ Enum comparison
    if (task.status === TaskStatus.DONE) {
      throw new BadRequestException('Cannot start a completed task');
    }

    task.status = TaskStatus.IN_PROGRESS;
    return this.tasksRepository.save(task);
  }

  // ✅ Enum iteration
  getStatusSummary() {
    return {
      [TaskStatus.OPEN]: 0,
      [TaskStatus.IN_PROGRESS]: 0,
      [TaskStatus.DONE]: 0,
    };
  }
}

// tasks/tasks.controller.ts ✅
import { Controller, Get, Patch, Param, Body } from '@nestjs/common';
import { TaskStatus } from './task-status.enum';

@Controller('tasks')
export class TasksController {
  @Get('by-status/:status')
  getTasksByStatus(@Param('status') status: TaskStatus) {
    // ✅ Type-safe route parameter
    return this.tasksService.getTasksByStatus(status);
  }

  @Patch(':id/status')
  updateStatus(
    @Param('id') id: string,
    @Body() dto: UpdateTaskStatusDto,
  ) {
    // ✅ dto.status is typed as TaskStatus
    return this.tasksService.updateStatus(id, dto.status);
  }
}
```

## Advanced: Enum Utilities

```typescript
// ✅ Helper functions for enum operations
// common/utils/enum.utils.ts

/**
 * Get all enum values as array
 */
export function getEnumValues<T extends Record<string, string>>(enumObj: T): string[] {
  return Object.values(enumObj);
}

/**
 * Check if value is valid enum member
 */
export function isValidEnumValue<T extends Record<string, string>>(
  enumObj: T,
  value: string,
): value is T[keyof T] {
  return Object.values(enumObj).includes(value as any);
}

/**
 * Get enum key from value
 */
export function getEnumKey<T extends Record<string, string>>(
  enumObj: T,
  value: T[keyof T],
): keyof T | undefined {
  return Object.keys(enumObj).find((key) => enumObj[key] === value);
}

/**
 * Get random enum value
 */
export function getRandomEnumValue<T extends Record<string, string>>(
  enumObj: T,
): T[keyof T] {
  const values = Object.values(enumObj);
  return values[Math.floor(Math.random() * values.length)] as T[keyof T];
}

// Usage examples
import { TaskStatus } from './task-status.enum';

getEnumValues(TaskStatus); // ['OPEN', 'IN_PROGRESS', 'DONE']
isValidEnumValue(TaskStatus, 'OPEN'); // true
isValidEnumValue(TaskStatus, 'INVALID'); // false
getEnumKey(TaskStatus, 'OPEN'); // 'OPEN'
getRandomEnumValue(TaskStatus); // Random status
```

## Advanced: Const Enums

```typescript
// ✅ Const enums for better performance (no runtime code)
// users/user-role.const-enum.ts
export const enum UserRole {
  ADMIN = 'ADMIN',
  USER = 'USER',
  GUEST = 'GUEST',
}

// Const enums are inlined at compile time
// Result: if (user.role === 'ADMIN') instead of if (user.role === UserRole.ADMIN)
```

## Advanced: String Union Types

```typescript
// ✅ Alternative: String union types (for simple cases)
// tasks/task-status.type.ts
export type TaskStatus = 'OPEN' | 'IN_PROGRESS' | 'DONE';

// Still type-safe, but no enum object at runtime
const status: TaskStatus = 'OPEN'; // ✅ Valid
const invalid: TaskStatus = 'INVALID'; // ❌ Compile error

// You can still get all values (requires manual array)
export const TASK_STATUSES: TaskStatus[] = ['OPEN', 'IN_PROGRESS', 'DONE'];
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use enums for constant values | Type-safe, autocomplete support |
| Define enums in separate files | Reusable across the application |
| Use enum type in entities | Database-level constraint |
| Add @IsEnum() in DTOs | Validation for API inputs |
| Use consistent casing | Avoids confusion (OPEN vs open vs Open) |
| Create enum utilities | Helper functions for common operations |

**Sources:**
- [TypeScript Enums Documentation](https://www.typescriptlang.org/docs/handbook/enums.html)
- [NestJS Validation with Enums](https://docs.nestjs.com/techniques/validation)
- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application
