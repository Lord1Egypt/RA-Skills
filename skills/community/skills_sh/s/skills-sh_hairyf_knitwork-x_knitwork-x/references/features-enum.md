---
name: features-enum
description: Enum and const enum generation
---

# Enum Generation

Generate TypeScript enums and const enums. Members can be numeric, string, or auto-increment (undefined value).

## genEnum(name, members, options, indent?)

Produces `[const] enum Name { ... }`. **members** is an object: key = member name, value = number, string, or `undefined` (auto-increment from 0). **Options:** `export`, `const`.

```ts
genEnum('Color', { Red: 0, Green: 1, Blue: 2 })
// => enum Color { Red = 0, Green = 1, Blue = 2 }

genEnum('Status', { Active: 'active', Inactive: 'inactive' })
// => enum Status { Active = "active", Inactive = "inactive" }

genEnum('Auto', { A: undefined, B: undefined, C: undefined })
// => enum Auto { A = 0, B = 1, C = 2 }

genEnum('MyEnum', { Foo: 1 }, { export: true, const: true })
// => export const enum MyEnum { Foo = 1 }
```

## genConstEnum(name, members, options, indent?)

Shorthand for `genEnum(..., { const: true })`.

```ts
genConstEnum('Direction', { Up: 1, Down: 2 })
// => const enum Direction { Up = 1, Down = 2 }
```

## Key Points

- Use **undefined** for auto-increment numeric members (0, 1, 2, ...).
- Pass **CodegenOptions** (e.g. `singleQuotes`) so string enum values are quoted consistently.

<!-- Source references: docs/2.apis/6.enum.md, src/enum.ts -->
