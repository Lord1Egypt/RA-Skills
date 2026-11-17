# Node Expansion Rules

Figma URL `node-id` is a strong clue, not final proof of the exact repair target.

The script records:

- Target node.
- Parent candidates when available from the fetched tree.
- Target children up to `--max-child-depth`.
- Siblings up to `--max-siblings`.
- Candidate nodes with explicit `source`: `target`, `parent`, `child`, `sibling`, `component-instance`, or `layout-container`.

Warnings:

- `target_too_broad`: URL points at a page, section, huge frame, or node count exceeds budget.
- `target_may_be_child_node`: URL points at text, icon, vector, image, or an internal leaf node.
- `expansion_budget_exceeded`: script stopped expanding because a budget was reached.

Repair expert rule:

Use these candidates plus the issue text to choose the repair target. Do not write that the script identified a designer-confirmed unique target unless the artifact actually proves it.
