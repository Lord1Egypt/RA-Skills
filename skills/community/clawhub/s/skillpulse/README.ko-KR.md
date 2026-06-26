# Skill Profiler

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> OpenClaw 스킬 실행 샘플을 분석해 병목 구간을 빠르게 찾아주는 프로파일링 CLI입니다.

| 항목 | 내용 |
| --- | --- |
| 패키지 | `@mike007jd/openclaw-skill-profiler` |
| 런타임 | Node.js 18+ |
| 인터페이스 | CLI + JavaScript 모듈 |
| 주요 명령 | `run`, `report`, `compare` |

## 왜 필요한가

OpenClaw 워크플로는 겉으로는 정상처럼 보여도 특정 스킬 하나가 tail latency, CPU 사용량, 메모리 피크를 끌어올리면서 전체 체인을 느리게 만들 수 있습니다. Skill Profiler는 샘플 로그를 빠르게 집계해 이런 문제를 릴리스 전에 확인할 수 있게 합니다.

## 제공 기능

- JSON 샘플 배열에서 `latencyMs`, `cpuMs`, `memoryMb` 집계
- 스킬별 평균 지연 시간, p95 지연 시간, 평균 CPU, 최대 메모리 계산
- 사용자 지정 임계값 기반 병목 감지
- 공유 가능한 JSON 또는 HTML 보고서 생성
- 두 세션을 비교해 추가, 제거, 변경된 스킬 표시

## 대표 워크플로

1. 실행 샘플을 JSON 배열로 준비합니다.
2. `skill-profiler run` 으로 병목을 빠르게 확인합니다.
3. `skill-profiler report` 로 공식 보고서를 저장합니다.
4. `skill-profiler compare` 로 개선 전후를 비교합니다.

## 빠른 시작

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-profiler
npm install
node ./bin/skill-profiler.js run --input ./fixtures/samples-a.json
```

## 명령어

| 명령 | 설명 |
| --- | --- |
| `skill-profiler run --input <samples.json>` | 단일 샘플 세트를 분석하고 병목 여부에 따라 `0` 또는 `2` 반환 |
| `skill-profiler report --input <samples.json> --out <file>` | JSON 또는 HTML 보고서 생성 |
| `skill-profiler compare --left <samples.json> --right <samples.json>` | 두 프로파일 스냅샷 비교 |

## 예시 입력

```json
[
  {
    "sessionId": "s1",
    "skill": "clawshield",
    "latencyMs": 1320,
    "cpuMs": 910,
    "memoryMb": 240
  }
]
```

## 출력에서 확인할 점

- `run` 은 요약 테이블 또는 JSON envelope 를 출력하고 임계값 초과 시 종료 코드 `2` 를 반환합니다
- `report` 는 대시보드, 리뷰, 인수인계를 위한 아티팩트를 생성합니다
- `compare` 는 회귀, 개선, 신규/삭제 스킬을 빠르게 드러냅니다

## 프로젝트 구조

```text
skill-profiler/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 현재 상태

현재 구현은 실시간 트레이싱보다 오프라인 샘플 분석에 맞춰져 있습니다. 임계값 기반 병목 감지, 보고서 생성, 세션 비교는 이미 포함되어 있습니다.
