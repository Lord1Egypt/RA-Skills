---
title: Use Lazy State Initialization
impact: MEDIUM
impactDescription: wasted computation on every render
tags: react, hooks, useState, initialization, performance
---

## 지연 초기화

비용이 큰 초기값은 함수 형태로 `useState`에 전달. 함수 없이 전달하면 매 렌더링마다 실행.

**Incorrect (매 렌더링마다 실행):**

```tsx
const [searchIndex, setSearchIndex] = useState(buildSearchIndex(items));
const [settings, setSettings] = useState(
  JSON.parse(localStorage.getItem("settings") || "{}"),
);
```

**Correct (최초 1회만 실행):**

```tsx
const [searchIndex, setSearchIndex] = useState(() => buildSearchIndex(items));
const [settings, setSettings] = useState(() => {
  const stored = localStorage.getItem("settings");
  return stored ? JSON.parse(stored) : {};
});
```

**지연 초기화가 필요한 경우:**
- localStorage/sessionStorage 읽기
- 데이터 구조 빌드 (인덱스, Map)
- DOM 읽기
- 무거운 변환 작업

**불필요한 경우:** `useState(0)`, `useState(props.value)`, `useState({})`

> 원본: [vercel-react-best-practices: rerender-lazy-state-init](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-lazy-state-init.md)
