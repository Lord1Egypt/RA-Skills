# Session State Schema

Version: 1.0.1

Use this schema conceptually. The state does not need to be emitted as JSON, but every text reply must preserve these fields in the required current-status/current-output footer.

```yaml
skill: research-paper-figure-skill-factory
version: 1.0.1
mode: TEXT_ONLY | IMAGE_ONLY
current_step:
  code: S0 # S0 | B1-B9 | P1-P9
  layer: startup | skill_builder | figure_production
  response_mode: TEXT_ONLY | IMAGE_ONLY | STARTUP_PLAN_ONLY_TEXT_ONLY
all_steps_and_current_position: ""

builder_layer:
  target_figure_class: null
  target_skill_slug: null
  builder_time_acquisition:
    required: true
    status: not_started | planning | searching | downloading | extracting | completed | blocked | user_supplied_evidence
    local_corpus_root: null
    retrieval_manifest_json: null
    evidence_map_json: null
  local_corpus:
    processing_scope: all_accessible_relevant_pdfs | chunked_resumable | user_approved_pilot_sample | resource_limited_sample | metadata_or_caption_fallback
    candidate_pdf_count: 0
    accessible_pdf_count: 0
    processed_pdf_count: 0
    skipped_pdf_count: 0
    skipped_reasons: []
    ready_for_extraction: false
  extracted_evidence:
    status: not_started | extracting | extracted | partial | caption_only | metadata_only | blocked
    ready_for_taxonomy: false
    evidence_map_json: null
    multi_label_records_count: 0
  evidence_sufficiency:
    level: not_assessed | full_taxonomy | thin_taxonomy | pilot_taxonomy | fallback_taxonomy
  generated_skill:
    status: not_started | generated | tested | patched | locked
    slug: null
    version: null
    package_path: null
    lock_grade: none | production_grade | limited | pilot | fallback
    known_limitations: []
    test_results:
      startup_gate: not_started | passed | failed
      state_footer: not_started | passed | failed
      candidate_image_bridge: not_started | passed | failed
      rendering_boundary: not_started | passed | failed

production_layer:
  active_specialized_skill:
    slug: null
    version: null
    limitations: []
  material_status: not_provided | partial | sufficient
  sample_reference_images:
    status: none | requested | provided | analyzed
    images: []
  text_candidate_count: 0
  image_candidate_count: 0
  candidate_generation_mode: none | multi_scheme_multi_image | single_scheme_multi_image
  candidate_scheme_ids: []
  candidate_comparison_focus: null
  visual_candidate_board_status: not_started | setup_ready | confirmed | generated | reviewed | skipped_by_user
  visual_board_type: subtype | scheme | layout | style | metaphor | density | prompt | final_candidate | null
  visual_board_axis_varied: null
  visual_board_fixed_elements: []
  candidate_image_batch_id: null
  visual_candidate_history: []
  selected_visual_candidate: null
  visual_candidate_board_skipped_by_user: false

deliverables:
  current_turn_outputs: []
  cumulative_outputs: []
  output_paths_or_ids: []
  pending_outputs: []
  previous_image_only_outputs_recorded: not_applicable | recorded | pending_record

navigation:
  recommended_prompt_prefix: "Use the exact Chinese prefix from SKILL.md."
  unknown_next_prompt: "Use the exact Chinese fallback prompt from SKILL.md."
  after_multi_option_text_first_prompt: "Ask to generate/display 6 candidate images or schematic candidates."
  state_source_default: active_session_history
```
