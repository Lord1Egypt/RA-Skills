---
name: features-conditional
description: Conditional type and ternary expression generation
---

# Conditional Type and Ternary

Generate TypeScript conditional types `T extends U ? X : Y` and JavaScript ternary expressions.

## genConditionalType(checkType, extendsType, trueType, falseType)

Produces a conditional type: `checkType extends extendsType ? trueType : falseType`.

```ts
genConditionalType('T', 'U', 'X', 'Y')
// => T extends U ? X : Y

genConditionalType('T', 'null', 'never', 'T')
// => T extends null ? never : T
```

Use for type-level conditionals (e.g. null/undefined stripping, distributive conditionals).

## genTernary(cond, whenTrue, whenFalse)

Produces a runtime ternary: `cond ? whenTrue : whenFalse`.

```ts
genTernary('x > 0', 'x', '-x')
// => x > 0 ? x : -x

genTernary('ok', "'yes'", "'no'")
// => ok ? 'yes' : 'no'
```

## Key Points

- **genConditionalType** is for types only; **genTernary** is for value expressions.
- Arguments are emitted as-is; for string literals in ternary use quoted strings like `"'yes'"`.

<!-- Source references: docs/2.apis/9.conditional.md, src/conditional.ts -->
