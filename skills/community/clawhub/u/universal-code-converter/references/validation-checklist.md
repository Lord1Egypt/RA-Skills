# Validation Checklist

## Minimum Test Matrix

Run the following checks for every supported language pair:

1. Parse the source fixtures successfully.
2. Probe the parser contract on representative fixtures: root node type, critical field names, and one query or capture path.
3. If using Tree-sitter, run one incremental reparse capability check with `old_tree`.
4. Convert the fixtures into IR without dropping required nodes.
5. Emit target code and reparse it successfully.
6. Compile or type-check the emitted code when tooling exists.
7. Run execution fixtures for behavior-preserving conversions.
8. Assert that unsupported constructs produce explicit diagnostics.

## Fixture Strategy

Maintain fixtures at three sizes:

- `smoke`: tiny syntax slices such as literals, returns, and calls
- `feature`: one construct family at a time such as loops or classes
- `scenario`: realistic files with imports, helpers, and control flow

Cover both happy-path and failure-path examples.

## Regression Gates

Require these checks before expanding scope:

- Golden snapshot or executable assertion for the parser-probe contract
- Golden snapshot for IR output
- Golden snapshot for emitted target code
- One round-trip parse check on emitted code
- One compile or type-check pass on emitted code
- One behavioral test for every feature family marked `direct` or `desugar`

## Release Criteria

Treat a language pair as ready only when all are true:

- Supported features are documented
- Unsupported features fail loudly
- Representative fixtures pass end to end
- Known lossy rewrites are listed in release notes or diagnostics

## Review Prompts

Use these prompts during implementation or review:

- Where can CST shape differ from program meaning?
- Which features need semantic enrichment before lowering?
- Which rewrites rely on runtime helpers?
- Which behaviors could change silently across languages?
- Which tests would fail if a node field name changed upstream?
