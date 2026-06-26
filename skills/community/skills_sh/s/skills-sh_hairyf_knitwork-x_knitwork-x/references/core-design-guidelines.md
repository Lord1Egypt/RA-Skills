---
name: core-design-guidelines
description: Design conventions for knitwork-x gen* APIs (naming, params, options)
---

# Design Guidelines for knitwork-x APIs

Conventions for the `gen*` APIs—useful when extending or contributing to knitwork-x.

## Naming

- **Public API:** Prefix with `gen` + verb/noun (e.g. `genImport`, `genClass`, `genBlock`).
- **Internal helpers:** Use `_gen` prefix or non-gen names (e.g. `escapeString`, `wrapInDelimiters`).

## Parameter Order

1. Required "subject" parameters (e.g. `specifier`, `name`, `object`).
2. Optional subject parameters (e.g. `imports?`, `statements?`).
3. Options object (e.g. `options = {}`).
4. **Indent** as the last parameter when supported (`indent = ""`).

## Options Object

- Type: `GenXxxOptions` or `XxxCodeGenOptions`; extend `CodegenOptions` when needed (e.g. `singleQuotes?`).
- All option fields optional; callers default to `{}`.
- Boolean flags: e.g. `export`, `const`, `singleQuotes`.

## Return Value

- Always **string** (code fragment).
- **Pure:** no mutation of inputs; same input and options → stable output.
- Output is a fragment that can be spliced into source (may include newlines and indent).

## Polymorphic Input

- Accept `T | T[]` when "one vs many" is clear (e.g. `statements?: string | string[]`); normalize to array inside.
- For object vs array shapes, use a union (e.g. `genTypeObject(object: TypeObject | TypeObjectField[])`).

## Strings and Keys

- Use **genString(input, options)** for any quoted/escaped string so `singleQuotes` is respected.
- Use **genKey(key)** for object literal keys (unquoted for valid identifiers, otherwise quoted).

## Key Points

- When adding new `gen*` helpers, follow the same parameter order and options pattern.
- Pass **CodegenOptions** through to nested `genString`, `genEnum`, etc., for consistent style.

<!-- Source references: docs/2.apis/index.md (Design Guidelines) -->
