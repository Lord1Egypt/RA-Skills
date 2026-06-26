# Reactive Resume API 开发参考

## 概述

Reactive Resume 使用 ORPC (Open RPC) 构建类型安全的 API。API 位于 `src/server/api/routers/` 目录。

## 架构

```
src/server/api/
├── root.ts           # 根路由，注册所有子路由
├── trpc.ts           # tRPC 配置
├── routers/
│   ├── auth.ts       # 认证相关
│   ├── resume.ts     # 简历 CRUD
│   ├── user.ts       # 用户管理
│   ├── template.ts   # 模板管理
│   └── ...
└── procedures/       # 可复用的 procedure
```

## 基础概念

### Router

```typescript
// src/server/api/routers/custom.ts
import { router, protectedProcedure } from '../trpc';
import { z } from 'zod';

export const customRouter = router({
  // Query (读取操作)
  getItems: protectedProcedure
    .input(z.object({
      page: z.number().default(1),
      limit: z.number().default(10),
    }))
    .query(async ({ ctx, input }) => {
      const items = await ctx.db.query.items.findMany({
        where: (items, { eq }) => eq(items.userId, ctx.user.id),
        limit: input.limit,
        offset: (input.page - 1) * input.limit,
      });
      return items;
    }),

  // Mutation (写入操作)
  createItem: protectedProcedure
    .input(z.object({
      name: z.string().min(1),
      description: z.string().optional(),
    }))
    .mutation(async ({ ctx, input }) => {
      const item = await ctx.db.insert.items.insert({
        userId: ctx.user.id,
        name: input.name,
        description: input.description,
      }).returning();
      return item[0];
    }),
});
```

### Procedure 类型

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| `publicProcedure` | 无需认证 | 公开数据查询 |
| `protectedProcedure` | 需要登录 | 用户数据操作 |
| `adminProcedure` | 需要管理员 | 管理功能 |

### 注册路由

```typescript
// src/server/api/root.ts
import { router } from './trpc';
import { authRouter } from './routers/auth';
import { resumeRouter } from './routers/resume';
import { customRouter } from './routers/custom';

export const appRouter = router({
  auth: authRouter,
  resume: resumeRouter,
  custom: customRouter,  // 添加新路由
});

export type AppRouter = typeof appRouter;
```

## 前端调用 API

### 使用 ORPC 客户端

```typescript
// src/lib/api.ts
import { createClient } from '@orpc/client';
import type { AppRouter } from '@/server/api/root';

export const api = createClient<AppRouter>({
  endpoint: '/api/rpc',
});

// 使用
const items = await api.custom.getItems.query({ page: 1, limit: 10 });
const newItem = await api.custom.createItem.mutate({ name: 'Test' });
```

### React Hook

```typescript
// src/hooks/use-items.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useItems() {
  return useQuery({
    queryKey: ['items'],
    queryFn: () => api.custom.getItems.query({ page: 1, limit: 10 }),
  });
}

export function useCreateItem() {
  return useMutation({
    mutationFn: (data: { name: string }) => 
      api.custom.createItem.mutate(data),
  });
}
```

## 数据库操作

### Drizzle ORM 基础

```typescript
import { db } from '@/server/db';
import { items } from '@/server/db/schema';

// 查询
const allItems = await db.query.items.findMany();
const itemById = await db.query.items.findFirst({
  where: (items, { eq }) => eq(items.id, '123'),
});

// 插入
await db.insert(items).values({
  userId: 'user-123',
  name: 'New Item',
});

// 更新
await db.update(items)
  .set({ name: 'Updated' })
  .where(eq(items.id, '123'));

// 删除
await db.delete(items)
  .where(eq(items.id, '123'));
```

### 关联查询

```typescript
// Schema 定义关系
export const resumes = pgTable('resumes', {
  id: uuid('id').primaryKey(),
  userId: uuid('user_id').references(() => users.id),
  // ...
});

export const usersRelations = relations(users, ({ many }) => ({
  resumes: many(resumes),
}));

// 查询关联数据
const userWithResumes = await db.query.users.findFirst({
  where: (users, { eq }) => eq(users.id, userId),
  with: {
    resumes: true,
  },
});
```

## 认证和授权

### 获取当前用户

```typescript
import { protectedProcedure } from '../trpc';

protectedProcedure.query(async ({ ctx }) => {
  // ctx.user 包含当前用户信息
  const userId = ctx.user.id;
  const userEmail = ctx.user.email;
});
```

### 权限检查

```typescript
import { TRPCError } from '@trpc/server';

protectedProcedure
  .input(z.object({ resumeId: z.string() }))
  .query(async ({ ctx, input }) => {
    const resume = await ctx.db.query.resumes.findFirst({
      where: (resumes, { eq }) => eq(resumes.id, input.resumeId),
    });

    if (!resume) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: 'Resume not found',
      });
    }

    // 检查所有权
    if (resume.userId !== ctx.user.id) {
      throw new TRPCError({
        code: 'FORBIDDEN',
        message: 'You do not own this resume',
      });
    }

    return resume;
  });
```

## 错误处理

### TRPCError 类型

