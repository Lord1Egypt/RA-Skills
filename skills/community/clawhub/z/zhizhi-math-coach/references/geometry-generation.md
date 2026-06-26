# Geometry Generation

## Purpose

Generate geometry practice that is reproducible, printable, and checkable.

Do not use free-form AI images as the default. Use structured `geometry_spec` and deterministic SVG/HTML rendering.

## Supported V1 Pattern

Use `geometry_problem` items with:

```json
{
  "type": "geometry_problem",
  "prompt": "求下面长方形的周长。",
  "geometry_spec": {
    "type": "rectangle",
    "width_label": "8 cm",
    "height_label": "5 cm"
  },
  "answer_prompt": "周长是",
  "answer_suffix": "cm",
  "answer_detail": "`(8 + 5) × 2 = 26`，周长是 26 cm。"
}
```

V1 supports simple deterministic diagrams. Extend carefully when a format will recur.

## Quality Rules

- Labels must be readable after printing.
- Diagrams must not reveal answers that should be solved.
- The child-facing worksheet must not contain `answer_detail`.
- The answer key must include the formula and intermediate values.
- If a diagram is ambiguous or cannot be rendered deterministically, mark it `human_review_needed`.

## Future Geometry Extensions

- angles;
- measuring lines;
- composite area and perimeter;
- grid-based shapes;
- symmetry and folding;
- unit conversion around area and perimeter.
