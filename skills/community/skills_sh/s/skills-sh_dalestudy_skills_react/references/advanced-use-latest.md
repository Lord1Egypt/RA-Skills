---
title: useEffectEvent for Stable Callback Refs
impact: LOW
impactDescription: prevents unnecessary effect re-runs
tags: advanced, hooks, useEffectEvent, refs, closures, optimization
---

## useEffectEvent로 안정적 콜백 참조

Effect 내에서 최신 값에 접근하되 의존성 배열에 추가하지 않아 불필요한 Effect 재실행 방지. Stale closure 문제도 해결.

---

### useEffectEvent (React 실험적 API)

**Incorrect (onSearch 변경마다 타이머 재설정):**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const timeout = setTimeout(() => onSearch(query), 300);
    return () => clearTimeout(timeout);
  }, [query, onSearch]); // onSearch 변경마다 재실행
}
```

**Correct (query 변경 시에만 재실행):**

```tsx
import { useEffectEvent } from "react";

function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");
  const onSearchEvent = useEffectEvent(onSearch);

  useEffect(() => {
    const timeout = setTimeout(() => onSearchEvent(query), 300);
    return () => clearTimeout(timeout);
  }, [query]); // onSearch는 의존성에서 제외
}
```

---

### useInsertionEffect 기반 폴리필 (현재 사용 가능)

`useEffectEvent`가 실험적이므로 `useInsertionEffect` 기반으로 직접 구현. DOM 변경 전 동기 실행되어 ref 업데이트 타이밍이 가장 안전.

```tsx
function useEffectEvent<T extends (...args: any[]) => any>(fn: T): T {
  const ref = useRef(fn);

  useInsertionEffect(() => {
    ref.current = fn;
  });

  return useCallback((...args: any[]) => ref.current(...args), []) as T;
}
```

> `useInsertionEffect`는 `useLayoutEffect`보다 먼저 실행. 다른 Effect에서 ref를 읽을 때 항상 최신값이 보장됨.

### useLatest 커스텀 Hook

값만 추적할 때 (함수 반환 불필요):

```tsx
function useLatest<T>(value: T) {
  const ref = useRef(value);
  useInsertionEffect(() => {
    ref.current = value;
  });
  return ref;
}
```

**활용:**

```tsx
function SearchInput({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState("");
  const onSearchRef = useLatest(onSearch);

  useEffect(() => {
    const timeout = setTimeout(() => onSearchRef.current(query), 300);
    return () => clearTimeout(timeout);
  }, [query]);
}
```

---

### 여러 값에 적용

```tsx
function usePolling(url: string, interval: number, onData: (data: unknown) => void) {
  const onDataRef = useLatest(onData);

  useEffect(() => {
    const id = setInterval(async () => {
      const res = await fetch(url);
      const data = await res.json();
      onDataRef.current(data);
    }, interval);
    return () => clearInterval(id);
  }, [url, interval]); // onData 변경 시 폴링 재시작 없음
}
```

---

### useEffectEvent vs useLatest vs 의존성 포함

| 패턴 | 재실행 | Stale closure | 안정성 |
|------|--------|--------------|--------|
| 의존성에 포함 | 콜백 변경마다 | ✅ 없음 | 안정적 |
| `useEffectEvent` | 명시적 의존성만 | ✅ 없음 | 실험적 |
| `useLatest` (ref) | 명시적 의존성만 | ✅ 없음 | 안정적 |
| 의존성 생략 | 초기 1회 | ❌ 발생 | ❌ 버그 |

> `advanced-event-handler-refs`와 동일 원리. 차이점: `event-handler-refs`는 이벤트 리스너 구독에, `use-latest`는 Effect 내부 콜백에 초점.

> 원본: [vercel-react-best-practices: advanced-use-latest](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/advanced-use-latest.md)
