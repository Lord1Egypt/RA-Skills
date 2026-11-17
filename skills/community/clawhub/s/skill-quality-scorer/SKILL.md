---
name: skill-quality-scorer
description: >-
  Deterministic TRACE+ quality scorer for Agent Skills (SKILL.md): six dimensions T-R-F-S-I-E,
  30 sub-items, merges TRACE, good-skill authoring reverse-rubric (Extra08/skill-creator), and
  ClawHub meta-skills (skill-reviewer, skill-quality-audit). Use when scoring, rating, auditing,
  or comparing skills; or says「给技能打分」「技能评分」「和同类 skill 差在哪」「是否符合规范」.
  Runs static_audit.py first; outputs JSON + Markdown. Not TRACE-only.
---

# Skill Quality Scorer · 技能质量评分器

> **EN** TRACE+ (T-R-F-S-I-E) × 30 sub-items · static script first · formula score · JSON + Markdown.  
> **中文** TRACE+ 六维 30 子项 · 先 static_audit · 公式算分 · JSON + Markdown。

**When / 何时用：** 迭代没方向 · 对标同类 · 发布前自检 · 批量评 `skills/`  
**Not / 不用：** 从零写 Skill · 替代 skill-eval 行为实验（E 维默认 `static_proxy`）

```text
Score portfolio-doctor with TRACE+ — where vs skill-reviewer?
给 portfolio-doctor 做 TRACE+ 全维评分。
```

## 可直接触发的说法

以下口语输入都应触发本技能：

- 给这个 skill 打分。
- 看看这个技能哪里不符合规范。
- 用 TRACE+ 评一下这个 SKILL.md。
- 这两个技能哪个质量更高？
- 批量扫一下这个 skills 目录。
- SkillHub 分数低，帮我找提分项。
- 和 skill-reviewer 差在哪？

## 最小可用输入

**最低可启动**：一个目标 skill 目录，或一个 `SKILL.md` 文件路径。

**推荐输入**：目标路径、评分模式（单个/A vs B/批量）、是否有行为评测结果、期望输出格式（JSON / Markdown / 两者）。

**可兼容输入**：

- 只给目录：自动定位目录下 `SKILL.md`。
- 只给父目录：按批量模式逐个扫描子目录。
- 只给两条路径：按 A vs B 对比模式。
- 没有 behavior eval：E 维使用 `static_proxy`，E3 不强行给满。

## 评测模式

| 模式 | 输出 |
|------|------|
| 单个 | JSON + Markdown（[audit-playbook](references/audit-playbook.md)） |
| A vs B | 两份 JSON + 分差表 + 推荐 |
| 批量 | 汇总表 + 各 skill 简评 |

评分前先确认输出格式：`JSON`、`Markdown` 或`两者`。用户未指定时，默认输出 JSON + Markdown。

对比/批量：**同一 rubric v2**，不得换公式或跳过子项。

## 工作流

```text
1) 定位 skill 目录（对比/批量则逐个重复 2–6）
2) python scripts/static_audit.py "<skill-dir>" → auto_scores（不可改分）
3) Read scoring-engine-deterministic.md → 30 子项 evidence
4) Read 目标 SKILL.md + 链接的 references/scripts
5) composite = round((T+R+F+S+I+E)×100/60, 1) → 评级 + Verdict
6) 按 audit-playbook 输出（含 F 维触发测试各 ≥3 条）
```

评级 / Verdict / 30 子项定义 / JSON schema → [scoring-engine-deterministic.md](references/scoring-engine-deterministic.md)

## 硬约束

1. 先脚本后 rubric；`auto_scores` 只补 evidence 不改分
2. 30 子项逐项 evidence；禁止旧公式 `(T+R+A+C+E)×2`
3. E 维默认 `static_proxy`；有 skill-eval 时切换 `behavioral_eval`
4. **Rigid**：子项、公式、Verdict 不可改 · **Flexible**：evidence 表述、Top 修复排序

## 验收与失败路径

- **路径不存在**：先要求用户提供正确路径，不得凭名称臆测
- **缺少 SKILL.md**：判定目标不是标准 skill 包，输出结构问题而非强行评分
- **批量模式**：每个 skill 必须使用同一 rubric v2 和同一公式
- **无行为评测**：明确标注 `effectiveness_mode: static_proxy`
- **完成标准**：JSON 算术校验通过，Markdown 报告含 Top 修复项和触发测试

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) | 30 子项 rubric · 公式 · JSON schema |
| [references/audit-playbook.md](references/audit-playbook.md) | 技能质量审计方法手册：报告模板 · 对比/批量 · 触发测试 |
| [examples/sample-score-v2.json](examples/sample-score-v2.json) | JSON 样例 |
| [scripts/static_audit.py](scripts/static_audit.py) | 静态审计（唯一运行时脚本） |
