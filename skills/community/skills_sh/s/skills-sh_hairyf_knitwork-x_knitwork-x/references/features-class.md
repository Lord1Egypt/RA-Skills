---
name: features-class
description: Class, constructor, property, method, getter/setter generation
---

# Class Generation

Generate TypeScript/JavaScript classes, constructors, class properties, methods, and getters/setters.

## genClass(name, members, options, indent?)

Produces `class Name [extends Base] [implements I1, I2] { ... }`. **members** is an array of strings (e.g. from `genConstructor`, `genProperty`, `genMethod`). **Options:** `extends`, `implements` (string or array), `export`.

```ts
genClass('Foo')
// => class Foo {}

genClass('Bar', [genConstructor([], ['super();'])])
// => class Bar { constructor() { super(); } }

genClass('Baz', [], { extends: 'Base', implements: ['I1', 'I2'] })
// => class Baz extends Base implements I1, I2 {}

genClass('Exported', [], { export: true })
// => export class Exported {}
```

## genConstructor(parameters, body, options, indent?)

Produces `constructor(params) { [super(...);] ... }`. **parameters** is an array of `{ name, type?, optional?, default? }`. **body** is a string or array of statement strings. **Options:** `super` (arguments string).

```ts
genConstructor()
// => constructor() {}

genConstructor([{ name: 'x', type: 'string' }], ['super();', 'this.x = x;'])
// => constructor(x: string) { super(); this.x = x; }
```

## genProperty(field, indent?)

Produces a single property: `[modifiers?] name [?:] type [ = value ]`. **field** is `TypeField`: `name`, `type?`, `optional?`, `value?`, `readonly?`, `static?`, `jsdoc?`.

```ts
genProperty({ name: 'foo', type: 'string' })
// => foo: string

genProperty({ name: 'bar', type: 'number', optional: true })
// => bar?: number

genProperty({ name: 'x', value: '0' })
// => x = 0

genProperty({ name: 'id', type: 'string', readonly: true, static: true })
// => static readonly id: string
```

## genMethod(options, indent?)

Produces a method (or get/set) for class or object: `name(params) { body }`, `get name() { }`, `set name(v) { }`. **Options:** `name`, `parameters`, `body`, `returnType`, `kind: 'get' | 'set'`, `async`, `static`, etc.

## genGetter / genSetter

Shorthand for get/set: `genGetter('value', ['return this._v;'])`, `genSetter('value', 'v', ['this._v = v;'])`.

## Key Points

- Compose members: pass `genConstructor(...)`, `genProperty(...)`, `genMethod(...)` into the **members** array of `genClass`.
- Use **genProperty** for both interface-like signatures and class fields with initializers (`value`).

<!-- Source references: docs/2.apis/4.class.md, src/class.ts -->
