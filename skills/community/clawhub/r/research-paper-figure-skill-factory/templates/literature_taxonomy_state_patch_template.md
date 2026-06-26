# Literature / Taxonomy State Patch Template — v1.16

Use this when literature/taxonomy work is executed, skipped, or partially executed.

```markdown
### Skill Builder 状态补充
- acquisition_mode：not_started / auto_download / user_upload_required / metadata_only / mixed
- retrieval_log：DOI/URL/source/status/inspection-level summary
- figure_inspection.status：not_started / full_figures_viewed / captions_only / metadata_only / mixed
- taxonomy_build_status：not_started / corpus_planned / papers_acquired / triaged / taxonomy_drafted / skill_blueprint_drafted / skill_generated / skill_tested / skill_locked
- taxonomy_source_limitations：...
- workflow_shortcut：
  - skipped_steps：[]
  - shortcut_type：none / partial_builder_shortcut / full_production_fast_track
  - skip_reason：user_has_sufficient_materials / user_requested_fast_track / prior_skill_available / tool_unavailable / other
  - fallback_skill_used：built_in_general_figure_skill / prior_generated_skill / user_provided_skill / newly_generated_skill / null
  - fallback_taxonomy_used：built_in_general_taxonomy / prior_session_taxonomy / user_provided_taxonomy / newly_built_taxonomy / null
```

Guidance:

- Record skipped B2-B5 when the user has an existing corpus/taxonomy but still wants to generate a specialized skill.
- Record skipped B1-B9 when the user bypasses Skill Builder entirely and wants concrete figure production immediately.
- Never imply that a generated specialized skill exists unless B7 has actually produced one or the user provided one.

- host_capabilities：web_search / pdf_download / pdf_open / pdf_figure_inspection / file_upload / image_generation = available / unavailable / unknown
