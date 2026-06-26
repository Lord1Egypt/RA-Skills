# Block 3: Plugin 심화 + clarify:unknown 체험 + 과제

## EXPLAIN

### Part 1: Plugin Deep Dive (~15분)

#### Day 1 복습: Plugin이란

Day 1 Block 3-7에서 배웠다. Plugin은 **Skill + MCP + Hook + Agent를 하나의 설치 단위로 묶은 패키지**다.

```
개별 설치 (Plugin 없이)          Plugin (한 번에)
┌─────────┐                    ┌─────────────────┐
│ Skill A │ ← 수동 복사         │ clarify plugin  │
│ Skill B │ ← 수동 복사         │ ┌─ vague        │
│ MCP 설정 │ ← 수동 설정   vs   │ ├─ unknown      │
│ Hook 설정│ ← 수동 설정         │ └─ metamedium   │
│ Agent   │ ← 수동 설정         └────────┬────────┘
└─────────┘                             │
  팀원 각자 반복                  /plugin install clarify
                                   한 줄이면 끝
```

#### clarify 플러그인 해부

clarify 플러그인은 이렇게 구성되어 있다:

```
clarify/
├── .claude-plugin/
│   └── plugin.json          ← 플러그인의 신분증
│                               name, version, description,
│                               author, keywords 등
├── skills/
│   ├── vague/               ← 스킬 1: 요구사항 명확화
│   │   └── SKILL.md
│   ├── unknown/             ← 스킬 2: 전략 사각지대 분석
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── question-design.md
│   │       └── playbook-template.md
│   └── metamedium/          ← 스킬 3: 내용 vs 형식 관점 전환
│       ├── SKILL.md
│       └── references/
│           └── alan-kay-quotes.md
```

**plugin.json 핵심 필드:**

| 필드 | 값 | 역할 |
|------|-----|------|
| `name` | "clarify" | 설치/호출 시 사용하는 이름 |
| `version` | "2.0.0" | 버전 관리 |
| `description` | "Three lenses for clarity..." | 마켓플레이스에서 보이는 설명 |
| `keywords` | ["requirements", "strategy", ...] | 검색용 태그 |

**3개 스킬의 역할 차이:**

| 스킬 | 용도 | 핵심 도구 |
|------|------|----------|
| **vague** | 모호한 요구사항 → 구체적 스펙 | AskUserQuestion (5-8개 질문) |
| **unknown** | 전략의 사각지대 → 4분면 분석 | AskUserQuestion (R1→R2→R3, 7-10개 질문) |
| **metamedium** | 내용 vs 형식 → 관점 전환 | Alan Kay의 metamedium 개념 |

#### Plugin Marketplace 심화

Plugin은 Marketplace를 통해 배포된다.

```
┌─ 마켓플레이스 등록 ─────────────────────────────┐
│ /plugin marketplace add [owner/repo]             │
│ 예: /plugin marketplace add team-attention/...   │
└──────────────────────────────┬───────────────────┘
                               ↓
┌─ 플러그인 설치 ─────────────────────────────────┐
│ /plugin install [name]                           │
│ 예: /plugin install clarify                      │
└──────────────────────────────┬───────────────────┘
                               ↓
┌─ 설치된 플러그인 확인 ──────────────────────────┐
│ /plugin                                          │
│ → 설치된 모든 플러그인과 스킬 목록               │
└──────────────────────────────────────────────────┘
```

> 나중에 자신만의 플러그인을 만들어 마켓플레이스에 등록할 수도 있다. 오늘은 "사용하는 쪽"에 집중한다.

---

### Part 2: clarify:unknown 체험 (~15분)

#### Known/Unknown 4분면 프레임워크

vague가 "모호한 요구사항"을 다뤘다면, unknown은 **"전략의 사각지대"**를 다룬다.

```
              ┌─────────────────────────────────────┐
              │           내가 아는가?                │
              │       YES              NO            │
         ┌────┼──────────────┬──────────────────┐   │
   남들이│YES │  KK (60%)     │  KU (25%)         │   │
   아는가?│    │ 이미 아는 것  │ 모르는 줄 아는 것  │   │
         │    │ → 체계화      │ → 실험 설계        │   │
         ├────┼──────────────┼──────────────────┤   │
         │ NO │  UK (10%)     │  UU (5%)          │   │
         │    │ 갖고 있지만   │  모르는 줄도       │   │
         │    │ 활용 안 하는것│  모르는 것          │   │
         │    │ → 레버리지    │  → 안테나 설치     │   │
         └────┴──────────────┴──────────────────┘   │
              └─────────────────────────────────────┘
```

| 분면 | 이름 | 설명 | 전략 |
|------|------|------|------|
| **KK** | Known Knowns | 이미 알고 있고, 남들도 아는 것 | 체계화하여 효율 높이기 |
| **KU** | Known Unknowns | 모르는 줄 아는 것 (질문은 있지만 답이 없음) | 실험을 설계하여 답 찾기 |
| **UK** | Unknown Knowns | 갖고 있지만 활용하지 않는 자산 | 발굴하여 레버리지 |
| **UU** | Unknown Unknowns | 모르는 줄도 모르는 것 (사각지대) | 안테나를 설치하여 감지 |

