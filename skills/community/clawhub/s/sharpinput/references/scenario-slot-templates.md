# Scenario Slot Templates

Scenario templates collect the variables that most affect prompt quality. Ask at most 1-3 high-impact slots at once.

## Slot Priority

- `required`: without this, the upgraded prompt may be misleading or too generic.
- `useful`: improves precision but can be represented as a placeholder.
- `optional`: only ask when the user wants high depth.

## Known Scenarios

### computer_purchase

Use for laptop, desktop, monitor, phone, camera, and hardware purchase prompts.

Required slots:
- budget_range
- primary_use
- must_have_constraints

Useful slots:
- region_or_platform
- portability_or_performance_preference
- existing_devices
- purchase_timing

Ask first:
> 你最不能妥协的是预算、用途，还是便携/性能？

### ai_subscription_choice

Use for ChatGPT Plus, Claude Pro, Gemini, Perplexity, local model, or AI tool subscription comparison.

Required slots:
- main_workflows
- monthly_budget
- privacy_or_data_constraints

Useful slots:
- preferred_language
- coding_or_writing_ratio
- team_or_personal_use

Ask first:
> 你最常用 AI 做什么：写作/学习、代码、研究搜索，还是产品方案？

### prd_srs_generation

Use for PRD, SRS, requirements, product specification, user story, and acceptance criteria prompts.

Required slots:
- product_or_feature_goal
- target_user
- business_or_operational_constraint

Useful slots:
- platform
- scope_boundary
- success_metrics
- known_edge_cases

Ask first:
> 这个 PRD 最重要的是讲清功能、约束边界，还是验收标准？

### ui_review

Use for web/app UI critique, "页面乱", design review, or visual quality improvement prompts.

Required slots:
- target_user
- page_goal
- review_focus

Useful slots:
- screenshot_or_url_available
- brand_constraints
- device_viewport
- benchmark_reference

Ask first:
> 你希望重点看信息层级、视觉风格、转化效率，还是交互可用性？

### frontend_demo_generation

Use for asking AI to build a frontend demo, landing page, dashboard, game, or interactive prototype.

Required slots:
- app_goal
- target_user
- core_interactions

Useful slots:
- tech_stack
- visual_style
- responsive_requirements
- data_source_or_mock_data

Ask first:
> 这个 demo 的第一屏应该让用户完成什么动作？

### learning_exam_prep

Use for learning plans, exams, certifications, courses, or skill development prompts.

Required slots:
- current_level
- target_outcome
- time_budget

Useful slots:
- weak_topics
- preferred_learning_style
- deadline
- practice_materials

Ask first:
> 你现在的水平、目标结果、可投入时间里，哪一个最确定？

### code_debugging

Use only when the user wants a better debugging prompt, not when they ask Codex to debug directly.

Required slots:
- expected_behavior
- actual_behavior
- reproduction_or_error

Useful slots:
- environment
- recent_changes
- constraints
- logs_or_stack_trace

Ask first:
> 现在最关键的证据是错误信息、复现步骤，还是最近改动？

### server_network_troubleshooting

Use for deployment, network, DNS, proxy, server, CI, or runtime issue prompt improvement.

Required slots:
- symptom
- environment
- scope_of_impact

Useful slots:
- timeline
- recent_changes
- logs
- rollback_options

Ask first:
> 这个问题是完全不可用、间歇失败，还是只有某些用户/环境失败？

### product_plan_review

Use for plan critique, roadmap, strategy, launch plan, or project proposal prompts.

Required slots:
- plan_goal
- audience_or_decision_maker
- success_metric

Useful slots:
- constraints
- known_risks
- alternatives
- timeline

Ask first:
> 这个方案最需要被检验的是方向、可执行性，还是资源投入是否值得？

## Fallback Template

When no scenario matches, use generic context fields:

- goal
- audience
- constraints
- output format
- evaluation criteria
- attempted solutions
- unacceptable outcomes

Prefer placeholders over interrogation when the user requests speed.
