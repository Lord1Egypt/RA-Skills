# Protocols

ThoughtCodec is built around two complementary protocols: decompression and compression.

## Decompression Protocol

Use decompression when the input is dense, abstract, strategic, or underspecified, and the expected result is an executable plan or artifact.

### Input

```json
{
  "intent_abstract": "The high-density goal or idea.",
  "context": "Relevant background, constraints, users, and environment.",
  "success_criteria": ["Observable outcome 1", "Observable outcome 2"],
  "constraints": ["Boundary 1", "Boundary 2"],
  "preferred_output": "SOP, architecture, code scaffold, checklist, diagram, or document"
}
```

### Output

```json
{
  "version": "V1.0.0",
  "logic_core": {
    "workflow_nodes": [
      {
        "step": 1,
        "action": "Concrete action",
        "input": "Required input",
        "output": "Expected output",
        "validation": "How to check the step"
      }
    ]
  },
  "presentation_layer": {
    "format": "Markdown, Mermaid, JSON, code tree, or table",
    "display_rules": "Presentation rules only; no business computation"
  }
}
```

## Compression Protocol

Use compression when the input is noisy, repeated, corrective, or operational, and the expected result is a reusable rule or skill.

### Input

```json
{
  "source_material": "Conversation history, diffs, logs, code, review notes, or repeated decisions.",
  "observed_problem": "What kept going wrong or repeating.",
  "human_correction": "What the user changed or clarified.",
  "reuse_target": "Prompt rule, skill, component, checklist, or policy"
}
```

### Output

```json
{
  "rule_id": "short-stable-id",
  "layer": "L1_Presentation | L2_Application | L3_Logic | L4_Base_Protocol",
  "rule": "Reusable rule stated as an instruction.",
  "evidence": ["Short evidence item 1", "Short evidence item 2"],
  "regression_checks": ["Check that prevents harmful overgeneralization"],
  "version_patch": "V1.0.1-draft"
}
```

## Four-Layer Evolution Model

| Layer | Scope | Examples |
| --- | --- | --- |
| L1 Presentation | Output style and formatting | Markdown layout, table shape, tone rules |
| L2 Application | Tool or domain usage | Codex workflow, Claude drafting, RPA source rules |
| L3 Logic | Core decision logic | Planning rules, validation strategy, data flow |
| L4 Base Protocol | Non-negotiable system principles | Privacy, safety, computation-presentation separation |

New rules should enter as draft patches. L3 and L4 changes need explicit review because they can affect many downstream tasks.

## Agentic Loop

```text
Task Ingestion
  -> Decompression
  -> Execution
  -> Telemetry
  -> Compression Gate
  -> Regression Check
  -> Merge or Rollback
```

The loop prevents the system from blindly treating every correction as a universal truth. Corrections become draft patches, then pass checks before becoming durable rules.