```typescript
import { TRPCError } from '@trpc/server';

// 常见错误
throw new TRPCError({ code: 'BAD_REQUEST', message: 'Invalid input' });
throw new TRPCError({ code: 'UNAUTHORIZED', message: 'Not logged in' });
throw new TRPCError({ code: 'FORBIDDEN', message: 'No permission' });
throw new TRPCError({ code: 'NOT_FOUND', message: 'Resource not found' });
throw new TRPCError({ code: 'INTERNAL_SERVER_ERROR', message: 'Something went wrong' });
```

### 统一错误处理

```typescript
import { TRPCError } from '@trpc/server';
import { z } from 'zod';

protectedProcedure
  .input(z.object({ id: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    try {
      const result = await someOperation(input.id);
      return result;
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new TRPCError({
          code: 'BAD_REQUEST',
          message: 'Invalid input',
          cause: error,
        });
      }
      
      if (error instanceof DatabaseError) {
        throw new TRPCError({
          code: 'INTERNAL_SERVER_ERROR',
          message: 'Database error',
        });
      }
      
      throw error;
    }
  });
```

## 文件上传

### 配置存储

```typescript
// src/lib/storage.ts
import { S3Client } from '@aws-sdk/client-s3';

export const s3Client = new S3Client({
  endpoint: process.env.STORAGE_ENDPOINT,
  region: process.env.STORAGE_REGION,
  credentials: {
    accessKeyId: process.env.STORAGE_ACCESS_KEY_ID!,
    secretAccessKey: process.env.STORAGE_SECRET_ACCESS_KEY!,
  },
});
```

### 上传处理

```typescript
import { PutObjectCommand } from '@aws-sdk/client-s3';

protectedProcedure
  .input(z.object({
    file: z.instanceof(File),
    resumeId: z.string(),
  }))
  .mutation(async ({ ctx, input }) => {
    const buffer = await input.file.arrayBuffer();
    const key = `resumes/${ctx.user.id}/${input.resumeId}/${input.file.name}`;
    
    await s3Client.send(new PutObjectCommand({
      Bucket: process.env.STORAGE_BUCKET,
      Key: key,
      Body: Buffer.from(buffer),
      ContentType: input.file.type,
    }));
    
    return { url: `https://${process.env.STORAGE_BUCKET}/${key}` };
  });
```

## PDF 导出

### 调用 Printer 服务

```typescript
// src/lib/printer.ts
import puppeteer from 'puppeteer';

export async function generatePdf(resumeUrl: string): Promise<Buffer> {
  const browser = await puppeteer.connect({
    browserWSEndpoint: process.env.PRINTER_ENDPOINT!,
  });
  
  const page = await browser.newPage();
  await page.goto(resumeUrl, { waitUntil: 'networkidle0' });
  
  const pdf = await page.pdf({
    format: 'A4',
    printBackground: true,
  });
  
  await browser.close();
  return Buffer.from(pdf);
}
```

### API 端点

```typescript
protectedProcedure
  .input(z.object({ resumeId: z.string() }))
  .mutation(async ({ ctx, input }) => {
    const resumeUrl = `${process.env.APP_URL}/resume/${input.resumeId}`;
    const pdfBuffer = await generatePdf(resumeUrl);
    
    // 上传到存储或返回
    return { 
      pdf: pdfBuffer.toString('base64'),
      contentType: 'application/pdf',
    };
  });
```

## 性能优化

### 分页

```typescript
protectedProcedure
  .input(z.object({
    page: z.number().default(1),
    limit: z.number().default(10).max(100),
    cursor: z.string().optional(),
  }))
  .query(async ({ ctx, input }) => {
    const items = await ctx.db.query.items.findMany({
      limit: input.limit + 1, // 多取一个判断是否有下一页
      cursor: input.cursor ? { id: input.cursor } : undefined,
    });
    
    let nextCursor: string | undefined;
    if (items.length > input.limit) {
      const nextItem = items.pop();
      nextCursor = nextItem?.id;
    }
    
    return {
      items,
      nextCursor,
    };
  });
```

### 缓存

```typescript
import { cache } from 'react';

export const getResume = cache(async (id: string) => {
  const resume = await db.query.resumes.findFirst({
    where: (resumes, { eq }) => eq(resumes.id, id),
  });
  return resume;
});
```

## 测试 API

### 单元测试

```typescript
// tests/api/custom.test.ts
import { describe, it, expect } from 'vitest';
import { appRouter } from '@/server/api/root';
import { createCaller } from '../helpers';

describe('Custom Router', () => {
  it('should get items', async () => {
    const caller = createCaller(appRouter, { user: testUser });
    const items = await caller.custom.getItems({ page: 1, limit: 10 });
    expect(items).toBeDefined();
  });
});
```

## 最佳实践

### ✅ 推荐

- 使用 Zod 验证所有输入
- 统一的错误处理
- 适当的分页和限制
- 权限检查
- 使用事务处理多表操作
- 记录重要操作日志

### ❌ 避免

- 跳过输入验证
- 暴露敏感数据
- N+1 查询问题
- 无限制的数据返回
- 忽略错误处理

---

*参考：[ORPC 文档](https://orpc.unno.io/), [Drizzle 文档](https://orm.drizzle.team/)*
