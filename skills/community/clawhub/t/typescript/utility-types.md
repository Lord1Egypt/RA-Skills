# Utility Type Traps

## Depth And Optionality

- `Partial<T>` and `Readonly<T>` are shallow — nested objects stay required/mutable. Deep variants must be hand-rolled recursively, and a naive `DeepPartial` also mangles `Date`, `Map`, and arrays: special-case them first
- `Required<{ a?: number }>` yields `{ a: number }` — the `-?` modifier strips `undefined` that came from optionality. But `{ a: number | undefined }` (explicit, non-optional) keeps its `undefined`: `Required` removes optionality, not declared union members
- No built-in `Mutable` — write `{ -readonly [K in keyof T]: T[K] }`

## Keys Nobody Checked

- `Pick<T, K>` constrains `K extends keyof T` and errors on typos; `Omit<T, K>` accepts ANY key — `Omit<User, "tyop">` compiles silently. Define `type StrictOmit<T, K extends keyof T> = Omit<T, K>` once and use it everywhere renames can bite
- `Omit`/`Pick` on a union does NOT distribute — `Omit<A | B, "id">` first collapses `A | B` to its common keys, destroying the union. Distribute manually: `type DistributiveOmit<T, K extends PropertyKey> = T extends unknown ? Omit<T, K> : never`
- Mapped types (so `Omit`, `Pick`, `Partial`...) keep only properties — call signatures, construct signatures, and `this` types are dropped from the result

## Record Semantics

- `Record<string, T>`: every access returns `T`, even for keys that don't exist — that's the lie `noUncheckedIndexedAccess` fixes (→ SKILL.md, Strictness Beyond `strict`)
- `Record<"a" | "b", T>` with a concrete union REQUIRES all keys — for a subset, use `Partial<Record<"a" | "b", T>>`

## Extraction Surprises

- `Extract<T, U>` with no match is `never` — no error, downstream code just stops compiling somewhere else. When the match must exist, assert it: `type Hit = Extract<Shape, { kind: "circle" }>; const _check: [Hit] extends [never] ? false : true = true`
- `ReturnType<typeof fn>` and `Parameters<typeof fn>` on an overloaded function see only the LAST overload signature — reorder overloads or type the specific call
- `ReturnType` of a generic function instantiates type params as `unknown` — capture the concrete type at a call site instead: `const r = fn(arg); type R = typeof r`
- `NonNullable<T>` strips BOTH `null` and `undefined` — to remove one, `Exclude<T, null>`
- `Awaited<T>` (TS >=4.5) unwraps recursively — `Awaited<Promise<Promise<number>>>` is `number`, matching what `await` actually does; don't expect one level
