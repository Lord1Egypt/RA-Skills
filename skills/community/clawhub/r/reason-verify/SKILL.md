---
name: reason-verify
type: synthesized
agent_created: true
description: 可靠推理与自验证：对推理结果做命题抽取、矛盾检测、覆盖度评估与事实锚定校验，输出可验证的结论，纯Python零依赖。当需要"验证推理是否正确""自查答案""检测逻辑矛盾""reason-verify"时使用。
summary: 由 lifelong-skill-synthesis 自主合成的技能。需求：构建[reason-verify]专门技能：可靠推理与自验证任务的自验证可靠性与工具链准确性
visibility: public
read_when:
  - 出现与「通用处理」相关的任务
---

# reason-verify（自主合成技能）

## 需求来源
构建[reason-verify]专门技能：可靠推理与自验证任务的自验证可靠性与工具链准确性

## 输入 / 输出
- 输入：用户提供的原始材料/请求
- 输出：满足需求的结构化结果

## 复用构件（跨域检索得到）
- **meta-gen-针对维度-定向补强-构建专门技能-提升该任务的自验证可靠性与工具链准-5160ee**：---
- **reason-verify**：---
- **math-reasoner**：---
- **gen-针对维度-定向补强-构建专门技能-提升该任务的自验证可靠性与工具链准-5160ee**：---

## 工作流
感知 → 规划(long-horizon-planner) → 执行(capability) → 自验证(reason-verify) → 反思

## 使用
```
python scripts/run.py --input "..."     # 正常执行
python scripts/run.py --smoke           # 自测
```
