---
title: Early Return from Functions
impact: LOW-MEDIUM
impactDescription: avoids unnecessary computation
tags: javascript, early-return, optimization, validation
---

## 조기 반환

결과 확정 시 즉시 반환하여 불필요한 처리 방지.

**Incorrect (에러 발견 후에도 계속 순회):**

```typescript
function validateUsers(users: User[]) {
  let hasError = false;
  let errorMessage = "";
  for (const user of users) {
    if (!user.email) {
      hasError = true;
      errorMessage = "Email required";
    }
    if (!user.name) {
      hasError = true;
      errorMessage = "Name required";
    }
  }
  return hasError ? { valid: false, error: errorMessage } : { valid: true };
}
```

**Correct (즉시 반환):**

```typescript
function validateUsers(users: User[]) {
  for (const user of users) {
    if (!user.email) return { valid: false, error: "Email required" };
    if (!user.name) return { valid: false, error: "Name required" };
  }
  return { valid: true };
}
```

> 원본: [vercel-react-best-practices: js-early-exit](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-early-exit.md)
