---
name: features-switch
description: switch, case, default generation
---

# Switch Generation

Generate `switch (expr) { cases }` and `case` / `default` clauses. Compose by passing an array of case/default strings to **genSwitch**.

## genSwitch(expr, cases, options, indent?)

Produces `switch (expr) { cases }`. **cases** is an array of strings (typically from **genCase** and **genDefault**).

```ts
genSwitch('x', [genCase('1', 'break;'), genDefault('return 0;')])
// => switch (x) { case 1: break; default: return 0; } (with newlines/indent)

genSwitch('key', [])
// => switch (key) {}
```

## genCase(value, statements?, indent?)

Produces `case value:` optionally followed by indented statements. Omit **statements** for fall-through.

```ts
genCase('1', 'break;')
// => case 1:\n  break;

genCase("'a'", ['doA();', 'break;'])
// => case 'a':\n  doA();\n  break;

genCase('0')
// => case 0: (fall-through)
```

## genDefault(statements?, indent?)

Produces `default:` optionally followed by indented statements. Omit **statements** for fall-through.

```ts
genDefault('return 0;')
// => default:\n  return 0;

genDefault()
// => default:
```

## Key Points

- **value** in **genCase** is emitted as-is (e.g. `'1'`, `"'a'"`, `'MyEnum.A'`).
- Build **cases** array by mixing **genCase** and **genDefault** in the desired order.

<!-- Source references: docs/2.apis/16.switch.md, src/switch.ts -->
