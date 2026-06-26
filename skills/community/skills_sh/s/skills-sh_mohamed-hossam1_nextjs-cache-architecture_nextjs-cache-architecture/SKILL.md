---
name: nextjs-cache-architecture
description: Use this skill whenever the user wants to design or implement caching in a Next.js 16+ App Router project — setting up the "use cache" directive, building a cache tag registry, wiring mutations to invalidation utilities, structuring Suspense boundaries for partial prerendering, handling personalized content near cache boundaries, choosing cacheLife profiles, calling cacheTag / updateTag / revalidateTag correctly, migrating from unstable_cache, or debugging stale or incorrectly fresh data. Trigger even when the user only describes their domain (e.g. "I have a posts table") and asks how to cache it properly.
metadata:
  author: mohamed-hossam1
  version: 2.2.0
---

# Next.js Cache Architecture

Architect caching in a Next.js 16+ App Router project from day one — not just
dropping `"use cache"` where it happens to fit, but structuring the tag
registry, revalidation utilities, Suspense boundaries, and mutation wiring so
the cache stays correct as the codebase grows.

## How to use this skill

Apply every rule and template below to the user's actual project. Replace
placeholders like `[Entity]` and `[collection]` with names from their codebase
before writing any code.

```text
$ARGUMENTS
```

## Where to look next

Most implementations only need this file. Load a reference when the task
calls for it.

| If the user is...                                                                                       | Read                                          |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Asking how cache keys are derived, what `cacheLife` profiles mean, or hitting a `"use cache"` limitation | `references/core-concepts.md`                 |
| Caching anything that depends on a logged-in user                                                       | `references/personalized-content.md`          |
| Reporting stale data, or doing a final review pass                                                      | `references/debugging-and-checklist.md`       |
| Migrating an existing codebase off `unstable_cache`                                                     | `references/migration-from-unstable-cache.md` |

Drop-in templates in `assets/` (rename placeholders to match the user's
codebase):

- `assets/tags.ts` → `lib/cache/tags.ts`
- `assets/revalidate.ts` → `lib/cache/revalidate.ts`
- `assets/SuspenseOnSearchParams.tsx` → `components/SuspenseOnSearchParams.tsx`

## The architecture in one breath

A correct cache implementation has three load-bearing pieces. Build all three
on day one — adding them later is much harder than getting them right up
front.

1. **Tag registry** (`lib/cache/tags.ts`) — every tag string lives here. No
   raw strings anywhere else.
2. **Revalidation utilities** (`lib/cache/revalidate.ts`) — every
   `updateTag()` lives here. Mutations import from this file.
3. **Cache placement on data, not on pages** — `"use cache"` goes on
   data-fetching functions or cached child components. Page components
   orchestrate Suspense boundaries; the children fetch.

Once those three are in place, the rest is just applying them consistently.

## Step 1 — Enable Cache Components

```ts
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  cacheComponents: true,
};

export default nextConfig;
```

## Step 2 — Build the cache tag registry

**File:** `lib/cache/tags.ts` (template: `assets/tags.ts`)

Use the `assets/tags.ts` template. The `as const satisfies TagRegistry` shape
gives literal types and rejects malformed entries at compile time.

```ts
// lib/cache/tags.ts (skeleton — full template in assets/tags.ts)

export const CACHE_TAGS = {
  // Collection tags — one per logical data group, always present.
  [collection]: "[collection]",

  // Entity tag factories — only when a mutation targets a single entry.
  [entity]: (id: string | number) => `[entity]:${id}`,
} as const;
```

## Step 3 — Build revalidation utilities

**File:** `lib/cache/revalidate.ts` (template: `assets/revalidate.ts`)

All `updateTag()` calls live here. Mutations import these functions — they
never call `updateTag()` directly.

