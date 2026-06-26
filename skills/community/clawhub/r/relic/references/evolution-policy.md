# Evolution policy

Relic should evolve, but it must not drift silently.

## Safe defaults

- Capture is append-only.
- Distillation may refresh structured summaries.
- Major identity changes should flow through proposals.
- Before apply, snapshot the current vault state.
- Package files are not mutable runtime state.

## What counts as a major change

- materially rewriting the tone or personality section
- removing or negating previously stable values or preferences
- compressing contradictory evidence into one overly confident claim
- changing exported agent instructions in a way that alters downstream behavior materially

## Approval guidance

- minor additive changes may be applied automatically
- major identity changes require explicit human approval

## Auditability

Every proposal should include:
- rationale
- source observations
- target files
- human-readable summary

## Publication boundary

When relic is installed from ClawHub/OpenClaw, the package should stay portable and generic.

That means:
- docs and metadata describe the package
- hooks and scripts operate on the configured vault path
- no proposal or apply step mutates package content
