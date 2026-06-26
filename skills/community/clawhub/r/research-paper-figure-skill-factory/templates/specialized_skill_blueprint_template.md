# Specialized Figure Skill Blueprint Template

```yaml
target_figure_class: ""
target_skill_slug: ""
version: ""
domain_scope: ""
intended_paper_slots: []
reader_questions: []
figure_taxonomy_axes: []
figure_type_cards: []

workflow:
  production_steps:
    P1: {mode: TEXT_ONLY, purpose: material_intake}
    P2: {mode: TEXT_ONLY, purpose: figure_need_diagnosis_and_routing}
    P3: {mode: TEXT_ONLY, purpose: reader_effect_and_4_to_6_text_candidates}
    P4: {mode: TEXT_ONLY, purpose: visual_candidate_board_setup, mandatory_after_multi_option_text: true}
    P5: {mode: IMAGE_ONLY, purpose: generate_4_to_6_candidate_images_or_schematics}
    P6: {mode: TEXT_ONLY, purpose: record_candidate_batch_review_and_lock_or_revise_direction}
    P7: {mode: TEXT_ONLY, purpose: final_image_brief}
    P8: {mode: IMAGE_ONLY, purpose: formal_figure_candidate_or_revision_generation}
    P9: {mode: TEXT_ONLY, purpose: review_caption_legend_body_text_handoff}
  cannot_skip_candidate_image_bridge_unless_user_explicitly_requests_text_only: true

candidate_policy:
  text_candidates_default: 6
  text_candidates_min: 4
  text_candidates_max: 6
  image_candidates_default: 6
  image_candidates_min: 4
  image_candidates_max: 6
  if_user_says_generate_without_count: default_to_6_images
  single_image_only_when_explicit: true
  candidate_image_bridge_required_after_multi_option_text: true
  required_bridge_steps:
    - TEXT_ONLY_candidate_board_setup
    - IMAGE_ONLY_candidate_board_generation
    - TEXT_ONLY_candidate_review_and_direction_lock
  rendering_route_for_candidate_images: ChatGPT web Create image through ChatGPT Images 2.0; Codex $imagegen skill first; if unavailable, ChatGPT Images 2.0 API or another approved image-generation API.
  forbidden_generated_visual_outputs: [svg, mermaid, tikz, graphviz, html_css_diagram, canvas_diagram, matplotlib_figure, code_generated_figure]

state_fields:
  - text_candidate_count
  - image_candidate_count
  - candidate_generation_mode
  - candidate_scheme_ids
  - candidate_comparison_focus
  - visual_candidate_board_status
  - visual_board_type
  - visual_board_axis_varied
  - visual_board_fixed_elements
  - candidate_image_batch_id
  - visual_candidate_history
  - selected_visual_candidate
  - visual_candidate_board_skipped_by_user

reference_image_policy:
  optional: true
  multiple_images_allowed: true
  per_image_attribute_preferences: [style, layout, panel_rhythm, information_density, content_detail_level, labels, color_semantics, callout_grammar, negative_reference]

text_image_turn_policy:
  first_reply_mode: STARTUP_PLAN_ONLY_TEXT_ONLY
  no_image_on_first_reply: true
  no_text_and_image_same_turn: true
  text_turn_stops_before_image_generation: true
  image_turn_has_no_prose_or_state: true
  user_must_confirm_after_text_prompt_before_image_generation: true

next_prompt_policy:
  recommended_prompt_prefix: "请使用**<当前skill名称>**，执行，根据当前状态，下一步执行："
  unknown_next_prompt: "请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。"
  after_multi_option_text_first_prompt: "请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：生成 6 张候选图/示意图供我比较选择。"

release_tests:
  - startup_no_image
  - text_candidates_default_6
  - candidate_board_setup_after_text_candidates
  - image_only_candidate_board_generation
  - candidate_review_records_image_batch
  - no_text_image_same_turn
  - rendering_route_chatgpt_create_image_codex_imagegen_first
```
