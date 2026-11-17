# Roundtable Output Template

This file defines the visual structure of the user-facing Markdown transcript. The actual transcript is generated from a Memory JSON file by [scripts/render_memory_to_markdown.py](../scripts/render_memory_to_markdown.py). Use this template as the layout reference when updating the renderer.

## Selected route

- **Character roster**: {{characters}}
- **Runtime claim**: {{runtime_claim}}
- **Output artifacts**: {{output_artifacts}}
- **Rounds run**: {{round_count}}
- **Seat expansions**: {{expansion_count}}
- **Memory file**: {{memory_file_path}}

## Why

{{rationale for roster, runtime, and protocol}}

## Runtime claim

{{single_backend_multi_session / real_subagent_runtime / soft_orchestration_only}}

## Discussion summary

### Round {{n}}

**Focus question**: {{focus_question}}

**Speaking order**: {{speaking_order}}

{{character}} [{{action_type}}]: {{speech_summary}}

...

## Synthesis

### Consensus

- {{point}}

### Divergence

- {{position_a}} vs {{position_b}}

### Open questions

- {{question}}

## Argument graph

When `metadata.output_artifacts` contains `argument_graph`, deliver a separate
`*.argument-graph.md` artifact generated from
`synthesis.argument_graph`. The artifact contains:

- a compact Mermaid viewpoint graph;
- the controlled relationship legend;
- node-to-speech traceability;
- edge rationales and source speech ids.

## Fallback

If the user wants a different shape, offer:

- Fewer characters and a single-round debate.
- A single perspective deep-dive instead of a roundtable.
- A different runtime tier (e.g., real subagents if available).
- A written essay synthesizing the same material without dialogue.

## Next step

{{continue / follow-up / export Memory}}

---

{{disclaimer}}
