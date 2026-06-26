---
name: universal-code-converter
description: Design, review, or implement source-to-source code translation pipelines that convert or port code between programming languages. Use when building or evaluating a transpiler, code-porting or migration scaffold, tree-sitter-based parser pipeline, intermediate representation (IR), lowering rules, semantic-gap handling, or validation strategy for multi-language code conversion.
---

# Universal Code Converter

Build or refine the converter as a staged translation pipeline. Optimize for semantic fidelity, diagnostics, and incremental delivery instead of "convert everything" claims.

## Run This Workflow

1. Clarify the scope.
   - Capture the source language, target language, runtime constraints, supported constructs, and quality bar.
   - Ask for or extract at least 3 representative snippets before designing the pipeline.
   - Define what "done" means: compilable output, behavior-preserving output, migration scaffold, or partial assisted conversion.

2. Verify the parser frontend.
   - Confirm the required Tree-sitter grammars exist and are actively usable.
   - Prefer official prebuilt bindings or grammar packages for the first frontend probe. Compile grammars manually only when official artifacts are missing or the task needs grammar changes.
   - Inspect actual node types and field names before hardcoding visitors.
   - Capture one reusable parser-probe artifact from real fixtures: root node type, critical field names, and one query/capture example. Keep it in tests or fixtures so later work does not repeat manual spelunking.
   - If Tree-sitter is part of the plan, run one incremental reparse check with `old_tree` to prove the grammar is usable as an editing frontend. Treat this as a capability check, not a brittle microbenchmark.
   - Treat Tree-sitter as a concrete syntax tree frontend with incremental parsing, not as a full semantic compiler.

3. Separate the pipeline into explicit passes.
   - Use this default flow:

```text
parse -> normalize -> semantic enrichment -> IR -> lowering -> emit -> validate
```

   - Keep normalization separate from semantic analysis.
   - Keep shared IR logic separate from pair-specific lowering rules.
   - Keep code formatting separate from translation logic.

4. Design the IR around semantics, not surface syntax.
   - Model declarations, scopes, bindings, literals, calls, control flow, imports, types, and diagnostics.
   - Represent lossy or unsupported constructs explicitly with diagnostic nodes or status flags.
   - Remove syntax sugar early when it simplifies downstream lowering.

5. Implement a narrow vertical slice first.
   - Start with one source-target pair.
   - Start with modules, functions, parameters, literals, identifiers, returns, calls, and simple conditionals.
   - Add tests for each slice before adding more syntax.

6. Handle semantic gaps intentionally.
   - Classify every feature as one of: direct mapping, desugaring, runtime helper, manual rewrite required, or unsupported.
   - Emit warnings for behavior changes or lossy rewrites.
   - Never silently drop exceptions, mutability rules, async semantics, or type expectations.

7. Generate target code from a structured model.
   - Prefer a typed target-language model or emitter API over raw string replacement.
   - Centralize naming, escaping, and indentation in the emitter layer.
   - Preserve comments or source maps only when the task explicitly requires them.

8. Validate the output at multiple levels.
   - Validate frontend assumptions separately from lowering assumptions.
   - Reparse representative source fixtures and assert the parser-probe contract stays stable.
   - Reparse the generated code.
   - Compile or type-check the generated code when tooling is available.
   - Run fixture-based execution tests for behavior-preserving conversions.
   - Include at least one explicit failure-path fixture that must emit diagnostics.
   - Snapshot IR and emitted output for regression coverage.

9. Deliver a bounded result.
   - Return the supported feature matrix, known gaps, assumptions, warnings, and next steps.
   - Say clearly when the result is a scaffold, partial converter, or production-ready slice.

## Produce These Deliverables

- For architecture requests, return: scope, pipeline, IR outline, feature mapping taxonomy, validation plan, and risk list.
- For implementation requests, code the smallest working slice first, add executable tests with it, and record the exact frontend dependency/version used for the parser probe.
- For review requests, prioritize semantic drift, unsupported constructs, parser-shape assumptions, and missing validation.

## Read Additional References Only When Needed

- Read `references/architecture-blueprint.md` for module layout, feature mapping taxonomy, and IR design prompts.
- Read `references/validation-checklist.md` for test strategy, regression gates, and release criteria.

## Apply These Guardrails

- Do not call the converter "universal" unless a supported-language and supported-feature matrix exists.
- Do not equate CST shape with program meaning.
- Do not put all translation rules in one transformer file.
- Do not promise idiomatic target code before correctness and diagnostics exist.
- Do not add a new language pair without representative fixtures and validation.

## Start With This Repo Shape

```text
src/
  frontends/
  normalization/
  semantic/
  ir/
  lowering/
  emitters/
  diagnostics/
tests/
  fixtures/
  golden/
```
