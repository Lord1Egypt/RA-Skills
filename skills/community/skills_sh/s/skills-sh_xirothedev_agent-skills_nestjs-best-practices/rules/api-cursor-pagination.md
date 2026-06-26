---
title: Use Cursor-Based Pagination for Large Datasets
impact: HIGH
section: 8
impactDescription: 10-100x faster than offset for large datasets
tags: api, pagination, performance, prisma
---

Offset-based pagination (`OFFSET` + `LIMIT`) becomes slow as the offset grows because the database must scan and discard all previous rows. Cursor-based pagination uses indexed columns to jump directly to the correct position, providing consistent performance regardless of page depth.

> **Hint**: Use cursor pagination for infinite scroll, real-time feeds, and large datasets. Keep offset pagination only for small datasets with direct page jumping.

## For AI Agents

When implementing or reviewing pagination, **always** follow these steps:

### Step 1: Check Pagination Pattern
**Pattern to check:** Look for `skip`/`take` or `offset`/`limit` parameters.

```typescript
// ❌ WRONG - Offset pagination (slow for large offsets)
async getUsers(page: number, limit: number) {
  return prisma.user.findMany({
    skip: (page - 1) * limit,  // Scans and discards rows
    take: limit,
  });
}

// ✅ CORRECT - Cursor pagination (fast at any depth)
async getUsers(first: number, after?: string) {
  return prisma.user.findMany({
    take: first,
    cursor: after ? { id: after } : undefined,
    orderBy: { id: 'asc' },
  });
}
```

**If found:** Replace offset pagination with cursor pagination.

### Step 2: Create Pagination DTO
**File:** `src/common/dto/pagination.dto.ts`

```typescript
// ✅ REQUIRED: Pagination DTO
import { IsOptional, IsInt, Min, IsString } from 'class-validator';
import { Type } from 'class-transformer';

export class CursorPaginationDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  first?: number = 20;  // Number of items to fetch

  @IsOptional()
  @IsString()
  after?: string;  // Cursor of the last item from previous page

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  last?: number;  // For backward pagination

  @IsOptional()
  @IsString()
  before?: string;  // Cursor of first item from next page
}
```

### Step 3: Implement Cursor Pagination Service
**File:** `src/users/users.service.ts`

```typescript
// ✅ REQUIRED: Service with cursor pagination
@Injectable()
export class UsersService {
  async findAll(dto: CursorPaginationDto) {
    const { first, after, last, before } = dto;

    // Forward pagination
    if (first || after) {
      const take = first || 20;
      return this.prisma.user.findMany({
        take: take + 1,  // Fetch one extra to check if there's a next page
        cursor: after ? { id: after } : undefined,
        orderBy: { createdAt: 'desc' },
      });
    }

    // Backward pagination
    if (last || before) {
      const take = last || 20;
      return this.prisma.user.findMany({
        take: take + 1,
        cursor: before ? { id: before } : undefined,
        skip: 1,  // Skip the cursor item itself
        orderBy: { createdAt: 'asc' },
      });
    }

    // Default: first page
    return this.prisma.user.findMany({
      take: 21,
      orderBy: { createdAt: 'desc' },
    });
  }
}
```

### Step 4: Return Paginated Response
**File:** `src/users/interfaces/paginated-result.interface.ts`

```typescript
// ✅ REQUIRED: Paginated response interface
export interface PaginatedResult<T> {
  items: T[];
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  startCursor?: string;
  endCursor?: string;
  totalCount?: number;
}
```

## Installation

```bash
# Prisma is already installed
# Additional utilities for cursor encoding (optional)
bun add base64url
```

## Quick Reference Checklist

Use this checklist when reviewing or creating paginated endpoints:

- [ ] Pagination uses cursor-based approach (not offset/skip)
- [ ] Cursor is based on indexed column (usually `id` or `createdAt`)
- [ ] Response includes `hasNextPage`/`hasPreviousPage` flags
- [ ] Response includes `startCursor`/`endCursor` for navigation
- [ ] Fetches one extra item to determine if there's a next page
- [ ] Handles edge cases (first page, last page, empty results)
- [ ] Cursor is safely encoded/decoded (base64url recommended)

**Incorrect:**

