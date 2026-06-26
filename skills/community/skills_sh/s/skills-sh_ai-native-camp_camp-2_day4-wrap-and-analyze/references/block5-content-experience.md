# Block 5: 콘텐츠 소화 체험 — Fetch & Digest

> 공식 문서: https://code.claude.com/docs/ko/skills

## EXPLAIN

### 1. 콘텐츠 소화 파이프라인

Day 4의 마지막 블록입니다. 지금까지 session-wrap, history-insight, session-analyzer로 "내 작업을 분석하는 스킬"을 만들었습니다. 이제 **외부 콘텐츠를 가져와서 소화하는** 방법을 체험합니다.

**비유: 외국 음식 먹기**

1. **메뉴 가져오기 (Fetch)**: 영어 트윗이나 아티클을 가져온다
2. **번역하기 (Translate)**: 요약 → 인사이트 → 전체 번역 순서로 이해한다
3. **소화하기 (Digest)**: 퀴즈를 풀며 기억에 남긴다

### 2. 스킬 체이닝 (Skill Chaining)

**비유: 공장 생산라인**

```
[URL 입력] → [fetch 스킬: 원문 추출 + 번역] → [digest 스킬: 퀴즈-학습]
```

앞 스킬의 결과물을 다음 스킬이 받아서 처리합니다. 이것이 **스킬 체이닝**입니다.

### 3. fetch-tweet: 트윗 가져오기

X/Twitter URL을 받으면:
1. **FxEmbed API**로 트윗 텍스트, 작성자, 반응 수치를 추출
2. **번역 파이프라인**: 요약(3-5문장) → 인사이트(3개) → 전체 번역

```
원래 URL: https://x.com/user/status/123456
변환 URL: https://api.fxtwitter.com/user/status/123456
```

도메인만 바꾸면 트윗 데이터가 JSON으로 옵니다. 왜 요약부터? **전체 번역을 먼저 보면 핵심을 놓치기 쉽습니다.** 요약으로 핵심을 잡고, 인사이트로 의미를 파악한 뒤, 전체를 읽으면 이해도가 훨씬 높아집니다.

### 4. content-digest: Quiz-First 학습법

가져온 콘텐츠를 "소화"하는 스킬입니다.

**핵심 원칙: "요약을 먼저 보여주지 않는다"**

보통은 요약을 읽고 → 퀴즈를 풀지만, 연구에 따르면 **반대로 하는 것이 9-12% 더 효과적**입니다.

```
❌ 일반적 순서: 요약 읽기 → 퀴즈
✅ Quiz-First: 퀴즈 먼저 → 틀린 부분 확인 → 선택적으로 읽기
```

- **Pretesting Effect**: 학습 전 테스트가 기억력을 9-12% 향상 (Richland et al.)
- **Information Gap Theory**: 틀린 문제가 "궁금함"을 만들고, 궁금함이 도파민 → 기억 강화

**간단히 말해: 틀려야 배운다.**

### 5. 오늘 체험할 것

직접 스킬을 만들지 않고, 이미 설치된 스킬을 **체험**합니다:

| 체험 | 하는 일 | 시간 |
|------|---------|------|
| fetch-tweet 체험 | 실제 영어 트윗을 가져와서 번역 파이프라인 확인 | ~5분 |
| content-digest 체험 | 설치된 content-digest 스킬로 Quiz-First 학습 | ~5분 |
| compound 체험 | 오늘 배운 인사이트를 구조화된 문서로 기록 | ~5분 |
| team-assemble 소개 | 전문가 에이전트 팀 구성 개념 이해 | ~5분 |

> 스킬을 직접 만들고 싶다면, 캠프 이후 `day5-fetch-and-digest` 스킬로 심화 학습할 수 있습니다.

> **보너스 스킬**: compound는 작업 중 발견한 인사이트를 `knowledge/` 폴더에 구조화해서 저장합니다. team-assemble은 복잡한 작업을 전문가 에이전트 팀으로 나눠서 병렬 실행합니다. 둘 다 이미 설치되어 있으니 바로 체험할 수 있습니다.

---

## EXECUTE

### 체험 1: fetch-tweet으로 트윗 가져오기

좋아하는 영어 트윗 URL을 하나 찾으세요. AI, 기술, 비즈니스 관련 트윗이면 더 좋습니다.

Claude에게 이렇게 입력하세요:

```
이 트윗을 요약-인사이트-전체 번역 해줘: [여기에 실제 X/Twitter URL]
```

> **결과를 확인하세요:**
> - 요약이 핵심을 잘 잡았는지
> - 인사이트가 실제로 유용한지
> - 전체 번역이 자연스러운지

### 체험 2: content-digest로 Quiz-First 학습

방금 가져온 트윗 내용으로 퀴즈를 풀어봅니다:

```
/content-digest [방금 가져온 트윗 URL 또는 내용을 붙여넣기]
```

