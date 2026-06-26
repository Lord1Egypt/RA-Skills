---
title: Use Iterator Helpers for Lazy Processing
impact: MEDIUM
impactDescription: avoids intermediate arrays and enables lazy evaluation
tags: js, iterator, lazy, map, filter, generator, performance
---

## Iterator Helper로 지연 처리

배열로 변환하지 않고 `Iterator.prototype`의 메서드로 직접 처리. 중간 배열 생성 없이 지연 평가(lazy evaluation).

**Incorrect (배열 변환 후 처리):**

```tsx
// NodeList → Array 변환 → 중간 배열 2개 생성
const items = Array.from(document.querySelectorAll("li"))
  .filter((el) => el.textContent?.includes("active"))
  .map((el) => el.textContent);
```

**Correct (Iterator Helper로 지연 처리):**

```tsx
// 중간 배열 없음, 필요한 만큼만 처리
const items = document.querySelectorAll("li")
  .values()
  .filter((el) => el.textContent?.includes("active"))
  .map((el) => el.textContent);

for (const text of items) {
  console.log(text);
}
```

---

### 주요 메서드

| 메서드 | 반환 | 설명 |
|--------|------|------|
| `.map(fn)` | Iterator | 각 요소 변환 |
| `.filter(fn)` | Iterator | 조건에 맞는 요소만 |
| `.take(n)` | Iterator | 처음 n개만 |
| `.drop(n)` | Iterator | 처음 n개 건너뜀 |
| `.flatMap(fn)` | Iterator | map + flatten |
| `.find(fn)` | 값 | 조건에 맞는 첫 요소 |
| `.some(fn)` | boolean | 하나라도 조건 충족? |
| `.every(fn)` | boolean | 모두 조건 충족? |
| `.reduce(fn, init)` | 값 | 누적 계산 |
| `.forEach(fn)` | undefined | 각 요소에 함수 실행 |
| `.toArray()` | Array | 배열로 변환 |

> `.map()`, `.filter()`, `.take()`, `.drop()`, `.flatMap()`은 **Iterator를 반환** → 체이닝 가능, 지연 평가.

---

### 무한 이터레이터와 take

Generator와 결합하면 무한 시퀀스에서 필요한 만큼만 추출:

```tsx
function* naturals() {
  let n = 1;
  while (true) {
    yield n++;
  }
}

// 무한 시퀀스에서 짝수 처음 5개만 추출
const firstFiveEvens = naturals()
  .filter((n) => n % 2 === 0)
  .take(5)
  .toArray();

// [2, 4, 6, 8, 10]
```

배열 메서드로는 무한 이터레이터를 처리할 수 없음. `take()`가 5개를 수집하면 즉시 중단.

---

### Map/Set 직접 처리

```tsx
const userMap = new Map([
  ["alice", { age: 30, active: true }],
  ["bob", { age: 25, active: false }],
  ["carol", { age: 35, active: true }],
]);

// ❌ 배열 변환 필요
const activeNames = Array.from(userMap.entries())
  .filter(([, user]) => user.active)
  .map(([name]) => name);

// ✅ Iterator Helper로 직접 처리
const activeNames = userMap.entries()
  .filter(([, user]) => user.active)
  .map(([name]) => name)
  .toArray();
```

---

### React에서의 활용

**큰 데이터셋 렌더링 시 중간 배열 제거:**

```tsx
function UserList({ users }: { users: Map<string, User> }) {
  return (
    <ul>
      {users.values()
        .filter((user) => user.active)
        .map((user) => <li key={user.id}>{user.name}</li>)
        .toArray()}
    </ul>
  );
}
```

**Generator 기반 페이지네이션:**

```tsx
function* paginate<T>(items: T[], pageSize: number) {
  for (let i = 0; i < items.length; i += pageSize) {
    yield items.slice(i, i + pageSize);
  }
}

// 처음 3페이지만
const firstThreePages = paginate(allItems, 20).take(3).toArray();
```

---

### Array 메서드 vs Iterator Helper

| | Array 메서드 | Iterator Helper |
|---|---|---|
| 평가 방식 | 즉시 (eager) | 지연 (lazy) |
| 중간 배열 | 매 단계 생성 | 없음 |
| 무한 시퀀스 | 불가능 | 가능 (`take` 필수) |
| 입력 타입 | Array만 | 모든 Iterator (Map, Set, Generator, NodeList) |
| 체이닝 결과 | Array | Iterator (`.toArray()`로 변환) |

> 소규모 배열(<100)에서는 차이 미미. 대규모 데이터, 다단계 체이닝, 무한 시퀀스에서 효과적.

---

### Polyfill

Iterator Helper는 ES2025에 포함. Node.js 22+, 최신 브라우저에서 네이티브 지원. 구형 환경은 polyfill 사용.

**core-js (권장):**

```bash
npm install core-js
```

```tsx
// 필요한 메서드만 import
import "core-js/actual/iterator/map";
import "core-js/actual/iterator/filter";
import "core-js/actual/iterator/take";
import "core-js/actual/iterator/to-array";

// 또는 Iterator helper 전체
import "core-js/actual/iterator";
```

**es-iterator-helpers:**

```bash
npm install es-iterator-helpers
```

```tsx
import "es-iterator-helpers/auto";
// Iterator.prototype에 자동 패치
```

**번들러 설정 (Babel + core-js):**

```json
// babel.config.json
{
  "presets": [
    ["@babel/preset-env", {
      "useBuiltIns": "usage",
      "corejs": "3.41"
    }]
  ]
}
```

> `useBuiltIns: "usage"`로 설정하면 코드에서 사용하는 Iterator Helper만 자동으로 polyfill 포함.

> 원본: [web.dev - Iterator helpers are now baseline](https://web.dev/blog/baseline-iterator-helpers)
