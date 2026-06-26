---
title: React.lazy for Code Splitting
impact: CRITICAL
impactDescription: directly affects TTI and LCP
tags: bundle, lazy-loading, code-splitting, suspense
---

## React.lazy 코드 스플리팅

초기 렌더링에 불필요한 대형 컴포넌트는 `React.lazy`로 지연 로드.

**Incorrect (메인 번들에 포함 ~300KB):**

```tsx
import { MonacoEditor } from "./monaco-editor";

function CodePanel({ code }: { code: string }) {
  return <MonacoEditor value={code} />;
}
```

**Correct (필요 시 로드):**

```tsx
const MonacoEditor = lazy(() => import("./monaco-editor"));

function CodePanel({ code }: { code: string }) {
  return (
    <Suspense fallback={<div>Loading editor...</div>}>
      <MonacoEditor value={code} />
    </Suspense>
  );
}
```

`React.lazy`는 기본적으로 default export를 기대. named export 사용 시:

```tsx
const MonacoEditor = lazy(() =>
  import("./monaco-editor").then((mod) => ({ default: mod.MonacoEditor }))
);
```

> 원본: [vercel-react-best-practices: bundle-dynamic-imports](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/bundle-dynamic-imports.md)
