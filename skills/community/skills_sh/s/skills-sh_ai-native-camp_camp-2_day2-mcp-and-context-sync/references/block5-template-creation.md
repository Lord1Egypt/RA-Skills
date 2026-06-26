# Block 5: Context Sync 개념 + 스켈레톤 생성

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/sub-agents
> ```

## EXPLAIN

### Context Sync란?

매일 아침 출근하면 이런 일을 한다:

1. Slack 열어서 밤새 온 메시지 확인
2. Gmail 열어서 안 읽은 이메일 확인
3. 캘린더 열어서 오늘 일정 확인
4. Notion 열어서 내 태스크 확인
5. Linear 열어서 이슈 확인

5개 앱을 돌아다니며 30분. 매일 반복. 이것이 **컨텍스트 스위칭**이다.

**Context Sync**는 이 과정을 자동화한다. Claude Code가 여러 도구에서 정보를 모아서 하나의 문서로 정리해준다. 한 번 만들어두면 "싱크해줘" 한 마디로 끝난다.

```
평소                              Context Sync 이후
─────────────                    ──────────────────
Slack 열기                        "싱크해줘" (한 마디)
Gmail 열기                              │
Calendar 열기        ──▶          Claude가 알아서 수집
Notion 열기                             │
Linear 열기                       하나의 문서로 정리!
= 30분 소요                       = 1분 소요
```

### Day 1에서 배운 것과의 연결

Day 1 Block 3-2에서 **스킬(Skill)**을 배웠다. "반복하는 업무를 한 번 저장하면 다음부터 한 줄로 실행하는 업무 레시피." 오늘은 이 스킬을 **직접 만든다.** 그것도 여러 도구를 연결하는 실전 스킬을.

### 오늘 만들 스킬: 4개 도구 × 4가지 연결 방법

오늘은 **4개 도구를 각각 다른 방법으로 연결**하면서 스킬을 완성한다. 블록마다 하나의 도구를 연결하고, 스킬 파일에 해당 소스를 채워넣는 **점진적 빌드** 방식이다.

| Block | 연결 방법 | 도구 | 핵심 배움 |
|-------|----------|------|----------|
| **6** | claude.ai Connector | **Slack** | 가장 쉬운 연결. 클릭 몇 번이면 끝 |
| **7** | `claude mcp add` 명령어 | **Notion** | CLI로 MCP 서버 직접 추가 |
| **8** | Official Plugin (`/plugin`) | **Linear** | Plugin 설치 = MCP 자동 등록 |
| **9** | 커뮤니티 Plugin (구조 분석) | **Google** | Plugin의 내부 구조까지 이해 |

> 4가지 방법을 다 배우면, 앞으로 어떤 도구든 상황에 맞는 방법으로 연결할 수 있다.

### Explore 에이전트

스킬을 만들기 전에, 프로젝트의 현재 상태를 먼저 파악해야 한다. **Explore 에이전트**는 프로젝트의 폴더와 파일을 빠르게 탐색하는 전문 subagent다.

| 구분 | 일반 Subagent | Explore 에이전트 |
|------|--------------|-----------------|
| 역할 | 다양한 작업 수행 | 파일/폴더 탐색 전문 |
| 권한 | 파일 읽기 + 쓰기 | **읽기 전용** (안전함) |
| 용도 | 분석, 작성, 실행 등 | 프로젝트 구조 파악 |

> 요리를 시작하기 전에 냉장고를 여는 것과 같다. 뭐가 있는지 먼저 파악해야 빠진 재료를 알 수 있다.

### 스킬은 이렇게 만들어진다

```
Block 5 (지금):  [STUB] [STUB] [STUB] [STUB] ← 빈 골격 생성
Block 6:         [Slack] [STUB] [STUB] [STUB] ← 소스 1 채움
Block 7:         [Slack] [Notion] [STUB] [STUB] ← 소스 2 채움
Block 8:         [Slack] [Notion] [Linear] [STUB] ← 소스 3 채움
Block 9:         [Slack] [Notion] [Linear] [Google] ← 소스 4 채움
Block 10:        [완성!] 병렬 수집 실행 → 결과 확인
```

## EXECUTE

### Step 1: Explore 에이전트로 프로젝트 구조 파악

Claude가 Explore 에이전트를 호출하여 프로젝트 구조를 파악한다.

> 아래는 Claude가 자동으로 실행하는 코드입니다. 여러분이 직접 입력할 필요 없습니다.

```
Claude가 수행:
  Agent(
    description="프로젝트 구조 탐색",
    prompt="프로젝트 루트에서 다음을 확인하라:
      1. 전체 폴더 구조 (최대 2단계)
      2. .claude/ 디렉토리 내용
      3. .mcp.json 존재 여부와 내용
      4. .env 파일 존재 여부
      5. 기존 스킬이 있다면 목록",
    subagent_type="Explore"
  )
```

탐색 결과를 사용자에게 공유한다:
- 이미 설정된 MCP 서버가 있는지
- API 키나 환경변수가 존재하는지
- 기존 스킬이 있는지

### Step 2: 스켈레톤 스킬 파일 생성

`templates/context-sync.md`를 읽고, 사용자의 프로젝트에 `.claude/skills/my-context-sync/SKILL.md`를 생성한다.

생성 규칙:
1. 템플릿을 **그대로** 복사한다 (4개 소스의 STUB 포함)
2. Explore 결과를 바탕으로 frontmatter의 description을 프로젝트에 맞게 수정한다
3. 탐색에서 발견한 기존 설정이 있으면 해당 소스의 코멘트에 메모한다

### Step 3: 생성 결과 확인

생성된 파일의 전체 구조를 보여준다:

```
.claude/skills/my-context-sync/SKILL.md 생성 완료!

구조:
  📌 소스 1: Slack      [STUB - Block 6에서 Connector로 연결]
  📌 소스 2: Notion     [STUB - Block 7에서 claude mcp add로 연결]
  📌 소스 3: Linear     [STUB - Block 8에서 /plugin install로 연결]
  📌 소스 4: Google     [STUB - Block 9에서 커뮤니티 Plugin으로 연결]
  📌 실행 흐름          [STUB - Block 10에서 완성]
  📌 출력 포맷          [STUB - Block 10에서 완성]

다음 블록(Block 6)부터 STUB을 하나씩 채워갑니다!
```

> 지금은 빈 골격만 만든 것이다. Block 6부터 본격적으로 도구를 연결하고 소스를 채운다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "Context Sync 스킬이 하는 일을 한 문장으로 말하면?",
    "header": "Quiz Block 5",
    "options": [
      {"label": "Claude Code를 설치한다", "description": "설치는 Day 1에서 이미 완료"},
      {"label": "여러 도구에서 정보를 모아 하나의 문서로 정리한다", "description": "Slack, Notion, Linear, Google에서 수집 → 통합"},
      {"label": "Slack 메시지만 정리한다", "description": "Slack은 여러 소스 중 하나일 뿐"}
    ],
    "multiSelect": false
  }]
})
```

정답: 2번. Context Sync 스킬은 **여러 도구에서 정보를 모아 하나의 문서로 정리**하는 스킬이다. 오늘은 4개 도구를 각각 다른 방법으로 연결하면서 이 스킬을 점진적으로 완성한다.
