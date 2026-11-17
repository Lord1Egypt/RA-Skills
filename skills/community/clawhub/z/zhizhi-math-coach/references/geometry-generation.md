# Geometry Generation

## Purpose

Generate geometry practice that is reproducible, printable, and checkable.

These are optional internal tools, not the required public workflow. Default paper design follows `worksheet-generation.md`; parents receive the paper preview and print file without choosing a drawing technology. Use these helpers when repeatability is useful.

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

The renderer also supports `polygon`, `shape_collection`, `clock`, `number_line` and `grid`. Diagrams are bounded and validated before rendering.

## Automatic Visual Variants

```bash
python3 {baseDir}/scripts/generate_visual_practice.py \
  --kind mixed --count 4 --seed 12 \
  --output worksheets/visual-practice/worksheet-spec.json
python3 {baseDir}/scripts/generate_worksheet.py worksheets/visual-practice/worksheet-spec.json
```

Supported template kinds: `shape_collection` (count shapes), `clock` (whole/half hours), `number_line` (missing values up to 20), `grid` (count shaded cells), and `mixed`. Change `--seed` for reproducible variants. `--kind auto --workspace .` selects a supported visual knowledge point from the saved assessment, prioritizing weak/uncertain topics.

Stable IDs used for automatic topic selection:

| Knowledge-point ID | Template |
| --- | --- |
| `geometry.shape-recognition` | shape_collection |
| `time.clock-reading` | clock |
| `number.number-line` | number_line |
| `geometry.grid-counting` | grid |

Generated items use `review_status: template_verified`: the validator recalculates the expected prompt and answer from the geometry and rejects mismatches. This status does not mean a human reviewed the question. Edited/custom prompts should use the normal model/human review workflow. Clock hour hands include minute-dependent movement; hidden number-line values and digital clock answers do not appear in SVG accessibility text.

## Diagram Data

- `shape_collection`: `shapes` contains `kind` (`circle`, `triangle`, `square`, `rectangle`), `x`, `y`, `width`, `height`. Coordinates use the specified canvas; circle/square dimensions must match.
- `clock`: `hour` 0–23 and `minute` 0–59; use a canvas at least 180×180. The drawing represents a 12-hour dial, not an AM/PM indicator.
- `number_line`: integer `start`, `end`, positive `step`, and `hidden_values`; at most 20 intervals.
- `grid`: `rows`, `cols` up to 12 and unique zero-based `[row, col]` `shaded_cells`.
- `polygon`: three or more `[x, y]` `points` inside the canvas. The model must check side relationships and avoid unintended self-intersections; coordinate validation alone does not prove the mathematical diagram is correct.

For photo-derived variants, identify the tested concept and spatial relations before changing the diagram. A photo can contain overlapping shapes, folding, solids or perspective not covered by these templates. Preserve its original and diagram description; do not replace it with an unrelated easy template or claim exact reconstruction. Use custom structured geometry plus explicit review where feasible.

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
