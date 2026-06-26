---
title: useTransition Over Manual Loading States
impact: LOW
impactDescription: reduces re-renders and improves code clarity
tags: rendering, transitions, useTransition, loading, state
---

## useTransition으로 수동 로딩 상태 대체

`useState`로 `isLoading`을 수동 관리하지 않고 `useTransition`의 `isPending` 사용.

**Incorrect (수동 로딩 상태):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (value: string) => {
    setIsLoading(true);
    setQuery(value);
    const data = await fetchResults(value);
    setResults(data);
    setIsLoading(false);
  };

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isLoading && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}
```

**Correct (useTransition):**

```tsx
function SearchResults() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleSearch = (value: string) => {
    setQuery(value); // 즉시 업데이트

    startTransition(async () => {
      const data = await fetchResults(value);
      setResults(data);
    });
  };

  return (
    <>
      <input onChange={(e) => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <ResultsList results={results} />
    </>
  );
}
```

장점:
- 에러 발생 시에도 pending 상태 자동 리셋
- 새 transition이 이전 pending을 자동 취소
- UI 반응성 유지

> [`rerender-transitions`](rerender-transitions.md)는 startTransition의 일반적 사용, 이 규칙은 로딩 상태 관리에 특화.

> 원본: [vercel-react-best-practices: rendering-usetransition-loading](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-usetransition-loading.md)
