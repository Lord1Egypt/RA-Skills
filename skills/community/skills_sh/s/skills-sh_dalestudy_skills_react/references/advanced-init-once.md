---
title: Initialize App Once, Not Per Mount
impact: LOW-MEDIUM
impactDescription: avoids duplicate init in development
tags: advanced, initialization, useEffect, side-effects
---

## 앱 초기화는 컴포넌트가 아닌 모듈 레벨에서

`useEffect([], ...)`에 앱 전체 초기화를 넣으면 개발 모드에서 2번, 리마운트 시 재실행됨. 모듈 레벨 가드 사용.

**Incorrect (리마운트 시 재실행):**

```tsx
function App() {
  useEffect(() => {
    loadFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

**Correct (앱 로드 시 1회만):**

```tsx
let didInit = false;

function App() {
  useEffect(() => {
    if (didInit) return;
    didInit = true;
    loadFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

**useRef로 컴포넌트 내부에서 1회 실행:**

```tsx
function App() {
  const initialized = useRef(false);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;
    loadFromStorage();
    checkAuthToken();
  }, []);
  // ...
}
```

> 모듈 변수(`let didInit`)와 달리 `useRef`는 컴포넌트 인스턴스에 귀속. 단, 앱 루트 컴포넌트는 하나이므로 동작은 동일.

**또는 모듈 최상위에서 직접 실행:**

```tsx
// app-init.ts
if (typeof window !== "undefined") {
  loadFromStorage();
  checkAuthToken();
}
```

---

### 방식 비교

| 방식 | 스코프 | Strict Mode 안전 | 클린업 가능 |
|------|--------|-----------------|------------|
| 모듈 변수 `let didInit` | 모듈 전체 | ✅ | ❌ |
| `useRef` | 컴포넌트 인스턴스 | ✅ | ✅ (`useEffect` return) |
| 모듈 최상위 실행 | 모듈 전체 | ✅ | ❌ |
| `useEffect([], ...)` (가드 없음) | 컴포넌트 | ❌ (2번 실행) | ✅ |

> 참고: [React 공식 문서 - Initializing the application](https://react.dev/learn/you-might-not-need-an-effect#initializing-the-application)

> 원본: [vercel-react-best-practices: advanced-init-once](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/advanced-init-once.md)
