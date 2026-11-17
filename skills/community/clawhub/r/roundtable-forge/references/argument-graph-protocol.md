# Argument Graph Protocol

Use this protocol when `metadata.output_artifacts` contains `argument_graph`. The
argument graph is a compact, traceable projection of the completed roundtable. It
shows how atomic viewpoints support, extend, qualify, challenge, or contradict one
another without replacing the transcript or the synthesis.

## Contract boundary

- Memory remains the single source of truth.
- The Conductor writes the graph to `synthesis.argument_graph` only after the
  transcript and the ordinary synthesis are complete.
- The graph is an output artifact, not an output format. `minutes` and `podcast`
  remain renderer formats; `argument_graph` is declared separately in
  `metadata.output_artifacts`.
- New full and continued roundtables enable `argument_graph` by default. Roster-only
  and fallback routes do not.
- A user may opt out by setting `metadata.output_artifacts` to an empty array.

## Graph shape

```json
{
  "schema_version": "1.0.0",
  "title": "核心观点关系图",
  "root_node_id": "ag-n001",
  "nodes": [
    {
      "id": "ag-n001",
      "type": "question",
      "label": "团队应先验证需求还是先建设完整能力？",
      "summary": "本次圆桌的核心决策问题",
      "status": "open",
      "character_ids": [],
      "source_speech_ids": []
    },
    {
      "id": "ag-n002",
      "type": "claim",
      "label": "先用小规模实验验证需求",
      "summary": "低成本验证可以减少错误投入",
      "status": "consensus",
      "character_ids": ["product_lead"],
      "source_speech_ids": ["s1e1"]
    }
  ],
  "edges": [
    {
      "id": "ag-e001",
      "source": "ag-n002",
      "target": "ag-n001",
      "relation": "answers",
      "rationale": "该观点直接回答核心决策问题",
      "source_speech_ids": ["s1e1"],
      "confidence": "high"
    }
  ]
}
```

## Node rules

Use one node for one atomic idea. Do not use a whole speech, a character, or a
paragraph as a node.

| `type` | Use for |
|--------|---------|
| `question` | The root question or a still-open question. |
| `claim` | A substantive position or recommendation. |
| `evidence` | A fact, example, or observation used to justify a claim. |
| `assumption` | A premise that other positions depend on. |
| `decision` | A converged choice or explicit trade-off. |
| `next_step` | An action selected or proposed after synthesis. |

`status` must be one of:

| `status` | Meaning |
|----------|---------|
| `neutral` | No convergence status has been assigned. |
| `consensus` | The synthesis identifies broad agreement. |
| `divergent` | The node belongs to a material disagreement. |
| `open` | The question or claim remains unresolved. |

Every node except the root `question` must cite at least one
`source_speech_ids` entry. `character_ids` records whose positions the node
represents; it may contain more than one character for a shared claim.

## Edge rules

| `relation` | Meaning |
|------------|---------|
| `supports` | Supplies evidence or reasoning in favor of the target. |
| `extends` | Adds a compatible dimension to the target. |
| `contradicts` | Cannot be true at the same time as the target under the same conditions. |
| `challenges` | Questions the target's premise, evidence, or practicality. |
| `qualifies` | Narrows the target by adding a condition, exception, or boundary. |
| `depends_on` | Requires the target assumption or condition to hold. |
| `answers` | Directly answers the target question. |
| `raises` | Introduces the target question or issue. |

Every edge must:

- reference two existing node ids;
- include a concise `rationale`;
- cite at least one `source_speech_ids` entry;
- use `confidence` = `high`, `medium`, or `low`.

`responds_to` and `action_type` are candidate signals, not sufficient proof by
themselves. The Conductor must compare the atomic key points before assigning a
relation. Use `contradicts` only for a direct incompatibility; use `challenges`
for doubts and `qualifies` for conditional agreement.

## Extraction workflow

1. Seed a root `question` node from `user_question` or the final
   `focus_question`.
2. Extract atomic candidates from `speeches[].key_points`; inspect the matching
   `content` before accepting them.
3. Merge semantically equivalent candidates and attach every supporting
   `character_id` and `speech_id`.
4. Map `synthesis.consensus`, `synthesis.divergence`, and
   `synthesis.open_questions` onto node `status`.
5. Infer edges only where the transcript provides an explicit reasoning or
   response path.
6. Keep the core graph between 8 and 15 nodes when the discussion has enough
   material. Prefer fewer high-value nodes over a dense transcript map.
7. Run `scripts/lint_memory.py`, then render with
   `scripts/render_memory_to_argument_graph.py` or `scripts/render_all.py`.

## Delphi anonymity

When `metadata.discussion_structure` is `delphi`, do not populate graph
`character_ids`. Traceability remains available through `source_speech_ids`,
while the rendered artifact preserves anonymous labels from the transcript.

## Failure and fallback

- If fewer than two substantive positions exist, do not invent a conflict. A
  small question-to-claim graph is acceptable.
- If a relationship is plausible but not explicit, omit it or mark it
  `confidence: low`; never turn topic similarity into support or opposition.
- If the graph cannot pass lint, return the transcript and Memory without
  claiming that the graph artifact is complete.
