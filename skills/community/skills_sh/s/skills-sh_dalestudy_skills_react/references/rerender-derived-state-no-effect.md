---
title: Calculate Derived State During Rendering
impact: MEDIUM
impactDescription: avoids redundant renders and state drift
tags: rerender, derived-state, useEffect, state
---

## 파생 상태는 렌더링 중 계산

props/state에서 도출 가능한 값은 별도 useState + useEffect로 동기화하지 않기. 렌더링 중 직접 계산.

**Incorrect (불필요한 상태 + Effect):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState("First");
  const [lastName, setLastName] = useState("Last");
  const [fullName, setFullName] = useState("");

  useEffect(() => {
    setFullName(firstName + " " + lastName);
  }, [firstName, lastName]); // 추가 리렌더링 발생

  return <p>{fullName}</p>;
}
```

**Correct (렌더링 중 계산):**

```tsx
function Form() {
  const [firstName, setFirstName] = useState("First");
  const [lastName, setLastName] = useState("Last");
  const fullName = firstName + " " + lastName;

  return <p>{fullName}</p>;
}
```

비용 큰 계산은 `useMemo`:

```tsx
const fullName = useMemo(
  () => expensiveFormat(firstName, lastName),
  [firstName, lastName],
);
```

> [`rerender-derived-state`](rerender-derived-state.md)는 파생 boolean 구독 최적화, 이 규칙은 useEffect에서 파생 상태 제거.

> 참고: [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)

> 원본: [vercel-react-best-practices: rerender-derived-state-no-effect](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-derived-state-no-effect.md)
