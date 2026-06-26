# ClawShield

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 설치 전에 OpenClaw 스킬을 정적으로 검사해 위험한 셸 패턴, 수상한 콜백, 사회공학성 지시를 찾아내는 보안 스캐너입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-clawshield` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + JavaScript 모듈 |
| 주요 명령 | `scan` |

## 왜 필요한가

스킬 마켓과 내부 저장소 모두 공급망 위험을 만듭니다. ClawShield는 코드를 실행하지 않고 파일을 스캔하여 위험을 먼저 드러내고, 그 결과를 CI 또는 설치 단계에서 강제할 수 있도록 설계되었습니다.

## 무엇을 탐지하나

- `curl | sh` 같은 다운로드 후 즉시 실행 패턴
- `eval()` 과 base64 디코드 흐름 같은 난독화 또는 동적 실행
- 신뢰되지 않는 외부 엔드포인트로 향하는 수상한 콜백
- 사용자가 안전 장치를 우회하도록 유도하는 사회공학성 문구
- 원격 실행을 감추는 셸 래퍼 패턴

## 대표 워크플로

1. 스킬 디렉터리를 대상으로 스캔합니다.
2. 위험도와 상세 findings 를 검토합니다.
3. 필요하면 JSON 또는 SARIF 를 내보냅니다.
4. `--fail-on caution|avoid` 로 CI 차단 조건을 설정합니다.

## 빠른 시작

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/clawshield
npm install
node ./bin/clawshield.js scan ./fixtures/malicious-skill --format table --fail-on caution
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `clawshield scan <skill-path> --format <table|json|sarif> --fail-on <caution|avoid> [--suppressions <path>]` | 스킬을 스캔하고 지정한 위험도 이상이면 실패 처리 |

## 위험도 모델

| 위험도 | 의미 |
| --- | --- |
| `Safe` | suppression 적용 후 남은 문제 없음 |
| `Caution` | 사람이 검토해야 하는 중간 수준 문제 존재 |
| `Avoid` | 실질적 위험을 의미하는 높은 수준의 문제 존재 |

## Suppressions

ClawShield는 rule ID, 파일 경로, 줄 번호, justification 을 담은 `.clawshield-suppressions.json` 을 지원합니다. justification 이 없는 항목은 무시됩니다.

## 프로젝트 구조

```text
clawshield/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

현재 규칙 세트는 의도적으로 좁고 실용적입니다. 로컬 리뷰, CI 게이트, Safe Install 같은 상위 도구에서 바로 효용이 있는 고신호 패턴에 집중합니다.
