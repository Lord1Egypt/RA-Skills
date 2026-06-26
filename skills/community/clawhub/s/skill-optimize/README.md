# Skill Optimizer

> EN | [中文](README.zh-cn.md)

An opinionated, focused tool for **auditing and improving existing Agent Skills** (`SKILL.md` files) against the [agentskills.io](https://agentskills.io/) standard. Where [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) covers the full create-from-scratch workflow (interview → draft → eval → iterate), this skill is the lighter, faster counterpart you reach for when the skill already exists and the question is "how do I make it better?"

## When to use this

- "Audit my skill against the spec"
- "Improve the triggering of my skill"
- "Rewrite the frontmatter description"
- "This skill is too long — help me trim it"
- "Review this skill before I publish it"
- "Add gotchas and examples to my skill"
- Any request to edit, polish, or refine an existing `SKILL.md`

If the user wants to **create** a new skill from scratch, hand off to `skill-creator`. If they want to **measure output quality** with evals and baselines, also hand off to `skill-creator`. This skill optimizes the *artifact*; `skill-creator` measures the *outcome*.

## The 3-dimension audit

The optimization framework is built on the three pillars from [agentskills.io](https://agentskills.io/):

1. **Specification compliance** — Is the file structurally valid? Does the frontmatter conform? Are naming and length rules respected?
2. **Best practices alignment** — Is the content clear, scoped, and well-organized?
3. **Description optimization** — Will the skill trigger on the right prompts and stay quiet on the wrong ones?

Always run the dimensions in this order: spec first (binary, blocks loading), best practices next (content quality), description last (triggering accuracy). The bundled `scripts/audit_skill.py` handles Dimension 1 mechanically; Dimensions 2 and 3 are judgment-based and use the bundled reference checklists.

## What's in this skill

```
skill-optimizer/
├── SKILL.md                              # Main entry point
├── README.md                             # This file (English)
├── README.zh.md                          # 中文文档 (Chinese)
├── references/
│   ├── specification-checklist.md       # Dimension 1 — spec checks
│   ├── best-practices-checklist.md      # Dimension 2 — content quality
│   ├── description-guide.md             # Dimension 3 — description optimization
│   └── common-issues.md                 # 18 recurring problems and fixes
├── scripts/
│   └── audit_skill.py                   # Programmatic spec + body audit
└── assets/
    └── report-template.md               # Report structure to fill in
```

## Quick start

Run the mechanical audit on any existing skill:

```bash
python3 scripts/audit_skill.py /path/to/target-skill
```

Or in JSON form (for piping into other tools):

```bash
python3 scripts/audit_skill.py /path/to/target-skill --json
```

Exit codes: `0` (clean), `1` (majors), `2` (blockers), strict mode also counts minors and nits.

For a full optimization pass — including Best Practices review and Description rewrites — invoke the `skill-optimizer` skill from your agent. The skill walks through the full workflow: capture intent → locate & snapshot → 3-dimension audit → generate report → propose edits → apply with approval.

## Sources

The audit checklists and best-practices are synthesized from:

- [agentskills.io Specification](https://agentskills.io/specification) — file structure, frontmatter, naming, length rules
- [agentskills.io Best Practices](https://agentskills.io/skill-creation/best-practices) — scope, calibration, defaults, procedure over declaration, gotchas, output templates, progressive disclosure
- [agentskills.io Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — triggering, eval queries, train/test split, the optimization loop
- [OpenClaw skill-format](https://docs.openclaw.ai/clawhub/skill-format) — bundle size discipline, declaration-vs-actual alignment, cost/credential transparency (universal subset only)
- [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) — the upstream create-from-scratch workflow this skill complements

## License

MIT-0. Anyone may use, modify, and redistribute, including commercially.

---

[中文文档 / Chinese version →](README.zh.md)
