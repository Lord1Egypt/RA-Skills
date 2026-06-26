---
title: Use Custom Repository Pattern for Database Logic Encapsulation
impact: HIGH
impactDescription: Separates concerns and improves testability
section: 6
tags: database, repository, typeorm, encapsulation, clean-architecture
---

Placing database query logic directly in services leads to bloated service classes, mixing business logic with data access, and difficult testing. Custom repositories extend the base TypeORM repository and encapsulate all database logic, keeping services clean and focused on business rules.

## For AI Agents

When implementing or reviewing database operations, **always** follow these steps:

### Step 1: Check for Database Logic in Services
**Pattern to check:** Look for `@InjectRepository()`, query builders, or database methods (find, save, update, delete) in service files.

```typescript
// ❌ WRONG - Database logic in service
@Injectable()
export class TasksService {
  constructor(
    @InjectRepository(Task) private repo: Repository<Task>
  ) {}

  async getTasks(user: User, filterDto: GetTasksFilterDto) {
    // ❌ Database query logic in service
    const { status, search } = filterDto;
    const query = this.repo.createQueryBuilder('task');
    query.where({ user });

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    return await query.getMany();
  }

  async findOne(id: string, user: User) {
    // ❌ Repeated query logic
    return this.repo.findOne({ where: { id, user } });
  }
}
```

**If found:** Extract to custom repository.

### Step 2: Create Custom Repository
**File:** `tasks/tasks.repository.ts`

```typescript
// ✅ REQUIRED: Custom repository extending TypeORM Repository
import { EntityRepository, Repository } from 'typeorm';
import { Task } from './task.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';

// For TypeORM < 0.3
@EntityRepository(Task)
export class TasksRepository extends Repository<Task> {
  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    const { status, search } = filterDto;
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

    return await query.getMany();
  }

  async findOneById(id: string, user: User): Promise<Task> {
    return this.findOne({ where: { id, user } });
  }
}

// For TypeORM >= 0.3 (using dataSource)
import { DataSource, Repository } from 'typeorm';
import { Task } from './task.entity';
import { Injectable } from '@nestjs/common';

@Injectable()
export class TasksRepository {
  constructor(private dataSource: DataSource) {
    // Get repository from dataSource
  }

  private get repo(): Repository<Task> {
    return this.dataSource.getRepository(Task);
  }

  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    const { status, search } = filterDto;
    const query = this.repo.createQueryBuilder('task');

    query.where({ user });

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    return await query.getMany();
  }

  async findOneById(id: string, user: User): Promise<Task> {
    return this.repo.findOne({ where: { id, user } });
  }
}
```

### Step 3: Register Repository in Module
**File:** `tasks/tasks.module.ts`

```typescript
// ✅ REQUIRED: Register custom repository
import { TypeOrmModule } from '@nestjs/typeorm';
import { TasksController } from './tasks.controller';
import { TasksService } from './tasks.service';
import { TasksRepository } from './tasks.repository';
import { Task } from './task.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Task])],
  controllers: [TasksController],
  providers: [TasksService, TasksRepository],
  exports: [TasksService, TasksRepository],
})
export class TasksModule {}
```

### Step 4: Inject Repository in Service
**File:** `tasks/tasks.service.ts`

```typescript
// ✅ REQUIRED: Clean service with repository
@Injectable()
export class TasksService {
  constructor(
    private tasksRepository: TasksRepository
  ) {}

  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    // ✅ Delegates to repository
    return this.tasksRepository.getTasks(filterDto, user);
  }

  async findOne(id: string, user: User): Promise<Task> {
    // ✅ Simple delegation
    return this.tasksRepository.findOneById(id, user);
  }

  async create(dto: CreateTaskDto, user: User): Promise<Task> {
    // Service handles business rules
    const task = this.tasksRepository.create({
      ...dto,
      user,
      status: TaskStatus.OPEN,
    });
    return this.tasksRepository.save(task);
  }
}
```

