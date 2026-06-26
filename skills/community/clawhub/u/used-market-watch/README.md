# used-market-watch

당근마켓, 번개장터, 중고나라를 대상으로 **중고 매물 검색 / 채팅형 브리핑 / 저장형 감시 규칙 / 신규 매물 / 가격하락 체크**를 수행하는 OpenClaw 스킬입니다.

이 스킬은 `used-market-notifier`의 핵심 아이디어를 OpenClaw 운영 흐름에 맞게 다시 묶은 버전입니다.

- 자연어로 검색하고
- 결과를 바로 브리핑하고
- 감시 규칙을 저장하고
- `watch-check`를 cron/heartbeat/메시징에 연결해 반복 운영하는 데 초점을 맞췄습니다.

## 지원 마켓

- 당근마켓
- 번개장터
- 중고나라

## 이번 버전에서 강해진 점

- `1시간마다`, `30분마다`, `매일 아침 8시` 같은 **주기 표현 해석**
- `신규만 감시`, `가격 내려가면 알려줘`, `브리핑해줘` 같은 **채팅형 의도 파싱 강화**
- `watch-plan` 출력에 **실행 주기 / 권장 명령 / cron 예시** 포함
- 저장된 rule에 **delivery_mode / schedule / plan_hints** 메타 저장
- 운영자가 `watch-list`만 봐도 **주기와 브리핑/알림 성격**을 바로 확인 가능

## 어떤 요청을 잘 받나

### 신규 매물 감시형

```text
아이폰 15 프로 1시간마다 신규만 감시해줘
```

해석 포인트:
- 감시 대상: 아이폰 15 프로
- 주기: 1시간마다
- 알림 조건: 신규만
- 출력 성격: 알림(alert)

### 가격하락 알림형

```text
맥북 에어 가격 내려가면 알려줘
```

해석 포인트:
- 감시 대상: 맥북 에어
- 주기: 수동 또는 상위 스케줄러 연결
- 알림 조건: 가격하락만
- 출력 성격: 알림(alert)

### 정기 브리핑형

```text
플스5 매일 아침 8시에 브리핑해줘
```

해석 포인트:
- 감시 대상: 플스5
- 주기: 매일 08:00
- 알림 조건: 신규 + 가격하락 기본
- 출력 성격: 브리핑(briefing)
- cron 예시: `0 8 * * * ... watch-check "플스5 감시" --json`

## 설치

```bash
clawhub install used-market-watch
```

## 준비

```bash
pip install playwright
python -m playwright install chromium
```

## 빠른 시작

### 1) 자연어 파싱 확인

```bash
python scripts/used_market_watch.py parse "잠실에서 아이폰 15 프로 120만원 이하 당근 번장만 -깨짐"
```

### 2) 원샷 검색 / 브리핑

```bash
python scripts/used_market_watch.py search "잠실에서 아이폰 15 프로 120만원 이하 당근 번장만 -깨짐"
python scripts/used_market_watch.py search "맥북 에어 m2 중고나라 포함" --json
```

### 3) 감시 규칙 해석 미리보기

```bash
python scripts/used_market_watch.py watch-plan "아이폰 15 프로 1시간마다 신규만 감시해줘"
python scripts/used_market_watch.py watch-plan "맥북 에어 가격 내려가면 알려줘" --json
python scripts/used_market_watch.py watch-plan "플스5 매일 아침 8시에 브리핑해줘"
```

### 4) OpenClaw용 자동화 연동 번들 생성

```bash
python scripts/used_market_watch.py integration-plan "아이폰 15 프로 신규 매물만 1시간마다 감시해줘"
python scripts/used_market_watch.py integration-plan "플스5 매일 아침 8시에 브리핑해줘" --json
python scripts/used_market_watch.py integration-plan "맥북 에어 가격 내려가면 알려줘" --persist --json
```

출력에 포함되는 것:
- 파싱된 감시 계획
- 실제 저장 명령(`watch-upsert`)
- 실제 실행 명령(`watch-check`)
- cron payload 제안
- systemEvent 힌트
- 사용자 확인용 짧은 한국어 문구

### 5) 감시 규칙 저장 / 업데이트

```bash
python scripts/used_market_watch.py watch-upsert "아이폰 15 프로 1시간마다 신규만 감시해줘"
python scripts/used_market_watch.py watch-upsert "맥북 에어 가격 내려가면 알려줘"
python scripts/used_market_watch.py watch-upsert "플스5 매일 아침 8시에 브리핑해줘"
```

같은 이름의 규칙이 이미 있으면 새로 만들지 않고 업데이트합니다.
이름을 고정하고 싶으면 큰따옴표로 먼저 지정하면 됩니다.

```bash
python scripts/used_market_watch.py watch-upsert '"잠실 맥북 하락" 맥북 에어 m2 잠실 가격하락만 감시'
```

### 6) 저장된 규칙 목록 확인

```bash
python scripts/used_market_watch.py watch-list
python scripts/used_market_watch.py watch-list --json
```

### 7) 실제 점검 실행

```bash
python scripts/used_market_watch.py watch-check
python scripts/used_market_watch.py watch-check --alerts-only --json
python scripts/used_market_watch.py watch-check "잠실 맥북 하락" --json
```

### 8) 최근 이벤트 피드 보기

```bash
python scripts/used_market_watch.py watch-events --limit 20
python scripts/used_market_watch.py watch-events "잠실 맥북 하락" --json
```

