---
title: Hoist RegExp Creation
impact: LOW-MEDIUM
impactDescription: avoids recreation every render
tags: javascript, regexp, optimization, memoization
---

## RegExp를 모듈 스코프로 호이스팅

렌더링 내에서 RegExp를 생성하면 매 렌더링마다 재생성. 정적이면 모듈 스코프, 동적이면 `useMemo`.

**Incorrect (매 렌더링마다 RegExp 생성):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = new RegExp(`(${query})`, "gi");
  const parts = text.split(regex);
  return <>{parts.map((part, i) => /* ... */)}</>;
}
```

**Correct (정적 → 모듈 스코프):**

```tsx
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function EmailInput({ value }: Props) {
  const isValid = EMAIL_REGEX.test(value);
  // ...
}
```

**Correct (동적 → useMemo):**

```tsx
function Highlighter({ text, query }: Props) {
  const regex = useMemo(
    () => new RegExp(`(${escapeRegex(query)})`, "gi"),
    [query],
  );
  const parts = text.split(regex);
  return <>{parts.map((part, i) => /* ... */)}</>;
}
```

**주의: 글로벌 regex의 가변 상태:**

```tsx
const regex = /foo/g;
regex.test("foo"); // true, lastIndex = 3
regex.test("foo"); // false, lastIndex = 0
```

모듈 스코프의 `/g` regex는 `lastIndex`가 공유되므로 주의. `test()` 대신 `match()`를 사용하거나 매번 `lastIndex = 0` 초기화.

> 원본: [vercel-react-best-practices: js-hoist-regexp](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/js-hoist-regexp.md)
