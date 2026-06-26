---
title: Subscribe to Derived State
impact: MEDIUM
impactDescription: reduces re-render frequency
tags: react, hooks, state, derived-state, optimization
---

## 파생 상태 구독

연속 값 대신 파생 boolean을 구독하여 리렌더링 빈도 감소.

**Incorrect (매 픽셀마다 리렌더링):**

```tsx
function Sidebar() {
  const width = useWindowWidth(); // 연속 업데이트
  const isMobile = width < 768;
  return <nav className={isMobile ? "mobile" : "desktop"} />;
}
```

**Correct (boolean 전환 시에만 리렌더링):**

```tsx
function Sidebar() {
  const isMobile = useMediaQuery("(max-width: 767px)");
  return <nav className={isMobile ? "mobile" : "desktop"} />;
}
```

> 원본: [vercel-react-best-practices: rerender-derived-state](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-derived-state.md)
