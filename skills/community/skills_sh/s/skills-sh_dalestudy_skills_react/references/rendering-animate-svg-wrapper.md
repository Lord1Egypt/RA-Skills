---
title: Animate SVG Wrapper Instead of SVG Element
impact: LOW
impactDescription: enables hardware acceleration
tags: rendering, svg, animation, gpu, performance
---

## SVG 애니메이션: 래퍼 사용

브라우저는 SVG 요소에 CSS3 애니메이션 하드웨어 가속을 지원하지 않는 경우가 많음. `<div>` 래퍼로 감싸서 애니메이션 적용.

**Incorrect (하드웨어 가속 없음):**

```tsx
function LoadingSpinner() {
  return (
    <svg className="animate-spin" width="24" height="24" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="currentColor" />
    </svg>
  );
}
```

**Correct (GPU 가속):**

```tsx
function LoadingSpinner() {
  return (
    <div className="animate-spin">
      <svg width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" stroke="currentColor" />
      </svg>
    </div>
  );
}
```

`transform`, `opacity`, `translate`, `scale`, `rotate` 등 모든 CSS 변환에 해당.

> 원본: [vercel-react-best-practices: rendering-animate-svg-wrapper](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-animate-svg-wrapper.md)
