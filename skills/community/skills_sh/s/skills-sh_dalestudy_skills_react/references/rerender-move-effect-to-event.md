---
title: Put Interaction Logic in Event Handlers
impact: MEDIUM
impactDescription: avoids effect re-runs and duplicate side effects
tags: rerender, useEffect, events, side-effects
---

## 인터랙션 로직은 이벤트 핸들러에

특정 사용자 액션(제출, 클릭)에 의한 사이드 이펙트는 이벤트 핸들러에서 직접 실행. 상태 + Effect로 모델링하면 의존성 변경 시 중복 실행.

**Incorrect (이벤트를 상태 + Effect로 모델링):**

```tsx
function Form() {
  const [submitted, setSubmitted] = useState(false);
  const theme = useContext(ThemeContext);

  useEffect(() => {
    if (submitted) {
      post("/api/register"); // theme 변경 시에도 재실행!
      showToast("Registered", theme);
    }
  }, [submitted, theme]);

  return <button onClick={() => setSubmitted(true)}>Submit</button>;
}
```

**Correct (이벤트 핸들러에서 직접):**

```tsx
function Form() {
  const theme = useContext(ThemeContext);

  function handleSubmit() {
    post("/api/register");
    showToast("Registered", theme);
  }

  return <button onClick={handleSubmit}>Submit</button>;
}
```

> 참고: [Should this code move to an event handler?](https://react.dev/learn/removing-effect-dependencies#should-this-code-move-to-an-event-handler)

> 원본: [vercel-react-best-practices: rerender-move-effect-to-event](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/rerender-move-effect-to-event.md)
