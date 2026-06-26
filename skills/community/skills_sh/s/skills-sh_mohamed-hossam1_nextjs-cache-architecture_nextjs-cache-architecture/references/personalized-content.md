# Personalized Content Near Cache Boundaries

Background reading for the `nextjs-cache-architecture` skill. Load this when the
user is dealing with per-user data, cookies, headers, or auth — the most
error-prone area of `"use cache"`, because dynamic request APIs and cached
functions interact in ways that look subtle but fail loudly.

## The rule

Never call `cookies()`, `headers()`, or `auth()` inside a `"use cache"` function.
Read them outside the cache boundary and pass the derived primitives as props.
The arguments become part of the auto-generated cache key, so each user gets
their own cache entry without any manual keying.

## Pattern: read outside, cache inside

```tsx
// app/dashboard/page.tsx
import { cookies } from "next/headers";
import { cacheLife } from "next/cache";

// Good: 1. Read request-time data outside the cache boundary.
async function PersonalizedSection() {
  const cookieStore = await cookies();
  const userId = cookieStore.get("userId")?.value;

  // Good: 2. Pass as a prop — auto-included in the cache key.
  return <CachedPersonalizedView userId={userId} />;
}

// Good: 3. Cache the stable rendering, keyed per user automatically.
async function CachedPersonalizedView({
  userId,
}: {
  userId: string | undefined;
}) {
  "use cache";
  cacheLife("minutes");
  // userId is an argument → auto-keyed per user

  const data = await getPersonalizedData(userId);
  return <div>{/* render */}</div>;
}
```

## Anti-pattern

```tsx
// Bad: dynamic API inside cached function — throws or produces wrong behavior.
import { cookies } from "next/headers";

async function CachedView() {
  "use cache";
  const cookieStore = await cookies();
  return <div />;
}
```

## Exception: `"use cache: private"`

Use only when compliance requirements prevent refactoring to the props pattern
(for example, the request-time secret cannot leave a specific function for
audit reasons). The `private` variant scopes the cache to the current user
session and allows dynamic APIs inside.

```tsx
import { cookies } from "next/headers";

async function getData() {
  "use cache: private";
  const session = (await cookies()).get("session")?.value; // allowed inside private
  return fetchData(session);
}
```

Prefer the props pattern when both are viable — it shares cache entries across
identical inputs, while `private` always keeps a per-session copy.
