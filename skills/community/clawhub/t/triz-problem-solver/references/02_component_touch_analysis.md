# Contact Relationship Analysis

## Task

Based on the system component inventory and functional descriptions, analyze the contact relationship between every pair of components and output a standardized contact relationship matrix.

- If a modification request exists, understand the user's modification intent, adjust based on existing results, and re-output

---

## Input Information

Retrieve the following data from preceding steps:

- **Problem summary**: Core summary of the complete technical problem
- **System component list**: Each component includes its name and main functional description
- **Modification request** (optional): User-provided modification content, supplied in modification scenarios
- **Existing data** (optional): Previously generated contact analysis content, supplied in modification scenarios

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "component_touch_analysis" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[Problem Summary]
{problem summary content}

[System Component List]
{system component inventory content}

// Append the following in modification scenarios
[Modification Request]
{user's modification content}

[Existing Data]
{previously generated contact analysis content}
```

---

## Tool Result Parsing

The tool returns JSON-format data directly, with the following structure:

```json
{
  "contact_relations": [
    {
      "component_a": "Component A name",
      "component_b": "Component B name",
      "contact_type": "Contact relationship description"
    }
  ]
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert the `contact_relations` array into a Markdown table with field mappings:
   - `component_a` → `Component A`
   - `component_b` → `Component B`
   - `contact_type` → `Contact Relationship`
3. List only component pairs with contact relationships (upper triangle); component pairs not appearing in the table are assumed to have no contact

---

## Output Format

Display the parsed data in Markdown table format, listing only component pairs that have a contact relationship (upper triangle); component pairs not appearing in the table are assumed to have no contact.

**Output example** (6 components, showing component pairs with contact relationships):

| Component A | Component B | Contact Relationship |
|------|------|---------|
| Indoor unit | Top panel | Mechanical connection |
| Indoor unit | Bottom panel | Mechanical connection |
| Indoor unit | Power module | Energy transfer |
| Indoor unit | Wiring | Energy transfer |
| Top panel | Bottom panel | Surface bonding |

**Key requirements**:
1. Output strictly in the order of component input
2. List only component pairs with contact relationships; do not output non-contact or self-referential relationships
3. Output only the table, without additional text descriptions
