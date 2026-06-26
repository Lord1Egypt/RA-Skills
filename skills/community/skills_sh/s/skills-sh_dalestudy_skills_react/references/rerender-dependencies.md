---
title: Narrow Effect Dependencies
impact: LOW
impactDescription: minimizes effect re-runs
tags: react, hooks, useEffect, dependencies, optimization
---

## Effect 의존성 좁히기

객체 대신 원시값을 의존성으로 사용하여 불필요한 Effect 재실행 방지.

**Incorrect (user 객체의 아무 필드 변경 시 재실행):**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user]);
```

**Correct (id 변경 시에만 재실행):**

```tsx
useEffect(() => {
  console.log(user.id);
}, [user.id]);
```

**파생 상태로 Effect 외부에서 계산:**

```tsx
// Incorrect: width=767, 766, 765... 모두 실행
useEffect(() => {
  if (width < 768) enableMobileMode();
}, [width]);

// Correct: boolean 전환 시에만 실행
const isMobile = width < 768;
useEffect(() => {
  if (isMobile) enableMobileMode();
}, [isMobile]);
```

> 원본: [vercel-react-best-practices: rerender-dependencies](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-dependencies.md)
