# Quest Chain Decomposer / 任务链分解器

Break a fuzzy, high-friction goal into a sequenced quest chain with prerequisite nodes, parallel branches, waiting points, Definition of Done, and the first three actions.

## Tags
productivity, task-management, gamification, project-planning

## Usage Scenarios

### Scenario 1: 任务太大不知道从哪下手
**User Input:** "老板让我做一个完整的年度营销方案，我一看就觉得好难好焦虑，拖了一个月了还没开始。怎么把这任务拆成能马上做的事？"

**Expected Output:** 大任务拆解法——第一步：把最终成果拆成3-5个模块（年度营销方案=市场分析、竞品分析、目标用户、策略规划、执行计划、预算评估）；第二步：每个模块再拆成当天可完成的"最小行动"（如市场分析=打开百度/知乎查3篇行业报告+整理5个核心结论+写300字摘要，一天内必须完成这个最小行动）；第三步：每天只做1-2个最小行动，做完就下班不贪多；第四步：障碍识别（如果某个步骤卡住超过2天=拆得更小或换顺序做后面的）；第五步：给自己一个"日终结硬"——每天下班前发一条微信消息给自己：今天完成了什么+明天要做的第一件事。关键：最小行动是要在30分钟内能完成且做完后有明显进步感。

### Scenario 2: Decompose 'Launch a podcast' into a quest chain
**User Input:** "Decompose 'Launch a podcast' into a quest chain with dependencies and effort estimates."

**Expected Output:** Quest tree: Main Quest → (A) Define niche & format [3h], (B) Procure equipment [4h] → (C) Record pilot [2h, depends on A+B], (D) Edit & mix [4h, depends on C], (E) Submit to directories [1h, depends on D]. Parallel paths marked. Total: 14h.

### Scenario 3: Health check on a stale quest chain
**User Input:** "The 'Build a course' quest chain is stale (50% done, no activity in 3 weeks). Should I restart or pivot?"

**Expected Output:** Chain health assessment: 3 of 6 quests completed. The stuck quest ("Record lessons") is blocked by equipment not yet purchased. Suggests either purchasing equipment or rewriting the quest to use existing phone camera as a temporary path.
