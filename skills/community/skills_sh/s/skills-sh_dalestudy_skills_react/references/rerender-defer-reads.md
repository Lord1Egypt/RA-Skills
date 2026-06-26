---
title: Defer State Reads to Usage Point
impact: MEDIUM
impactDescription: avoids unnecessary subscriptions and re-renders
tags: rerender, searchParams, localStorage, optimization
---

## 상태 읽기를 사용 시점으로 지연

콜백 내에서만 사용하는 값을 hook으로 구독하면 불필요한 리렌더링. 이벤트 핸들러에서 직접 읽기.

**Incorrect (searchParams 전체 구독):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const searchParams = useSearchParams(); // 모든 파라미터 변경에 리렌더링

  const handleShare = () => {
    const ref = searchParams.get("ref");
    shareChat(chatId, { ref });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

**Correct (이벤트 핸들러에서 직접 읽기):**

```tsx
function ShareButton({ chatId }: { chatId: string }) {
  const handleShare = () => {
    const params = new URLSearchParams(window.location.search);
    const ref = params.get("ref");
    shareChat(chatId, { ref });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

**동일 원칙 - localStorage:**

```tsx
// ❌ 구독 (불필요한 리렌더링)
const theme = useSyncExternalStore(subscribe, () => localStorage.getItem("theme"));
const handleExport = () => exportWithTheme(theme);

// ✅ 이벤트 핸들러에서 직접 읽기
const handleExport = () => {
  const theme = localStorage.getItem("theme");
  exportWithTheme(theme);
};
```

> 원본: [vercel-react-best-practices: rerender-defer-reads](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-defer-reads.md)
