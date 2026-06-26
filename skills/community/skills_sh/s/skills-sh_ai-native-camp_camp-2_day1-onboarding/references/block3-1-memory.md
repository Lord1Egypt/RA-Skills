# Block 3-1: Memory

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/memory
> 📖 기능을 목표에 맞추기: https://code.claude.com/docs/ko/features-overview#%EA%B8%B0%EB%8A%A5%EC%9D%84-%EB%AA%A9%ED%91%9C%EC%97%90-%EB%A7%9E%EC%B6%94%EA%B8%B0
> 📖 기능이 어떻게 로드되는지 이해하기: https://code.claude.com/docs/ko/features-overview#%EA%B8%B0%EB%8A%A5%EC%9D%B4-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%A1%9C%EB%93%9C%EB%90%98%EB%8A%94%EC%A7%80-%EC%9D%B4%ED%95%B4%ED%95%98%EA%B8%B0
> ```

> **Camp 2 변경점**: 1기에서는 CLAUDE.md만 다뤘지만, 그 사이 Auto Memory 기능이 새로 추가됐다. 2기에서는 CLAUDE.md와 Auto Memory를 함께 배운다. 내가 쓰는 지시문(CLAUDE.md)과 Claude가 스스로 기록하는 메모(Auto Memory) — 이 두 가지가 Claude의 기억 시스템이다.

## EXPLAIN

### 1. CLAUDE.md — 내가 쓰는 지시문

| 항목 | 내용 |
|------|------|
| 근본 원리 | **시스템 프롬프트** — AI가 대화를 시작할 때 가장 먼저 읽는 지시문. 매 세션마다 규칙을 주입하여 AI의 휘발성 기억을 영구 기억으로 만든다 |
| 비유 | 팀 위키 — Claude가 매 대화 시작할 때 읽는 규칙서 |
| 예시 | "항상 존댓말로", "표로 정리해줘", "내 이름은 OOO" |

```
세션 시작
  │
  ▼
┌─────────────┐     ┌─────────────┐
│ CLAUDE.md   │────▶│ 시스템       │────▶ Claude가 규칙을 아는 상태로 대화 시작
│ (내 지시문)  │     │ 프롬프트     │
└─────────────┘     └─────────────┘
  항상 읽힘            매번 자동 주입
```

### 2. Auto Memory — Claude가 스스로 적는 메모

| 항목 | 내용 |
|------|------|
| 근본 원리 | Claude가 작업하면서 발견한 패턴, 선호사항, 디버깅 인사이트를 **스스로 기록**한다. 다음 세션에서 자동으로 읽어서 이전 맥락을 이어간다 |
| 비유 | 업무 수첩 — Claude가 일하면서 적어두는 자기 노트 |
| CLAUDE.md와 차이 | CLAUDE.md는 **내가** Claude에게 주는 규칙. Auto Memory는 **Claude가** 스스로 적는 메모 |

```
세션 중 작업
  │
  ▼
┌─────────────────┐     ┌──────────────────────┐
│ Claude가 패턴    │────▶│ ~/.claude/projects/  │
│ 발견/학습        │     │   <project>/memory/  │
└─────────────────┘     │   ├── MEMORY.md      │
                        │   ├── debugging.md   │
  다음 세션 시작          │   └── patterns.md   │
  │                     └──────────────────────┘
  ▼                              │
┌─────────────┐                  │
│ MEMORY.md   │◀─────────────────┘
│ 자동 로드    │  (첫 200줄이 시스템 프롬프트에 주입)
└─────────────┘
```

**Auto Memory가 기록하는 것들:**

- **프로젝트 패턴**: 빌드 명령어, 테스트 방식, 코드 스타일
- **디버깅 인사이트**: 까다로운 문제의 해결법, 자주 나는 에러 원인
- **아키텍처 노트**: 핵심 파일, 모듈 관계, 중요한 추상화
- **내 선호사항**: 소통 방식, 워크플로우 습관, 도구 선택

**Auto Memory 관리:**

- 기본으로 켜져 있다 (따로 설정할 필요 없음)
- `/memory` 로 Auto Memory 토글 가능
- "이건 기억해둬", "pnpm 쓴다고 기억해" 같이 직접 지시해도 된다
- `~/.claude/projects/<프로젝트>/memory/` 에 마크다운 파일로 저장된다

## EXECUTE

3가지를 순서대로 실행하라고 안내한다:

**1. `/init` — CLAUDE.md 자동 생성**

```
/init
```

> 현재 폴더를 분석해서 CLAUDE.md를 자동으로 생성해준다. 프로젝트 구조, 기술 스택, 빌드 방법 등을 자동으로 파악해서 작성한다.

**2. `/memory` — 메모리 확인**

```
/memory
```

> CLAUDE.md와 Auto Memory 파일들을 확인하고 편집할 수 있다. Auto Memory 토글도 여기서 할 수 있다.

**3. Auto Memory 직접 체험**

Claude Code에 이렇게 말해본다:

```
나는 [이름]이고, [직업]이야. 이걸 기억해둬.
```

> Claude가 Auto Memory에 정보를 기록하는 것을 직접 확인해보자. `/memory` 로 저장된 내용을 열어볼 수 있다.

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "CLAUDE.md와 Auto Memory의 차이는?",
    "header": "Quiz 3-1",
    "options": [
      {"label": "CLAUDE.md는 내가 쓰고, Auto Memory는 Claude가 쓴다", "description": "각각 작성 주체가 다르다"},
      {"label": "같은 파일이다", "description": "이름만 다른 같은 기능"},
      {"label": "Auto Memory는 한 번만 읽힌다", "description": "매 세션마다 읽히는지 아닌지"}
    ],
    "multiSelect": false
  }]
})
```

정답: 1번. CLAUDE.md는 **내가 Claude에게 주는 지시문**이고, Auto Memory는 **Claude가 작업하면서 스스로 기록하는 메모**다. 둘 다 매 세션 시작 시 자동으로 읽힌다.
