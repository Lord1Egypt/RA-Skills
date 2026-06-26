---
title: Defer Non-Critical Third-Party Libraries
impact: MEDIUM
impactDescription: loads analytics/tracking after hydration
tags: bundle, third-party, analytics, defer, lazy-loading, partytown, web-worker
---

## 비필수 서드파티 라이브러리 지연 로드

Analytics, 에러 트래킹, 로깅 등은 사용자 인터랙션을 차단하지 않아야 함. 하이드레이션 후 로드.

**Incorrect (초기 번들에 포함):**

```tsx
import { init as initAnalytics } from "analytics-sdk";

function App() {
  useEffect(() => {
    initAnalytics();
  }, []);
  return <MainContent />;
}
```

**Correct (React.lazy로 지연 로드):**

```tsx
import { lazy, Suspense } from "react";

const Analytics = lazy(() =>
  import("./Analytics").then((m) => ({ default: m.Analytics })),
);

function App() {
  return (
    <>
      <MainContent />
      <Suspense fallback={null}>
        <Analytics />
      </Suspense>
    </>
  );
}
```

**Correct (동적 import로 하이드레이션 후 초기화):**

```tsx
function App() {
  useEffect(() => {
    // 하이드레이션 완료 후 실행
    import("analytics-sdk").then(({ init }) => init());
  }, []);

  return <MainContent />;
}
```

**requestIdleCallback으로 더 낮은 우선순위:**

```tsx
useEffect(() => {
  const id = requestIdleCallback(() => {
    import("analytics-sdk").then(({ init }) => init());
  });
  return () => cancelIdleCallback(id);
}, []);
```

---

### Partytown: 서드파티를 Web Worker로 이동

[Partytown](https://partytown.builder.io/)은 서드파티 스크립트(Google Analytics, Tag Manager, Facebook Pixel 등)를 Web Worker에서 실행. 메인 스레드를 완전히 해방.

```bash
npm install @builder.io/partytown
```

**HTML script 태그 방식:**

```html
<script>
  /* Partytown 인라인 스니펫 (공식 문서 참고) */
</script>

<!-- type="text/partytown"으로 Worker 이동 -->
<script type="text/partytown" src="https://www.googletagmanager.com/gtag/js?id=G-XXXXX"></script>
<script type="text/partytown">
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXX');
</script>
```

**React 컴포넌트 방식 (Astro, Vite 등):**

```tsx
import { Partytown } from "@builder.io/partytown/react";

function Document() {
  return (
    <html>
      <head>
        <Partytown forward={["dataLayer.push"]} />
        <script
          type="text/partytown"
          src="https://www.googletagmanager.com/gtag/js?id=G-XXXXX"
        />
      </head>
      <body>
        <App />
      </body>
    </html>
  );
}
```

`forward` 배열에 메인 스레드에서 호출하는 함수를 선언하면 Partytown이 Worker로 프록시.

---

### 지연 로드 방식 선택 기준

| 방식 | 메인 스레드 영향 | 복잡도 | 적합한 경우 |
|------|----------------|--------|------------|
| 동적 `import()` | 로드 후 실행 시 차지 | 낮음 | 자체 SDK, 에러 트래킹 |
| `React.lazy` + `Suspense` | 로드 후 실행 시 차지 | 낮음 | UI 컴포넌트 형태의 서드파티 |
| `requestIdleCallback` | 유휴 시에만 | 낮음 | 긴급하지 않은 초기화 |
| **Partytown** | **완전 제거** | 중간 | Google Analytics, Tag Manager, 광고 픽셀 |

> Partytown은 DOM 접근이 필요한 스크립트(채팅 위젯 등)에는 부적합. 순수 추적/분석 스크립트에 최적.

> 원본: [vercel-react-best-practices: bundle-defer-third-party](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/bundle-defer-third-party.md)
