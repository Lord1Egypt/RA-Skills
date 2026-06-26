---
title: Don't Wrap Simple Expressions in useMemo
impact: LOW-MEDIUM
impactDescription: useMemo overhead exceeds computation cost
tags: rerender, useMemo, optimization
---

## 단순 표현식에 useMemo 사용하지 않기

논리/산술 연산 몇 개와 원시 결과(boolean, number, string)인 경우 `useMemo` 오버헤드가 계산 자체보다 큼.

**Incorrect:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = useMemo(() => {
    return user.isLoading || notifications.isLoading;
  }, [user.isLoading, notifications.isLoading]);

  if (isLoading) return <Skeleton />;
  // ...
}
```

**Correct:**

```tsx
function Header({ user, notifications }: Props) {
  const isLoading = user.isLoading || notifications.isLoading;

  if (isLoading) return <Skeleton />;
  // ...
}
```

**useMemo가 필요한 경우:**
- 배열/객체 생성 (`.filter()`, `.map()`, `{ ... }`)
- 비용 큰 계산 (정렬, 포맷팅, 파싱)
- 자식 컴포넌트에 참조 안정성이 필요한 경우

> 원본: [vercel-react-best-practices: rerender-simple-expression-in-memo](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-simple-expression-in-memo.md)
