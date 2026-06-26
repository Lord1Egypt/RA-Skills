# Solution Generation

## Task

Retrieve the key problem description selected by the user from the causal chain problem filtering, and generate concept solution recommendations in two phases:
1. **Phase 1**: Invoke the `batch_solution_workflow` MCP tool to batch-generate concept solutions, then recommend the Top 4 solutions to the user after filtering and ranking
2. **Phase 2**: Based on the Top 4 solutions recommended in Phase 1, invoke the `image_generation` MCP tool in parallel to generate a concept schematic for each solution

---

## Input Information

Retrieve the following data from the causal chain problem filtering:

- **Key problem list**: Key problems selected by the user from the causal chain analysis (maximum 3)
- **Problem description**: Technical detailed description of each key problem (content of the problem_description field)

---

## Phase 1: Concept Solution Generation

### Tool Invocation Instructions

Invoke the `batch_solution_workflow` MCP tool:

```bash
bash scripts/call_batch_solution_workflow.sh 'INNOVATION' '[{"problem_type":"Causal chain key problem","problem_description":"Technical detailed description of the specific problem selected by the user"}]'
```

#### Input Parameters

```json
{
    "workflow_type": "INNOVATION",
    "problems": [
        {
            "problem_type": "Causal chain key problem",
            "problem_description": "Technical detailed description of the specific problem selected by the user"
        }
    ]
}
```

- `workflow_type` (required): Workflow type, fixed value `"INNOVATION"`
- `problems` (required): List of problems selected by the user, each record corresponds to a specific problem
  - `problem_type`: Fixed value "Causal chain key problem", used as a problem group identifier
  - `problem_description`: Technical detailed description content of the problem selected by the user

#### Return Results

The tool returns JSON-format data, a collection of concept solutions grouped by problem:

```json
{
  "solution_idea_groups": [
    {
      "key_problem": {
        "problem_type": "Causal chain key problem",
        "problem_description": "Specific problem description",
        "select": true
      },
      "idea_list": [
        {
          "idea_id": "Unique solution identifier (UUID)",
          "problem": "Corresponding problem description",
          "idea_title": "Concept solution title",
          "advantage_tag_list": ["Advantage tag 1", "Advantage tag 2"],
          "idea_summary": "Solution summary (HTML format, with technical parameters)",
          "analysis_method": "Analysis method",
          "triz_principle": "Applied TRIZ principle",
          "is_cross_domain": false,
          "feasibility": "Feasibility rating (high/medium/low)",
          "triz_feature_mapping": [
            {
              "patent_id": "Reference patent ID",
              "title": "Reference patent title",
              "feature_type": "Feature type",
              "feature_content": "Feature content description",
              "application_method": "Application method description"
            }
          ]
        }
      ],
      "used_patent_ids": ["List of cited patent IDs"]
    }
  ]
}
```

### Result Processing Rules

> **Note**: If a problem in the returned results has no corresponding solution data, it means no solution can currently be found for that problem. This is normal and the tool does not need to be called again.

#### 1. Flatten

Flatten all concept solutions from all groups into a one-dimensional list, with each solution retaining the key problem description it belongs to as a source identifier.

#### 2. Comprehensive Ranking

Rank solutions comprehensively by the following factors (priority from high to low):

1. **Feasibility**: High > Medium > Low
2. **Innovativeness**: Prefer cross-domain solutions and solutions containing unique TRIZ principles
3. **Implementation difficulty**: Prefer solutions with tags such as "technically mature", "simple structure", "easy to manufacture"
4. **Source diversity**: Try to cover different key problems; avoid all solutions coming from the same problem

#### 3. Take Top 4

Take the top 4 concept solutions from the ranked list.

### Output Format

Display 4 concept solutions in a numbered list, each with complete details. **Immediately execute Phase 2 after output is complete**:

```
### Concept Solution Recommendations

---

**Solution 1: [Solution Title]**

**Basic Information**
- Source problem: [Key problem description]
- Feasibility: [High/Medium/Low]
- Analysis method: [Name]
- TRIZ principle: [Principle name]
- Cross-domain: [Yes/No]

**Advantage Tags**
[Each tag displayed independently]

**Solution Summary**
[Converted to plain text, displayed item by item]

**Reference Patents and Application Methods**

| PN | Patent Title | Feature Type | Feature Content | Application Method |
|------|---------|---------|---------|---------|
| [PN](https://eureka.patsnap.com/view/#/fullText'figures/?patentId={patent_id}) | ... | ... | ... | ... |

---

**Solution 2: [Solution Title]**
...
```

#### Analysis Method Name Mapping

| English Value | Display Name |
|-------|---------|
| physical_contradiction | Physical contradiction analysis |
| technical_contradiction | Technical contradiction analysis |
| function_modeling | Functional modeling analysis |
| substance_field_model | Substance-field model analysis |

#### Feature Type Name Mapping

| English Value | Display Name |
|-------|---------|
| physical_contradiction | Physical contradiction |
| technical_contradiction | Technical contradiction |
| function_fingerprint | Function fingerprint |
| sufield_features | Substance-field features |

---

## Phase 2: Concept Solution Schematic Generation

Based on the Top 4 concept solutions recommended in Phase 1, **invoke** the `image_generation` MCP tool **in parallel**, generating schematics for all solutions simultaneously.

### Tool Invocation Instructions

Initiate calls for all Top 4 solutions simultaneously. Use the corresponding solution's `idea_id` field and `idea_summary` field content:

```bash
bash scripts/call_image_generation.sh "[idea_id of the solution]" "[idea_summary content of the solution]"
```

### Return Result Processing

The tool returns a result containing `idea_id` and an `images` list, each item containing `image_object_key` and `image_url`. Match the corresponding solution by `idea_id`, and take the `image_url` of the first image to display below the corresponding solution.

### Phase 2 Output Format

After Phase 2 is complete, **output only the concept schematics for each solution**, arranged by solution number:

```
**Solution 1 Concept Schematic**
![Solution 1 Schematic]([image_url])

**Solution 2 Concept Schematic**
![Solution 2 Schematic]([image_url])

**Solution 3 Concept Schematic**
![Solution 3 Schematic]([image_url])

**Solution 4 Concept Schematic**
![Solution 4 Schematic]([image_url])
```

---

## User Interaction: Show More Solutions

Triggered when the user expresses the following intent:
- "Show more", "show different solutions", "are there other solutions?", "let me see others"
- "I want to see more solutions", "any other ideas?", "recommend a few more"

**Processing rules**:
1. Re-select from the most recent tool call's return results
2. Exclude solutions that have already been displayed
3. If the user expresses a specific preference (e.g., "I want cross-domain ones", "are there simpler ones?"), adjust ranking weights according to the user's requirements and re-select 4 solutions
4. If fewer than 4 solutions remain, display all remaining solutions and inform the user "All solutions have been displayed"
5. After showing more, also execute Phase 2 to generate schematics for the newly recommended solutions

---

## Guide User Selection

After displaying concept solutions, guide the user to select one solution for detailed design:

> The above are the Top 4 concept solutions after comprehensive ranking. Please select a solution to generate a detailed design (enter a number from 1–4), or enter "show more" to see additional solutions.

After the user selects → read [08_solution_detail.md](08_solution_detail.md) to generate the detailed design.
