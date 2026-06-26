---
name: core-variable
description: Variable name and variable declaration generation
---

# Variable Generation

Generate safe variable names and variable declarations (`const` / `let`).

## genVariableName(name)

Produces a safe JavaScript identifier. Reserves (e.g. `for`, `class`) are prefixed with `_`; spaces and other invalid characters are replaced (e.g. `with space` → `with_32space`).

```ts
genVariableName('valid_import')
// => valid_import

genVariableName('for')
// => _for

genVariableName('with space')
// => with_32space
```

## genVariable(name, value, options?)

Produces a variable declaration. **Options:** `kind: 'let' | 'var' | 'const'` (default `'const'`), `export: true`.

```ts
genVariable('a', '2')
// => const a = 2

genVariable('foo', "'bar'")
// => const foo = 'bar'

genVariable('x', '1', { kind: 'let' })
// => let x = 1

genVariable('y', '2', { export: true })
// => export const y = 2
```

## Key Points

- **value** is emitted as-is (no quoting). For string values use a quoted string like `"'bar'"` or build with `genString(...)` and pass the result.
- Use **genVariableName** when generating identifiers from arbitrary names (e.g. import names, file names) to avoid invalid identifiers.

<!-- Source references: docs/2.apis/2.variable.md, src/variable.ts -->
