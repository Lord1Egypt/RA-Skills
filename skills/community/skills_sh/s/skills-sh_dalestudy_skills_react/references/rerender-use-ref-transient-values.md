---
title: Use useRef for Transient Values
impact: MEDIUM
impactDescription: avoids unnecessary re-renders on frequent updates
tags: rerender, useRef, state, performance, dom
---

## 일시적 값에 useRef 사용

빈번하게 변경되지만 UI 업데이트가 불필요한 값(마우스 위치, 타이머, 플래그)은 `useRef`로 리렌더링 방지.

**Incorrect (매 mousemove마다 리렌더링):**

```tsx
function Tracker() {
  const [lastX, setLastX] = useState(0);

  useEffect(() => {
    const onMove = (e: MouseEvent) => setLastX(e.clientX);
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, []);

  return (
    <div style={{ position: "fixed", top: 0, left: lastX, width: 8, height: 8, background: "black" }} />
  );
}
```

**Correct (ref + DOM 직접 조작):**

```tsx
function Tracker() {
  const lastXRef = useRef(0);
  const dotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      lastXRef.current = e.clientX;
      if (dotRef.current) {
        dotRef.current.style.transform = `translateX(${e.clientX}px)`;
      }
    };
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, []);

  return (
    <div
      ref={dotRef}
      style={{ position: "fixed", top: 0, left: 0, width: 8, height: 8, background: "black" }}
    />
  );
}
```

UI 업데이트가 필요하면 `useState`, 값만 추적하면 `useRef`.

> 원본: [vercel-react-best-practices: rerender-use-ref-transient-values](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-use-ref-transient-values.md)
