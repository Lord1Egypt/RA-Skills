---
name: features-function
description: Function, arrow function, block, and parameter generation
---

# Function and Block Generation

Generate function declarations, arrow functions, statement blocks, and parameter lists. For class/object methods use **genMethod** (see features-object).

## genFunction(options, indent?)

Produces `[export] function name [<generics>](params) [: returnType] { body }`. **Options:** `name`, `parameters`, `body` (string or array), `returnType`, `generics`, `async`, `export`.

```ts
genFunction({ name: 'foo' })
// => function foo() {}

genFunction({ name: 'foo', parameters: [{ name: 'x', type: 'string' }, { name: 'y', type: 'number', optional: true }] })
// => function foo(x: string, y?: number) {}

genFunction({ name: 'id', generics: [{ name: 'T' }], parameters: [{ name: 'x', type: 'T' }], returnType: 'T', body: ['return x;'] })
// => function id<T>(x: T): T { return x; }

genFunction({ name: 'foo', export: true })
// => export function foo() {}
```

## genArrowFunction(options)

Produces `(params) => body` or `(params) => { statements }`. **body** can be a single expression string (no braces) or an array of statements (block). **Options:** `parameters`, `body`, `returnType`, `async`.

```ts
genArrowFunction({ body: 'x + 1' })
// => () => x + 1

genArrowFunction({ parameters: [{ name: 'x', type: 'number' }], body: 'x * 2' })
// => (x: number) => x * 2

genArrowFunction({ parameters: [{ name: 'x' }], body: ['return x + 1;'] })
// => (x) => { return x + 1; }
```

## genBlock(statements?, indent?)

Produces `{ statements }`. **statements** can be a single string or array of strings; normalized to array and joined with newlines and indent.

```ts
genBlock()
// => {}

genBlock('return x;')
// => { return x; }

genBlock(['const a = 1;', 'return a;'])
// => { const a = 1; return a; }
```

## genParam(p)

Produces a single parameter string from a **TypeField**: `name [: type] [= default]`, `name?` for optional.

```ts
genParam({ name: 'x', type: 'string' })
// => x: string

genParam({ name: 'z', type: 'number', default: '0' })
// => z: number = 0
```

## Key Points

- Use **genBlock** wherever a block body is needed (functions, if/else, try/catch, etc.).
- **body** in **genArrowFunction**: one expression → no braces; array of statements → block with braces.

<!-- Source references: docs/2.apis/7.function.md, src/function.ts -->
