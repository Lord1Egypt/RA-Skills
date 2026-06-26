# Block 8: Official Plugin → Linear

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 참조: https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins
> ```

## EXPLAIN

### 세 번째 연결 방법: Official Plugin (`/plugin`)

Block 6에서 Connector(클릭), Block 7에서 `claude mcp add`(명령어 한 줄)를 배웠다. 이번에는 **Plugin**이다.

Day 1 Block 3-5에서 Plugin을 잠깐 언급했다: "Skill + MCP + Hook + Agent를 묶은 패키지." 이번에 실제로 설치해본다.

### Plugin이 특별한 이유

Plugin을 설치하면 **MCP 서버가 자동으로 등록**된다. `claude mcp add`를 별도로 실행할 필요가 없다.

```
claude mcp add (Block 7):  명령어 실행 → MCP 서버 등록
/plugin install (이번 블록): 설치 한 줄 → MCP + 스킬 + 설정 전부 자동!
```

비유하면:
```
Connector (Block 6) = 블루투스 이어폰 (페어링만 하면 끝)
claude mcp add (Block 7) = 와이파이 공유기 (비밀번호 입력)
Plugin (이번 블록) = 스마트홈 패키지 (조명+스피커+센서 한 번에 설치)
```

### 3가지 연결 방법 비교 (여기까지 정리)

| 비교 | Connector | `claude mcp add` | Plugin |
|------|-----------|-----------------|--------|
| Block | 6 | 7 | **8 (지금)** |
| 도구 | Slack | Notion | **Linear** |
| 비유 | 블루투스 | 와이파이 | **스마트홈 패키지** |
| 난이도 | ★☆☆☆ | ★★☆☆ | **★★★☆** |
| MCP 등록 | 자동 (cloud) | 수동 (명령어) | **자동 (패키지)** |
| 설정 파일 | 없음 | `.mcp.json` | **`.mcp.json` 자동 생성** |
| 추가 기능 | MCP만 | MCP만 | **MCP + Skill + Hook + Agent** |
| `/mcp` 위치 | claude.ai 섹션 | local 섹션 | **local 섹션** |

> Plugin은 MCP만 연결하는 게 아니라, 스킬/훅/에이전트까지 한꺼번에 설치한다. 가장 많은 것을 한 번에 하는 방법이다.

### 오늘의 도구: Linear

Linear는 이슈 트래커다. 팀의 할 일(이슈)을 관리하는 도구로, 공식 Plugin이 제공된다.

### Plan B: Linear가 없다면?

Linear를 사용하지 않는다면, 다른 공식 Plugin으로 같은 체험을 할 수 있다:

1. `/plugin` 명령어를 실행하면 설치 가능한 Plugin 목록이 나온다
2. 자신이 사용하는 도구의 Plugin이 있으면 그것을 설치한다 (예: GitHub, Jira 등)
3. **어떤 Plugin이든 "설치 → MCP 자동 등록" 과정은 동일**하다
4. Plugin이 없으면 이 블록을 skip하고 Block 9로 이동할 수 있다

> ⚠️ 보안 안내: Plugin 설치 시 인증이 필요할 수 있다. 회사 계정이 제한될 경우 개인 계정이나 테스트 환경을 사용한다.

## EXECUTE

### Step 1: Linear 사용 여부 확인

```json
AskUserQuestion({
  "questions": [{
    "question": "Linear (이슈 트래커)를 사용하고 계신가요?",
    "header": "Linear 확인",
    "options": [
      {"label": "네, Linear 사용합니다", "description": "Linear Plugin을 설치합니다"},
      {"label": "아니요, 다른 Plugin으로 할게요", "description": "/plugin에서 다른 공식 Plugin을 찾습니다"},
      {"label": "Skip할게요", "description": "이 블록을 건너뛰고 Block 9로 이동합니다"}
    ],
    "multiSelect": false
  }]
})
```

> **Linear가 없어도 괜찮습니다.** 이 블록의 핵심은 "Plugin을 설치하면 MCP가 자동으로 등록된다"는 체험입니다. 다른 공식 Plugin으로도 같은 체험이 가능합니다.

### Step 2: `/plugin` 명령어로 Plugin 찾기

터미널에서 `/plugin`을 실행한다:

```
/plugin

