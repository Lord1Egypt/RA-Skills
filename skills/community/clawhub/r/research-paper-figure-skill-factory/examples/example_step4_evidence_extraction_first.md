# Example — B4 Evidence Extraction First Turn — completed extraction example v1.0.0

## 当前执行计划

- **当前处于：B4 — 从本地 corpus 提取结构化证据**
- **当前层级：Skill Builder layer**
- **本轮目标：**从 B3 下载/上传的论文 corpus 中提取 paper cards、figure inventory、caption inventory、panel notes、visual observations 和 evidence map，供 B5 taxonomy 使用。
- **计划步骤：**
  1. 目标图类与专项 skill 目标定义 ✅
  2. 文献目标与语料计划 ✅
  3. 合法文献发现与下载 ✅
  4. 结构化证据提取 ✅ 已完成
  5. 基于 evidence map 构建 taxonomy ⏳ 下一步
  6. 专项制图 skill 蓝图 ⬜ 待 taxonomy 完成后执行
- **本轮是否调整计划：**无。

## B4 已完成的本地产物

```text
/mnt/data/method-framework-figure-guide-corpus/extracted/
  paper_cards.csv
  paper_cards.json
  figure_inventory.csv
  figure_inventory.json
  caption_inventory.csv
  panel_structure_notes.md
  visual_pattern_observations.md
  evidence_map.json
  extraction_report.md
```

## 默认推荐

下一步进入 **B5：基于 evidence map 构建方法框架图 taxonomy**。B5 必须把每条 taxonomy claim 绑定到 evidence_map 中的 paper / figure / caption / panel 来源；无法绑定的规则必须进入 `generic_fallback_claims`，不能作为 class-specific taxonomy 的核心证据。

## 当前状态与产物

- **阶段：**B4 evidence extraction completed
- **当前层级：**Skill Builder layer
- **当前处于计划B4：**从本地 corpus 提取结构化证据
- **mode：**TEXT_ONLY
- **text_submode：**EVIDENCE_EXTRACTION_COMPLETED
- **start_confirmed：**true
- **awaiting_user_confirmation：**false
- **host_capabilities：**web_search=available; pdf_download=available; pdf_open=available; pdf_figure_inspection=available; file_upload=available; image_generation=available
- **当前执行计划：**B4 已生成结构化 evidence；下一步进入 B5 taxonomy construction
- **计划调整：**无
- **已定：**B5 必须基于 `evidence_map.json`、figure inventory、caption inventory 和 paper cards
- **待定：**taxonomy claims、evidence sufficiency 等级、generic fallback claims
- **默认推荐：**进入 B5，先构建方法框架图 taxonomy draft，再做 evidence sufficiency 检查
- **本轮新增产物：**paper cards、figure inventory、caption inventory、panel notes、visual observations、evidence map、extraction report
- **累计产物：**B3 local corpus、B4 extracted evidence artifacts
- **产物路径/ID：**evidence_map_json=/mnt/data/method-framework-figure-guide-corpus/extracted/evidence_map.json
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable
- **session状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若宿主无法访问历史、历史被截断或跨会话迁移，再提供最近的 `当前状态与产物` 作为兜底。可问：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

