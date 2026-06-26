# Timeline and Diagram Rendering

## :::timeline

Each item: `- Date: Description`

Whitelist for `Date`:

- `YYYY-MM-DD`
- `YYYY-MM`
- `YYYY`
- `Q[1-4] YYYY`
- `Day N`
- `Week N`
- `Month N`

**Temporal content rule (MANDATORY):** The `:::timeline` component is ONLY for content with actual dates, timestamps, or sequential time markers (e.g. `2024-07`, `Q1 2025`, `Day 1`, `Week 3`). It represents chronological progression — items must have a clear before/after relationship.

**Prohibited:** Do NOT use `:::timeline` for parallel, non-sequential items like principles, rules, features, or categories (e.g. "真诚服务", "安全可信", "专业高效" — these are并列关系, not chronological). For parallel items, use `:::list` or prose with `:::callout` instead.

**When in doubt:** If the items could be reordered without changing meaning, they are NOT timeline content.

- `invalid_syntax`: the item is not in `- Date: Description` form.
- `invalid_semantics`: the item is syntactically valid but `Date` is not actually chronological.
- `contract_conflict`: none.
- `auto_downgrade_target`: `list`.

    <div data-component="timeline" class="timeline fade-in-up">
      <div class="timeline-item">
        <div class="timeline-date">2024-07</div>
        <div class="timeline-dot"></div>
        <div class="timeline-content">Project kickoff</div>
      </div>
    </div>

## :::diagram

Generate inline SVG. All SVGs must be self-contained (no external refs). Wrap in:

    <div data-component="diagram" data-type="[type]" class="diagram-wrapper fade-in-up">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 [w] [h]">
        <!-- generated SVG -->
      </svg>
    </div>

**viewBox height rule:** Always add 30px of bottom padding beyond the last drawn element's bottom edge. For example, if the lowest element ends at y=346, set viewBox height to 376. This prevents content clipping.

Schema by `type`:

- `sequence`:
  ```yaml
  actors: [A, B, C]
  steps:
    - from: A
      to: B
      msg: 请求
  ```
- `flowchart`:
  ```yaml
  nodes:
    - id: start
      kind: oval
      label: 开始
  edges:
    - from: start
      to: step1
      label: 可选
  ```
- `tree`:
  ```yaml
  root: 平台
  children:
    - name: 数据层
      children: []
  ```
- `mindmap`:
  ```yaml
  center: 协同能力
  branches:
    - name: 流程
      items: [采集, 编排]
  ```

- `invalid_syntax`: body is missing the required keys for the chosen `type`.
- `invalid_semantics`: the structure parses but the chosen diagram type misrepresents the content.
- `contract_conflict`: examples previously acted as hidden spec. The schema above is now canonical.
- `auto_downgrade_target`: `callout`.

**type=sequence:** Draw vertical lifelines for each actor, horizontal arrows for each step. Actors as columns at top with labels, steps numbered on left, arrows with labels between lifelines.
Sizing: width = 180 × (actor count), height = 80 + 50 × (step count).

**type=flowchart:** Draw nodes as shapes (circle=oval, diamond=rhombus, rect=rectangle). Connect with directed arrows. Use edge labels where provided.
Sizing: width = 600, height = 120 × (node count).

**type=tree:** Top-down tree with root at top, children below, connected by lines.
Sizing: width = 200 × (max leaf count at any level), height = 120 × (depth).

**type=mindmap:** Radial layout, center node in middle, branches radiating out with items as leaf nodes.
Sizing: width = 700, height = 500.
