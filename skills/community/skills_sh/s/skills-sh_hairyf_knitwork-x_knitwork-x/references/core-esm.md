---
name: core-esm
description: ESM import, export, default export, and dynamic import generation
---

# ESM Code Generation

Generate ESM module syntax: `import`, `export`, `export default`, and dynamic `import()`.

## genImport(specifier, imports?, options?)

Produces an `import` statement. `imports` can be:

- **Omitted or default:** `genImport('pkg')` → `import "pkg";`
- **String (default import):** `genImport('pkg', 'foo')` → `import foo from "pkg";`
- **Array of names:** `genImport('pkg', ['a', 'b'])` → `import { a, b } from "pkg";`
- **Array of `{ name, as }`:** `genImport('pkg', [{ name: 'foo', as: 'bar' }])` → `import { foo as bar } from "pkg";`

**Options:** `type: true` for type-only import; `attributes: { type: 'json' }` for import attributes.

```ts
genImport('vue', ['ref', 'computed'])
// => import { ref, computed } from "vue";

genImport('pkg', 'foo', { type: true })
// => import type foo from "pkg";
```

## genExport(specifier, exports?, options?)

Produces `export ... from "specifier"`. `exports` can be a string, array of names, `'*'`, or `{ name: '*', as: 'bar' }`.

```ts
genExport('pkg', ['a', 'b'])
// => export { a, b } from "pkg";

genExport('pkg', { name: '*', as: 'bar' })
// => export * as bar from "pkg";
```

## genDefaultExport(value, _options?)

Produces `export default value;`. Use `genString` for quoted values; options (e.g. `singleQuotes`) apply to string output.

```ts
genDefaultExport('foo')
// => export default foo;
```

## genDynamicImport(specifier, options?)

Produces dynamic `import()` or `typeof import()`. Options:

- **wrapper: true** → `() => import("pkg")`
- **interopDefault: true** → `() => import("pkg").then(m => m.default || m)`
- **type: true** → `typeof import("pkg")`; with **name: 'foo'** → `typeof import("pkg").foo`

```ts
genDynamicImport('pkg', { wrapper: true })
// => () => import("pkg")

genDynamicImport('pkg', { type: true, name: 'foo' })
// => typeof import("pkg").foo
```

## Key Points

- Module specifiers are passed as strings; the implementation uses `genString` for the quoted output.
- Use `type: true` for type-only imports/exports.
- Use `attributes` for import attributes (e.g. `with { type: "json" }`).

<!-- Source references: docs/2.apis/3.esm.md, src/esm.ts, README ESM section -->
