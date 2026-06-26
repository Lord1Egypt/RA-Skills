---
title: Cache Repeated Function Calls
impact: MEDIUM
impactDescription: avoids redundant computation
tags: javascript, cache, memoization, performance
---

## 반복 함수 호출 캐싱

동일 입력으로 반복 호출되는 함수는 모듈 레벨 Map으로 결과 캐싱.

**Incorrect (동일 이름에 대해 slugify 100+회 반복):**

```tsx
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map((project) => {
        const slug = slugify(project.name); // 매번 재계산
        return <ProjectCard key={project.id} slug={slug} />;
      })}
    </div>
  );
}
```

**Correct (모듈 레벨 캐시):**

```tsx
const slugifyCache = new Map<string, string>();

function cachedSlugify(text: string): string {
  const cached = slugifyCache.get(text);
  if (cached !== undefined) return cached;
  const result = slugify(text);
  slugifyCache.set(text, result);
  return result;
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map((project) => {
        const slug = cachedSlugify(project.name); // 고유 이름당 1회만
        return <ProjectCard key={project.id} slug={slug} />;
      })}
    </div>
  );
}
```

Map(hook 아님)을 사용하면 유틸리티, 이벤트 핸들러 등 React 컴포넌트 외부에서도 동작.

> 원본: [vercel-react-best-practices: js-cache-function-results](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-cache-function-results.md)
