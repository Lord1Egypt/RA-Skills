---
title: Build Index Maps for Repeated Lookups
impact: LOW-MEDIUM
impactDescription: 1M ops to 2K ops
tags: javascript, map, lookup, performance, optimization
---

## Map으로 반복 조회 최적화

같은 키로 `.find()`를 여러 번 호출하면 Map 사용.

**Incorrect (O(n) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  return orders.map((order) => ({
    ...order,
    user: users.find((u) => u.id === order.userId),
  }));
}
```

**Correct (O(1) per lookup):**

```typescript
function processOrders(orders: Order[], users: User[]) {
  const userById = new Map(users.map((u) => [u.id, u]));
  return orders.map((order) => ({
    ...order,
    user: userById.get(order.userId),
  }));
}
```

Map 빌드 O(n) 후 모든 조회 O(1). 1000 orders x 1000 users: 1M ops → 2K ops.

> 원본: [vercel-react-best-practices: js-index-maps](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-index-maps.md)
