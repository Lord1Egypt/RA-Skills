# Migrating from `unstable_cache`

Background reading for the `nextjs-cache-architecture` skill. Load this when
the user has existing code calling `unstable_cache` (Next.js 13/14/15) and
wants to move to the `"use cache"` directive on Next.js 16.

## Why migrate

`unstable_cache` is deprecated in Next.js 16. The new directive-based API
fixes three architectural issues that made `unstable_cache` painful to use
correctly:

- **Manual cache keys** were error-prone — closure variables silently leaked
  into output. The new directive auto-keys on arguments and closures.
- **String tags scattered across files** had no single source of truth.
  The architecture in `SKILL.md` centralizes them in `lib/cache/tags.ts`.
- **`revalidate` as a number on every call site** mixed lifecycle policy
  with the fetch logic. `cacheLife()` separates the two.

## The four mechanical rewrites

### 1. Function wrap → directive

```ts
// Bad: unstable_cache wrapper, manual key array.
import { unstable_cache } from "next/cache";

export const getPosts = unstable_cache(
  async () => {
    const res = await fetch(`${BASE_URL}/posts`);
    return res.json();
  },
  ["posts"],            // cache key — repeated everywhere
  { tags: ["posts"], revalidate: 3600 },
);
```

```ts
// Good: directive at the top of the function body.
import { cacheLife, cacheTag } from "next/cache";
import { CACHE_TAGS } from "@/lib/cache/tags";

export async function getPosts() {
  "use cache";
  cacheLife("hours");
  cacheTag(CACHE_TAGS.posts);

  const res = await fetch(`${BASE_URL}/posts`);
  return res.json();
}
```

### 2. Manual key array → auto-keying

`unstable_cache` required a manual key array that had to include every
variable the function depended on. The new directive auto-derives the key
from arguments and closure variables, so the manual array goes away.

```ts
// Bad: easy to forget a variable, silently caches wrong values per user.
export const getUserPosts = unstable_cache(
  async (userId: string) => fetchUserPosts(userId),
  ["user-posts"],          // userId NOT in the key — every user shares cache
  { tags: ["posts"] },
);
```

```ts
// Good: userId is an argument, auto-included in the key.
export async function getUserPosts(userId: string) {
  "use cache";
  cacheLife("minutes");
  cacheTag(CACHE_TAGS.posts);
  return fetchUserPosts(userId);
}
```

### 3. `revalidate: number` → `cacheLife()`

| Old `unstable_cache` option   | New equivalent                       |
| ----------------------------- | ------------------------------------ |
| `{ revalidate: 60 }`          | `cacheLife("minutes")`               |
| `{ revalidate: 3600 }`        | `cacheLife("hours")`                 |
| `{ revalidate: 86400 }`       | `cacheLife("days")`                  |
| `{ revalidate: false }`       | `cacheLife("max")`                   |
| Custom number                 | `cacheLife({ revalidate, expire })`  |

See `references/core-concepts.md` for the full profile table.

### 4. `tags: [...]` option → `cacheTag()`

```ts
// Bad: string literals scattered in option objects, no central registry.
unstable_cache(fn, key, { tags: ["posts", `post:${id}`] });
```

```ts
// Good: centralized tags, registry-derived.
"use cache";
cacheLife("hours");
cacheTag(CACHE_TAGS.posts, CACHE_TAGS.post(id));
```

## Common gotchas during migration

- **Closures that worked before may now fail** — `"use cache"` cannot capture
  non-serializable values (class instances, functions, request-time symbols).
  If your `unstable_cache` body referenced `db.client` from an outer scope,
  pass the data the function needs as an explicit argument instead.
- **`cookies()` / `headers()` inside the function body throws.** Move the
  read above the call site and pass the value as an argument. See
  `references/personalized-content.md` for the full pattern.
- **`Math.random()` and `Date.now()` inside the function body run once, at
  build time.** If `unstable_cache` happened to mask this (because each cache
  miss re-ran it), the directive will surface the bug. Defer with
  `await connection()` if request-time non-determinism is required.
- **`revalidatePath()` callers do not need to change**, but consider whether
  `revalidateTag()` (with the second-argument form) is a better fit now that
  tags are centralized.

## Order of operations

1. Add `cacheComponents: true` to `next.config.ts`.
2. Create `lib/cache/tags.ts` with collection tags for every domain that
   currently appears in `unstable_cache` calls.
3. Create `lib/cache/revalidate.ts` and move every `revalidateTag()` call
   into it (the centralization step from `SKILL.md`).
4. Migrate one fetcher at a time. Run `next build` after each — it surfaces
   broken closures and dynamic-API leaks immediately.
5. Delete the now-unused `unstable_cache` imports.
6. Run `scripts/audit.mjs` (if shipped with this skill) to confirm no raw
   `updateTag(` / `revalidateTag(` calls remain outside `revalidate.ts`.
