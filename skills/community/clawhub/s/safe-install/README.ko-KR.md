# Safe Install

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> OpenClaw 스킬을 활성화하기 전에 스캔하고, 기록을 남기고, 롤백 가능한 스냅샷을 보관하는 보호형 설치 도구입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-safe-install` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + JavaScript 모듈 |
| 주요 명령 | 설치, `history`, `rollback`, `policy validate` |

## 왜 필요한가

스킬 설치는 단순 복사가 아니라 신뢰를 부여하는 작업입니다. Safe Install은 정책 검증, ClawShield 스캔, 설치 기록, 롤백 스냅샷 보관을 한 흐름으로 묶어 이 결정을 더 안전하게 만듭니다.

## 제공 기능

- 로컬 경로 또는 정책에 매핑된 registry 항목에서 스킬 소스 해석
- 작업 시작 전 정책 파일 검증
- ClawShield 기반 보안 스캔
- 정책과 위험도에 따른 차단 또는 허용 결정
- `.openclaw-tools/safe-install` 아래 스냅샷, 활성 상태, 이력 저장
- 이전 설치 스냅샷으로 롤백

## 대표 워크플로

1. 허용 소스와 차단 규칙을 담은 정책 파일을 준비합니다.
2. 로컬 경로나 이름 기반 스킬에 대해 Safe Install을 실행합니다.
3. 설치 후 이력과 활성 상태를 확인합니다.
4. 새 버전에 문제가 있으면 즉시 롤백합니다.

## 빠른 시작

Safe Install은 ClawShield에 의존합니다. 비공개 IndieSite 워크스페이스에서는 npm workspaces가 이 의존성을 이미 연결해 둡니다.

```bash
cd skills/openclaw/safe-install
node ./bin/safe-install.js ./fixtures/safe-skill --yes --format json
node ./bin/safe-install.js history --format table
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `safe-install <skill[@version]|local-path>` | 현재 정책에 따라 스캔 후 설치 |
| `safe-install history` | 설치 및 차단 이력 조회 |
| `safe-install rollback <skill>` | 이전 설치 스냅샷으로 복원 |
| `safe-install policy validate --file <path>` | 정책 JSON 파일 검증 |

## 정책 모델

Safe Install은 사용자 설정을 아래 기본값과 병합합니다.

```json
{
  "defaultAction": "prompt",
  "blockedPatterns": [],
  "allowedSources": [],
  "forceRequiredForAvoid": true
}
```

## 저장되는 항목

- `snapshots/<skill>/<version>/<hash>`: 롤백용 스냅샷
- `active/<skill>`: 현재 활성 버전
- `history.json`: 설치 및 차단 이력
- `state.json`: 현재 활성 상태 맵

## 프로젝트 구조

```text
safe-install/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

현재 구현은 로컬 경로 설치, 정책 검증, 스캔 기반 의사결정, 이력 관리, 롤백에 초점을 맞춥니다. 완전한 원격 registry 클라이언트라기보다 더 안전한 설치 제어 계층에 가깝습니다.
