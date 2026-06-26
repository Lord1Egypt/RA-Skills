---
title: Combine Multiple Array Iterations
impact: LOW-MEDIUM
impactDescription: reduces iterations from N to 1
tags: javascript, arrays, loops, performance
---

## 배열 반복 합치기

`.filter()`, `.map()` 체이닝은 배열을 여러 번 순회. 단일 루프로 합치기.

**Incorrect (3회 순회):**

```tsx
const admins = users.filter((u) => u.isAdmin);
const testers = users.filter((u) => u.isTester);
const inactive = users.filter((u) => !u.isActive);
```

**Correct (1회 순회):**

```tsx
const admins: User[] = [];
const testers: User[] = [];
const inactive: User[] = [];

for (const user of users) {
  if (user.isAdmin) admins.push(user);
  if (user.isTester) testers.push(user);
  if (!user.isActive) inactive.push(user);
}
```

> 원본: [vercel-react-best-practices: js-combine-iterations](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-combine-iterations.md)
