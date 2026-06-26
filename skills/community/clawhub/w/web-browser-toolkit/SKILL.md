---
name: web-browser-toolkit
description: "웹사이트 브라우징, 정보 수집, 데이터 추출, 모니터링을 위한 종합 브라우징 스킬. 정적/동적 웹페이지에서 데이터를 수집하고 JSON으로 구조화하며, 변경사항 모니터링과 정기 수집을 지원한다. 항공(ICAO, FAA 등) 기관 수집에 특화된 프리셋도 포함."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
    emoji: "🌐"
    tags:
      - web-scraping
      - monitoring
      - data-extraction
      - aviation
---

# Web Browser Toolkit for OpenClaw

웹 브라우징, 정보 수집, 데이터 추출, 모니터링을 위한 종합 스킬.
OpenClaw의 3가지 웹 접근 방식(`web_fetch`, `browser`, Python 스크립트)을 상황에 맞게 자동 선택한다.

## 아키텍처: 3계층 브라우징 엔진

웹 페이지의 특성에 따라 가장 효율적인 방법을 자동 선택한다. 가벼운 도구로 먼저 시도하고, 실패하면 다음 계층으로 올라가는 방식이다.

```
┌─────────────────────────────────────────────┐
│  Layer 3: Browser (Playwright/CDP)          │  ← JS 렌더링, 로그인, 인터랙션 필요 시
│  ─ openclaw browser navigate/click/type     │
├─────────────────────────────────────────────┤
│  Layer 2: Python Fetcher (requests + BS4)   │  ← 정적 HTML 구조적 파싱 필요 시
│  ─ scripts/fetcher.py                       │
├─────────────────────────────────────────────┤
│  Layer 1: web_fetch / curl                  │  ← 단순 페이지 읽기 (기본)
│  ─ 가장 빠르고 가벼움                         │
└─────────────────────────────────────────────┘
```

### 계층 자동 선택 기준

| 조건 | 선택 계층 | 이유 |
|------|----------|------|
| 단순 텍스트 페이지, 뉴스, 블로그 | Layer 1 | HTML → Markdown 변환이면 충분 |
| 표, 목록, 구조적 데이터가 있는 페이지 | Layer 2 | CSS 셀렉터로 정확한 추출 필요 |
| JS 동적 렌더링 (SPA, React 등) | Layer 3 | 페이지 완전 로딩 후 추출 필요 |
| 로그인 필요, 폼 제출, 클릭 필요 | Layer 3 | 사용자 인터랙션 시뮬레이션 필요 |
| robots.txt 차단 또는 봇 감지 | Layer 3 | 실제 브라우저 세션 필요 |

판단이 어려우면 Layer 1부터 시도한다. 빈 결과나 의미 없는 내용이 오면 다음 계층으로 올린다.

---

## 워크플로우

### A. 단일 페이지 수집

```
1. URL 확인 및 계층 선택
2. 페이지 콘텐츠 수집
3. 데이터 추출 및 정리
4. JSON 구조화 (선택)
5. 사용자에게 결과 전달
```

### B. 리서치 (다중 페이지)

```
1. 검색어 구성
2. 검색 결과 수집 (web_search 또는 구글 검색)
3. 상위 N개 결과 페이지를 순회하며 수집
4. 수집 데이터 통합 및 중복 제거
5. JSON 구조화 + 태깅
6. 보고서 생성
```

### C. 모니터링 (정기 수집)

```
1. 대상 URL 및 수집 항목 정의
2. 초기 수집 및 베이스라인 저장
3. 정기 실행 시 재수집
4. 이전 결과와 diff 비교
5. 변경사항 알림 및 기록
```

---

## Layer 1: web_fetch / curl 사용법

가장 기본적이고 빠른 수집 방법.

### web_fetch 사용 (OpenClaw 내장)

```
web_fetch https://www.icao.int/safety/Pages/default.aspx
```

web_fetch는 HTML을 자동으로 Markdown으로 변환해주므로, 텍스트 기반 콘텐츠를 읽을 때 가장 편하다.

### curl 사용 (web_fetch 실패 시)

```bash
curl -sL -A "Mozilla/5.0 (compatible; OpenClaw/1.0)" \
  -H "Accept: text/html" \
  "https://www.faa.gov/regulations_policies/airworthiness_directives" \
  | python3 scripts/html_to_text.py
```

### 어떤 상황에 적합한가

- 뉴스 기사, 블로그 포스트 읽기
- 공지사항, 보도자료 확인
- 정적 HTML 페이지의 텍스트 추출
- 빠른 URL 내용 확인

---

## Layer 2: Python Fetcher 사용법

구조적 데이터 추출이 필요할 때 사용. `scripts/fetcher.py`가 핵심 도구.

### 기본 사용

