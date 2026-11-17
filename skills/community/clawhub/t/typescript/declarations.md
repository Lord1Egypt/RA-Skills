# Declaration File Traps

## Typing an Untyped Package

1. Check first: `@types/<pkg>` on DefinitelyTyped, or a `types`/`typings` field the package ships but your resolution misses (moduleResolution, → tsconfig.md) — writing types that already exist is the most common waste here
2. Unblock in one line: `declare module "pkg";` in any included `.d.ts` — every import becomes `any`. A tourniquet, not a fix; pair it with a TODO the ratchet counts (→ migration.md)
3. Real shim: `declare module "pkg" { export function f(x: string): number }` — type only the members you call, add as usage grows; wrong-but-narrow beats right-but-`any`
4. Placement: the file just has to be in the program (`include` glob covers it, e.g. `src/types/pkg.d.ts`); no import needed — and remember an accidental top-level import flips the file to module semantics (next section) and the `declare module` stops applying
5. Types worth keeping → PR to DefinitelyTyped; local shims rot silently when the package updates

## Script vs Module (the invisible switch)

- A `.d.ts` with no top-level `import`/`export` is a global SCRIPT: everything it declares pollutes global scope. Add `export {}` to force module semantics — this one line flips the meaning of the whole file
- In a module file, globals need `declare global { ... }`; outside a module, `declare global` is an error — the two failure modes mirror each other
- `declare const`/`declare function` at top level of a script file creates real globals that can collide with DOM lib names — check `lib.dom.d.ts` before naming

## Augmentation

- `declare module "x"` needs the EXACT resolved specifier — `"lodash"` and `"lodash/fp"` are different modules; augmenting the wrong one silently does nothing
- Augmentation MERGES: you can add members to an existing interface but never change an existing property's type — attempts produce "subsequent declarations must have the same type", and the fix is a wrapper type, not a fight with the augmentation
- Only `interface` merges across files — `type` aliases are closed. Libraries that intend augmentation (Express `Request`, theme objects) expose interfaces for exactly this reason
- `declare module "*.svg"` types EVERY .svg import identically — fine for asset URLs, wrong when one loader returns components and another returns strings

## Resolution And Publishing

- `paths` aliases affect type checking only, never the runtime — full treatment in tsconfig.md
- Publishing a package: in the `exports` map, the `"types"` condition must come FIRST in each entry — conditions match in order, and a `"default"` before `"types"` makes consumers lose your types
- `@types/x` versions pair by major/minor with the package, not patch — a mismatch shows up as methods that exist at runtime but not in the types (or vice versa); check the DefinitelyTyped version before assuming the package is wrong
- Prefer named exports in hand-written `.d.ts` — `export default` interacts badly with `esModuleInterop` differences between consumers
- Generating types for a JS lib you control: `allowJs` + `declaration` + `emitDeclarationOnly` beats hand-maintaining a parallel `.d.ts` that drifts
- Type-test the published surface: assertions like `expectTypeOf` (vitest) or `tsd` in CI catch a widened return or a lost generic before consumers do — runtime tests can't see either
- Smoke the artifact, not the source: run `tsc` against a scratch project that installs the *packed* tarball — `exports`-map and interop mistakes only reproduce through a real install
