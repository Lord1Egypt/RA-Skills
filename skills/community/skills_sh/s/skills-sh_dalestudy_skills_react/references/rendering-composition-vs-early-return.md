---
title: Choose Between Composition and Early Returns
impact: MEDIUM
impactDescription: prevents state-crossing bugs and improves readability
tags: rendering, composition, early-return, conditional-rendering, children, pattern
---

## Composition vs Early Return 선택 기준

조건부 렌더링에서 **여러 상태(loading, error, empty, success)** 를 처리할 때 인라인 조건문 대신 early return 또는 composition 사용.

---

### 인라인 조건문의 문제

**Incorrect (상태 교차 버그 위험):**

```tsx
function ShoppingCard({ data, isPending }: Props) {
  return (
    <Card>
      <CardContent>
        {isPending ? <Skeleton /> : null}
        {!data && !isPending ? <EmptyScreen /> : null}
        {data ? (
          data.content.map((item) => (
            <ShoppingItem key={item.id} {...item} />
          ))
        ) : null}
      </CardContent>
    </Card>
  );
}
// ❌ isPending=true이면서 data가 남아있으면 Skeleton과 목록이 동시 표시
// ❌ 조건 추가할수록 조합이 기하급수적으로 증가
```

---

### Early Return: 상호 배타적 상태 처리

**Correct (early return으로 상태 분기):**

```tsx
function ShoppingCard({ data, isPending }: Props) {
  if (isPending) {
    return (
      <Card>
        <CardContent>
          <Skeleton />
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card>
        <CardContent>
          <EmptyScreen />
        </CardContent>
      </Card>
    );
  }

  // ✅ 여기서 data는 확실히 존재 (TypeScript 타입 좁히기)
  return (
    <Card>
      <CardContent>
        {data.content.map((item) => (
          <ShoppingItem key={item.id} {...item} />
        ))}
      </CardContent>
    </Card>
  );
}
```

> Early return의 장점: 상태 교차 불가, TypeScript 타입 내로잉, 각 분기가 독립적으로 읽힘.

---

### Composition: 공유 레이아웃 추출

Early return에서 레이아웃 중복이 발생하면 composition으로 해결:

```tsx
function CardLayout({ children }: { children: ReactNode }) {
  return (
    <Card>
      <CardHeading>Shopping Cart</CardHeading>
      <CardContent>{children}</CardContent>
    </Card>
  );
}

function ShoppingCard({ data, isPending }: Props) {
  if (isPending) {
    return (
      <CardLayout>
        <Skeleton />
      </CardLayout>
    );
  }

  if (!data) {
    return (
      <CardLayout>
        <EmptyScreen />
      </CardLayout>
    );
  }

  return (
    <CardLayout>
      {data.content.map((item) => (
        <ShoppingItem key={item.id} {...item} />
      ))}
    </CardLayout>
  );
}
```

---

### 인라인 조건이 괜찮은 경우: 보충 콘텐츠

상호 배타적 **상태**가 아닌 **선택적 UI**는 인라인 조건 사용:

```tsx
function ShoppingCard({ data }: Props) {
  return (
    <CardLayout>
      {/* 선택적 보충 콘텐츠 → 인라인 OK */}
      {data.assignee ? <UserInfo {...data.assignee} /> : null}
      {data.content.map((item) => (
        <ShoppingItem key={item.id} {...item} />
      ))}
    </CardLayout>
  );
}
```

---

### 선택 기준

| 상황 | 패턴 |
|------|------|
| 상호 배타적 상태 (loading / error / empty / success) | **Early return** |
| 공유 레이아웃 + 상태별 콘텐츠 | **Early return + Layout composition** |
| 선택적 보충 UI (배지, 아바타, 라벨) | **인라인 조건** (`{x ? <A /> : null}`) |
| 복잡한 슬롯 기반 레이아웃 | **children / render props** |

> 원본: [TkDodo - Component Composition is Great BTW](https://tkdodo.eu/blog/component-composition-is-great-btw)
