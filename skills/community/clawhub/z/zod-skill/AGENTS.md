# Zod v4 — Complete Guide

> This document is for AI agents and LLMs to follow when writing, reviewing, or debugging Zod schemas. It compiles all rules and references into a single executable guide.

**Baseline:** zod ^4.0.0 with TypeScript ^5.5

---

## Abstract

Zod is a TypeScript-first schema validation library for runtime type checking at system boundaries — API input, form data, environment variables, external services. Use `z.infer<typeof Schema>` for type extraction, `safeParse()` for validation, and composition methods (`.pick()`, `.omit()`, `.partial()`) to derive schema variants. Zod v4 introduces breaking changes to string formats, enums, error handling, and recursive types. This guide also covers architectural placement (where to parse), schema organization, versioning strategy, and production observability.

---

## Table of Contents

1. [Parsing & Type Safety](#1-parsing--type-safety) — CRITICAL
2. [Schema Design](#2-schema-design) — CRITICAL
3. [Refinements & Transforms](#3-refinements--transforms) — HIGH
4. [Error Handling](#4-error-handling) — HIGH
5. [Performance & Composition](#5-performance--composition) — MEDIUM
6. [v4 Migration](#6-v4-migration) — MEDIUM
7. [Advanced Patterns](#7-advanced-patterns) — MEDIUM
8. [Architecture & Boundaries](#8-architecture--boundaries) — CRITICAL/HIGH
9. [Observability](#9-observability) — HIGH/MEDIUM

---

## 1. Parsing & Type Safety
**Impact: CRITICAL**

### Rule: Use safeParse() for User Input

`parse()` throws on invalid input. Use `safeParse()` which returns a discriminated result.

```typescript
// INCORRECT — try/catch is verbose and catches unrelated errors
try {
  const user = UserSchema.parse(data)
} catch (e) {
  if (e instanceof z.ZodError) { ... }
}

// CORRECT — discriminated union result
const result = UserSchema.safeParse(data)
if (!result.success) {
  console.log(result.error.issues)
} else {
  console.log(result.data)
}
```

Use `parse()` only for internal data that should never be invalid (config, constants).

### Rule: Use parseAsync for Async Refinements

When a schema has async `.refine()` or `.transform()`, sync `.parse()` throws. Must use `parseAsync()` or `safeParseAsync()`.

```typescript
const UniqueEmail = z.email().refine(
  async (email) => !(await db.users.exists({ email })),
  { error: "Email already registered" }
)

// INCORRECT — throws error with async refinement
const result = UniqueEmail.safeParse(input)

// CORRECT
const result = await UniqueEmail.safeParseAsync(input)
```

### Rule: Infer Types from Schemas

Never manually define TypeScript types alongside Zod schemas. Use `z.infer` and `z.input`.

```typescript
const UserSchema = z.object({
  name: z.string(),
  email: z.email(),
  age: z.number().min(0),
})

// Output type (after transforms)
type User = z.infer<typeof UserSchema>

// Input type (before transforms — useful for forms)
type UserInput = z.input<typeof UserSchema>
```

### Schema Types Quick Reference

| Type | Syntax |
|------|--------|
| String | `z.string()` |
| Number | `z.number()`, `z.int()`, `z.float()` |
| Boolean | `z.boolean()` |
| BigInt | `z.bigint()` |
| Date | `z.date()` |
| Literal | `z.literal("foo")`, `z.literal(42)` |
| Enum | `z.enum(["a", "b"])`, `z.enum(TSEnum)` |
| Email | `z.email()` |
| URL | `z.url()` |
| UUID | `z.uuid()` |
| String→Bool | `z.stringbool()` |
| ISO DateTime | `z.iso.datetime()` |
| File | `z.file()` |
| JSON | `z.json()` |
| Any | `z.any()` |
| Unknown | `z.unknown()` |
| Never | `z.never()` |

---

## 2. Schema Design
**Impact: CRITICAL**

### Rule: Handle Unknown Keys Explicitly

`z.object()` silently strips unknown keys. Choose the right variant:

```typescript
// z.object() — strips unknown keys (default)
const Safe = z.object({ host: z.string() })
Safe.parse({ host: "localhost", debug: true })
// { host: "localhost" } — debug is gone

// z.strictObject() — rejects unknown keys
const Strict = z.strictObject({ host: z.string() })
Strict.parse({ host: "localhost", debug: true })
// ZodError: unrecognized key "debug"

// z.looseObject() — preserves unknown keys
const Loose = z.looseObject({ host: z.string() })
Loose.parse({ host: "localhost", debug: true })
// { host: "localhost", debug: true }
```

| Variant | Unknown keys | Use when |
|---------|-------------|----------|
| `z.object()` | Strips | Sanitizing user input |
| `z.strictObject()` | Rejects | API contracts, config validation |
| `z.looseObject()` | Preserves | Proxying data, forwarding payloads |

### Rule: Use Discriminated Unions

For tagged object unions, use `z.discriminatedUnion()` instead of `z.union()`.

```typescript
// INCORRECT — sequential matching, poor error messages
const Shape = z.union([
  z.object({ type: z.literal("circle"), radius: z.number() }),
  z.object({ type: z.literal("square"), side: z.number() }),
])

// CORRECT — O(1) dispatch, targeted errors
const Shape = z.discriminatedUnion("type", [
  z.object({ type: z.literal("circle"), radius: z.number() }),
  z.object({ type: z.literal("square"), side: z.number() }),
])
```

### Rule: Coercion Pitfalls — Boolean Strings

`z.coerce.boolean()` uses JavaScript `Boolean()` — `Boolean("false")` is `true`.

```typescript
// INCORRECT — "false" becomes true
z.coerce.boolean().parse("false") // true

// CORRECT — z.stringbool() handles string booleans
z.stringbool().parse("false") // false
// Accepts: "true"/"false", "1"/"0", "yes"/"no", "on"/"off"
```

### Rule: Recursive Schema Design

Use getter pattern for recursive schemas. `z.lazy()` is removed in v4.

```typescript
// INCORRECT — z.lazy() removed in v4
const Category = z.object({
  name: z.string(),
  children: z.lazy(() => z.array(Category)),
})

// CORRECT — getter pattern
const Category = z.object({
  name: z.string(),
  get children() {
    return z.array(Category).optional()
  },
})

type Category = z.infer<typeof Category>
```

Never pass cyclical data to recursive schemas — it causes infinite loops.

---

## 3. Refinements & Transforms
**Impact: HIGH**

### Rule: Never Throw in Refinements

Refinement and transform functions must never throw. Return false or use `ctx.addIssue()`.

```typescript
// INCORRECT — bypasses Zod error handling
z.number().refine((n) => {
  if (n <= 0) throw new Error("Must be positive")
  return true
})

// CORRECT — return boolean
z.number().refine((n) => n > 0, { error: "Must be positive" })

// CORRECT — superRefine for multiple issues
z.string().superRefine((val, ctx) => {
  if (val.length < 8) {
    ctx.addIssue({ code: "custom", message: "Too short" })
  }
  if (!/[A-Z]/.test(val)) {
    ctx.addIssue({ code: "custom", message: "Needs uppercase" })
  }
})
```

### Rule: Refine for Validation, Transform for Conversion

```typescript
// INCORRECT — validation inside transform
z.string().transform((val) => {
  const n = parseInt(val, 10)
  if (isNaN(n)) throw new Error("Not a number")
  return n
})

// CORRECT — validate then transform
z.string()
  .refine((val) => !isNaN(parseInt(val, 10)), { error: "Not numeric" })
  .transform((val) => parseInt(val, 10))

// BETTER — staged parsing with pipe
z.string().pipe(z.coerce.number()).pipe(z.int())
```

### Rule: Cross-Field Validation

Use `.superRefine()` on the parent object with `path` targeting.

```typescript
const Form = z
  .object({
    password: z.string().min(8),
    confirm: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password !== data.confirm) {
      ctx.addIssue({
        code: "custom",
        path: ["confirm"],
        message: "Passwords don't match",
      })
    }
  })
```

---

## 4. Error Handling
**Impact: HIGH**

### Rule: Custom Error Messages (v4 API)

v3's `required_error`, `invalid_type_error`, `message` are removed. Use `error`.

```typescript
// INCORRECT — v3 API, silently ignored in v4
z.string({ required_error: "Required" })
z.number().min(18, { message: "Too young" })

// CORRECT — v4 error parameter
z.string({ error: "Name is required" })
z.number().min(18, { error: "Must be 18+" })
z.number().min(18, "Must be 18+") // string shorthand

// CORRECT — function form for dynamic messages
z.string({
  error: (issue) =>
    issue.input === undefined ? "Required" : "Must be a string",
})
```

### Rule: Error Formatting

```typescript
const result = schema.safeParse(data)
if (!result.success) {
  // For flat forms
  const flat = z.flattenError(result.error)
  // { formErrors: string[], fieldErrors: { email: ["Invalid"] } }

  // For nested structures
  const tree = z.treeifyError(result.error)

  // For debugging
  const pretty = z.prettifyError(result.error)
}
```

| Function | Output | Use case |
|----------|--------|----------|
| `z.flattenError()` | `{ formErrors, fieldErrors }` | Flat forms |
| `z.treeifyError()` | Nested tree | Deeply nested forms |
| `z.prettifyError()` | Human string | Logging, debugging |

### Rule: reportInput Leaks Sensitive Data

```typescript
// INCORRECT — leaks passwords, tokens into logs
schema.safeParse(data, { reportInput: true })

// CORRECT — only in development
schema.safeParse(data, {
  reportInput: process.env.NODE_ENV === "development",
})
```

---

## 5. Performance & Composition
**Impact: MEDIUM**

### Rule: Spread Over Extend

```typescript
// INCORRECT — chained .extend() is slow to compile
const Full = Base.extend({ name: z.string() })
  .extend({ email: z.email() })
  .extend({ role: z.enum(["admin", "user"]) })

// CORRECT — single object with spread
const Full = z.object({ ...Base.shape, name: z.string(), email: z.email() })
```

### Rule: Reuse Schemas with Composition

```typescript
const User = z.object({
  id: z.string(),
  name: z.string(),
  email: z.email(),
  password: z.string().min(8),
  createdAt: z.date(),
})

const UserCreate = User.omit({ id: true, createdAt: true })
const UserUpdate = User.pick({ name: true, email: true }).partial()
const UserResponse = User.omit({ password: true })
```

### Rule: Use Zod Mini for Client Bundles

```typescript
// Full Zod (~13kb gzip) — server, scripts
import { z } from "zod"

// Zod Mini (~1.88kb gzip) — client bundles
import { z } from "zod/v4/mini"

const Form = z.object({
  email: z.email(),
  password: z.string().check(z.minLength(8)),
})
```

---

## 6. v4 Migration
**Impact: MEDIUM**

### Rule: Top-Level String Formats

```typescript
// DEPRECATED — v3 chained style
z.string().email()
z.string().url()
z.string().uuid()

// v4 — top-level functions
z.email()
z.url()
z.uuid()
z.cuid()
z.ulid()
z.ipv4()
z.ipv6()
z.jwt()
z.base64()
```

### Rule: Unified z.enum()

```typescript
enum Role { Admin = "admin", User = "user" }

// REMOVED — z.nativeEnum()
z.nativeEnum(Role)

// v4 — z.enum() accepts TS enums directly
z.enum(Role)
z.enum(["active", "inactive"]) // also still works
```

### Rule: Unified Error Parameter

```typescript
// REMOVED — v3 error customization
z.string({ required_error: "...", invalid_type_error: "..." })
z.number().min(5, { message: "..." })

// v4 — unified error parameter
z.string({ error: "..." })
z.number().min(5, { error: "..." })
z.number().min(5, "...") // shorthand
```

---

## 7. Advanced Patterns
**Impact: MEDIUM**

### Rule: Branded Types

```typescript
const USD = z.number().brand<"USD">()
const EUR = z.number().brand<"EUR">()

type USD = z.infer<typeof USD> // number & { __brand: "USD" }
type EUR = z.infer<typeof EUR>

function convert(amount: USD, rate: number): EUR {
  return EUR.parse(amount * rate)
}

const price = EUR.parse(100)
convert(price, 1.1) // TypeScript error! EUR is not USD
```

### Rule: Codecs for Bidirectional Transforms

```typescript
// One-way: can't serialize back
const DateField = z.string().transform((s) => new Date(s))

// Bidirectional: parse AND serialize
const DateField = z.codec(z.iso.datetime(), z.date(), {
  decode: (s) => new Date(s),
  encode: (d) => d.toISOString(),
})

const parsed = DateField.parse("2024-01-01T00:00:00Z") // Date
const serialized = DateField.encode(parsed) // "2024-01-01T00:00:00.000Z"
```

### Rule: Pipe for Staged Parsing

```typescript
// INCORRECT — everything in one transform
z.string().transform((val) => {
  const n = parseInt(val, 10)
  if (n < 1 || n > 65535) throw new Error("Bad port")
  return n
})

// CORRECT — staged with pipe
const PortNumber = z
  .string()
  .pipe(z.coerce.number())
  .pipe(z.int().min(1).max(65535))
```

---

## 8. Architecture & Boundaries
**Impact: CRITICAL/HIGH**

### Rule: Parse at System Boundaries, Not in Domain Logic

Call `safeParse()` at entry points (API handlers, env startup, form resolvers, external fetches). Pass typed data inward. Domain logic receives typed values, never `unknown`.

```typescript
// INCORRECT — domain logic handles unknown input
function calculateDiscount(data: unknown) {
  const result = OrderSchema.safeParse(data)
  if (!result.success) throw new Error("Invalid order")
  return result.data.total > 100 ? result.data.total * 0.1 : 0
}

// CORRECT — parse at boundary, pass typed data inward
app.post("/orders", (req, res) => {
  const result = OrderSchema.safeParse(req.body)
  if (!result.success) {
    return res.status(400).json({
      errors: z.flattenError(result.error).fieldErrors,
    })
  }
  const discount = calculateDiscount(result.data) // typed Order
  res.json({ total: result.data.total - discount })
})

function calculateDiscount(order: Order): number {
  return order.total > 100 ? order.total * 0.1 : 0
}
```

| Boundary | Where to parse |
|----------|---------------|
| Express/Fastify | Route handler or validation middleware |
| tRPC | `.input(Schema)` — framework parses for you |
| Next.js Server Action | Top of action function |
| React Hook Form | `zodResolver(Schema)` |
| Env vars | At app startup (`parse()` — crash on invalid is intentional) |
| External API | After `fetch()`, before using data |

### Rule: Co-locate Schemas with Their Boundary Layer

Place schemas next to the boundary that uses them. Domain types use `z.infer`, never re-export raw schemas across layers.

```typescript
// INCORRECT — everything in one folder
src/schemas/user.ts      // who uses this?
src/schemas/order.ts
src/schemas/config.ts

// CORRECT — co-located with boundaries
src/api/users/schemas.ts     // API request/response schemas
src/features/profile/form-schema.ts  // form validation
src/config/env.ts            // env parsing
src/domain/types.ts          // z.infer types only
```

### Rule: Evolve Schemas Without Breaking Consumers

Additive changes only for non-breaking evolution. New fields use `.optional()`. Never remove required fields without a major version bump.

```typescript
// INCORRECT — removing role breaks consumers silently
const UserV2 = z.object({ name: z.string(), email: z.email() })
// role is gone — consumers get undefined

// CORRECT — keep role, add new field as optional
const UserV2 = z.object({
  name: z.string(),
  email: z.email(),
  role: z.enum(["admin", "user"]),       // kept
  displayName: z.string().optional(),    // new, optional
})
```

| Change | Breaking? |
|--------|-----------|
| Add optional field | No |
| Add required field | **Yes** |
| Remove field | **Yes** |
| Tighten constraint | **Yes** |
| Loosen constraint | No |
| Add union member | No |
| Remove union member | **Yes** |

---

## 9. Observability
**Impact: HIGH/MEDIUM**

### Rule: Log Structured Errors, Not Raw ZodError

Use `z.flattenError()` for compact, structured logs with request correlation IDs. Never log raw ZodError objects.

```typescript
// INCORRECT — raw ZodError is noisy and unqueryable
logger.error("Validation failed", { error: result.error })

// CORRECT — structured, compact, queryable
const flat = z.flattenError(result.error)
logger.warn("validation_failed", {
  requestId: req.id,
  schema: "UserSchema",
  path: req.path,
  formErrors: flat.formErrors,
  fieldErrors: flat.fieldErrors,
})
```

### Rule: Track Validation Error Rates per Schema and Field

Wrap `safeParse` in a tracked helper that increments counters per schema and per field on failure.

```typescript
function trackedSafeParse<T extends z.ZodType>(
  schema: T,
  data: unknown,
  schemaName: string
): z.SafeParseReturnType<z.input<T>, z.output<T>> {
  const result = schema.safeParse(data)
  metrics.increment("zod.validation.attempt", { schema: schemaName })
  if (!result.success) {
    metrics.increment("zod.validation.failure", { schema: schemaName })
    const flat = z.flattenError(result.error)
    for (const field of Object.keys(flat.fieldErrors)) {
      metrics.increment("zod.validation.field_error", {
        schema: schemaName,
        field,
      })
    }
  }
  return result
}
```

| Signal | Meaning |
|--------|---------|
| High failure rate | Schema may be too strict |
| One field dominates failures | Confusing input format |
| Schema never fails | Schema may be too loose |
| Failure spike after deploy | Schema change broke clients |

---

## Object Composition Quick Reference

| Method | Purpose |
|--------|---------|
| `.extend({})` | Add new fields |
| `.safeExtend({})` | Extend with conflict detection |
| `.pick({ key: true })` | Select specific fields |
| `.omit({ key: true })` | Remove specific fields |
| `.partial()` | Make all fields optional |
| `.required()` | Make all fields required |
| `.catchall(schema)` | Validate unknown keys |
| `.keyof()` | Get z.enum of keys |
| `.shape` | Access shape for spreading |

## Prerequisites

- `zod` ^4.0.0
- TypeScript ^5.5
- Node.js with ES2020+ support

## License

MIT
