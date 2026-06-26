---
title: Promise.all() for Independent Operations
impact: CRITICAL
impactDescription: 2-10x improvement
tags: async, parallelization, promises, waterfalls
---

## Promise.all()로 독립 작업 병렬화

비동기 작업 간 의존성이 없으면 `Promise.all()`로 동시 실행.

**Incorrect (순차 실행, 3 round trip):**

```typescript
const user = await fetchUser();
const posts = await fetchPosts();
const comments = await fetchComments();
```

**Correct (병렬 실행, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments(),
]);
```

> 원본: [vercel-react-best-practices: async-parallel](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-parallel.md)
