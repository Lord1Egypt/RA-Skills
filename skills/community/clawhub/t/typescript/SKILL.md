---
name: typescript
slug: typescript
version: 1.0.5
description: >-
  Writes, reviews, and debugs type-safe TypeScript: type errors, narrowing, generics, tsconfig
  strictness, and declaration files. Use when a build hits type errors ("not assignable",
  "possibly undefined", "excessively deep", "cannot find module"), when eliminating any or
  unchecked as casts, designing generics or discriminated unions, writing .d.ts files or typing
  untyped npm packages, configuring tsconfig or module resolution, fixing ESM/CJS import
  crashes ("ERR_REQUIRE_ESM", "x is not a function"), validating API or JSON data at runtime,
  migrating JavaScript to TypeScript or upgrading the TypeScript version, or when tsc or the
  editor gets slow or runs out of memory.
homepage: https://clawic.com/skills/typescript
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 🔷
    displayName: TypeScript
    configPaths:
    - ~/Clawic/data/typescript/
---

User preferences and memory live in `~/Clawic/data/typescript/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/typescript/` or `~/clawic/typescript/`), move it to `~/Clawic/data/typescript/`.

## When To Use

- Decoding type errors: "not assignable" walls, narrowing failures, inference surprises, errors that appear only in CI
- Designing types for an API surface: generics, discriminated unions, utility types, branded types
- tsconfig decisions: strict flags, module resolution, target/lib, monorepo project references, JS-to-TS migration order
- Writing or fixing declaration files (`.d.ts`, module augmentation, publishing types)
- Code that compiles green but fails at runtime — ESM/CJS interop crashes, unvalidated external data — or tsc/editor slowness
- Not for runtime JavaScript semantics (closures, event loop, coercion) — that is the javascript skill

## Quick Reference

| Situation | Play |
|---|---|
| Value of unknown shape (API, `JSON.parse`, `catch`) | `unknown` + narrow before use; never `any` |
| Config/lookup object losing literal types | `satisfies` (TS >=4.9), not a type annotation |
| Union variant not narrowing | Add a literal discriminant field + exhaustive `never` check |
| 40-line "not assignable" error | Read the deepest `Types of property ... are incompatible` line first — root cause is at the bottom; full decoder → `errors.md` |
| Cryptic diagnostic (TS2589, TS2742, "no overload matches"), error only in CI | `errors.md` |
| Generic won't infer / variance confusion / overload design | `generics.md` |
| `Partial`/`Omit`/`Record` behaving oddly | `utility-types.md` |
| Untyped npm package, globals, augmentation, publishing types | `declarations.md` |
| JS conversion, strict-flag rollout, `as` debt, TS version upgrade | `migration.md` |
| target/module/paths choices, monorepo, project references | `tsconfig.md` |
| Green compile, runtime crash (`x is not a function`, `ERR_REQUIRE_ESM`) | `modules.md` |
| External data crossing a trust boundary | Validate at runtime at the boundary; static types only downstream → `boundaries.md` |
| tsc slow, editor lag, compiler out of memory | `performance.md` |
| Anything else typed | Default: full `strict`, infer locals, annotate exports |

Depth on demand: `errors.md` diagnostic decoding · `generics.md` inference, variance, conditional types, overloads · `utility-types.md` built-in type traps · `declarations.md` .d.ts, augmentation, publishing · `migration.md` JS-to-TS, strictness ratchets, TS upgrades · `tsconfig.md` compiler configuration · `modules.md` ESM/CJS interop · `boundaries.md` runtime validation · `performance.md` compile and editor speed.

## Core Rules

1. **Full `strict` or you are reviewing half the code.** Every flag off is a bug class the checker won't report. Greenfield: `strict: true` day one plus `noUncheckedIndexedAccess` (TS >=4.1). Legacy: stage flags with a ratchet (`migration.md`).
2. **`unknown` in, typed out.** Data you didn't construct (network, JSON, env, storage) enters as `unknown` and gets validated once at the boundary (`boundaries.md`); past that point no `any` and no re-checking.
3. **Annotate exports, infer locals.** Annotated parameters and return on every exported function put errors at the boundary that caused them, not at 30 call sites downstream; inference inside bodies keeps the noise down.
4. **Make illegal states unrepresentable.** n independent optional fields admit 2^n combinations: `{ data?: T; error?: E }` is 4 states of which 2 are illegal. A discriminated union with one variant per legal state encodes exactly the truth.
5. **Every `as` carries a proof.** A cast overrides the checker — attach the runtime guard that makes it true, or a one-line comment saying why it cannot be wrong. An unexplained cast is a deferred bug report.
6. **Exhaustive by construction.** Every `switch` over a union ends in `default: x satisfies never` (TS >=4.9) — adding a variant then becomes a compile error at every site that must handle it, which is the entire point of the union.
7. **Errors read bottom-up.** The first lines of a long diagnostic are wrappers; the root cause is the deepest `Types of property ... are incompatible` line (`errors.md`).

