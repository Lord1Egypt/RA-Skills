# Block 10: 병렬 수집 + Output + 마무리

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/sub-agents
> ```

## EXPLAIN

### Block 5~9 정리

지금까지 4개 소스를 각각 다른 방법으로 연결했다:

```
Block 5:  스켈레톤 생성 (4개 STUB)
Block 6:  Slack     ← Connector (브라우저 클릭)         ★☆☆☆
Block 7:  Notion    ← claude mcp add (CLI 명령어)       ★★☆☆
Block 8:  Linear    ← Official Plugin (/plugin)         ★★★☆
Block 9:  Google    ← 커뮤니티 Plugin (구조 분석)        ★★★★
```

### 4가지 연결 방법 총정리: 언제 어떤 방법?

| 상황 | 추천 방법 | 이유 |
|------|----------|------|
| 해당 서비스가 Connector에 있다 | **Connector** | 가장 쉽고 빠르다 |
| HTTP MCP 서버 주소를 알고 있다 | **`claude mcp add`** | 명령어 한 줄이면 끝 |
| 공식 Plugin이 있다 | **Plugin** | MCP + 스킬 + 설정 한 번에 |
| 위 방법이 다 안 된다 | **API 스크립트 (고급)** | Claude가 코드를 작성 |

> 난이도 순서: Connector < mcp add < Plugin < API 스크립트 (고급)
> 유연성 순서: API 스크립트 > Plugin > mcp add > Connector
>
> **참고**: API 스크립트는 고급 방법이다. 오늘 배운 4가지 방법으로 대부분의 도구를 연결할 수 있다.

### 병렬 수집이란?

여러 도구에서 **동시에** 정보를 가져오는 것이다.

**카페로 비유해볼게요.**

점심시간, 손님이 한꺼번에 몰린 카페를 상상해보세요.

**직원 1명인 카페 (순차 수집)**
- 한 명이 주문 받고 → 커피 만들고 → 디저트 준비하고 → 서빙
- 손님 4팀 처리에 40분

**직원 4명인 카페 (병렬 수집)**
- 한 명은 Slack, 한 명은 Notion, 한 명은 Linear, 한 명은 Google
- 각자 맡은 일만 집중 → 4팀 처리에 10분

```
❌ 순차 수집 (직원 1명): 120초
  Slack(30초) → Notion(30초) → Linear(30초) → Google(30초)

✅ 병렬 수집 (직원 4명): 30초
  Slack(30초)    ─┐
  Notion(30초)    ├── 동시에!
  Linear(30초)    │
  Google(30초)   ─┘
```

Claude는 **Subagent(부하 직원)**를 여러 명 동시에 부른다. Day 1에서 배운 그 subagent다.

### 출력 형식 옵션

수집한 정보를 어디에 내보낼 것인가?

| 옵션 | 설명 | 필요 조건 |
|------|------|----------|
| **Markdown 파일** (기본) | 프로젝트 폴더에 .md 파일로 저장 | 없음 (항상 가능) |
| **+ Slack 메시지** | 특정 채널에 요약 발송 | Slack MCP 연결 |
| **+ Notion 페이지** | DB에 새 페이지 생성 | Notion MCP 연결 |

Markdown은 기본으로 항상 포함하고, Slack이나 Notion을 추가하면 더 편리해진다. 여러 개를 동시에 쓸 수도 있다:

```
수집된 정보
  ├── Markdown 파일로 저장 (기록용)     ← 항상 포함
  ├── Slack 채널로 전송 (공유용)        ← 선택
  └── Notion 페이지 생성 (축적용)       ← 선택