## 운영 패턴 추천

### 패턴 A. 검색 후 감시 등록

1. `search`로 검색 품질과 키워드를 먼저 확인
2. 원하는 조건이 맞으면 `watch-upsert`로 저장
3. 이후는 scheduler가 `watch-check`만 주기적으로 실행

### 패턴 B. 신규 매물만 짧은 주기로 추적

추천 예시:

```text
아이폰 15 프로 1시간마다 신규만 감시해줘
```

권장 연결:
- 실행: `watch-check "아이폰 15 프로 감시" --alerts-only --json`
- 용도: 텔레그램/디스코드 신규 매물 알림

### 패턴 C. 가격하락만 저소음 감시

추천 예시:

```text
맥북 에어 가격 내려가면 알려줘
```

권장 연결:
- 실행: `watch-check "맥북 에어 감시" --alerts-only --json`
- 용도: 노이즈를 줄이고 할인 신호만 받고 싶을 때

### 패턴 D. 하루 1회 아침 브리핑

추천 예시:

```text
플스5 매일 아침 8시에 브리핑해줘
```

권장 연결:
- 실행: `watch-check "플스5 감시" --json`
- 용도: 아침 요약 브리핑, 데일리 리포트, 채널 게시

## OpenClaw 채팅→자동화 연결 패턴

메인 어시스턴트가 자연어 요청을 받으면 보통 아래 순서로 쓰면 됩니다.

1. `integration-plan "사용자 요청" --json` 실행
2. `user_confirmation` 문구로 사용자에게 최종 확인
3. 확인되면 `persist.command` 또는 `integration-plan ... --persist --json`으로 규칙 저장
4. `execution.cron_payload`를 기준으로 cron/systemEvent 초안 생성
5. 실제 주기 실행에서는 `execution.recommended_command`를 호출

예시 JSON 필드:
- `parsed_plan`: 저장될 rule 원본
- `persist.command`: 실제 watch-upsert 명령
- `execution.recommended_command`: 실제 watch-check 명령
- `execution.cron_payload.expr`: cron 식
- `execution.system_event`: 상위 자동화 레이어에 넘길 힌트 객체
- `user_confirmation`: 사용자에게 보여줄 짧은 한국어 확인 문구

## cron 연결 힌트

`watch-plan`과 `integration-plan`은 해석뿐 아니라 운영 힌트를 함께 보여줍니다.
예를 들어 `플스5 매일 아침 8시에 브리핑해줘`를 넣으면 다음 정보를 얻을 수 있습니다.

- 실행 주기: `매일 08:00`
- 권장 실행: `python ... watch-check "플스5 감시" --json`
- cron 예시: `0 8 * * * python ... watch-check "플스5 감시" --json`

자주 쓰는 패턴:

```bash
python scripts/used_market_watch.py watch-check --alerts-only --json
```
- 여러 규칙의 신규/가격하락 이벤트만 모아 채팅 알림으로 보낼 때 적합

```bash
python scripts/used_market_watch.py watch-check "플스5 감시" --json
```
- 특정 규칙 브리핑을 정해진 시각에 보내고 싶을 때 적합

## JSON 출력 포인트

### `search`
- `kind=used-market-search`
- `intent`
- `summary.total`, `summary.by_market`
- `items[]`

### `watch-plan`
- `kind=used-market-watch-plan`
- `rule.delivery_mode`
- `rule.schedule`
- `rule.plan_hints.recommended_command`
- `rule.plan_hints.cron_example`

### `watch-check`
- `kind=used-market-watch-check`
- `alert_count`
- `summary.rule_count`
- `summary.rules_with_matches`
- `summary.event_counts`
- `alerts[]`

### `watch-events`
- `kind=used-market-watch-events`
- `count`
- `events[]`

## 운영 팁

- 규칙 이름을 고정하려면 큰따옴표로 먼저 이름을 주는 편이 안전합니다.
- `신규만`, `가격하락만`, `브리핑해줘` 같은 표현으로 감시 성격을 자연어로 제어할 수 있습니다.
- `5개`, `10건` 같은 limit 힌트도 자연어로 줄 수 있습니다.
- 비활성화는 삭제보다 `watch-disable`이 안전합니다.
- 상위 레이어에서는 `summary.event_counts`, `alerts`, `events`를 바로 재가공하면 됩니다.

## 테스트

```bash
python -m pytest tests -q
```

## 한계

- 실검색은 Playwright와 각 마켓 DOM 구조에 의존합니다.
- 로그인/봇 차단이 강한 경우 결과가 줄 수 있습니다.
- 중고나라는 메타데이터가 제한적일 수 있습니다.
- 현재는 Playwright 단일 경로입니다.

## 설치 / 링크

- GitHub: <https://github.com/twbeatles/openclaw-used-market-watch>
- ClawHub 홈: <https://clawhub.com>
- 설치 명령: `clawhub install used-market-watch`

## 대표 예시 요청 모음

- `잠실에서 아이폰 15 프로 120만원 이하 당근 번장만 찾아줘`
- `아이폰 15 프로 신규 매물만 1시간마다 감시해줘`
- `맥북 에어 가격 내려가면 알려줘`
- `플스5 매일 아침 8시에 브리핑해줘`
- `후지 x100 시리즈 번장 포함 -고장 -파손 조건으로 계속 체크해줘`
