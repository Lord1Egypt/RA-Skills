# Problem Description and Core Problem Selection

## Task

Convert the key problems already identified in functional modeling into a user-friendly problem description list. Each problem will serve as an entry point for the user to proceed with causal chain analysis. Based on the problem identifiers already assigned in the system structure analysis, convert functional relationship data into clear, specific, and actionable problem descriptions, maintaining full consistency with the structural analysis.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Functional model**: Functional modeling analysis results
- **System structure analysis**: Structural elements containing annotated problem identifiers

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "functional_modeling_problem_summary" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[Problem Summary]
{problem summary content}

[Functional Model]
{functional modeling analysis results}

[System Structure Analysis]
{structural elements containing problem identifiers}
```

---

## Tool Result Parsing

The tool returns JSON-format data directly, with the following structure:

```json
{
  "problems": [
    {
      "id": 1,
      "problem_type": "Problem type",
      "problem_description": "Problem description"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `problems` array into a Markdown table with field mappings:
   - `id` → `#`
   - `problem_type` → `Problem Type`
   - `problem_description` → `Problem Description`

---

## Output Format

Display the parsed data in Markdown table format, containing three fields: number, problem type, and problem description, with 3–5 problems.

**Output example**:

| # | Problem Type | Problem Description |
|---|---------|---------|
| 1 | Harmful elimination | **[Root cause problem]** The **connection structure** amplifies the **gap** at the panel joint, becoming the underlying source of condensate water leakage |
| 2 | Function enhancement | **[Key link]** The **sealing structure**'s ability to block **condensate water** is insufficient, directly leading to the formation of a leakage path |
