# Block 6: Connector → Slack

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 참조: https://claude.ai/settings/connectors
> ```

## EXPLAIN

### 첫 번째 연결 방법: Connector

도구를 Claude에 연결하는 가장 쉬운 방법이다. **클릭 몇 번이면 끝난다.**

스마트폰에서 "Google로 로그인" 버튼 눌러본 적 있는가? Connector도 똑같다. 웹 브라우저에서 해당 서비스에 로그인만 하면 자동으로 연결된다.

```
Connector 연결 과정:

① https://claude.ai/settings/connectors 접속
② 연결하고 싶은 서비스 선택
③ 해당 서비스에 로그인
④ "허용" 클릭
⑤ 끝! Claude Code에서 바로 사용 가능
```

### Connector의 장점과 한계

| 장점 | 한계 |
|------|------|
| API 키가 필요 없다 | 지원하는 서비스가 정해져 있다 |
| 설정 파일을 건드릴 필요 없다 | 세밀한 설정이 어렵다 |
| 브라우저에서 클릭만 하면 된다 | 클라우드 기반이라 로컬 도구는 불가 |
| 연결 해제도 같은 페이지에서 클릭 한 번 | |

### `/mcp`에서 어떻게 보이는가?

Connector로 연결하면 `/mcp` 명령을 입력했을 때 **"claude.ai" 섹션**에 표시된다:

```
/mcp
→ claude.ai:
→   slack: connected (tools: 11)
→   notion: connected (tools: 8)
```

> 뒤에서 배울 `claude mcp add`로 연결하면 **"local" 섹션**에 표시된다. 위치가 다른 것뿐, 사용법은 같다.

### 오늘의 도구: Slack

Slack은 Connector를 지원하는 대표적인 도구다. 이번 블록에서 Slack을 Connector로 연결하고, 스킬의 소스 1을 채운다.

### Plan B: Slack이 없다면?

Slack을 사용하지 않는다면 이 블록을 skip하고 Block 7로 이동할 수 있다. 소스 1은 비워둔 채 다음 도구부터 연결하면 된다.

## EXECUTE

### Step 1: Slack 사용 여부 확인

```json
AskUserQuestion({
  "questions": [{
    "question": "Slack을 사용하고 계신가요?\n\n⚠️ 회사 Slack은 관리자 정책상 외부 앱 연결이 차단될 수 있습니다.",
    "header": "Slack 확인",
    "options": [
      {"label": "네, Slack 연결합니다", "description": "Connector로 Slack을 연결합니다"},
      {"label": "회사 계정이라 안 될 것 같아요", "description": "개인 Slack이나 AI Native Camp Slack으로 연결합니다"},
      {"label": "Slack 안 씁니다, skip할게요", "description": "이 블록을 건너뛰고 Block 7로 이동합니다"}
    ],
    "multiSelect": false
  }]
})
```

> **회사 계정 제한 시**: 개인 Slack workspace나 AI Native Camp Slack으로 연결하면 된다. Connector 연결 방식 자체를 체험하는 것이 이 블록의 핵심이다.

### Step 2: Connector로 Slack 연결

아래 과정을 안내한다:

```
① 브라우저에서 https://claude.ai/settings/connectors 에 접속하세요
② "Slack"을 찾아서 클릭하세요
③ Slack 워크스페이스에 로그인하세요
④ "허용(Allow)" 버튼을 클릭하세요
⑤ 완료!
```

### Step 3: 연결 확인 (`/mcp`)

터미널에서 연결 상태를 확인한다:

```
/mcp 입력

확인할 것:
→ claude.ai 섹션에 "slack: connected" 가 보이는지
→ tools 숫자가 표시되는지 (예: tools: 11)
```

### Step 4: 연결 테스트

실제로 Slack 도구가 작동하는지 간단히 테스트한다:

```
Claude에게 요청: "Slack 채널 목록 보여줘"

기대 결과:
  - Slack 워크스페이스의 채널 목록이 출력됨
  - 또는 특정 채널의 최근 메시지가 출력됨
```

> 테스트에서 에러가 발생하면 Connectors 페이지에서 연결을 해제했다가 다시 연결해본다.

### Step 5: 스킬 소스 1 채우기

테스트가 성공하면, `.claude/skills/my-context-sync/SKILL.md`의 **소스 1: Slack** 섹션을 채운다.

STUB을 실제 내용으로 교체:

```markdown
### 소스 1: Slack

| 항목 | 값 |
|------|-----|
| 연결 방법 | Connector (claude.ai/settings/connectors) |
| MCP 도구 | `mcp__claude_ai_Slack__slack_read_channel` |
| 수집 범위 | 최근 7일 |

수집할 채널 목록:
(테스트에서 확인한 실제 채널명으로 채운다)

수집 방법:
각 채널에 대해 mcp__claude_ai_Slack__slack_read_channel 호출.
  mcp__claude_ai_Slack__slack_read_channel(channel="general", limit=50)

추출할 정보:
- 중요 공지사항
- 의사결정 사항 ("확정", "결정", "합의" 키워드)
- 나에게 멘션된 메시지
- 답장이 필요한 질문
```

> 스킬 파일의 진행 상황:
> ```
> 소스 1: Slack     ✅ 채움!
> 소스 2: Notion    [STUB]
> 소스 3: Linear    [STUB]
> 소스 4: Google    [STUB]
> ```

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "Connector로 도구를 연결하면 /mcp에서 어느 섹션에 표시되나요?",
      "header": "Quiz 6-1",
      "options": [
        {"label": "local 섹션", "description": "local은 claude mcp add로 연결한 것"},
        {"label": "plugin 섹션", "description": "plugin은 /plugin으로 설치한 것"},
        {"label": "claude.ai 섹션", "description": "Connector는 claude.ai 클라우드를 통해 연결"}
      ],
      "multiSelect": false
    },
    {
      "question": "Connector의 가장 큰 장점은?",
      "header": "Quiz 6-2",
      "options": [
        {"label": "모든 도구를 연결할 수 있다", "description": "Connector가 지원하는 서비스만 가능"},
        {"label": "가장 빠르다", "description": "속도보다는 편의성이 핵심 장점"},
        {"label": "API 키 없이 브라우저 로그인만으로 연결된다", "description": "클릭 몇 번이면 끝나는 가장 쉬운 방법"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 6-1은 3번, Quiz 6-2는 3번.
- Connector로 연결하면 `/mcp`의 **claude.ai 섹션**에 표시된다. 뒤에서 배울 `claude mcp add`는 local 섹션에 표시된다.
- Connector의 최대 장점은 **API 키 없이 브라우저 로그인만으로** 연결된다는 것이다. 비개발자에게 가장 친절한 방법이다.
