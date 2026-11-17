## Description:

技术方案调研/框架选型/技术对比/最终报告生成 - multi-source evidence orchestration for technical decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and technical decision-makers use this skill to compare technical options, collect multi-source evidence, score tradeoffs, and produce implementation-oriented recommendations. It is intended for technical solution research, framework selection, technical comparisons, feasibility assessment, and risk review rather than market sizing or business-only analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research may rely on external web, GitHub, platform, or community sources that can change or conflict.

Mitigation: Record source dates, separate first-party evidence from community interpretation, and review key recommendations before acting on them.

Risk: Runtime tests, platform tools, or internal materials may expose sensitive context if used without clear scope.

Mitigation: Ask for the preferred language and source boundaries up front, and avoid private repositories or internal documents unless they are necessary for the task.

Risk: A technical report can become misleading if missing tests or source coverage gaps are presented as settled conclusions.

Mitigation: Use the skill's coverage checklist, mark unavailable runtime validation as pending, and keep unresolved evidence conflicts visible in the final recommendation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/tech-solution-research)
- [Publisher Profile](https://clawhub.ai/user/lanyasheng)
- [Evidence Schema](references/evidence-schema.md)
- [Report Template](references/report-template.md)
- [Source Matrix](references/source-matrix.md)
- [Scoring Rubric](references/scoring-rubric.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with evidence matrices, scoring tables, risk lists, implementation paths, references, and optional code or shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured evidence records, source coverage notes, runtime validation status, and citations.]

## Skill Version(s):

0.3.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
