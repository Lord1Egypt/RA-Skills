# SharpInput Intent Taxonomy

Intent describes what the eventual AI answer should do. It is separate from scenario.

## Canonical 14 Intents

| Intent | When The User Wants | Compiler Cue |
|---|---|---|
| 理解 | explain a concept, mechanism, or idea | ask for layered explanation and examples |
| 决策 | choose among options or make a recommendation | force criteria, trade-offs, and final recommendation |
| 生成 | create text, plan, code prompt, PRD, message, or artifact | specify audience, format, constraints, acceptance criteria |
| 分析 | inspect an object, page, plan, argument, or result | require evidence, dimensions, and prioritized findings |
| 探索 | open-ended ideation or option discovery | ask for divergent options before converging |
| 诊断 | find root cause of a problem | require symptoms, constraints, hypotheses, and next checks |
| 说服 | convince a stakeholder | require target stance, objections, and persuasion path |
| 验证 | test whether something is true, good, feasible, or risky | require criteria, counterexamples, and pass/fail signals |
| 规划 | design steps, roadmap, implementation plan, or schedule | require milestones, dependencies, risks, and checkpoints |
| 学习 | learn a topic, prepare an exam, build a practice path | require level, timeline, weak spots, practice loop |
| 优化 | improve an existing artifact or process | require before/after criteria and constraints |
| 对比 | compare tools, options, models, products, or approaches | require decision criteria and weighted comparison |
| 梳理 | organize messy thoughts, notes, requirements, or context | require structure, hierarchy, and missing pieces |
| 求助 | ask for help with an unclear problem | require current state, desired state, blockers, and evidence |

## Confidence Rules

- If one intent clearly dominates, set `primary_intent` and optionally `secondary_intent`.
- If two intents are tightly coupled, keep both. Example: "帮我判断这个方案并优化提问" = 验证 + 优化.
- If confidence is below 0.65, ask the user to choose between the top two interpretations.
- Do not infer scenario from intent alone. "决策" can mean laptop purchase, AI subscription, hiring, architecture, or career choice.

## Intent Drift Checks

Before final output, verify:

1. The upgraded prompt still asks for the same underlying help.
2. Added constraints do not force a conclusion the user did not ask for.
3. Pressure requirements improve answer quality without turning the request into debate.
