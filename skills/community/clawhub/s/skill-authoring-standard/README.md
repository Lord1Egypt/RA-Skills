# Skill Authoring Standard

**A six-step standard for building production-ready Agent Skills — with a copy-paste template, eval cases, and an audit script that gates releases.**

Most skills fail not because the prompt is bad, but because one of six things is missing: a clear boundary, routing metadata, a complete SOP, resources/state, an evaluation set, or an iteration loop. This repository turns those into explicit gates.

## What's inside

| Path | Purpose |
|---|---|
| `SKILL.md` | The standard itself: boundaries, routing, SOP five modules, resources/state/permissions, evaluation, iteration |
| `assets/SKILL.template.md` | Copy-paste skeleton for a new skill |
| `assets/eval-cases.template.md` | Positive / negative / abnormal test cases + rubric |
| `references/six-step-standard.md` | Full six-step standard and launch checklist |
| `references/editorial-qa.md` | Section contracts, glossary/MECE, cold-reader review |
| `scripts/audit_skill.py` | Release gate: frontmatter, required sections, eval files, heading collisions |
| `eval/cases.md` | Test cases for this skill |
| `eval/failures.md` | Failure log template |

## The six steps

| # | Step | Deliverable | Gate |
|---|---|---|---|
| 1 | Define the scenario and boundary | "Can / must not" list + granularity note | Boundary explainable in one sentence |
| 2 | Configure metadata and routing | frontmatter + positive/negative routing cases | Routing accuracy ≥95% |
| 3 | Write the SOP | Goal & acceptance, fixed flow, dependencies, presentation format, exception fallback | Five modules present |
| 4 | Add resources and state | few-shot, references, templates, `.skill-state/`, permission rules | Degradation path for missing deps; confirmation for high-risk actions |
| 5 | Build evaluation | `eval/cases.md` + rubric | No evaluation, no release |
| 6 | Roll out and iterate | version, `last_updated`, `eval/failures.md` | Every fix has a regression case |

## Quick start

```bash
# 1. Copy the template into your skills directory
mkdir -p ~/.zcode/skills/<your-skill>
cp assets/SKILL.template.md ~/.zcode/skills/<your-skill>/SKILL.md

# 2. Fill in the six steps, then add eval cases
mkdir -p ~/.zcode/skills/<your-skill>/eval
cp assets/eval-cases.template.md ~/.zcode/skills/<your-skill>/eval/cases.md

# 3. Run the audit gate
python scripts/audit_skill.py ~/.zcode/skills/<your-skill>

# 4. Self-test the auditor
python scripts/audit_skill.py --selftest
```

## What the audit checks

- Required frontmatter: `name`, `description`, `user-invocable`, `version`, `last_updated`
- `description` contains triggers and an "not applicable" / disabled scenario
- Required sections: boundary list, routing metadata, workflow, dependencies, exception fallback, state & permissions, evaluation, iteration
- `eval/cases.md` and `eval/failures.md` exist
- Sibling headings do not share an unqualified abstract word (`output`, `standard`, `format`, `goal`, `flow`, etc.)
- Optional `assets/`, `references/`, `scripts/` presence

Exit code `0` means pass (warnings allowed), `1` means a hard failure. Use it as a pre-release gate.

## Editorial quality gate

Two problems are not caught by structural checks: **misplaced content** (a definition sitting in the iteration section) and **naming collisions** (two headings that read like the same thing). The standard adds:

1. A section contract: each section states what question it answers, what it accepts, and what it rejects.
2. A glossary + MECE test: two modules sharing an unqualified word must be renamed or given a "not responsible for" scope.
3. A cold-reader review: read only headings and first sentences, then ask whether each sentence answers its heading and whether two headings are distinguishable.
4. An automated sibling-heading collision warning in the audit script.

## Compatibility

Works with Agent Skills that use `SKILL.md` plus YAML frontmatter (ZCode, Claude Code, and compatible runners). The examples use `~/.zcode/skills/`; substitute your runner's skills directory.

## 中文说明

这个仓库把「定边界 → 配元信息 → 编 SOP → 配资源 → 建评测 → 灰度迭代」做成了一个可执行的 skill：

- **边界**：先写“能做什么 / 绝对不做什么”，避免大而全或碎而杂。
- **路由**：description 里写触发词和“不适用于”，配正反用例，目标路由准确率 ≥95%。
- **SOP**：目标与验收标准、固定流程、依赖、呈现格式、异常兜底五模块缺一不可。
- **资源**：模板、few-shot、中间状态、高风险二次确认。
- **评测**：路由准确率、任务完成率、抗幻觉；无评测不上线。
- **迭代**：版本、失败回流、回归集。
- **编辑质量门**：章节契约、术语表/MECE、冷读者复审、标题撞词检查。

审计命令：

```bash
python scripts/audit_skill.py <skill_dir>
python scripts/audit_skill.py --selftest
```

## License

MIT. See [LICENSE](LICENSE).