```

## EXECUTE

### Step 1: 출력 형식 선택

```json
AskUserQuestion({
  "questions": [{
    "question": "수집 결과를 어떤 형식으로 출력할까요?\n\nMarkdown 파일은 기본으로 항상 포함됩니다.\n추가로 Slack이나 Notion 출력을 선택할 수 있습니다.",
    "header": "출력 형식",
    "options": [
      {"label": "Markdown 파일만", "description": "프로젝트 폴더에 .md 파일로 저장 (가장 간단)"},
      {"label": "Markdown + Slack 전송", "description": "파일 저장 + 특정 Slack 채널에 요약 발송"},
      {"label": "Markdown + Notion 페이지", "description": "파일 저장 + Notion DB에 페이지 생성"},
      {"label": "Markdown + Slack + Notion", "description": "세 곳 모두에 출력"}
    ],
    "multiSelect": false
  }]
})
```

### Step 2: 스킬 파일 실행 흐름 + 출력 포맷 완성

출력 형식 선택 결과에 따라 `.claude/skills/my-context-sync/SKILL.md`의 남은 STUB을 모두 채운다.

**실행 흐름 섹션 완성:**

각 소스별 Agent 호출을 구체화한다:

```
각 소스 수집은 subagent(Agent 도구)로 실행한다.
(아래는 Claude가 자동으로 실행합니다. 여러분이 입력할 필요 없습니다.)

Agent(description="Slack 수집", prompt="...", subagent_type="general-purpose")
Agent(description="Notion 수집", prompt="...", subagent_type="general-purpose")
Agent(description="Linear 수집", prompt="...", subagent_type="general-purpose")
Agent(description="Google 수집", prompt="...", subagent_type="general-purpose")

→ 4개를 동시에 호출 (병렬 실행)
→ 일부 소스가 연결되지 않은 경우, 연결된 소스만으로 수집 진행
```

리포트 형식도 완성:

```
싱크 완료!

수집 결과:
  Slack: 3개 채널, 47개 메시지 ✅
  Notion: 15개 태스크 ✅
  Linear: 8개 이슈 ✅
  Google: 5개 일정, 12개 이메일 ✅

하이라이트 3건:
  1. [Slack] #project-updates: 배포 일정 확정
  2. [Linear] 마감 임박 이슈 2건
  3. [Calendar] 내일 10시 팀 미팅

액션 아이템:
  - [ ] 이메일 회신 2건
  - [ ] Linear 이슈 마감일 확인

파일 저장: sync/2026-03-02-context-sync.md
```

**출력 포맷 섹션 완성:**

선택에 따라 출력 포맷 섹션을 구체화한다.

Slack 포함 시:
```
mcp__claude_ai_Slack__slack_send_message(channel="{채널명}", content="{요약}")
```

Notion 포함 시:
```
Notion MCP로 데이터베이스에 새 페이지 생성
```

### Step 3: 4개 소스 병렬 수집 실행

완성된 스킬을 **실제로 실행**한다.

Claude가 4개 subagent를 동시에 호출하여 수집을 시작한다:

```
[Slack 수집] 진행 중...
[Notion 수집] 진행 중...
[Linear 수집] 진행 중...
[Google 수집] 진행 중...
```

### Step 4: 결과 확인 + 리포트

수집 결과를 성공/실패로 구분하여 보여준다:

```
수집 결과:
  Slack: ✅ 성공 (3개 채널, 47개 메시지)
  Notion: ✅ 성공 (15개 태스크)
  Linear: ❌ 실패 (원인: 인증 토큰 만료)
  Google: ✅ 성공 (5개 일정)

성공: 3/4 소스
```

실패한 소스가 있으면 원인을 분석하고 재시도를 안내한다.

> **성공한 소스만으로도 충분합니다.** 4개 중 2~3개만 성공해도 Context Sync의 가치를 충분히 체험할 수 있다. 나머지 소스는 나중에 추가로 연결하면 된다.

### Step 5: 축하 + 활용 팁

```
축하합니다! 나만의 Context Sync 스킬이 완성되었습니다!

오늘 배운 것:
  ✅ 4가지 연결 방법 (Connector, mcp add, Plugin, 커뮤니티 Plugin)
  ✅ 병렬 수집 (subagent로 동시에)
  ✅ 스킬 구축 (STUB → 점진적 완성)

이제 "싱크해줘" 한마디로 흩어진 정보가 자동으로 모입니다.

활용 팁:
  1. 매일 아침 실행하면 "모닝 브리핑"처럼 사용할 수 있습니다
  2. CLAUDE.md에 스케줄을 추가하면 매일 자동 실행도 가능합니다:
     ## 스케줄
     - context-sync: 매일 09:00 실행
  3. 소스를 추가하고 싶으면 스킬 파일에 같은 형식으로 넣으면 됩니다
  4. Day 3 이후에 이 스킬을 더 발전시킬 수 있습니다