```typescript
// dto/get-users.dto.ts - Offset pagination 🚨
export class GetUsersDto {
  @IsInt()
  @Min(1)
  page: number = 1;

  @IsInt()
  @Min(1)
  @Max(100)
  limit: number = 20;
}

// users.controller.ts - Offset based 🚨
@Controller('users')
export class UsersController {
  @Get()
  async findAll(@Query() dto: GetUsersDto) {
    return this.usersService.findAll(dto);
  }
}

// users.service.ts - OFFSET scans all rows 🚨
@Injectable()
export class UsersService {
  async findAll(dto: GetUsersDto) {
    const { page, limit } = dto;
    const skip = (page - 1) * limit;

    // Page 1000: scans 19,980 rows just to return 20!
    const [users, total] = await Promise.all([
      this.prisma.user.findMany({
        skip,  // ❌ Scans and discards rows
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      this.prisma.user.count(),
    ]);

    return {
      data: users,
      meta: {
        total,
        page,
        limit,
        totalPages: Math.ceil(total / limit),
      },
    };
  }
}

/* Performance issues:
 * Page 1:    ~1ms    (scans 0 rows)
 * Page 10:   ~5ms    (scans 180 rows)
 * Page 100:  ~50ms   (scans 1,980 rows)
 * Page 1000: ~500ms  (scans 19,980 rows)
 * Page 10000: ~5000ms (scans 199,980 rows)
 */
```

**Correct:**

```typescript
// dto/get-users.dto.ts - Cursor pagination ✅
import { IsOptional, IsInt, Min, Max, IsString } from 'class-validator';
import { Type } from 'class-transformer';

export class GetUsersDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  first?: number = 20;  // Number of items

  @IsOptional()
  @IsString()
  after?: string;  // Cursor (base64url encoded)

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  last?: number;  // For backward pagination

  @IsOptional()
  @IsString()
  before?: string;
}

// interfaces/paginated-result.interface.ts ✅
export interface PaginatedResult<T> {
  items: T[];
  pageInfo: {
    hasNextPage: boolean;
    hasPreviousPage: boolean;
    startCursor?: string;
    endCursor?: string;
  };
  totalCount?: number;
}

// utils/cursor.util.ts ✅
import { base64url } from 'base64url';

export interface Cursor {
  id: string;
  createdAt?: string;
}

export function encodeCursor(cursor: Cursor): string {
  return base64url.encode(JSON.stringify(cursor));
}

export function decodeCursor(cursor: string): Cursor {
  return JSON.parse(base64url.decode(cursor));
}

// users.service.ts - Cursor pagination ✅
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { GetUsersDto } from './dto/get-users.dto';
import { PaginatedResult } from '../interfaces/paginated-result.interface';
import { encodeCursor, decodeCursor, Cursor } from '../utils/cursor.util';

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async findAll(dto: GetUsersDto): Promise<PaginatedResult<any>> {
    const { first = 20, after, last, before } = dto;

    // Forward pagination
    if (first || after) {
      return this.paginateForward(first, after);
    }

    // Backward pagination
    if (last || before) {
      return this.paginateBackward(last, before);
    }

    // Default: first page forward
    return this.paginateForward(20);
  }

  private async paginateForward(first: number, after?: string) {
    const cursor = after ? decodeCursor(after) : undefined;

    const items = await this.prisma.user.findMany({
      take: first + 1,  // Fetch extra to check for next page
      cursor: cursor ? { id: cursor.id } : undefined,
      orderBy: [{ createdAt: 'desc' }, { id: 'desc' }],
    });

    const hasNextPage = items.length > first;
    const slicedItems = hasNextPage ? items.slice(0, first) : items;

    return {
      items: slicedItems,
      pageInfo: {
        hasNextPage,
        hasPreviousPage: !!after,
        startCursor: slicedItems[0]
          ? encodeCursor({ id: slicedItems[0].id })
          : undefined,
        endCursor: slicedItems[slicedItems.length - 1]
          ? encodeCursor({ id: slicedItems[slicedItems.length - 1].id })
          : undefined,
      },
    };
  }

  private async paginateBackward(last: number, before?: string) {
    const cursor = before ? decodeCursor(before) : undefined;

    const items = await this.prisma.user.findMany({
      take: last + 1,
      cursor: cursor ? { id: cursor.id } : undefined,
      skip: 1,  // Skip the cursor item
      orderBy: [{ createdAt: 'asc' }, { id: 'asc' }],
    });

    const hasPreviousPage = items.length > last;
    const slicedItems = hasPreviousPage ? items.slice(0, last) : items;

    // Reverse to maintain original order
    const reversedItems = slicedItems.reverse();

    return {
      items: reversedItems,
      pageInfo: {
        hasNextPage: !!before,
        hasPreviousPage: hasPreviousPage,
        startCursor: reversedItems[0]
          ? encodeCursor({ id: reversedItems[0].id })
          : undefined,
        endCursor: reversedItems[reversedItems.length - 1]
          ? encodeCursor({ id: reversedItems[reversedItems.length - 1].id })
          : undefined,
      },
    };
  }
}

// users.controller.ts ✅
@Controller('users')
export class UsersController {
  @Get()
  findAll(@Query() dto: GetUsersDto) {
    return this.usersService.findAll(dto);
  }
}

/* Performance:
 * Page 1:     ~1ms (consistent)
 * Page 10:    ~1ms (consistent)
 * Page 100:   ~1ms (consistent)
 * Page 1000:  ~1ms (consistent)
 * Page 10000: ~1ms (consistent)
 */
```

