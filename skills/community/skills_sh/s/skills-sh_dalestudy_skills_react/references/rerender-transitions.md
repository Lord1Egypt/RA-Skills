---
title: Use Transitions for Non-Urgent Updates
impact: MEDIUM
impactDescription: maintains UI responsiveness
tags: react, transitions, startTransition, useDeferredValue, useTransition, concurrent, performance
---

## Transition으로 UI 반응성 유지

긴급하지 않은 상태 업데이트를 낮은 우선순위로 처리하여 입력, 클릭 등 긴급한 업데이트가 블로킹되지 않도록 함.

---

### startTransition

상태 업데이트를 직접 제어할 수 있을 때 사용.

**Incorrect (매 스크롤마다 UI 블로킹):**

```tsx
function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);
}
```

**Correct (논블로킹 업데이트):**

```tsx
import { startTransition } from "react";

function ScrollTracker() {
  const [scrollY, setScrollY] = useState(0);
  useEffect(() => {
    const handler = () => {
      startTransition(() => setScrollY(window.scrollY));
    };
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);
}
```

---

### useDeferredValue

상태 업데이트를 직접 제어할 수 없을 때(props로 받은 값, 외부 라이브러리) 사용. 값의 "지연된 복사본"을 생성.

**검색 입력 + 무거운 목록:**

```tsx
function SearchPage() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  return (
    <>
      {/* 입력은 즉시 반영 */}
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      {/* 목록은 지연된 값으로 렌더링 → 입력이 끊기지 않음 */}
      <SearchResults query={deferredQuery} />
    </>
  );
}

const SearchResults = memo(function SearchResults({ query }: { query: string }) {
  const filteredItems = items.filter((item) =>
    item.name.toLowerCase().includes(query.toLowerCase()),
  );
  return (
    <ul>
      {filteredItems.map((item) => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});
```

> `memo`와 함께 사용해야 효과적. `deferredQuery`가 이전 값과 같으면 `SearchResults` 리렌더링을 건너뜀.

**지연 상태 시각적 피드백:**

```tsx
function SearchPage() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.5 : 1, transition: "opacity 0.2s" }}>
        <SearchResults query={deferredQuery} />
      </div>
    </>
  );
}
```

---

### Suspense와 useDeferredValue

새 데이터 로딩 중 이전 결과를 유지하면서 fallback 표시를 방지.

```tsx
function ProfilePage({ userId }: { userId: string }) {
  const deferredId = useDeferredValue(userId);

  return (
    <Suspense fallback={<Skeleton />}>
      {/* userId 변경 시 이전 프로필을 유지하면서 새 데이터 로드 */}
      <ProfileDetails userId={deferredId} />
    </Suspense>
  );
}
```

`useDeferredValue` 없이 userId가 변경되면 Suspense fallback이 즉시 표시됨. `useDeferredValue`를 사용하면 이전 결과를 보여주다가 새 데이터가 준비되면 전환.

---

### startTransition vs useDeferredValue vs useTransition

| 훅 | 사용 시점 | pending 상태 |
|----|----------|-------------|
| `startTransition` | setState를 직접 호출할 수 있을 때 | ❌ |
| `useTransition` | setState + pending 표시가 필요할 때 | ✅ `isPending` |
| `useDeferredValue` | props/외부 값을 지연시킬 때 | `value !== deferredValue` |

```tsx
// startTransition: 상태 업데이트를 직접 감싸기
startTransition(() => setQuery(value));

// useTransition: pending 상태 필요
const [isPending, startTransition] = useTransition();
startTransition(() => setQuery(value));

// useDeferredValue: props로 받은 값 지연
const deferredQuery = useDeferredValue(query);
```

> `useTransition`으로 수동 로딩 상태를 대체하는 패턴은 [`rendering-usetransition-loading`](rendering-usetransition-loading.md) 참고.

> 원본: [vercel-react-best-practices: rerender-transitions](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-transitions.md)
