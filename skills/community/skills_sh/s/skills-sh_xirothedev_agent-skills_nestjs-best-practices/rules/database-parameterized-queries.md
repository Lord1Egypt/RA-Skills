---
title: Use Parameterized Queries to Prevent SQL Injection
impact: CRITICAL
section: 6
impactDescription: Eliminates SQL injection vulnerabilities
tags: security, database, sql-injection, prisma
---

Raw SQL queries with string concatenation allow attackers to inject malicious code. Prisma Client automatically parameterizes all queries, preventing injection. **Never use string concatenation with user input.**

> **Hint**: Prisma v7 introduces the new `sql` template tag for raw queries. Always use tagged template literals instead of string concatenation. Prisma automatically parameterizes all variables passed to template tags.

## For AI Agents

When implementing or reviewing database queries, **always** follow these steps:

### Step 1: Check for Raw SQL Usage
**Pattern to check:** Look for `$queryRaw`, `$executeRaw`, or `sql` template tag usage.

```typescript
// ❌ WRONG - String concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;
await prisma.$queryRawUnsafe(query);

// ❌ WRONG - String concatenation with template literal
const query = `SELECT * FROM users WHERE name = '${name}' AND status = '${status}'`;
await prisma.$executeRawUnsafe(query);

// ✅ CORRECT - Prisma v7 sql template tag (auto-parameterized)
import { sql } from '@prisma/client/runtime/library';

const result = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE id = ${userId}
`;
```

**If found:** Replace with Prisma v7 `sql` template tag or typed queries.

### Step 2: Verify Prisma v7 Syntax for Raw Queries
**File:** Any service using Prisma

```typescript
// ✅ REQUIRED: Prisma v7 pattern with sql tag
import { sql } from '@prisma/client/runtime/library';

// Single parameter
const users = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE email = ${email}
`;

// Multiple parameters
const results = await prisma.$queryRaw`
  SELECT * FROM orders
  WHERE user_id = ${userId}
    AND status = ${status}
    AND created_at > ${since}
`;

// With JOIN
const userWithOrders = await prisma.$queryRaw`
  SELECT u.*, COUNT(o.id) as order_count
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.id
  WHERE u.id = ${userId}
  GROUP BY u.id
`;
```

### Step 3: Check Transaction Syntax
**Prisma v7 transaction pattern:**

```typescript
// ❌ WRONG - Old transaction syntax (v6 and below)
await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.post.create({ data: postData }),
]);

// ✅ CORRECT - Prisma v7 interactive transactions
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData });
  await tx.post.create({ data: { ...postData, userId: user.id } });
});
```

### Step 4: Verify Client Extension Patterns
**File:** `src/database/prisma.service.ts` or similar

```typescript
// ✅ CORRECT: Prisma v7 client extension for custom queries
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient().$extends({
  query: {
    $allOperations({ operation, args, query }) {
      // Log all queries
      console.log(`[Prisma] ${operation}`, args);
      return query(args);
    },
  },
});

// Extended client with custom methods
const extendedPrisma = new PrismaClient().$extends({
  model: {
    user: {
      async findByEmail(email: string) {
        return prisma.user.findFirst({ where: { email } });
      },
    },
  },
});
```

## Installation

```bash
bun add @prisma/client @prisma/adapter-pg
bun add -D prisma
```

## Quick Reference Checklist

Use this checklist when reviewing or creating database queries:

- [ ] No string concatenation in SQL queries
- [ ] All `$queryRaw` uses template literals with variables
- [ ] All `$executeRaw` uses template literals with variables
- [ ] Prisma v7 `sql` template tag imported when needed
- [ ] Transactions use async callback pattern
- [ ] Client extensions use `$extends()` method
- [ ] User input never interpolated directly into SQL

**Incorrect:**