```bash
# 단일 URL 수집
python3 scripts/fetcher.py fetch "https://www.icao.int/safety/Pages/default.aspx" \
  --selectors "title=h1" "items=.news-item" "links=a[href]" \
  --output result.json

# 검색 후 수집
python3 scripts/fetcher.py search "ICAO UAM regulation 2026" \
  --max-results 10 \
  --output search_results.json

# 다중 URL 수집
python3 scripts/fetcher.py batch urls.txt \
  --selectors "title=h1" "content=.main-content" \
  --output batch_results.json
```

### CSS 셀렉터 가이드

자주 쓰는 패턴:

```
제목:       h1, h2, .title, .headline, #page-title
본문:       .content, .main-content, article, .post-body
목록:       ul li, ol li, .list-item, table tr
링크:       a[href], .nav-link, .menu a
날짜:       time, .date, .published, .timestamp
태그:       .tag, .category, .label, meta[name="keywords"]
표:         table, .data-table, .grid
```

사이트 구조를 모를 때는 셀렉터 없이 실행하면 자동으로 주요 콘텐츠를 추출한다.

### 어떤 상황에 적합한가

- 표 형태 데이터 추출 (가격표, 통계 등)
- 목록 항목 수집 (AD 목록, 뉴스 리스트)
- 특정 요소만 정확히 추출할 때
- 대량 URL 배치 처리

---

## Layer 3: Browser (Playwright/CDP) 사용법

JavaScript 렌더링이나 사용자 인터랙션이 필요한 경우 사용.

### 브라우저 시작 및 기본 탐색

```bash
# 브라우저 시작
openclaw browser start

# 페이지 이동
openclaw browser navigate "https://www.icao.int"

# 페이지 스냅샷 (현재 상태 확인)
openclaw browser snapshot

# 스크린샷 저장
openclaw browser screenshot --path page.png
```

### 인터랙션

```bash
# 요소 클릭
openclaw browser click "검색 버튼"

# 텍스트 입력
openclaw browser type "검색창" "UAM regulation"

# 키 입력
openclaw browser press "Enter"

# 드롭다운 선택
openclaw browser select "정렬 기준" "최신순"

# 스크롤
openclaw browser evaluate "window.scrollTo(0, document.body.scrollHeight)"
```

### 페이지 텍스트 추출

```bash
# 전체 텍스트
openclaw browser evaluate "document.body.innerText"

# 특정 요소
openclaw browser evaluate "document.querySelector('.main-content').innerText"

# 모든 링크 추출
openclaw browser evaluate "[...document.querySelectorAll('a')].map(a => ({text: a.textContent.trim(), href: a.href})).filter(a => a.text)"
```

### PDF 저장

```bash
openclaw browser pdf --path page.pdf
```

### 어떤 상황에 적합한가

- SPA(Single Page Application) 크롤링
- 로그인 후 콘텐츠 접근
- 검색 폼 제출 후 결과 수집
- 무한 스크롤 페이지
- 봇 차단이 있는 사이트

---

## 데이터 구조화 (JSON)

수집한 데이터를 표준 JSON으로 구조화한다. `scripts/fetcher.py structurize` 명령 또는 수동 구성 가능.

### 표준 출력 스키마

```json
{
  "metadata": {
    "collection_id": "uuid",
    "collected_at": "ISO 8601 timestamp",
    "source_url": "https://...",
    "method": "web_fetch | python_fetcher | browser",
    "collector": "web_browser_toolkit",
    "version": "1.0"
  },
  "pages": [
    {
      "url": "https://...",
      "title": "페이지 제목",
      "content": "추출된 텍스트",
      "extracted_data": {
        "tables": [],
        "lists": [],
        "links": [],
        "images": []
      },
      "tags": ["auto-generated-tags"],
      "fetched_at": "ISO 8601"
    }
  ],
  "summary": {
    "total_pages": 5,
    "success": 4,
    "failed": 1,
    "total_items": 42
  }
}
```

### 자동 태깅

`scripts/fetcher.py`의 `auto_tag()` 함수가 페이지 내용을 분석하여 태그를 자동 부여한다.

---

## 모니터링 모드

특정 페이지의 변경사항을 감지하고 기록한다.

### 모니터 설정

```bash
# 모니터 등록
python3 scripts/monitor.py add \
  --url "https://www.faa.gov/regulations_policies/airworthiness_directives" \
  --name "FAA AD Monitor" \
  --selectors "items=.ad-list-item" \
  --check-interval "daily"

# 수동 체크
python3 scripts/monitor.py check --name "FAA AD Monitor"

# 전체 모니터 상태
python3 scripts/monitor.py status
```

### 모니터링 데이터 저장 구조

