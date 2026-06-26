---
title: Use Set/Map for O(1) Lookups
impact: LOW-MEDIUM
impactDescription: O(n) to O(1)
tags: javascript, set, map, lookup, performance
---

## Set으로 O(1) 멤버십 검사

배열을 Set/Map으로 변환하여 반복 멤버십 검사 최적화.

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ["a", "b", "c"];
items.filter((item) => allowedIds.includes(item.id));
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(["a", "b", "c"]);
items.filter((item) => allowedIds.has(item.id));
```

> 원본: [vercel-react-best-practices: js-set-map-lookups](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-set-map-lookups.md)
