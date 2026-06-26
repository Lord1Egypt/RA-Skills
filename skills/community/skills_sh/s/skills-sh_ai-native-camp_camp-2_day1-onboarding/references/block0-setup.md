# Block 0: Setup

> Claude Code 설치는 이미 README의 Step 0에서 완료한 상태다.
> 이 블록에서는 첫 실행 설정과 에디터를 안내한다.

## EXPLAIN

> **Phase A 시작 시 반드시 아래 형태로 출력한다:**
> ```
> 📖 공식 문서: https://code.claude.com/docs/ko/setup
> 📖 빠른 시작: https://code.claude.com/docs/ko/quickstart
> ```

### 에디터 (선택사항)

Claude Code는 터미널에서 `claude`만 치면 된다. 하지만 파일을 눈으로 보면서 작업하고 싶다면 에디터를 설치할 수 있다:

| 에디터 | 특징 | 추천 대상 | 공식 사이트 |
|--------|------|-----------|-------------|
| [Antigravity](https://antigravity.google/) | 무료, AI 내장, 가장 간단 | 처음 시작하는 분 | antigravity.google |
| [Cursor](https://www.cursor.com/) | AI 내장, CC 시너지 | 코드 편집도 할 분 | cursor.com |
| [VSCode](https://code.visualstudio.com/) | 범용적, 확장 풍부 | 이미 쓰고 계신 분 | code.visualstudio.com |

> "이 캠프에서는 에디터 없이 터미널에서 `claude`만 쳐도 충분합니다. 에디터는 나중에 필요할 때 설치해도 됩니다."

### Mac 꿀팁: 숨겨진 폴더 보기

Mac에서는 `.`으로 시작하는 폴더(`.claude`, `.git` 등)가 기본적으로 안 보인다. Claude Code에게 시키면 된다:

```
Finder에서 .claude, .git 처럼 숨겨진 폴더도 볼 수 있게 설정해줘
```

설정이 끝나면 Finder로 직접 확인해보자:

```
open ./
```

> `.claude/skills/` 폴더 안에 지금 배우고 있는 교안이 들어있다! Finder에서 직접 눈으로 확인해보자.

### 첫 실행

터미널에 `claude` 한 글자를 입력하라고 안내한다. Anthropic 계정 로그인 + Claude 구독(Pro, Max, Teams, Enterprise) 연결을 확인시킨다.

### Output Style 설정

로그인이 끝나면 아래 순서로 Output Style을 설정하라고 안내한다:

1. Claude Code 대화창에 `/config` 입력
2. **Output style** 선택
3. **Explanatory** 선택

```
/config
→ Output style 선택
→ Explanatory 선택
```

> Explanatory 모드로 설정하면 Claude가 코드를 작성할 때 왜 그렇게 하는지 설명을 함께 해준다. 배우는 단계에서 가장 적합한 모드다.

## EXECUTE

참가자에게 순서대로 실행하라고 안내한다:

1. **첫 실행**: 터미널에서 `claude` 입력
2. **첫 대화**: "안녕, 나는 [이름]이고 [직업]이야. 나한테 인사해줘"
3. **자유 대화**: 5분간 자유롭게 대화

## QUIZ

```json
AskUserQuestion({
  "questions": [{
    "question": "설치와 첫 대화까지 완료했나요?",
    "header": "Setup 확인",
    "options": [
      {"label": "모두 완료!", "description": "Block 1로 이동"},
      {"label": "아직 진행 중", "description": "더 시간이 필요함"},
      {"label": "트러블슈팅 필요", "description": "설치나 실행에 문제 발생"}
    ],
    "multiSelect": false
  }]
})
```

> Block 0은 퀴즈 대신 완료 확인만 한다.
