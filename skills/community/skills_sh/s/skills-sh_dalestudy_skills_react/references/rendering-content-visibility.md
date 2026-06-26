---
title: CSS content-visibility for Long Lists
impact: HIGH
impactDescription: faster initial render
tags: rendering, css, content-visibility, lists, performance
---

## content-visibility로 긴 목록 최적화

`content-visibility: auto`로 오프스크린 렌더링 지연.

**CSS:**

```css
.message-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

**사용 예:**

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map((msg) => (
        <div key={msg.id} className="message-item">
          <Avatar user={msg.author} />
          <div>{msg.content}</div>
        </div>
      ))}
    </div>
  );
}
```

1000개 메시지 중 ~990개 오프스크린 아이템의 레이아웃/페인트 건너뜀 (초기 렌더 10배 빨라짐).

> 원본: [vercel-react-best-practices: rendering-content-visibility](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rendering-content-visibility.md)