## Cursor Pagination with Prisma

### Basic Cursor Pagination

```typescript
// Simple forward pagination
const users = await prisma.user.findMany({
  take: 20,
  cursor: { id: lastUserId },  // Start from this user
  orderBy: { id: 'asc' },
});

// With compound cursor (multiple columns)
const posts = await prisma.post.findMany({
  take: 20,
  cursor: {
    userId_createdAt: {
      userId: lastUserId,
      createdAt: lastCreatedAt,
    },
  },
  orderBy: [
    { userId: 'desc' },
    { createdAt: 'desc' },
  ],
});
```

### Relay-Style Pagination (Recommended)

```typescript
// interfaces/connection.interface.ts
export interface Connection<T> {
  edges: Edge<T>[];
  pageInfo: PageInfo;
  totalCount?: number;
}

export interface Edge<T> {
  node: T;
  cursor: string;
}

export interface PageInfo {
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  startCursor?: string;
  endCursor?: string;
}

// users.service.ts
async findConnection(dto: CursorPaginationDto): Promise<Connection<any>> {
  const { first = 20, after } = dto;
  const cursor = after ? decodeCursor(after) : undefined;

  const nodes = await this.prisma.user.findMany({
    take: first + 1,
    cursor: cursor ? { id: cursor.id } : undefined,
    orderBy: { createdAt: 'desc' },
  });

  const hasNextPage = nodes.length > first;
  const slicedNodes = hasNextPage ? nodes.slice(0, first) : nodes;

  const edges = slicedNodes.map((node) => ({
    node,
    cursor: encodeCursor({ id: node.id, createdAt: node.createdAt }),
  }));

  return {
    edges,
    pageInfo: {
      hasNextPage,
      hasPreviousPage: !!after,
      startCursor: edges[0]?.cursor,
      endCursor: edges[edges.length - 1]?.cursor,
    },
  };
}
```

## Edge Cases and Solutions

### Empty Results

```typescript
async findAll(dto: CursorPaginationDto) {
  const items = await this.prisma.user.findMany({
    take: dto.first + 1,
    cursor: dto.after ? { id: decodeCursor(dto.after).id } : undefined,
    orderBy: { createdAt: 'desc' },
  });

  // Handle empty result
  if (items.length === 0) {
    return {
      items: [],
      pageInfo: {
        hasNextPage: false,
        hasPreviousPage: !!dto.after,
      },
    };
  }

  // ... rest of logic
}
```

### Invalid Cursor

```typescript
async findAll(dto: CursorPaginationDto) {
  let cursor: Cursor | undefined;

  try {
    cursor = dto.after ? decodeCursor(dto.after) : undefined;
  } catch (error) {
    // Invalid cursor - start from beginning
    cursor = undefined;
  }

  // ... rest of logic
}
```

### Deleted Items

