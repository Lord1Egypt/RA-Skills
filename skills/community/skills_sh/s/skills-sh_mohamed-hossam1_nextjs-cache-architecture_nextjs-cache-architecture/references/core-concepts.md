# Core Concepts

Background reading for the `nextjs-cache-architecture` skill. Load this when the
agent needs to explain *why* the architecture is shaped the way it is, or when
the user asks how cache keys are derived, what `cacheLife` profiles mean, or
what the hard limits of `"use cache"` are.

## Contents

- [Auto cache key generation](#auto-cache-key-generation)
- [`"use cache"` placement rules](#use-cache-placement-rules)
- [Cache duration reference](#cache-duration-reference)
- [Limitations](#limitations)

## Auto cache key generation

Next.js generates a unique cache key for every `"use cache"` function
automatically. You never construct cache keys manually.

| Component         | What it includes                                                  |
| ----------------- | ----------------------------------------------------------------- |
| Build ID          | Changes on every deploy — all caches invalidated automatically    |
| Function ID       | Hash of the function's file path and position in source           |
| Arguments         | Every value passed to the function at call time                   |
| Closure variables | Every outer-scope value captured by the function                  |

```tsx
// Good: every unique resourceId produces a separate cache entry — automatically.
async function Parent({ resourceId }: { resourceId: string }) {
  const fetchData = async (filter: string) => {
    "use cache";
    // key = [buildId] + [fn hash] + resourceId (closure) + filter (argument)
    return fetch(`/api/resources/${resourceId}?filter=${filter}`);
  };
  return fetchData("active");
}
```

Tags are for **invalidation**. Auto-keying handles **scoping**. These are
different concerns and should not be conflated.

## `"use cache"` placement rules

| Placement                             | When to use                                   |
| ------------------------------------- | --------------------------------------------- |
| Top of an async function body         | Single data-fetching function                 |
| Top of an async Server Component body | Entire component output is cacheable          |
| Never in a page component             | Page components orchestrate; they don't fetch |

`"use cache"` must be the first statement in the function body — before any
`await`. If it appears after an `await`, Next.js silently ignores it and the
function runs uncached on every request.

## Cache duration reference

| Profile     | Use when                                                    |
| ----------- | ----------------------------------------------------------- |
| `"seconds"` | Near-real-time data (live feeds, counters)                  |
| `"minutes"` | Frequently updated content (dashboards, notifications)      |
| `"hours"`   | Moderately stable content (listings, articles, configs)     |
| `"days"`    | Rarely updated content (reference data, documentation)      |
| `"max"`     | Effectively permanent (build-time constants, static assets) |

For fine-grained control, pass an object instead of a profile name:

```ts
import { cacheLife } from "next/cache";

cacheLife({
  stale: 3600,      // serve stale for up to 1 hour
  revalidate: 7200, // background revalidation every 2 hours
  expire: 86400,    // hard expiration at 1 day
});
```

## Limitations

- Edge runtime is not supported — `"use cache"` requires Node.js.
- Static export (`output: "export"`) is not supported.
- `Math.random()` and `Date.now()` inside `"use cache"` execute once at build
  time, not per request. They will appear "stuck" on a single value.
- `cacheTag()` accepts max 128 tags per call and max 256 characters per tag.
  Tags exceeding these limits are silently dropped with a console warning.

For request-time non-determinism inside cached output, defer execution with
`connection()`:

```tsx
import { connection } from "next/server";

async function DynamicContent() {
  await connection(); // defers execution to request time
  const id = crypto.randomUUID(); // different per request
  return <div>{id}</div>;
}
```
