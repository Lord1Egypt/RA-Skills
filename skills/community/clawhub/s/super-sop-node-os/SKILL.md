---
name: super-sop-node-os
description: Nodeize complex AI work for the node era: a 6-layer, 14-node SOP system with Radar, Normalize, Test, Score, Check, Handoff, and Sediment loops.
version: 1.0.3
metadata:
  openclaw:
    homepage: https://github.com/pagoda111king/super-sop-node-os
    requires:
      bins:
        - python3
---

# Super SOP Node OS · Node Era Protocol

Use this skill to turn complex work into node runs for projects, research, learning, implementation, enterprise delivery, and reusable SOP design.

## Node Era Thesis

AI work is moving from the large-model chat era, to the agent era, to OpenClaw / Hermes-style always-on systems, and now toward the node era.

In the node era, valuable work should be rebuilt as composable nodes. A node has a stable role, inputs, outputs, checks, memory, and a way to connect with other nodes. This makes AI work more reliable, reusable, testable, and improvable than one-off prompts.

## Default Behavior

For project-like, recurring, research-heavy, workflow, product, learning, or system-building tasks:

1. Select the smallest useful node chain.
2. Run nodes in order.
3. Produce durable artifacts when useful.
4. Run Check before delivery.
5. Sediment reusable assets only when they have `source_ref` and `next_use_case`.

For simple one-off tasks, use the minimum relevant nodes and do not over-process.

## 14 Node Classes

```text
Intake, Context, Radar, Normalize, Data, Planning, Routing, Learning, Action, Test, Score, Check, Handoff, Sediment
```

## Common Chains

```text
Research:
Intake -> Context -> Radar -> Normalize -> Score -> Check -> Sediment

Implementation:
Intake -> Context -> Planning -> Routing -> Action -> Test -> Check -> Handoff -> Sediment

Learning:
Intake -> Context -> Radar -> Normalize -> Learning -> Test -> Score -> Check -> Sediment

Enterprise:
Intake -> Context -> Data -> Planning -> Action -> Check -> Handoff -> Sediment
```

## Run Folder

When a durable run is useful, run:

```bash
python3 scripts/create_node_run.py --goal "<goal>" --type research
```

Then fill the generated node files.

## Reference Loading

Read only what is needed:

- `references/architecture.md` for 6-layer / 14-node architecture.
- `references/node-protocol.md` for node artifact format.
- `references/memory-symbols.md` for colors, runes, and memory palace symbols.
- `references/company-patterns.md` for external framework lessons mapped into nodes.
- `references/node-system-audit.md` for the v1.1 layer/rail recommendation.

## Quality Gate

Before finalizing complex work, answer:

```text
Which chain ran?
What evidence supports it?
What artifact was created?
What check passed?
What should be sedimented?
```

Do not send unlearned concepts directly into review/battle. Run Learning, enrichment, Test, Score, and Check first.

## Safety

This skill does not require external credentials. Its helper script creates local markdown run folders and should only write under the run root chosen by the user.
