---
title: Ref Callbacks for DOM Access
impact: MEDIUM
impactDescription: eliminates unnecessary useRef + useEffect pairs
tags: react, ref, callback, DOM, useEffect, cleanup, react-19
---

## Ref Callback으로 DOM 접근

DOM 노드 접근 시 `useRef` + `useEffect` 대신 ref callback 사용. 의도가 명확하고, 불필요한 Effect를 줄임.

---

### 기본 패턴: 컴포넌트 외부 함수

**Incorrect (useRef + useEffect):**

```tsx
function ChatMessages() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  return <div ref={ref}>...</div>;
}
```

**Correct (ref callback):**

```tsx
function scrollIntoView(node: HTMLDivElement | null) {
  node?.scrollIntoView({ behavior: "smooth" });
}

function ChatMessages() {
  return <div ref={scrollIntoView}>...</div>;
}
```

함수를 컴포넌트 외부에 정의하면 리렌더링 시 재생성되지 않음. `useCallback` 불필요.

---

### DOM 측정값으로 상태 업데이트

```tsx
function MeasureExample() {
  const [height, setHeight] = useState(0);

  return (
    <>
      <h1
        ref={(node) => {
          if (node !== null) {
            setHeight(node.getBoundingClientRect().height);
          }
        }}
      >
        Hello, world
      </h1>
      <h2>The above header is {Math.round(height)}px tall</h2>
    </>
  );
}
```

`useState`는 동일 원시값 전달 시 리렌더링을 건너뜀.

---

### React 19: Cleanup 함수

React 19에서 ref callback이 cleanup 함수를 반환 가능. 언마운트 시 자동 호출.

**Incorrect (useRef + useEffect로 ResizeObserver):**

```tsx
function MeasureExample() {
  const ref = useRef<HTMLHeadingElement>(null);
  const [height, setHeight] = useState(0);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new ResizeObserver(([entry]) => {
      setHeight(entry.contentRect.height);
    });
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <>
      <h1 ref={ref}>Hello, world</h1>
      <h2>The above header is {Math.round(height)}px tall</h2>
    </>
  );
}
```

**Correct (ref callback + cleanup):**

```tsx
function MeasureExample() {
  const [height, setHeight] = useState(0);

  return (
    <>
      <h1
        ref={(node) => {
          const observer = new ResizeObserver(([entry]) => {
            setHeight(entry.contentRect.height);
          });
          observer.observe(node);
          return () => observer.disconnect();
        }}
      >
        Hello, world
      </h1>
      <h2>The above header is {Math.round(height)}px tall</h2>
    </>
  );
}
```

`useRef` 없이 observer 설정과 해제가 한 곳에. `getBoundingClientRect()`와 달리 레이아웃 스래싱(layout thrashing) 없음.

---

### Ref Callback vs useEffect 판단 기준

| 상황 | 사용 |
|------|------|
| DOM 노드 접근 (스크롤, 포커스, 측정) | ref callback |
| Observer 등록/해제 (React 19+) | ref callback + cleanup |
| 노드와 무관한 사이드 이펙트 (document.title 등) | useEffect |
| 비동기 데이터 페칭 | 데이터 페칭 라이브러리 |

---

### useCallback 감싸지 않기

```tsx
// ❌ useCallback으로 감싸면 의미가 불분명해짐
const ref = useCallback((node: HTMLDivElement | null) => {
  node?.scrollIntoView({ behavior: "smooth" });
}, []);

// ✅ 컴포넌트 외부에 함수 정의
function scrollIntoView(node: HTMLDivElement | null) {
  node?.scrollIntoView({ behavior: "smooth" });
}
```

`useCallback`은 성능 최적화 용도. 제거해도 코드가 동작해야 함. React Compiler 사용 시 `useCallback` 자동 처리되므로 수동 적용 불필요.

> 원본: [TkDodo: Ref Callbacks, React 19 and the Compiler](https://tkdodo.eu/blog/ref-callbacks-react-19-and-the-compiler)