## Stop Using `any`

- `any` is viral both directions: it silences errors on reads AND poisons everything it's assigned to. `unknown` only blocks reads until you narrow — same flexibility, none of the spread
- `catch (e)` is `unknown` under strict since TS 4.4 (`useUnknownInCatchVariables`) — check `e instanceof Error` before `.message`
- Every remaining cast (`as`) gets either a runtime guard above it or a one-line comment saying why it's safe (rule 5)
- Ratchet, don't boil the ocean: count `any`s (typescript-eslint `no-explicit-any` + `no-unsafe-*`), record the baseline, fail CI when the count rises

## Inference & Widening

Widening:

- `let x = "hello"` is `string`; `const x = "hello"` is `"hello"` — mutability drives widening
- Object and array literals widen their members even under `const`: `const cfg = { mode: "dark" }` has `mode: string` — `as const` freezes the whole tree (readonly + literals)
- Literal arguments: primitives infer as literals, objects/arrays widen — `<const T>` type parameters (TS >=5.0) preserve them at the call site
- Function return types widen too — annotate the return when a caller needs the literal

Inference limits:

- Inference flows from arguments to parameters, not through intermediate generics — when a nested generic fails, name the intermediate type and split into two steps
- No partial type argument inference: `fn<T, U>` with one explicit argument turns off inference for the rest — use the curried two-call pattern `make<T>()(config)` to fix one and infer the other
- `NoInfer<T>` (TS >=5.4) excludes a position from inference: `declare function set<T>(vals: T[], initial: NoInfer<T>): void` — without it, a wrong `initial` widens `T` instead of erroring
- Callback parameters get contextual types only when the expected signature is known — assigning the function to a typed variable or parameter is what enables `(x) =>` without annotation

## Discriminated Unions & Narrowing

Modeling with unions:

- Add a literal `kind` field to each variant — narrowing and exhaustive switches come free (rules 4 and 6)
- Discriminant must be a literal type — a field typed `string` discriminates nothing; `as const` the source values

Narrowing failures:

- `filter(Boolean)` doesn't narrow in any TS version — write `.filter((x): x is T => Boolean(x))`. TS >=5.5 infers predicates from simple lambdas, so `.filter(x => x != null)` narrows there; below 5.5 it doesn't
- Narrowing dies inside callbacks: after `if (x)`, `arr.map(() => x.foo)` re-errors because TS assumes `x` may be reassigned — copy to a `const` before the callback
- `typeof x === "object"` includes `null` — check `x !== null` in the same condition
- `Object.keys(obj)` returns `string[]`, not `keyof typeof obj` — intentional: structural types can carry extra keys. Cast only when you own the object literal
- `Array.isArray()` on `unknown` narrows to `any[]` — element type needs its own check
- `in` narrows unions only when the property appears in exactly one branch; on unlisted properties it narrows since TS 4.9
- Destructured discriminants (`const { kind } = action; if (kind === ...)`) narrow only in TS >=4.6 — on older versions switch on `action.kind` directly

## `satisfies` vs Annotation vs Cast

Three tools, three guarantees — pick by what you need to keep:

- `const x: T = v` — checks AND widens to `T`: literal info gone, excess properties rejected
- `const x = v satisfies T` (TS >=4.9) — checks compatibility, keeps the inferred narrow type: the default for config/route/theme objects
- `v as T` — checks nothing beyond rough overlap; `"hello" as number` fails but `{} as User` compiles. It's an assertion, not a conversion

## Strict Null Handling

- `??` vs `||`: `port || 3000` turns a legitimate `0` into 3000; `port ?? 3000` only replaces `null`/`undefined`. Same for `""` in string options
- Optional chaining `?.` produces `undefined`, never `null` — APIs contracted to `null` need an explicit `?? null`
- Non-null `!` is a cast in disguise — prefer early return or narrowing; each `!` is a runtime crash candidate the compiler can no longer see

## Strictness Beyond `strict`

`strict: true` is not the strictest configuration. Flags it does NOT include:

- `noUncheckedIndexedAccess` (TS >=4.1) — `arr[i]` and `record[key]` become `T | undefined`. Catches the most common real crash (indexing off the end); enable on greenfield day one, on legacy expect a large error wave and stage it
- `exactOptionalPropertyTypes` (TS >=4.4) — distinguishes "absent" from "explicitly undefined"; breaks code that assigns `undefined` to optional props
- `noPropertyAccessFromIndexSignature`, `noImplicitOverride` — cheap to adopt, low churn
- `verbatimModuleSyntax` (TS >=5.0) — forces `import type` for type-only imports; the modern replacement for `isolatedModules` import hygiene (`modules.md`)

