---
title: Early Length Check for Array Comparisons
impact: MEDIUM-HIGH
impactDescription: avoids expensive operations when lengths differ
tags: javascript, arrays, performance, comparison
---

## 배열 비교 시 길이 먼저 확인

비용 큰 비교(정렬, 깊은 동등성) 전에 O(1) 길이 확인으로 조기 반환.

**Incorrect (항상 정렬 + 조인):**

```tsx
function hasChanges(current: string[], original: string[]) {
  return current.sort().join() !== original.sort().join();
}
```

**Correct (길이 다르면 즉시 반환):**

```tsx
function hasChanges(current: string[], original: string[]) {
  if (current.length !== original.length) return true;

  const currentSorted = current.toSorted();
  const originalSorted = original.toSorted();
  return currentSorted.some((val, i) => val !== originalSorted[i]);
}
```

> 원본: [vercel-react-best-practices: js-length-check-first](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-length-check-first.md)