### Step 5: Add Complex Query Methods

```typescript
// ✅ OPTIONAL: Complex queries in repository
// tasks/tasks.repository.ts
@EntityRepository(Task)
export class TasksRepository extends Repository<Task> {
  async getTasksWithStats(user: User): Promise<{ tasks: Task[]; stats: any }> {
    const query = this.createQueryBuilder('task');

    query.where({ user });

    // ✅ Complex joins and aggregations
    query.leftJoinAndSelect('task.comments', 'comment');
    query.loadRelationCountAndMap('task.commentCount', 'task.comments');

    const tasks = await query.getMany();

    // ✅ Statistics calculation
    const stats = {
      total: tasks.length,
      byStatus: this.groupByStatus(tasks),
    };

    return { tasks, stats };
  }

  async findOverdueTasks(user: User): Promise<Task[]> {
    return this.createQueryBuilder('task')
      .where('task.user = :user', { user })
      .andWhere('task.dueDate < :now', { now: new Date() })
      .andWhere('task.status != :status', { status: TaskStatus.DONE })
      .orderBy('task.dueDate', 'ASC')
      .getMany();
  }

  private groupByStatus(tasks: Task[]): Record<string, number> {
    return tasks.reduce((acc, task) => {
      acc[task.status] = (acc[task.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
  }
}
```

### Step 6: Add Transaction Support

```typescript
// ✅ OPTIONAL: Transaction methods
// tasks/tasks.repository.ts
import { DataSource, QueryRunner } from 'typeorm';

export class TasksRepository extends Repository<Task> {
  constructor(private dataSource: DataSource) {
    super();
  }

  async createWithComments(
    taskData: CreateTaskDto,
    comments: CreateCommentDto[],
    user: User,
  ): Promise<Task> {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      // Create task
      const task = queryRunner.manager.create(Task, {
        ...taskData,
        user,
      });
      const savedTask = await queryRunner.manager.save(task);

      // Create comments
      for (const commentData of comments) {
        const comment = queryRunner.manager.create(Comment, {
          ...commentData,
          task: savedTask,
        });
        await queryRunner.manager.save(comment);
      }

      await queryRunner.commitTransaction();
      return savedTask;
    } catch (error) {
      await queryRunner.rollbackTransaction();
      throw error;
    } finally {
      await queryRunner.release();
    }
  }
}
```

### Step 7: Testing the Repository

```typescript
// ✅ REQUIRED: Test repository independently
// tasks/tasks.repository.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { TasksRepository } from './tasks.repository';
import { Task } from './task.entity';
import { User } from '../auth/entities/user.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';

describe('TasksRepository', () => {
  let repository: TasksRepository;

  const mockTask = {
    id: '123',
    title: 'Test Task',
    description: 'Test Description',
    status: TaskStatus.OPEN,
    user: { id: 'user-123' } as User,
  };

  const mockRepository = {
    createQueryBuilder: jest.fn(),
    findOne: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        TasksRepository,
        {
          provide: getRepositoryToken(Task),
          useValue: mockRepository,
        },
      ],
    }).compile();

    repository = module.get<TasksRepository>(TasksRepository);
  });

  describe('getTasks', () => {
    it('should return filtered tasks', async () => {
      const mockQuery = {
        where: jest.fn().mockReturnThis(),
        andWhere: jest.fn().mockReturnThis(),
        getMany: jest.fn().mockResolvedValue([mockTask]),
      };

      mockRepository.createQueryBuilder.mockReturnValue(mockQuery);

      const filterDto: GetTasksFilterDto = {
        status: TaskStatus.OPEN,
        search: 'test',
      };

      const result = await repository.getTasks(filterDto, mockTask.user);

      expect(result).toEqual([mockTask]);
      expect(mockQuery.where).toHaveBeenCalled();
      expect(mockQuery.andWhere).toHaveBeenCalledTimes(2);
    });
  });
});
```