Everything else about compiler configuration — target/lib, `module` × `moduleResolution`, paths, monorepos — lives in `tsconfig.md`; import/export mechanics and transpile-only compatibility in `modules.md`.

## Where To Annotate

- Default: annotate exported function signatures (parameters AND return), infer everything inside bodies (rule 3)
- Explicit return types on the public surface also unlock `isolatedDeclarations` (TS >=5.5) and faster declaration emit
- A type parameter must relate at least two positions (two params, or param and return). Used once, it's decoration — replace with `unknown` or the concrete type
- Slow type checking has structural causes and a measurement workflow — `performance.md`

## Output Gates

Before emitting TypeScript, verify:

- No `any` introduced, explicit or implicit — `unknown` where the shape is genuinely open?
- Exported functions annotated, parameters and return?
- Every `as` has a runtime guard above it or a justifying comment?
- Every `switch` over a union ends in an exhaustiveness check?
- External data validated at runtime before its first typed use?
- No `!` where narrowing or `??` would prove it?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/typescript/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| runtime_target | node \| browser \| bun \| deno \| isomorphic | node | Drives `module`/`moduleResolution` and lib advice in `tsconfig.md` and import-extension rules in `modules.md` |
| project_kind | app \| library | app | Library flips guidance to declaration emit, exports-map types, and wider TS-version support; app defaults to `skipLibCheck` and bundler resolution |
| compile_pipeline | tsc \| transpile-only | transpile-only | transpile-only (esbuild, swc, Babel, bundlers) enforces the single-file-safe subset: no `const enum`, `isolatedModules` rules apply (`modules.md`); tsc lifts those bans |
| validation_library | zod \| valibot \| arktype \| ajv \| none | none | Names the schema library used in boundary-validation examples (`boundaries.md`); none keeps guidance library-neutral |
| ts_version | text (e.g. "5.4") | latest | Gates every `TS >=X.Y`-marked recommendation in this skill: below the mark, the pre-version workaround is offered instead (e.g. below 4.9 an annotation replaces `satisfies`) |

Preference areas to record as the user reveals them:

- **conventions** — `interface` vs `type` default, type naming style, banned features (enums, namespaces, decorators), type-only import style
- **strictness posture** — which beyond-`strict` flags to push proactively, cast tolerance, error-suppression policy
- **tooling** — package manager, typescript-eslint strictness, monorepo layout (project references vs single config), type-test tooling
- **output format** — quick fix vs explained fix, whether to show before/after diffs

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `enum` | The one TS feature with runtime emit; `const enum` breaks under transpile-only compilers | `as const` object + `keyof typeof` (`modules.md`) |
| `Function` or `{}` as a type | `Function` accepts any callable and calls return `any`; `{}` accepts everything except `null`/`undefined` | Exact signature `(a: A) => R`; `Record<string, unknown>` for bags |
| Trusting excess property checks as validation | They fire only on fresh object literals — a value passed through a variable skips them | Runtime validation at boundaries (`boundaries.md`) |
| `// @ts-ignore` | Keeps suppressing after the error is fixed, hiding the next one | `// @ts-expect-error` (TS >=3.9) — errors itself once stale |
| `!` to silence `strictNullChecks` | Each one is an invisible cast and a crash candidate | Narrow, early-return, or `??`; sanctioned only for framework-assigned class fields (`migration.md`) |
| `[key: string]: any` to quiet index errors | Poisons every access on the object with `any` | Precise keys, `Record<K, V>`, or a `Map`; `noUncheckedIndexedAccess` (TS >=4.1) keeps even honest signatures honest |

## Where Experts Disagree

- **`interface` vs `type`.** Default: `interface` for object shapes (merges for augmentation, caches relationships for faster checking), `type` for unions, functions, tuples, and mapped/conditional results. An existing codebase convention beats either.
- **Explicit return types everywhere vs boundary-only.** Boundary-only is the default (rule 3). The everywhere school wins on published libraries and under `isolatedDeclarations` (TS >=5.5), where emit requires them anyway.
- **Runtime validation depth.** Edges-only is the default — validating internally recomputes what the checker already proved. The schema-first school (schema as source of truth, static types inferred from it) wins when one shape crosses many boundaries (`boundaries.md`).

## Related Skills

More Clawic skills, get them at https://clawic.com/skills/typescript (install if the user confirms):

- **javascript** — runtime semantics: coercion, closures, event loop
- **react** — typing components, hooks, and props in practice
- **nodejs** — Node runtime, packaging, and ESM/CJS beyond the type layer
- **deno** — TypeScript-native runtime without a build step

## Feedback

- If useful, star it: https://clawic.com/skills/typescript
- Latest version: https://clawic.com/skills/typescript

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/typescript.
