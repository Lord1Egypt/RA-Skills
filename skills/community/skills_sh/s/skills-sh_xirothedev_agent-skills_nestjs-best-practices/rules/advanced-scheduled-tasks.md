---
title: Use @nestjs/schedule for Cron Jobs and Scheduled Tasks
impact: MEDIUM
section: 13
impactDescription: Ensures reliable periodic task execution
tags: advanced, scheduled-tasks, cron, jobs, schedule
---

## Use @nestjs/schedule for Cron Jobs and Scheduled Tasks

Scheduled tasks like cleanup jobs, data synchronization, and periodic reports need reliable execution. The `@nestjs/schedule` module provides decorators for cron jobs, intervals, and timeouts with proper NestJS lifecycle management. **Never use raw `setInterval` or external cron schedulers.**

**Incorrect:**

```typescript
// cleanup.service.ts - Raw timers 🚨
import { Injectable, OnModuleDestroy } from '@nestjs/common';

@Injectable()
export class CleanupService implements OnModuleDestroy {
  private intervals: NodeJS.Timeout[] = [];

  constructor() {
    // ❌ Raw interval - no NestJS lifecycle
    const interval1 = setInterval(() => {
      this.cleanupExpiredSessions().catch(console.error);
    }, 60000);  // Every minute

    // ❌ Another raw interval
    const interval2 = setInterval(() => {
      this.deleteOldLogs().catch(console.error);
    }, 3600000);  // Every hour

    // ❌ Manual interval tracking
    this.intervals.push(interval1, interval2);
  }

  // ❌ Manual cleanup required
  onModuleDestroy() {
    this.intervals.forEach(clearInterval);
  }

  // ❌ No error handling in callbacks
  async cleanupExpiredSessions() {
    await this.prisma.session.deleteMany({
      where: { expiresAt: { lt: new Date() } },
    });
  }

  async deleteOldLogs() {
    await this.prisma.log.deleteMany({
      where: { createdAt: { lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) } },
    });
  }
}

// subscription.service.ts - Manual tracking 🚨
@Injectable()
export class SubscriptionService {
  private checkInterval: NodeJS.Timeout;

  constructor(private prisma: PrismaService) {
    // ❌ Manually start interval
    this.startCheckingExpiringSubscriptions();
  }

  private startCheckingExpiringSubscriptions() {
    this.checkInterval = setInterval(async () => {
      try {
        await this.checkExpiringSubscriptions();
      } catch (error) {
        console.error('Subscription check failed:', error);
        // ❌ No structured logging
      }
    }, 24 * 60 * 60 * 1000);  // Daily
  }

  private async checkExpiringSubscriptions() {
    // Business logic
  }
}
```

**Correct:**

