# Example — B5 Evidence-Backed Taxonomy Turn v1.0.0

## 当前执行计划

- **当前处于：B5 — 基于 evidence map 构建该图类 taxonomy**
- **当前层级：Skill Builder layer**
- **本轮目标：**只基于 B4 提取出的结构化证据，构建方法框架图 taxonomy、pattern library、anti-patterns 和 prompt/review 规则，并评估 evidence sufficiency。
- **计划步骤：**
  3. 本地 corpus artifact ✅
  4. 结构化证据提取 ✅
  5. Evidence-backed taxonomy ⏳ 当前
  6. 专项制图 skill 蓝图 ⬜ 待 taxonomy 完成后执行
  7. 生成专项制图 skill ⬜ 待执行
- **本轮是否调整计划：**无。

## B5 生成原则

每条 taxonomy claim 必须包含：claim、supporting papers、supporting figures、supporting captions / panels、observed pattern、confidence、limitation。无法绑定 evidence_map 的规则必须进入 `generic_fallback_claims`，不能作为 class-specific taxonomy 的核心证据。

## v1.14 full-taxonomy 判定

只有当以下条件同时成立，才能标记为 `full_taxonomy`：

- `paper_count_threshold_met=true`
- `figure_count_threshold_met=true`
- `core_claims_supported=true`
- `unsupported_core_claims=[]`

任何一项不成立，都必须降级为 `thin_taxonomy`、`pilot_taxonomy` 或 `fallback_taxonomy`，并写入 limitations。

## 默认推荐

优先生成 **evidence-backed 方法框架图 taxonomy draft**，但在锁定为 full taxonomy 前先运行 sufficiency check。若核心 claims 中有任何 unsupported 项，默认推荐先补充 corpus 或降级为 thin taxonomy，而不是直接生成可锁定的专项 skill。

## 当前状态与产物

- **阶段：**B5 taxonomy construction
- **当前层级：**Skill Builder layer
- **当前处于计划B5：**基于 evidence map 构建 taxonomy
- **mode：**TEXT_ONLY
- **text_submode：**EVIDENCE_BACKED_TAXONOMY
- **start_confirmed：**true
- **awaiting_user_confirmation：**false
- **host_capabilities：**web_search=available; pdf_download=available; pdf_open=available; pdf_figure_inspection=available; file_upload=available; image_generation=available
- **当前执行计划：**已基于 B4 evidence map 生成 taxonomy draft，并正在评估 evidence sufficiency
- **计划调整：**无
- **已定：**taxonomy claims must cite paper/figure/caption/panel evidence or be labeled fallback
- **待定：**是否达到 full_taxonomy；是否需要补充 corpus；是否进入 B6 skill blueprint
- **默认推荐：**若 sufficiency 达到 full_taxonomy，则进入 B6；否则先补证据或明确 thin taxonomy 限制
- **本轮新增产物：**evidence-backed taxonomy draft、pattern library、evidence sufficiency assessment
- **累计产物：**local corpus、extracted evidence、taxonomy draft、evidence sufficiency notes
- **产物路径/ID：**evidence_map_json=/mnt/data/method-framework-figure-guide-corpus/extracted/evidence_map.json; taxonomy_draft=method-framework-taxonomy-draft
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable
- **session状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若宿主无法访问历史、历史被截断或跨会话迁移，再提供最近的 `当前状态与产物` 作为兜底。可问：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

### Skill Builder 状态
- **目标图类：**方法框架图 / Method Framework Figure
- **目标专项 skill：**method-framework-figure-guide
- **specialized_skill_first_policy：**true
- **corpus_acquisition_status：**downloaded
- **文献语料状态：**local corpus extracted and taxonomy draft created
- **acquisition_mode：**mixed
- **local_corpus：**root_dir=/mnt/data/method-framework-figure-guide-corpus; paper_pdf_dir=/mnt/data/method-framework-figure-guide-corpus/papers; manifest_csv=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.csv; manifest_json=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.json; acquisition_report=/mnt/data/method-framework-figure-guide-corpus/metadata/acquisition_report.md; failed_or_blocked_items=/mnt/data/method-framework-figure-guide-corpus/metadata/failed_or_blocked_items.md; figure_inspection_queue=/mnt/data/method-framework-figure-guide-corpus/metadata/figure_inspection_queue.md
- **local_corpus counts：**downloaded_pdf_count=12; user_uploaded_pdf_count=0; metadata_only_count=2; failed_count=1; oral_or_spotlight_count=8; verified_oral_count=8; unverified_oral_count=0; fallback_non_oral_count=0; official_oral_evidence_count=8
- **local_corpus.ready_for_extraction：**true; basis=mixed
- **local_corpus.ready_for_taxonomy：**deprecated compatibility only; do not use as active gate
- **extracted_evidence.status：**extracted
- **extracted_evidence paths：**extracted_dir=/mnt/data/method-framework-figure-guide-corpus/extracted; paper_cards_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/paper_cards.csv; figure_inventory_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/figure_inventory.csv; caption_inventory_csv=/mnt/data/method-framework-figure-guide-corpus/extracted/caption_inventory.csv; evidence_map_json=/mnt/data/method-framework-figure-guide-corpus/extracted/evidence_map.json; extraction_report=/mnt/data/method-framework-figure-guide-corpus/extracted/extraction_report.md
- **extracted_evidence counts：**paper_count=12; figure_count=24; caption_count=24; full_figure_inspection_count=20; caption_only_count=4; metadata_only_count=2
- **extracted_evidence.ready_for_taxonomy：**true; basis=mixed
- **evidence_lineage：**taxonomy_claims_with_sources_count=18; unsupported_claims=[]; generic_fallback_claims=[]; evidence_lineage_complete=true
- **evidence_sufficiency：**level=full_taxonomy; paper_count_threshold_met=true; figure_count_threshold_met=true; core_claims_supported=true; unsupported_core_claims=[]
- **retrieval_log：**manifest records DOI/URL/source/local_path/status for all included and blocked items
- **figure_inspection.status：**mixed
- **taxonomy_source_status：**built
- **taxonomy 状态：**taxonomy_drafted
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

- **产物：**evidence-backed taxonomy draft and pattern library; evidence sufficiency assessment
- **下一轮建议（动作，不写成用户提问句）：**若用户确认 taxonomy，则进入 B6 专项制图 skill 蓝图；若不确认，则补充 evidence 或降级 taxonomy label
- **候选图提醒：**关键视觉选择不要只靠文字定稿；可先要求 4 / 5 / 6 张 imagegen/API 候选图，未指定数量时默认 6 张。
- **渲染规则提醒：**ChatGPT 网页版使用 Create image，通过 ChatGPT Images 2.0 生图；Codex 优先用 `$imagegen` skill，若不可用则用 ChatGPT Images 2.0 API 或其他图像生成 API；该路线产生/导出的 PNG / JPG / JPEG / WebP 等位图结果允许。禁止用 SVG / Mermaid / TikZ / Graphviz / HTML-CSS / canvas / matplotlib / 代码绘图或本地代码导出的图片作为候选图、草稿图、最终图或兜底输出。

## 下一步你可以这样问

提示：正常续问会根据当前 session 记录自动延续状态，不需要手动上传状态；跨会话或历史不可用时再提供最近的 `当前状态与产物`。

1. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：继续第6步，基于这个evidence-backed taxonomy生成方法框架图制图skill蓝图。`
2. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：先检查taxonomy中哪些claim缺少论文figure证据。`
3. 不知道下一步时：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

