# tsconfig — The Decisions That Matter

Dozens of flags, four real decisions: where the code runs (`module` × `moduleResolution`), what syntax and APIs exist (`target`/`lib`), how strict the checker is (SKILL.md, Strictness Beyond `strict`), and whether tsc emits at all. Everything else follows from those.

## module × moduleResolution (pick by runtime, not by fashion)

| You ship via (`runtime_target`) | module | moduleResolution |
|---|---|---|
| Bundler app (Vite, webpack, esbuild) | `esnext` | `bundler` (TS >=5.0) |
| Node ESM, or a published library | `nodenext` | `nodenext` (implied — don't set it separately) |
| Legacy Node CJS you can't migrate | `commonjs` | `node10` |

- `node10` resolution cannot read `exports` maps — modern packages look like they "ship no types". The fix is your `moduleResolution`, not the package.
- Mismatched pairs (`esnext` + `node10`) are the classic broken combo: imports that resolve for the bundler but not for tsc, or vice versa.
- Import extension rules and runtime crashes that follow from this choice: modules.md.

## target and lib

- `target` downlevels *syntax* only; `lib` declares which *APIs* the checker believes exist. Nothing is polyfilled.
- "Property 'at' does not exist on type 'string[]'" with the method working at runtime = `lib` set below `es2022` — raise `lib`, don't cast.
- Server-only code: drop `"dom"` from `lib`, or `document`/`window` typos type-check silently.
- Don't downlevel for a runtime you control: modern Node takes `target: es2022` — lower targets emit helper-heavy code you then debug through.

## paths

- `paths` aliases affect *type resolution only* — the bundler/runtime needs its own alias config. Green `tsc` + "Cannot find module" at runtime is the signature of this miss.
- Since TS >=4.1 `paths` works without `baseUrl` (entries resolve relative to the tsconfig).
- In a monorepo prefer real package names + `exports` maps over `paths` — they work in every tool at once.

## Monorepos and Project References

- Per package: `composite: true`, `declaration: true`, `declarationMap: true` (go-to-definition lands in source, not in a `.d.ts`).
- Root tsconfig lists `references`; build with `tsc --build` — incremental via `.tsbuildinfo`, and only downstream of a change rebuilds.
- Each package's `include` covers only its own source. A stray glob into a sibling creates duplicate program trees and phantom "two different types with the same name" errors.
- References are also the only way to vary strictness per directory — strict config for migrated packages, loose for the legacy core (migration.md).
- Splitting one big program into references is the structural fix for slow checking and editor memory (performance.md).

## Flags People Misread

- `skipLibCheck: true` — right default for apps (checking all of node_modules' `.d.ts` is wasted work), but it also skips YOUR hand-written `.d.ts` — cover those with a test file that imports them.
- `noEmit: true` for the typecheck job; `emitDeclarationOnly: true` when a bundler produces the JS but consumers need your types.
- `incremental: true` caches in `.tsbuildinfo`; a stale cache after branch switches produces ghost errors — `tsc --build --clean` (errors.md).
- `exclude` only trims the initial file glob — an `import` pulls the excluded file straight back into the program. To truly keep code out, stop importing it.
- `outDir` never deletes stale output — an orphaned `.js` from a renamed file keeps getting imported; clean in the build script.
- `esModuleInterop`, `verbatimModuleSyntax`, `isolatedModules`: interop semantics live in modules.md.
