---
title: useReducer for Complex State Transitions
impact: MEDIUM
impactDescription: centralizes state logic, prevents invalid transitions
tags: react, useState, useReducer, state-machine, dispatch
---

## useReducer로 복잡한 상태 전이

여러 setState가 산재된 복잡한 로직은 `useReducer`로 이벤트 기반 상태 전이. 상태 업데이트에 명확한 제약과 인과관계 부여.

**Incorrect (여러 useState 산재):**

```tsx
function Timer() {
  const [isRunning, setIsRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [laps, setLaps] = useState<number[]>([]);

  function start() {
    setIsRunning(true);
  }
  function pause() {
    setIsRunning(false);
  }
  function lap() {
    setLaps((prev) => [...prev, elapsed]);
  }
  function reset() {
    setIsRunning(false);
    setElapsed(0);
    setLaps([]);
  }
  // ...
}
```

**Correct (useReducer로 명확한 상태 전이):**

```tsx
type TimerState = {
  status: "idle" | "running" | "paused";
  elapsed: number;
  laps: number[];
};

type TimerAction =
  | { type: "start" }
  | { type: "pause" }
  | { type: "tick" }
  | { type: "lap" }
  | { type: "reset" };

function timerReducer(state: TimerState, action: TimerAction): TimerState {
  switch (action.type) {
    case "start":
      return { ...state, status: "running" };
    case "pause":
      return { ...state, status: "paused" };
    case "tick":
      return state.status === "running"
        ? { ...state, elapsed: state.elapsed + 1 }
        : state; // running이 아니면 무시
    case "lap":
      return { ...state, laps: [...state.laps, state.elapsed] };
    case "reset":
      return { status: "idle", elapsed: 0, laps: [] };
  }
}

function Timer() {
  const [state, dispatch] = useReducer(timerReducer, {
    status: "idle",
    elapsed: 0,
    laps: [],
  });

  // dispatch({ type: "start" }), dispatch({ type: "lap" }) 등
}
```

---

### useReducer 사용 기준

| 상황 | 사용 |
|------|------|
| 연관된 상태 3개 이상 | useReducer |
| 상태 전이에 조건이 있음 (running일 때만 tick) | useReducer |
| 여러 곳에서 같은 상태를 다른 방식으로 업데이트 | useReducer |
| 단순 토글, 카운터 | useState |

> 불가능한 상태 조합 방지는 [`rerender-discriminated-union`](rerender-discriminated-union.md) 참고.

> 원본: [David Khourshid - Goodbye, useState (BeJS Conference)](https://www.youtube.com/watch?v=aGkscOKWQvQ)
