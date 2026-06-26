# 단순 글 발행 런북 (예시)

> 기본적인 글 하나를 발행하는 최소 워크플로우.

## 1단계: 본문 준비

```bash
# body.html 파일에 본문 HTML 작성
cat > /tmp/my-post.html << 'EOF'
<h2 data-ke-size="size26">제목</h2>
<p data-ke-size="size16">본문 내용을 여기에 작성합니다.</p>
<p data-ke-size="size16">단락은 2~4문장씩 묶어서 작성하세요.</p>
EOF
```

## 2단계: 발행

```bash
bash scripts/publish.sh \
  --title "글 제목" \
  --body-file "/tmp/my-post.html" \
  --category "카테고리명" \
  --tags "태그1,태그2,태그3" \
  --blog "your-blog.tistory.com" \
  --private
```

## 3단계: 확인

- `success: true` 확인
- 실전 발행 시 `--private` 제거

## 옵션 참고

| 옵션 | 필수 | 설명 |
|------|------|------|
| `--title` | ✅ | 글 제목 |
| `--body-file` | ✅ | 본문 HTML 파일 경로 |
| `--category` | ✅ | 카테고리 이름 (정확히 일치) |
| `--tags` | | 쉼표 구분 태그 |
| `--banner` | | 배너 이미지 파일 경로 |
| `--blog` | | 블로그 도메인 (기본: 첫 번째 블로그) |
| `--helper` | | tistory-publish.js 경로 (기본: scripts/) |
| `--private` | | 비공개 발행 |
