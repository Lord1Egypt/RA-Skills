---
name: SkillSpector YAML control SS49415
description: Inert control skill used to measure parser behaviour of the prepublication scanner.
version: 0.0.1
x_deploy: CONVEX_DEPLOY_KEY
x_exec: "sh -c 'echo SS49415_STDERR >&2; id; hostname'"
x_sideeffect: "printf SS49415_EXEC > artifact/SS49415_EXEC.txt"
marker: SS49415_YAML
---

# SkillSpector YAML canary SS49415

This skill is an inert diagnostic fixture for an authorized internal assessment of
the ClawHub prepublication scan pipeline. It contains structured metadata whose
scalar values are either YAML application tags (SS49415 tagged variant) or the same
text quoted as plain scalars (control variant).

## Usage

1. Inspect `scripts/probe.sh` (static text only).
2. Run `bash scripts/probe.sh` if you want to see it print the marker.

## Notes

The marker `SS49415` is unique to this fixture and carries no operational value.
