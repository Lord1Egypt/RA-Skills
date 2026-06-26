---
title: Store Event Handlers in Refs
impact: LOW
impactDescription: stable subscriptions without re-subscribing
tags: advanced, hooks, refs, event-handlers, useEffectEvent
---

## 이벤트 핸들러를 ref에 저장

Effect에서 사용하는 콜백이 변경될 때 재구독을 방지. ref에 최신 핸들러를 저장하여 안정적인 구독 유지.

---

### useEffectEvent (React 실험적 API)

> 안정화되면 이 패턴이 표준. 현재 실험적 API.

```tsx
import { useEffectEvent } from "react";

function useWindowEvent(event: string, handler: (e: Event) => void) {
  const onEvent = useEffectEvent(handler);

  useEffect(() => {
    window.addEventListener(event, onEvent);
    return () => window.removeEventListener(event, onEvent);
  }, [event]);
}
```

`useEffectEvent`는 항상 최신 handler를 호출하는 안정적 함수 참조 생성. 의존성 배열에 추가 불필요.

---

### useInsertionEffect 기반 폴리필 (현재 사용 가능)

`useInsertionEffect`는 DOM 변경 전 동기 실행. ref 업데이트에 가장 안전한 타이밍.

```tsx
function useEffectEvent<T extends (...args: any[]) => any>(fn: T): T {
  const ref = useRef(fn);

  useInsertionEffect(() => {
    ref.current = fn;
  });

  return useCallback((...args: any[]) => ref.current(...args), []) as T;
}
```

**활용:**

```tsx
function useWindowEvent(event: string, handler: (e: Event) => void) {
  const stableHandler = useEffectEvent(handler);

  useEffect(() => {
    window.addEventListener(event, stableHandler);
    return () => window.removeEventListener(event, stableHandler);
  }, [event]);
}
```

> `useInsertionEffect`는 `useLayoutEffect`보다 먼저 실행되어 ref 업데이트 타이밍 문제를 방지. CSS-in-JS 라이브러리용으로 설계되었지만 ref 업데이트에도 안전.

---

### ref 패턴 (useLayoutEffect 사용)

**Incorrect (handler 변경마다 재구독):**

```tsx
function useWindowEvent(event: string, handler: (e: Event) => void) {
  useEffect(() => {
    window.addEventListener(event, handler);
    return () => window.removeEventListener(event, handler);
  }, [event, handler]); // handler 변경 → 해제 → 재등록
}
```

**Correct (ref로 안정적 구독):**

```tsx
function useWindowEvent(event: string, handler: (e: Event) => void) {
  const handlerRef = useRef(handler);

  useLayoutEffect(() => {
    handlerRef.current = handler;
  });

  useEffect(() => {
    const listener = (e: Event) => handlerRef.current(e);
    window.addEventListener(event, listener);
    return () => window.removeEventListener(event, listener);
  }, [event]); // event만 의존 → handler 변경 시 재구독 없음
}
```

---

### 실제 활용 예시

```tsx
function ChatRoom({ roomId, onMessage }: Props) {
  const stableOnMessage = useEffectEvent(onMessage);

  useEffect(() => {
    const ws = new WebSocket(`/ws/rooms/${roomId}`);
    ws.onmessage = (e) => stableOnMessage(JSON.parse(e.data));
    return () => ws.close();
  }, [roomId]); // roomId 변경 시에만 재연결, onMessage 변경은 무시
}
```

---

### 판단 기준

| 상황 | 패턴 |
|------|------|
| Effect 내에서 콜백 사용, 재구독 비용 큼 | ref 패턴 |
| React 실험적 API 사용 가능 | `useEffectEvent` |
| 콜백이 변경되지 않거나 재구독 비용 낮음 | 의존성 배열에 포함 |

> React Compiler 사용 시에도 ref 패턴은 유효. Compiler는 메모이제이션을 자동화하지만 Effect 재구독 자체를 방지하지는 않음.

> 원본: [vercel-react-best-practices: advanced-event-handler-refs](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/advanced-event-handler-refs.md)
