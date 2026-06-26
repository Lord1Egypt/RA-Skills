---
name: sn94-competition-poster
description: Use when creating, reviewing, or packaging SN94 BitSota competition proposals and replayable task repositories that fit the autoresearch backend format, including model compression, kernel/runtime optimization, pruning, quantization, symbolic search, or other measurable research tasks for AgentSkills, Hermes, Claw/OpenClaw, Codex, Claude, or Cursor agents.
metadata:
  short-description: Build replayable SN94 competition repos
---

# SN94 Competition Poster

Use this skill to turn any measurable competition idea into a concrete SN94 task proposal and, when asked, a replayable public task repository skeleton.

## Core Workflow

1. Define the competition objective, input/output contract, hardware target, expected runtime, and what miners are allowed to edit.
2. Convert that into the SN94 replay fields: `repository_url`, `base_ref`, `allowed_patch_paths`, `setup_command`, `benchmark_command`, `result_path`, and `max_patch_bytes`.
3. Keep the validator generic. Put problem-specific scoring, datasets, and harness code in the public task repo. Hidden eval handles may come from the backend at replay time.
4. Enforce narrow patch surfaces. Submissions must patch only allowed files, with no bytecode, cache files, generated artifacts, model blobs, wallet files, secrets, or repo-wide rewrites.
5. Produce a poster-facing problem brief, an agent-facing implementation prompt, and an operator launch checklist.
6. Tell the poster to submit the finished proposal as a GitHub issue in `AlveusLabs/SN94-BitSota` with title `[Competition Proposal] <problem name>`, including the public task repo link.

## When Creating A Task Repo

Read `references/task-repo-spec.md` for the task repo contract and problem quality rules. Do not assume a fixed problem type. Pick the simplest task-specific submission format that fits the problem and can be replayed safely.

Use `scripts/create_competition_repo.py` when the user asks for a starter task repo:

```bash
python scripts/create_competition_repo.py \
  --out /tmp/sn94-example-task \
  --slug example-frontier \
  --title "Example Frontier"
```

## Review Checklist

- The task repo can be cloned and checked out at a pinned immutable ref.
- `setup_command` and `benchmark_command` run without network during reward-active validation unless the operator explicitly allows setup networking.
- `result_path` is a JSON file with enough fields for the backend to score and audit the result.
- `allowed_patch_paths` points only to miner-owned submission files.
- `max_patch_bytes` is present and small enough to prevent model-smuggling and oversized patch attacks.
- Public smoke tests exist, but release gating requires full local and testnet E2E replay.
- Hidden validation can rotate by backend-provided env or manifest without changing the public repo.
- The proposal states whether rewards are winner-take-all, pooled frontier, or another explicit policy.
- The final answer includes the submission target: `https://github.com/AlveusLabs/SN94-BitSota/issues/new?template=competition_proposal.md`.

## References

- `references/replay-contract.md`: SN94 backend and validator replay contract.
- `references/task-repo-spec.md`: task repo shape, examples, and scoring guidance.
- `references/marketplace-packaging.md`: Packaging the same skill for AgentSkills, Hermes/HermesHub, and Claw/OpenClaw.
