---
name: security-news-feed
version: 1.1.0
description: Automated security news aggregation and summarization module. Collects news from 11 Korean security sources (KRCERT, NCSC, Boho, Dailysec, etc.) → summarizes with Gemini API → publishes to Notion/Tistory. Runs hourly. Use when you want to monitor security news, collect Korean security updates, or aggregate news feeds. Triggers: "보안 뉴스", "security news", "뉴스 수집".
---

# Security News Module

## 개요

한국 보안 뉴스 소스 11곳에서 뉴스를 자동으로 수집하고, Gemini API로 요약한 후 Notion과 Tistory에 발행하는 모듈입니다.

**주기**: 1시간마다 자동 실행

## 워크플로우

```
11개 보안 뉴스 소스 병렬 크롤링
    ├─ KRCERT (한국인터넷진흥원)
    ├─ NCSC (국가사이버안보센터)
    ├─ Boho (보호나라)
    ├─ Dailysec
    ├─ KISA
    ├─ K-shield
    ├─ KrCert
    ├─ Notice
    ├─ Boho2
    ├─ Krcert2
    └─ Ncsc2
    ↓
키워드 기반 필터링 (보안 관련 키워드)
    ↓
Gemini API 요약 (140자 요약 + 상세 분석)
    ↓
Notion 데이터베이스 저장
    ↓
Tistory 블로그 발행 (선택)
```

## 주요 기능

### 1. 뉴스 수집 (Collection)
**11개 한국 보안 뉴스 소스**:

| 소스 | URL | 타입 |
|------|-----|------|
| KRCERT | https://www.krcert.or.kr | 공식 |
| NCSC | https://www.ncsc.go.kr | 공식 |
| Boho | https://www.boho.or.kr | 공식 |
| Dailysec | https://dailysecu.com | 민간 |
| KISA | https://www.kisa.or.kr | 공식 |
| K-shield | https://k-shield.or.kr | 공식 |
| KrCert | https://krcert.or.kr | 공식 |
| Notice | 내부 소스 | 내부 |
| Boho2 | https://boho.or.kr | 공식 |
| Krcert2 | https://www.krcert.or.kr | 공식 |
| Ncsc2 | https://ncsc.go.kr | 공식 |

### 2. 키워드 필터링 (Filtering)
**보안 관련 키워드**:
```python
keywords = [
    "취약점", "악성코드", "해킹", "랜섬웨어",
    "보안", "침해", "공격", "암호화",
    "인증", "방화벽", "악성", "피싱",
    "스파이웨어", "트로이목마", "봇넷"
]
```

### 3. Gemini API 요약 (Summarization)
**요약 구조**:
```
[140자 요약]
- 핵심 내용 3줄 요약

[상세 분석]
- 배경 설명
- 주요 내용
- 시사점
- 대응 방안
```

### 4. Notion 발행 (Notion Publishing)
- **자동 저장**: 수집된 뉴스 자동 저장
- **태그 분류**: 키워드 기반 자동 태그
- **상태 관리**: New → Read → Archived

### 5. Tistory 발행 (Tistory Publishing)
- **선택적 발행**: 중요 뉴스만 발행
- **자동 포맷팅**: 마크다운 → HTML 변환
- **카테고리 분류**: 자동 카테고리 할당

## 설치 방법

### 1. 저장소 클론
```bash
git clone --recursive https://github.com/rebugui/OpenClaw.git
cd OpenClaw/submodules/security_news_aggregator
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일 수정:
```bash
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Notion API (선택)
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id

# Tistory API (선택)
TISTORY_ACCESS_TOKEN=your_access_token
TISTORY_BLOG_NAME=your_blog_name
```

## 사용법

### 수동 실행
```bash
# 1회 실행
python security_news_aggregator.py --once

# 데몬 모드 (지속 실행)
python security_news_aggregator.py

# 특정 소스만 수집
python security_news_aggregator.py --sources krcert,ncsc
```

### 스케줄러 등록
OpenClaw 스케줄러에 등록하여 자동 실행:

```yaml
# config.yaml
jobs:
  - id: "security_news_aggregator"
    name: "Security News Aggregator - 매 1시간 보안 뉴스 수집"
    enabled: true
    module: "security_news_aggregator.security_news_aggregator"
    function: "main"
    is_async: false
    working_dir: "submodules/security_news_aggregator"
    trigger:
      type: "interval"
      hours: 1