## Installation

```bash
# For TypeORM (required)
bun add @nestjs/typeorm typeorm
# or
npm install @nestjs/typeorm typeorm

# Database driver (choose one)
bun add pg          # PostgreSQL
bun add mysql2      # MySQL
bun add sqlite3     # SQLite
```

**Incorrect:**

```typescript
// tasks/tasks.service.ts - Database logic in service 🚨
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Task } from './task.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';

@Injectable()
export class TasksService {
  constructor(
    @InjectRepository(Task) // ❌ Direct repository injection
    private repo: Repository<Task>
  ) {}

  async getTasks(filterDto: GetTasksFilterDto, user: User) {
    const { status, search } = filterDto;

    // ❌ Database query logic in service
    const query = this.repo.createQueryBuilder('task');
    query.where({ user });

    if (status) {
      query.andWhere('task.status = :status', { status });
    }

    if (search) {
      query.andWhere('(task.title LIKE :search OR task.description LIKE :search)', {
        search: `%${search}%`,
      });
    }

    return await query.getMany();
  }

  async findOne(id: string, user: User) {
    // ❌ Repeated query logic
    return this.repo.findOne({ where: { id, user } });
  }

  async create(dto: CreateTaskDto, user: User) {
    // ❌ Mixed business and data logic
    const task = this.repo.create({ ...dto, user });
    return this.repo.save(task);
  }

  async findOverdue(user: User) {
    // ❌ Complex query in service - hard to test
    return this.repo
      .createQueryBuilder('task')
      .where('task.user = :user', { user })
      .andWhere('task.dueDate < :now', { now: new Date() })
      .andWhere('task.status != :status', { status: TaskStatus.DONE })
      .getMany();
  }
}
```

**Correct:**

```typescript
// tasks/tasks.repository.ts - Encapsulated database logic ✅
import { EntityRepository, Repository } from 'typeorm';
import { Task } from './task.entity';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';
import { TaskStatus } from './task-status.enum';

@EntityRepository(Task)
export class TasksRepository extends Repository<Task> {
  /**
   * Get tasks with optional filtering
   */
  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    const { status, search } = filterDto;
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

    return await query.getMany();
  }

  /**
   * Find a single task by ID for a specific user
   */
  async findOneById(id: string, user: User): Promise<Task> {
    return this.findOne({ where: { id, user } });
  }

  /**
   * Find overdue tasks for a user
   */
  async findOverdue(user: User): Promise<Task[]> {
    return this.createQueryBuilder('task')
      .where('task.user = :user', { user })
      .andWhere('task.dueDate < :now', { now: new Date() })
      .andWhere('task.status != :status', { status: TaskStatus.DONE })
      .orderBy('task.dueDate', 'ASC')
      .getMany();
  }

  /**
   * Get tasks with statistics
   */
  async getTasksWithStats(user: User) {
    const tasks = await this.find({ where: { user } });

    const stats = {
      total: tasks.length,
      open: tasks.filter((t) => t.status === TaskStatus.OPEN).length,
      inProgress: tasks.filter((t) => t.status === TaskStatus.IN_PROGRESS).length,
      done: tasks.filter((t) => t.status === TaskStatus.DONE).length,
    };

    return { tasks, stats };
  }
}

// tasks/tasks.service.ts - Clean business logic ✅
import { Injectable, NotFoundException } from '@nestjs/common';
import { TasksRepository } from './tasks.repository';
import { CreateTaskDto } from './dto/create-task.dto';
import { UpdateTaskDto } from './dto/update-task.dto';
import { GetTasksFilterDto } from './dto/get-tasks-filter.dto';
import { User } from '../auth/entities/user.entity';
import { Task } from './task.entity';

@Injectable()
export class TasksService {
  constructor(
    private tasksRepository: TasksRepository,
  ) {}

  /**
   * Get all tasks for a user with optional filtering
   */
  async getTasks(filterDto: GetTasksFilterDto, user: User): Promise<Task[]> {
    return this.tasksRepository.getTasks(filterDto, user);
  }

  /**
   * Get a single task by ID
   */
  async findOne(id: string, user: User): Promise<Task> {
    const task = await this.tasksRepository.findOneById(id, user);

    if (!task) {
      throw new NotFoundException(`Task with ID "${id}" not found`);
    }

    return task;
  }

  /**
   * Create a new task
   */
  async create(dto: CreateTaskDto, user: User): Promise<Task> {
    const task = this.tasksRepository.create({
      ...dto,
      user,
      status: TaskStatus.OPEN,
    });

    return this.tasksRepository.save(task);
  }

  /**
   * Update an existing task
   */
  async update(id: string, dto: UpdateTaskDto, user: User): Promise<Task> {
    const task = await this.findOne(id, user);

    // Business logic: only allow updating own tasks
    Object.assign(task, dto);

    return this.tasksRepository.save(task);
  }

  /**
   * Delete a task
   */
  async delete(id: string, user: User): Promise<void> {
    const result = await this.tasksRepository.delete({ id, user });

    if (result.affected === 0) {
      throw new NotFoundException(`Task with ID "${id}" not found`);
    }
  }

  /**
   * Get overdue tasks
   */
  async getOverdue(user: User): Promise<Task[]> {
    return this.tasksRepository.findOverdue(user);
  }
}

// tasks/tasks.module.ts - Proper registration ✅
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { TasksController } from './tasks.controller';
import { TasksService } from './tasks.service';
import { TasksRepository } from './tasks.repository';
import { Task } from './task.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Task])],
  controllers: [TasksController],
  providers: [TasksService, TasksRepository],
  exports: [TasksService, TasksRepository],
})
export class TasksModule {}
```

