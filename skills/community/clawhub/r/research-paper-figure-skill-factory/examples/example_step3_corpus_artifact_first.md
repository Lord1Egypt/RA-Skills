# Example — B3 Corpus Artifact First Acquisition Turn

## 当前执行计划

- **当前处于：B3 — 合法文献发现与下载，并生成本地 corpus artifact**
- **当前层级：Skill Builder layer**
- **本轮目标：**为“方法框架图制图 skill”检索最近2年计算机顶会oral方法论文，合法下载开放 PDF 到本地，并生成 retrieval manifest。
- **计划步骤：**
  1. 目标图类与专项 skill 目标定义 ✅
  2. 文献目标与语料计划 ✅
  3. 合法文献发现与下载 ⏳ 当前
  4. 图像检查与论文卡片 ⬜ 等 local_corpus.ready_for_extraction=true 后执行
- **本轮是否调整计划：**无。

## B3 执行动作

本轮应创建或更新：

```text
/mnt/data/method-framework-figure-guide-corpus/
  papers/
  metadata/retrieval_manifest.csv
  metadata/retrieval_manifest.json
  metadata/acquisition_report.md
  metadata/failed_or_blocked_items.md
  metadata/figure_inspection_queue.md
```

如果 host 能搜索和下载开放 PDF，就实际下载并把本地路径写进 manifest；如果不能下载，就生成同样的 manifest/upload plan，并把 `local_corpus.ready_for_extraction` 保持为 `false`。

## 默认推荐

默认优先检索最近2年计算机顶会中带有官方oral证据的开放获取方法论文；每条记录都必须保存 官方oral证据来源。

## 当前状态与产物

- **阶段：**B3 corpus acquisition
- **当前层级：**Skill Builder layer
- **当前处于计划B3：**合法文献发现与下载，并生成本地 corpus artifact
- **mode：**TEXT_ONLY
- **text_submode：**CORPUS_ACQUISITION
- **start_confirmed：**true
- **host_capabilities：**web_search=available/unknown; pdf_download=available/unknown; pdf_open=unknown; pdf_figure_inspection=unknown; file_upload=available/unknown; image_generation=available/unknown; local_file_write=available/unknown; artifact_packaging=available/unknown; zip_creation=available/unknown
- **本轮新增产物：**本地 corpus artifact、retrieval manifest、acquisition report、blocked items、inspection queue
- **累计产物：**目标图类、corpus scope、B3 acquisition artifacts
- **产物路径/ID：**local_corpus_root=/mnt/data/method-framework-figure-guide-corpus; retrieval_manifest_csv=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.csv
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable
- **session状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若宿主无法访问历史、历史被截断或跨会话迁移，再提供最近的 `当前状态与产物` 作为兜底。可问：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`
- **目标图类：**方法框架图 / Method Framework Figure
- **目标专项 skill：**method-framework-figure-guide
- **corpus_scope：**year_window=last_2_conference_years; year_window_resolved=[2024,2025]; field_scope=computer_science_top_conferences; venue_set=[CVPR,ICCV,ECCV,NeurIPS,ICML,ICLR,ACL,EMNLP,NAACL,KDD,SIGIR,TheWebConf]; presentation_filter=oral_required; oral_evidence_required=true; fallback_policy=user_approval_required
- **specialized_skill_first_policy：**true
- **builder_time_acquisition：**required=true; owner=research-paper-figure-skill-factory; status=searching / downloading / blocked; may_defer_to_generated_skill=false; deferment_exception=none; b7_generation_allowed=false; b7_gate_basis=blocked / null
- **builder_time_acquisition artifacts：**local_corpus_root=/mnt/data/method-framework-figure-guide-corpus; retrieval_manifest_csv=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.csv; retrieval_manifest_json=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.json; evidence_map_json=null; initial_corpus_included_or_referenced_in_generated_skill=false
- **B7 gate：**builder_time_acquisition_ok=false; local_corpus_ready_for_extraction=false; extracted_evidence_ready_for_taxonomy=false; evidence_lineage_complete=false; evidence_sufficiency_assessed=false; production_grade_conditions_met=false; allowed_lock_grade=none
- **corpus_acquisition_status：**searching / downloading / blocked
- **acquisition_mode：**auto_download / user_upload_required / metadata_only / mixed
- **local_corpus：**root_dir=/mnt/data/method-framework-figure-guide-corpus; paper_pdf_dir=/mnt/data/method-framework-figure-guide-corpus/papers; manifest_csv=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.csv; manifest_json=/mnt/data/method-framework-figure-guide-corpus/metadata/retrieval_manifest.json; acquisition_report=/mnt/data/method-framework-figure-guide-corpus/metadata/acquisition_report.md; failed_or_blocked_items=/mnt/data/method-framework-figure-guide-corpus/metadata/failed_or_blocked_items.md; figure_inspection_queue=/mnt/data/method-framework-figure-guide-corpus/metadata/figure_inspection_queue.md
- **local_corpus.ready_for_extraction：**false / true
- **local_corpus.ready_for_taxonomy：**deprecated compatibility only; do not use as active gate
- **retrieval_log：**按 manifest 汇总
- **figure_inspection.status：**not_started
- **taxonomy_source_status：**not_started / corpus_ready
- **production_unlocked：**false
- **generated_skill.status：**not_started
- **workflow_shortcut：**shortcut_type=none; skipped_steps=[]; skip_reason=null
- **产物：**本地 corpus artifact、retrieval manifest、acquisition report、blocked items、inspection queue
- **下一轮建议（动作，不写成用户提问句）：**如果 local corpus 已准备好，进入 B4 检查论文图；否则补充上传 PDF 或调整检索范围。

## 下一步你可以这样问

提示：正常续问会根据当前 session 记录自动延续状态，不需要手动上传状态；跨会话或历史不可用时再提供最近的 `当前状态与产物`。

1. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：继续执行B3，实际检索并下载开放PDF到本地，同时生成retrieval manifest。`
2. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：我上传PDF后继续更新local corpus并进入B4图像检查。`
3. 不知道下一步时：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

