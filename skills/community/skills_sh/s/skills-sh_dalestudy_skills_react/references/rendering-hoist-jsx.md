---
title: Hoist Static JSX Elements
impact: LOW
impactDescription: avoids re-creation
tags: rendering, jsx, static, optimization
---

## 정적 JSX 호이스팅

정적 JSX를 컴포넌트 외부로 추출하여 매 렌더링마다 재생성 방지.

**Incorrect (매 렌더링마다 재생성):**

```tsx
function LoadingSkeleton() {
  return <div className="animate-pulse h-20 bg-gray-200" />;
}

function Container() {
  return <div>{loading && <LoadingSkeleton />}</div>;
}
```

**Correct (한 번만 생성):**

```tsx
const loadingSkeleton = <div className="animate-pulse h-20 bg-gray-200" />;

function Container() {
  return <div>{loading && loadingSkeleton}</div>;
}
```

대형 정적 SVG 노드에서 특히 효과적.

> [React Compiler](https://react.dev/learn/react-compiler) 사용 시 자동 호이스팅.

> 원본: [vercel-react-best-practices: rendering-hoist-jsx](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-hoist-jsx.md)
