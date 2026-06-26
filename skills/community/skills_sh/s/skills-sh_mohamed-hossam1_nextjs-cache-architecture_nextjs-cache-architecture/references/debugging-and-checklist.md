# Debugging and Post-Implementation Checklist

Background reading for the `nextjs-cache-architecture` skill. Load this when
cache behavior is wrong — stale data, no invalidation, unexpected freshness —
or when reviewing an implementation before sign-off.

## Contents

- [Debugging order](#debugging-order)
- [Post-implementation checklist](#post-implementation-checklist)

## Debugging order

When cache behavior is wrong, walk these checks in order. The first six catch
the vast majority of issues; only run `next build` after the rest pass.

1. Is `"use cache"` the first statement in the function body, before any
   `await`? If it appears after an `await`, Next.js ignores it.
2. Is a dynamic API (`cookies`, `headers`, `auth`) called inside a cached
   function? Move the read outside and pass the value as an argument.
3. Does the collection tag in `cacheTag()` exactly match the tag string in the
   registry? A typo silently creates a separate, never-invalidated tag.
4. If surgical invalidation is needed, does the entity tag factory exist in
   `lib/cache/tags.ts`? Calling `updateTag` with a string that no `cacheTag`
   ever registered is a no-op.
5. Is the revalidation utility actually called *after* the mutation completes?
   Calling it before the write means the cache repopulates with stale data.
6. Are Suspense boundaries correctly isolating dynamic from cached sections?
   A dynamic child inside a cached parent forces the parent to re-render too.
7. Run `next build` and inspect the static vs dynamic route output. Routes
   marked dynamic that you expected to be static usually point at a leaked
   request-time API.

## Post-implementation checklist

Use this as a final review pass. Every item below should be checked off
before treating the cache architecture as production-ready.

| Check                                                                                                | Status |
| ---------------------------------------------------------------------------------------------------- | ------ |
| `next.config.ts` has `cacheComponents: true`                                                         | Yes/No |
| `lib/cache/tags.ts` has a collection tag for every data domain                                       | Yes/No |
| Entity tag factories exist only where mutations require surgical `updateTag()`                       | Yes/No |
| `lib/cache/revalidate.ts` contains all `updateTag()` calls — nowhere else                            | Yes/No |
| Every `"use cache"` function has both `cacheTag()` and `cacheLife()`                                 | Yes/No |
| `"use cache"` is the first statement in every function that uses it                                  | Yes/No |
| No dynamic request APIs (`cookies`, `headers`, `auth`) inside cached functions                       | Yes/No |
| Closure variables captured by cached functions are primitives — not whole objects or class instances | Yes/No |
| Page components are synchronous and do not fetch data                                                | Yes/No |
| `SuspenseOnSearchParams` used on every page with search or filter params                             | Yes/No |
| Mutations call revalidation utilities — never `updateTag()` directly                                 | Yes/No |
| `revalidateTag()` called with two arguments — never the deprecated single-argument form              | Yes/No |
| `next build` confirms expected static/dynamic rendering boundaries                                   | Yes/No |
