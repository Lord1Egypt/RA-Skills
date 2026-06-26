---
title: Use Filter DTOs for Query Parameter Validation
impact: HIGH
impactDescription: Validates and type-checks query parameters
section: 5
tags: validation, query, dto, filter, search, pagination
---

Extracting query parameters individually (`@Query('status') status: string`) results in no validation, no type safety, and verbose code. Filter DTOs validate all query parameters consistently and provide automatic type transformation.

## For AI Agents

When implementing or reviewing query parameter handling, **always** follow these steps:

### Step 1: Check for Individual Query Parameters
**Pattern to check:** Look for `@Query()` decorators with parameter names, manual string parsing, or optional chaining.

```typescript
// ❌ WRONG - Individual parameters with no validation
@Get()
findAll(
  @Query('status') status: string,        // ❌ No validation
  @Query('search') search: string,        // ❌ No validation
  @Query('page') page: string,            // ❌ String instead of number
  @Query('limit') limit: string,          // ❌ String instead of number
) {
  // ❌ Manual type conversion
  const pageNum = parseInt(page) || 1;
  const limitNum = parseInt(limit) || 10;
  // ...
}

// ❌ WRONG - Manual parsing with no validation
@Get()
findAll(@Query() query: any) {
  const status = query.status as string;     // ❌ Type assertion
  const page = parseInt(query.page) || 1;    // ❌ Manual parse
  const limit = parseInt(query.limit) || 10; // ❌ Manual parse
  // ...
}
```

**If found:** Replace with filter DTO.

### Step 2: Create Filter DTO
**File:** `tasks/dto/get-tasks-filter.dto.ts`

```typescript
// ✅ REQUIRED: Filter DTO with validation
import { IsOptional, IsEnum, IsString, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';
import { TaskStatus } from '../task-status.enum';

export class GetTasksFilterDto {
  // ✅ Optional enum validation
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  // ✅ Optional string with validation
  @IsOptional()
  @IsString()
  search?: string;

  // ✅ Auto-transform string to number
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  // ✅ Auto-transform string to number
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}
```

### Step 3: Use Filter DTO in Controller

```typescript
// ✅ REQUIRED: Use DTO in controller
// tasks/tasks.controller.ts
import { Get, Query, Controller } from '@nestjs/common';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto) {
    // ✅ filterDto is validated and typed
    // filterDto.status is TaskStatus | undefined
    // filterDto.page is number (not string!)
    // filterDto.limit is number (not string!)
    return this.tasksService.getTasks(filterDto);
  }
}
```

### Step 4: Create Reusable Pagination DTO

```typescript
// ✅ OPTIONAL: Base pagination DTO
// common/dto/pagination.dto.ts
import { IsOptional, IsInt, Min } from 'class-validator';
import { Type } from 'class-transformer';

export class PaginationDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// ✅ Extend pagination DTO
// tasks/dto/get-tasks-filter.dto.ts
import { PaginationDto } from '../../common/dto/pagination.dto';

export class GetTasksFilterDto extends PaginationDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  @IsOptional()
  @IsString()
  search?: string;
}
```

### Step 5: Create Sort/Order DTO

```typescript
// ✅ OPTIONAL: Sortable fields
// common/dto/sort.dto.ts
import { IsOptional, IsEnum, IsIn } from 'class-validator';

export class SortDto {
  @IsOptional()
  @IsEnum(['ASC', 'DESC'])
  order?: 'ASC' | 'DESC' = 'ASC';

  @IsOptional()
  @IsString()
  sortBy?: string;
}

// ✅ Strongly typed sort
// tasks/dto/get-tasks-filter.dto.ts
import { TaskSortableFields } from '../task-sortable-fields.enum';

export class GetTasksFilterDto extends PaginationDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  @IsOptional()
  @IsEnum(['ASC', 'DESC'])
  order?: 'ASC' | 'DESC' = 'ASC';

  @IsOptional()
  @IsEnum(TaskSortableFields)
  sortBy?: TaskSortableFields = TaskSortableFields.CREATED_AT;
}

// tasks/task-sortable-fields.enum.ts
export enum TaskSortableFields {
  TITLE = 'title',
  STATUS = 'status',
  CREATED_AT = 'createdAt',
  UPDATED_AT = 'updatedAt',
}
```