```typescript
// app.module.ts - Configure scheduler ✅
import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';
import { ScheduledTasksModule } from './tasks/scheduled-tasks.module';

@Module({
  imports: [
    ScheduleModule.forRoot(),  // ✅ Initialize with defaults
    ScheduledTasksModule,
  ],
})
export class AppModule {}

// tasks/scheduled-tasks.service.ts - Proper scheduling ✅
import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression, Interval, Timeout } from '@nestjs/schedule';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ScheduledTasksService {
  private readonly logger = new Logger(ScheduledTasksService.name);
  private isProcessingData = false;

  constructor(private prisma: PrismaService) {}

  // ✅ Every day at midnight
  @Cron(CronExpression.EVERY_DAY_AT_MIDNIGHT)
  async cleanupExpiredSessions() {
    try {
      this.logger.log('Starting session cleanup...');
      const deleted = await this.prisma.session.deleteMany({
        where: { expiresAt: { lt: new Date() } },
      });
      this.logger.log(`Deleted ${deleted.count} expired sessions`);
    } catch (error) {
      this.logger.error('Session cleanup failed', error.stack);
    }
  }

  // ✅ Every day at 2 AM
  @Cron('0 2 * * *')
  async deleteOldLogs() {
    try {
      this.logger.log('Starting log cleanup...');
      const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
      const deleted = await this.prisma.log.deleteMany({
        where: { createdAt: { lt: thirtyDaysAgo } },
      });
      this.logger.log(`Deleted ${deleted.count} old logs`);
    } catch (error) {
      this.logger.error('Log cleanup failed', error.stack);
    }
  }

  // ✅ Every hour
  @Cron(CronExpression.EVERY_HOUR)
  async checkExpiringSubscriptions() {
    try {
      this.logger.log('Checking for expiring subscriptions...');
      const expiringSoon = await this.prisma.subscription.findMany({
        where: {
          endDate: {
            gte: new Date(),
            lte: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
          },
          notificationSent: false,
        },
      });

      for (const subscription of expiringSoon) {
        await this.sendExpirationNotice(subscription);
        await this.prisma.subscription.update({
          where: { id: subscription.id },
          data: { notificationSent: true },
        });
      }

      this.logger.log(`Processed ${expiringSoon.length} expiring subscriptions`);
    } catch (error) {
      this.logger.error('Subscription check failed', error.stack);
    }
  }

  // ✅ Every 30 seconds - with overlap prevention
  @Interval(30000)
  async processQueue() {
    if (this.isProcessingData) {
      this.logger.debug('Queue processing already in progress, skipping');
      return;
    }

    this.isProcessingData = true;
    try {
      this.logger.debug('Processing job queue...');
      const jobs = await this.prisma.job.findMany({
        where: { status: 'PENDING' },
        take: 10,
      });

      for (const job of jobs) {
        await this.processJob(job);
      }

      this.logger.debug(`Processed ${jobs.length} jobs`);
    } catch (error) {
      this.logger.error('Queue processing failed', error.stack);
    } finally {
      this.isProcessingData = false;
    }
  }

  // ✅ One-time execution after 10 seconds
  @Timeout(10000)
  async initializeData() {
    try {
      this.logger.log('Running startup initialization...');
      await this.seedInitialData();
      this.logger.log('Startup initialization completed');
    } catch (error) {
      this.logger.error('Startup initialization failed', error.stack);
    }
  }

  // ✅ Custom cron expression - every Monday at 9 AM
  @Cron('0 9 * * 1')
  async sendWeeklyReport() {
    try {
      this.logger.log('Generating weekly report...');
      const report = await this.generateWeeklyReport();
      await this.emailService.sendReport(report);
      this.logger.log('Weekly report sent successfully');
    } catch (error) {
      this.logger.error('Weekly report failed', error.stack);
    }
  }

  private async sendExpirationNotice(subscription: Subscription) {
    // Send notification
  }

  private async processJob(job: Job) {
    // Process job
  }

  private async seedInitialData() {
    // Initialize data
  }

  private async generateWeeklyReport() {
    // Generate report
  }
}

// tasks/scheduled-tasks.module.ts ✅
import { Module } from '@nestjs/common';
import { ScheduledTasksService } from './scheduled-tasks.service';

@Module({
  providers: [ScheduledTasksService],
  exports: [ScheduledTasksService],
})
export class ScheduledTasksModule {}
```

## Cron Expression Patterns

### Using CronExpression Enum

```typescript
import { CronExpression } from '@nestjs/schedule';

// Common patterns from enum
@Cron(CronExpression.EVERY_MINUTE)        // * * * * *
@Cron(CronExpression.EVERY_HOUR)          // 0 * * * *
@Cron(CronExpression.EVERY_DAY_AT_MIDNIGHT)  // 0 0 * * *
@Cron(CronExpression.EVERY_DAY_AT_10AM)   // 0 10 * * *
@Cron(CronExpression.EVERY_WEEK)          // 0 0 * * 0
@Cron(CronExpression.EVERY_MONTH)         // 0 0 1 * *
@Cron(CronExpression.EVERY_YEAR)          // 0 0 1 1 *
@Cron(CronExpression.EVERY_5_MINUTES)     // */5 * * * *
@Cron(CronExpression.EVERY_30_MINUTES)    // */30 * * * *
```

### Custom Cron Expressions

```typescript
// Format: second minute hour day month weekday

// Every day at 6:30 AM
@Cron('0 30 6 * * *')

// Every Monday at 9 AM
@Cron('0 0 9 * * 1')

// Every 5 minutes
@Cron('0 */5 * * * *')

// Every weekday at 5 PM
@Cron('0 0 17 * * 1-5')

// Every 6 hours
@Cron('0 0 */6 * * *')

// First day of every month at midnight
@Cron('0 0 0 1 * *')

// Every Tuesday and Thursday at 2:30 PM
@Cron('0 30 14 * * 2,4')

// Every 10 seconds
@Cron('*/10 * * * * *')

// Range: Every hour between 9 AM and 5 PM
@Cron('0 0 9-17 * * *')
```

## Dynamic Scheduler Configuration

