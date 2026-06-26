---
name: typescript-mastery
description: TypeScript advanced patterns — branded types, discriminated unions, template literals, generics, type guards, tsconfig optimization, and migration strategies
version: 1.0.0
tags:
  - typescript
  - javascript
  - web-development
  - types
  - midos
---

# TypeScript Mastery

## Description

Advanced TypeScript patterns for professional-grade applications. Covers branded types for nominal typing, discriminated unions for state machines, template literal types for DSLs, generics with constraints, utility type composition, custom type guards, and performance-tuned tsconfig.json settings. Also includes a practical incremental migration strategy from JavaScript. TypeScript is the #1 language on GitHub in 2026 with 80%+ adoption in new projects.

## Usage

Install this skill to get advanced TypeScript patterns including:
- Branded types to prevent mixing structurally identical types (UserId vs OrderId)
- Discriminated unions with exhaustiveness checking for state machines
- Template literal types for type-safe API routes and event names
- tsconfig.json settings that reduce compilation time by 30-50%
- Incremental migration strategy from JavaScript to TypeScript

When working on TypeScript projects, this skill provides context for:
- Designing type-safe APIs using generics and constraints
- Replacing `any` with `unknown` + type narrowing
- Using `as const` instead of enums (better tree-shaking)
- Validating runtime data with Zod instead of type assertions
- Organizing types to avoid slow inline complex type expressions

## Key Patterns

### Pattern 1: Branded Types (Nominal Typing)

Prevent accidentally passing the wrong ID or value:

```typescript
type Brand<T, TBrand> = T & { __brand: TBrand };
type UserId = Brand<number, "UserId">;
type OrderId = Brand<number, "OrderId">;

function createUserId(id: number): UserId { return id as UserId; }
function getUser(id: UserId) { /* ... */ }

const userId = createUserId(123);
const orderId = 456 as OrderId;

getUser(userId);  // OK
getUser(orderId); // Type error -- caught at compile time
```

Use cases: Database IDs, monetary values (USD, EUR), validated strings (Email, URL).

### Pattern 2: Discriminated Unions with Exhaustiveness Checking

```typescript
type Shape =
  | { type: "circle"; radius: number }
  | { type: "rectangle"; width: number; height: number }
  | { type: "square"; size: number };

function calculateArea(shape: Shape): number {
  switch (shape.type) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    case "square": return shape.size ** 2;
    default:
      const _exhaustive: never = shape;
      throw new Error(`Unhandled shape: ${_exhaustive}`);
  }
}
```

TypeScript errors when you add a new variant but forget to handle it — perfect for state machines.

### Pattern 3: Template Literal Types

```typescript
type EventNames = "click" | "focus" | "blur";
type EventHandlers = `on${Capitalize<EventNames>}`;
// Result: "onClick" | "onFocus" | "onBlur"

type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE";
type APIRoute = `/${string}`;
type Endpoint = `${HTTPMethod} ${APIRoute}`;
// Enforces: "GET /users", "POST /users/123", etc.
```

### Pattern 4: Const Assertions (Better Than Enums)

```typescript
// Use as const instead of enum: no runtime overhead, better tree-shaking
const Status = {
  Active: "ACTIVE",
  Inactive: "INACTIVE",
  Pending: "PENDING"
} as const;

type StatusType = typeof Status[keyof typeof Status];
// "ACTIVE" | "INACTIVE" | "PENDING"

function setStatus(status: StatusType) { /* ... */ }
setStatus(Status.Active);  // OK
setStatus("INVALID");      // Type error
```

### Pattern 5: Custom Type Guards

```typescript
function isNotNull<T>(value: T | null): value is T {
  return value !== null;
}

const mixed: (string | null)[] = ["a", null, "b", null];
const strings: string[] = mixed.filter(isNotNull);
// Type: string[] -- TypeScript knows nulls are gone
```

### Pattern 6: unknown vs any

```typescript
// WRONG: 'any' disables type safety -- errors cascade silently
function processInput(data: any) {
  data.nonExistentMethod(); // No error, but crashes at runtime
}

// CORRECT: 'unknown' forces narrowing first
function processInput(data: unknown) {
  if (typeof data === "string") {
    return data.toUpperCase(); // Safe
  }
  throw new Error("Expected string");
}
```

### Pattern 7: Runtime Validation with Zod

```typescript
// WRONG: type assertion without validation -- silently wrong
const user = JSON.parse(apiResponse) as User;

// CORRECT: validate at the boundary
import { z } from "zod";
const UserSchema = z.object({
  id: z.number(),
  name: z.string(),
  email: z.string().email()
});
const user = UserSchema.parse(JSON.parse(apiResponse));
```

### Pattern 8: Named Types for Performance

```typescript
// SLOW: TypeScript re-evaluates complex inline types every use
function processData(input:
  Pick<Omit<User, "password">, "id" | "name"> & { role: string }
) { }

// FAST: TypeScript caches named types (30%+ speedup on large codebases)
type UserBasicInfo = Pick<Omit<User, "password">, "id" | "name">;
type UserWithRole = UserBasicInfo & { role: string };
function processData(input: UserWithRole) { }
```

### tsconfig.json Performance Settings

```json
{
  "compilerOptions": {
    "incremental": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "strictFunctionTypes": true
  }
}
```

`incremental`: 30-50% faster rebuilds. `skipLibCheck`: 20-40% speed boost. `isolatedModules`: 32% faster compilation.

### Migration Strategy: JavaScript to TypeScript

Phase 1 (Day 1): `{ "allowJs": true, "checkJs": false, "strict": false }`

Phase 2 (Weeks 1-4): Convert bottom-up (no-dependency modules first). Use `any` temporarily.

Phase 3 (Month 2): `{ "checkJs": true, "strict": true, "noImplicitAny": true }`

### Utility Types Reference

```typescript
type User = { id: number; name: string; password: string };
type PartialUser = Partial<User>;          // all fields optional
type ReadonlyUser = Readonly<User>;        // all fields readonly
type PublicUser = Omit<User, "password">; // remove specific fields
type LoginFields = Pick<User, "id" | "name">;
type UserMap = Record<string, User>;
```

## Tools & References

- [TypeScript Official Docs](https://www.typescriptlang.org/docs/)
- [Total TypeScript -- Matt Pocock](https://www.totaltypescript.com/)
- [TypeScript Performance Wiki](https://github.com/microsoft/TypeScript/wiki/Performance)
- [Zod -- Runtime Schema Validation](https://zod.dev/)
- `npm install -D typescript ts-node @types/node`
- `npx tsc --init` -- generate tsconfig.json

---
*Published by [MidOS](https://midos.dev) — MCP Community Library*
