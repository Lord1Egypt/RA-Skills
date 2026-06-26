# Solution Detail Generation

## Task

Based on the concept solution selected by the user, generate complete solution details in one pass, including the solution name, working principle, technology grafting, solution conversion logic, implementation method, and a mermaid-format implementation flowchart.

---

## Input Information

Retrieve the following data from preceding steps:

- **User problem**: Confirmed core problem / improvement goal
- **Key problem**: Description of the causal chain key problem that the user's selected solution belongs to
- **Concept solution**: Complete concept solution data selected by the user, including idea_id, solution title, solution summary, advantage tags, applied TRIZ principles, feasibility rating, analysis method, whether cross-domain, and associated patent feature mapping information
- **Component analysis**: System component inventory and functional descriptions
- **Functional model**: Functional modeling results
- **Patent information**: Reference patent data associated with the concept solution, including patent title, feature type, feature content, and application method

---

## Execution Method

Invoke the `triz_analysis` MCP tool to complete this task:

```bash
bash scripts/call_triz_analysis.sh "solution_detail" "<user_input>"
```

`user_input` uses tags to distinguish each section:
```
[User Problem]
{core problem / improvement goal}

[Key Problem]
{causal chain key problem description}

[Concept Solution]
{complete concept solution data selected by the user}

[Component Analysis]
{system component inventory and functional descriptions}

[Functional Model]
{functional modeling results}

[Patent Information]
{associated reference patent data}
```

---

## Tool Result Parsing

The tool returns JSON-format data with the following structure:

```json
{
  "idea_id": "idea_id of the concept solution",
  "idea_title": "consistent with the input concept solution title",
  "principle_of_work": "working principle description, with patent citation markers [1], [2]",
  "technical_grafting": [
    {
      "patent_id": "PN number",
      "description": "Extract [original patent core mechanism] + Execute [specific adaptation action] → Solve [current specific problem]"
    }
  ],
  "implementation": "complete Markdown content of specific implementation method",
  "implementation_flowchart": "mermaid-format flowchart code"
}
```

### Parsing Rules

1. Parse the JSON data returned by the tool
2. Convert each field to Markdown format output:
   - `idea_id` → idea identifier for the solution detail
   - `idea_title` → solution detail title (`## Solution Details: {idea_title}`)
   - `principle_of_work` → `### Working Principle` section content
   - `technical_grafting` → `### Technology Grafting Description` section, each record formatted as: `- **Patent {patent_id}**: {description}`
   - `implementation` → `### Specific Implementation Method` section content (output Markdown directly)
   - `implementation_flowchart` → `### Implementation Flowchart` section, wrapped in a mermaid code block

---

## Output Format

Display the parsed data in Markdown format:

```
## Solution Details: [idea_title]

### Working Principle
[principle_of_work]

### Technology Grafting Description
- **Patent [PN]**: [description]

### Specific Implementation Method
[implementation]

### Implementation Flowchart
[mermaid flowchart]
```
