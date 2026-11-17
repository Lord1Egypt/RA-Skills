# Question-list branch

The input is a batch of questions selected from any source: mistakes, review material, a topic needing practice, or a larger paper. Generation does not require knowing why each question was selected. A full-paper photo requesting a whole-paper variant still uses `full_paper` directly.

## Input contract

Accept plain text, Markdown, or JSON. Assign stable IDs and retain question text, choices, and essential diagram information. Grade, concepts, reference answers, practice goals, and diagnosis are optional. Recheck supplied answers. Missing student answers or error diagnoses are not a reason to refuse generation.

Structured handoff example; parents do not need to prepare this themselves:

```json
{
  "request": {
    "branch": "question_list",
    "generation": "variants",
    "language": "en",
    "answer_language": "en",
    "paper_size": "A4",
    "scope": "Previously learned multiplication using equal groups",
    "length": "About 10 minutes"
  },
  "questions": [
    {
      "id": "q1",
      "stem": "Write a multiplication equation for the picture.",
      "diagram_description": "Three separate boxes, each containing four dots. All dots are visible. Find the total number of dots.",
      "knowledge_points": ["Equal groups and multiplication"]
    }
  ]
}
```

`language`, `answer_language`, and `paper_size` are optional design instructions, not required configuration fields. Explicit values override inference. If absent, follow the main skill's language policy and A4 default. Preserve the input values and do not translate IDs.

`generation` distinguishes two intentions:

- `variants`: keep the concepts, change numbers, context, or representation, and generate new questions, diagrams, and solutions.
- `typeset`: arrange the supplied questions into a paper, preserving meaning and numbers. Do not silently create variants.

“Make similar questions” means `variants`; “put these questions into a worksheet” means `typeset`. Clarify only if the intent remains ambiguous and materially changes the result.

## Describing diagrams in text

Text can support diagram-based output when it preserves the information needed to solve the question:

- Grouped objects: group counts, objects per group, equal/unequal groups, and occlusion or overlap.
- Routes: ordered nodes, start and end, adjacency, and each segment's conditions. Distinguish stops from intervals.
- Jumps: count, equal-length conditions, starting point, labeled landing positions, and the unknown position.
- Geometry: shapes, dimensions, spatial relationships, constraints, and the requested quantity. Keep a cropped image as supplementary input when text cannot capture the diagram reliably.

Do not invent answer-determining conditions. Continue with complete items and identify missing inputs. Redrawing may change decorative style but must not give away quantities the student was meant to infer from the figure.

## Composition and review

Organize questions around the requested goal. Cover the supplied list by default; duplicates can be consolidated with source mappings preserved. Explain selection if a length limit prevents full coverage. Without diagnostic evidence, describe the paper as practice on the supplied questions, not a diagnosis of a learner.

Save the input list, generated content, and answer manifest. Retain `source_ids` for each output item and check coverage, completeness, difficulty, and diagram consistency. Internal drawing data is an implementation choice, not a question-template schema parents must supply.

Follow the main skill's PDF and mathematical review. Apply additional error-specific strategies only when relevant evidence is supplied.
