# Block 2: 나만의 Clarify 스킬 만들기

## EXPLAIN

### 플러그인 스킬을 해부한다

Block 1에서 clarify:vague를 체험했다. 이제 그 스킬이 **어떻게 만들어져 있는지** 직접 열어보자.

Claude에게 이렇게 요청한다:

```
clarify 플러그인의 vague SKILL.md를 Read로 읽어줘
```

> Claude가 Read 도구로 설치된 플러그인의 SKILL.md 파일을 열어서 보여줄 것이다.

### SKILL.md의 구조

vague SKILL.md를 열어보면 이런 구조로 되어 있다:

```
---
name: vague                          ← 스킬 이름
description: ...trigger on...         ← 언제 이 스킬이 호출되는지
---

# Vague: Requirement Clarification   ← 제목

## When to Use                        ← 사용 상황
## Core Principle                     ← 핵심 원칙 (Hypothesis-as-Options)
## Protocol                           ← 실행 프로토콜
  ### Phase 1: Capture                ←   1단계: 캡처
  ### Phase 2: Iterate                ←   2단계: 반복 질문
  ### Phase 3: Before/After           ←   3단계: 전후 비교
  ### Phase 4: Save                   ←   4단계: 저장
## Ambiguity Categories              ← 모호함 분류표
## Rules                              ← 규칙
```

### 나만의 버전을 만든다

이 구조를 기반으로, **자신의 업무에 맞는 Clarify 스킬**을 만들어보자.

뭘 바꿀 수 있나?

| 커스터마이즈 포인트 | 원본 | 자기 버전 예시 |
|-------------------|------|--------------|
| **트리거 키워드** | "clarify", "spec this out" | "기획 정리", "요구사항 뽀개기" |
| **사용 상황** | 기능 요청, 버그 리포트 | 마케팅 캠페인, 콘텐츠 기획 |
| **모호함 카테고리** | Scope, Behavior, Interface... | 대상, 톤앤매너, 채널, 기한... |
| **질문 개수** | 5-8개 | 3-5개 (업무가 단순하면) |
| **Before/After 포맷** | Goal, Scope, Constraints | 목표, 대상, 메시지, KPI |

### 6단계 작성 가이드

1. **Read**: 플러그인의 vague SKILL.md를 읽어서 구조를 파악한다
2. **Copy**: 이 스킬의 `templates/clarify-vague.md` 템플릿을 가져온다
3. **Customize**: `<!-- CUSTOMIZE -->` 주석이 있는 부분을 자기 업무에 맞게 수정한다
4. **Save**: `.claude/skills/my-clarify/SKILL.md`로 저장한다
5. **Test**: 저장 후 새 세션에서 트리거 키워드로 호출해본다
6. **Iterate**: 써보면서 질문/카테고리를 계속 다듬는다

## EXECUTE

나만의 Clarify 스킬을 직접 만들어보자.

### 1단계: 플러그인 스킬 분석

먼저 원본을 분석한다. Claude에게 이렇게 요청한다:

```
clarify 플러그인의 vague SKILL.md를 Read로 읽어서 구조를 분석해줘
```

### 2단계: 템플릿 기반으로 작성

이 스킬의 `templates/clarify-vague.md`를 기반으로 자신만의 버전을 만든다:

```
templates/clarify-vague.md를 Read로 읽어서 보여줘.
이 템플릿을 기반으로 내 업무([자신의 업무 설명])에 맞는 clarify 스킬을 만들어줘.
.claude/skills/my-clarify/SKILL.md에 저장해줘.
```

> `<!-- CUSTOMIZE -->` 주석이 있는 부분을 꼭 자기 상황에 맞게 바꿔야 한다.
> 그대로 복사하면 의미가 없다.

### 3단계: 테스트

저장이 되었으면 바로 테스트해보자:

```
내가 만든 my-clarify 스킬로 [모호한 요구사항]을 clarify해줘
```

> 잘 동작하는지 확인한다. 질문이 자기 업무에 맞게 나오는지, Before/After가 유용한지 체크한다.

## QUIZ

```json
AskUserQuestion({
  "questions": [
    {
      "question": "SKILL.md의 Protocol에서 Phase 2의 핵심은 무엇인가요?",
      "header": "Quiz 2-1",
      "options": [
        {"label": "AskUserQuestion으로 가설 기반 질문을 반복한다", "description": "최대 4개씩 묶어서, 5-8개 상한"},
        {"label": "사용자에게 자유롭게 설명하게 한다", "description": "열린 질문은 Hypothesis-as-Options 위반"},
        {"label": "Claude가 알아서 결정한다", "description": "가정하지 않는 것이 규칙"}
      ],
      "multiSelect": false
    },
    {
      "question": "Phase 3에서 반드시 보여줘야 하는 것은 무엇인가요?",
      "header": "Quiz 2-2",
      "options": [
        {"label": "Before/After — 원본과 구체화된 요구사항의 비교", "description": "변환 과정을 시각화하여 확인"},
        {"label": "질문 목록만 나열", "description": "질문보다 결과(변환된 스펙)가 중요"},
        {"label": "실행 코드", "description": "Clarify는 스펙을 만드는 과정, 코드는 그 다음"}
      ],
      "multiSelect": false
    }
  ]
})
```

정답: Quiz 2-1은 1번. Phase 2의 핵심은 **AskUserQuestion으로 가설 기반 질문을 반복**하는 것이다. 관련 질문을 최대 4개씩 묶어서 효율적으로 물어본다.

정답: Quiz 2-2는 1번. Phase 3의 핵심은 **Before/After 비교**다. 원래 모호했던 요구사항과 clarify 후 구체화된 스펙을 나란히 보여줘야 한다. 이 비교가 있어야 "이 과정이 의미 있었다"는 걸 실감할 수 있다.
