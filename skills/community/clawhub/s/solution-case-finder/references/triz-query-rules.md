# TRIZ Query Rules

## Problem Extraction

Extract these fields before querying:

- product or component
- function to improve
- failure mode or pain point
- measurable target
- worsening side effect
- industry domain
- material, structure, process, or control constraints
- operating environment

If the user gives only a broad problem, generate a best-effort query and ask one clarifying question after returning initial patterns.

## MCP Query Input

The `solution_search` tool accepts one required field, `user_question`, and one optional field, `limit`.

Build `user_question` as a compact English natural-language description. Include:

- user's original question
- product or component
- improvement target
- worsening constraint
- industry if known
- measurable constraints if known

Example:

```json
{
  "user_question": "A compact appliance fan should reduce noise without sacrificing airflow or increasing product volume. Search for similar TRIZ solution cases, especially airflow path design, fan control, and structural noise reduction.",
  "limit": 100
}
```

Use `limit: 100` by default to retrieve the largest supported result set. Do not send complex filters unless the MCP schema later exposes them.

## Query Expansion

Before calling MCP, mentally expand the question with three layers, but keep the actual tool input concise:

1. Direct technical terms from the user.
2. TRIZ contradiction terms:
   - improve speed vs accuracy
   - improve strength vs weight
   - improve heat dissipation vs volume
   - improve sealing vs assembly convenience
   - improve noise reduction vs airflow
   - improve yield vs process complexity
3. Inventive principle labels:
   - segmentation
   - taking out
   - local quality
   - asymmetry
   - merging
   - universality
   - nested doll
   - counterweight
   - preliminary action
   - prior cushioning
   - equipotentiality
   - inversion
   - spheroidality
   - dynamics
   - partial or excessive action
   - another dimension
   - mechanical vibration
   - periodic action
   - continuity of useful action
   - skipping
   - blessing in disguise
   - feedback
   - intermediary
   - self-service
   - copying
   - cheap short-living objects
   - mechanics substitution
   - pneumatic or hydraulic construction
   - flexible shells and thin films
   - porous materials
   - color changes
   - homogeneity
   - discarding and recovering
   - parameter changes
   - phase transitions
   - thermal expansion
   - strong oxidants
   - inert atmosphere
   - composite materials

## Industry Priority

Default search order:

1. User-specified industry.
2. Adjacent industries with similar physics or process constraints.
3. Cross-industry analogy among small appliances, automotive, semiconductor, and mechanical manufacturing.

Examples:

- Noise vs airflow: small appliances, automotive HVAC, rotating machinery.
- Heat dissipation vs compactness: semiconductor packaging, automotive thermal management, appliances.
- Accuracy vs speed: semiconductor process tools, mechanical fixtures, automotive assembly.
- Strength vs weight: automotive structures, mechanical manufacturing, appliance housings.

## Ranking

When `relevance_score` is provided, sort cases by score in descending order. When all scores are missing or null, preserve the MCP returned order. Present all returned cases by default, then summarize recurring patterns after the case list.

- clear problem-solution mapping
- explicit TRIZ principle labels
- source traceability for internal use
- same physical contradiction
- transferable mechanism, not just similar keywords
- recent or widely cited cases when available

If some cases only share surface words but solve a different engineering tradeoff, keep them in the full returned list but clearly mark them as weaker analogies rather than removing them.

## Synthesis

Do not simply list cases. Cluster cases into solution patterns and explain the transfer logic:

- Same contradiction, different industry.
- Same inventive principle, different structural implementation.
- Same structural pattern, different material or process condition.

Always distinguish direct applicability from analogy.
