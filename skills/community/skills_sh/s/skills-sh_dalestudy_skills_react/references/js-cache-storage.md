---
title: Cache Storage API Calls
impact: LOW-MEDIUM
impactDescription: reduces expensive synchronous I/O
tags: javascript, localStorage, storage, caching, performance
---

## Storage API 호출 캐싱

`localStorage`, `sessionStorage`, `document.cookie`는 동기적이고 비용이 큼. 메모리에 캐싱.

**Incorrect (호출마다 스토리지 읽기):**

```tsx
function getTheme() {
  return localStorage.getItem("theme") ?? "light";
}
// 10회 호출 = 10회 스토리지 읽기
```

**Correct (Map 캐시):**

```tsx
const storageCache = new Map<string, string | null>();

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key));
  }
  return storageCache.get(key);
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value);
  storageCache.set(key, value);
}
```

**외부 변경 시 캐시 무효화:**

```tsx
window.addEventListener("storage", (e) => {
  if (e.key) storageCache.delete(e.key);
});

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    storageCache.clear();
  }
});
```

> [`client-localstorage-schema`](client-localstorage-schema.md)는 스키마 버전 관리, 이 규칙은 읽기 성능 최적화.

> 원본: [vercel-react-best-practices: js-cache-storage](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-cache-storage.md)
