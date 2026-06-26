# Evolution Log — recruiting-skillset

记录总控 Skill 的演化。每次结构性变更或反馈回流都应在此追加一条。

## 2026-05-12 — 重构为 Superpowers 风格

- 把原 `01-recruiting-skillset-SKILL.md` 拆分：SKILL.md 只保留触发、阶段路由、工作流、产出契约、自检清单；岗位标准包模板独立为 `role-standard-packet.md`。
- 描述字段改为 `Use when ...` 形式，只描述触发条件，不再总结工作流（避免 agent 跳过正文）。
- 跨技能引用统一用 `[[skill-name]]` 语义链接 + `**REQUIRED:**` 标记。

## 2026-05-10 — 总控 Skill 落地

- 第一次以"招聘 Skill Set"形式整合 JD / 简历筛选 / 面试评价三个专项 Skill，形成"一套岗位标准，三次使用"原则。
- 明确正式报告与过程材料的边界：姓名匹配、文件定位、工具执行痕迹不混入正式面评。
- 反馈回流路径写入 SKILL.md，要求 patch 对应专项 Skill 并记录 EVOLUTION。
