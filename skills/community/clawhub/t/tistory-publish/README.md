# tistory-publish

티스토리 블로그 범용 자동 발행 스킬. OpenClaw Playwright CDP로 TinyMCE 에디터를 조작해 어떤 형식의 글이든 자동 발행합니다.

## 왜 브라우저 자동화?

티스토리 Open API가 2024년 2월에 종료됐습니다. 공식 API 없이 발행하려면 브라우저를 직접 제어하는 수밖에 없습니다.

## 빠른 시작

```bash
# 설치
clawhub install tistory-publish

# 가장 단순한 발행
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file body.html \
  --category "카테고리명" \
  --blog "your-blog.tistory.com"
```

## 기능

- **본문 삽입**: HTML → TinyMCE 에디터 (`data-ke-*` 속성 지원)
- **OG 카드**: URL placeholder → 자동 카드 렌더링 (`isTrusted` 우회)
- **배너/이미지**: 파일 업로드 → 대표이미지 자동 설정
- **카테고리**: ARIA combobox 자동 선택
- **태그**: nativeSetter 패턴으로 `isTrusted` 필터링 우회
- **공개/비공개**: `--private` 플래그로 제어

## 구조

```
scripts/
├── tistory-publish.js    # 코어 — 에디터 조작 함수 모음
└── publish.sh            # 범용 발행 스크립트

templates/
├── mk-review/            # 예시: 신문 리뷰 (배너+OG 카드)
│   ├── RUNBOOK.md
│   ├── TEMPLATE.md
│   └── banner.js
└── simple-post/           # 예시: 단순 글 발행
    └── RUNBOOK.md
```

## 발행 옵션

| 옵션 | 필수 | 설명 |
|------|------|------|
| `--title` | ✅ | 글 제목 |
| `--body-file` | ✅ | 본문 HTML 파일 경로 |
| `--category` | ✅ | 카테고리 이름 |
| `--tags` | | 쉼표 구분 태그 |
| `--banner` | | 배너 이미지 경로 |
| `--blog` | | 블로그 도메인 |
| `--private` | | 비공개 발행 |

## 기술 스택

- **브라우저**: OpenClaw Playwright CDP (`connect_over_cdp`)
- **에디터**: TinyMCE DOM API, `setContent`, `save`, native 이벤트 보조
- **배너 생성**: Node.js Canvas (`@napi-rs/canvas`, 선택)
- **OG 카드**: JS(URL 준비) + Playwright(Enter 키) 조합
- **태그**: helper 함수 + 이벤트 디스패치

## 나만의 템플릿 만들기

`templates/` 안에 폴더를 추가하면 됩니다:

```
templates/my-template/
├── RUNBOOK.md       # 발행 순서
├── TEMPLATE.md      # 원고 작성 가이드
└── banner.js        # 배너 생성 (선택)
```

## 전제 조건

- OpenClaw 브라우저 서비스(CDP) 실행 가능 환경
- 티스토리 카카오 로그인 완료(OpenClaw Chrome)
- Python 3 + Playwright
- Node.js 18+ (배너 생성 시)

## 라이선스

MIT
