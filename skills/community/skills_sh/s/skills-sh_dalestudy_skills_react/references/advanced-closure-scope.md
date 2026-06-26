---
title: Isolate Closure Scopes to Prevent Memory Leaks
impact: LOW
impactDescription: prevents hidden memory retention from closure chains
tags: advanced, closure, memory, useCallback, useRef, scope, garbage-collection
---

## 클로저 스코프 격리로 메모리 누수 방지

`useCallback` 등 메모이제이션 훅은 클로저 스코프 전체를 캡처. 큰 컴포넌트에서 의도치 않은 메모리 유지 발생.

**Incorrect (큰 스코프를 캡처하는 콜백):**

```tsx
function Dashboard() {
  const [count, setCount] = useState(0);
  const chartData = useMemo(() => generateChartData(), []); // 10MB

  const handleClick = useCallback(() => {
    setCount((c) => c + 1);
  }, []);
  // ❌ handleClick의 클로저가 chartData를 포함한 전체 스코프 참조
  // chartData가 필요 없어도 GC 불가

  return (
    <>
      <Chart data={chartData} />
      <ExpensiveChild onClick={handleClick} />
    </>
  );
}
```

**Correct (커스텀 훅으로 스코프 분리):**

```tsx
function useCounter(initial: number) {
  const [count, setCount] = useState(initial);
  const increment = useCallback(() => setCount((c) => c + 1), []);
  return { count, increment };
}

function Dashboard() {
  const { count, increment } = useCounter(0);
  const chartData = useMemo(() => generateChartData(), []);

  // ✅ increment의 클로저는 useCounter 내부 스코프만 캡처
  // chartData와 무관

  return (
    <>
      <Chart data={chartData} />
      <ExpensiveChild onClick={increment} />
    </>
  );
}
```

---

### 교차 참조 체인 문제

같은 컴포넌트의 여러 `useCallback`이 서로의 이전 버전을 참조하면서 GC 불가능한 체인 형성:

```tsx
function App() {
  const [countA, setCountA] = useState(0);
  const [countB, setCountB] = useState(0);
  const bigData = new Uint8Array(10_000_000); // 10MB

  // countA 변경 → handleA 재생성 → 이전 handleA는 이전 handleB 참조
  // countB 변경 → handleB 재생성 → 이전 handleB는 이전 handleA 참조
  // ❌ 교대로 업데이트되면 이전 클로저들이 체인으로 연결되어 GC 불가
  const handleA = useCallback(() => setCountA((a) => a + 1), [countA]);
  const handleB = useCallback(() => setCountB((b) => b + 1), [countB]);

  return (
    <>
      <ChildA onClick={handleA} />
      <ChildB onClick={handleB} />
    </>
  );
}
```

**Correct (독립 훅으로 분리):**

```tsx
function useCounterA() {
  const [count, setCount] = useState(0);
  const increment = useCallback(() => setCount((c) => c + 1), []);
  return { count, increment };
}

function useCounterB() {
  const [count, setCount] = useState(0);
  const increment = useCallback(() => setCount((c) => c + 1), []);
  return { count, increment };
}

function App() {
  const { count: countA, increment: incA } = useCounterA();
  const { count: countB, increment: incB } = useCounterB();
  // ✅ 각 훅의 클로저가 독립적 → 교차 참조 없음

  return (
    <>
      <ChildA onClick={incA} />
      <ChildB onClick={incB} />
    </>
  );
}
```

---

### useRef로 큰 객체 참조 관리

큰 객체를 ref에 저장하면 클로저가 ref 객체만 캡처 (값 자체는 `.current`로 간접 접근):

```tsx
function ImageProcessor() {
  const imageDataRef = useRef<Uint8Array | null>(
    new Uint8Array(10_000_000),
  );

  const processImage = useCallback(() => {
    if (!imageDataRef.current) return;
    // ref.current를 통해 접근 → 클로저가 값 자체를 캡처하지 않음
    transform(imageDataRef.current);
  }, []);

  useEffect(() => {
    return () => {
      imageDataRef.current = null; // 언마운트 시 해제
    };
  }, []);

  return <button onClick={processImage}>Process</button>;
}
```

---

### 판단 기준

| 상황 | 대응 |
|------|------|
| 컴포넌트에 `useCallback` 2개 이상 + 큰 데이터 | 커스텀 훅으로 스코프 분리 |
| 큰 객체가 콜백에서 사용됨 | `useRef`로 간접 참조 |
| `useCallback` 의존성이 자주 변경 | 함수형 setState `(prev) => ...` 사용 |
| 단순 핸들러, memo된 자식 없음 | `useCallback` 사용하지 않기 |

> React Compiler를 사용하면 메모이제이션이 자동으로 최적화되어 이 문제의 대부분이 완화됨.

> 원본: [schiener.io - React, Pair-wise Closures & Memory Leaks](https://www.schiener.io/2024-03-03/react-closures)
