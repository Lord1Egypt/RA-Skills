---
title: Preload Based on User Intent
impact: MEDIUM
impactDescription: reduces perceived latency
tags: bundle, preload, hover, focus, user-intent
---

## 사용자 의도 기반 프리로드

hover/focus 시 미리 로드하여 체감 지연 감소.

**hover/focus 시 프리로드:**

```tsx
function EditorButton({ onClick }: { onClick: () => void }) {
  const preload = () => void import("./monaco-editor");

  return (
    <button onMouseEnter={preload} onFocus={preload} onClick={onClick}>
      Open Editor
    </button>
  );
}
```

**feature flag 활성화 시 프리로드:**

```tsx
function FlagsProvider({ children, flags }: Props) {
  useEffect(() => {
    if (flags.editorEnabled) {
      void import("./monaco-editor").then((mod) => mod.init());
    }
  }, [flags.editorEnabled]);

  return <FlagsContext.Provider value={flags}>{children}</FlagsContext.Provider>;
}
```

> 원본: [vercel-react-best-practices: bundle-preload](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/bundle-preload.md)