```typescript
// Use a unique compound cursor for stability
async findAll(dto: CursorPaginationDto) {
  const { first, after } = dto;
  const cursor = after ? decodeCursor(after) : undefined;

  const items = await this.prisma.post.findMany({
    take: first + 1,
    cursor: cursor
      ? {
          userId_createdAt_id: {
            userId: cursor.userId,
            createdAt: new Date(cursor.createdAt!),
            id: cursor.id,
          },
        }
      : undefined,
    orderBy: [
      { userId: 'desc' },
      { createdAt: 'desc' },
      { id: 'desc' },
    ],
  });

  // ... rest of logic
}
```

## Frontend Integration

### React Example

```typescript
// hooks/useUsers.ts
import { useState, useCallback } from 'react';

interface UseUsersResult {
  users: User[];
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  loadNext: () => void;
  loadPrevious: () => void;
}

export function useUsers(): UseUsersResult {
  const [users, setUsers] = useState<User[]>([]);
  const [endCursor, setEndCursor] = useState<string>();
  const [startCursor, setStartCursor] = useState<string>();
  const [hasNextPage, setHasNextPage] = useState(false);
  const [hasPreviousPage, setHasPreviousPage] = useState(false);

  const loadNext = useCallback(async () => {
    const response = await fetch(
      `/api/users?first=20${endCursor ? `&after=${endCursor}` : ''}`
    );
    const data = await response.json();

    setUsers(data.items);
    setEndCursor(data.pageInfo.endCursor);
    setStartCursor(data.pageInfo.startCursor);
    setHasNextPage(data.pageInfo.hasNextPage);
    setHasPreviousPage(data.pageInfo.hasPreviousPage);
  }, [endCursor]);

  const loadPrevious = useCallback(async () => {
    const response = await fetch(
      `/api/users?last=20&before=${startCursor}`
    );
    const data = await response.json();

    setUsers(data.items);
    setEndCursor(data.pageInfo.endCursor);
    setStartCursor(data.pageInfo.startCursor);
    setHasNextPage(data.pageInfo.hasNextPage);
    setHasPreviousPage(data.pageInfo.hasPreviousPage);
  }, [startCursor]);

  return {
    users,
    hasNextPage,
    hasPreviousPage,
    loadNext,
    loadPrevious,
  };
}
```

### Infinite Scroll Component

```tsx
// components/UserInfiniteScroll.tsx
import { useEffect, useRef } from 'react';
import { useUsers } from '../hooks/useUsers';

export function UserInfiniteScroll() {
  const { users, hasNextPage, loadNext } = useUsers();
  const observerRef = useRef<IntersectionObserver>();

  const lastUserRef = (node: HTMLLIElement) => {
    if (observerRef.current) observerRef.current.disconnect();

    observerRef.current = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && hasNextPage) {
        loadNext();
      }
    });

    if (node) observerRef.current.observe(node);
  };

  return (
    <ul>
      {users.map((user, index) => (
        <li
          key={user.id}
          ref={index === users.length - 1 ? lastUserRef : undefined}
        >
          {user.name}
        </li>
      ))}
    </ul>
  );
}
```

## Comparison: Offset vs Cursor

| Aspect | Offset Pagination | Cursor Pagination |
|--------|------------------|-------------------|
| **Performance** | Degrades with page number | Consistent |
| **Deep pages** | Very slow (scans rows) | Same speed as page 1 |
| **Page jumping** | Easy (go to page 100) | Not supported |
| **Real-time updates** | Shows duplicate/missing items | Handles new items well |
| **Implementation** | Simple | More complex |
| **Use case** | Small datasets, admin panels | Infinite scroll, feeds |

## When to Use Each

**Use Cursor Pagination When:**
- Large datasets (>10,000 rows)
- Infinite scroll UI
- Real-time data feeds
- Mobile apps (better performance)
- Social media-style pagination

**Use Offset Pagination When:**
- Small datasets (<1,000 rows)
- Need page jumping (direct page access)
- Admin panels with pagination controls
- Static data that doesn't change often

**Sources:**
- [Pagination | Prisma Documentation](https://www.prisma.io/docs/concepts/components/prisma-client/pagination)
- [Relay Cursor Connections Specification](https://relay.dev/graphql/connections.htm)
- [PostgreSQL Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