```typescript
// tasks/dynamic-scheduler.service.ts ✅
import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression, SchedulerRegistry } from '@nestjs/schedule';

@Injectable()
export class DynamicSchedulerService {
  private readonly logger = new Logger(DynamicSchedulerService.name);

  constructor(private schedulerRegistry: SchedulerRegistry) {}

  // ✅ Get job by name
  getCronJob(name: string) {
    return this.schedulerRegistry.getCronJob(name);
  }

  // ✅ Add cron job dynamically
  addCronJob(name: string, seconds: string) {
    const job = new CronJob(`${seconds} * * * * *`, () => {
      this.logger.warn(`Dynamic job ${name} executing!`);
    });

    this.schedulerRegistry.addCronJob(name, job);
    job.start();

    this.logger.log(`Job ${name} added to run at ${seconds} seconds`);
  }

  // ✅ Delete cron job
  deleteCronJob(name: string) {
    this.schedulerRegistry.deleteCronJob(name);
    this.logger.log(`Job ${name} deleted`);
  }

  // ✅ List all cron jobs
  listCronJobs() {
    const jobs = this.schedulerRegistry.getCronJobs();
    return Array.from(jobs.keys()).map(name => ({
      name,
      running: jobs.get(name).running,
    }));
  }

  // ✅ Pause and resume jobs
  pauseCronJob(name: string) {
    const job = this.schedulerRegistry.getCronJob(name);
    job.stop();
    this.logger.log(`Job ${name} paused`);
  }

  resumeCronJob(name: string) {
    const job = this.schedulerRegistry.getCronJob(name);
    job.start();
    this.logger.log(`Job ${name} resumed`);
  }
}
```

## Monitoring Scheduled Tasks

```typescript
// tasks/task-monitor.service.ts ✅
import { Injectable } from '@nestjs/common';
import { Cron, CronExpression, SchedulerRegistry } from '@nestjs/schedule';
import { CronJob } from 'cron';

@Injectable()
export class TaskMonitorService {
  constructor(private schedulerRegistry: SchedulerRegistry) {}

  @Cron(CronExpression.EVERY_HOUR)
  monitorScheduledTasks() {
    const jobs = this.schedulerRegistry.getCronJobs();
    const status: any[] = [];

    jobs.forEach((job, name) => {
      status.push({
        name,
        running: job.running,
        lastExecution: job.lastDate(),
        nextExecution: job.nextDate()?.toISO(),
      });
    });

    // Log or send to monitoring service
    console.table(status);
  }
}
```

## Testing Scheduled Tasks

```typescript
// tasks/scheduled-tasks.service.spec.ts ✅
import { Test, TestingModule } from '@nestjs/testing';
import { ScheduledTasksService } from './scheduled-tasks.service';
import { SchedulerRegistry } from '@nestjs/schedule';

describe('ScheduledTasksService', () => {
  let service: ScheduledTasksService;
  let schedulerRegistry: SchedulerRegistry;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ScheduledTasksService,
        {
          provide: PrismaService,
          useValue: { session: { deleteMany: jest.fn() } },
        },
        {
          provide: SchedulerRegistry,
          useValue: {
            addCronJob: jest.fn(),
            getCronJob: jest.fn(),
            deleteCronJob: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<ScheduledTasksService>(ScheduledTasksService);
    schedulerRegistry = module.get<SchedulerRegistry>(SchedulerRegistry);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should cleanup expired sessions', async () => {
    const deleteMany = jest.fn().mockResolvedValue({ count: 5 });
    service['prisma'].session.deleteMany = deleteMany;

    await service.cleanupExpiredSessions();

    expect(deleteMany).toHaveBeenCalledWith({
      where: { expiresAt: { lt: expect.any(Date) } },
    });
  });

  it('should handle errors gracefully', async () => {
    const loggerSpy = jest.spyOn(service['logger'], 'error');
    jest.spyOn(service['prisma'].session, 'deleteMany').mockRejectedValue(
      new Error('Database error')
    );

    await service.cleanupExpiredSessions();

    expect(loggerSpy).toHaveBeenCalled();
  });
});
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use `@nestjs/schedule` decorators | Proper NestJS lifecycle management |
| Use `CronExpression` enum | Readable, less error-prone |
| Always handle errors | Prevent cascading failures |
| Prevent overlapping executions | Avoid resource exhaustion |
| Log task execution | Monitor and debug issues |
| Use `@Interval()` for simple frequencies | More readable than cron |
| Use `@Timeout()` for startup tasks | One-time initialization |

**Sources:**
- [Task Scheduling | NestJS - Official Documentation](https://docs.nestjs.com/techniques/task-scheduling)
- [Cron Expression Format | crontab.guru](https://crontab.guru/)
- [Cron Documentation | npm](https://www.npmjs.com/package/cron)
