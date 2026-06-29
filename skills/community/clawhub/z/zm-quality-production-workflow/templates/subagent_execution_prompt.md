# 可复制给 SubAgent 的执行提示词

你正在执行 `zm-quality-production-workflow` Skill。

## 任务

请基于用户需求，按“标准化输入 → 依赖检查 → 样章/样页 → 专业生产 → 自检 → 双 Agent 审核 → 返工 → main 终审 → 交付包”的流程完成正式产出。

## 你必须先做

1. 读取 `SKILL.md`。
2. 读取 `workflows/full-quality-production-workflow.md`。
3. 读取 `workflows/task-type-routing.md`。
4. 根据任务类型读取对应 checklist。
5. 先创建或填写：
   - `standard_input_card.md`
   - `dependency_gap_list.md`
   - `production_plan.md`

## 最小必填信息

如果以下任一项缺失，不得进入全量生产：

- 任务类型；
- 目标用户；
- 使用场景；
- 核心目标；
- 最终输出清单；
- 必需素材状态；
- 样章/样页门禁；
- 审核标准；
- BLOCKED 条件。

## 特别规则

- 正式视觉/生图不得由 main 直接执行，交 media-director。
- 正式正文不得由 main 直接写，交 writer-pro。
- 正式代码不得由 main 直接写，交 code-engineer。
- 缺真实 Logo、二维码、主角图、数据来源、真实案例时，不得伪造。
- 漫画/手册必须先做 P1 样章，P1 未确认不得扩全套。
- 双 Agent 审核未通过，不得宣称完成。

## 输出要求

请输出：

1. 标准化输入卡路径；
2. 依赖缺口清单路径；
3. 生产计划路径；
4. 样章/样页计划；
5. 需要哪些 SubAgent；
6. 当前状态：READY / PARTIAL_READY / BLOCKED；
7. 下一步动作。
