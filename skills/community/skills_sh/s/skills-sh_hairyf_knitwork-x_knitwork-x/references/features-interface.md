---
name: features-interface
description: Interface, index signature, call signature, construct signature generation
---

# Interface Generation

Generate TypeScript interfaces, index signatures, call signatures, and construct signatures.

## genInterface(name, contents?, options, indent?)

Produces `interface Name [extends Other] { ... }`. **contents** can be an object (key → type string), an array of `TypeField`, or omitted for `{}`. **Options:** `extends` (string or array), `export`.

```ts
genInterface('FooInterface')
// => interface FooInterface {}

genInterface('FooInterface', { name: 'string', count: 'number' })
// => interface FooInterface { name: string, count: number }

genInterface('FooInterface', undefined, { extends: 'Other' })
// => interface FooInterface extends Other {}

genInterface('FooInterface', {}, { export: true })
// => export interface FooInterface {}
```

## genIndexSignature(keyType, valueType, keyName?)

Produces `[keyName: keyType]: valueType`. Default **keyName** is `'key'`.

```ts
genIndexSignature('string', 'number')
// => [key: string]: number

genIndexSignature('number', 'string')
// => [key: number]: string
```

## genCallSignature(options)

Produces a call signature `(params): returnType` (and optional generics). Use inside interface body for callable types.

```ts
genCallSignature({ parameters: [{ name: 'x', type: 'string' }], returnType: 'number' })
// => (x: string): number
```

## genConstructSignature(options)

Produces a construct signature `new (params): returnType`. Use inside interface body for constructible types.

```ts
genConstructSignature({ parameters: [{ name: 'x', type: 'string' }], returnType: 'MyClass' })
// => new (x: string): MyClass
```

## Key Points

- **contents** can be a plain object `{ key: "type" }` or an array of `{ name, type, optional?, jsdoc? }`.
- Combine **genIndexSignature** with other members in **contents** for mixed interface shapes.

<!-- Source references: docs/2.apis/5.interface.md, src/interface.ts -->
