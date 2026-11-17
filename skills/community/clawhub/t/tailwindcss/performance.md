# Performance — Build Speed And Bundle Size

Tailwind's cost is proportional to how much it has to **scan**, not to how many classes you write. Almost every performance report resolves to a scan-scope problem.

## Diagnose Before Optimizing

1. Measure the CSS artifact: size on disk, and gzipped. Also count rules — `grep -o '{' dist/app.css | wc -l` — a rule count in the tens of thousands with a small app means generation ran wild. Not `grep -c`: that counts matching *lines*, and minified CSS is one line, so it answers 1 for every artifact.
2. Measure the build: time a cold build and an incremental rebuild separately. They have different causes.
3. Look at what got scanned: temporarily narrow the sources to one directory and rebuild. A large drop names the culprit directory.

Rough expectations: an application-sized project's minified CSS lands in the single-digit to low-tens of KB gzipped. Hundreds of KB means a pattern safelist or a source that swept a dependency tree; a few hundred bytes means nothing was scanned at all.

## Bundle Size

| Cause | Signature | Fix |
|---|---|---|
| Pattern safelist (`/bg-.*/`) | Every shade of every color present in the output | Enumerate real classes; anchor regexes (`^…$`) |
| A source glob covering `node_modules` or `dist` | Rule count explodes; build time also up | Narrow `@source` / `content` to source directories |
| Two Tailwind entrypoints in one document | Utilities appear twice in the artifact | One stylesheet per rendered document; two imports ship two utility layers |
| Near-duplicate arbitrary values | `w-[301px]`, `w-[302px]`, … each its own rule | Promote to tokens, or use inline `style` for continuous values |
| A component library shipping its own Tailwind build | Two utility layers, one wins, both download | Consume its source and let your build generate once |
| `@theme` importing an entire token package | Hundreds of unused variables in `:root` | Import only the namespaces in use |

Compression matters more than raw size here: utility CSS is extremely repetitive, so gzip and brotli do unusually well on it. Judge the transferred size, not the file size.

## Build And Rebuild Speed

- v4's engine is a large step up on v3 — Tailwind's own published benchmark reports full builds several times faster and incremental rebuilds with no new CSS effectively instant. If your incremental rebuilds are slow, the scan scope is wrong, not the engine.
- Cold builds scale with files scanned. A `@source` pointing at a monorepo root walks every package on every build.
- v4 respects `.gitignore` and skips binaries and `node_modules` by default. Undoing that with a broad `@source "../"` is the usual self-inflicted slowdown.
- v3 with a glob like `./**/*` walks the entire tree including build output — restrict to source directories and list extensions.
- The Vite plugin is faster than the PostCSS route; if the project already builds with Vite, the plugin is free speed.
- Restart the dev server after changing source configuration; a stale watcher looks identical to a slow build.
- Fresh-checkout CI builds have no cache by definition. Cache `node_modules` and the framework's own build cache; Tailwind itself has little to cache beyond that.

## Runtime Cost

- Utility CSS is parsed once and matched cheaply — a large class attribute costs nothing at runtime. Long class strings are a readability problem, not a performance one.
- What does cost: `twMerge` on every render of a large list. Memoize the class string, or use a static string where no override is possible.
- `backdrop-blur` and large `shadow` on many elements are paint costs and have nothing to do with Tailwind; the fix is fewer blurred surfaces, not fewer classes.
- `**:` (all descendants) and heavy `:has()` usage generate expensive selectors on large, frequently-mutating DOMs — the only Tailwind features with a real style-recalculation cost. Confirm with a devtools performance trace before rewriting anything.
- The browser build compiles Tailwind in the page on every load. That is a real runtime cost and the reason it never ships (SKILL.md Traps).

## Editor Responsiveness

- IntelliSense scanning a monorepo root is slow for the same reason the build is; point it at the app's CSS entrypoint or config explicitly.
- Very long class attributes slow some editors' syntax highlighting more than they slow anything else — another argument for a component over a 40-class `div`.

## Guardrails Worth Adding

- A CI check that fails when the built CSS crosses a size ceiling you set. It catches an accidental safelist or a widened source the day it lands, not at the next audit.
- A floor as well as a ceiling: an artifact suddenly under a few KB means scanning broke and the site ships unstyled.
- Record the artifact size in the build log so a regression is a diff, not an investigation.

