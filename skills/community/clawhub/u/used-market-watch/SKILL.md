---
name: used-market-watch
description: Search, brief, and monitor Korean used-market listings across 당근마켓, 번개장터, and 중고나라. Use when the user wants 중고 매물 찾아줘, 당근/번장/중고나라 동시 검색, 아이폰/맥북 같은 물건의 신규 매물 감시, 가격하락 체크, 자연어 기반 한국 중고거래 브리핑, 자연어 watch rule 추가/수정, 최근 watch 이벤트 확인, 1시간마다/매일 아침 8시 같은 주기 표현이 포함된 감시 요청, or cron-friendly stdout/JSON monitoring output.
---

# Used Market Watch

한국 중고거래 매물을 **자연어 검색 / 채팅형 브리핑 / persistent watch rule / 신규·가격하락 체크 / 주기 해석 기반 운영 계획** 형태로 다루는 OpenClaw 스킬이다.

핵심 원칙:
- **chat-first**: 사람이 읽는 한국어 브리핑을 먼저 만든다.
- **json-ready**: cron/상위 레이어 연결용 JSON도 바로 뽑는다.
- **watch-state 단순화**: GUI/DB 대신 `data/watch-rules.json` 하나로 상태를 유지한다.
- **natural-language ops**: 검색과 감시 등록을 분리하지 않고 한 줄 한국어 요청에서 watch intent를 최대한 바로 해석한다.
- **plan-aware**: `1시간마다`, `30분마다`, `매일 아침 8시`, `브리핑해줘` 같은 운영 문장을 rule 메타와 실행 힌트로 변환한다.
- **upstream 계승**: `used-market-notifier`의 마켓 범위, 가격 파싱, Playwright 검색 감각, 신규/가격하락 개념을 OpenClaw용 CLI로 재구성했다.

## Source dependency / analysis

분석 기준 upstream:
- `tmp/used-market-notifier-upstream`
- public repo: `twbeatles/used-market-notifier`

핵심 참고 내용은 `references/upstream-notes.md`에 정리돼 있다.

## Scripts

### 1) 자연어 파싱 확인
```bash
python skills/used-market-watch/scripts/used_market_watch.py parse "잠실에서 아이폰 15 프로 120만원 이하 당근 번장만 -깨짐"
```

### 2) 원샷 검색 / 브리핑
```bash
python skills/used-market-watch/scripts/used_market_watch.py search "잠실에서 아이폰 15 프로 120만원 이하 당근 번장만 -깨짐"
python skills/used-market-watch/scripts/used_market_watch.py search "맥북 에어 m2 중고나라 포함" --json
```

출력 특징:
- 마켓별 개수 요약
- 대표 매물 리스트
- 링크 포함
- text / JSON 선택 가능

### 3) 자연어 watch 미리보기 / 저장
```bash
python skills/used-market-watch/scripts/used_market_watch.py watch-plan "아이폰 15 프로 1시간마다 신규만 감시해줘"
python skills/used-market-watch/scripts/used_market_watch.py watch-plan "맥북 에어 가격 내려가면 알려줘" --json
python skills/used-market-watch/scripts/used_market_watch.py watch-plan "플스5 매일 아침 8시에 브리핑해줘"
python skills/used-market-watch/scripts/used_market_watch.py integration-plan "아이폰 15 프로 신규 매물만 1시간마다 감시해줘"
python skills/used-market-watch/scripts/used_market_watch.py integration-plan "플스5 매일 아침 8시에 브리핑해줘" --json
python skills/used-market-watch/scripts/used_market_watch.py integration-plan "맥북 에어 가격 내려가면 알려줘" --persist --json
python skills/used-market-watch/scripts/used_market_watch.py watch-upsert "아이폰 15 프로 1시간마다 신규만 감시해줘"
python skills/used-market-watch/scripts/used_market_watch.py watch-upsert '"잠실 맥북 하락" 맥북 에어 m2 잠실 가격하락만 감시'
```

동작 특징:
- `신규만`, `가격하락만`, `가격 내려가면` 같은 표현을 해석한다.
- `1시간마다`, `30분마다`, `매일 아침 8시` 같은 주기 표현을 해석한다.
- `브리핑해줘`, `요약해줘` 같은 표현을 브리핑 모드로 해석한다.
- `5개`, `10건` 같은 limit 힌트를 반영한다.
- 이름을 따로 안 주면 keyword 기반 규칙 이름을 만든다.
- 같은 이름이 있으면 `watch-upsert`가 갱신한다.
- `integration-plan`은 저장 명령, 실행 명령, cron payload, systemEvent 힌트, 사용자 확인 문구까지 한 번에 묶어 준다.
- 해석 결과에 권장 실행 명령과 cron 예시를 포함한다.

### 4) watch rule 목록 / 상태 관리
```bash
python skills/used-market-watch/scripts/used_market_watch.py watch-list
python skills/used-market-watch/scripts/used_market_watch.py watch-enable "잠실 맥북 하락"
python skills/used-market-watch/scripts/used_market_watch.py watch-disable "잠실 맥북 하락"
python skills/used-market-watch/scripts/used_market_watch.py watch-remove "잠실 맥북 하락"
```

### 5) watch 점검 / 이벤트 피드
```bash
python skills/used-market-watch/scripts/used_market_watch.py watch-check
python skills/used-market-watch/scripts/used_market_watch.py watch-check --alerts-only --json
python skills/used-market-watch/scripts/used_market_watch.py watch-events --limit 20
python skills/used-market-watch/scripts/used_market_watch.py watch-events "잠실 맥북 하락" --json
```

점검 결과:
- 신규 매물(`new_listing`)
- 가격하락(`price_drop`)
- 각 rule별 snapshot 요약
- `summary.event_counts` 포함 JSON
- 최근 이벤트 조회용 `watch-events`

## Runtime notes

필수 준비:
```bash
pip install playwright
python -m playwright install chromium
```

테스트:
```bash
python -m pytest skills/used-market-watch/tests -q
```

## Stored files

- `data/watch-rules.json`: watch rule + last_seen + dedupe event state
- `references/upstream-notes.md`: upstream 분석 메모
- `dist/used-market-watch.skill`: 배포용 패키지 아티팩트

## Recommended workflow

1. 사용자가 한 줄로 원하는 물건/가격/마켓을 말하면 `search`로 먼저 브리핑한다.
2. 반복 추적이 필요하면 `watch-plan`으로 해석을 확인하거나 바로 `watch-upsert`로 규칙을 저장한다.
3. 채팅 자동화/cron 연결이 목적이면 `integration-plan`으로 저장 명령, 실행 명령, cron payload, systemEvent 힌트를 한 번에 만든다.
4. heartbeat/cron에서는 `watch-check --alerts-only --json` 또는 특정 rule 대상 `watch-check "이름" --json`을 사용한다.
5. 운영 중에는 `watch-list`, `watch-events`, `watch-enable`, `watch-disable`로 상태를 관리한다.
6. 상위 레이어(OpenClaw)가 텔레그램/디스코드 전달을 담당한다.

## Current limitations

- 각 마켓 DOM 구조 변경에 민감하다.
- 로그인 필요/봇 차단이 강한 상황에서는 결과가 줄 수 있다.
- 중고나라는 네이버 검색 결과 기반이라 가격 정보가 제한적일 수 있다.
- 현재는 Playwright 단일 경로이며 Selenium fallback은 넣지 않았다.
