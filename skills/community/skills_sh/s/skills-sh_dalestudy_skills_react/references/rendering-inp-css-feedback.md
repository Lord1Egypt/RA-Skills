---
title: Use CSS for Immediate Visual Feedback
impact: MEDIUM
impactDescription: improves INP by avoiding JS for visual responses
tags: rendering, INP, CSS, active, yield, performance, interaction
---

## CSS로 즉각적인 시각 피드백 제공

버튼 클릭 시 JS 이벤트 핸들러 대신 CSS `:active`로 즉시 시각 피드백. JS 핸들러는 yield 후 실행.

**Incorrect (JS로 시각 피드백 → 페인트 지연):**

```tsx
function ActionButton({ onClick }: { onClick: () => void }) {
  const [pressed, setPressed] = useState(false);

  return (
    <button
      style={{ boxShadow: pressed ? "2px 2px 5px #fc894d" : "none" }}
      onPointerDown={() => setPressed(true)}
      onPointerUp={() => setPressed(false)}
      onClick={onClick}
    >
      Click me
    </button>
  );
}
// ❌ pointerdown → setState → 리렌더 → 페인트 지연
```

**Correct (CSS :active + yield):**

```css
.action-btn:active {
  box-shadow: 2px 2px 5px #fc894d;
}
```

```tsx
function ActionButton({ onClick }: { onClick: () => void }) {
  return (
    <button
      className="action-btn"
      onClick={async () => {
        // 브라우저가 먼저 페인트하도록 양보
        await yieldToMain();
        onClick();
      }}
    >
      Click me
    </button>
  );
}
```

---

### yieldToMain 구현

브라우저가 페인트를 완료한 후 JS를 재개하도록 양보하는 유틸리티.

**`scheduler.yield()` 사용 (최신 브라우저):**

```tsx
async function yieldToMain() {
  if ("scheduler" in globalThis && "yield" in scheduler) {
    return scheduler.yield();
  }
  // 폴백: setTimeout(0)
  return new Promise((resolve) => setTimeout(resolve, 0));
}
```

**`requestAnimationFrame` + `setTimeout` 폴백:**

```tsx
function yieldToMain(): Promise<void> {
  return new Promise((resolve) => {
    requestAnimationFrame(() => {
      setTimeout(resolve, 0);
    });
  });
}
```

---

### 이벤트 체인 문제

`pointerdown` → `pointerup` → `click` 순서로 이벤트가 발생. 각 이벤트에 JS 핸들러가 있으면 모두 메인 스레드를 차지.

```tsx
// ❌ 3개 이벤트 모두 JS 실행
<button
  onPointerDown={() => setActive(true)}
  onPointerUp={() => setActive(false)}
  onClick={handleExpensiveWork}
>

// ✅ CSS가 시각 피드백 처리, JS는 click만
<button
  className="action-btn"
  onClick={handleExpensiveWork}
>
```

---

### useAfterPaintEffect: 페인트 후 Effect 실행

`useEffect`/`useLayoutEffect`는 사용자 인터랙션 응답 시 페인트 전에 실행될 수 있음. 페인트 후 실행을 보장하는 패턴:

```tsx
function useAfterPaintEffect(
  effect: () => void | (() => void),
  deps: DependencyList,
) {
  useLayoutEffect(() => {
    let cleanup: void | (() => void);

    requestAnimationFrame(() => {
      setTimeout(() => {
        cleanup = effect();
      }, 0);
    });

    return () => {
      if (typeof cleanup === "function") cleanup();
    };
  }, deps);
}

// 사용: 분석 전송, 로깅 등 시각 피드백과 무관한 작업
useAfterPaintEffect(() => {
  sendAnalytics("button_clicked");
}, []);
```

> `useLayoutEffect` → `requestAnimationFrame` → `setTimeout` 순서로 페인트 후 실행 보장.

---

### 패턴 선택 기준

| 상황 | 패턴 |
|------|------|
| 버튼/링크 시각 피드백 | CSS `:active`, `:hover` |
| 클릭 후 무거운 작업 | `await yieldToMain()` + 작업 |
| Effect에서 비시각 작업 | `useAfterPaintEffect` |
| 스크롤/리사이즈 핸들러 | `passive: true` + `startTransition` |

> 원본: [kurtextrem - Improve INP in React](https://kurtextrem.de/posts/improve-inp-react)