#### 3-Round Depth Pattern

unknown 스킬은 3라운드에 걸쳐 점점 깊이 파고든다:

```
R1: 넓게 (3-4개 질문)     "대충 맞나요?"
  ↓ R1 답변 분석
R2: 집중 (2-3개 질문)     "여기가 약하네요, 더 파봅시다"
  ↓ R2 답변 분석
R3: 실행 (2-3개 질문)     "구체적으로 어떻게 할까요?" (선택)
```

**핵심**: R2 질문은 R1 답변에서 만든다. R3 질문은 R2 답변에서 만든다. 미리 준비한 질문을 쓰지 않는다.

## EXECUTE

### Part 1: Plugin 파일 탐색

설치된 clarify 플러그인의 실제 파일을 직접 확인해보자.

```
/plugin
```

> 설치된 플러그인 목록을 확인한다.

그 다음, Claude에게 플러그인 파일을 직접 읽어달라고 해보자:

```
clarify 플러그인의 plugin.json을 Read로 읽어줘
```

```
clarify 플러그인의 skills 폴더에 어떤 SKILL.md 파일들이 있는지 보여줘
```

> Plugin의 구조를 직접 눈으로 확인하는 것이 목표다.

### Part 2: clarify:unknown 체험

이제 clarify 플러그인의 두 번째 스킬, unknown을 사용해보자.

자신의 과제나 업무 전략에 대해 Known/Unknown 분석을 요청한다:

```
/clarify:unknown
```

또는:

```
내 [1주일 과제 / 업무 전략]에 대해 Known/Unknown 분석해줘
```

> R1 → R2 → R3 라운드를 거치면서, 자신이 "모르는 줄도 몰랐던 것"이 드러나는 경험을 한다.

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "Plugin의 핵심 파일은 무엇인가요?",
      "header": "Quiz 3-1",
      "options": [
        {"label": "plugin.json", "description": "플러그인의 이름, 버전, 설명 등 메타데이터를 담는 매니페스트 파일"},
        {"label": "SKILL.md", "description": "스킬의 본체이지만, 플러그인 전체를 정의하는 파일은 아님"},
        {"label": "CLAUDE.md", "description": "프로젝트 설정 파일이지, 플러그인의 핵심 파일은 아님"}
      ],
      "multiSelect": false
    },
    {
      "question": "clarify 플러그인에 포함된 스킬 개수는 몇 개인가요?",
      "header": "Quiz 3-2",
      "options": [
        {"label": "3개 (vague, unknown, metamedium)", "description": "요구사항 명확화, 전략 사각지대, 관점 전환"},
        {"label": "1개 (vague만)", "description": "unknown과 metamedium도 포함"},
        {"label": "2개 (vague, unknown)", "description": "metamedium도 있음"}
      ],
      "multiSelect": false
    },
    {
      "question": "vague와 unknown의 차이는 무엇인가요?",
      "header": "Quiz 3-3",
      "options": [
        {"label": "vague는 요구사항 명확화, unknown은 전략 사각지대 분석", "description": "vague=모호한 요청→스펙, unknown=전략→4분면 분석"},
        {"label": "vague는 쉬운 버전, unknown은 어려운 버전", "description": "난이도 차이가 아니라 목적이 다름"},
        {"label": "둘 다 같은 기능의 다른 이름", "description": "프로토콜과 출력 형식이 완전히 다름"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 3-1은 1번. **plugin.json**이 플러그인의 핵심 파일이다. 이름, 버전, 설명, 키워드 등 메타데이터를 담고 있어 마켓플레이스에서 검색/설치의 기준이 된다.

정답: Quiz 3-2는 1번. clarify 플러그인에는 **3개 스킬** (vague, unknown, metamedium)이 포함되어 있다.

정답: Quiz 3-3은 1번. **vague는 모호한 요구사항을 구체적 스펙으로** 바꾸고 (Phase 1-4), **unknown은 전략의 사각지대를 4분면으로 분석**한다 (R1→R2→R3). 목적이 다르기 때문에 프로토콜도 다르다.

---

## 과제 안내

Quiz 완료 후 아래 과제를 안내한다:

### Day 3 과제

> **1주일 과제 중 하나를 골라서, clarify를 시켜보세요.**

1. 1주일 과제 중 가장 모호한 부분을 하나 고른다
2. Claude에게 clarify를 요청한다 (직접 만든 my-clarify 스킬 또는 clarify:vague 플러그인 사용)
3. AskUserQuestion을 통한 질문에 답하면서, 요구사항이 구체화되는 과정을 경험한다

### Slack 공유 (#day3)

채널에 올릴 내용:

- **clarify 전**: 처음에 Claude에게 던진 요구사항 (원문 그대로)
- **clarify 후**: AskUserQuestion을 거친 뒤 구체화된 요구사항
- **가장 의외였던 질문**: Claude가 물어본 것 중 "아, 이걸 생각 못 했네" 싶었던 질문 1개

> 요구사항이 완벽하지 않아도 된다. "이 과정을 거치니까 내가 뭘 원하는지 더 알게 됐다"는 경험 자체가 핵심이다.
