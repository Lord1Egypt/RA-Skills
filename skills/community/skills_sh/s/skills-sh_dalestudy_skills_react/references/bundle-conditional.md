---
title: Conditional Module Loading
impact: HIGH
impactDescription: loads large data only when needed
tags: bundle, conditional, dynamic-import, lazy-loading
---

## 조건부 모듈 로딩

기능 활성화 시에만 대형 모듈 로드.

```tsx
function AnimationPlayer({
  enabled,
  setEnabled,
}: {
  enabled: boolean;
  setEnabled: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const [frames, setFrames] = useState<Frame[] | null>(null);

  useEffect(() => {
    if (enabled && !frames) {
      import("./animation-frames")
        .then((mod) => setFrames(mod.frames))
        .catch(() => setEnabled(false));
    }
  }, [enabled, frames, setEnabled]);

  if (!frames) return <Skeleton />;
  return <Canvas frames={frames} />;
}
```

> 원본: [vercel-react-best-practices: bundle-conditional](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/bundle-conditional.md)
