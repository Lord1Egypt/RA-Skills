# CSS 셀렉터 치트시트

웹 페이지에서 특정 요소를 추출할 때 사용하는 CSS 셀렉터 빠른 참조.

## 기본 셀렉터

| 셀렉터 | 설명 | 예시 |
|--------|------|------|
| `tag` | HTML 태그 | `h1`, `p`, `table` |
| `.class` | CSS 클래스 | `.news-item`, `.title` |
| `#id` | 요소 ID | `#main-content`, `#header` |
| `tag.class` | 태그 + 클래스 | `div.article`, `li.result` |

## 계층 셀렉터

| 셀렉터 | 설명 | 예시 |
|--------|------|------|
| `A B` | A 하위의 모든 B | `div.content p` |
| `A > B` | A의 직계 자식 B | `ul > li` |
| `A + B` | A 바로 다음의 B | `h2 + p` |
| `A ~ B` | A 이후의 모든 B | `h2 ~ p` |

## 속성 셀렉터

| 셀렉터 | 설명 | 예시 |
|--------|------|------|
| `[attr]` | 속성 존재 | `[href]`, `[data-id]` |
| `[attr="val"]` | 속성 값 일치 | `[type="text"]` |
| `[attr*="val"]` | 속성 값 포함 | `a[href*="safety"]` |
| `[attr^="val"]` | 속성 값 시작 | `a[href^="https"]` |
| `[attr$="val"]` | 속성 값 끝 | `a[href$=".pdf"]` |

## 자주 쓰는 패턴 (사이트 유형별)

### 뉴스/블로그 사이트
```
제목:    h1, .entry-title, .post-title, article h2
본문:    .entry-content, .post-body, article .content
날짜:    time, .published, .post-date, .meta-date
저자:    .author, .byline, .writer
태그:    .tags a, .categories a, .label
```

### 정부/기관 사이트
```
공지:    .board_list tr, .bbs-list li, .notice-list li
제목:    .view_title, .board_title, h3.title
날짜:    .date, .txt_date, td.date
첨부:    .file-list a, .attach a, a[href$=".pdf"]
```

### 데이터/통계 사이트
```
표:      table, .data-table, .stat-table
행:      table tr, tbody tr
셀:      td, th
차트:    .chart, canvas, svg
```

### SPA/동적 사이트 (Browser 모드에서)
```javascript
// 동적 로딩 대기 후 추출
document.querySelectorAll('.result-item')
document.querySelector('[data-testid="results"]')
document.querySelector('.infinite-scroll-component')
```

## 브라우저 개발자 도구로 셀렉터 찾기

1. 원하는 요소를 우클릭 → "검사" 선택
2. Elements 패널에서 해당 요소의 class/id 확인
3. Console에서 테스트: `document.querySelectorAll('.your-selector')`
4. 결과 개수 확인: `document.querySelectorAll('.your-selector').length`
