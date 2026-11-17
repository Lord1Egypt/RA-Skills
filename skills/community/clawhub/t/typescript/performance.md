# Performance — Slow tsc, Laggy Editor, Compiler OOM

Slow checking has structural causes; the compiler will name them if you ask. Measure, find the one exploding type or the one oversized program, fix that — never sprinkle config flags hoping.

## Measure Before Touching Anything

- `tsc --extendedDiagnostics` — read *Check time* (the real work), *Types* and *Instantiations* (type-level explosion), *Memory used*.
- `tsc --generateTrace <dir>` (TS >=4.1), then `@typescript/analyze-trace` — names the exact file and type costing the time.
- Instantiations in the millions with a modest codebase = one exploding generic, not "TS is slow". The trace points at it; don't guess.
- Editor laggy but `tsc` fast = a TS-server problem, not a checker problem — see Editor Lag below.

## Cheap Wins (in order of payoff)

1. `skipLibCheck: true` — biggest single win for apps; caveat about your own `.d.ts` in tsconfig.md.
2. `incremental: true` — pays on every repeated local run; watch for stale-cache ghost errors (errors.md).
3. Stop checking what you don't ship: generated and vendored dirs out of `include` — remembering `exclude` only trims the glob; an import pulls the file back in (tsconfig.md).
4. Annotate return types on exported functions — inference across module boundaries is work the checker redoes per consumer; annotations cap it (SKILL.md rule 3 pays twice).

## Structural Causes (what the trace usually finds)

- **Giant unions** — every assignability check walks the members; a codegen'd union of thousands of string literals makes each use O(members). Collapse to `string` + a branded type (boundaries.md), or split the union by domain.
- **Deep recursive conditional types** — rewrite tail-recursive with an accumulator (generics.md); the depth-limit error is TS2589 (errors.md).
- **Long intersection chains** — `A & B & C & D` re-resolves members at every use; `interface X extends A, B` caches the flattened result. Prefer interface extension for object composition.
- **Barrel files** — one `export * from` hub pulls the entire library graph into the program when anyone imports one symbol; import from the concrete module, or split the barrel per subdomain.
- **One huge file** — after every edit the checker re-checks the containing file; a 10k-line file makes every keystroke expensive. Split by responsibility.

## Editor Lag Specifically

1. Restart TS Server first — stale server state mimics every other problem (errors.md).
2. Pin the editor to the workspace TS version — otherwise you profile a different compiler than CI runs.
3. Project too big for one server: split with project references — the editor then loads only the projects the open files belong to.
4. Auto-import suggestions scanning everything: `exports` maps in your packages shrink the surface the server indexes.

## Big Projects and CI

- Project references (tsconfig.md) turn one giant program into small ones: `tsc --build` rebuilds only downstream of a change and skips clean projects entirely.
- Take type checking off the deploy critical path: transpile with esbuild/swc (`compile_pipeline`) while `tsc --noEmit` runs as a parallel CI job. Type errors still block merge — they just don't serialize the build.
- Compiler out of memory: same structural causes at larger scale — split the program (references) before reaching for a bigger heap; a growing heap requirement is the symptom, not the problem.
- Re-run `--extendedDiagnostics` after each fix and compare Check time and Instantiations — perf work without before/after numbers is superstition.
