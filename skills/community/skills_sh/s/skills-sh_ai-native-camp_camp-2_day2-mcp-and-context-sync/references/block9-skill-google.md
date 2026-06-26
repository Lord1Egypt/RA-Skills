# Block 9: Plugin 구조 분석 → Google Calendar/Gmail

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 참조: https://github.com/team-attention/plugins-for-claude-natives
> ```

## EXPLAIN

### 네 번째 연결 방법: 커뮤니티 Plugin (구조까지 이해하기)

Block 8에서 공식 Plugin을 `/plugin install`로 설치했다. 한 줄이면 MCP까지 자동 등록되는 편리함을 체험했다.

이번 블록에서는 한 걸음 더 나아간다:

> **"Plugin 속은 어떻게 생겼을까?"**

Plugin을 **쓸 줄 아는 사람**과 **만들 줄 아는 사람**은 다르다. Plugin의 내부 구조를 이해하면, 나중에 나만의 Plugin도 만들 수 있다.

### Plugin 디렉토리 구조

Plugin은 이런 파일들로 구성되어 있다:

```
my-plugin/
├── plugin.json              ← "이 Plugin의 이력서" (루트에 위치)
├── skills/                  ← 스킬 파일들 (루트에 위치)
│   └── my-skill/
│       └── SKILL.md
├── .mcp.json                ← MCP 서버 자동 등록 설정 (루트에 위치)
├── settings.json            ← Claude Code 설정 (루트에 위치)
└── hooks/                   ← 자동 실행 트리거
```

### 파일별 역할

| 파일 | 역할 | 비유 |
|------|------|------|
| `plugin.json` | Plugin 정보 (이름, 설명, 버전) | 제품 상자의 라벨 |
| `skills/` | 이 Plugin이 가르치는 스킬 | 설명서 |
| `.mcp.json` | MCP 서버 자동 등록 설정 | 전원 어댑터 (꽂으면 바로 연결) |
| `settings.json` | Claude Code 설정 | 기본 세팅 값 |
| `hooks/` | 특정 시점에 자동 실행되는 스크립트 | 알람 설정 |

> **핵심**: `.mcp.json`이 Plugin 루트에 있기 때문에 Plugin을 설치하면 MCP가 자동으로 활성화되는 것이다! Block 8에서 "claude mcp add 안 했는데!" 했던 이유가 바로 이 파일 덕분이다.

### 커뮤니티 Plugin

공식 Plugin 외에 커뮤니티에서 만든 Plugin도 있다. 오늘은 **team-attention/plugins-for-claude-natives**에서 Google Calendar/Gmail Plugin을 설치한다.

이 Plugin은 비개발자를 위해 설계된 것으로:
- Google Calendar: 일정 조회, 생성, 수정
- Gmail: 이메일 조회, 발송, 검색
- 설치만 하면 MCP 서버가 자동 등록되어 바로 사용 가능

### 4가지 연결 방법 총정리

| # | 방법 | Block | 도구 | 난이도 | 핵심 |
|---|------|-------|------|--------|------|
| 1 | Connector | 6 | Slack | ★☆☆☆ | 브라우저 클릭 |
| 2 | `claude mcp add` | 7 | Notion | ★★☆☆ | CLI 명령어 |
| 3 | Official Plugin | 8 | Linear | ★★★☆ | 공식 패키지 |
| 4 | **커뮤니티 Plugin** | **9** | **Google** | **★★★★** | **구조 이해 + 설치** |

### Plan B: Google 서비스가 없다면?

Google Calendar/Gmail을 사용하지 않는다면, Plugin의 구조 분석만 진행하고 소스 4를 비워둘 수 있다. 구조를 이해하는 것 자체가 이 블록의 핵심 배움이다.

## EXECUTE

### Step 1: 커뮤니티 Plugin Marketplace 추가

```bash
/plugin marketplace add team-attention/plugins-for-claude-natives
```

이 명령어로 team-attention의 Plugin marketplace를 등록한다.

### Step 2: 도구 선택

```json
AskUserQuestion({
  "questions": [{
    "question": "Google Calendar과 Gmail 중 어떤 것을 연결할까요?",
    "header": "Google 도구 선택",
    "options": [
      {"label": "Google Calendar", "description": "일정 조회/관리"},
      {"label": "Gmail", "description": "이메일 조회/관리"},
      {"label": "둘 다", "description": "Calendar + Gmail 모두 연결"},
      {"label": "Skip", "description": "Plugin 구조 분석만 하고 넘어가기"}
    ],
    "multiSelect": false
  }]
})
```

### Step 3: Explore 에이전트로 Plugin 구조 탐색

설치 전에, Plugin의 내부 구조를 먼저 살펴본다:

> 아래는 Claude가 자동으로 실행하는 코드입니다. 여러분이 직접 입력할 필요 없습니다.

```
Claude가 수행:
  Agent(
    description="Plugin 구조 탐색",
    prompt="team-attention/plugins-for-claude-natives 플러그인의 구조를 탐색하라:
      1. plugin.json 내용
      2. skills/ 디렉토리 구조
      3. .mcp.json 내용 (MCP 자동 등록 설정)
      4. 스킬 파일이 있다면 목록
      5. hooks/ 디렉토리가 있다면 내용",
    subagent_type="Explore"
  )