### Step 6: Use in Repository Queries

```typescript
// ✅ REQUIRED: Type-safe queries in repository
// tasks/tasks.repository.ts
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';

export class TasksRepository extends Repository<Task> {
  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    const { status, search, page = 1, limit = 10 } = filterDto;
    const query = this.createQueryBuilder('task');

    query.where({ user });

    if (status) {
      // ✅ Type-safe: status is TaskStatus, not any string
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    // ✅ Type-safe: page and limit are numbers
    query.skip((page - 1) * limit).take(limit);

    return await query.getMany();
  }
}
```

### Step 7: Add Date Range Filters

```typescript
// ✅ OPTIONAL: Date range DTO
// common/dto/date-range.dto.ts
import { IsOptional, IsDate } from 'class-validator';
import { Type } from 'class-transformer';

export class DateRangeDto {
  @IsOptional()
  @Type(() => Date)
  @IsDate()
  startDate?: Date;

  @IsOptional()
  @Type(() => Date)
  @IsDate()
  endDate?: Date;
}

// ✅ Use date range in filter
// tasks/dto/get-tasks-filter.dto.ts
import { DateRangeDto } from '../../common/dto/date-range.dto';

export class GetTasksFilterDto extends PaginationDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @Type(() => Date)
  @IsDate()
  createdAfter?: Date;

  @IsOptional()
  @Type(() => Date)
  @IsDate()
  createdBefore?: Date;
}
```

## Installation

```bash
# Install required packages
bun add class-validator class-transformer
# or
npm install class-validator class-transformer
```

**Incorrect:**

```typescript
// tasks/tasks.controller.ts - Individual parameters 🚨
import { Controller, Get, Query } from '@nestjs/common';

@Controller('tasks')
export class TasksController {
  @Get()
  findAll(
    @Query('status') status: string,        // ❌ No validation
    @Query('search') search: string,        // ❌ No validation
    @Query('page') page: string,            // ❌ String, not number
    @Query('limit') limit: string,          // ❌ String, not number
  ) {
    // ❌ Manual type conversion
    const pageNum = parseInt(page) || 1;
    const limitNum = parseInt(limit) || 10;

    // ❌ No type safety - status could be "INVALID"
    return this.tasksService.getTasks(status, search, pageNum, limitNum);
  }

  @Get()
  findAll(@Query() query: any) {
    // ❌ No type safety at all
    const status = query.status as string;
    const page = parseInt(query.page) || 1;
    const limit = parseInt(query.limit) || 10;
    const search = query.search;

    return this.tasksService.getTasks(status, search, page, limit);
  }
}

// tasks/tasks.service.ts 🚨
@Injectable()
export class TasksService {
  // ❌ Too many parameters, no type safety
  async getTasks(
    status: string | undefined,
    search: string | undefined,
    page: number,
    limit: number,
  ) {
    // ❌ What values are valid for status? No hints.
    const query = this.repo.createQueryBuilder('task');

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    query.skip((page - 1) * limit).take(limit);

    return query.getMany();
  }
}
```

**Correct:**

