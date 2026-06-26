---
name: features-statement
description: return, throw, and prefixed block generation
---

# Statement Generation

Generate `return` and `throw` statements. **genPrefixedBlock** is in the condition module; use it for any `prefix { body }` form.

## genReturn(expr?, indent?)

Produces `return expr;` or `return;`. **expr** is optional.

```ts
genReturn('x')
// => return x;

genReturn()
// => return;

genReturn('a + b')
// => return a + b;
```

## genThrow(expr, indent?)

Produces `throw expr;`.

```ts
genThrow("new Error('failed')")
// => throw new Error('failed');

genThrow('e')
// => throw e;
```

## Key Points

- **expr** is emitted as-is (no quoting). For string literals use a quoted string like `"'error'"` or build with **genString**.
- Use **genReturn** / **genThrow** inside **genBlock** or as part of **genIf** / **genSwitch** body arrays.

<!-- Source references: docs/2.apis/17.statement.md, src/statement.ts -->
