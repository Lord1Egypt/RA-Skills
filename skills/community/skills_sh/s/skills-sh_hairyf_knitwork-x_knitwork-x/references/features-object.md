---
name: features-object
description: Object literal, array, Map, Set, type object, getter/setter, method generation
---

# Object and Serialization Generation

Generate object literals, arrays, Map, Set (runtime serialization), TypeScript object types, and object/class methods (getter, setter, method).

## Serialization (runtime values)

### genObject(object, indent, options?)

Produces an object literal `{ key: value, ... }`. **object** can be a plain object (key → value string) or array of `{ name, value, jsdoc? }`. Values are **not** escaped or quoted (emit raw code).

```ts
genObject({ foo: 'bar', test: '() => import("pkg")' })
// => { foo: bar, test: () => import("pkg") }

genObject([{ name: 'count', value: '0', jsdoc: 'Counter value' }])
// => { /** Counter value */ count: 0 }
```

### genArray(array, indent, options?)

Produces an array literal `[ ... ]`. Values are not escaped or quoted.

```ts
genArray([1, 2, 3])
// => [1, 2, 3]
```

### genMap(entries, indent, options?) / genSet(values, indent, options?)

**genMap** produces `new Map([...])` from array of `[key, value]`; **genSet** produces `new Set([...])`. String values are escaped and quoted via **genString** when options are passed.

```ts
genMap([['foo', 'bar'], ['baz', 1]])
// => new Map([["foo", "bar"], ["baz", 1]])

genSet(['foo', 'bar', 1])
// => new Set(["foo", "bar", 1])
```

## Type object (type-level)

**genTypeObject** (see features-type) produces `{ key: type }` for type aliases and interfaces.

## Method / getter / setter (class or object)

### genMethod(options, indent?)

Produces a method or get/set: `name(params) { body }`, `get name() { }`, `set name(v) { }`. **Options:** `name`, `parameters`, `body`, `returnType`, `kind: 'get' | 'set'`, `async`, `static`.

```ts
genMethod({ name: 'foo' })
// => foo() {}

genMethod({ name: 'bar', parameters: [{ name: 'x', type: 'string' }], body: ['return x;'], returnType: 'string' })
// => bar(x: string): string { return x; }

genMethod({ name: 'value', kind: 'get', body: ['return this._v;'], returnType: 'number' })
// => get value(): number { return this._v; }
```

### genGetter(name, body, options, indent?) / genSetter(name, paramName, body, options, indent?)

Shorthand for get/set. **genSetter** takes **paramName** and optional **paramType** in options.

## Key Points

- **genObject** / **genArray** values are raw code strings; for string literals use **genString** and pass the result as the value.
- **genMethod** is shared between class members and object literal methods; use with **genClass** or inside object literal generation.

<!-- Source references: docs/2.apis/18.object.md, src/object.ts -->
