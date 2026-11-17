# AGENTS.md — skill-quality-inspector

本仓库是一个 **AI Agent 技能库**（superpower 架构），用于治理 skills-repo 组织内的技能仓库质量。

## 目录约定（superpower 五层）

```
skill-quality-inspector/
├── SKILL.md          # L1 路由层：能力索引表，唯一入口
├── references/       # L2 深层 playbook（按需加载）
├── skills/           # L3 细粒度子技能（可单独 npx skills add）
├── scripts/          # L4 确定性脚本（stdlib-only，带 --help）
├── assets/           # L5 模板资源
├── AGENTS.md         # 本文件
├── README.md         # 面向人类的项目文档
├── LICENSE           # MIT
└── .gitignore
```

## 加载顺序

1. 先读根 `SKILL.md` 路由表，判断任务落到哪一类。
2. 方法论决策 → 读对应 `references/<topic>.md`。
3. 要落地具体动作 → 直接调 `skills/<name>/SKILL.md` 或跑 `scripts/<name>.py`。
4. 复用模板 → 取 `assets/`。

## SKILL.md 格式

- 根 `SKILL.md`：frontmatter 含 `name`/`description`/`agent_created: true`/`metadata.architecture: superpower`；≤150 行；无 TODO；路由表每行带 grep 关键词。
- 子技能 `skills/<name>/SKILL.md`：frontmatter 含 `name`/`description`/`source.*`（Q5）；`name` 与目录名一致；正文含 能力/使用方式/工作流/适用场景/限制。

## 工作约定

- **编写语言**：正文中文，技术术语保留英文。
- **内容范围**：只治理组织内部技能仓库，不评价单领域技能内容好坏。
- **设计原则**：确定性任务脚本化（scripts/），可复用模板沉淀（assets/），方法论展开（references/），不把方法论塞进 L1。

## 技能添加流程

1. 在 `skills/<new-name>/SKILL.md` 写子技能（source.type 标注 original/derived）。
2. 在根 `SKILL.md` 路由表新增一行（含 grep 关键词）——漏了等于对 Agent 不可见。
3. 若带来新方法论，评估是否新增 `references/<topic>.md`。
4. 更新 README 技能清单表。
5. 跑 `audit_architecture.py --repo skill-quality-inspector --strict` 与 `audit_readme_gates.py --repo skill-quality-inspector --strict`。

## 不做什么

- 不自动修改被测仓库文件（只读默认）；修复需用户显式授权。
- 不删除已发布子技能目录（只增不减，下线走 `deprecated: true`）。
- 不替代 `skills-repo-admin` 的架构 / 内容门禁脚本，只做其之上的跨文件一致性补充。
