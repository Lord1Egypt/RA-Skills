# 输出契约

本文件定义 `wiki-intent-scope` 的输出形状。生成聊天摘要、 `scope.md` 、 `scope.json`。

## 输出关系

- 聊天摘要：面向当前对话，给用户快速判断任务界定结果、缺口和下一步。
- `scope.md`：面向人工阅读和确认，保留完整任务界定、口径、风险和待补充问题。
- `scope.json`：面向后续工作流交接，字段稳定，供 `wiki-framework-builder` 等下游节点消费。

## 输出要求

- 需求清晰度和课题可推进性判断应融入聊天摘要、`scope.md` 的“风险与人工确认事项/待补充问题”，以及 `scope.json.handoff_record`。
- 聊天回复只输出聊天摘要，不要把 `scope.md` 或 `scope.json` 的全文贴进聊天框。若用户提供输出路径，将 `scope.md` 和 `scope.json` 写入该路径；若用户未提供输出路径，默认输出到当前项目的 `output/[标准化研究对象]/`，其中 `[标准化研究对象]` 必须使用 `normalize.standardized_name`。聊天摘要末尾说明实际文件路径。
- 客户可见文本使用中文表达确认状态、置信度和风险等级；英文枚举值只用于 `scope.json`。例如：`confirmed` 和 `pending_confirmation` 在聊天摘要和 `scope.md` 中分别写作“已确认”和“待确认”；`low/medium/high` 写作“低/中/高”。
- 未知信息填入 `待确认`或空数组，不要静默假设。

## 聊天摘要

聊天摘要直接回复给用户，不需要输出文件。面向快速阅读确认，按以下顺序组织：

1. 任务界定结论：用 2-4 句话说明标准化研究对象、项目类型/研究意图、建议深度、当前需求是否清晰、课题是否可基于当前假设推进。
2. 关键判断：展示推断的管理问题、确认状态和置信度，以及主意图、辅助意图和更细颗粒度意图。
3. 研究口径：用紧凑列表展示时间、区域、语言/信源、统计基础、币种、价格基础、纳入排除范围、输出用途和结论强度；未知项标记为“待确认”。
4. 风险与护栏：说明预设结论、发布风险、排名/背书风险及处理护栏。
5. 待补充问题：如存在会影响任务界定和后续框架生成的关键缺口，按重要性列出；不要为凑数量而生成低价值问题。

静默忽略客户报价、项目预算、服务费用等商务信息。不要说明这些信息已被移除；不要因此删除研究口径中的价格基础、定价问题或市场价格相关模块。

## Markdown：`scope.md`

建议章节：

1. 任务界定结论
   - 用短段落说明研究对象、研究意图、建议深度、需求清晰度和课题可推进性。
   - 明确哪些判断是当前假设，哪些内容需要用户或人工确认。
2. 客户原始需求摘要
   - 摘要客户原话、发起方/使用场景、隐含目标和对外使用可能性。
3. 标准化研究对象与边界预检查
   - 展示标准化研究对象、规模核算基础、相关术语、边界歧义和纳入/排除提示。
4. 管理问题假设
   - 区分客户原始问题、推断的管理问题、备选管理问题、研究问题和证据问题。
5. 研究意图判断
   - 展示主意图、辅助意图、细化意图和判断依据。
6. 研究口径与待确认项
   - 集中呈现时间、区域、语言/信源、统计基础、币种、价格基础、纳入排除范围、输出用途和结论强度。
7. 框架深度建议
   - 说明建议深度和原因。
8. 风险与人工确认事项
   - 说明预设结论、发布/排名/背书风险、处理护栏，以及需要人工确认的关键判断。
9. 待补充问题
   - 列出最关键问题，优先排序；如果用户暂不补充，也应说明可基于哪些假设继续推进或阶段性结束。

客户可见文本不要暴露 L1-L5 的内部使用规则、内部置信度推理过程或被忽略的商务报价信息。

## JSON：`scope.json`

一级字段含义：

- `client_request`：客户原始表达和可识别的需求背景。
- `normalize`：`wiki-normalize` 的固定输出结果，字段保持原样。
- `scope_caliber`：时间、区域、语言/信源、统计基础、币种、价格基础、纳入排除范围、输出用途和结论强度等研究口径。
- `boundary_precheck`：任务界定阶段识别到的相关术语和边界歧义。
- `problem_transform`：客户问题到管理问题、研究问题、证据问题的转换。
- `research_intent`：研究意图分类，以及用户明确提出的更细颗粒度意图。
- `framework_depth`：框架深度建议。
- `conclusion_risk`：预设结论、对外发布相关的结论风险，以及必须遵守的处理护栏。
- `handoff_record`：记录当前假设、待确认项、建议追问、其他情况备注；在 `notes` 中说明当前需求是否清晰、课题是否可基于当前假设推进。

```json
{
  "client_request": {
    "raw_text": "",
    "recognized_client_or_sponsor": "",
    "recognized_use_context": "",
    "implicit_goal": "",
    "external_use_likelihood": "low/medium/high"
  },
  "normalize": {
    "original_name": "",
    "assigned_level": "L1/L2/L3/L4/L5",
    "standardized_name": "",
    "sizing_metric_baseline": "",
    "reasoning": ""
  },
  "boundary_precheck": {
    "related_terms": [
      {
        "term": "",
        "relation": "parent/child/sibling_confusable/value_chain_stage/substitute_or_competition",
        "note": ""
      }
    ],
    "ambiguity_points": []
  },
  "problem_transform": {
    "client_problem": "",
    "management_problem": "",
    "management_problem_status": "confirmed/pending_confirmation",
    "management_problem_confidence": "low/medium/high",
    "alternative_management_problems": [],
    "research_problem": "",
    "evidence_questions": []
  },
  "research_intent": {
    "primary_type": "",
    "secondary_type": "",
    "confidence": "low/medium/high",
    "explicit_granular_intents": []
  },
  "scope_caliber": {
    "time_range": "",
    "data_cutoff_date": "",
    "forecast_horizon": "",
    "region": "",
    "included_scope": [],
    "excluded_scope": [],
    "language_scope": "",
    "currency": "",
    "price_basis": "",
    "statistical_basis": "",
    "decision_owner": "",
    "conclusion_strength": "",
    "source_constraints": ""
  },
  "framework_depth": {
    "suggested_depth": "简易/常规/深度",
    "reason": ""
  },
  "conclusion_risk": {
    "presupposed_conclusion": "",
    "publication_risk": "low/medium/high",
    "guardrails": ["结论相关处理约束，例如将预设结论改写为可验证问题、确认对外发布场景、谨慎处理排名背书、缺少证据时不生成强主张"]
  },
  "handoff_record": {
    "current_assumptions": [],
    "pending_confirmations": [],
    "recommended_confirmation_questions": [],
    "notes": []
  }
}
```
