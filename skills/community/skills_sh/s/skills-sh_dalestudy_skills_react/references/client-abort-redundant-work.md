---
title: Abort Redundant Async Work
impact: MEDIUM
impactDescription: prevents stale updates and wasted computation
tags: client, AbortController, abort, cancel, async, performance, fetch
---

## AbortController로 불필요한 비동기 작업 취소

사용자 입력이 빠르게 변할 때 이전 작업을 취소하여 stale 업데이트와 불필요한 연산 방지.

**Incorrect (이전 작업이 계속 실행):**

```tsx
function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Item[]>([]);

  useEffect(() => {
    fetchResults(query).then(setResults);
    // ❌ 이전 요청이 취소되지 않음 → 느린 요청이 빠른 요청을 덮어씀
  }, [query]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

**Correct (AbortController로 이전 요청 취소):**

```tsx
function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Item[]>([]);

  useEffect(() => {
    const controller = new AbortController();

    fetchResults(query, { signal: controller.signal })
      .then(setResults)
      .catch((err) => {
        if (err.name !== "AbortError") throw err;
      });

    return () => controller.abort();
  }, [query]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

---

### 이벤트 핸들러에서 AbortController 사용

```tsx
function SearchForm() {
  const controllerRef = useRef<AbortController | null>(null);
  const [results, setResults] = useState<Item[]>([]);

  async function handleSearch(query: string) {
    // 이전 요청 취소
    controllerRef.current?.abort();
    controllerRef.current = new AbortController();

    try {
      const data = await fetchResults(query, {
        signal: controllerRef.current.signal,
      });
      setResults(data);
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return;
      throw err;
    }
  }

  // 컴포넌트 언마운트 시 정리
  useEffect(() => {
    return () => controllerRef.current?.abort();
  }, []);

  return <input onChange={(e) => handleSearch(e.target.value)} />;
}
```

---

### 비용 큰 계산 취소

`fetch`뿐 아니라 CPU 집약적 작업도 signal로 취소 가능:

```tsx
function filterLargeDataset(
  items: Item[],
  query: string,
  signal: AbortSignal,
): Item[] {
  const results: Item[] = [];

  for (const item of items) {
    if (signal.aborted) return results; // 조기 종료
    if (item.name.toLowerCase().includes(query.toLowerCase())) {
      results.push(item);
    }
  }

  return results;
}

// 사용
const controller = new AbortController();
const filtered = filterLargeDataset(items, query, controller.signal);
```

---

### cleanup 패턴 비교

| 패턴 | 취소 대상 | 적합한 경우 |
|------|----------|------------|
| `useEffect` return + AbortController | fetch, 타이머, 비동기 작업 | Effect 내 비동기 작업 |
| `useRef` + AbortController | 이벤트 핸들러 비동기 작업 | 빠른 연속 입력 (검색, 자동완성) |
| `useDeferredValue` | 리렌더링 | 렌더링 단계의 무거운 계산 |
| `startTransition` | 상태 업데이트 | 낮은 우선순위 업데이트 |

> `useDeferredValue`/`startTransition`은 렌더링 수준의 취소. `AbortController`는 네트워크/계산 수준의 취소. 함께 사용하면 효과적.

> 원본: [kurtextrem - Improve INP in React](https://kurtextrem.de/posts/improve-inp-react)
