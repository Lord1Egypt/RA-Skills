---
name: wadiz-dm-pipeline
description: "와디즈/텀블벅 펀딩 프로젝트를 크롤링해서 달성률 50~99% 메이커에게 보낼 개인화 DM을 자동 생성하는 파이프라인. 달비님 맥에서 직접 실행. 사용 시 — 와디즈 DM 뽑아줘, 텀블벅 프로젝트 스크랩해서 DM 만들어줘, 광고 소재 서비스 DM 파이프라인 돌려줘."
---

# Wadiz DM Pipeline

와디즈/텀블벅 카테고리 페이지 크롤링 → 달성률 50~99% 필터 → 프로젝트 분석 → 개인화 DM 생성.

## 실행 방법

```bash
python3 scripts/pipeline.py [카테고리] [최대개수]
```

**카테고리 옵션:**
- `food` — 식품
- `beauty` — 뷰티
- `lifestyle` — 라이프스타일
- `fashion` — 패션
- `all` — 전체 (기본값)

**예시:**
```bash
python3 scripts/pipeline.py all 100
python3 scripts/pipeline.py beauty 50
```

## 출력

실행 후 `output/dm_results_YYYYMMDD.csv` 파일 생성:
- 프로젝트명, URL, 달성률, 카테고리
- 개인화 DM 텍스트 (즉시 복붙 가능)

## DM 오퍼 설정

`references/dm-template.md` 참조. 현재 오퍼: **무료 소재 10개 먼저 제작, 마음에 들면 결제**.

## 주의사항

- 달비님 맥 로컬에서만 실행 (서버 IP는 CDN 차단됨)
- Playwright 필요: `pip install playwright && python -m playwright install chromium`
- 과도한 요청 방지를 위해 요청 간 2~3초 딜레이 내장
- 결과 파일은 `output/` 폴더에 저장됨
