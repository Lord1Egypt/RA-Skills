# Type Safety

This document defines type system constraints for all TypeScript code in the z.ai sandbox. These rules enforce correctness at compile time rather than runtime, reducing the class of bugs that reach production.

---

## No `any` — Use `unknown` Then Narrow [REQUIRED]

The `any` type disables the TypeScript compiler for that value. This defeats the purpose of using TypeScript and allows type errors to propagate silently through the codebase.

When a value's type is genuinely unknown (e.g., parsed JSON, external API response), declare it as `unknown` and narrow with type guards:

```typescript
// [REQUIRED-ban]
function process(data: any) { ... }

// [REQUIRED] correct pattern
function process(data: unknown): Result {
  if (typeof data === 'string' && data.length > 0) {
    return handleString(data);
  }
  throw new TypeError('Expected a non-empty string');
}
```

Why: `unknown` forces callers to handle the uncertain type before using the value, catching errors at compile time.

## Explicit Return Types on All Functions [REQUIRED]

Every function and method declaration must include an explicit return type annotation.

```typescript
// [REQUIRED-ban]
function getUserName(id: string) { return db.user.findFirst(...); }

// [REQUIRED] correct pattern
function getUserName(id: string): Promise<User | null> {
  return db.user.findFirst({ where: { id } });
}
```

Why: explicit returns serve as documentation, catch unintended type changes during refactoring, and make the public API of each function immediately clear to reviewers.

## Null Safety — Optional Chaining and Nullish Coalescing [REQUIRED]

All code must account for `null` and `undefined` values. Prefer optional chaining (`?.`) and nullish coalescing (`??`) over manual null checks.

```typescript
// [REQUIRED-ban]
const city = user.address.city;

// [REQUIRED] correct pattern
const city = user?.address?.city ?? 'Unknown';
```

Why: runtime `TypeError: Cannot read properties of undefined` is one of the most common failure modes in JavaScript applications. Handling it at the point of access prevents cascading failures.

## Prisma Scalar Types Cannot Be Lists [CRITICAL]

In Prisma schema definitions, scalar fields (String, Int, Float, Boolean, DateTime) cannot use the list modifier (`[]`). Only relation fields can be lists.

```prisma
// [CRITICAL-ban] — this will fail at schema push
model Item {
  tags String[]  // scalar list — not supported with SQLite
}

// [CRITICAL] correct pattern — use a separate model for one-to-many
model Item {
  tags ItemTag[]
}

model ItemTag {
  id    String @id @default(cuid())
  value String
  item  Item   @relation(fields: [itemId], references: [id])
  itemId String
}
```

Why: the sandbox uses SQLite, which does not support scalar list types. Attempting to push this schema produces a runtime error that blocks database setup.

## Generic Constraints Where Applicable [RECOMMENDED]

When writing generic functions, constrain type parameters to the narrowest valid supertype rather than leaving them unbounded.

```typescript
// [RECOMMENDED] unbounded — accepts anything, no type guidance
function merge<T>(a: T, b: T): T { ... }

// [RECOMMENDED] better — constrains to objects with an id
function mergeById<T extends { id: string }>(a: T, b: Partial<T>): T { ... }
```

Why: constrained generics provide better IDE autocompletion, catch misuse at the call site, and communicate the intended domain of the function.
