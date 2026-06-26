# Block 7: `claude mcp add` → Notion

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/mcp
> 📖 참조: https://mcp.notion.com
> ```

## EXPLAIN

### 두 번째 연결 방법: `claude mcp add`

Block 6에서는 Connector로 연결했다. 클릭 몇 번이면 끝나는 가장 쉬운 방법이었다.

하지만 Connector에 원하는 서비스가 없을 수도 있다. 그럴 때 쓰는 것이 **`claude mcp add` 명령어**다. 터미널에 한 줄 입력하면 MCP 서버가 등록된다.

```
Connector:      브라우저에서 클릭 → 자동 연결 (블루투스 자동 페어링)
claude mcp add: 터미널에 명령어 입력 → 수동 연결 (와이파이 비밀번호 입력)
```

### Connector vs `claude mcp add` 비교

| 비교 | Connector (Block 6) | `claude mcp add` (이번 블록) |
|------|---------------------|--------------------------|
| 비유 | 블루투스 자동 연결 | 와이파이 비밀번호 입력 |
| 난이도 | ★☆☆☆ (클릭만) | ★★☆☆ (명령어 한 줄) |
| `/mcp` 위치 | claude.ai 섹션 | **local 섹션** |
| 설정 파일 | 필요 없음 | `.mcp.json` 자동 생성 |
| 지원 범위 | 정해진 서비스만 | HTTP MCP 서버가 있는 모든 도구 |

### `.mcp.json`이란?

`claude mcp add` 명령어를 실행하면 프로젝트 루트에 `.mcp.json` 파일이 자동으로 만들어진다.

```
내 프로젝트/
├── .mcp.json          <-- MCP 서버 설정 파일 (여기!)
├── .claude/
│   └── skills/
│       └── my-context-sync/
└── ...
```

파일 안에는 "어떤 서버를, 어떻게 연결할지"가 적혀 있다:

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

> 대부분 Claude가 알아서 만들어주므로 직접 수정할 일은 거의 없다. 하지만 구조를 알아두면 나중에 Plugin을 이해할 때 도움이 된다.

### 오늘의 도구: Notion

Notion은 공식 HTTP MCP 서버(`https://mcp.notion.com/mcp`)를 제공한다. `claude mcp add` 한 줄이면 연결된다.

### Plan B: Notion이 없다면?

Notion을 사용하지 않는다면, Claude가 대체 MCP 서버를 검색해준다. "다른 도구를 연결하고 싶어요"라고 말하면 Claude가 `scripts/mcp_servers.py`를 실행하여 사용 가능한 MCP 서버를 찾아준다.

검색 결과에서 적합한 서버를 찾아 `claude mcp add`로 등록하면 된다.

> ⚠️ 보안 안내: MCP 서버에 연결하면 해당 서비스의 데이터에 Claude가 접근할 수 있다. 회사 데이터가 포함된 서비스는 개인 workspace나 테스트 환경으로 연결하는 것을 권장한다.

## EXECUTE

### Step 1: Notion 사용 여부 확인

```json
AskUserQuestion({
  "questions": [{
    "question": "Notion을 사용하고 계신가요?",
    "header": "Notion 확인",
    "options": [
      {"label": "네, Notion 사용합니다", "description": "Notion MCP 서버로 연결합니다"},
      {"label": "아니요, 다른 도구로 할게요", "description": "mcp_servers.py로 대체 서버를 검색합니다"}
    ],
    "multiSelect": false
  }]
})
```

### Step 2: MCP 서버 등록

**Notion을 사용하는 경우:**

Claude가 아래 명령어를 실행한다:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

명령어 해부:
```
claude mcp add          ← "MCP 서버를 추가해줘"
  --transport http      ← "클라우드 웹 서버야" (로컬이 아님)
  notion                ← "이름은 notion으로 해줘"
  https://mcp.notion.com/mcp  ← "이 주소로 연결해줘"
```

**다른 도구를 선택한 경우:**

