---
name: core-string
description: String literal and template literal generation
---

# String and Literal Generation

Helpers for generating string literals, escaping, and template literals.

## escapeString(id)

Escapes a string for use inside a JavaScript string literal (backslashes, quotes, newlines, etc.).

```ts
escapeString("foo'bar")
// => foo\'bar

escapeString("foo\nbar")
// => foo\nbar
```

## genString(input, options?)

Produces a quoted string literal with proper escaping. **Options:** `singleQuotes: true` for single quotes. Use this for any user-facing or config-driven string so quote style is consistent.

```ts
genString('foo')
// => "foo"

genString('foo', { singleQuotes: true })
// => 'foo'

genString('foo\nbar')
// => "foo\nbar"
```

## genTemplateLiteral(parts)

Produces a runtime template literal `` `...${expr}...` ``. `parts` is an array of alternating string chunks and expression names (as strings). Length must be odd: first and last are string parts, between them are expression names.

```ts
genTemplateLiteral(['hello ', 'x'])
// => `hello ${x}`

genTemplateLiteral(['prefix', 'expr', 'suffix'])
// => `prefix${expr}suffix`

genTemplateLiteral(['', 'value'])
// => `${value}`

genTemplateLiteral(['text only'])
// => `text only`
```

## Key Points

- Always use **genString** for values that need quoting/escaping so `singleQuotes` and escaping are consistent across generated code.
- **genTemplateLiteral** is for runtime template literals (values), not TypeScript template literal types (use `genTemplateLiteralType` from the type module).

<!-- Source references: docs/2.apis/1.string.md, src/string.ts -->
