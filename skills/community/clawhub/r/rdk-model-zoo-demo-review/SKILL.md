---
name: rdk-model-zoo-demo-review
description: Use when reviewing a new, changed, migrated, or pre-merge RDK Model Zoo sample/demo for repository compliance or delivery completeness across RDK X3, X5, and RDK S branches.
---

# RDK Model Zoo Demo Review

Review a sample on two independent axes. Do not let a clean convention review hide a missing delivery requirement, or vice versa.

## Resolve the target

Use this order to identify the review target:

1. A repository and sample path explicitly supplied by the user.
2. The current Git repository root, branch, and the supplied model/sample name.
3. A uniquely matching sample directory in the current repository.

If those do not identify one target, ask for the repository path and sample path. Do not infer a platform or branch from a model name alone.

Read the target branch's `docs/Model_Zoo_Repository_Guidelines.md`, root README files, and the relevant sample tree. Read [references/review-checklist.md](references/review-checklist.md) before judging any finding. Use [references/branch-matrix.md](references/branch-matrix.md) to select branch exceptions and [references/family-patterns.md](references/family-patterns.md) only for the matching sample family; validate both against target-branch documentation and the closest sibling sample.

## Gather evidence

Inspect only material relevant to the target:

- The target sample's complete path listing, top-level docs, and applicable `conversion/`, `evaluator/`, `model/`, `runtime/`, and `test_data/` contents.
- Runtime entry points, wrappers, `run.sh`, build files, and only the shared utilities needed to judge possible duplication.
- Root and category indexes affected by the sample; for vision, include `samples/vision/README*` when that branch uses them.
- The issue, PR description, specification, or user request when one exists; this is the delivery source.

Each finding needs a `path:line` citation, or a command plus the relevant output. A passed check must name the files or command that support it. Never claim board execution unless it was actually run.

## Review axes

### Model Zoo standards

Apply the precedence order in the checklist: target branch rules, target branch documentation, target sample code/files, closest family sibling, then `sample_template`. Report whether each rule is a hard requirement, platform requirement, or convention.

Check only applicable categories: branch/platform fit; directory shape and generated files; required names; bilingual docs; runtime paths and default commands; model download artifacts; conversion/evaluator boundaries; public-code comments; shared-utils reuse; and repository/category index and cross-document consistency.

### Delivery specification

When a delivery source exists, independently check:

- Requested model, task capabilities, and input/output behavior.
- Requested boards, model formats, Python/C++ runtime scope, conversion, evaluator, and documentation deliverables.
- Promised accuracy, performance, result images, or benchmark evidence.
- Missing or partial requirements, incorrect-looking implementations, and scope that was added without a stated need.

If no delivery source exists, state `No delivery specification available`; do not invent one from repository conventions.

## Verification level

End the report with one level and its evidence:

- `static-reviewed` — files, paths, docs, and code were inspected for consistency.
- `host-verified` — a host-side build, script, or test was run successfully.
- `board-verified` — the stated command, board, model artifact, input, and result were observed on target hardware.
- `not-verified` — state the missing environment, artifact, or access.

`board-verified` includes `static-reviewed`; it does not excuse standards findings.

## Output

Produce findings first. For every finding include:

- Severity: `blocking`, `major`, or `minor` (use the checklist guidance).
- Axis: `Model Zoo standards` or `Delivery specification`.
- Location, rule/requirement, evidence, impact, and the smallest corrective action.

Then provide, in this order:

1. `## Model Zoo Standards`
2. `## Delivery Specification`
3. `## Passed Checks`
4. `## Open Questions` — only unresolved facts.
5. `## Verification Level`
6. `## Overall Verdict` — `pass`, `pass with fixes`, or `needs rework`.

Keep the two axes separate; do not merge or rerank their findings. If no finding exists on an axis, say so explicitly.

## Boundaries

Focus on compliance, regressions, and missing delivery pieces. Do not rewrite the sample unless asked. Treat board execution as unverified unless evidence is available.
