---
name: features-decorator
description: Decorator syntax generation
---

# Decorator Generation

Generate decorator syntax `@Decorator` or `@Decorator(args)`.

## genDecorator(name, args?, indent?)

Produces `@name` or `@name(args)`. **args** is optional; pass a string for the parenthesized argument list (e.g. `"()"`, `'("/api")'`, `"(min: 0, max: 100)"`).

```ts
genDecorator('Component')
// => @Component

genDecorator('Injectable', '()')
// => @Injectable()

genDecorator('Route', '("/api")')
// => @Route("/api")

genDecorator('Validate', '(min: 0, max: 100)')
// => @Validate(min: 0, max: 100)
```

## Key Points

- **args** is emitted as-is (no quoting of the whole). Include parentheses in the string when you need `@Decorator(...)`.
- Typically used together with **genClass** or **genProperty** / **genMethod**; prepend decorator lines with appropriate indent before the declaration.

<!-- Source references: docs/2.apis/10.decorator.md, src/decorator.ts -->
