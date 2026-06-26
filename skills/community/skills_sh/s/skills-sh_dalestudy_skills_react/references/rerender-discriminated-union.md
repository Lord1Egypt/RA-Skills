---
title: Prevent Impossible States with Discriminated Unions
impact: MEDIUM
impactDescription: eliminates invalid state combinations at type level
tags: react, useState, typescript, discriminated-union, state-machine
---

## Discriminated Union으로 불가능한 상태 방지

여러 boolean 대신 하나의 상태 문자열로 불가능한 상태 조합을 원천 차단.

**Incorrect (불가능한 상태 가능):**

```tsx
const [isLoading, setIsLoading] = useState(false);
const [isError, setIsError] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
// ❌ isLoading && isError && isSuccess 동시 true 가능
```

**Correct (하나의 상태 문자열):**

```tsx
type Status = "idle" | "loading" | "success" | "error";
const [status, setStatus] = useState<Status>("idle");
```

---

### TypeScript Discriminated Union

각 상태에 따라 다른 데이터를 타입 안전하게 접근.

```tsx
type State =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: Data }
  | { status: "error"; error: Error };

const [state, setState] = useState<State>({ status: "idle" });

// 타입 안전한 분기
if (state.status === "success") {
  console.log(state.data); // ✅ data 접근 가능
}
if (state.status === "error") {
  console.log(state.error); // ✅ error 접근 가능
}
```

---

### 실제 활용: 비동기 요청

```tsx
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function useAsync<T>(asyncFn: () => Promise<T>) {
  const [state, setState] = useState<AsyncState<T>>({ status: "idle" });

  const execute = useCallback(async () => {
    setState({ status: "loading" });
    try {
      const data = await asyncFn();
      setState({ status: "success", data });
    } catch (error) {
      setState({ status: "error", error: error as Error });
    }
  }, [asyncFn]);

  return { ...state, execute };
}
```

> 복잡한 상태 전이가 필요하면 [`rerender-use-reducer`](rerender-use-reducer.md) 참고.

> 원본: [David Khourshid - Goodbye, useState (BeJS Conference)](https://www.youtube.com/watch?v=aGkscOKWQvQ)
