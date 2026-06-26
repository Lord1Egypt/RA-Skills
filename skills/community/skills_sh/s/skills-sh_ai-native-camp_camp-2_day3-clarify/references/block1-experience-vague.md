# Block 1: clarify:vague 체험

## EXPLAIN

### clarify 플러그인의 vague 스킬

Day 1에서 설치한 clarify 플러그인에는 `vague`라는 스킬이 있다. 모호한 요구사항을 구체적인 스펙으로 바꿔주는 스킬이다.

vague 스킬의 4단계 프로토콜:

```
Phase 1: Capture        원본 요구사항을 그대로 기록
    ↓
Phase 2: Iterate        AskUserQuestion으로 5-8개 질문
    ↓                   (가설 기반 선택지, 최대 4개씩 묶어서)
Phase 3: Before/After   변환 전후를 비교하여 보여줌
    ↓
Phase 4: Save           결과를 파일로 저장할지 물어봄
```

### 실제 변환 예시

```
┌─ Before ──────────────────────────┐
│ "우리 팀 회의록 자동화해줘"         │
└───────────────────────────────────┘
                 ↓ Clarify (질문 6개)
┌─ After ───────────────────────────┐
│ 목표: 주간 팀 회의 후 회의록 자동 생성│
│ 범위: 월요일 오전 회의만 대상        │
│ 형식: Notion 페이지, 참석자별 액션   │
│ 입력: Fireflies 녹취록             │
│ 제약: 회의 후 30분 내 완성          │
│ 우선순위: 액션 아이템 > 논의 내용    │
└───────────────────────────────────┘
```

"회의록 자동화해줘"라는 5단어가 구체적인 실행 스펙으로 바뀌었다. 이 과정에서 사용자 스스로도 "아, 나는 전체 회의가 아니라 월요일 회의만 원했구나"를 발견하게 된다.

## EXECUTE

이제 clarify:vague를 직접 체험해보자.

### 1단계: 플러그인 설치 확인

먼저 clarify 플러그인이 설치되어 있는지 확인한다:

```
/plugin
```

> 목록에 `clarify`가 보이면 OK. 없으면 아래 명령으로 다시 설치한다:
> ```
> /plugin marketplace add team-attention/plugins-for-claude-natives
> /plugin install clarify
> ```

### 2단계: 모호한 요구사항 던지기

자신의 1주일 과제 중 가장 모호한 부분을 하나 골라서, Claude에게 던져보자.

예시:

```
나는 [내 과제 중 모호한 부분]을 하고 싶어.
근데 아직 구체적으로 뭘 어떻게 해야 할지 모르겠어.
모호한 부분을 clarify해줘.
```

또는 직접 스킬을 호출할 수도 있다:

```
/clarify:vague
```

> Claude가 AskUserQuestion으로 5-8개의 가설 기반 질문을 던질 것이다.
> 각 질문에 선택지를 고르면서, 처음에는 몰랐던 내 요구사항이 구체화되는 과정을 경험하자.
> 마지막에 Before/After 요약이 나온다.

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "clarify:vague의 핵심 원칙은 무엇인가요?",
      "header": "Quiz 1-1",
      "options": [
        {"label": "가설을 선택지로 제시 (Hypothesis-as-Options)", "description": "열린 질문 대신 가설 기반 옵션을 AskUserQuestion으로 제시"},
        {"label": "최대한 많은 질문을 한다", "description": "5-8개 상한이 있음"},
        {"label": "사용자의 답을 그대로 실행한다", "description": "Clarify 후에도 확인이 필요함"}
      ],
      "multiSelect": false
    },
    {
      "question": "clarify:vague 체험 중 가장 의외였던 점은 무엇인가요?",
      "header": "체험 소감",
      "options": [
        {"label": "내가 뭘 원하는지 스스로 몰랐던 부분이 있었다", "description": "질문을 받으면서 비로소 깨달음"},
        {"label": "선택지로 물어보니 결정이 빨라졌다", "description": "열린 질문보다 인지 부하가 낮았음"},
        {"label": "Before/After 비교가 인상적이었다", "description": "변환 전후의 차이가 명확"},
        {"label": "아직 잘 와닿지 않는다", "description": "다음 블록에서 직접 만들어보면 더 체감됨"}
      ],
      "multiSelect": true
    }
  ]
})
```

정답: Quiz 1-1은 1번. **Hypothesis-as-Options**이 clarify:vague의 핵심이다. 열린 질문이 아니라, Claude가 먼저 가설을 세워서 선택지로 제시한다. 체험 소감은 어떤 것이든 좋다 — 중요한 건 "clarify 받는 사람" 입장을 직접 경험한 것이다.