```

## QUIZ

> Block 10은 종합 퀴즈를 출제한다. 사용자가 돌아오면 먼저 "Day 2의 모든 과정을 완료했습니다! 마지막으로 오늘 배운 것을 정리하는 퀴즈입니다." 라고 안내한 뒤 아래 퀴즈를 순서대로 출제한다.

### Quiz 10-1: 병렬 수집

```json
AskUserQuestion({
  "questions": [{
    "question": "\"병렬 수집\"의 가장 큰 장점은 무엇인가요?",
    "header": "Quiz 10-1",
    "options": [
      {"label": "하나가 실패하면 전체가 멈춘다", "description": "오히려 독립 실행이라 다른 소스에 영향 없음"},
      {"label": "여러 소스를 동시에 수집하여 시간을 절약한다", "description": "각 subagent가 독립적으로 동시 실행"},
      {"label": "데이터를 더 정확하게 수집한다", "description": "정확도는 병렬/순차와 무관"}
    ],
    "multiSelect": false
  }]
})
```

정답: 2번. 병렬 수집은 여러 소스를 **동시에** 수집하여 시간을 대폭 절약한다. 4개 소스를 순차적으로 하면 120초 걸릴 것을, 동시에 하면 30초면 된다.

### Quiz 10-2: 출력 형식

```json
AskUserQuestion({
  "questions": [{
    "question": "3가지 출력 형식 중 가장 간단하고, 외부 서비스 연결 없이 바로 쓸 수 있는 것은?",
    "header": "Quiz 10-2",
    "options": [
      {"label": "Slack 메시지", "description": "Slack MCP 연결 필요"},
      {"label": "Notion 페이지", "description": "Notion MCP 연결 필요"},
      {"label": "Markdown 파일", "description": "프로젝트 폴더에 .md 파일로 저장"}
    ],
    "multiSelect": false
  }]
})
```

정답: 3번 (Markdown 파일). 별도 설정 없이 바로 사용할 수 있어서 가장 간단하다. 그래서 기본 출력으로 항상 포함된다.

### Quiz 10-3: 4가지 연결 방법

```json
AskUserQuestion({
  "questions": [{
    "question": "오늘 배운 4가지 연결 방법을 난이도가 낮은 순서대로 나열하면?",
    "header": "Quiz 10-3",
    "options": [
      {"label": "mcp add → Connector → Plugin → 커뮤니티 Plugin", "description": "Connector가 가장 쉬운 방법"},
      {"label": "Connector → mcp add → Plugin → 커뮤니티 Plugin", "description": "Block 6 → 7 → 8 → 9 순서 그대로"},
      {"label": "Plugin → Connector → mcp add → 커뮤니티 Plugin", "description": "Plugin이 가장 쉽지는 않음"}
    ],
    "multiSelect": false
  }]
})
```

정답: 2번. Connector(클릭) → mcp add(명령어) → Plugin(패키지 설치) → 커뮤니티 Plugin(구조 이해까지) 순으로 난이도가 올라간다.

### Quiz 10-4: Day 2 종합

```json
AskUserQuestion({
  "questions": [{
    "question": "Day 2에서 배운 핵심 3가지를 고르세요.",
    "header": "Quiz 10-4",
    "options": [
      {"label": "4가지 도구 연결 방법", "description": "Connector, mcp add, Plugin, 커뮤니티 Plugin"},
      {"label": "HTML 코딩", "description": "Day 2에서 HTML은 다루지 않았음"},
      {"label": "subagent 병렬 수집", "description": "여러 소스에서 동시에 정보 수집"},
      {"label": "서버 배포", "description": "Day 2에서 배포는 다루지 않았음"},
      {"label": "점진적 스킬 구축", "description": "STUB → 하나씩 채움 → 완성"}
    ],
    "multiSelect": true
  }]
})
```

정답: 4가지 도구 연결 방법(1번), subagent 병렬 수집(3번), 점진적 스킬 구축(5번) — 3개 모두 선택
피드백: "완벽합니다! 4가지 방법으로 도구를 연결하고, subagent로 동시에 수집하고, STUB에서 시작해 점진적으로 스킬을 완성했습니다. 이 3가지가 Day 2의 핵심입니다. 내일부터는 이 스킬을 기반으로 더 발전시켜 나갑니다!"
