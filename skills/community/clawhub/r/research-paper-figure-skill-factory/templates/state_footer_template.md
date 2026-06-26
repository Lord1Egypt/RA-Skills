# State Footer Template

Every `TEXT_ONLY` reply must include this footer immediately before `下一步你可以这样问`.

```markdown
## 当前状态与产物

- **阶段：**Startup / Skill Builder / Figure Production
- **当前步骤：**S0 / B1-B9 / P1-P9 中的当前编号
- **当前回复模式：**TEXT_ONLY
- **全部步骤与当前位置：**S0(STARTUP_PLAN_ONLY/TEXT_ONLY) -> B1(TEXT_ONLY) -> B2(TEXT_ONLY) -> B3(TEXT_ONLY) -> B4(TEXT_ONLY) -> B5(TEXT_ONLY) -> B6(TEXT_ONLY) -> B7(TEXT_ONLY) -> B8(TEXT_ONLY) -> B9(TEXT_ONLY) -> P1(TEXT_ONLY) -> P2(TEXT_ONLY) -> P3(TEXT_ONLY) -> P4(TEXT_ONLY candidate-board setup) -> P5(IMAGE_ONLY candidate-board generation) -> P6(TEXT_ONLY candidate review/selection) -> P7(TEXT_ONLY final image brief) -> P8(IMAGE_ONLY formal generation) -> P9(TEXT_ONLY review/final text)；当前=...
- **当前执行计划：**...
- **默认推荐：**...
- **本轮新增产物：**...
- **累计产物：**...
- **产物路径/ID：**...
- **待产物：**...
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable / recorded / pending_record
- **session 状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若历史不可用、被截断或跨会话迁移，再提供最近的 `当前状态与产物`。

### Skill Builder 状态
- **目标图类：**...
- **目标专项 skill：**slug / display name / not_started
- **builder_time_acquisition：**required=true; status=not_started / planning / searching / downloading / extracting / completed / blocked / user_supplied_evidence
- **corpus coverage：**processing_scope=all_accessible_relevant_pdfs / chunked_resumable / user_approved_pilot_sample / resource_limited_sample / metadata_or_caption_fallback; candidate_pdf_count=...; accessible_pdf_count=...; processed_pdf_count=...; skipped_pdf_count=...; skipped_reasons=[]
- **extracted_evidence：**status=not_started / extracting / extracted / partial / caption_only / metadata_only / blocked; ready_for_taxonomy=false / true
- **evidence_sufficiency：**level=not_assessed / full_taxonomy / thin_taxonomy / pilot_taxonomy / fallback_taxonomy
- **generated_skill：**status=not_started / generated / tested / patched / locked; slug=...; version=...; package_path=...; lock_grade=none / production_grade / limited / pilot / fallback

### Figure Production 状态
- **active_specialized_skill：**slug / version / source / limitations
- **目标论文材料状态：**not_provided / partial / sufficient
- **样例/参考图状态：**none / requested / provided / analyzed；如果已提供，列出每张图要参考的属性
- **text_candidate_count：**0 / 4 / 5 / 6
- **image_candidate_count：**0 / 4 / 5 / 6
- **candidate_generation_mode：**none / multi_scheme_multi_image / single_scheme_multi_image
- **candidate_scheme_ids：**[]
- **candidate_comparison_focus：**...
- **visual_candidate_board_status：**not_started / setup_ready / confirmed / generated / reviewed / skipped_by_user
- **visual_board_type：**subtype / scheme / layout / style / metaphor / density / prompt / final_candidate
- **visual_board_axis_varied：**...
- **visual_board_fixed_elements：**[]
- **candidate_image_batch_id：**...
- **selected_visual_candidate：**...
- **visual_candidate_board_skipped_by_user：**false / true
- **多方案下一步提醒：**如果本轮给了多个方案/布局/风格/prompt，`下一步你可以这样问` 的第一条必须要求生成/展示多张候选图或示意图来选择，通常 6 张；不要只建议从文字方案里定稿。
- **渲染规则提醒：**ChatGPT 网页版使用 Create image / ChatGPT Images 2.0；Codex 优先 `$imagegen`，不可用时使用 ChatGPT Images 2.0 API 或其他批准的图像 API；禁止 SVG/Mermaid/TikZ/Graphviz/HTML-CSS/canvas/matplotlib/code-rendered visual fallback。
```

When this footer appears, the response is text-only and must stop before image generation.
