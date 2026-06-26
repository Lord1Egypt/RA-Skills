---
name: doc_recommender
description: "웹에서 수집한 정보와 관련된 공식 문서(규칙, 규정, 표준, 가이드라인)를 자동으로 찾아 추천하는 스킬. 사용자가 '관련 규정 찾아줘', '공식 문서 추천', '어떤 표준이 적용돼?', '규정 레퍼런스' 등을 요청할 때 사용. 항공, 법률, 기술 표준 등 어떤 도메인이든 공식 출처 문서를 찾아 추천하는 요청에 반드시 이 스킬을 사용해야 한다."
---

# Official Document Recommender (Claude Cowork 버전)

웹에서 수집한 정보와 관련된 공식 문서를 자동으로 찾아 추천하는 엔진.
Claude Cowork의 WebSearch, WebFetch, Read 도구와 연동하여 동작한다.

## 사용 조건

- Claude Cowork 환경 (WebSearch, WebFetch 도구 사용 가능)
- `scripts/doc_recommender.py` 실행을 위한 Python 3 환경
- `references/doc_knowledge_base.json` — 문서 지식 베이스
- `references/keyword_mapping.json` — 키워드-문서 매핑 테이블

## 워크플로우

### Step 1: 입력 분석

사용자 요청을 분석하여 입력 유형을 판별한다:

| 입력 유형 | 처리 방법 |
|-----------|-----------|
| 수집된 JSON 파일 | `Read`로 JSON 읽기 → tags 필드 추출 → 키워드 매칭 |
| 직접 질문 | 질문에서 키워드 추출 → 도메인 식별 → 문서 매칭 |
| URL | `WebFetch`로 페이지 읽기 → 키워드 추출 → 문서 매칭 |
| 키워드 목록 | 바로 문서 매칭 |

### Step 2: 키워드 추출 및 매칭

**Python 스크립트 실행:**
```bash
# JSON 파일에서 추천
python3 scripts/doc_recommender.py recommend \
  --input /path/to/collection.json \
  --top 10 --output recommendations.json

# 키워드로 추천
python3 scripts/doc_recommender.py recommend \
  --keywords "eVTOL UAM certification" \
  --top 10 --output recommendations.json

# 기관간 비교
python3 scripts/doc_recommender.py compare \
  --topic "eVTOL certification" \
  --issuers "FAA,EASA,ICAO" \
  --output comparison.json
```

**또는 직접 매칭 (스크립트 없이):**

`references/keyword_mapping.json`의 `keyword_groups`를 참조하여 Claude가 직접 매칭할 수 있다:

| 키워드 그룹 | 트리거 키워드 | 주요 문서 |
|-------------|--------------|-----------|
| evtol_certification | eVTOL, 전기수직이착륙, powered lift | SC-VTOL-02, Part 23, F3230, Annex 8 |
| uam_policy | UAM, AAM, 도심항공교통 | Annex 8, Cir 328, SC-VTOL-02 |
| drone_uas | 드론, UAS, 무인기 | Cir 328, Part 107, F3548 |
| noise_regulation | 소음, noise | Annex 16, Part 36 |
| software_avionics | DO-178, 항전, 소프트웨어 | DO-178C, DO-254, ARP4754A |
| safety_management | SMS, 안전관리 | Annex 19, Doc 9859 |
| airworthiness | 감항, certification | Annex 8, Part 21, Part 23 |

### Step 3: 웹 검증 (WebSearch 활용)

매칭된 문서에 대해 WebSearch로 최신 정보를 검증한다:

```
1. 문서 URL 유효성 확인
2. 최신 개정판(amendment) 확인
3. 추가 관련 문서 탐색
4. 해석 문서나 가이던스 검색
```

WebSearch 쿼리 예시:
- `"ICAO Annex 8" latest amendment 2025 2026`
- `"14 CFR Part 23" amendment eVTOL powered lift`
- `"EASA SC-VTOL" special condition latest`

### Step 4: 추천 결과 출력

**표 형식으로 출력:**

📋 **[주제] 관련 공식 문서 추천**

| 순위 | 문서 | 발행기관 | 유형 | 최신 개정 | 관련도 |
|------|------|----------|------|-----------|--------|
| 1 | 문서명 | ICAO | 국제표준 | 2024 | ⭐⭐⭐⭐⭐ |

각 문서에 대해:
- **적용 맥락**: 왜 이 문서가 관련되는지 1-2문장
- **URL**: 공식 문서 링크
- **관련 문서**: 함께 참고할 문서

### Step 5: JSON 출력 (선택)

사용자가 JSON 출력을 요청하거나 다른 스킬과 연동 시:

```json
{
  "query": {"keywords": [...], "domain": "aviation"},
  "recommendations": [
    {
      "rank": 1,
      "document": {"id": "ICAO-Annex-8", "title": "...", "issuer": "ICAO", "url": "..."},
      "relevance_score": 0.95,
      "relevance_context": "적용 맥락 설명"
    }
  ]
}
```

## 브라우징 스킬 연동

이 스킬은 `web_browser_toolkit`의 하위 확장 모듈이다.

**자동 추천 모드**: 브라우징 스킬이 수집을 완료하면, 수집 JSON의 tags를 분석하여 관련 공식 문서를 자동으로 추천한다.

```
브라우징 스킬 수집 완료
  ↓ (수집 JSON 생성)
doc_recommender 자동 실행
  ↓ (tags → keywords → 문서 매칭)
추천 결과 사용자에게 제공
```

**수동 추천 모드**: 사용자가 직접 질문하면 독립적으로 동작한다.

## 중요 규칙

1. **정확성**: 문서 번호와 제목을 정확히 인용. 불확실하면 WebSearch로 확인.
2. **최신성**: 항상 최신 개정판을 추천. 폐지된 문서는 [폐지] 표시.
3. **이중 언어**: 한국어/영어 키워드 모두 지원. 문서 제목은 원어, 설명은 사용자 언어.
4. **출처 명시**: 모든 추천 문서에 공식 URL 포함.
5. **공식 문서만**: 블로그, 뉴스, 논문 제외. 해설 필요 시 별도 표시.

## 참고 파일

- `scripts/doc_recommender.py` — 핵심 추천 엔진
- `references/doc_knowledge_base.json` — 문서 지식 베이스
- `references/keyword_mapping.json` — 키워드-문서 매핑 테이블
