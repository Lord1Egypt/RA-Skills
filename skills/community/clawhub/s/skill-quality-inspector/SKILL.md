---
name: skill-quality-inspector
description: >-
  技能质量检查官：检查技能仓库质量、修复技能矛盾点、评估技能风险、减少技能冗余、规范技能目录。
  覆盖 superpower 五层结构校验、质量门禁（Q1–Q10/W1–W7）对账、断链与数字矛盾扫描、
  安全/维护/合规三维风险评估、跨仓库重名与近重检测。
  触发词："技能质量"、"质量门禁"、"矛盾修复"、"风险评估"、"技能冗余"、"目录规范"、
  "skill audit"、"quality gate"、"skill lint"。
agent_created: true
metadata:
  version: 1.0.0
  category: 技能治理
  difficulty: 进阶
  architecture: superpower
---

# 技能质量检查官

> 把 AI 助手变成一名技能仓库的"质检 + 风控 + 整理"搭档：拿组织规范当尺子，逐条量一个技能仓库是否达标、有无隐患、是否冗余、目录是否规范。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 新建技能仓库提交前做质量自检
- 定期巡检组织内所有仓库的健康度与账实一致性
- 合并 PR 前的质量 / 安全卡点
- 发现 README 与 SKILL.md 数字对不上、链接断了、规则打架
- 新仓库立项前排查与已有仓库的功能重叠
- 把 legacy 仓库迁移到 superpower 时的结构对齐

## 能力索引（超级技能路由）

本技能采用渐进式加载。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook。

| 任务 | 读取·调用 | grep 关键词 |
|------|-----------|-------------|
| 质量维度与门禁对照 | [references/quality-dimensions.md](references/quality-dimensions.md) | 质量门禁、Q1-Q10、W1-W7、质检清单 |
| 矛盾点检测方法论 | [references/contradiction-detection.md](references/contradiction-detection.md) | 矛盾、断链、数字对账、术语漂移、重复标题 |
| 风险评估矩阵 | [references/risk-assessment.md](references/risk-assessment.md) | 风险、P1/P2/P3、安全、维护、合规 |
| 冗余识别与去重 | [references/redundancy-reduction.md](references/redundancy-reduction.md) | 冗余、重名、近重、只增不减、去重 |
| 目录规范化 | [references/directory-standardization.md](references/directory-standardization.md) | 五层结构、命名、路由完整性、Level A/B |

| 任务 | 读取·调用（子技能） | grep 关键词 |
|------|---------------------|-------------|
| 技能质量检查 | [skills/quality-auditor/SKILL.md](skills/quality-auditor/SKILL.md) | 质量检查、门禁对账、定级 |
| 技能矛盾点修复 | [skills/contradiction-fixer/SKILL.md](skills/contradiction-fixer/SKILL.md) | 矛盾修复、断链、数字不一致 |
| 技能风险评估 | [skills/risk-evaluator/SKILL.md](skills/risk-evaluator/SKILL.md) | 风险评估、安全、维护、合规 |
| 技能冗余治理 | [skills/redundancy-reducer/SKILL.md](skills/redundancy-reducer/SKILL.md) | 冗余治理、重名、重叠 |
| 技能目录规范化 | [skills/directory-standardizer/SKILL.md](skills/directory-standardizer/SKILL.md) | 目录规范、五层、路由孤儿 |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本做确定性检查，而非每次重写：

- `scripts/quality_audit.py --repo <path> [--json] [--strict]` — 结构 + 跨文件一致性 + 路由完整性，汇总质量报告
- `scripts/contradiction_scan.py --repo <path> [--json] [--strict]` — 断链 / 重复标题 / 数字矛盾 / 术语漂移
- `scripts/redundancy_scan.py --org <root> [--json] [--strict]` — 跨仓库重名 / 近重描述 / 关键词打架

运行示例：

```bash
python3 scripts/quality_audit.py --repo ../career-coach --strict
python3 scripts/contradiction_scan.py --repo ../career-coach
python3 scripts/redundancy_scan.py --org .. --json
```

## 模板资源

`assets/` 提供可直接套用的模板：

- [assets/quality-report-template.md](assets/quality-report-template.md) — 质量报告模板（阻断/警告/建议三档）
- [assets/risk-matrix.csv](assets/risk-matrix.csv) — 三维 × P1/P2/P3 风险矩阵骨架

## 核心原则（始终遵循）

1. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜命令。
2. **只读默认不改**：审计 / 扫描脚本默认只读，修复动作需用户显式授权。
3. **只增不减**：去重 / 下线一律走 `deprecated: true`，绝不删已发布路径（破坏下游 `skills-lock.json`）。
4. **账实一致**：`registry/repos.json` 计数以实时扫描为准，不在旧数上 +1。
5. **明确边界**：只出报告与证据，不替仓库负责人拍板"是否发布"。
6. **脚本可验证**：每个脚本用坏 / 好样本验证，误报同属 bug。

## 与其他技能协作

- 结构 / 内容门禁的事实来源是 `skills-repo-admin` 的 `audit_architecture.py` 与 `audit_readme_gates.py`（本仓库脚本做其之上的跨文件一致性补充，不重复造轮子）。
- 规范定义见 `skills-repo-admin/rules/`（`superpower-architecture.md` / `quality-gates.md` / `skill-format.md` / `repo-structure.md`）。
- 新仓库创建流程见 `skills-repo-admin/workflows/creation.md`。
