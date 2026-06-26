---
title: Extract to Memoized Components
impact: MEDIUM
impactDescription: enables early returns
tags: react, memo, useMemo, optimization, components
---

## memo로 비용 큰 작업 분리

비용이 큰 계산을 memo된 컴포넌트로 추출하여, 불필요한 경우 계산을 건너뜀.

**Incorrect (loading 시에도 avatar 계산):**

```tsx
function Profile({ user, loading }: Props) {
  const avatar = useMemo(() => {
    const id = computeAvatarId(user);
    return <Avatar id={id} />;
  }, [user]);

  if (loading) return <Skeleton />;
  return <div>{avatar}</div>;
}
```

**Correct (loading 시 계산 건너뜀):**

```tsx
const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const id = useMemo(() => computeAvatarId(user), [user]);
  return <Avatar id={id} />;
});

function Profile({ user, loading }: Props) {
  if (loading) return <Skeleton />;
  return (
    <div>
      <UserAvatar user={user} />
    </div>
  );
}
```

> [React Compiler](https://react.dev/learn/react-compiler) 사용 시 `memo()`, `useMemo()` 수동 적용 불필요.

> 원본: [vercel-react-best-practices: rerender-memo](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-memo.md)