```typescript
// users.service.ts - DANGEROUS 🚨

import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  // ❌ String concatenation - SQL INJECTION
  async findByName(name: string) {
    const query = `SELECT * FROM users WHERE name = '${name}'`;
    return this.prisma.$queryRawUnsafe(query);
  }

  // ❌ Template literal concatenation - VULNERABLE
  async findByEmailAndPassword(email: string, password: string) {
    const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
    return this.prisma.$executeRawUnsafe(query);
  }

  // ❌ Direct interpolation - VULNERABLE
  async searchUsers(searchTerm: string) {
    return this.prisma.$queryRaw(
      `SELECT * FROM users WHERE name LIKE '%${searchTerm}%'`
    );
  }

  // ❌ Old Prisma syntax (pre-v7)
  async oldTransactionPattern(userData: any, postData: any) {
    return this.prisma.$transaction([
      this.prisma.user.create({ data: userData }),
      this.prisma.post.create({ data: postData }),
    ]);
  }
}
```

**Correct:**

```typescript
// users.service.ts - SAFE ✅

import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { sql } from '@prisma/client/runtime/library';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  // ✅ Typed query - Safest option
  async findByName(name: string) {
    return this.prisma.user.findMany({
      where: { name },
    });
  }

  // ✅ Raw query with parameterization
  async findByEmail(email: string) {
    return this.prisma.$queryRaw`
      SELECT * FROM users
      WHERE email = ${email}
    `;
  }

  // ✅ Multiple parameters - All auto-parameterized
  async findByEmailAndStatus(email: string, status: string) {
    return this.prisma.$queryRaw`
      SELECT * FROM users
      WHERE email = ${email}
        AND status = ${status}
    `;
  }

  // ✅ Parameterized LIKE query
  async searchUsers(searchTerm: string) {
    return this.prisma.$queryRaw`
      SELECT * FROM users
      WHERE name LIKE ${`%${searchTerm}%`}
    `;
  }

  // ✅ Prisma v7 transaction pattern
  async createUserWithPost(userData: any, postData: any) {
    return this.prisma.$transaction(async (tx) => {
      const user = await tx.user.create({ data: userData });
      const post = await tx.post.create({
        data: { ...postData, userId: user.id },
      });
      return { user, post };
    });
  }

  // ✅ Complex JOIN with parameterization
  async getUserWithOrderCount(userId: string) {
    return this.prisma.$queryRaw`
      SELECT
        u.id,
        u.name,
        u.email,
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent
      FROM users u
      LEFT JOIN orders o ON o.user_id = u.id
      WHERE u.id = ${userId}
      GROUP BY u.id, u.name, u.email
    `;
  }

  // ✅ Execute raw with parameterization
  async bulkUpdateStatus(userIds: string[], newStatus: string) {
    return this.prisma.$executeRaw`
      UPDATE users
      SET status = ${newStatus}, updated_at = NOW()
      WHERE id = ANY(${userIds})
    `;
  }
}
```

## Prisma v7 Raw Query Examples

### Basic SELECT Queries

```typescript
import { sql } from '@prisma/client/runtime/library';

// Simple WHERE
const users = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE status = ${status}
    AND created_at > ${since}
`;

// IN clause with array
const activeUsers = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE id IN (${[userId1, userId2, userId3]})
`;

// ORDER BY with dynamic column (use sql tag for identifiers)
const users = await prisma.$queryRaw`
  SELECT * FROM users
  ORDER BY ${sql('created_at')} ${sortOrder === 'asc' ? sql('ASC') : sql('DESC')}
  LIMIT ${limit} OFFSET ${offset}
`;
```

### INSERT, UPDATE, DELETE

```typescript
// INSERT with returning
const newUser = await prisma.$queryRaw`
  INSERT INTO users (name, email, status)
  VALUES (${name}, ${email}, ${status})
  RETURNING *
`;

// UPDATE
const updated = await prisma.$executeRaw`
  UPDATE users
  SET status = ${newStatus}, updated_at = NOW()
  WHERE id = ${userId}
`;

// DELETE with returning
const deleted = await prisma.$queryRaw`
  DELETE FROM sessions
  WHERE expires_at < NOW()
  RETURNING *
`;
```

### Complex Queries

```typescript
// Aggregation
const stats = await prisma.$queryRaw`
  SELECT
    DATE(created_at) as date,
    COUNT(*) as count,
    SUM(amount) as total
  FROM orders
  WHERE created_at >= ${startDate}
    AND created_at <= ${endDate}
  GROUP BY DATE(created_at)
  ORDER BY date DESC
