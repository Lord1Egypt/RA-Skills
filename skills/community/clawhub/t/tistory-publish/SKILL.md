---
name: tistory-publish
description: Automate Tistory blog publishing via OpenClaw Playwright CDP. Supports any post format — handles TinyMCE editor manipulation, OG card insertion, banner upload, tag registration, category setting, and representative image selection. Includes template presets (mk-review, simple-post). Works around Tistory's isTrusted event filtering.
runtime:
  - python3
  - playwright
  - node (optional, for banner generation)
credentials:
  - purpose: Kakao login for Tistory session recovery (used only by scripts/login.sh --cred-file)
    required: false
    format: '{"email": "...", "password": "..."}  or  email: ...\npassword: ...'
    note: Path is user-specified via --cred-file or TISTORY_CRED_FILE env var
---

# Tistory Publish

티스토리 블로그 범용 자동 발행 스킬. 어떤 형식의 글이든 자동 발행할 수 있습니다.

Tistory Open API 종료(2024.02) 이후 유일한 자동화 경로인 브라우저 자동화를 제공합니다.

## 전제 조건

- OpenClaw 브라우저 서비스 (Chrome CDP, 기본 port 18800)
- 티스토리 카카오 로그인 완료 (OpenClaw Chrome에서)
- Python 3 + Playwright (`pip install playwright`)
- Node.js 18+ (배너 생성 시, 선택)
- (선택) 카카오 자격증명 파일 — 로그인 세션 만료 시 복구용 (`scripts/login.sh --cred-file <경로>`)
  - JSON 형식: `{"email": "...", "password": "..."}`
  - 또는 key-value 형식: `email: ...\npassword: ...`
  - `publish.sh`는 자격증명을 읽지 않음 (로그인은 `login.sh`에서만 처리)

## 구조

```
tistory-publish/
├── SKILL.md                     # 이 파일
├── scripts/
│   ├── tistory-publish.js       # 코어 — 에디터 조작 함수 모음
│   ├── publish.sh               # 범용 발행 스크립트
│   └── login.sh                 # 카카오 로그인 세션 복구
└── templates/
    └── simple-post/             # 예시: 단순 글 발행
        └── RUNBOOK.md
```

## 빠른 시작

```bash
# 가장 단순한 발행
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file body.html \
  --category "카테고리명" \
  --blog "your-blog.tistory.com"

# 매경 리뷰 (템플릿 사용)
bash scripts/publish.sh \
  --template mk-review \
  --article-title "기사 제목" \
  --body-file body.html \
  --banner /tmp/banner.jpg \
  --tags "매경,경제뉴스"

# 배너 + 태그 + 비공개
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file body.html \
  --category "카테고리명" \
  --banner /tmp/banner.jpg \
  --tags "태그1,태그2,태그3" \
  --private
```

## 발행 스크립트 옵션 (`publish.sh`)

| 옵션 | 필수 | 설명 |
|------|------|------|
| `--title` | ✅ | 글 제목 |
| `--body-file` | ✅ | 본문 HTML 파일 경로 |
| `--category` | ✅ | 카테고리 이름 (에디터에 표시되는 이름 그대로) |
| `--template` | | 템플릿 preset (mk-review, simple-post) |
| `--article-title` | | mk-review용 기사 제목 (자동 날짜 접두사) |
| `--tags` | | 쉼표 구분 태그 목록 |
| `--banner` | | 배너 이미지 파일 경로 |
| `--blog` | | 블로그 도메인 (기본: tistory.com 첫 번째 블로그) |
| `--cdp-port` | | OpenClaw Chrome CDP 포트 (기본: 18800) |
| `--helper` | | tistory-publish.js 경로 (기본: scripts/ 내) |
| `--private` | | 비공개 발행 |

### 템플릿 preset

| 이름 | 카테고리 | 블로그 | 제목 형식 | 배너 |
|------|---------|--------|----------|------|
| `simple-post` | (직접 지정) | (직접 지정) | (직접 지정) | 선택 |

> 자신만의 preset을 추가하려면 `templates/` 아래에 폴더를 만들고 `publish.sh --template <이름>` 으로 사용하세요.

## 자동 처리 항목

스크립트가 순서대로 처리:

1. 새 글 페이지 열기
2. JS 헬퍼 함수 주입
3. 카테고리 선택 (ARIA combobox → Playwright click)
4. 제목 입력 (base64 디코딩으로 한글 처리)
5. 본문 HTML 삽입
6. 배너 이미지 업로드 (첨부→사진 메뉴 → file input)
7. OG 카드 생성 (placeholder URL → Enter 키 → 카드 렌더링)
8. 대표이미지 설정
9. 태그 등록
10. 발행 (공개/비공개)

## 본문 HTML 작성 규칙

- `<p data-ke-size="size16">` 태그 사용
- 단락 = 여러 문장 묶음 (`<p>` 하나에 2~4문장)
- OG 카드 위치: `<p data-og-placeholder="URL">&#8203;</p>`
- 구분선: `<hr contenteditable="false" data-ke-type="horizontalRule" data-ke-style="style1">`

## 템플릿 추가하기

`templates/` 디렉토리에 새 폴더를 만들어 자신만의 워크플로우를 추가할 수 있습니다:

```
templates/my-template/
├── RUNBOOK.md       # 발행 순서
├── TEMPLATE.md      # 원고 작성 템플릿
└── banner.js        # 배너 생성 스크립트 (선택)
```

## 주요 JS 함수 (`tistory-publish.js`)

### 콘텐츠
- `insertContent(html)` — TinyMCE에 HTML 삽입
- `buildBlogHTML({intro, articles})` — 구조화된 데이터 → HTML 변환

### OG 카드
- `getOGPlaceholders()` — placeholder URL 목록
- `prepareOGPlaceholder(url)` — placeholder → URL 텍스트 교체
- `verifyOGCard(url)` — 카드 렌더링 확인

### 메타데이터
- `setTags(tags[])` — 태그 등록
- `setRepresentImageFromEditor()` — 대표이미지 설정

### 배너
- `verifyBannerUpload()` — 업로드 확인

## 알려진 제약

- `isTrusted=false` 이벤트 무시 → OG/태그에 우회 로직 필요
- 카테고리가 ARIA combobox → Playwright click 필요
- 대표이미지 셀렉터가 Tistory 업데이트마다 변경 가능

## 변경 이력

[CHANGELOG.md](CHANGELOG.md) 참조
