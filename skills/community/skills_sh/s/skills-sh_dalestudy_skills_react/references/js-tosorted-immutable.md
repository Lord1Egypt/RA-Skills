---
title: Use toSorted() Instead of sort() for Immutability
impact: MEDIUM-HIGH
impactDescription: prevents mutation bugs in React state
tags: javascript, sort, immutability, react, state
---

## toSorted()로 불변성 유지

`.sort()`는 원본 배열을 변이. React 상태/props의 불변성 원칙 위반. `.toSorted()`로 새 배열 생성.

**Incorrect (원본 배열 변이):**

```typescript
function UserList({ users }: { users: User[] }) {
  const sorted = useMemo(
    () => users.sort((a, b) => a.name.localeCompare(b.name)),
    [users],
  );
  return <div>{sorted.map(renderUser)}</div>;
}
```

**Correct (새 배열 생성):**

```typescript
function UserList({ users }: { users: User[] }) {
  const sorted = useMemo(
    () => users.toSorted((a, b) => a.name.localeCompare(b.name)),
    [users],
  );
  return <div>{sorted.map(renderUser)}</div>;
}
```

**구 브라우저 fallback:**

```typescript
const sorted = [...items].sort((a, b) => a.value - b.value);
```

**기타 불변 배열 메서드:** `.toReversed()`, `.toSpliced()`, `.with()`

> 원본: [vercel-react-best-practices: js-tosorted-immutable](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-tosorted-immutable.md)
