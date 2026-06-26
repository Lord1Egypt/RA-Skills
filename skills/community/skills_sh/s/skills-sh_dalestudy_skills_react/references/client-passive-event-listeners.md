---
title: Use Passive Event Listeners for Scrolling Performance
impact: MEDIUM
impactDescription: eliminates scroll delay caused by event listeners
tags: events, passive, scroll, touch, performance
---

## passive 이벤트 리스너

`preventDefault()` 호출하지 않는 touch/wheel 리스너에 `{ passive: true }` 추가. 브라우저가 `preventDefault()` 호출 여부 확인을 기다리지 않아 즉시 스크롤.

**Incorrect:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener("touchstart", handleTouch);
  document.addEventListener("wheel", handleWheel);

  return () => {
    document.removeEventListener("touchstart", handleTouch);
    document.removeEventListener("wheel", handleWheel);
  };
}, []);
```

**Correct:**

```typescript
useEffect(() => {
  const handleTouch = (e: TouchEvent) => console.log(e.touches[0].clientX);
  const handleWheel = (e: WheelEvent) => console.log(e.deltaY);

  document.addEventListener("touchstart", handleTouch, { passive: true });
  document.addEventListener("wheel", handleWheel, { passive: true });

  return () => {
    document.removeEventListener("touchstart", handleTouch);
    document.removeEventListener("wheel", handleWheel);
  };
}, []);
```

**passive 사용:** 트래킹/분석, 로깅, `preventDefault()` 불필요한 리스너
**passive 미사용:** 커스텀 스와이프, 커스텀 줌, `preventDefault()` 필요한 리스너

> 원본: [vercel-react-best-practices: client-passive-event-listeners](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/client-passive-event-listeners.md)
