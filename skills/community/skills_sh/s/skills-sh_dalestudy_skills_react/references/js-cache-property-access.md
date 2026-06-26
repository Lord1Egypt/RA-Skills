---
title: Cache Property Access in Loops
impact: LOW-MEDIUM
impactDescription: reduces repeated lookups
tags: javascript, loops, optimization, caching
---

## 루프 내 프로퍼티 접근 캐싱

핫 패스에서 객체 프로퍼티 체이닝을 반복 접근하면 불필요한 룩업 발생. 변수에 캐싱.

**Incorrect (3단계 룩업 × N 반복):**

```tsx
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value);
}
```

**Correct (1회 룩업):**

```tsx
const value = obj.config.settings.value;
const len = arr.length;
for (let i = 0; i < len; i++) {
  process(value);
}
```

> 원본: [vercel-react-best-practices: js-cache-property-access](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-cache-property-access.md)
