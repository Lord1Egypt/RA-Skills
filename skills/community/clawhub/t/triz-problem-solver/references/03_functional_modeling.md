# Functional Modeling

## Task

Based on system component information and contact analysis results, build a complete functional relationship network, identify beneficial, harmful, and neutral functions, and provide an accurate functional model foundation for subsequent technical contradiction analysis and innovative solution design.

- Every component in the system component list must appear at least once in the model
- For core problem components, deeply decompose their conflict chains; for peripheral components, assign only the most basic maintenance functions (support, containment, etc.) without diverging or creating unnecessary connections
- If a modification request exists, understand the user's modification intent and adjust based on existing results

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **System component list**: System component inventory
- **Contact relationship matrix**: Contact relationships between components
- **Modification request** (optional): User-provided modification content, supplied in modification scenarios
- **Existing data** (optional): Previously generated functional modeling content, supplied in modification scenarios

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "functional_modeling" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[Problem Summary]
{problem summary content}

[System Component List]
{system component inventory content}

[Contact Relationship Matrix]
{contact relationship analysis content}

// Append the following in modification scenarios
[Modification Request]
{user's modification content}

[Existing Data]
{previously generated functional modeling content}
```

---

## Tool Result Parsing

The tool returns JSON-format data directly, with the following structure:

```json
{
  "functional_relations": [
    {
      "function_carrier": "Function carrier name",
      "action": "Action",
      "function_object": "Function object name",
      "performance_level": "N (Normal)"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `functional_relations` array into a Markdown table with field mappings:
   - `function_carrier` → `Function Carrier`
   - `action` → `Action`
   - `function_object` → `Function Object`
   - `performance_level` → `Performance Level` (extract the letter part, e.g., `N (Normal)` → `N`)

---

## Output Format

Display the parsed data in Markdown table format, containing four fields: function carrier, action, function object, and performance level (H/I/N/E).
- **H (Harmful)**: Causes performance degradation >20%, creates safety risks, or causes user discomfort
- **I (Insufficient)**: Function completion <70%, fails to meet design specifications
- **E (Excessive)**: Function output >130% of requirement, causes resource waste >20%
- **N (Normal)**: None of the above conditions are met

**Output example**:

| Function Carrier | Action | Function Object | Performance Level |
|-----------------|--------|-----------------|-------------------|
| Cooling system | Cools | Top panel | N |
| Condensate water | Wets | Connection structure | H |
| Sealing structure | Blocks | Condensate water | I |
