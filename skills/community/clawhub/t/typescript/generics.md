# Generic Traps

## Inference

- `useState<User>()` is `[User | undefined, ...]` — React's overload adds `undefined` for the missing initial value; pass an initial value or handle the undefined
- `<T = any>` as a default leaks `any` into every unparameterized call — default to `unknown` or a concrete safe type
- A literal object argument widens: `f({ mode: "dark" })` infers `{ mode: string }`. Fixes by version: `as const` on the argument (any TS), or `function f<const T>(x: T)` (TS >=5.0) so every call site keeps literals
- No partial type argument inference: `fn<Explicit, ???>` disables inference for ALL remaining params — curried two-call pattern: `makeClient<Api>()(config)` fixes `Api`, infers the config type
- `NoInfer<T>` (TS >=5.4): mark positions that must check against T, not contribute to it — `function fill<T>(vals: T[], fallback: NoInfer<T>)` makes a wrong fallback error instead of widening T to a union

## Constraints

- `<T extends object>` admits arrays, functions, and class instances — for plain records constrain to `Record<string, unknown>`
- `keyof T` in a generic body is `string | number | symbol` until T is constrained — `<T extends Record<string, unknown>>` gets you `string` keys
- `infer S extends string` (TS >=4.7) constrains inside conditional types — avoids a second nested conditional just to check the inferred type

## Variance

- Arrays are covariant by fiat: `Dog[]` assigns to `Animal[]`, then `animals.push(cat)` corrupts it at runtime — accept `readonly Animal[]` when you only read
- Function parameters are contravariant under `strictFunctionTypes`: `(a: Animal) => void` is NOT assignable where `(d: Dog) => void` is expected
- Method shorthand is exempt: `on(e: E): void` in an interface checks bivariantly EVEN with strictFunctionTypes — declare callbacks as properties, `on: (e: E) => void`, to get real contravariance checks
- `in`/`out` annotations (TS >=4.7) declare variance explicitly — use on recursive generic interfaces where inference of variance is slow or wrong

## Overloads

- Overloads resolve top-down, first match wins — order most-specific first; a general signature above a specific one shadows it forever with no error
- The implementation signature is invisible to callers — only the overload list is the public contract; a call that matches the implementation but no overload is an error
- `ReturnType`/`Parameters` on an overloaded function see only the last overload (→ utility-types.md) — a reason to reach for overloads late
- Same arity, related types: a generic or a union parameter beats overloads (one signature to maintain, inference still works). Overloads earn their keep when *arity* differs or when the return type depends on which argument form was used
- A conditional return type (`T extends string ? A : B`) type-checks poorly *inside* the implementation — the common pattern is overloads for the public surface + one loosely-typed implementation, with the safety burden on the overload list

## Template Literals & Key Remapping

- Template literal types (TS >=4.1) distribute over unions: `` `${"get"|"set"}${Capitalize<K>}` `` produces the full cross product — the size multiplies per slot, which is also how they blow up compile time (→ performance.md)
- Key remapping with `as` (TS >=4.1): ``{ [K in keyof T as `get${Capitalize<K & string>}`]: () => T[K] }`` — remap to `never` to drop keys, the mapped-type equivalent of `Omit` that survives unions
- `infer` inside a template literal pattern is greedy per-slot but each slot matches minimally: `` `${infer A}-${infer B}` `` on `"a-b-c"` gives `A = "a"`, `B = "b-c"` — anchor with literal separators you control
- Intrinsics `Uppercase`/`Lowercase`/`Capitalize`/`Uncapitalize` are compiler-implemented — there is no way to write custom character-level transforms; if you need one, the answer is codegen, not types

## Conditional & Mapped Types

- Naked `T` in `T extends U ? X : Y` distributes over unions: `Exclude`-style behavior whether you wanted it or not — wrap both sides `[T] extends [U]` to compare the union as one type
- `{ [K in keyof T]: X }` copies `?` and `readonly` modifiers; to strip them you need `-?` / `-readonly` explicitly
- Recursive conditional types hit the compiler's instantiation depth limit — rewrite with an accumulator parameter so the recursion is in tail position (TS >=4.5 eliminates tail calls), e.g. `Split<S, Acc extends string[] = []>`
- `Partial<T>` and `Required<T>` are shallow — nested objects keep their original optionality (→ utility-types.md)