```ts
// lib/cache/revalidate.ts
"use server";

import { updateTag } from "next/cache";
import { CACHE_TAGS } from "./tags";

function updateTags(tags: string[]) {
  for (const tag of tags) updateTag(tag);
}

// Bulk — any entry in the collection changed.
export async function revalidate[Collection]Cache() {
  updateTags([CACHE_TAGS.[collection]]);
}

// Surgical — one specific entry changed.
// Only write this if `CACHE_TAGS.[entity]` factory exists in the registry.
export async function revalidate[Entity]Cache(id: string | number) {
  updateTags([
    CACHE_TAGS.[collection], // always invalidate the parent collection too
    CACHE_TAGS.[entity](id),
  ]);
}
```


## Step 4 — Implement data fetching

Place `"use cache"` in data-fetching functions. Never fetch inside page
components — page components orchestrate, they do not fetch.

```ts
// lib/data/[domain].ts
import { cacheLife, cacheTag } from "next/cache";
import { CACHE_TAGS } from "@/lib/cache/tags";

const BASE_URL = process.env.API_BASE_URL!;

// Good: collection fetch.
export async function get[Collection]() {
  "use cache";
  cacheLife("hours");
  cacheTag(CACHE_TAGS.[collection]);

  const res = await fetch(`${BASE_URL}/[endpoint]`);
  return res.json();
}

// Good: entity fetch.
export async function get[Entity](id: string) {
  "use cache";
  cacheLife("hours");
  cacheTag(CACHE_TAGS.[collection]);
  // Add CACHE_TAGS.[entity](id) only if a mutation calls updateTag on this entry.

  const res = await fetch(`${BASE_URL}/[endpoint]/${id}`);
  return res.json();
}
```

```tsx
// Bad: fetching in a page component bypasses caching and invalidation.
export default async function Page() {
  const res = await fetch("/api/items");
  const data = await res.json();
  return <View data={data} />;
}
```

## Step 5 — Structure rendering boundaries

Every page follows this shape:

```
Page component (sync, orchestration only — no data fetching)
  ├── Static shell (layout, nav — no data)
  ├── <Suspense> → cached shared content
  └── <Suspense> → dynamic personalized content
```

### Standard page

```tsx
// app/[route]/page.tsx
import { Suspense } from "react";
import { cacheLife, cacheTag } from "next/cache";
import { CACHE_TAGS } from "@/lib/cache/tags";
import { get[Collection] } from "@/lib/data/[domain]";

export default function AnyPage() {
  return (
    <>
      <StaticShell />

      <Suspense fallback={<SharedSkeleton />}>
        <SharedContent />
      </Suspense>

      <Suspense fallback={<PersonalizedSkeleton />}>
        <PersonalizedSection />
      </Suspense>
    </>
  );
}

async function SharedContent() {
  "use cache";
  cacheLife("hours");
  cacheTag(CACHE_TAGS.[collection]);

  const data = await get[Collection]();
  return <[Collection]List data={data} />;
}
```

### Dynamic route page

```tsx
// app/[domain]/[id]/page.tsx
import { Suspense } from "react";
import { cacheLife, cacheTag } from "next/cache";
import { CACHE_TAGS } from "@/lib/cache/tags";
import { get[Entity] } from "@/lib/data/[domain]";

export default function EntityPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  return (
    <Suspense fallback={<EntitySkeleton />}>
      <EntityDetail params={params} />
    </Suspense>
  );
}

async function EntityDetail({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CachedEntityView id={id} />;
}

async function CachedEntityView({ id }: { id: string }) {
  "use cache";
  cacheLife("hours");
  cacheTag(CACHE_TAGS.[collection]);
  // Add CACHE_TAGS.[entity](id) only if a mutation needs surgical invalidation.

  const item = await get[Entity](id);
  return <[Entity]View item={item} />;
}
```

### Filtered / search params page

