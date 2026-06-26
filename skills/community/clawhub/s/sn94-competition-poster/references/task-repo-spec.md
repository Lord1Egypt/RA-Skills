# SN94 Task Repo Spec

SN94 task repos are problem-agnostic. A task can be model compression, binary/ternary inference, pruning, quantization, kernel/runtime optimization, symbolic search, algorithm search, or another measurable research target.

The only requirement is that validators can replay a miner submission from a clean clone and produce a deterministic result JSON.

## Where To Submit

Submit the finished proposal as a GitHub issue in:

```text
https://github.com/AlveusLabs/SN94-BitSota/issues/new?template=competition_proposal.md
```

Use this issue title:

```text
[Competition Proposal] <problem name>
```

Include:

- the filled proposal template
- the public task repo URL
- the pinned commit, tag, or branch intended as `base_ref`
- any expected hardware requirements
- the scoring and reward policy
- known risks or special engineering requirements

## Required Shape

```text
README.md
problem.yaml
submission/
scripts/setup.sh
scripts/benchmark.sh
scripts/validate_submission.py
tests/
results/.gitkeep
```

Equivalent layouts are fine if `problem.yaml` points to the correct commands and result path.

## Miner Submission Surface

Keep allowed edits narrow, for example:

```yaml
allowed_patch_paths:
  - submission/**
```

For kernel or compression tasks, the allowed path may be a miner-owned source file such as `kernels/miner_kernel.cu` or `submission/solution.py`. Do not let miners patch scorers, hidden eval loaders, task config, Dockerfiles, or backend integration.

## Good Problem Shape

Good problems:

- Have one clear primary metric.
- Are deterministic under fixed seeds.
- Can be replayed from a clean clone.
- Have a starter that is valid but beatable.
- Have hidden or rotated validation.
- Fit a practical validator runtime budget.
- Have a patch surface small enough to audit.

Weak problems:

- Depend on one memorized public dataset.
- Require manual judging.
- Let miners patch the benchmark.
- Require large downloads for every replay.
- Have unstable scores between runs.
- Require arbitrary full-repo execution without a sandbox plan.

## Scoring Pattern

For frontier tasks:

```text
primary: hidden validation quality
acceptance floor: task-specific minimum before reward eligibility
tie 1: smaller artifact/model if relevant
tie 2: lower runtime
tie 3: lower memory
tie 4: earlier accepted submission
```

For pooled tasks, define dedupe per task. Repeated equivalent outputs from many hotkeys should not farm rewards.

## Example Families

- Binary or ternary model optimization.
- Quantization method improvement.
- Pruning or sparsity schedule search.
- CUDA, CPU, or runtime kernel optimization.
- Symbolic regression or formula search.
- Compiler pass or graph optimization.
- Data-structure or retrieval improvement.
- CPU-friendly problems for non-GPU miners.
