---
title: Avoid Layout Thrashing
impact: MEDIUM
impactDescription: prevents forced synchronous layouts
tags: javascript, dom, css, performance, reflow, layout-thrashing
---

## 레이아웃 스래싱 방지

스타일 쓰기와 레이아웃 읽기를 번갈아 수행하면 브라우저가 동기 리플로우를 강제. 읽기/쓰기를 분리.

**Incorrect (읽기/쓰기 교차 → 리플로우 2회):**

```tsx
function layoutThrashing(el: HTMLElement) {
  el.style.width = "100px";
  const width = el.offsetWidth; // 리플로우 강제
  el.style.height = "200px";
  const height = el.offsetHeight; // 리플로우 또 강제
}
```

**Correct (쓰기 모아서 → 읽기 1회):**

```tsx
function updateStyles(el: HTMLElement) {
  el.style.width = "100px";
  el.style.height = "200px";

  // 모든 쓰기 후 읽기 (리플로우 1회)
  const { width, height } = el.getBoundingClientRect();
}
```

**Best: CSS 클래스 사용:**

```css
.highlighted-box {
  width: 100px;
  height: 200px;
  background-color: blue;
}
```

```tsx
function Box({ isHighlighted }: { isHighlighted: boolean }) {
  return (
    <div className={isHighlighted ? "highlighted-box" : ""}>Content</div>
  );
}
```

인라인 스타일보다 CSS 클래스 선호. 브라우저 캐시, 관심사 분리, 유지보수성 모두 우수.

> 레이아웃을 강제하는 속성: `offsetWidth`, `offsetHeight`, `getBoundingClientRect()`, `getComputedStyle()`, `scrollTop` 등. 전체 목록: [What forces layout](https://gist.github.com/paulirish/5d52fb081b3570c81e3a)

> 원본: [vercel-react-best-practices: js-batch-dom-css](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-batch-dom-css.md)
