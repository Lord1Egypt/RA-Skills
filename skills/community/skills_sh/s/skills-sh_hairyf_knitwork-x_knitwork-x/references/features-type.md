---
name: features-type
description: Type alias, union, intersection, mapped type, template literal type, keyof, typeof
---

# Type Alias and Type Expression Generation

Generate type aliases, object types, union/intersection, mapped types, template literal types, and keyof/typeof/satisfies/assertion.

## genTypeAlias(name, value, options, indent?)

Produces `[export] type Name [<generics>] = value`. **value** can be a string (raw type) or a type object (passed to genTypeObject). **Options:** `export`, `generics`.

```ts
genTypeAlias('Foo', 'string')
// => type Foo = string

genTypeAlias('FooType', { name: 'string', count: 'number' })
// => type FooType = { name: string, count: number }

genTypeAlias('Id', 'T', { generics: [{ name: 'T' }] })
// => type Id<T> = T

genTypeAlias('Baz', 'string', { export: true })
// => export type Baz = string
```

## genTypeObject(object, indent?)

Produces an object type `{ ... }`. **object** can be a plain object (key → type), object with `"key?": type` for optional, or array of `TypeObjectField`. Supports nested objects and JSDoc.

```ts
genTypeObject({ name: 'string', count: 'number' })
// => { name: string, count: number }

genTypeObject([{ name: 'name', type: 'string' }, { name: 'count', type: 'number', required: true }])
// => { name?: string, count: number }
```

## genUnion(types) / genIntersection(types)

**genUnion** produces `A | B | C`; **genIntersection** produces `A & B & C`. **types** can be a string (single) or array of strings.

```ts
genUnion(['string', 'number'])
// => string | number

genIntersection(['A', 'B', 'C'])
// => A & B & C
```

## genMappedType(keyName, keyType, valueType)

Produces `{ [K in keyof T]: U }`.

```ts
genMappedType('K', 'keyof T', 'U')
// => { [K in keyof T]: U }
```

## genKeyOf(type) / genTypeof(expr)

**genKeyOf** → `keyof Type`; **genTypeof** → `typeof expr`.

## genTemplateLiteralType(parts)

Produces a template literal type (type-level). **parts** is alternating string chunks and type names (same shape as genTemplateLiteral).

```ts
genTemplateLiteralType(['prefix', 'T', 'suffix'])
// => `prefix${T}suffix`
```

## genTypeAssertion(expr, type) / genSatisfies(expr, type)

**genTypeAssertion** → `expr as Type`; **genSatisfies** → `expr satisfies Type`.

## genTypeExport(specifier, imports, options) / genInlineTypeImport(specifier, name?, options)

**genTypeExport** → `export type { ... } from "specifier";`. **genInlineTypeImport** → `typeof import("specifier").name` (default export when name omitted).

## Key Points

- **genTypeObject** accepts both `{ key: "type" }` and `[{ name, type, required? }]`; use the latter for optional keys and JSDoc.
- Use **genUnion**/ **genIntersection** for complex types; pass options through for consistent quoting where applicable.

<!-- Source references: docs/2.apis/8.type.md, src/type.ts -->
