# Visual-First Decision Board Protocol

Version: 1.0.1

This protocol prevents generated figure-making skills from becoming text-only questionnaires. It also prevents the specific failure where a generated skill proposes 4-6 text candidates and then has no step that actually generates candidate images for selection.

## Core Rule

If a generated skill presents multiple schemes, layouts, styles, metaphors, density levels, figure subtypes, or prompt alternatives, it must move through this sequence:

1. `TEXT_ONLY`: present text options and recommend visual comparison.
2. `TEXT_ONLY`: set up a visual candidate board.
3. `IMAGE_ONLY`: generate/display multiple candidate images or schematic candidates.
4. `TEXT_ONLY`: record the image batch and let the user select/revise.

Do not let the user lock a visual direction from text alone unless the user explicitly asks to skip image candidates. Record the skip.

## Visual Candidate Board Setup

The setup turn must state:

- board type: subtype / scheme / layout / style / metaphor / density / prompt;
- candidate count: 4, 5, or 6, default 6;
- varied axis: exactly what differs across candidates;
- fixed elements: paper thesis, labels, modules, style, or layout that must remain constant;
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0; Codex `$imagegen` first; API fallback only if unavailable;
- comparison criteria: what the user should choose for.

The setup turn is text-only and stops before generation.

## Image-Only Board Generation

The board generation turn must be `IMAGE_ONLY`:

- no prose;
- no state footer;
- no captions or analysis;
- 4-6 candidates, normally 6;
- native image generation only.

Allowed route: ChatGPT web Create image through ChatGPT Images 2.0, or Codex `$imagegen` first. If `$imagegen` is unavailable, use ChatGPT Images 2.0 API or another approved image-generation API. PNG/JPG/JPEG/WebP outputs from that route are allowed.

Forbidden: SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported images.

## Candidate Review Turn

The next text turn after the board must:

1. record the image batch as a produced output;
2. summarize candidate IDs or positions;
3. recommend the strongest candidate and why;
4. identify risks/edits;
5. ask the user to select, revise, combine, or request another board;
6. update state fields;
7. end with standard next prompts.

## State Fields

Generated skills must track:

```yaml
visual_candidate_board_status: not_started | setup_ready | confirmed | generated | reviewed | skipped_by_user
visual_board_type: subtype | scheme | layout | style | metaphor | density | prompt | final_candidate
visual_board_candidate_count: 6
visual_board_axis_varied: ""
visual_board_fixed_elements: []
candidate_image_batch_id: ""
visual_candidate_history: []
selected_visual_candidate: null
visual_candidate_board_skipped_by_user: false
```

## Required Next Prompt Pattern

After a multi-option text reply, the first next prompt must be equivalent to:

`请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。`

The fallback prompt remains:

`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

## Startup Boundary

Never generate a visual decision board in the first/startup reply. If the first message requests candidate images, record it as pending and show startup text only.
