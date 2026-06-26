# Architecture Blueprint

## Recommended Stages

| Stage | Purpose | Output |
| --- | --- | --- |
| Parse | Build a concrete syntax tree from source text | CST + source ranges |
| Normalize | Remove syntax sugar and normalize surface forms | Normalized CST or pre-IR nodes |
| Semantic enrichment | Resolve scopes, bindings, imports, and inferred types | Annotated nodes |
| IR build | Convert source-specific structure into a neutral model | Typed IR |
| Lowering | Map IR into a target-language model | Target AST/model |
| Emit | Render text, helpers, imports, and formatting | Source code |
| Validate | Reparse, compile, test, and compare behavior | Diagnostics + confidence |

## Feature Mapping Taxonomy

Use one status for every feature or node family:

- `direct`: one-to-one mapping with no semantic drift
- `desugar`: rewrite source sugar into simpler IR before lowering
- `runtime-helper`: require helper functions or support libraries
- `manual-rewrite`: emit scaffold plus clear warning for human follow-up
- `unsupported`: stop or skip with explicit diagnostic

## IR Design Checklist

Model these concepts before expanding language coverage:

- Module and file boundaries
- Imports and exports
- Function and method declarations
- Parameters, defaults, and return behavior
- Variable declarations, assignment, and mutability
- Primitive literals and composite literals
- Calls and member access
- Conditionals and loops
- Error handling and control-flow exits
- Type annotations or inferred type hints
- Diagnostics for unsupported or lossy conversions

## Suggested Module Boundaries

```text
src/
  frontends/<language>/
  normalization/<language>/
  semantic/
  ir/
  lowering/<target-language>/
  emitters/<target-language>/
  diagnostics/
```

Keep source-language logic in `frontends/` and `normalization/`.
Keep target-language logic in `lowering/` and `emitters/`.
Keep shared reasoning in `semantic/`, `ir/`, and `diagnostics/`.

For Tree-sitter frontends, prefer official bindings/packages for the first working probe.
Persist one parser contract artifact from representative fixtures so node-type and field-name assumptions are testable instead of tribal knowledge.

## Readiness Questions

Answer these before claiming a language pair is supported:

1. Which syntax families are in scope?
2. Which runtime behaviors must stay equivalent?
3. Which type-system differences require helpers or warnings?
4. Which standard-library calls need remapping?
5. Which constructs are intentionally unsupported in v1?
6. Which parser assumptions are recorded as executable fixtures or snapshots?