## TypeORM 0.3+ Migration

```typescript
// For TypeORM >= 0.3, @EntityRepository() decorator is deprecated
// Use dataSource-based approach:

// tasks/repositories/tasks.repository.ts ✅
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource, Repository } from 'typeorm';
import { Task } from '../entities/task.entity';

@Injectable()
export class TasksRepository {
  private get repo(): Repository<Task> {
    return this.dataSource.getRepository(Task);
  }

  constructor(@InjectDataSource() private dataSource: DataSource) {}

  async getTasks(user: User): Promise<Task[]> {
    return this.repo.find({ where: { user } });
  }

  async findOne(id: string, user: User): Promise<Task> {
    const task = await this.repo.findOne({ where: { id, user } });
    if (!task) {
      throw new NotFoundException();
    }
    return task;
  }
}

// Or use the new TypeOrmEx decorator approach:
// common/decorators/typeorm-ex.decorator.ts ✅
import { DataSource } from 'typeorm';
import { TYPEORM_EX_DATA_SOURCE } from './typeorm-ex.constants';

export const TypeormExRepository = <T>(entity: Type<any>) =>
  InjectDataSource(TYPEORM_EX_DATA_SOURCE);

// tasks/repositories/tasks.repository.ts
@Injectable()
export class TasksRepository {
  constructor(
    @TypeormExRepository(Task)
    private dataSource: DataSource,
  ) {
    // Use dataSource.getRepository(Task)
  }
}
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Create custom repositories | Separates data access from business logic |
| Extend TypeORM Repository | Reuse base CRUD methods |
| Put complex queries in repository | Single responsibility, easier testing |
| Keep services clean | Focus on business rules only |
| Inject repository into service | Proper dependency injection |
| Test repositories independently | Isolated data layer testing |

**Sources:**
- [TypeORM Custom Repositories](https://typeorm.io/#/custom-repository)
- [NestJS TypeORM Documentation](https://docs.nestjs.com/techniques/database)
- [arielweinberger/nestjs-recipe](https://github.com/arielweinberger/nestjs-recipe) - Production-ready NestJS application
