---
name: skill-quality-scorer
description: >-
  Deterministic TRACE+ quality scorer for Agent Skills (SKILL.md): six dimensions T-R-F-S-I-E,
  30 sub-items, merges TRACE, good-skill authoring reverse-rubric (Extra08/skill-creator), and
  ClawHub meta-skills (skill-reviewer, skill-quality-audit). Use when scoring, rating, auditing,
  or comparing skills; or says「给技能打分」「技能评分」「和同类 skill 差在哪」「是否符合规范」.
  Runs static_audit.py first; outputs JSON + Markdown. Not TRACE-only.
disable-model-invocation: true
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

## 评测模式

| 模式 | 输出 |
|------|------|
| 单个 | JSON + Markdown（[audit-playbook](references/audit-playbook.md)） |
| A vs B | 两份 JSON + 分差表 + 推荐 |
| 批量 | 汇总表 + 各 skill 简评 |

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

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/scoring-engine-deterministic.md](references/scoring-engine-deterministic.md) | 30 子项 rubric · 公式 · JSON schema |
| [references/audit-playbook.md](references/audit-playbook.md) | 报告模板 · 对比/批量 · 触发测试 |
| [examples/sample-score-v2.json](examples/sample-score-v2.json) | JSON 样例 |
| [scripts/static_audit.py](scripts/static_audit.py) | 静态审计（唯一运行时脚本） |
