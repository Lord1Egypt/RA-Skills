# zh-project-proposal-writing

中文项目申请书写作与交付 Skill。主文件为 `SKILL.md`，参考资料在 `references/`，少样例在 `examples/`。

本版本把 Skill 从“写作辅助”升级为“可交付项目书生产系统”，可用于生成整本项目书 Word 文档，文档内包含正文草稿、约束响应矩阵、事实台账、附件/预算/合规清单、红队评审意见和最终核验清单。

## 安装

```bash
npx skills add ECNU-ICALK/zh-project-proposal-writing-skill
```

## 结构

- `SKILL.md`：触发条件、工作模式、来源分级、可交付工作流、输出契约和质量闸门。
- `AGENTS.md`：维护本 Skill 时的 agent 指令。
- `references/deliverable_proposal_workflow.md`：整本项目书可交付生产流程、版本推进、矩阵模板、红队问题库和交付包格式。
- `references/expert_wisdom_synthesis.md`：无姓名、无 URL 的可靠来源经验归类、主题共识和可执行写作动作。
- `references/funder_rules.md`：不同资助方/项目类型的写作口径。
- `references/title_abstract_story.md`：标题、摘要、项目简介和故事线写作规则。
- `references/module_writing_guide.md`：立项依据、目标、内容、路线、创新、可行性等章节写作手册。
- `references/templates_checklists.md`：诊断、模拟评审、自检、提示词和清单模板。
- `references/knowledge_boundaries.md`：公开资料、用户材料、不可编造事实和核验边界。
- `references/writing_logic_consensus.md`：项目书通用写作逻辑与评审视角。
- `examples/proposal_skill_examples.md`：常规任务少样例。
- `examples/deliverable_proposal_examples.md`：可交付项目书、专家经验融合和定稿前红队少样例。

## 推荐使用方式

1. 先上传当年指南、申报模板、评分标准、已有项目素材和依托单位通知。
2. 让 Skill 先建立“约束矩阵”和“事实台账”，再写标题、摘要和正文。
3. 整本项目书建议按 V0–V5 推进：约束盘点 → 主线骨架 → 正文草稿 → 模拟评审 → 定稿润色 → Word 交付文档。
4. 专家经验只作为写作动作和检查清单，不能替代当年官方指南和依托单位要求。

## 合规提醒

正式申报前必须由申请人、财务、伦理/数据、知识产权、科研管理部门和合作单位按职责核验。本 Skill 不生成未核实事实，不替代合规审查，不保证立项或中标。
