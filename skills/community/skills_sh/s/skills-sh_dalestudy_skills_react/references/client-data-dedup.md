---
title: Deduplicate Client Data Fetching
impact: MEDIUM-HIGH
impactDescription: automatic deduplication, caching, revalidation
tags: client, data-fetching, deduplication, tanstack-query, swr, cache
---

## 클라이언트 데이터 페칭 중복 제거

동일 데이터를 여러 컴포넌트에서 fetch하면 중복 요청 발생. 데이터 페칭 라이브러리로 자동 중복 제거, 캐싱, 재검증.

---

### 문제: 수동 fetch의 중복

**Incorrect (컴포넌트마다 독립 fetch):**

```tsx
function UserAvatar() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("/api/user").then((r) => r.json()).then(setUser);
  }, []);
  return <img src={user?.avatar} />;
}

function UserName() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch("/api/user").then((r) => r.json()).then(setUser);
  }, []);
  return <span>{user?.name}</span>;
}

// 같은 페이지에서 두 컴포넌트 사용 → /api/user 2번 호출
```

---

### TanStack Query

```tsx
import { useQuery } from "@tanstack/react-query";

function useUser() {
  return useQuery({
    queryKey: ["user"],
    queryFn: () => fetch("/api/user").then((r) => r.json()),
  });
}

function UserAvatar() {
  const { data: user } = useUser();
  return <img src={user?.avatar} />;
}

function UserName() {
  const { data: user } = useUser();
  return <span>{user?.name}</span>;
}

// 같은 queryKey → 요청 1번, 결과 공유
```

**변경 불가 데이터 (재검증 불필요):**

```tsx
const { data } = useQuery({
  queryKey: ["config"],
  queryFn: fetchConfig,
  staleTime: Infinity, // 캐시 만료 없음
});
```

**뮤테이션 후 자동 갱신:**

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function UpdateButton() {
  const queryClient = useQueryClient();
  const { mutate } = useMutation({
    mutationFn: updateUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });

  return <button onClick={() => mutate({ name: "New Name" })}>Update</button>;
}
```

> Suspense 통합은 [`async-suspense-boundaries`](async-suspense-boundaries.md) 참고.

---

### SWR

```tsx
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((r) => r.json());

function UserAvatar() {
  const { data: user } = useSWR("/api/user", fetcher);
  return <img src={user?.avatar} />;
}

function UserName() {
  const { data: user } = useSWR("/api/user", fetcher);
  return <span>{user?.name}</span>;
}

// 같은 키 → 요청 1번, 결과 공유
```

**변경 불가 데이터:**

```tsx
import useSWRImmutable from "swr/immutable";

const { data } = useSWRImmutable("/api/config", fetcher);
```

**뮤테이션:**

```tsx
import useSWRMutation from "swr/mutation";

function UpdateButton() {
  const { trigger } = useSWRMutation("/api/user", updateUser);
  return <button onClick={() => trigger()}>Update</button>;
}
```

---

### React Router v7: clientLoader

라우트 레벨에서 데이터 페칭. 컴포넌트에 `useState`/`useEffect` 없이 loader가 데이터 제공.

```tsx
// routes/users.tsx
import type { Route } from "./+types/users";

export async function clientLoader({}: Route.ClientLoaderArgs) {
  const res = await fetch("/api/users");
  if (!res.ok) throw new Response("Failed", { status: res.status });
  return { users: await res.json() };
}

export default function UsersPage({ loaderData }: Route.ComponentProps) {
  const { users } = loaderData;
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**TanStack Query와 결합 (캐싱 + 중복 제거):**

```tsx
import type { Route } from "./+types/users";
import { useQuery } from "@tanstack/react-query";

const usersQueryOptions = {
  queryKey: ["users"],
  queryFn: () => fetch("/api/users").then((r) => r.json()),
};

export async function clientLoader({ context }: Route.ClientLoaderArgs) {
  // loader에서 프리페칭 → 컴포넌트 즉시 렌더링
  await context.queryClient.ensureQueryData(usersQueryOptions);
  return null;
}

export default function UsersPage() {
  const { data: users } = useQuery(usersQueryOptions);
  return (
    <ul>
      {users?.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

> `clientLoader`는 클라이언트 네비게이션 시 실행. SSR이 필요하면 `loader` (서버) 사용.

---

### 선택 기준

| 기준 | TanStack Query | SWR |
|------|---------------|-----|
| 번들 크기 | ~39KB | ~12KB |
| Suspense 지원 | `useSuspenseQuery` | `{ suspense: true }` |
| 뮤테이션 | `useMutation` + 자동 무효화 | `useSWRMutation` |
| DevTools | 내장 | 플러그인 |
| 프레임워크 | React, Vue, Solid, Angular | React 전용 |
| Optimistic update | 내장 지원 | 수동 구현 |

둘 다 동일 키 기반 중복 제거, 캐싱, 백그라운드 재검증 제공.

> 원본: [vercel-react-best-practices: client-swr-dedup](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/client-swr-dedup.md)
