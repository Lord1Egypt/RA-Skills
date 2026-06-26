# Self-Evolving Agent v4.1 — 통합 기능 가이드

> **v4.1 신규 기능:** 대화형 승인, 멀티포맷 리포트 내보내기, GitHub Issues 통합

---

## 목차

1. [대화형 승인 (interactive-approve.sh)](#1-대화형-승인)
2. [sea watch 커맨드](#2-sea-watch)
3. [멀티포맷 리포트 내보내기 (export-report.sh)](#3-리포트-내보내기)
4. [GitHub Issues 통합 (github-issue.sh)](#4-github-issues-통합)
5. [설정 (config.yaml)](#5-설정)
6. [전체 워크플로우](#6-전체-워크플로우)

---

## 1. 대화형 승인

**파일:** `scripts/v4/interactive-approve.sh`

v4.1부터 제안 전달 시 Discord/Telegram에 인터랙티브 승인 지시가 자동으로 포함됩니다.

### Discord 리액션 지시

`synthesize-proposal.sh` 실행 후 proposal.md 끝에 자동 추가:

```
## 💬 승인 방법

> ✅ 리액션 → 승인 (자동으로 `sea approve` 실행)
> ❌ 리액션 → 거부
> 🔍 리액션 → diff 전체 보기 (스레드로 확장)
```

> **참고:** Discord 리액션을 실제로 감지해서 `sea approve`를 자동 실행하려면
> OpenClaw heartbeat에서 최근 리액션을 폴링하는 로직이 필요합니다.
> 현재는 사용자에게 수동 명령을 안내하는 방식입니다.

### Telegram 인라인 버튼

Telegram으로 제안을 전송할 때 인라인 버튼 포함:

```bash
# 버튼 포함 Telegram 전송
bash scripts/v4/interactive-approve.sh --send-telegram "제안 내용" "prop-20260218-001"
```

버튼 구성:
- **✅ 승인** — callback_data: `sea_approve:prop-20260218-001`
- **❌ 거부** — callback_data: `sea_reject:prop-20260218-001`
- **🔍 diff** — callback_data: `sea_diff:prop-20260218-001`

> Telegram 버튼 클릭 콜백을 처리하려면 Telegram webhook 또는 long-polling 서버가 필요합니다.
> 콜백 처리 시 `sea approve <id>` 또는 `sea reject <id> "이유"` 실행.

### 직접 사용법

```bash
# 특정 제안 파일 알림 + 터미널 대화형 승인
bash scripts/v4/interactive-approve.sh --notify data/proposals/proposal-20260218.json

# Discord 리액션 지시 푸터만 출력
bash scripts/v4/interactive-approve.sh --discord-footer

# Telegram 버튼 JSON 출력
bash scripts/v4/interactive-approve.sh --telegram-buttons prop-20260218-001
```

---

## 2. sea watch

`sea watch`는 30초마다 새 제안을 감지하여 macOS 데스크탑 알림을 띄우고,
터미널에서 대화형으로 승인/거부할 수 있게 해줍니다.

### 사용법

```bash
sea watch                   # 30초 간격 (기본)
sea watch --interval 60     # 60초 간격

# 또는 직접
bash scripts/v4/interactive-approve.sh --watch
```

### 동작 흐름

```
1. 시작 시 기존 미처리 (pending) 제안 목록 표시
2. 각 제안에 대해 macOS 알림 + 터미널 프롬프트
3. [a] 승인 → sea approve <id> 자동 실행
   [r] 거부 → 이유 입력 → sea reject <id> 자동 실행
   [s] 건너뜀
4. 30초 대기 후 새 제안 감지 (새로 생성된 .json 파일)
5. Ctrl+C로 종료
```

### macOS 알림 예시

```
[알림] 🧠 새 제안 도착 (high)
       AGENTS.md exec 재시도 규칙 강화
```

### 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SEA_WATCH_INTERVAL` | `30` | 폴링 간격 (초) |
| `SEA_NOTIFY_SOUND` | `on` | macOS 알림 소리 on/off |

---

## 3. 리포트 내보내기

**파일:** `scripts/v4/export-report.sh`

주간 제안 리포트를 4가지 형식으로 내보냅니다.

### 사용법

```bash
# sea CLI (권장)
sea export                                    # Markdown stdout
sea export --format html                      # HTML stdout
sea export --format html --output report.html # HTML 파일 저장
sea export --format json --output report.json
sea export --format pdf  --output report.pdf
sea export --format all  --output-dir ./reports/

# 직접 실행
bash scripts/v4/export-report.sh --format html --output ~/sea-report.html
```

### 형식별 특징

| 형식 | 의존성 | 설명 |
|------|--------|------|
| `markdown` | 없음 | 기본 형식, proposal.md 그대로 출력 |
| `html` | python3 (내장) 또는 pandoc | GitHub 다크 테마 스타일 포함 |
| `json` | python3 | API 소비용 구조화 데이터 |
| `pdf` | pandoc + wkhtmltopdf 또는 pdflatex | 인쇄/아카이브용 |
| `all` | 위 조합 | 모든 형식 한 번에 출력 디렉토리에 저장 |

### JSON 출력 구조

```json
{
  "meta": {
    "title": "Self-Evolving Agent 주간 리포트",
    "generated_at": "2026-02-18T01:00:00+09:00",
    "version": "4.1",
    "source": "self-evolving-agent"
  },
  "summary": {
    "total": 5,
    "pending": 2,
    "applied": 2,
    "rejected": 1,
    "by_severity": {
      "critical": 0,
      "high": 1,
      "medium": 3,
      "low": 1
    }
  },
  "proposals": [ ... ]
}
```

### PDF 설치 (선택)

```bash
# macOS
brew install pandoc
brew install wkhtmltopdf

# 한국어 폰트 (pdflatex 사용 시)
brew install --cask mactex
```

---

## 4. GitHub Issues 통합

**파일:** `scripts/v4/github-issue.sh`

각 제안을 GitHub Issue로 추적합니다.
승인 시 자동으로 이슈가 종료되며, before/after diff가 본문에 포함됩니다.

### 사전 준비

```bash
# 1. GitHub PAT 발급 (repo 권한 필요)
#    Settings → Developer settings → Personal access tokens

# 2. 환경변수 설정
export GH_TOKEN=ghp_your_token_here
export GH_REPO=owner/repo     # 선택 (git remote에서 자동 감지 가능)
```

### 사용법

```bash
# sea CLI (권장)
sea github create data/proposals/proposal-20260218.json   # 단일 이슈 생성
sea github create --all                                    # 모든 pending 이슈 생성
sea github close prop-20260218-001                        # 이슈 종료
sea github sync                                           # 양방향 동기화
sea github list                                           # 이슈 목록
sea github labels                                         # 레이블 초기화

# 직접 실행
GH_TOKEN=ghp_xxx bash scripts/v4/github-issue.sh create --all
```

### 자동 레이블

초기화 시 자동 생성되는 레이블:

| 레이블 | 색상 | 용도 |
|--------|------|------|
| `self-evolving` | 파랑 | 모든 SEA 이슈 |
| `agent-proposal` | 보라 | 자동 생성 제안 |
| `severity:critical` | 빨강 | 즉시 적용 필요 |
| `severity:high` | 노랑 | 높은 우선순위 |
| `severity:medium` | 황금 | 보통 우선순위 |
| `severity:low` | 초록 | 낮은 우선순위 |
| `status:pending-review` | 주황 | 승인 대기 |
| `status:approved` | 초록 | 승인됨 |
| `status:rejected` | 노랑 | 거부됨 |

### 이슈 본문 예시

```markdown
## 🤖 Self-Evolving Agent — 자동 생성 제안

> 이 이슈는 Self-Evolving Agent v4.1이 자동 생성했습니다.
> 승인: `sea approve prop-20260218-001`

---

### 메타데이터

| 항목 | 값 |
|------|----|
| **ID** | `prop-20260218-001` |
| **심각도** | 🔴 high |
| **대상 섹션** | AGENTS.md exec 규칙 |

---

### 📋 근거

```
exec 재시도 이벤트: 45건 (지난 7일)
```

### 🔴 Before

```
exec 실패 시 그냥 진행
```

### 🟢 After

```
exec 실패 시 || true 패턴 필수
```
```

### sea approve와의 통합

`GH_TOKEN`이 설정된 경우, `sea approve <id>` 실행 시 자동으로 해당 GitHub Issue가 종료됩니다:

```bash
sea approve prop-20260218-001
# → AGENTS.md 패치
# → git commit
# → GitHub Issue #42 자동 종료 + 승인 코멘트
```

### 동기화 모드

```bash
sea github sync
# → pending 제안 중 이슈 없는 것: 이슈 생성
# → applied 제안 중 열린 이슈 있는 것: 이슈 종료
# 출력: 동기화 완료: 생성=2, 건너뜀=1, 종료=1
```

---

## 5. 설정

`config.yaml`에서 모든 통합 기능을 설정합니다:

```yaml
# GitHub 통합
github:
  token: ""                    # 또는 환경변수 GH_TOKEN
  repo: ""                     # 자동 감지 또는 "owner/repo"
  assignee: ""                 # 기본: 레포 소유자
  auto_create_issues: false    # 제안 생성 시 자동 이슈 생성
  auto_close_on_approve: true  # 승인 시 자동 이슈 종료

# 대화형 승인
interactive:
  watch_interval: 30           # sea watch 폴링 간격 (초)
  notify_sound: "on"           # macOS 알림 소리
  telegram_buttons: false      # Telegram 인라인 버튼

# 리포트 내보내기
export:
  output_dir: ""               # 기본 출력 디렉토리
  title: "Self-Evolving Agent 주간 리포트"
  prefer_pandoc: true          # HTML 생성 시 pandoc 우선
```

---

## 6. 전체 워크플로우

### 권장 주간 워크플로우

```
일요일 22:00 (자동 크론)
  ↓
orchestrator.sh
  → Stage 1~5: 분석 → 합성
  → proposal.md 생성 (Discord 리액션 지시 포함)
  → Discord 전송
  ↓
사용자 (월요일)
  옵션 A: sea watch (터미널 대화형)
  옵션 B: Discord에서 직접 sea approve/reject
  옵션 C: GitHub Issue에서 검토 후 승인
  ↓
sea approve <id>
  → AGENTS.md 패치
  → git commit
  → GitHub Issue 자동 종료 (GH_TOKEN 있을 때)
  ↓
다음 주 효과 측정 (measure-effects.sh)
```

### 첫 설정 체크리스트

```bash
# 1. GitHub 연동 (선택)
export GH_TOKEN=ghp_your_token
sea github labels          # 레이블 초기화

# 2. watch 모드 테스트
sea watch --interval 5     # 5초 간격으로 빠르게 테스트

# 3. 리포트 내보내기 테스트
sea run --stage 5          # 제안 합성
sea export --format html --output /tmp/test-report.html
open /tmp/test-report.html # macOS

# 4. 전체 파이프라인
sea run                    # 전체 실행
sea github create --all    # 이슈 생성
sea watch                  # 대화형 승인 대기
```

---

## 변경 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| v4.1 | 2026-02-18 | interactive-approve.sh, export-report.sh, github-issue.sh 신규 추가 |
| v4.0 | 2026-02-11 | 4단계 파이프라인, 효과 측정 루프 |
| v3.0 | 이전 | 단일 Claude 호출, 키워드 매칭 |

---

*self-evolving-agent v4.1 — docs/integrations-v4.1.md*
