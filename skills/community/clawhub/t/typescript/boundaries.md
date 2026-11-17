# Runtime Boundaries — Where Static Types End

The checker proves nothing about data it didn't watch being constructed. Every value entering from outside is `unknown` wearing whatever type someone asserted. The discipline: validate once at the edge, then let static types carry the proof downstream (SKILL.md rule 2).

## Where the Boundaries Are

HTTP responses and request bodies · `JSON.parse` · `process.env` · `localStorage`/`sessionStorage` · database rows (unless codegen-typed from the schema) · queue messages and webhooks · file reads · `postMessage`/IPC · URL params and form data · third-party SDK callbacks typed `any`.

If you didn't construct it in this process, it crosses a boundary.

## The Pattern

1. Value enters typed `unknown` (never `as T` — that's an assertion, not a check).
2. Validate once, at the edge, producing a domain type. Prefer *parse, don't validate*: return the transformed value (dates parsed, defaults applied), not a boolean next to the raw input.
3. Downstream code is statically typed only — no re-validation, no `any`, no defensive re-checks recomputing what the checker already proved.

## Schema-First

Declare the schema as the source of truth and infer the static type from it — schema and type physically cannot drift:

```ts
const User = schema.object({ id: schema.string(), age: schema.number() });
type User = InferType<typeof User>;   // zod: z.infer · valibot: InferOutput · arktype: typeof User.infer
const user = User.parse(await res.json());   // typed User past this line, throws before it
```

- `validation_library` in config names the library for examples; the pattern is identical across zod, valibot, arktype, and ajv (+ JSON-schema-to-type tooling).
- Validate at the edge module, not in every service layer — one schema per boundary shape, exported next to its inferred type.

## Hand-Rolled Guards

- `function isUser(x: unknown): x is User` — the predicate is a promise the compiler takes on faith. When `User` gains a field, the guard silently keeps passing values that lack it. If you hand-roll: colocate guard with type and unit-test the guard, or generate it from the schema instead.
- Assertion functions — `function assertUser(x: unknown): asserts x is User` (TS >=3.7) — throw instead of branching; the right shape for startup config and invariants ("this can only be absent if the code is wrong").

## Environment Variables

- `process.env.X` is `string | undefined` — validate ALL env in one startup module, export the typed frozen result, and report every missing/invalid variable in a single error, not just the first. A container that crash-loops one missing var at a time wastes a deploy cycle per variable.
- Empty string passes `??` — decide explicitly whether `""` is a value or an absence for each variable.

## Branded Types — Making Validation Stick

```ts
declare const EmailBrand: unique symbol;
type Email = string & { [EmailBrand]: true };
const toEmail = (s: string): Email => { validate(s); return s as Email; };
```

- Only the validator mints the brand, and downstream functions accept `Email`, not `string` — an unvalidated string at a call site is now a *compile* error. The type system enforces that validation happened, not just that it exists.
- Brand where mixups are catastrophic and values share a primitive: IDs of different entities, currency amounts, sanitized vs raw HTML. Branding everything is ceremony without payoff.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `JSON.parse(s) as User` | Compiles, proves nothing; the grep-able marker of boundary debt | Parse to `unknown`, validate at the edge |
| Validating deep in the call graph | Recomputes what the checker proved; duplicate schemas drift | Edge-only; pass domain types down (SKILL.md, Where Experts Disagree) |
| Trusting your own API client types across deploys | Server and client version independently — the response type is a hope, not a contract | Validate endpoints that change shape; or generate both sides from one schema |
| Guard checks only some fields "for speed" | Passes objects that explode three layers later, far from the boundary | Full-shape validation at the edge — the cost is paid once |
