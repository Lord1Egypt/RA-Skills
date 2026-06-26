---
title: Use Loop for Min/Max Instead of Sort
impact: LOW
impactDescription: O(n) instead of O(n log n)
tags: javascript, arrays, performance, algorithms
---

## 최솟값/최댓값은 정렬 대신 단일 루프

최솟값/최댓값만 필요하면 정렬(O(n log n))은 낭비. 단일 순회(O(n))로 충분.

**Incorrect (전체 정렬):**

```tsx
function getLatestProject(projects: Project[]) {
  const sorted = [...projects].sort((a, b) => b.updatedAt - a.updatedAt);
  return sorted[0];
}
```

**Correct (단일 루프):**

```tsx
function getLatestProject(projects: Project[]) {
  if (projects.length === 0) return null;

  let latest = projects[0];
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt > latest.updatedAt) {
      latest = projects[i];
    }
  }
  return latest;
}
```

**최솟값과 최댓값 동시:**

```tsx
function getOldestAndNewest(projects: Project[]) {
  if (projects.length === 0) return { oldest: null, newest: null };

  let oldest = projects[0];
  let newest = projects[0];
  for (let i = 1; i < projects.length; i++) {
    if (projects[i].updatedAt < oldest.updatedAt) oldest = projects[i];
    if (projects[i].updatedAt > newest.updatedAt) newest = projects[i];
  }
  return { oldest, newest };
}
```

> 원본: [vercel-react-best-practices: js-min-max-loop](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-min-max-loop.md)
