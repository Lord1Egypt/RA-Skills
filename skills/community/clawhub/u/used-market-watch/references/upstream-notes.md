# Upstream notes: `used-market-notifier`

이 스킬은 `tmp/used-market-notifier-upstream` 및 public repo `twbeatles/used-market-notifier`를 분석해, 다음 개념을 OpenClaw용으로 재구성했다.

## 유지한 핵심 개념

- **지원 마켓 범위**: 당근마켓 / 번개장터 / 중고나라
- **가격 정규화**: `10만`, `2만5천`, `무료나눔` 같은 한국형 가격 파싱
- **검색 후 필터링**: 가격 범위, 지역, 제외 키워드
- **신규/가격하락 감지**: article key + 이전 가격 상태를 로컬 저장소에 유지
- **Playwright 우선 수집**: 동적 마켓 검색 페이지에 맞춘 one-shot browser 세션
- **채팅/알림 친화 출력**: GUI 대신 text + JSON stdout

## 의도적으로 제거/축소한 것

- PyQt GUI 전체
- Telegram/Discord/Slack 직접 전송
- DB 기반 대시보드/백업/즐겨찾기/메시지 템플릿 UI
- 복잡한 dual-engine orchestration

## 이 스킬에서의 재해석

- OpenClaw가 상위 레이어에서 메시징/cron을 담당하므로, 이 스킬은 **검색·브리핑·watch state 계산**에 집중한다.
- persistent state는 `data/watch-rules.json` 하나로 단순화했다.
- upstream scrapers의 title/link/article-id 파싱 감각을 가져오되, CLI용으로 최소한의 구조만 남겼다.

## upstream에서 특히 참고한 파일

- `README.md`
- `monitor_engine.py`
- `models.py`
- `price_utils.py`
- `scrapers/playwright_danggeun.py`
- `scrapers/playwright_bunjang.py`
- `scrapers/playwright_joonggonara.py`