```tsx
// app/[route]/page.tsx
import { cacheLife, cacheTag } from "next/cache";
import { CACHE_TAGS } from "@/lib/cache/tags";
import { get[Collection]ByFilter } from "@/lib/data/[domain]";
import SuspenseOnSearchParams from "@/components/SuspenseOnSearchParams";

export default function FilteredPage({
  searchParams,
}: {
  searchParams: Promise<Record<string, string>>;
}) {
  return (
    <SuspenseOnSearchParams fallback={<FilteredListSkeleton />}>
      <FilteredList searchParams={searchParams} />
    </SuspenseOnSearchParams>
  );
}

async function FilteredList({
  searchParams,
}: {
  searchParams: Promise<Record<string, string>>;
}) {
  "use cache";
  cacheLife("minutes");
  cacheTag(CACHE_TAGS.[collection]);
  // searchParams is an argument → auto-keyed per unique param combination.

  const { q = "", page = "1" } = await searchParams;
  return await get[Collection]ByFilter(q, page);
}
```

A standard `<Suspense>` does not re-trigger its fallback on client-side
navigation when only `searchParams` changes. Use `SuspenseOnSearchParams`
(template: `assets/SuspenseOnSearchParams.tsx`) on every page with search or
filter params.

## Step 6 — Handle personalized content

Read `cookies()` / `headers()` / `auth()` **outside** the cache boundary and
pass the value as a prop. The argument becomes part of the auto-generated
cache key, so each user gets their own entry. Calling any of those APIs
inside a `"use cache"` function throws or produces wrong behavior.

See `references/personalized-content.md` for the full read-outside / cache-inside
pattern and the rare `"use cache: private"` exception.

## Step 7 — Wire mutations to invalidation

Mutations call revalidation utilities and never reach for `updateTag()`
themselves. This keeps the cache layer mechanical and auditable from one
file, and lets you add observability (logging, tracing) in one place.

```ts
// app/actions/[domain].ts
"use server";

import {
  revalidate[Collection]Cache,
  revalidate[Entity]Cache,
} from "@/lib/cache/revalidate";

export async function create[Entity](payload: unknown) {
  await db.[entity].create(payload);
  await revalidate[Collection]Cache();
}

export async function update[Entity](id: string | number, payload: unknown) {
  await db.[entity].update(id, payload);
  await revalidate[Entity]Cache(id); // requires the surgical utility to be exported
}
```

### `updateTag` vs `revalidateTag`

Two APIs for two different needs:

| API                         | Effect                                                           | Call from                          |
| --------------------------- | ---------------------------------------------------------------- | ---------------------------------- |
| `updateTag(tag)`            | Immediate — the same request sees fresh data                     | Server actions, via `revalidate.ts` |
| `revalidateTag(tag, "max")` | Background stale-while-revalidate — next request sees fresh data | Route handlers, webhooks            |

`revalidateTag` always takes a second argument (`"max"` for
stale-while-revalidate, `{ expire: 0 }` for immediate hard expiry). The
single-argument form is deprecated and silently does nothing in some
configurations.

## Common mistakes

When the cache misbehaves, walk these in order. The first six catch nearly
everything; only run `next build` after the rest pass. The full debug walk
and a sign-off checklist are in `references/debugging-and-checklist.md`.

| Symptom or smell                                            | Fix                                                                          |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Function runs uncached on every request                     | `"use cache"` is after an `await` — move it to be the first statement.       |
| Cached function throws or returns wrong data per user       | Move `cookies()` / `headers()` / `auth()` outside; pass values as arguments. |
| `updateTag` does nothing                                    | Tag string typo, or no `cacheTag` ever registered the matching tag.          |
| Mutation completes but the list still reads stale           | Revalidation utility called before the write, or not called at all.          |
| Whole page re-renders even though only one section changed  | A dynamic child sits inside a cached parent — split with `<Suspense>`.       |
| Filter UI doesn't show a loading state on navigation        | Plain `<Suspense>` — switch to `SuspenseOnSearchParams`.                     |
| Page marked dynamic when you expected static                | Run `next build`; trace the leaked dynamic API in the route's source tree.   |
| Page component fetches data directly                        | Move the fetch into a cached child; pages should orchestrate, not fetch.     |

For the full debug walk and a sign-off checklist, see
`references/debugging-and-checklist.md`. To verify the static parts of a
finished implementation against the user's project, run
`scripts/audit.mjs <project-root>` — usage and what it checks are documented
in `README.md`.
