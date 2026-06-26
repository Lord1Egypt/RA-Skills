---
name: typescript-strict
description: Deep TypeScript strictness workflow—incremental enablement, compiler flags, typing boundaries, narrowing, generics, utility types, and safe refactors. Use when adopting strict mode, reducing any, or hardening large TS codebases.
---

# TypeScript Strict Mode (Deep Workflow)

Strictness is a **gradient**, not a single switch. The goal is **fewer runtime surprises** without **blocking** delivery—via **incremental** migration and **clear** typing boundaries at IO edges.

## When to Offer This Workflow

**Trigger conditions:**

- Enabling `strict`, `strictNullChecks`, `noImplicitAny`, or `noUncheckedIndexedAccess`
- Legacy codebase full of `any` and `@ts-ignore`
- Runtime bugs that types would have caught (undefined, wrong shapes)
- Library authoring needing **accurate** `.d.ts` exports

**Initial offer:**

Use **six stages**: (1) baseline & goals, (2) compiler flags roadmap, (3) boundary typing, (4) narrowing & exhaustiveness, (5) generics & patterns, (6) verify & guardrails). Confirm **TS version**, **build tool** (tsc, esbuild, etc.), and **monorepo** layout.

---

## Stage 1: Baseline & Goals

**Goal:** Know **current pain** and **target** strictness with **metrics**.

### Actions

- Capture **`tsc --noEmit`** error count and **top files** by errors
- Identify **critical** packages vs **leaf** apps for sequencing
- Define **non-goals** (e.g., “no perfect types for untyped third-party JSON this quarter”)

**Exit condition:** **Baseline** error count + **priority** directories.

---

## Stage 2: Compiler Flags Roadmap

**Goal:** Enable flags **incrementally**—fix clusters, not the whole repo at once.

### Typical order (adapt)

1. **`strictNullChecks`** (often highest value)
2. **`noImplicitAny`** on new files + ratchet old
3. **`strictFunctionTypes`**, **`strictBindCallApply`**
4. **`noUncheckedIndexedAccess`** (verbose—plan for `undefined` unions)
5. **`exactOptionalPropertyTypes`** (sharp edges—later)

### Techniques

- **`// @ts-expect-error`** with **ticket** over blind `@ts-ignore`
- **Path-specific** `tsconfig` **extends** for stricter packages
- **CI** gate: **no new** `any` in changed lines (eslint `@typescript-eslint/no-explicit-any`)

**Exit condition:** **Flag timeline** with **owners** per package.

---

## Stage 3: Boundary Typing (IO Edges)

**Goal:** **Validate** external data once; **internal** code trusts **narrowed** types.

### Patterns

- **`zod` / `io-ts` / `valibot`** for runtime parse at API boundary
- **`satisfies`** for config objects—keeps **literal** types
- **Avoid** casting from `unknown` without **validation**

### APIs

- **Generated** types from OpenAPI/graphql-codegen when possible
- **Branded types** for IDs (`type UserId = string & { __brand: 'UserId' }`) to prevent mix-ups

**Exit condition:** **New** IO code has **parse → typed** pipeline documented.

---

## Stage 4: Narrowing & Exhaustiveness

**Goal:** **Control flow** analysis works for you—**discriminated unions**, **`never` checks**.

### Practices

- **Discriminated unions** for states: `{ status: 'loading' } | { status: 'ok', data: T }`
- **`switch`** with **`assertNever(x)`** for compile-time exhaustiveness
- **Optional chaining** vs **explicit** undefined handling—be consistent in module

### Nullability

- Prefer **`undefined`** vs **`null`** **one** convention per codebase section

**Exit condition:** **Representative** modules refactored with **fewer** optional footguns.

---

## Stage 5: Generics & Patterns

**Goal:** **Reuse** without **`any`** soup—**constraints** and **defaults**.

### Guidance

- **`extends`** constraints; avoid **unconstrained** generics unless truly generic
- **Conditional types** sparingly—**readability** over cleverness in app code
- **`ReturnType` / `Parameters`** for inference glue
- **Avoid** **mutable** array inference surprises—**explicit** element types when needed

### Performance

- **Huge** mapped types can slow `tsc`—**split** types or **simplify**

**Exit condition:** **Style guide** section for generics in **shared** libraries.

---

## Stage 6: Verify & Guardrails

**Goal:** Strictness **sticks**—**regressions** caught in CI.

### CI

- **`tsc --noEmit`** required green for affected projects
- **Type-aware** ESLint rules; **pre-commit** optional
- **`dtslint`** or **tsd** for **library** typings tests when authoring packages

### Refactor safety

- **Small PRs** per module; **runtime tests** still required—types don’t replace tests

---

## Final Review Checklist

- [ ] Baseline metrics and roadmap for flags
- [ ] IO boundaries validated with schemas or codegen
- [ ] Discriminated unions / exhaustiveness for key state machines
- [ ] Generics style documented for shared code
- [ ] CI enforces typecheck on merge

## Tips for Effective Guidance

- Prefer **`unknown` over `any`**—forces **narrowing** at use site.
- When user fights **`noUncheckedIndexedAccess`**, show **helper** getters or **Record** patterns.
- **Monorepo**: align **TypeScript** version across packages—**version skew** causes phantom errors.

## Handling Deviations

- **AllowJS** mixed codebase: **typed** wrappers for critical paths first.
- **Third-party** untyped libs: **local `d.ts`** or **wrapper module** with **narrow** exports.
