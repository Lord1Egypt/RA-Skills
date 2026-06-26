# Analysis schema for UI inspiration ingestion

Generate a structured analysis object from each incoming design image.

## Required output fields

```json
{
  "title": "Web dashboard with dense KPI cards",
  "platform": "Web",
  "page_type": ["Dashboard", "Data Table"],
  "style_tags": ["B2B", "Dense Layout", "Card-based"],
  "component_tags": ["Sidebar", "Table", "Filter Bar", "Chart"],
  "use_case": ["SaaS", "Admin"],
  "highlights": [
    "Clear information hierarchy with distinct KPI grouping",
    "Dense filtering and table controls remain readable",
    "Charts support quick scanning before deeper analysis"
  ],
  "summary": "A strong high-density B2B dashboard reference with clear KPI framing, robust table control patterns, and good scanability for data-heavy products.",
  "reference_value": "High",
  "source": ""
}
```

## Field guidance

### title
Create a concise retrieval-friendly title. Avoid generic titles like "UI design" or "nice screenshot".

### platform
Infer the likely platform from layout traits. Use the stable vocabulary values. Use `Unknown` when uncertain.

### page_type
Use 1-3 high-signal categories only. Prefer the recommended vocabulary first, then extend if needed.

### style_tags
Tag the overall visual/system character, not every visible detail. Use stable values and prefer reusing existing tags before adding new ones.

### component_tags
Focus on reusable UI patterns and structures. Use stable values and normalize near-duplicates before adding new ones.

### use_case
Infer probable business/domain context conservatively. Use stable values and keep the list compact.

### highlights
Write 2-5 short points in the user's language when helpful. Emphasize reusable design ideas, not vague praise.

### summary
Write one compact paragraph in the user's language explaining why the reference is useful.

### reference_value
Use:
- `High` for strong reusable references with clear patterns
- `Medium` for useful but ordinary references
- `Low` for weak, noisy, or low-transfer value material

## Classification principle

This skill is for design inspiration archiving, not pixel-perfect critique.
Prioritize:
1. retrievability,
2. reusable patterns,
3. practical inspiration value.

Do not overfit to visual trivia.
