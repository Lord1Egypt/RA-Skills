---
title: Use Functional setState Updates
impact: MEDIUM
impactDescription: prevents stale closures and unnecessary callback recreations
tags: react, hooks, useState, useCallback, callbacks, closures
---

## 함수형 setState

현재 상태 기반 업데이트 시 함수형 사용. 클로저 문제 방지, 안정적 콜백 참조.

**Incorrect (items 의존성 필요, 매번 재생성):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  const addItems = useCallback(
    (newItems: Item[]) => {
      setItems([...items, ...newItems]);
    },
    [items],
  ); // ❌ items 변경마다 재생성

  const removeItem = useCallback((id: string) => {
    setItems(items.filter((item) => item.id !== id));
  }, []); // ❌ items 의존성 누락 - stale closure!

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

**Correct (안정적 콜백, stale closure 없음):**

```tsx
function TodoList() {
  const [items, setItems] = useState(initialItems);

  const addItems = useCallback((newItems: Item[]) => {
    setItems((curr) => [...curr, ...newItems]);
  }, []); // ✅ 의존성 없음

  const removeItem = useCallback((id: string) => {
    setItems((curr) => curr.filter((item) => item.id !== id));
  }, []); // ✅ 안전하고 안정적

  return <ItemsEditor items={items} onAdd={addItems} onRemove={removeItem} />;
}
```

**함수형 업데이트 사용 시기:**
- 현재 상태에 의존하는 모든 setState
- useCallback/useMemo 내부에서 상태 필요 시
- 이벤트 핸들러에서 상태 참조 시
- 비동기 작업에서 상태 업데이트 시

**직접 업데이트 괜찮은 경우:**
- 정적 값 설정: `setCount(0)`
- props/인자만 사용: `setName(newName)`
- 이전 값에 의존하지 않는 경우

> [React Compiler](https://react.dev/learn/react-compiler) 사용 시에도 정확성과 stale closure 방지를 위해 함수형 업데이트 권장.

> 원본: [vercel-react-best-practices: rerender-functional-setstate](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-functional-setstate.md)
