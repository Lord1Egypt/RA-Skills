---
title: Simplify useEffect with Custom Hooks
impact: MEDIUM
impactDescription: reduces bugs from complex effects and improves testability
tags: react, useEffect, custom-hooks, single-responsibility, refactoring
---

## useEffect를 커스텀 훅으로 단순화

하나의 Effect에 여러 관심사를 넣지 않기. 단일 책임으로 분리하고 커스텀 훅으로 추출.

---

### 1. Effect 분리: 단일 책임 원칙

**Incorrect (하나의 Effect에 여러 관심사):**

```tsx
function Page({ title }: { title: string }) {
  useEffect(() => {
    document.title = title;
    trackPageVisit(); // ❌ title 변경마다 페이지 방문 추적
  }, [title]);
}
```

**Correct (관심사별 분리):**

```tsx
function Page({ title }: { title: string }) {
  useEffect(() => {
    document.title = title;
  }, [title]);

  useEffect(() => {
    trackPageVisit();
  }, []);
}
```

---

### 2. 커스텀 훅으로 추출

Effect + 관련 상태를 커스텀 훅으로 캡슐화. 컴포넌트는 **의도**만 표현.

**Before (컴포넌트에 Effect 로직 직접 작성):**

```tsx
function Profile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchUser(userId, { signal: controller.signal })
      .then(setUser)
      .catch(setError);
    return () => controller.abort();
  }, [userId]);

  if (error) return <ErrorMessage error={error} />;
  if (!user) return <Skeleton />;
  return <UserCard user={user} />;
}
```

**After (커스텀 훅 추출):**

```tsx
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetchUser(userId, { signal: controller.signal })
      .then(setUser)
      .catch(setError);
    return () => controller.abort();
  }, [userId]);

  return { user, error };
}

function Profile({ userId }: { userId: string }) {
  const { user, error } = useUser(userId);

  if (error) return <ErrorMessage error={error} />;
  if (!user) return <Skeleton />;
  return <UserCard user={user} />;
}
```

> 커스텀 훅은 독립적으로 테스트 가능. 데이터 페칭은 TanStack Query/SWR 사용 권장 ([`client-data-dedup`](client-data-dedup.md) 참고).

---

### 3. Effect에 이름 붙이기

익명 함수 대신 이름이 있는 함수를 사용하면 의도가 명확해짐:

```tsx
// ❌ 익명: 무엇을 하는지 Effect 내부를 읽어야 앎
useEffect(() => {
  document.title = title;
}, [title]);

// ✅ 명명: 이름만으로 의도 파악
useEffect(function syncDocumentTitle() {
  document.title = title;
}, [title]);
```

---

### 4. Effect가 필요 없는 경우

| 상황 | Effect 대신 사용할 것 |
|------|---------------------|
| props/state에서 파생된 값 | 렌더링 중 계산 또는 `useMemo` ([`rerender-derived-state-no-effect`](rerender-derived-state-no-effect.md)) |
| 사용자 이벤트 응답 | 이벤트 핸들러 ([`rerender-move-effect-to-event`](rerender-move-effect-to-event.md)) |
| 앱 초기화 (1회) | 모듈 레벨 또는 `useRef` 가드 ([`advanced-init-once`](advanced-init-once.md)) |
| 데이터 페칭 | TanStack Query / SWR ([`client-data-dedup`](client-data-dedup.md)) |

---

### 5. 의존성 정직하게 선언

```tsx
// ❌ 의존성 누락 → stale closure
useEffect(() => {
  fetchData(userId);
}, []);

// ✅ 모든 의존성 포함
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

의존성이 너무 많아지면 Effect가 너무 많은 일을 하고 있다는 신호. 분리하거나 커스텀 훅으로 추출.

> 원본: [TkDodo - Simplifying useEffect](https://tkdodo.eu/blog/simplifying-use-effect)
