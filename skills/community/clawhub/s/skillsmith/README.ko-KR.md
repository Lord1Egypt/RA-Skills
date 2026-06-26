# Skill Starter

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> OpenClaw 스킬 프로젝트를 빠르게 시작할 수 있도록 기본 구조와 보안 지향 템플릿을 생성하는 스캐폴딩 CLI입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-skill-starter` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + 프로젝트 생성기 |
| 템플릿 | `standard`, `strict-security` |

## 왜 필요한가

스킬의 첫 프로젝트 구조는 이후 품질을 크게 좌우합니다. Skill Starter는 `SKILL.md`, 테스트 스텁, 변경 로그, 예제 데이터, 선택형 CI 워크플로까지 포함한 기본 골격을 만들어 초기 품질을 안정적으로 맞출 수 있게 합니다.

## 생성되는 항목

- 정돈된 OpenClaw 스킬 프로젝트 구조
- frontmatter 와 안전 가이드가 포함된 `SKILL.md`
- `docs/`, `scripts/`, `.env.example`, `CHANGELOG.md`
- `tests/` 아래 smoke test 스캐폴드
- 프로파일링용 fixture 와 보조 스크립트
- 선택형 GitHub Actions 보안 스캔 워크플로
- 더 엄격한 템플릿에서 `.openclaw-tools/safe-install.policy.json`

## 대표 워크플로

1. 스킬 이름과 템플릿을 정합니다.
2. 프롬프트 방식 또는 무인자 방식으로 프로젝트를 생성합니다.
3. 실제 로직, 정책, 문서를 채웁니다.
4. 기본 smoke test 를 실행하고 이후 정식 lint/test 로 확장합니다.

## 빠른 시작

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-starter
npm install
node ./bin/create-openclaw-skill.js review-assistant --no-prompts --template strict-security --ci --out /tmp
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `create-openclaw-skill <name> [--template <standard|strict-security>] [--ci] [--no-prompts] [--force] [--out <dir>]` | 새 스킬 프로젝트 생성 |

## 생성 결과 예시

```text
<skill-name>/
├── SKILL.md
├── docs/README.md
├── scripts/README.md
├── fixtures/profile-input.json
├── tests/smoke.test.js
├── .env.example
└── CHANGELOG.md
```

## 템플릿 선택

| 템플릿 | 추천 상황 |
| --- | --- |
| `standard` | 빠른 내부 프로토타입과 범용 스킬 |
| `strict-security` | 더 강한 기본 보안값, CI 스캔, 정책 파일이 필요한 스킬 |

## 프로젝트 구조

```text
skill-starter/
├── bin/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

Skill Starter는 가볍지만 방향성이 분명한 도구입니다. 완전한 운영 시스템을 한 번에 만들기보다, 새 스킬을 빠르게 리뷰 가능한 형태로 올려놓는 데 집중합니다.