Claude가 `scripts/mcp_servers.py`를 실행하여 대체 MCP 서버를 검색한다. 사용자가 원하는 도구명을 말하면 Claude가 알아서 검색하고, 적합한 서버를 찾아 `claude mcp add`로 등록한다.

> ⚠️ 보안 안내: 연결 시 브라우저에서 해당 서비스의 인증 페이지가 열릴 수 있다. 회사 데이터가 있는 서비스는 개인 workspace나 테스트 환경 사용을 권장한다.

### Step 3: 연결 확인 (`/mcp`)

```
/mcp 입력

확인할 것:
→ local 섹션에 "notion" 이 보이는지
→ connected 상태인지
→ 도구(tools) 숫자가 표시되는지

⚠️ Block 6의 Connector는 "claude.ai" 섹션에 있었다.
   이번에는 "local" 섹션에 있는 것을 확인하자!
```

> Notion 연결 시 브라우저에서 Notion 인증 페이지가 열릴 수 있다. 로그인하고 "허용"을 클릭하면 된다.

### Step 4: 연결 테스트

```
Claude에게 요청: "Notion에서 최근 수정된 페이지 보여줘"

기대 결과:
  - Notion workspace의 페이지 목록이 출력됨
  - 또는 특정 데이터베이스의 항목이 출력됨
```

### Step 5: 스킬 소스 2 채우기

`.claude/skills/my-context-sync/SKILL.md`의 **소스 2: Notion** 섹션을 채운다.

```markdown
### 소스 2: Notion

| 항목 | 값 |
|------|-----|
| 연결 방법 | `claude mcp add --transport http` |
| MCP 서버 | `https://mcp.notion.com/mcp` |
| 수집 범위 | 지정된 데이터베이스 |

databases:
  - name: "{사용자 DB명}"
    id: "{실제 DB ID}"

수집 방법:
Notion MCP 서버의 도구를 사용하여 데이터베이스를 조회한다.
  mcp__notion__search(query="")
  mcp__notion__query_database(database_id="{id}")

추출할 정보:
- 진행 중인 태스크
- 기한이 임박한 항목
- 최근 업데이트된 페이지
```

> 스킬 파일의 진행 상황:
> ```
> 소스 1: Slack     ✅ 채움!
> 소스 2: Notion    ✅ 채움!
> 소스 3: Linear    [STUB]
> 소스 4: Google    [STUB]
> ```

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "`claude mcp add --transport http` 에서 `--transport http`의 의미는?",
      "header": "Quiz 7-1",
      "options": [
        {"label": "보안 연결이라는 뜻", "description": "보안과는 다른 개념"},
        {"label": "로컬 컴퓨터에서 실행한다는 뜻", "description": "로컬 실행은 stdio 방식"},
        {"label": "클라우드 웹 서버에 연결한다는 뜻", "description": "HTTP = 인터넷을 통한 원격 연결"}
      ],
      "multiSelect": false
    },
    {
      "question": "`claude mcp add` 명령어를 실행하면 어떤 파일이 자동으로 생성되나요?",
      "header": "Quiz 7-2",
      "options": [
        {"label": "CLAUDE.md", "description": "CLAUDE.md는 Claude의 지시사항 파일"},
        {"label": ".mcp.json", "description": "프로젝트 루트에 MCP 서버 설정이 저장됨"},
        {"label": "SKILL.md", "description": "SKILL.md는 스킬 정의 파일"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 7-1은 3번, Quiz 7-2는 2번.
- `--transport http`는 **클라우드 웹 서버에 연결**한다는 뜻이다. 인터넷을 통해 원격 MCP 서버에 접속한다. (로컬 실행은 `stdio` 방식)
- `claude mcp add` 명령어를 실행하면 프로젝트 루트에 **`.mcp.json`** 파일이 자동으로 생성/업데이트된다. 어떤 서버를 어떻게 연결할지 적어놓는 설정 파일이다.
