# Generated Skill Multi-Candidate Policy

Version: 1.0.1

Every generated figure-making skill must inherit this policy.

```yaml
candidate_policy:
  text_candidates_default: 6
  text_candidates_min: 4
  text_candidates_max: 6
  image_candidates_default: 6
  image_candidates_min: 4
  image_candidates_max: 6
  if_user_says_generate_without_count: default_to_6_images
  single_image_only_when_explicit: true
  always_prompt_for_multi_candidate_images: true
  candidate_image_bridge_required_after_multi_option_text: true
  required_bridge_steps:
    - TEXT_ONLY_candidate_board_setup
    - IMAGE_ONLY_candidate_board_generation
    - TEXT_ONLY_candidate_review_and_direction_lock
  key_visual_decision_default: recommend_6_generated_candidate_images_before_locking_direction
  rendering_route_for_candidate_images: ChatGPT web Create image through ChatGPT Images 2.0; Codex $imagegen skill first; if unavailable, ChatGPT Images 2.0 API or another approved image-generation API.
  svg_or_code_visual_candidates_allowed: false
  native_image_generation_required: true
  native_generated_bitmap_exports_allowed: true
  allowed_native_bitmap_output_formats: [png, jpg, jpeg, webp]
  forbidden_generated_visual_outputs: [svg, mermaid, tikz, graphviz, html_css_diagram, canvas_diagram, matplotlib_figure, code_generated_figure]
```

## Required Behavior

1. In candidate-scheme steps, provide 4-6 text candidates, normally 6.
2. After presenting text candidates, do not make “choose one from text” the primary next action. The first/recommended next prompt must ask to generate/display candidate images or schematic candidates, normally 6.
3. Add a dedicated `TEXT_ONLY` candidate-board setup step. It must state candidate count, varied axis, fixed elements, rendering route, and comparison criteria.
4. Add a dedicated `IMAGE_ONLY` candidate-board generation step. It must generate/display 4-6 candidate images or schematic candidates, normally 6, with no prose or state footer.
5. Add a dedicated `TEXT_ONLY` candidate-review step. It must record the previous image batch, compare candidates, recommend one direction, and ask the user to select, revise, or request another board.
6. If the user says only “继续 / 出图 / 生成 / generate” after a text-candidate or board-setup step, default to 6 candidate images.
7. Generate one image only when the user explicitly asks for one.
8. Map each image candidate to a scheme, layout, style, metaphor, density, or prompt variant.
9. Track `text_candidate_count`, `image_candidate_count`, `candidate_generation_mode`, `candidate_scheme_ids`, `candidate_comparison_focus`, `visual_candidate_board_status`, `candidate_image_batch_id`, and `selected_visual_candidate`.
10. Support optional sample/reference images with per-image attribute preferences.

## Required Chinese Reminder

Generated skills must include a reminder equivalent to:

> 以上是默认的 4-6 个文字候选方案，通常 6 个。  
> 下一步不要只从文字方案里定稿；建议先生成 **6 张候选图/示意图** 来比较方向，也可以指定 4 张或 5 张。  
> 请下一步要求输出展示多张候选图或示意图，然后再选择、合并或修改方向。  
> ChatGPT 网页版会使用 **Create image** 并通过 **ChatGPT Images 2.0** 生图；Codex 会优先使用 **$imagegen skill**，如果不可用，再使用 ChatGPT Images 2.0 API 或其他批准的图像生成 API。候选图可以输出 PNG/JPEG/WebP 等位图结果，但不会使用 SVG、Mermaid、TikZ、Graphviz、HTML/CSS、canvas、matplotlib 或代码绘图替代。

## Lock/Test Requirement

Fail the generated skill lock if any of these are missing:

- default text candidate count = 6;
- default image candidate count = 6;
- dedicated candidate-board setup step after text candidates;
- dedicated `IMAGE_ONLY` candidate-board generation step;
- dedicated candidate-review/selection step after image generation;
- next prompts after multi-option text ask for multiple candidate images or schematic candidates;
- rendering route uses ChatGPT web Create image / ChatGPT Images 2.0 and Codex `$imagegen` first;
- forbidden code/vector fallback list;
- state fields for candidate counts, visual board status, image batch ID, and selected candidate.
