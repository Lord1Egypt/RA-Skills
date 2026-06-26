---
title: Dependency-Based Parallelization
impact: CRITICAL
impactDescription: 2-10x improvement by maximizing parallelism
tags: async, parallelization, dependencies, promise
---

## 의존성 기반 병렬화

부분 의존성이 있는 비동기 작업에서 독립 작업을 최대한 병렬 실행.

**Incorrect (profile이 config를 불필요하게 대기):**

```tsx
const [user, config] = await Promise.all([fetchUser(), fetchConfig()]);
const profile = await fetchProfile(user.id);
// config와 profile은 독립적인데 순차 실행
```

**Correct (Promise 체이닝으로 최대 병렬화):**

```tsx
const userPromise = fetchUser();
const profilePromise = userPromise.then((user) => fetchProfile(user.id));

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(), // user와 독립 → 즉시 시작
  profilePromise, // user 완료 후 즉시 시작, config와 병렬
]);
```

> [`async-parallel`](async-parallel.md)은 독립 작업 병렬화, 이 규칙은 **부분 의존성**이 있는 경우.

> 원본: [vercel-react-best-practices: async-dependencies](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-dependencies.md)
