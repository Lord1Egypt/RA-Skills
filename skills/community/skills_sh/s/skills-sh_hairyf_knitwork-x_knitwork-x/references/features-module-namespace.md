---
name: features-module-namespace
description: declare module, module augmentation, namespace, declare global
---

# Module and Namespace Generation

Generate TypeScript `declare module`, module augmentation, `namespace`, and `declare global` blocks.

## genModule(specifier, statements?) / genAugmentation(specifier, statements?)

Produces `declare module "specifier" { ... }`. **genAugmentation** is an alias for **genModule**. **statements** can be a string or array of strings (e.g. interface/type declarations).

```ts
genModule('@nuxt/utils')
// => declare module "@nuxt/utils" {}

genModule('@nuxt/utils', 'interface MyInterface {}')
// => declare module "@nuxt/utils" { interface MyInterface {} }

genModule('@nuxt/utils', [
  'interface MyInterface { test?: string }',
  'type MyType = string',
])
// => multi-line declare module with both
```

Use for ambient module augmentation (e.g. adding types to third-party packages).

## genNamespace(name, statements?)

Produces `namespace Name { ... }`. **statements** can be a string or array of strings.

```ts
genNamespace('MyNamespace')
// => namespace MyNamespace {}

genNamespace('MyNamespace', ['interface MyInterface { test?: string }', 'const foo: string'])
// => namespace MyNamespace { ... }
```

## genDeclareNamespace(namespace, statements?)

Produces `declare namespace` (e.g. `declare global { ... }`). **namespace** is typically `"global"`. **statements** can be a string or array of strings.

```ts
genDeclareNamespace('global')
// => declare global {}

genDeclareNamespace('global', 'interface Window {}')
// => declare global { interface Window {} }
```

## Key Points

- **genModule** / **genAugmentation** use the specifier as a string (quoted in output); use for package name or path.
- **genDeclareNamespace('global')** is the standard way to extend global scope in ambient declarations.

<!-- Source references: docs/2.apis/11.module.md, docs/2.apis/12.namespace.md, src/module.ts, src/namespace.ts -->