`;

// CTE (Common Table Expression)
const paginatedResults = await prisma.$queryRaw`
  WITH user_orders AS (
    SELECT
      u.id,
      u.name,
      u.email,
      COUNT(o.id) as order_count,
      ROW_NUMBER() OVER (ORDER BY COUNT(o.id) DESC) as rn
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.name, u.email
  )
  SELECT * FROM user_orders
  WHERE rn BETWEEN ${offset + 1} AND ${offset + limit}
`;

// UNION
const allItems = await prisma.$queryRaw`
  SELECT id, name, 'product' as type FROM products
  WHERE name ILIKE ${`%${search}%`}
  UNION
  SELECT id, name, 'category' as type FROM categories
  WHERE name ILIKE ${`%${search}%`}
`;
```

## Prisma v7 Transaction Patterns

### Interactive Transactions

```typescript
// Single operation transaction
await prisma.$transaction(async (tx) => {
  const account = await tx.account.update({
    where: { id: accountId },
    data: { balance: { decrement: amount } },
  });

  if (account.balance < 0) {
    throw new Error('Insufficient funds');
  }

  await tx.transaction.create({
    data: {
      accountId,
      amount,
      type: 'WITHDRAWAL',
    },
  });
});

// Multiple related operations
await prisma.$transaction(async (tx) => {
  // Create order
  const order = await tx.order.create({
    data: {
      userId,
      total: cartTotal,
      status: 'PENDING',
    },
  });

  // Create order items
  await tx.orderItem.createMany({
    data: cartItems.map(item => ({
      orderId: order.id,
      productId: item.productId,
      quantity: item.quantity,
      price: item.price,
    })),
  });

  // Update inventory
  for (const item of cartItems) {
    await tx.product.update({
      where: { id: item.productId },
      data: { stock: { decrement: item.quantity } },
    });
  }

  return order;
});
```

### Transaction Options

```typescript
// With timeout
await prisma.$transaction(
  async (tx) => {
    // Operations here
  },
  {
    maxWait: 5000,  // Max time to wait for transaction
    timeout: 10000, // Max time for transaction execution
  }
);
```

## Client Extensions (Prisma v7)

### Logging Extension

```typescript
// prisma.service.ts
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    super({
      log: ['query', 'info', 'warn', 'error'],
    });

    // Add query logging extension
    this.$extends({
      query: {
        $allOperations({ operation, model, args, query }) {
          const start = Date.now();
          const result = query(args);
          const end = Date.now();
          console.log(`[Prisma] ${model}.${operation} took ${end - start}ms`);
          return result;
        },
      },
    });
  }

  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

### Model Extensions

```typescript
// Extended client with custom methods
const prisma = new PrismaClient().$extends({
  model: {
    user: {
      async findByEmail(email: string) {
        return prisma.user.findUnique({ where: { email } });
      },
      async findActive() {
        return prisma.user.findMany({ where: { status: 'ACTIVE' } });
      },
    },
    order: {
      async calculateTotal(orderId: string) {
        const items = await prisma.orderItem.findMany({
          where: { orderId },
        });
        return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    },
  },
});

// Usage
const user = await prisma.user.findByEmail('user@example.com');
const total = await prisma.order.calculateTotal('order-123');
```

## Best Practices Summary

| Practice | Why |
|----------|-----|
| Use typed queries | Type-safe, auto-parameterized |
| Avoid raw queries when possible | Prisma handles security automatically |
| Use `sql` template tag | Auto-parameterizes variables |
| Never concatenate strings | Prevents SQL injection |
| Use interactive transactions | Better error handling in v7 |
| Use client extensions | Reusable query patterns |

**Sources:**
- [Prisma v7 Release Notes](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Raw Database Queries | Prisma Documentation](https://www.prisma.io/docs/orm/prisma-client/queries/raw-database-access)
- [Transactions | Prisma Documentation](https://www.prisma.io/docs/orm/prisma-client/transactions)
- [SQL Injection | OWASP](https://owasp.org/www-community/attacks/SQL_Injection)
