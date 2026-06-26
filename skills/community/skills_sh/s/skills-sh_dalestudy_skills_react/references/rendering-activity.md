---
title: Activity Component for Show/Hide
impact: MEDIUM
impactDescription: preserves state and DOM across visibility toggles
tags: rendering, activity, visibility, state-preservation, offscreen
---

## Activity 컴포넌트로 상태/DOM 보존

자주 토글되는 컴포넌트의 상태와 DOM을 유지. 숨겨진 상태에서도 언마운트되지 않아 재생성 비용 없음.

---

### React `<Activity>` (실험적)

> React의 실험적 API. 안정화 전까지 변경 가능.

```tsx
import { unstable_Activity as Activity } from "react";

function Tabs({ activeTab }: { activeTab: string }) {
  return (
    <div>
      <Activity mode={activeTab === "home" ? "visible" : "hidden"}>
        <HomePage />
      </Activity>
      <Activity mode={activeTab === "settings" ? "visible" : "hidden"}>
        <SettingsPage />
      </Activity>
    </div>
  );
}
```

`hidden` 모드:
- DOM은 유지되지만 `display: none` 처럼 보이지 않음
- 내부 상태 (useState, useRef, 스크롤 위치 등) 보존
- Effect cleanup 실행되지 않음

---

### CSS 기반 대안 (안정적)

`Activity`가 실험적이므로 CSS로 동일 효과 달성.

**`display: none` 패턴:**

```tsx
function Tabs({ activeTab }: { activeTab: string }) {
  return (
    <div>
      <div style={{ display: activeTab === "home" ? "block" : "none" }}>
        <HomePage />
      </div>
      <div style={{ display: activeTab === "settings" ? "block" : "none" }}>
        <SettingsPage />
      </div>
    </div>
  );
}
```

**`content-visibility` 패턴 (렌더링 비용 절감):**

```tsx
function Tabs({ activeTab }: { activeTab: string }) {
  return (
    <div>
      <div
        style={{
          contentVisibility: activeTab === "home" ? "visible" : "hidden",
          containIntrinsicSize: "0 500px",
        }}
      >
        <HomePage />
      </div>
      <div
        style={{
          contentVisibility: activeTab === "settings" ? "visible" : "hidden",
          containIntrinsicSize: "0 500px",
        }}
      >
        <SettingsPage />
      </div>
    </div>
  );
}
```

`content-visibility: hidden`은 `display: none`과 달리 브라우저가 레이아웃/페인트를 건너뛰면서도 DOM 접근은 가능.

---

### 조건부 렌더링 vs Activity/CSS

| 패턴 | 상태 보존 | DOM 유지 | 사용 시점 |
|------|----------|---------|----------|
| `{isOpen && <Comp />}` | ❌ | ❌ | 가벼운 컴포넌트, 상태 불필요 |
| `display: none` | ✅ | ✅ | 상태 보존 필요, 간단한 토글 |
| `content-visibility` | ✅ | ✅ | 무거운 컴포넌트, 렌더링 비용 절감 |
| `<Activity>` | ✅ | ✅ | React 실험적 API 사용 가능 시 |

> 원본: [vercel-react-best-practices: rendering-activity](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-activity.md)
