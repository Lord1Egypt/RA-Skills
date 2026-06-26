---
title: Deduplicate Global Event Listeners
impact: LOW
impactDescription: single listener for N components
tags: client, event-listeners, subscription, deduplication
---

## 글로벌 이벤트 리스너 중복 제거

동일 이벤트를 여러 컴포넌트에서 구독하면 인스턴스 수만큼 리스너가 등록됨. 모듈 레벨에서 단일 리스너를 공유.

---

### 기본 패턴: 모듈 레벨 리스너 공유

**Incorrect (N 인스턴스 = N 리스너):**

```tsx
function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.metaKey && e.key === key) callback();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [key, callback]);
}
```

**Correct (N 인스턴스 = 1 리스너):**

```tsx
const keyCallbacks = new Map<string, Set<() => void>>();
let listenerAttached = false;

function handleKeydown(e: KeyboardEvent) {
  if (e.metaKey && keyCallbacks.has(e.key)) {
    keyCallbacks.get(e.key)!.forEach((cb) => cb());
  }
}

function useKeyboardShortcut(key: string, callback: () => void) {
  useEffect(() => {
    if (!keyCallbacks.has(key)) {
      keyCallbacks.set(key, new Set());
    }
    keyCallbacks.get(key)!.add(callback);

    if (!listenerAttached) {
      window.addEventListener("keydown", handleKeydown);
      listenerAttached = true;
    }

    return () => {
      const set = keyCallbacks.get(key);
      if (set) {
        set.delete(callback);
        if (set.size === 0) keyCallbacks.delete(key);
      }
      if (keyCallbacks.size === 0 && listenerAttached) {
        window.removeEventListener("keydown", handleKeydown);
        listenerAttached = false;
      }
    };
  }, [key, callback]);
}
```

---

### useSyncExternalStore 활용

리스너 중복 제거와 concurrent-safe 구독을 동시에 달성.

```tsx
function makeWindowSizeStore() {
  let size = { width: window.innerWidth, height: window.innerHeight };
  const listeners = new Set<() => void>();

  function handleResize() {
    size = { width: window.innerWidth, height: window.innerHeight };
    listeners.forEach((cb) => cb());
  }

  // 리스너 0 → 1일 때만 등록, 1 → 0일 때 해제
  function subscribe(callback: () => void) {
    if (listeners.size === 0) {
      window.addEventListener("resize", handleResize);
    }
    listeners.add(callback);
    return () => {
      listeners.delete(callback);
      if (listeners.size === 0) {
        window.removeEventListener("resize", handleResize);
      }
    };
  }

  function getSnapshot() {
    return size;
  }

  return { subscribe, getSnapshot };
}

const windowSizeStore = makeWindowSizeStore();

function useWindowSize() {
  return useSyncExternalStore(
    windowSizeStore.subscribe,
    windowSizeStore.getSnapshot,
    () => ({ width: 0, height: 0 }),
  );
}
```

N개 컴포넌트가 `useWindowSize()`를 호출해도 `resize` 리스너는 하나만 등록됨.

> `useSyncExternalStore` 상세는 [`client-sync-external-store`](client-sync-external-store.md) 참고.

> 원본: [vercel-react-best-practices: client-event-listeners](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/client-event-listeners.md)
