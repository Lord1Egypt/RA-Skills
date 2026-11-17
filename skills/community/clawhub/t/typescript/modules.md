# Modules & Interop — Green Compile, Runtime Crash

Every bug here has the same shape: tsc type-checked one module world, Node or the bundler executed another. The type layer has no authority at runtime — align the two worlds first, then trust the types again.

## Which World You Are Actually In

- The *runtime* decides format by `package.json` `"type"` (`"module"` = `.js` files are ESM) and by extension (`.mjs`/`.cjs` always win). tsconfig's `module` controls only what tsc *emits* — a mismatch between the two is the crash.
- TypeScript mirrors the extensions: `.mts`/`.cts` compile to `.mjs`/`.cjs` regardless of `"type"`.

| Crash | Cause | Fix |
|---|---|---|
| `ERR_REQUIRE_ESM` | CJS `require()` of an ESM-only package | Dynamic `import()`, migrate the caller to ESM, or Node >=22.12 which supports `require()` of synchronous ESM |
| `x is not a function` on a default import | CJS `module.exports = fn` imported without interop | `esModuleInterop: true`, or `import * as x` |
| `exports is not defined` / `Cannot use import statement outside a module` | Emitted format ≠ what the runtime expects for that file | Align tsconfig `module` with `package.json` `"type"` |
| `Cannot find module './util'` at runtime, ESM | NodeNext requires explicit extensions on relative imports | Write `./util.js` even though the source file is `util.ts` — tsc checks it correctly |
| Same package behaves differently in two entry points | Dual-package hazard: loaded once as CJS, once as ESM — two instances, `instanceof` and singletons break | Ship ESM-only, or a thin CJS wrapper re-exporting the ESM build |

## Interop Flags

- `esModuleInterop: true` synthesizes a default export for CJS modules so `import x from "cjs"` works. Set it once, codebase-wide; flipping it mid-project changes both what compiles and what tsc emits.
- Publishing types? `export default` in a hand-written `.d.ts` interacts badly with consumers' differing interop settings — prefer named exports (declarations.md).

## Type-Only Imports

- Under `verbatimModuleSyntax` (TS >=5.0), imports are emitted exactly as written. An import used only for types but *not* marked `import type` survives to runtime — and crashes if the package is types-only or has import side effects you didn't want. `import type` guarantees elision.
- Re-exports of types need `export type { T }` — a single-file transpiler cannot know `T` was a type (below).
- `verbatimModuleSyntax` replaces the older `isolatedModules` + `importsNotUsedAsValues` hygiene; prefer it on TS >=5.0.

## The Transpile-Only Subset (`compile_pipeline: transpile-only`)

esbuild, swc, Babel, and bundler pipelines transpile one file at a time with no type information. Whole-program features break silently:

- `const enum` — values are inlined from another file's type info; single-file transpilers emit a runtime reference to an object that doesn't exist. Plain `enum` works but has runtime emit — prefer `as const` + `keyof typeof` (SKILL.md Traps).
- Type-only re-exports without `export type` — transpiler emits a runtime re-export of nothing.
- `emitDecoratorMetadata` — esbuild doesn't implement it; frameworks that rely on it (NestJS, TypeORM) need tsc or swc for that code.
- Keep `isolatedModules: true` (or `verbatimModuleSyntax`) in tsconfig so tsc flags all of the above at check time instead of your bundler at 2 a.m.

## Top-Level Await

Needs all three: ESM at runtime, `module` of `es2022`/`esnext`/`nodenext`, `target` >= `es2017`. Missing any one produces a compile error or a runtime `SyntaxError` — it is not a strictness issue.
