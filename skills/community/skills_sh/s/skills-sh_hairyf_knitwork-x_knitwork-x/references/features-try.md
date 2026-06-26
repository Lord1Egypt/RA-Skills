---
name: features-try
description: try, catch, finally block generation
---

# Try / Catch / Finally Generation

Generate `try`, `catch`, and `finally` blocks. Compose them into a full try/catch/finally by concatenating the returned strings (with newlines/indent as needed).

## genTry(statements, options, indent?)

Produces `try { statements }` or `try statement`. **statements** can be a string or array of strings. **Options:** `bracket: false` for single statement without braces.

```ts
genTry('mightThrow();')
// => try { mightThrow(); }

genTry(['const x = await f();', 'return x;'])
// => try { const x = await f(); return x; }

genTry('f();', { bracket: false })
// => try f();
```

## genCatch(statements, options, indent?)

Produces `catch (binding) { statements }` or `catch { statements }`. **Options:** `binding` (e.g. `'e'`) for catch variable; omit for optional catch binding. **bracket: false** for single statement.

```ts
genCatch(['throw e;'], { binding: 'e' })
// => catch (e) { throw e; }

genCatch(['logError();'])
// => catch { logError(); }
```

## genFinally(statements, options, indent?)

Produces `finally { statements }` or `finally statement`. **Options:** `bracket: false`.

```ts
genFinally('cleanup();')
// => finally { cleanup(); }

genFinally(['release();', "log('done');"])
// => finally { release(); log('done'); }
```

## Key Points

- Build full try/catch/finally by concatenating: `genTry(...) + ' ' + genCatch(...)` and optionally `+ ' ' + genFinally(...)`.
- Use **binding** when you need the error variable in catch; omit for `catch { }` (optional catch binding).

<!-- Source references: docs/2.apis/14.try.md, src/try.ts -->
