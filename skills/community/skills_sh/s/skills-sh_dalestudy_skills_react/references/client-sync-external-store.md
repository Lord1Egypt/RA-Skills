---
title: useSyncExternalStore for External State
impact: MEDIUM
impactDescription: prevents tearing in concurrent rendering, replaces useEffect+useState for external sources
tags: react, useSyncExternalStore, browser-api, external-store, ssr, concurrent
---

## useSyncExternalStore로 외부 상태 구독

브라우저 API나 외부 스토어 구독 시 `useEffect` + `useState` 대신 `useSyncExternalStore` 사용. Concurrent 렌더링에서 데이터 불일치(tearing) 방지.

```tsx
const state = useSyncExternalStore(
  subscribe,        // (callback) => unsubscribe
  getSnapshot,      // () => 현재 값 (동기, 순수)
  getServerSnapshot // () => SSR 초기값 (선택, SSR 시 필수)
);
```

---

### 온라인 상태 감지

**Incorrect (useEffect + useState):**

```tsx
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOnline;
}
```

**Correct (useSyncExternalStore):**

```tsx
function subscribe(callback: () => void) {
  window.addEventListener("online", callback);
  window.addEventListener("offline", callback);
  return () => {
    window.removeEventListener("online", callback);
    window.removeEventListener("offline", callback);
  };
}

function getSnapshot() {
  return navigator.onLine;
}

function useOnlineStatus() {
  return useSyncExternalStore(subscribe, getSnapshot, () => true);
}
```

`subscribe`와 `getSnapshot`을 컴포넌트 외부에 정의. 리렌더링마다 함수가 재생성되면 무한 루프 발생.

---

### 미디어 쿼리 (팩토리 패턴)

```tsx
function makeMediaQueryStore(query: string) {
  function subscribe(callback: () => void) {
    const mql = window.matchMedia(query);
    mql.addEventListener("change", callback);
    return () => mql.removeEventListener("change", callback);
  }

  function getSnapshot() {
    return window.matchMedia(query).matches;
  }

  return function useMediaQuery() {
    return useSyncExternalStore(subscribe, getSnapshot, () => false);
  };
}

const useIsMobile = makeMediaQueryStore("(max-width: 767px)");
const usePrefersDark = makeMediaQueryStore("(prefers-color-scheme: dark)");
```

---

### localStorage 동기화

```tsx
function makeLocalStorageStore(key: string) {
  function subscribe(callback: () => void) {
    // 다른 탭에서 변경 시 동기화
    const handleStorage = (e: StorageEvent) => {
      if (e.key === key) callback();
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }

  function getSnapshot() {
    return localStorage.getItem(key);
  }

  return {
    useStore() {
      return useSyncExternalStore(subscribe, getSnapshot, () => null);
    },
    set(value: string) {
      localStorage.setItem(key, value);
      // 같은 탭에서는 storage 이벤트 미발생 → 수동 dispatch
      window.dispatchEvent(new StorageEvent("storage", { key }));
    },
  };
}

const themeStore = makeLocalStorageStore("theme");

function ThemeSwitcher() {
  const theme = themeStore.useStore();
  return (
    <button onClick={() => themeStore.set(theme === "dark" ? "light" : "dark")}>
      {theme ?? "system"}
    </button>
  );
}
```

---

### 스크롤 위치

```tsx
function subscribe(callback: () => void) {
  window.addEventListener("scroll", callback, { passive: true });
  return () => window.removeEventListener("scroll", callback);
}

function getSnapshot() {
  return Math.round(window.scrollY);
}

function useScrollY() {
  return useSyncExternalStore(subscribe, getSnapshot, () => 0);
}
```

---

### 주의사항

**함수를 컴포넌트 외부에 정의:**

```tsx
// ❌ 매 렌더링마다 재생성 → 무한 구독/해제
function Component() {
  const value = useSyncExternalStore(
    (cb) => { window.addEventListener("resize", cb); return () => window.removeEventListener("resize", cb); },
    () => window.innerWidth,
  );
}

// ✅ 외부 정의 또는 useCallback
function subscribe(callback: () => void) {
  window.addEventListener("resize", callback);
  return () => window.removeEventListener("resize", callback);
}

function getSnapshot() {
  return window.innerWidth;
}

function Component() {
  const width = useSyncExternalStore(subscribe, getSnapshot, () => 0);
}
```

**getSnapshot이 매번 새 참조를 반환하면 안 됨:**

```tsx
// ❌ 매번 새 객체 → 무한 리렌더링
function getSnapshot() {
  return { ...store.getData() };
}

// ✅ 스토어에서 같은 참조 반환
function getSnapshot() {
  return store.getData();
}
```

**SSR 시 `getServerSnapshot` 필수:**

브라우저 전용 API(`window`, `navigator`, `localStorage`)는 서버에서 접근 불가. 적절한 기본값 반환.

---

### 사용하지 않는 경우

- React 상태 (`useState`, `useReducer`, Context) → 이미 concurrent-safe
- Zustand, Redux, Jotai → 내부적으로 `useSyncExternalStore` 사용
- 서버 데이터 → TanStack Query, SWR 등 데이터 페칭 라이브러리

> 원본: [Epic React: useSyncExternalStore Demystified](https://www.epicreact.dev/use-sync-external-store-demystified-for-practical-react-development-w5ac0)
