---
name: features-utils
description: Comment, JSDoc, key, literal, regex, wrapInDelimiters
---

# Utils Generation

Utility helpers: comments, JSDoc, object keys, object literal shorthand, regex literals, and delimiter wrapping.

## genComment(text, options?, indent?)

Produces a single-line `//` comment or block comment (non-JSDoc). **Options:** `block: true` for `/* ... */`.

```ts
genComment('Single line comment')
// => // Single line comment

genComment('Block comment', { block: true })
// => /* Block comment */
```

## genJSDocComment(jsdoc, indent?)

Produces a JSDoc block `/** ... */`. **jsdoc** can be a string, array of lines, or object (e.g. `{ description, param: { x: "number" }, returns: "void" }`).

```ts
genJSDocComment('Single line')
// => /** Single line */

genJSDocComment({ description: 'Fn', param: { x: 'number' }, returns: 'void' })
// => /** Fn @param {number} x @returns {void} */ (formatted)
```

## genKey(key)

Produces a safe object key: unquoted for valid identifiers, otherwise quoted (e.g. **genString**). Use for object literal keys so reserved words and special characters are handled.

```ts
genKey('foo')
// => foo

genKey('foo-bar')
// => "foo-bar"

genKey('with space')
// => "with space"
```

## genLiteral(fields, indent, _options?)

Produces an object literal from field descriptors (shorthand and spread). **fields** is an array of `['key']` for shorthand or `['key', 'value']` or `['...', 'rest']` for spread.

```ts
genLiteral([['type'], ['type', 'A'], ['...', 'b']])
// => { type, type: A, ...b }
```

## genRegExp(pattern, flags?)

Produces a regex literal `/pattern/flags`.

```ts
genRegExp('foo')
// => /foo/

genRegExp('foo', 'gi')
// => /foo/gi

genRegExp('foo\\d+')
// => /foo\d+/
```

## wrapInDelimiters(lines, indent, delimiters, withComma?)

Low-level: wraps an array of strings in delimiters (e.g. `{`, `}`). **delimiters** is `[open, close]`. **withComma** controls trailing commas. Used internally by genObject, genBlock, genEnum, etc.

## Key Points

- Use **genKey** for object literal keys so identifiers and reserved words are correct.
- Use **genJSDocComment** for JSDoc on functions, interfaces, or properties (pass **indent** for alignment).

<!-- Source references: docs/2.apis/19.utils.md, src/utils.ts -->
