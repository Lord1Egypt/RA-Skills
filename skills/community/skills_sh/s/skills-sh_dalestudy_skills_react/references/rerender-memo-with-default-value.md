---
title: Extract Default Values from Memoized Components
impact: MEDIUM
impactDescription: restores broken memoization
tags: rerender, memo, optimization, default-values
---

## memo 컴포넌트의 기본값을 상수로 추출

`memo()` 컴포넌트에서 비원시 기본값(함수, 배열, 객체)은 매 렌더링마다 새 인스턴스 생성 → 메모이제이션 무효화.

**Incorrect (매 렌더링마다 새 함수 → memo 무효):**

```tsx
const UserAvatar = memo(function UserAvatar({
  onClick = () => {},
}: {
  onClick?: () => void;
}) {
  // ...
});

<UserAvatar />; // onClick이 매번 새 함수 → 항상 리렌더링
```

**Correct (상수로 추출):**

```tsx
const NOOP = () => {};

const UserAvatar = memo(function UserAvatar({
  onClick = NOOP,
}: {
  onClick?: () => void;
}) {
  // ...
});

<UserAvatar />; // NOOP은 항상 같은 참조 → memo 정상 작동
```

**배열/객체도 동일:**

```tsx
// ❌ 매번 새 배열
const List = memo(({ items = [] }: { items?: string[] }) => { /* ... */ });

// ✅ 상수
const EMPTY_ARRAY: string[] = [];
const List = memo(({ items = EMPTY_ARRAY }: { items?: string[] }) => { /* ... */ });
```

> 원본: [vercel-react-best-practices: rerender-memo-with-default-value](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-memo-with-default-value.md)