```

## 설정 파일

### `config.py`
```python
# 뉴스 소스 설정
NEWS_SOURCES = {
    'krcert': {
        'url': 'https://www.krcert.or.kr',
        'type': 'rss',
        'enabled': True
    },
    'ncsc': {
        'url': 'https://www.ncsc.go.kr',
        'type': 'web',
        'enabled': True
    },
    # ...
}

# 키워드 필터
KEYWORDS = [
    "취약점", "악성코드", "해킹", "랜섬웨어",
    "보안", "침해", "공격", "암호화"
]

# Gemini 설정
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_MAX_TOKENS = 1000
GEMINI_TEMPERATURE = 0.7

# Notion 설정
NOTION_ENABLED = True
NOTION_DATABASE_ID = "your_database_id"

# Tistory 설정
TISTORY_ENABLED = False
TISTORY_BLOG_NAME = "your_blog_name"
```

## 파일 구조

```
security_news_aggregator/
├── security_news_aggregator.py  # 메인 실행 파일
├── config.py                    # 설정 파일
├── .env.example                 # 환경 변수 예시
├── requirements.txt             # 의존성
│
├── modules/                     # 기능 모듈
│   ├── collectors/              # 뉴스 수집기
│   │   ├── krcert_collector.py
│   │   ├── ncsc_collector.py
│   │   └── ...
│   ├── summarizer.py            # Gemini 요약
│   ├── notion_publisher.py      # Notion 발행
│   └── tistory_publisher.py     # Tistory 발행
│
├── data/                        # 데이터 저장
│   └── news_cache.json
│
└── logs/                        # 로그
    └── aggregator.log
```

## Notion 데이터베이스 설정

### 필드 구성
- `Title` (제목)
- `Summary` (140자 요약)
- `Content` (상세 분석)
- `Source` (출처)
- `URL` (원문 링크)
- `Tags` (다중 선택)
- `Published` (발행일)
- `Status` (선택: New, Read, Archived)

## 예시 출력

### 수집된 뉴스
```markdown
# 새로운 랜섬웨어, 한국 기업 공격

**요약**: 새로운 랜섬웨어 변종이 한국 기업들을 대상으로 공격을 시작했습니다...

**상세 분석**:
- **배경**: 최근 들어 증가하는 랜섬웨어 공격...
- **주요 내용**: 이 랜섬웨어는...
- **시사점**: 기업들의 보안 강화 필요...
- **대응 방안**: 정기 백업, 보안 패치...

**태그**: #랜섬웨어 #한국 #기업공격

**출처**: KRCERT
**원문**: https://www.krcert.or.kr/...
```

## 실행 통계

### 최근 실행 결과 (2026-03-08 11:58)
```
✅ 수집된 뉴스: 169개
✅ URL 변환 완료: 137개
✅ 키워드 기반 필터링: 169개 처리
✅ Gemini 요약 완료
✅ Notion 저장 완료
```

## 문제 해결

### 뉴스 수집 실패
```bash
# 로그 확인
tail -f logs/aggregator.log

# 특정 소스 테스트
python security_news_aggregator.py --test krcert
```

### Gemini API 오류
```bash
# API 키 확인
echo $GEMINI_API_KEY

# API 할당량 확인
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp?key=$GEMINI_API_KEY"
```

### Notion 연결 오류
```bash
# Notion API 키 확인
curl -X POST https://api.notion.com/v1/databases/{database_id}/query \
  -H "Authorization: Bearer {token}" \
  -H "Notion-Version: 2022-06-28"
```

## 의존성

- Python 3.11+
- Gemini API
- Notion API (선택)
- Tistory API (선택)
- BeautifulSoup4
- Requests

## API 키 발급

### Gemini API
1. https://makersuite.google.com/app/apikey 접속
2. API 키 생성
3. 키 복사

### Notion API (선택)
1. https://www.notion.so/my-integrations 접속
2. 새 통합 생성
3. API 키 복사
4. 데이터베이스에 통합 연결

### Tistory API (선택)
1. https://www.tistory.com/guide/api/register 접속
2. 앱 등록
3. Access Token 발급

## 라이선스

MIT License

## 참고

- **저장소**: https://github.com/rebugui/security_news_aggregator
- **메인 저장소**: https://github.com/rebugui/OpenClaw