→ 설치 가능한 플러그인 목록이 표시됨
→ Linear (또는 선택한 다른 Plugin)을 찾는다
```

### Step 3: Plugin 설치

```bash
/plugin install linear
```

설치가 완료되면 아래가 자동으로 처리된다:
- Plugin의 `.mcp.json`이 자동 활성화되어 Linear MCP 서버가 연결됨
- Linear 관련 스킬이 설치될 수 있음
- 필요한 설정이 자동으로 구성됨

> ⚠️ Plugin 설치 후 MCP 연결이 바로 안 보이면 **Claude Code를 재시작**해보세요.

### Step 4: `/mcp`로 자동 등록 확인

```
/mcp 입력

확인할 것:
→ local 섹션에 "linear" 가 자동으로 추가되었는지
→ "claude mcp add를 안 했는데 MCP가 등록됐다!" ← 이것이 Plugin의 힘

⚠️ 비교해보자:
   Block 6 (Connector): claude.ai 섹션 → slack
   Block 7 (mcp add):   local 섹션 → notion
   Block 8 (Plugin):    local 섹션 → linear (자동 등록!)
```

> 이것이 Plugin의 핵심 편의성이다. Plugin 안에 MCP 설정이 포함되어 있어서, 설치만 하면 MCP 서버가 자동으로 활성화된다.

### Step 5: 연결 테스트

```
Claude에게 요청: "Linear 이슈 목록 보여줘"

기대 결과:
  - Linear workspace의 이슈 목록이 출력됨
  - 나에게 할당된 이슈가 보임
```

> Linear 인증 화면이 나오면 로그인하고 "허용"을 클릭한다.

### Step 6: 스킬 소스 3 채우기

`.claude/skills/my-context-sync/SKILL.md`의 **소스 3: Linear** 섹션을 채운다.

```markdown
### 소스 3: Linear

| 항목 | 값 |
|------|-----|
| 연결 방법 | Official Plugin (`/plugin install linear`) |
| MCP 도구 | Linear Plugin이 등록한 MCP 도구 |
| 수집 범위 | 나에게 할당된 이슈 |

수집 방법:
Linear Plugin의 MCP 도구를 사용하여 이슈를 조회한다.
  (도구명은 /mcp에서 확인한 것으로 교체)

추출할 정보:
- 진행 중인 이슈
- 이번 주 마감 이슈
- 최근 댓글/업데이트
```

> 스킬 파일의 진행 상황:
> ```
> 소스 1: Slack     ✅ 채움!
> 소스 2: Notion    ✅ 채움!
> 소스 3: Linear    ✅ 채움!
> 소스 4: Google    [STUB]
> ```

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "Plugin을 설치하면 MCP 서버를 별도로 추가해야 하나요?",
      "header": "Quiz 8-1",
      "options": [
        {"label": "네, claude mcp add를 따로 실행해야 합니다", "description": "Plugin의 장점은 자동 등록"},
        {"label": "아니요, Plugin이 MCP를 자동으로 활성화합니다", "description": "/plugin install만 하면 MCP가 자동 연결"},
        {"label": "MCP와 Plugin은 관계없습니다", "description": "Plugin은 MCP를 포함하는 패키지"}
      ],
      "multiSelect": false
    },
    {
      "question": "Plugin이 다른 연결 방법보다 편한 이유는?",
      "header": "Quiz 8-2",
      "options": [
        {"label": "가장 빠르기 때문", "description": "속도보다는 '한 번에 다 되는' 편의성"},
        {"label": "무료이기 때문", "description": "다른 방법도 무료"},
        {"label": "MCP + 스킬 + 설정을 한꺼번에 설치하기 때문", "description": "스마트홈 패키지처럼 한 번에 모든 것이 설치됨"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 8-1은 2번, Quiz 8-2는 3번.
- Plugin을 설치하면 Plugin 안에 포함된 MCP 설정이 **자동으로 활성화**된다. `claude mcp add`를 별도로 실행할 필요가 없다. 이것이 Plugin의 가장 큰 편의성이다.
- Plugin이 편한 이유는 **MCP + 스킬 + 설정을 한꺼번에 설치**하기 때문이다. 스마트홈 패키지처럼 설치 한 줄이면 모든 것이 한 번에 구성된다.
