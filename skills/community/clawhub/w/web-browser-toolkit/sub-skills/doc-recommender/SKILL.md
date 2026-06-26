---
name: doc_recommender
description: "웹사이트에서 수집한 주제와 관련된 공식 문서(규칙, 규정, 정의, 표준, 가이드라인)를 자동으로 찾아 추천하는 스킬. 브라우징 스킬의 확장 모듈로 동작하며, 수집된 데이터의 키워드/태그를 분석하여 관련 공식 문서 링크, 요약, 적용 맥락을 제공한다. 사용자가 '관련 규정 찾아줘', '이 주제의 공식 문서는?', '어떤 표준이 적용돼?', '근거 문서 추천', '규정 레퍼런스', '법적 근거', '관련 ICAO Annex', 'FAA 규정 번호', '적용 가능한 기준' 등을 요청할 때 이 스킬을 사용한다. 항공, 법률, 기술 표준, 정부 정책 등 어떤 도메인이든 공식 출처 문서를 찾아 추천하는 요청에 반드시 이 스킬을 사용해야 한다."
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Official Document Recommender

웹에서 수집한 정보와 관련된 공식 문서(규칙, 규정, 정의, 표준)를 자동으로 찾아 추천하는 엔진.
브라우징 스킬(`web_browser_toolkit`)의 하위 확장 모듈로 설계되었으며, 단독으로도 사용 가능하다.

## 아키텍처

```
┌──────────────────────────────────────────────────────┐
│  브라우징 스킬 (web_browser_toolkit)                   │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ fetcher  │→│ 수집 JSON │→│  doc-recommender   │ │
│  │ monitor  │  │ (태그포함) │  │  (이 스킬)          │ │
│  └──────────┘  └──────────┘  └────────┬───────────┘ │
│                                       ↓              │
│                              ┌────────────────────┐  │
│                              │ 추천 결과            │  │
│                              │ - 관련 공식 문서     │  │
│                              │ - 규정 번호/링크     │  │
│                              │ - 적용 맥락 설명     │  │
│                              └────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## 워크플로우

### Step 1: 입력 분석

추천 엔진은 다음 중 하나를 입력으로 받는다:

1. **수집된 JSON 파일** — 브라우징 스킬이 생성한 JSON에서 태그/키워드 자동 추출
2. **사용자 질문** — "UAM 관련 ICAO 규정 뭐가 있어?" 같은 직접 질문
3. **URL** — 웹페이지 내용을 분석하여 관련 문서 추천
4. **키워드 목록** — 특정 키워드에 대한 공식 문서 검색

### Step 2: 키워드 추출 및 도메인 식별

입력에서 핵심 키워드를 추출하고, 어떤 도메인(항공, 법률, 기술 표준 등)에 해당하는지 식별한다.

```bash
# JSON 입력에서 키워드 추출
python3 scripts/doc_recommender.py analyze --input collection.json

# 직접 키워드 지정
python3 scripts/doc_recommender.py analyze --keywords "UAM,eVTOL,airworthiness"

