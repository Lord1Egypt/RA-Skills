# Causal Chain Problem Filtering

## Task

Filter the most valuable core problems from the causal chain analysis results, generate a problem selection menu that balances technical depth and user-friendliness, for the user to select and proceed to solution generation.

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **Functional model**: Functional modeling result data
- **Causal chain analysis results**: Causal chain analysis output

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "causal_chain_problem_summary" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[Problem Summary]
{problem summary content}

[Functional Model]
{functional modeling result data}

[Causal Chain Analysis Results]
{causal chain analysis output}
```

---

## Tool Result Parsing

The tool returns JSON-format data directly, with the following structure:

```json
{
  "selected_problems": [
    {
      "id": 1,
      "user_friendly_description": "User-friendly description",
      "technical_description": "Technical detailed description"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `selected_problems` array into a Markdown table with field mappings:
   - `id` → `#`
   - `user_friendly_description` → `User-Friendly Description`
   - `technical_description` → `Technical Detailed Description`

---

## Output Format

Display the parsed data in Markdown table format, containing three fields: number, user-friendly description, and technical detailed description. The number of problems matches the number of key problem identifiers in the input (maximum 3).

**Output example**:

| # | User-Friendly Description | Technical Detailed Description |
|---|------------|------------|
| 1 | [Adjust operating parameters] **Cooling system controller** sets temperature too low → frost forms on fin surface | The refrigerant evaporation temperature target set by the **cooling system controller** is too low (pursuing high cooling capacity), causing the root temperature of the **air conditioner fin heat exchanger** to continuously stay below the air dew point temperature (over-cooled), driving water vapor in the air to continuously condense and solidify into frost on the fin surface |
