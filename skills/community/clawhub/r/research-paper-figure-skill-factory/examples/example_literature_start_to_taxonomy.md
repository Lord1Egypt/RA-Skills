# Example Literature-to-Taxonomy Builder Turn — v1.0.0

Scenario: the user has confirmed start and wants to generate a specialized skill for mechanism-intuition figures. This is a `TEXT_ONLY` example for B2. It plans acquisition; it does not pretend downloads or figure inspection happened unless tools and sources actually permit it.

```markdown
## 当前执行计划

- **当前处于：B2 — 文献目标与语料计划**
- **当前层级：**Skill Builder layer
- **本轮目标：**为“机制解释图 / mechanism-intuition figure”专项 skill 制定最近2年计算机顶会oral论文的合法文献/资料收集计划，准备后续下载、图像检查、taxonomy 构建和专项 skill 生成。
- **计划步骤：**
  1. 确认目标图类和专项 skill 目标 ✅
  2. 制定最近2年计算机顶会oral语料目标、关键词、venue、官方oral证据来源、纳入/排除规则 ⏳ 当前
  3. 根据 host_capabilities 执行开放获取检索/下载，或生成上传清单 ⬜
  4. 检查 figure/caption/metadata 并建立论文卡片 ⬜
  5. 构建该图类 taxonomy，再进入专项 skill 蓝图 ⬜
- **本轮是否调整计划：**无。当前仍处于 Skill Builder layer，不进入具体目标论文制图。

## 文献/资料收集计划

| 项目 | 计划 |
|---|---|
| 目标图类 | 机制解释图 / mechanism-intuition figure |
| 目标专项 skill | `mechanism-intuition-figure-guide` |
| 语料目标 | 收集最近2年计算机顶会oral论文中能代表“算法机制、方法直觉、模块作用、因果链路”的论文图 |
| 首选来源 | arXiv、OpenReview、ACL Anthology、CVF Open Access、PMLR、作者主页、用户上传 PDF |
| 检索关键词 | `mechanism diagram`, `algorithm intuition figure`, `method intuition`, `architecture intuition`, `visual explanation of method` |
| 纳入标准 | 最近2年；计算机顶会；官方oral证据已验证；论文中有可检查的机制/直觉/方法解释图；图能展示模块关系、因果链路或算法步骤 |
| 排除标准 | 只有结果表格/纯曲线图；无法合法访问全文或 figure；只含无关系统截图 |
| 可靠性记录 | 每篇记录 full_figures_viewed / captions_only / metadata_only / mixed |

## 默认推荐

默认推荐先用开放获取来源检索最近2年计算机顶会oral论文，只有官方oral证据已保存的论文才能计入默认corpus；如果当前 host 不能自动下载 PDF，则先输出 DOI/URL 清单并请用户上传 PDF。

## 当前状态与产物

- **builder_time_acquisition：**required=true; owner=research-paper-figure-skill-factory; status=not_started / planning / completed / blocked / user_supplied_evidence; may_defer_to_generated_skill=false; b7_generation_allowed=false
- **B7 gate：**builder_time_acquisition_ok=false; local_corpus_ready_for_extraction=false; extracted_evidence_ready_for_taxonomy=false; evidence_lineage_complete=false; evidence_sufficiency_assessed=false; production_grade_conditions_met=false; allowed_lock_grade=none

- **阶段：**文献目标与语料计划
- **当前层级：**Skill Builder layer
- **当前处于计划B2：**文献目标与语料计划
- **mode：**TEXT_ONLY
- **text_submode：**NORMAL_PLANNING
- **start_confirmed：**true
- **awaiting_user_confirmation：**false
- **host_capabilities：**web_search=unknown; pdf_download=unknown; pdf_open=unknown; pdf_figure_inspection=unknown; file_upload=available; image_generation=unknown; local_file_write=unknown; artifact_packaging=unknown; zip_creation=unknown
- **当前执行计划：**制定 pilot corpus 计划，下一步按合法来源检索/下载或生成上传清单
- **计划调整：**无
- **已定：**目标图类为机制解释图；下一步必须进入合法资料获取/下载或上传清单，不进入具体论文制图
- **待定：**用户是否提供种子论文、目标领域、目标 venue；host 是否支持搜索/下载/打开 PDF
- **默认推荐：**使用开放获取来源建立最近2年计算机顶会oral候选corpus，并验证官方oral证据
- **本轮新增产物：**机制解释图专项 skill 的文献/资料收集计划
- **累计产物：**启动确认、目标图类方向、pilot corpus 计划
- **产物路径/ID：**暂无本地文件；下一步生成 retrieval manifest / acquisition report
- **上一轮 IMAGE_ONLY 产物是否已登记：**not_applicable
- **session状态延续提醒：**默认根据当前 session/history 自动延续状态；用户不需要手动上传或粘贴状态。若宿主无法访问历史、历史被截断或跨会话迁移，再提供最近的 `当前状态与产物` 作为兜底。可问：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

### Skill Builder 状态
- **目标图类：**mechanism-intuition figure
- **目标专项 skill：**mechanism-intuition-figure-guide
- **specialized_skill_first_policy：**true
- **corpus_scope：**year_window=last_2_conference_years; year_window_resolved=[执行时解析]; field_scope=computer_science_top_conferences; venue_set=[CVPR,ICCV,ECCV,NeurIPS,ICML,ICLR,ACL,EMNLP,NAACL,KDD,SIGIR,TheWebConf]; presentation_filter=oral_required; oral_evidence_required=true; fallback_policy=user_approval_required; official_oral_evidence_sources=[]; unverified_oral_items=[]; fallback_items=[]
- **corpus_acquisition_status：**planning
- **文献语料状态：**corpus_plan_drafted
- **acquisition_mode：**not_started
- **retrieval_log：**[]
- **figure_inspection.status：**not_started
- **taxonomy_source_status：**not_started
- **taxonomy 状态：**not_started
- **generated_skill_reusability_scope：**arbitrary_target_papers_of_this_figure_class
- **production_unlocked：**false
- **production_unlocked_by：**none
- **generated_skill.lock_grade：**none / production_grade / limited / pilot / fallback
- **generated_skill.lock_basis：**none / full_taxonomy / user_approved_thin / user_approved_pilot / user_approved_fallback
- **generated_skill.status：**not_started
- **generated_skill.slug：**mechanism-intuition-figure-guide
- **generated_skill.version：**null
- **generated_skill.package_path：**null
- **generated_skill.included_files：**[]
- **generated_skill.known_limitations：**[]
- **generated_skill.test_results：**not_started
- **workflow_shortcut：**shortcut_type=none; skipped_steps=[]; skip_reason=null; fallback_skill_used=null; fallback_taxonomy_used=null

### Figure Production 状态
- **active_specialized_skill：**none
- **目标论文材料状态：**not_provided
- **参考图状态：**none，可选
- **图类型状态：**尚未进入具体论文制图
- **视觉风格状态：**尚未选择
- **视觉决策板状态：**not_started
- **board_step_context：**none

- **产物：**机制解释图专项 skill 的文献/资料收集计划
- **下一轮建议（动作，不写成用户提问句）：**执行 B3，按最近2年计算机顶会oral范围检索/下载资料并保存官方oral证据，或在工具不可用时生成上传/链接清单
- **候选图提醒：**关键视觉选择不要只靠文字定稿；可先要求 4 / 5 / 6 张 imagegen/API 候选图，未指定数量时默认 6 张。
- **渲染规则提醒：**ChatGPT 网页版使用 Create image，通过 ChatGPT Images 2.0 生图；Codex 优先用 `$imagegen` skill，若不可用则用 ChatGPT Images 2.0 API 或其他图像生成 API；该路线产生/导出的 PNG / JPG / JPEG / WebP 等位图结果允许。禁止用 SVG / Mermaid / TikZ / Graphviz / HTML-CSS / canvas / matplotlib / 代码绘图或本地代码导出的图片作为候选图、草稿图、最终图或兜底输出。

## 下一步你可以这样问

提示：正常续问会根据当前 session 记录自动延续状态，不需要手动上传状态；跨会话或历史不可用时再提供最近的 `当前状态与产物`。

1. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：继续第3步，按开放获取来源检索并下载机制解释图相关论文资料。`
2. `请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：继续第3步，但如果不能自动下载PDF，就先给我一个需要上传/提供链接的语料清单。`
3. 不知道下一步时：`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`
```