```

탐색 결과를 사용자에게 설명한다:
- "이 파일이 Plugin의 이력서(plugin.json)입니다"
- "이 파일(.mcp.json) 때문에 설치하면 MCP가 자동으로 활성화됩니다"
- "skills/ 폴더에 스킬이 들어있어서 설치 후 바로 사용할 수 있습니다"

> ⚠️ 보안 안내: Google 서비스 연결 시 Google 계정 인증이 필요하다. 회사 Google Workspace 계정은 관리자 정책에 따라 외부 앱 연결이 제한될 수 있으므로, 개인 Google 계정 사용을 권장한다.

### Step 4: Plugin 설치

선택한 도구에 따라 설치한다:

```bash
# Google Calendar 선택 시
/plugin install google-calendar

# Gmail 선택 시
/plugin install gmail

# 둘 다 선택 시
/plugin install google-calendar
/plugin install gmail
```

### Step 5: `/mcp` 확인 + 테스트

```
/mcp 입력

확인할 것:
→ local 섹션에 google-calendar 또는 gmail이 추가되었는지
→ 연결 상태가 정상인지

테스트:
  Calendar: "이번 주 일정 보여줘"
  Gmail: "안 읽은 이메일 보여줘"
```

> Google 인증이 필요할 수 있다. 브라우저에서 Google 계정으로 로그인하고 "허용"을 클릭한다.

### Step 6: 스킬 소스 4 채우기

`.claude/skills/my-context-sync/SKILL.md`의 **소스 4: Google Calendar / Gmail** 섹션을 채운다.

```markdown
### 소스 4: Google Calendar / Gmail

| 항목 | 값 |
|------|-----|
| 연결 방법 | 커뮤니티 Plugin (team-attention/plugins-for-claude-natives) |
| MCP 도구 | Plugin이 등록한 Google Calendar/Gmail MCP 도구 |
| 수집 범위 | 오늘 ~ 7일 후 (Calendar) / 최근 7일 (Gmail) |

수집 방법:
Plugin의 MCP 도구를 사용하여 일정/이메일을 조회한다.
  (도구명은 /mcp에서 확인한 것으로 교체)

추출할 정보:
- 오늘의 일정 + 이번 주 주요 미팅
- 안 읽은 이메일 요약
- 회신이 필요한 이메일
- 준비가 필요한 미팅
```

> 스킬 파일의 진행 상황:
> ```
> 소스 1: Slack     ✅ 채움!
> 소스 2: Notion    ✅ 채움!
> 소스 3: Linear    ✅ 채움!
> 소스 4: Google    ✅ 채움!
> 실행 흐름         [STUB - Block 10에서 완성]
> 출력 포맷         [STUB - Block 10에서 완성]
> ```

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "Plugin 루트에 있는 `.mcp.json` 파일의 역할은?",
      "header": "Quiz 9-1",
      "options": [
        {"label": "Plugin의 이름과 버전 정보", "description": "그건 plugin.json의 역할"},
        {"label": "Claude Code의 보안 설정", "description": "보안 설정과는 다른 파일"},
        {"label": "Plugin 설치 시 MCP 서버를 자동으로 활성화하는 설정", "description": "이 파일이 있어서 claude mcp add가 필요 없는 것"}
      ],
      "multiSelect": false
    },
    {
      "question": "4가지 연결 방법 중 가장 많은 것을 한 번에 설치하는 방법은?",
      "header": "Quiz 9-2",
      "options": [
        {"label": "Connector", "description": "Connector는 MCP 연결만 제공"},
        {"label": "Plugin (MCP + 스킬 + 설정 + 훅 포함)", "description": "패키지이므로 여러 구성요소를 한 번에 설치"},
        {"label": "claude mcp add", "description": "mcp add는 MCP 서버 하나만 등록"}
      ],
      "multiSelect": false
    },
    {
      "question": "Plugin 구조를 이해하면 무엇이 가능해지나요?",
      "header": "Quiz 9-3",
      "options": [
        {"label": "Claude Code를 더 빠르게 실행할 수 있다", "description": "속도와는 관계없음"},
        {"label": "다른 사람의 Plugin을 삭제할 수 있다", "description": "삭제와는 관계없음"},
        {"label": "나만의 Plugin을 만들 수 있다", "description": "구조를 알면 직접 제작 가능"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 9-1은 3번, Quiz 9-2는 2번, Quiz 9-3은 3번.
- `.mcp.json`은 Plugin 루트에 위치하며, **Plugin 설치 시 MCP 서버를 자동으로 활성화**하는 설정 파일이다. Block 8에서 "claude mcp add 안 했는데!" 했던 비밀이 바로 이 파일이다.
- **Plugin**은 MCP + 스킬 + 설정 + 훅을 한꺼번에 설치하므로, 4가지 방법 중 가장 많은 것을 한 번에 처리한다.
- Plugin 구조를 이해하면 **나만의 Plugin을 만들 수 있다.** "쓸 줄 아는 사람"에서 "만들 줄 아는 사람"으로 레벨업하는 것이다.
