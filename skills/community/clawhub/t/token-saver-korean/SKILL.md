---
name: token-saver
description: "🧠 한국어 Context DB for AI Agents — 토큰 91% 절감. 임베딩 의미 검색, 중복 자동 병합, 메모리 계층화(Hot/Warm/Cold), 자동 아카이브, WAL 프로토콜, 엔티티 추출. Korean-first + English support."
metadata:
  openclaw:
    requires:
      bins: []
      env:
        - FIREWORKS_API_KEY
    install:
      - id: pip-konlpy
        kind: pip
        package: konlpy
        label: "한국어 형태소 분석기 (konlpy)"
      - id: pip-nltk
        kind: pip
        package: nltk
        label: "영어 NLP (nltk)"
    compatibility: "OpenClaw 2.0+, Python 3.10+"
---

# 🧠 TokenSaver Korean v2.0

**AI 에이전트를 위한 한국어 최적화 Context Database**

토큰 소모를 최대 **91% 절감**하는 스마트 메모리 시스템.
저장·검색·압축·계층화·아카이브까지 완전 자동화.

---

## ✨ 핵심 기능

| 기능 | 한 줄 설명 |
|------|-----------|
| 🔍 **임베딩 의미 검색** | 키워드가 아니라 **의미**로 찾습니다 |
| 🔗 **중복 자동 병합** | 비슷한 메모리 알아서 합쳐줍니다 |
| 📊 **메모리 계층화** | Hot → Warm → Cold 자동 관리 |
| 🗄️ **자동 아카이브** | 30일 묵은 메모리 자동 정리 |
| 📝 **WAL 프로토콜** | 저장 먼저, 응답 나중 — 유실 제로 |
| 🏷️ **엔티티 추출** | 사람·브랜드·제품 자동 태깅 |
| 🌐 **다국어 지원** | 한국어(konlpy) + 영어(nltk) |

---

## 🚀 빠른 시작

### 1. 환경변수 설정

```bash
# Fireworks API 키 (임베딩 검색용)
export FIREWORKS_API_KEY="your-key"

# Windows PowerShell
$env:FIREWORKS_API_KEY="your-key"
```

### 2. Python에서 사용

```python
from token_saver.client import TokenSaverKorean

# 초기화 (자동으로 workspace 탐지)
client = TokenSaverKorean()

# 저장 — 임베딩 자동 생성 + 중복 시 자동 병합
client.save_memory(
    uri="biz/daily_sales",
    content="오늘 매출 500만원, ROAS 5.83",
    category="biz"
)

# 검색 — 키워드 + 임베딩 하이브리드
results = client.find("매출 현황", use_embedding=True)

# 티어 통계
stats = client.get_tier_stats()
# → {'hot': 14, 'warm': 0, 'cold': 0, 'archive': 0}

# 만료 메모리 정리
client.cleanup_expired(days=30)
```

### 3. OpenClaw에서 사용

```
마스터: "닥터레이디 ROAS 기억해"
→ 보라: memory_store(uri="memories/drlady/roas", content="ROAS 5.83...")

마스터: "저번에 마케팅 전략 뭐였지?"
→ 보라: memory_recall(query="마케팅 전략")
```

---

## 📊 토큰 절감 효과

| 시나리오 | 기존 토큰 | TokenSaver | 절감율 |
|----------|-----------|------------|--------|
| 전체 Context 로드 | 50,000 | 4,500 | **91%** |
| 한국어 검색 | 20,000 | 2,000 | **90%** |
| 메모리 압축 | 30,000 | 3,500 | **88%** |

---

## 🗂️ 메모리 계층화

자동으로 중요도에 따라 티어를 관리합니다:

| 티어 | 기간 | 저장 방식 |
|------|------|-----------|
| 🔥 **Hot** | 7일 내 | 전체 내용 + 임베딩 |
| 🌡️ **Warm** | 30일 내 | 요약 + 임베딩 |
| ❄️ **Cold** | 30일+ | 키워드만 (압축) |
| 🗄️ **Archive** | 30일 미접속 | 검색에서 제외 |

```python
# 자동 승격/강등 — 접근할수록 Hot으로 올라감
client.save_memory("test", "내용")  # → Hot
# 30일 후 자동 → Cold
# 다시 검색하면 → Warm → Hot
```

---

## 🔍 하이브리드 검색

키워드 매칭 + 임베딩 유사도를 결합한 하이브리드 검색:

```python
results = client.find(
    query="광고 효율 개선",
    limit=5,
    use_embedding=True    # 임베딩 검색 ON
)

# 결과: 키워드 점수 + 임베딩 점수 = 최종 순위
# "ROAS 최적화 방법" (12.45점)
# "광고 소재 성과 분석" (9.91점)
```

API 실패 시 자동으로 키워드 검색으로 폴백 — **절대 안 끊김**.

---

## 🔗 중복 자동 병합

비슷한 내용이면 새로 만들지 않고 기존 것에 업데이트:

```python
# 첫 저장
client.save_memory("biz/roas", "ROAS 5.83", category="biz")

# 비슷한 내용 재저장 → 자동 병합 (코사인 > 0.85)
client.save_memory("biz/roas", "ROAS 6.12로 상승", category="biz")
# → 같은 URI에 버전 업그레이드 (v1 → v2)
```

---

## 🏷️ 자동 엔티티 추출

저장 시 사람·브랜드·제품을 자동으로 인식:

```python
entities = client.extract_entities("김명진 대표가 닥터레이디 리쥬-톡스 출시")
# → {'persons': ['김명진'], 'brands': ['닥터레이디'], 'products': ['리쥬-톡스']}
```

---

## ⚙️ 설정 파일 (ovk.conf)

```json
{
  "embedding": {
    "dense": {
      "provider": "fireworks",
      "model": "qwen3-embedding-8b",
      "dimension": 768
    }
  },
  "language": "auto",
  "token_optimization": {
    "enabled": true,
    "target_reduction": 0.91
  }
}
```

---

## 🛡️ 안정성

| 기능 | 설명 |
|------|------|
| **WAL 프로토콜** | 응답 전에 먼저 저장 — 크래시해도 유실 없음 |
| **자동 백업** | 수정 전 원본 백업 보관 |
| **임베딩 폴백** | API 장애 시 키워드 검색으로 자동 전환 |
| **하위호환** | v1 데이터 그대로 사용 가능 |

---

## 📦 의존성

| 패키지 | 용도 | 필수? |
|--------|------|-------|
| **konlpy** | 한국어 형태소 분석 | 권장 |
| **nltk** | 영어 NLP | 권장 |
| **FIREWORKS_API_KEY** | 임베딩 검색 | 임베딩 사용 시 |

> konlpy/nltk 없이도 작동합니다 (기본 토크나이저 사용).

---

## 📄 라이선스

MIT License — 자유롭게 사용, 수정, 배포 가능.

---

*TokenSaver Korean v2.0*
*임베딩 검색 · 중복 병합 · 메모리 계층화 · 자동 아카이브*
*한국어 우선, 영어 지원, OpenClaw 최적화*