```typescript
// tasks/dto/get-tasks-filter.dto.ts - Filter DTO ✅
import { IsOptional, IsEnum, IsString, IsInt, Min, Max } from 'class-validator';
import { Type } from 'class-transformer';
import { TaskStatus } from '../task-status.enum';

export class GetTasksFilterDto {
  @IsOptional()
  @IsEnum(TaskStatus, {
    message: `Status must be one of: ${Object.values(TaskStatus).join(', ')}`,
  })
  status?: TaskStatus;

  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// common/dto/pagination.dto.ts - Reusable pagination ✅
import { IsOptional, IsInt, Min, Max } from 'class-validator';
import { Type } from 'class-transformer';

export class PaginationDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// tasks/tasks.controller.ts - Clean controller ✅
import { Controller, Get, Query } from '@nestjs/common';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';

@Controller('tasks')
export class TasksController {
  constructor(private tasksService: TasksService) {}

  @Get()
  findAll(@Query() filterDto: GetTasksFilterDto) {
    // ✅ Single parameter, fully typed and validated
    return this.tasksService.getTasks(filterDto);
  }
}

// tasks/tasks.service.ts - Clean service ✅
import { Injectable } from '@nestjs/common';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';

@Injectable()
export class TasksService {
  constructor(private tasksRepository: TasksRepository) {}

  // ✅ Single DTO parameter
  async getTasks(filterDto: GetTasksFilterDto): Promise<Task[]> {
    // ✅ Delegate to repository
    return this.tasksRepository.getTasks(filterDto);
  }
}

// tasks/tasks.repository.ts - Type-safe queries ✅
import { EntityRepository, Repository } from 'typeorm';
import { Task } from './task.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';

@EntityRepository(Task)
export class TasksRepository extends Repository<Task> {
  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    const { status, search, page = 1, limit = 10 } = filterDto;
    const query = this.createQueryBuilder('task');

    query.where({ user });

    // ✅ Type-safe: status is TaskStatus | undefined
    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    // ✅ Type-safe: search is string | undefined
    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    // ✅ Type-safe: page and limit are numbers
    query.skip((page - 1) * limit).take(limit);

    return await query.getMany();
  }
}
```

## Advanced: Paginated Response

```typescript
// ✅ Return paginated results with metadata
// common/dto/paginated-response.dto.ts
export class PaginatedResponseDto<T> {
  data: T[];
  meta: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// tasks/tasks.repository.ts ✅
export class TasksRepository extends Repository<Task> {
  async getTasksWithPagination(
    filterDto: GetTasksFilterDto,
    user: User,
  ): Promise<PaginatedResponseDto<Task>> {
    const { status, search, page = 1, limit = 10 } = filterDto;
    const query = this.createQueryBuilder('task');

    query.where({ user });

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    const [data, total] = await query
      .skip((page - 1) * limit)
      .take(limit)
      .getManyAndCount();

    return {
      data,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }
}
```

## Advanced: Composable Filter DTOs

```typescript
// ✅ Composable DTOs with intersections
// common/dto/base-filter.dto.ts
export class BaseFilterDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  limit?: number = 10;
}

// tasks/dto/get-tasks-filter.dto.ts ✅
import { BaseFilterDto } from '../../common/dto/base-filter.dto';

export class GetTasksFilterDto extends BaseFilterDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @Type(() => Date)
  @IsDate()
  from?: Date;

  @IsOptional()
  @Type(() => Date)
  @IsDate()
  to?: Date;
}
```

## Advanced: Validation Groups

```typescript
// ✅ Different validation for different scenarios
// tasks/dto/get-tasks-filter.dto.ts
import { ValidateIf } from 'class-validator';

export class GetTasksFilterDto {
  @IsOptional()
  @IsEnum(TaskStatus)
  status?: TaskStatus;

  // ✅ Only validate if search is present
  @IsOptional()
  @IsString()
  @MinLength(3, { message: 'Search must be at least 3 characters' })
  search?: string;

  // ✅ Validate 'from' only if 'to' is also present
  @IsOptional()
  @ValidateIf((o) => o.to !== undefined)
  @IsDate()
  from?: Date;

  @IsOptional()
  @ValidateIf((o) => o.from !== undefined)
  @IsDate()
  to?: Date;
}
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use filter DTOs | Single validated parameter |
| Add @Type() decorator | Auto-transform strings to numbers/dates |
| Use @IsOptional() | Parameters are optional by default |
| Add default values | Cleaner code with default pagination |
| Create reusable base DTOs | DRY principle for common filters |
| Extend base DTOs | Composable filter combinations |

**Sources:**
- [NestJS Query Parameters Documentation](https://docs.nestjs.com/controllers#query-parameters)
- [class-validator Documentation](https://github.com/typestack/class-validator)
- [class-transformer Documentation](https://github.com/typestack/class-transformer)
- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application
