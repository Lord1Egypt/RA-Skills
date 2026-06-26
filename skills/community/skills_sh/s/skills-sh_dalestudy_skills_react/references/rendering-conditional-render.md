---
title: Use Explicit Conditional Rendering
impact: LOW
impactDescription: prevents rendering 0 or NaN
tags: rendering, conditional, jsx, ternary
---

## 조건부 렌더링: 삼항 연산자

`&&` 사용 시 `0`, `NaN` 등 falsy 값이 렌더링되는 버그 방지. 삼항 연산자(`? :`) 사용.

**Incorrect (count가 0일 때 "0" 렌더링):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count && <span className="badge">{count}</span>}
    </div>
  );
}
// count = 0 → <div>0</div>
// count = 5 → <div><span class="badge">5</span></div>
```

**Correct (count가 0일 때 아무것도 렌더링하지 않음):**

```tsx
function Badge({ count }: { count: number }) {
  return (
    <div>
      {count > 0 ? <span className="badge">{count}</span> : null}
    </div>
  );
}
// count = 0 → <div></div>
// count = 5 → <div><span class="badge">5</span></div>
```

> 원본: [vercel-react-best-practices: rendering-conditional-render](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-conditional-render.md)