> content-digest 스킬이 자동으로 Quiz-First 방식을 적용합니다. 요약을 먼저 보여주지 않고 퀴즈부터 출제합니다.

> 퀴즈를 풀고 난 후의 느낌이 다릅니다:
> - 틀린 문제가 있으면 "왜 틀렸지?"라는 호기심이 생깁니다
> - 그 상태에서 내용을 다시 읽으면 기억에 더 잘 남습니다

### 체험 3: compound로 인사이트 기록

Day 4에서 가장 인상 깊었던 것을 compound 스킬로 기록해봅니다:

```
/compound
```

Claude가 인사이트를 어떤 도메인(work/learning/project/tool/personal)에 기록할지 물어볼 것입니다. 답변하면 구조화된 문서가 `knowledge/` 폴더에 생성됩니다.

> 예: "session-wrap을 만들면서 multi-agent 패턴의 핵심이 '병렬 실행 + 중복 검증'이라는 걸 알게 됐다"

### (선택) 나만의 콘텐츠 파이프라인 구상

시간이 있다면, 앞으로 어떤 콘텐츠를 자동으로 가져와서 학습할지 생각해보세요:

- 매일 아침 특정 인플루언서의 트윗을 가져와서 학습?
- YouTube 발표 영상을 자동으로 요약?
- 여러 소스를 모아서 주간 다이제스트?

```
나는 [분야]에 관심이 있어. 콘텐츠 소화 파이프라인을 어떻게 구성하면 좋을지 제안해줘.
```

### (선택) team-assemble 맛보기

여러 에이전트가 협력하는 팀을 구성해볼 수 있습니다:

```
/team-assemble 내 프로젝트의 README를 분석하고, 개선점을 제안하고, 실제로 수정해줘
```

> team-assemble은 작업을 분석 → 팀 설계 → 병렬 실행 → 검증까지 자동으로 진행합니다. session-wrap에서 배운 multi-agent 패턴이 실전에서 어떻게 쓰이는지 체감할 수 있습니다.

---

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "fetch-tweet에서 번역 순서가 '요약 → 인사이트 → 전체 번역'인 이유는?",
      "header": "Quiz 5-1",
      "options": [
        {"label": "API가 그 순서로 데이터를 반환하니까", "description": "FxEmbed API의 응답 구조 때문"},
        {"label": "전체 번역을 먼저 보면 핵심을 놓치기 쉬우니까", "description": "요약으로 핵심을 잡고 인사이트로 의미를 파악한 뒤 전체를 읽으면 이해도 향상"},
        {"label": "Claude의 토큰 제한 때문에 단계별로 처리해야 하니까", "description": "컨텍스트 윈도우 관리를 위해"}
      ],
      "multiSelect": false
    },
    {
      "question": "Quiz-First 학습법에서 '요약을 먼저 보여주지 않는' 이유는?",
      "header": "Quiz 5-2",
      "options": [
        {"label": "요약이 부정확할 수 있으니까", "description": "AI 요약의 정확도 문제"},
        {"label": "틀린 문제가 호기심을 만들고, 호기심이 기억을 강화하니까", "description": "학습 전 테스트가 기억력을 9-12% 향상시킨다는 연구"},
        {"label": "퀴즈로 수준을 파악해야 맞춤 요약을 줄 수 있으니까", "description": "수준별 맞춤 학습을 위한 선행 평가"}
      ],
      "multiSelect": false
    }
  ]
})
```

**정답 5-1: 2번.** 전체 번역부터 보면 핵심을 놓치기 쉽다. 요약으로 "이 트윗이 뭘 말하는지" 파악하고, 인사이트로 "나에게 어떤 의미인지" 정리한 뒤, 전체를 읽으면 맥락 속에서 이해도가 훨씬 높아진다.

**정답 5-2: 2번.** Pretesting Effect 연구에 따르면 학습 전 테스트가 기억력을 9-12% 향상시킨다. 퀴즈에서 틀리면 "왜 틀렸지?"라는 호기심(Information Gap)이 생기고, 이 상태에서 콘텐츠를 읽으면 기억이 더 잘 남는다.

### Day 4 마무리

4일간의 캠프를 돌아봅니다:

| Day | 배운 것 | 만든 것 |
|-----|---------|---------|
| Day 1 | Claude Code 핵심 기능 7개 | Memory, 첫 스킬, Plugin 설치 |
| Day 2 | MCP + Context Sync | MCP 연결, Context Sync 스킬 |
| Day 3 | Clarify + Plugin + GitHub | 나만의 Clarify 스킬, PRD 제출 |
| Day 4 | Wrap & Analyze + 콘텐츠 소화 | session-wrap 스킬, content-digest 체험, compound 기록, team-assemble 소개 |

> **수료가 아니라 시작입니다.** Claude Code라는 불을 다루는 신인류 커뮤니티의 일원이 되었습니다.
> 만든 스킬을 매일 사용하면서 개선해보세요. 실제 사용이 최고의 학습입니다.
