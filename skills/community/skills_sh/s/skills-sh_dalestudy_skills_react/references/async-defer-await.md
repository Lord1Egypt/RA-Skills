---
title: Defer Await Until Needed
impact: HIGH
impactDescription: avoids blocking unused code paths
tags: async, await, early-return, optimization
---

## await 지연

사용하지 않는 경로에서 `await`를 지연시켜 불필요한 블로킹 방지.

**Incorrect (항상 대기):**

```typescript
async function handleRequest(userId: string, skip: boolean) {
  const data = await fetchUserData(userId);
  if (skip) return { skipped: true };
  return processUserData(data);
}
```

**Correct (필요할 때만 대기):**

```typescript
async function handleRequest(userId: string, skip: boolean) {
  if (skip) return { skipped: true };
  const data = await fetchUserData(userId);
  return processUserData(data);
}
```

**또 다른 예: early return 최적화**

```typescript
// Incorrect: 항상 permissions 페칭
async function updateResource(resourceId: string, userId: string) {
  const permissions = await fetchPermissions(userId);
  const resource = await getResource(resourceId);
  if (!resource) return { error: "Not found" };
  if (!permissions.canEdit) return { error: "Forbidden" };
  return await updateResourceData(resource, permissions);
}

// Correct: 필요한 경우에만 페칭
async function updateResource(resourceId: string, userId: string) {
  const resource = await getResource(resourceId);
  if (!resource) return { error: "Not found" };
  const permissions = await fetchPermissions(userId);
  if (!permissions.canEdit) return { error: "Forbidden" };
  return await updateResourceData(resource, permissions);
}
```

skip되는 분기가 자주 실행되거나, 지연시키는 작업이 비용이 클수록 효과 큼.

> 원본: [vercel-react-best-practices: async-defer-await](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-defer-await.md)