### Skill Builder 状态
- **目标图类：**方法框架图 / Method Framework Figure
- **目标专项 skill：**method-framework-figure-guide
- **specialized_skill_first_policy：**true
- **corpus_acquisition_status：**downloaded
- **文献语料状态：**local corpus ready and extracted
- **acquisition_mode：**auto_download / user_upload_required / mixed
- **local_corpus：**root_dir=/mnt/data/method-framework-figure-guide-corpus; paper_pdf_dir=/mnt/data/method-framework-figure-guide-corpus/papers; manifest_csv=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.csv; manifest_json=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.json; acquisition_report=/mnt/data/method-framework-figure-guide-corpus/metadata/acquisition_report.md; failed_or_blocked_items=/mnt/data/method-framework-figure-guide-corpus/metadata/failed_or_blocked_items.md; figure_inspection_queue=/mnt/data/method-framework-figure-guide-corpus/metadata/figure_inspection_queue.md
- **local_corpus counts：**downloaded_pdf_count=12; user_uploaded_pdf_count=0; metadata_only_count=2; failed_count=1; oral_or_spotlight_count=8; verified_oral_count=8; unverified_oral_count=0; fallback_non_oral_count=0; official_oral_evidence_count=8
- **local_corpus.ready_for_extraction：**true; basis=downloaded_pdfs / mixed
- **local_corpus.ready_for_taxonomy：**deprecated compatibility only; do not use as active gate
- **extracted_evidence.status：**extracted
- **extracted_evidence paths：**extracted_dir=/mnt/data/method-framework-figure-guide-corpus/extracted; paper_cards_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/paper_cards.csv; figure_inventory_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/figure_inventory.csv; caption_inventory_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/caption_inventory.csv; evidence_map_json=/mnt/data/method-framework-figure-guide-corpus/extracted/evidence_map.json; extraction_report=/mnt/data/method-framework-figure-guide-corpus/extracted/extraction_report.md
- **extracted_evidence counts：**paper_count=12; figure_count=24; caption_count=24; full_figure_inspection_count=20; caption_only_count=4; metadata_only_count=2
- **extracted_evidence.ready_for_taxonomy：**true; basis=full_figures / mixed
- **evidence_lineage：**taxonomy_claims_with_sources_count=0; unsupported_claims=[]; generic_fallback_claims=[]; evidence_lineage_complete=false
- **evidence_sufficiency：**level=not_assessed; paper_count_threshold_met=true; figure_count_threshold_met=true; core_claims_supported=false; unsupported_core_claims=[]
- **retrieval_log：**manifest records DOI/URL/source/local_path/status for all included and blocked items
- **figure_inspection.status：**mixed
- **taxonomy_source_status：**extracted_evidence_ready
- **taxonomy 状态：**not_started
- **generated_skill_reusability_scope：**arbitrary_target_papers_of_this_figure_class
- **production_unlocked：**false
- **production_unlocked_by：**none
- **generated_skill.lock_grade：**none / production_grade / limited / pilot / fallback
- **generated_skill.lock_basis：**none / full_taxonomy / user_approved_thin / user_approved_pilot / user_approved_fallback
- **generated_skill.status：**not_started
- **generated_skill.slug：**method-framework-figure-guide
- **generated_skill.version：**null
- **generated_skill.package_path：**null
- **generated_skill.included_files：**[]
- **generated_skill.known_limitations：**[]
- **generated_skill.test_results：**startup_gate/state_footer/default_recommendation/visual_board/rendering_boundary/next_question_help=not_started
- **workflow_shortcut：**shortcut_type=none; skipped_steps=[]; skip_reason=null; fallback_skill_used=null; fallback_taxonomy_used=null

### Figure Production 状态
- **active_specialized_skill：**none
- **目标论文材料状态：**not_provided
- **参考图状态：**none
- **图类型状态：**method-framework target class only; no target-paper routing yet
- **视觉风格状态：**not_started
- **视觉决策板状态：**not_started
- **board_step_context：**none

- **产物：**B4 extracted artifacts: paper cards, figure inventory, caption inventory, panel notes, visual observations, evidence map, extraction report
- **下一轮建议（动作，不写成用户提问句）：**进入 B5，用 evidence_map 构建 taxonomy，并检查每条 claim 的证据绑定和 sufficiency 等级
- **候选图提醒：**关键视觉选择不要只靠文字定稿；可先要求 4 / 5 / 6 张 imagegen/API 候选图，未指定数量时默认 6 张。
- **渲染规则提醒：**ChatGPT 网页版使用 Create image，通过 ChatGPT Images 2.0 生图；Codex 优先用 `$imagegen` skill，若不可用则用 ChatGPT Images 2.0 API 或其他图像生成 API；该路线产生/导出的 PNG / JPG / JPEG / WebP 等位图结果允许。禁止用 SVG / Mermaid / TikZ / Graphviz / HTML-CSS / canvas / matplotlib / 代码绘图或本地代码导出的图片作为候选图、草稿图、最终图或兜底输出。

## 下一步你可以这样问

提示：正常续问会根据当前 session 记录自动延续状态，不需要手动上传状态；跨会话或历史不可用时再提供最近的 `当前状态与产物`。

1. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：继续第5步，基于evidence_map构建方法框架图taxonomy，并检查evidence sufficiency。`
2. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：先检查B4 evidence_map中哪些figure/caption证据最适合支撑taxonomy。`
3. 不知道下一步时：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

