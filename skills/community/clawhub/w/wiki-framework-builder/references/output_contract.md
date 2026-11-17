# Output contract

Produce four outputs.

## 1. Concise chat summary

Include:

- `框架定位`：报告类型、深度等级、章节数量、对外呈现风格
- `研究维度梳理`：用客户可读语言说明本框架采用哪些研究维度，例如产业背景、政策环境、产业链、市场空间、竞争格局、用户场景、商业模式、风险变量、实施路径；不要展示 D1-D8 编号
- `研究口径与待确认项`：必须直接展示在聊天回复中，至少覆盖时间、区域、语言/信源、统计口径、输出用途、结论强度；未知项标记为“待确认”
- `待补充问题`：必须直接展示在聊天回复中，优先列出会影响 Word 框架章节、研究维度和交付模块的关键问题
- `下一步建议`：用户若补充回答，则重新运行本技能；若暂不补充，则基于当前假设生成/确认 Word、Markdown 和 JSON 三件套

Do not include internal dimension codes unless the user explicitly asks.

## 2. Word file: `report_framework.docx`

This is the fixed-format formal output. It must be external-facing and directly usable.

Required structure:

1. Cover/title page
   - report/project title
   - optional client/project entity if known
   - date or version if known

2. Contents / 报告框架
   - first-level sections
   - second-level subsections

3. Framework detail
   - each section includes concise research content
   - include expected output only when useful

No L1-L5, D1-D8, JSON keys, pricing, or internal routing.

Follow `references/external_framework_standard.md`.

## 3. Markdown file: `report_framework.md`

Markdown mirrors the Word framework for quick review/editing:

- report title
- contents/framework
- sections and subsections
- concise descriptions
- expected outputs where useful

No L1-L5, D1-D8, JSON keys, pricing, or internal routing.

## 4. JSON: `report_framework_handoff.json`

Use this shape:

```json
{
  "normalize": {
    "original_name": "",
    "assigned_level": "L1/L2/L3/L4/L5",
    "standardized_name": "",
    "sizing_metric_baseline": "",
    "reasoning": ""
  },

  "research_intent": {
    "primary_type": "",
    "secondary_type": "",
    "confidence": "low/medium/high",
    "explicit_granular_intents": []
  },

  "framework_depth": {
    "suggested_depth": "简易/常规/深度",
    "reason": ""
  },

  "problem_transform": {
    "client_problem": "",
    "management_problem": "",
    "management_problem_status": "confirmed/inferred_current_assumption/pending_confirmation",
    "management_problem_confidence": "low/medium/high",
    "alternative_management_problems": [],
    "research_problem": "",
    "evidence_questions": []
  },

  "scope_caliber": {
    "time_range": "",
    "data_cutoff_date": "",
    "forecast_horizon": "",
    "region": "",
    "language_scope": "",
    "currency": "",
    "price_basis": "",
    "statistical_basis": "",
    "included_scope": [],
    "excluded_scope": []
  },

  "boundary_precheck": {
    "related_terms": [
      { "term": "", "relation": "parent/child/sibling_confusable/value_chain_stage/substitute_or_competition", "note": "" }
    ],
    "ambiguity_points": []
  },

  "report_framework": {
    "framework_type": "",
    "external_title": "",
    "client_visible_dimension_summary": [],
    "chapter_outline": [
      {
        "chapter_id": "",
        "chapter_title": "",
        "external_subsections": [],
        "engineering_dimensions_internal": [],
        "sub_dimensions_internal": [],
        "research_questions": [],
        "evidence_directions": [],
        "output_placeholders": []
      }
    ]
  },

  "definition_research_context": {
    "definition_focus_questions_placeholder": [],
    "must_preserve_boundaries": [],
    "do_not_expand_beyond": [],
    "notes_for_industry_definition_research": ""
  },

  "recommended_confirmation_questions": [],

  "next_step": {
    "rerun_skill2_if_user_answers": true,
    "proceed_with_current_framework_if_no_answer": true,
    "handoff_note_for_next_research_stage": ""
  },
}
```
