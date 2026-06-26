---
title: Use URL as State
impact: MEDIUM
impactDescription: persists state across refresh, enables sharing and back navigation
tags: react, useState, url, searchParams, react-router, nuqs
---

## URL을 상태로 활용

새로고침 시 유지, 공유, 뒤로가기가 필요한 상태(정렬, 필터, 페이지네이션, 검색어)는 URL 검색 매개변수에 저장.

**Incorrect (새로고침 시 초기화):**

```tsx
function ProductList() {
  const [sort, setSort] = useState("price");
  const [filter, setFilter] = useState("all");
  // ...
}
```

---

### React Router v7

```tsx
import { useSearchParams } from "react-router";

function ProductList() {
  const [searchParams, setSearchParams] = useSearchParams();
  const sort = searchParams.get("sort") ?? "price";
  const filter = searchParams.get("filter") ?? "all";

  function updateSort(newSort: string) {
    setSearchParams((prev) => {
      prev.set("sort", newSort);
      return prev;
    });
  }
  // ...
}
```

---

### nuqs (프레임워크 비종속)

[nuqs](https://nuqs.47ng.com/)는 타입 안전한 URL 상태 관리 라이브러리. React Router, Next.js, Remix 등과 호환.

```tsx
import { useQueryState, parseAsStringEnum } from "nuqs";

const sortOptions = ["price", "name", "date"] as const;

function ProductList() {
  const [sort, setSort] = useQueryState(
    "sort",
    parseAsStringEnum(sortOptions).withDefault("price"),
  );
  const [filter, setFilter] = useQueryState("filter", { defaultValue: "all" });

  return (
    <>
      <select value={sort} onChange={(e) => setSort(e.target.value)}>
        {sortOptions.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
      {/* ... */}
    </>
  );
}
```

---

### URL 상태의 장점

- 새로고침해도 상태 유지
- URL 공유 시 동일 화면 재현
- 브라우저 뒤로가기/앞으로가기 호환
- 여러 컴포넌트에서 동일 상태 읽기 가능 (글로벌 컨텍스트처럼)

### URL 상태에 적합한 경우

| 적합 | 부적합 |
|------|--------|
| 테이블 정렬/필터 | 모달 열림/닫힘 |
| 페이지네이션 | 폼 입력 중간값 |
| 검색어 | 애니메이션 상태 |
| 탭 선택 | 드래그 위치 |

> 콜백 내에서만 URL을 읽는 경우 hook 구독 대신 직접 읽기: [`rerender-defer-reads`](rerender-defer-reads.md) 참고.

> 원본: [David Khourshid - Goodbye, useState (BeJS Conference)](https://www.youtube.com/watch?v=aGkscOKWQvQ)