# URL에서 키워드 추출
python3 scripts/doc_recommender.py analyze --url "https://www.icao.int/safety/..."
```

### Step 3: 문서 지식 베이스 매칭

추출된 키워드를 `references/doc_knowledge_base.json`의 문서 데이터베이스와 매칭한다.

지식 베이스에는 다음이 포함되어 있다:
- **항공 규정**: ICAO Annexes, FAA FARs/CFRs, EASA CS 시리즈, 국토부 고시 등
- **기술 표준**: ASTM, SAE, RTCA/DO 시리즈, EUROCAE ED 시리즈
- **국제 조약/협약**: 시카고 협약, 몬트리올 협약 등
- **가이드라인**: ICAO Doc 시리즈, FAA AC 시리즈, EASA AMC/GM 등

### Step 4: 웹 검증 및 보강

지식 베이스 매칭 결과를 웹 검색으로 검증하고, 최신 개정사항이나 추가 문서를 보강한다.

```
1. 매칭된 문서의 URL 유효성 확인 (HEAD 요청)
2. 웹 검색으로 추가 관련 문서 탐색
3. 문서 개정 이력 확인 (최신 버전인지)
4. 관련 해석 문서나 가이던스 추가 검색
```

### Step 5: 추천 결과 생성

관련도 점수 기반으로 정렬된 추천 목록을 생성한다.

**출력 형식:**

```json
{
  "query": {
    "keywords": ["UAM", "eVTOL", "airworthiness", "certification"],
    "domain": "aviation",
    "context": "eVTOL 인증 규제 조화 관련"
  },
  "recommendations": [
    {
      "rank": 1,
      "relevance_score": 0.95,
      "document": {
        "id": "ICAO-Annex-8",
        "title": "Annex 8 — Airworthiness of Aircraft",
        "type": "international_standard",
        "issuer": "ICAO",
        "latest_edition": "12th Edition, 2018 (Amendment 108)",
        "url": "https://store.icao.int/en/annex-8-airworthiness-of-aircraft",
        "status": "active"
      },
      "relevance_context": "eVTOL 항공기의 감항성 인증 기반 표준. 현재 AAM SG에서 eVTOL에 대한 갭 분석 진행 중으로, Annex 8이 전기 추진 시스템과 통합 비행 제어를 적절히 다루지 못하는 영역이 식별됨.",
      "related_documents": ["ICAO-Doc-9760", "FAA-14CFR-Part23"],
      "tags": ["airworthiness", "certification", "eVTOL", "ICAO"]
    }
  ],
  "metadata": {
    "total_recommendations": 10,
    "generated_at": "2026-04-05T16:00:00+09:00",
    "knowledge_base_version": "1.0",
    "web_verified": true
  }
}
```

---

## 도메인별 문서 체계

### 항공 (Aviation)

#### ICAO 문서 체계
| 유형 | 설명 | 예시 |
|------|------|------|
| **Annex 1-19** | SARPs (국제 표준 및 권고사항) | Annex 8: 항공기 감항성 |
| **Doc 시리즈** | 기술 문서, 매뉴얼, 가이드 | Doc 9859: 안전관리매뉴얼 |
| **PANS** | 절차서 | PANS-ATM (Doc 4444) |
| **Circular** | 회람 | Cir 328: UAS |

#### FAA 문서 체계
| 유형 | 설명 | 예시 |
|------|------|------|
| **14 CFR (FAR)** | 연방항공규정 | Part 23: 일반항공기 |
| **AC** | Advisory Circular | AC 20-193: 전기 추진 |
| **AD** | Airworthiness Directive | AD 2026-04-01 |
| **Order** | 명령 | Order 8900.1 |
| **PS-AIR** | Policy Statement | PS-AIR-21.17-01 |

#### EASA 문서 체계
| 유형 | 설명 | 예시 |
|------|------|------|
| **CS 시리즈** | Certification Specifications | CS-23, CS-VTL |
| **SC** | Special Condition | SC-VTOL-02 |
| **AMC/GM** | Acceptable Means / Guidance | AMC to Part-21 |
| **EPTS** | 환경보호 기술사양 | EPTS (소음) |

#### 기술 표준
| 유형 | 설명 | 예시 |
|------|------|------|
| **ASTM** | 미국 시험재료학회 | F3230-21a: eVTOL |
| **SAE** | 자동차공학회 (항공도 포함) | ARP4754A: 개발보증 |
| **RTCA/DO** | 항전장비 표준 | DO-178C: 소프트웨어 |
| **EUROCAE/ED** | 유럽 항전장비 표준 | ED-12C (=DO-178C) |

### 범용 도메인 확장

항공 외 도메인도 `references/doc_knowledge_base.json`에 추가하여 확장할 수 있다.
지식 베이스 구조:

```json
{
  "domains": {
    "aviation": { "issuers": {...}, "documents": [...] },
    "maritime": { "issuers": {...}, "documents": [...] },
    "automotive": { "issuers": {...}, "documents": [...] }
  }
}
```

---

## 추천 모드

### 1. 자동 추천 (브라우징 스킬 연동)

브라우징 스킬이 수집을 완료하면, 수집 JSON의 태그를 분석하여 관련 공식 문서를 자동으로 추천한다.

```bash
python3 scripts/doc_recommender.py recommend \
  --input aviation-data/collections/2026-04-05_ICAO_UAM-AAM.json \
  --output recommendations.json \
  --top 10
```

### 2. 대화형 추천 (직접 질문)

사용자가 특정 주제에 대해 질문하면 관련 문서를 추천한다.

```
사용자: "eVTOL 소음 규정은 어떤 게 있어?"

추천 결과:
1. EASA EPTS (Environmental Protection Technical Specifications)
   - eVTOL 이착륙/비행 소음 기준 정의
2. FAA 14 CFR Part 36, Subpart H & K
   - 헬기/틸트로터 소음 기준 (eVTOL 임시 적용)
3. ICAO Annex 16, Volume I — Aircraft Noise
   - 국제 항공기 소음 표준
```

### 3. 비교 추천 (규제 비교)

같은 주제에 대한 여러 기관의 문서를 비교 형태로 추천한다.

```bash
python3 scripts/doc_recommender.py compare \
  --topic "eVTOL certification" \
  --issuers "FAA,EASA,ANAC" \
  --output comparison.json
```

### 4. 이력 추적 (개정 히스토리)

특정 문서의 개정 이력과 현재 상태를 추적한다.

```bash
python3 scripts/doc_recommender.py history \
  --document "14 CFR Part 23" \
  --output history.json
```

---

## 플랫폼별 사용법

### OpenClaw
```bash
# 스킬 설치
cp -r doc-recommender/ ~/.openclaw/skills/doc-recommender/

# 사용 예시 (메신저에서)
"UAM 관련 ICAO 공식 문서 추천해줘"
"이 JSON에서 관련 규정을 찾아줘" (파일 첨부)
```

### ChatGPT
`platforms/chatgpt_prompt.md`의 시스템 프롬프트를 Custom GPT Instructions에 추가한다. Code Interpreter + Web Browsing 필요.

### Claude Cowork
이 디렉토리를 `.claude/skills/doc-recommender/`에 복사한다. WebSearch/WebFetch와 연동하여 동작.

---

## 참고 파일

- `scripts/doc_recommender.py` — 핵심 추천 엔진
- `references/doc_knowledge_base.json` — 문서 지식 베이스 (항공 도메인)
- `references/keyword_mapping.json` — 키워드-문서 매핑 테이블
- `platforms/chatgpt_prompt.md` — ChatGPT용 시스템 프롬프트
- `platforms/claude_cowork_skill.md` — Claude Cowork용 SKILL.md 변형
