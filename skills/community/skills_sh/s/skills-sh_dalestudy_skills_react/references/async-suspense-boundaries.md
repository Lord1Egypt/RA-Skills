---
title: Strategic Suspense Boundaries
impact: HIGH
impactDescription: faster initial paint
tags: react, suspense, streaming, data-fetching, tanstack-query, react-router, tanstack-start
---

## Suspense 경계

데이터 페칭을 별도 컴포넌트로 분리하여 나머지 UI 즉시 표시. 전체 레이아웃이 데이터를 기다리지 않도록 함.

---

### React 19 (`use()`)

**Incorrect (전체 페이지 블로킹):**

```tsx
function Page() {
  const data = use(fetchData());
  return (
    <div>
      <Header />
      <DataDisplay data={data} />
      <Footer />
    </div>
  );
}
```

**Correct (Header, Footer 즉시 렌더링):**

```tsx
function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <Footer />
    </div>
  );
}

function DataDisplay() {
  const data = use(fetchData());
  return <div>{data.content}</div>;
}
```

**promise 공유 패턴:**

```tsx
function Page() {
  const dataPromise = fetchData();
  return (
    <div>
      <Header />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay dataPromise={dataPromise} />
        <DataSummary dataPromise={dataPromise} />
      </Suspense>
      <Footer />
    </div>
  );
}

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise);
  return <div>{data.content}</div>;
}

function DataSummary({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise);
  return <div>{data.summary}</div>;
}
```

---

### TanStack Query (`useSuspenseQuery`)

React 19 이전 또는 `use()` 없이 Suspense 사용. `data`는 타입 레벨에서 항상 정의됨 (`undefined` 체크 불필요).

```tsx
import { useSuspenseQuery } from "@tanstack/react-query";

function Page() {
  return (
    <div>
      <Header />
      <Suspense fallback={<Skeleton />}>
        <DataDisplay />
      </Suspense>
      <Footer />
    </div>
  );
}

function DataDisplay() {
  const { data } = useSuspenseQuery({
    queryKey: ["data"],
    queryFn: () => fetch("/api/data").then((res) => res.json()),
  });

  return <div>{data.content}</div>;
}
```

**여러 쿼리 병렬 실행:**

```tsx
import { useSuspenseQueries } from "@tanstack/react-query";

function Dashboard() {
  const [{ data: user }, { data: posts }] = useSuspenseQueries({
    queries: [
      { queryKey: ["user"], queryFn: fetchUser },
      { queryKey: ["posts"], queryFn: fetchPosts },
    ],
  });

  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
    </div>
  );
}
```

> `useSuspenseQuery`에서는 `enabled`, `placeholderData`, `throwOnError` 옵션 사용 불가.

---

### React Router v7 (`loader` + `Await`)

loader에서 critical 데이터는 `await`, non-critical 데이터는 promise 그대로 반환. `Await` + `Suspense`로 스트리밍.

```tsx
// routes/post.tsx
import type { Route } from "./+types/post";
import { Await } from "react-router";

export async function loader({ params }: Route.LoaderArgs) {
  // non-critical: await 하지 않음 → Suspense로 스트리밍
  const comments = getComments(params.id);

  // critical: await → 렌더링 전 완료
  const post = await getPost(params.id);

  return { post, comments };
}

export default function PostPage({ loaderData }: Route.ComponentProps) {
  const { post, comments } = loaderData;

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>

      <Suspense fallback={<CommentsSkeleton />}>
        <Await resolve={comments}>
          {(resolvedComments) => <Comments items={resolvedComments} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

> v7에서는 `defer()` 래퍼 없이 promise를 직접 반환. v6에서는 `defer()` 필수.

**여러 스트림 병렬 처리:**

```tsx
export async function loader({ params }: Route.LoaderArgs) {
  const post = await getPost(params.id);

  // 둘 다 await 하지 않음 → 병렬 스트리밍
  const comments = getComments(params.id);
  const related = getRelatedPosts(params.id);

  return { post, comments, related };
}

export default function PostPage({ loaderData }: Route.ComponentProps) {
  const { post, comments, related } = loaderData;

  return (
    <div>
      <PostContent post={post} />

      <Suspense fallback={<CommentsSkeleton />}>
        <Await resolve={comments}>
          {(data) => <Comments items={data} />}
        </Await>
      </Suspense>

      <Suspense fallback={<RelatedSkeleton />}>
        <Await resolve={related}>
          {(data) => <RelatedPosts items={data} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

---

### TanStack Start (`createServerFn` + `useSuspenseQuery`)

서버 함수로 데이터 페칭, route loader에서 `ensureQueryData`로 프리페칭, 컴포넌트에서 `useSuspenseQuery`로 소비.

```tsx
// api/posts.ts
import { createServerFn } from "@tanstack/react-start";
import { queryOptions } from "@tanstack/react-query";

const fetchPosts = createServerFn().handler(async () => {
  const res = await fetch("https://api.example.com/posts", {
    headers: { Authorization: `Bearer ${process.env.API_KEY}` },
  });
  if (!res.ok) throw new Error("Failed to fetch");
  return res.json();
});

export const postsQueryOptions = queryOptions({
  queryKey: ["posts"],
  queryFn: () => fetchPosts(),
});
```

```tsx
// routes/posts.tsx
import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { postsQueryOptions } from "../api/posts";

export const Route = createFileRoute("/posts")({
  loader: ({ context }) => {
    // 서버에서 프리페칭 → SSR 시 데이터 포함
    context.queryClient.ensureQueryData(postsQueryOptions);
  },
  component: PostsPage,
});

function PostsPage() {
  return (
    <div>
      <Header />
      <Suspense fallback={<Skeleton />}>
        <PostList />
      </Suspense>
      <Footer />
    </div>
  );
}

function PostList() {
  const { data: posts } = useSuspenseQuery(postsQueryOptions);

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

> `createServerFn`은 서버에서만 실행. API 키 등 민감 정보가 클라이언트에 노출되지 않음.

---

### Suspense 사용하지 않는 경우

- 레이아웃 결정에 필요한 데이터
- SEO 중요 콘텐츠
- 빠른 쿼리 (Suspense 오버헤드 대비 이득 없음)
- 레이아웃 시프트 방지가 중요한 경우

> 원본: [vercel-react-best-practices: async-suspense-boundaries](https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/rules/async-suspense-boundaries.md)
