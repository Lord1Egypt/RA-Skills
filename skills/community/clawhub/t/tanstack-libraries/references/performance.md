# Performance

> Virtual / Pacer

---

## Virtual

Virtual scrolling (vertical/horizontal/grid).

```bash
npm i @tanstack/react-virtual  # adapters: react/vue/solid/svelte/angular/lit
```

```ts
import { useVirtualizer } from '@tanstack/react-virtual'

const virtualizer = useVirtualizer({
  count: 10000,
  getScrollElement: () => scrollRef.current,
  estimateSize: () => 35,  // or getItemSize for dynamic height
  overscan: 5,             // Number of items to render outside the viewport
})

// virtualizer.getVirtualItems() → { index, size, start }[]
// virtualizer.getTotalSize() — Total height
// Manual setting of scroll container height and item positioning required
```

**Windowed vs Non-windowed:** Virtual windowed (renders only visible items) handles millions of rows at O(rows_visible) complexity. TanStack Table supports non-windowed out of the box (O(rows_total)).

**Use cases:** Flat lists, grids, fixed/variable sizing, sticky indices, smooth scrolling, SSR compatibility.

---

## Pacer (Beta)

Debounce/throttle/rate-limit/queue/batching.

```bash
npm i @tanstack/react-pacer  # adapters: react/solid
npm i @tanstack/pacer-lite   # Framework-agnostic version
```

```ts
import { useDebouncer, useThrottler, useQueuer } from '@tanstack/react-pacer'

const debounced = useDebouncer(search, { wait: 300 })
const throttled = useThrottler(scroll, { wait: 100, leading: true })
const queued = useQueuer(save, { concurrency: 3 })
```

Function-based versions: `debounce(fn, { wait })`, `throttle(fn, { wait, leading })`, `queue(fn, { concurrency })`, `batch(fn, { wait, maxSize })`