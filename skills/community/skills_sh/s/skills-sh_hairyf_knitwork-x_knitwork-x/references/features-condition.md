---
name: features-condition
description: if, else if, else and prefixed block generation
---

# Condition Generation (if / else)

Generate `if`, `else if`, and `else` blocks. **genPrefixedBlock** is a low-level helper for any `prefix { body }` form (e.g. `while`).

## genIf(cond, statements, options, indent?)

Produces `if (cond) { statements }` or `if (cond) statement`. **statements** can be a string or array of strings. **Options:** `bracket: false` for single statement without braces.

```ts
genIf('x > 0', 'return x;')
// => if (x > 0) { return x; }

genIf('ok', ['doA();', 'doB();'])
// => if (ok) { doA(); doB(); }

genIf('x', 'console.log(x);', { bracket: false })
// => if (x) console.log(x);
```

## genElseIf(cond, statements, options, indent?)

Produces `else if (cond) { statements }` or single-statement form. Same **options** as **genIf**.

```ts
genElseIf('x < 0', 'return -x;')
// => else if (x < 0) { return -x; }
```

## genElse(statements, options, indent?)

Produces `else { statements }` or `else statement`. **Options:** `bracket: false`.

```ts
genElse(['return 0;'])
// => else { return 0; }

genElse('fallback();', { bracket: false })
// => else fallback();
```

## genPrefixedBlock(prefix, statements, options, indent?)

Low-level: produces `prefix { statements }` or `prefix statement`. Use for custom constructs or when building `while`/`for`-like blocks manually.

```ts
genPrefixedBlock('if (ok)', 'return true;')
// => if (ok) { return true; }

genPrefixedBlock('while (running)', ['step();', 'check();'])
// => while (running) { step(); check(); }
```

## Key Points

- Compose **genIf** + **genElseIf** + **genElse** to build full if/else chains; pass **indent** for nested formatting.
- **bracket: false** emits a single statement without `{ }` (same as control-flow helpers in loop/switch).

<!-- Source references: docs/2.apis/13.condition.md, src/condition.ts -->
