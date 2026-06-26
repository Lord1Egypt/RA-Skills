# Causal Chain Analysis

## Task

Starting from the selected core problem, trace upward to find the root cause, build a clear problem tree, and identify the most actionable technical intervention points.

Core method: Why-Why analysis (continuously asking "why"), tracing from surface-level problems back to root causes, closing off at the engineering-operable layer or uncontrollable boundary.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Core problem description**: The selected core problem description
- **Functional model**: Functional modeling result data
- **Modification request** (optional): User-provided modification content, supplied in modification scenarios
- **Existing data** (optional): Previously generated causal chain content, supplied in modification scenarios

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "causal_chain_analysis" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[Problem Summary]
{problem summary content}

[Core Problem Description]
{core problem description automatically selected in Step 4}

[Functional Model]
{functional modeling result data}

// Append the following in modification scenarios
[Modification Request]
{user's modification content}

[Existing Data]
{previously generated causal chain content}
```

---

## Tool Result Parsing

The tool returns JSON-format data directly, with the following structure:

```json
{
  "causal_chain": [
    {
      "node_id": "N001",
      "parent_node": "ROOT",
      "problem_description": "Problem description",
      "logic_relation": "SINGLE",
      "key_problem": "",
      "node_type": "PROBLEM"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `causal_chain` array into a Markdown table with field mappings:
   - `node_id` → `Node ID`
   - `parent_node` → `Parent Node`
   - `problem_description` → `Problem Description`
   - `logic_relation` → `Logical Relationship`
   - `key_problem` → `Key Problem` (empty string outputs as empty cell)
   - `node_type` → `Node Type`

---

## Output Format

Display the parsed data in Markdown table format, containing six fields: node ID, parent node, problem description, logical relationship, key problem, and node type.

**Output example**:

| Node ID | Parent Node | Problem Description | Logical Relationship | Key Problem | Node Type |
|-------|-------|---------|---------|---------|---------|
| N001 | ROOT | Indoor environment is persistently humid, affecting living comfort | SINGLE | | PROBLEM |
| N002 | N001 | Condensate water seeps indoors, causing humidity to continuously rise | AND | | PROBLEM |
| N003 | N002 | Condensate water accumulates at joints and cannot drain in time | AND | 2 | PROBLEM |
| N005 | N003 | Drainage system flow capacity is insufficient to handle peak condensate water | OR | 1 | PROBLEM |
| N006 | N004 | Split design inevitably creates structural joints [Stop condition 3: geometric limit] | AND | | ROOT_CONSTRAINT |
