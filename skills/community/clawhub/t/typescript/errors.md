# Error Decoding — From Diagnostic Wall to Root Cause

Long TypeScript errors are a call stack of type comparisons. The outer lines name the assignment that failed; the deepest line names the property that caused it. Read bottom-up, always (SKILL.md rule 7).

## Reading a Long Error

1. Jump to the deepest `Types of property '...' are incompatible` — that property is the root cause; everything above is wrapper context.
2. Type printouts truncated with `...` hide the mismatch — set `noErrorTruncation: true` to see whole types, or hover both types in the editor to expand aliases.
3. If the error mentions a type parameter (`T is not assignable to ...`), the failure is at the *constraint*, not the call site — compare against `extends`, not against the instantiated type.

## Diagnostic Table

| Code | Message shape | Root cause / first move |
|---|---|---|
| TS2322 / TS2345 | not assignable (assignment / argument) | Read deepest property line; check optionality (`?` vs `\| undefined`) before structure |
| TS2339 | property does not exist | On a union: only common members are visible — narrow first. On DOM types: wrong `lib` (tsconfig.md) |
| TS18047 / TS18048 | possibly null / undefined | Narrow or `??`; if it's an index access, that's `noUncheckedIndexedAccess` working as intended |
| TS2769 | no overload matches this call | TS prints up to 3 candidate failures — find the overload matching your argument COUNT and read only its error |
| TS2589 | excessively deep / possibly infinite | Recursive conditional or exploding union — fixes below |
| TS2742 | inferred type cannot be named without a reference to ... | pnpm/monorepo symlink: annotate the export explicitly, or add the named package as a direct dependency |
| TS7053 | element implicitly has an 'any' type | Indexing with `string` into a keyed object — narrow the key (`if (k in obj)`), use `Record<K, V>`, or a `Map` |
| TS2307 | cannot find module | Resolution mismatch, not a missing file — `module`/`moduleResolution` pairing (tsconfig.md) |
| TS2688 | cannot find type definition file | Stale entry in `types: []` array — remove it or install the matching `@types` package |
| TS4023 / TS4025 | exported variable has or is using name from external module | Declaration emit can't name a private type — export the referenced type, or annotate the variable |
| Anything else | — | Reproduce in a minimal file with the two types inlined; the error usually becomes readable once aliases are gone |

## TS2589: Excessively Deep

- Cause A — recursive conditional type without tail position: rewrite with an accumulator parameter (`Split<S, Acc extends string[] = []>`) so TS >=4.5 tail-call elimination applies (generics.md).
- Cause B — distributive conditional over a huge union: every member instantiates the whole branch. Wrap `[T] extends [U]` to stop distribution, or shrink the union (performance.md).
- Cause C — a generic type applied to itself through inference. Name the intermediate type and split the computation into two aliases.

## Only in CI / Only in the Editor

| Symptom | Cause | Check |
|---|---|---|
| Editor green, CI red | Editor uses its bundled TS, CI uses the package's | "Select TypeScript Version → Use Workspace Version"; compare `tsc -v` to `package.json` |
| CI green, editor red | Stale TS server state | Restart TS Server first — it mimics every other bug |
| Errors appear after switching branches | Stale incremental cache | Delete `.tsbuildinfo` or `tsc --build --clean` |
| Works on macOS, fails on Linux | Import path differs from filename only by case | `forceConsistentCasingInFileNames` (default on since TS 5.0) catches it locally |
| New errors with no code change | `@types` drift through the lockfile | Diff the lockfile's `@types/*` and `typescript` entries against the last green build |
| CI checks files the editor never opens | Broader `include` glob in CI's tsconfig | Compare which tsconfig each side actually loads |

## Errors That "Make No Sense" (structural typing surprises)

- Two visually identical types mismatch → one has `a?: T`, the other `a: T | undefined`; under `exactOptionalPropertyTypes` (TS >=4.4) these are different types.
- Error appears inline but vanishes through a variable → excess property checking fires only on fresh object literals; the variable version is unchecked structure, not a fix (SKILL.md Traps).
- Two identical classes incompatible → `private`/`protected` members switch classes to nominal comparison; same for two separately declared enums.
- Assignment works one way but not the other → variance: function parameters are contravariant under `strictFunctionTypes` (generics.md).
