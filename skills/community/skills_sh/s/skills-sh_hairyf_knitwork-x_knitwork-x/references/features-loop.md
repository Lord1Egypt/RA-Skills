---
name: features-loop
description: for, for...of, for...in, while, do...while generation
---

# Loop Generation

Generate `for`, `for...of`, `for...in`, `while`, and `do...while` loops.

## genFor(init, test, update, statements, options, indent?)

Produces C-style `for (init; test; update) { body }`. **init**, **test**, **update** are strings (can be empty). **statements** can be a string or array. **Options:** `bracket: false` for single statement.

```ts
genFor('let i = 0', 'i < n', 'i++', 'console.log(i);')
// => for (let i = 0; i < n; i++) { console.log(i); }

genFor('', 'true', '', ['doWork();', 'if (done) break;'])
// => for (; true; ) { doWork(); if (done) break; }
```

## genForOf(left, iterable, statements, options, indent?)

Produces `for (left of iterable) { body }`. **left** is the loop variable (e.g. `'const x'`, `'let [k, v]'`).

```ts
genForOf('const x', 'items', 'console.log(x);')
// => for (const x of items) { console.log(x); }

genForOf('let [k, v]', 'Object.entries(obj)', ['process(k, v);'])
// => for (let [k, v] of Object.entries(obj)) { process(k, v); }
```

## genForIn(left, obj, statements, options, indent?)

Produces `for (left in obj) { body }`.

```ts
genForIn('const key', 'obj', 'console.log(key, obj[key]);')
// => for (const key in obj) { console.log(key, obj[key]); }
```

## genWhile(cond, statements, options, indent?)

Produces `while (cond) { body }`. **Options:** `bracket: false`.

```ts
genWhile('running', 'step();')
// => while (running) { step(); }
```

## genDoWhile(statements, cond, options, indent?)

Produces `do { body } while (cond);`. **Options:** `bracket: false`.

```ts
genDoWhile('step();', '!done')
// => do { step(); } while (!done);
```

## Key Points

- **left** in **genForOf** / **genForIn** is the full left-hand side (e.g. `'const x'`, `'let item'`).
- Use **bracket: false** when the body is a single statement and you want no braces.

<!-- Source references: docs/2.apis/15.loop.md, src/loop.ts -->