```
monitor-data/
├── monitors.json          # 모니터 설정 목록
├── snapshots/
│   ├── faa-ad-monitor/
│   │   ├── 2026-04-05.json  # 일별 스냅샷
│   │   ├── 2026-04-06.json
│   │   └── ...
│   └── ...
├── diffs/
│   ├── faa-ad-monitor/
│   │   ├── 2026-04-06_diff.json  # 변경사항 기록
│   │   └── ...
│   └── ...
└── alerts.json            # 미읽은 변경 알림
```

### cron 연동 (정기 실행)

```bash
# crontab -e
# 매일 오전 8시: 모든 모니터 체크
0 8 * * * cd ~/web-monitor && python3 scripts/monitor.py check-all

# 매주 월요일: 주간 변경 요약 보고서 생성
0 9 * * 1 cd ~/web-monitor && python3 scripts/monitor.py weekly-report
```

### OpenClaw 정기 태스크 연동

```bash
openclaw run "등록된 웹 모니터를 모두 체크하고, 변경사항이 있으면 요약해서 알려줘"
```

---

## 항공 기관 프리셋

항공 관련 사이트 수집에 최적화된 프리셋 설정. `references/aviation_presets.json` 참고.

```bash
# 프리셋 사용
python3 scripts/fetcher.py preset faa-ad --query "boeing 737"
python3 scripts/fetcher.py preset icao-safety --query "UAM"
python3 scripts/fetcher.py preset --list  # 전체 프리셋 목록
```

프리셋에는 각 기관의 URL, 검색 패턴, CSS 셀렉터, 태깅 규칙이 사전 정의되어 있다.

---

## 에러 처리 및 폴백

| 상황 | 대응 |
|------|------|
| web_fetch 실패 (403/차단) | → Layer 2 `fetcher.py` 시도 → Layer 3 `browser` 시도 |
| SSL 오류 | curl에 `--insecure` 추가 (경고와 함께) |
| 타임아웃 | 재시도 1회 → 실패 기록 |
| 인코딩 문제 | `chardet`로 감지 후 변환 |
| robots.txt 차단 | 사용자에게 알리고 브라우저 모드 제안 |
| 빈 콘텐츠 | JS 렌더링 필요 판단 → Layer 3 자동 승격 |
| CAPTCHA | 스크린샷으로 사용자에게 보여주고 수동 해결 요청 |

---

## 보안 및 윤리 가이드라인

- **robots.txt 존중**: `fetcher.py`는 기본적으로 robots.txt를 확인하고 존중한다
- **요청 빈도 제한**: 동일 도메인에 대해 최소 1초 간격 유지
- **저작권 보호**: 전문 복사 대신 요약 + 출처 링크 방식 권장
- **개인정보**: 수집 데이터에 개인정보가 포함되지 않도록 주의
- **User-Agent**: 정직한 UA 문자열 사용 (`OpenClaw WebBrowserToolkit/1.0`)

## 확장 모듈 (Sub-Skills)

### doc-recommender: 공식 문서 추천 엔진

웹에서 수집한 정보와 관련된 공식 문서(규칙, 규정, 표준, 가이드라인)를 자동으로 찾아 추천한다.
수집 JSON의 태그를 분석하거나, 사용자의 직접 질문에 대해 관련 공식 문서를 추천한다.

**사용법:**

```bash
# 수집 결과에서 자동 추천
python3 sub-skills/doc-recommender/scripts/doc_recommender.py recommend \
  --input collections/2026-04-05_ICAO_UAM-AAM.json \
  --top 10 --output recommendations.json

# 키워드로 직접 추천
python3 sub-skills/doc-recommender/scripts/doc_recommender.py recommend \
  --keywords "eVTOL UAM certification" --top 10

# 기관간 규제 비교
python3 sub-skills/doc-recommender/scripts/doc_recommender.py compare \
  --topic "eVTOL certification" --issuers "FAA,EASA,ICAO"
```

**연동 방식:**
1. 브라우징 수집 완료 → 수집 JSON 생성 → `doc-recommender`가 tags 분석 → 관련 공식 문서 자동 추천
2. 사용자 직접 질문 → 키워드 추출 → 지식 베이스 매칭 → 추천 결과 제공

**상세 정보**: `sub-skills/doc-recommender/SKILL.md` 참고

---

## 참고 파일

- `scripts/fetcher.py` — 핵심 웹 수집 엔진 (fetch/search/batch/structurize)
- `scripts/monitor.py` — 변경사항 모니터링 엔진
- `scripts/html_to_text.py` — HTML → 텍스트 변환 유틸리티
- `references/aviation_presets.json` — 항공 기관 수집 프리셋
- `references/selector_guide.md` — CSS 셀렉터 치트시트
- `sub-skills/doc-recommender/` — 공식 문서 추천 확장 모듈
