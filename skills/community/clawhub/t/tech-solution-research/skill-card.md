## Description: <br>
Supports technical solution research, framework selection, technical comparisons, and final report generation through multi-source evidence orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and technical decision-makers use this skill to compare frameworks, libraries, services, or architecture options and produce evidence-backed implementation recommendations. It is intended for technical feasibility and selection work, not market sizing or business strategy research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research tasks may prompt the agent to access external tools, accounts, browser automation, social or platform connectors, GitHub, and internal documents. <br>
Mitigation: Confirm authorized tools, accounts, scopes, and data boundaries before use, especially when internal or account-bound sources are involved. <br>
Risk: Technical recommendations can be misleading when based on stale, single-source, or unverified evidence. <br>
Mitigation: Require multi-source evidence, record evidence freshness, mark missing runtime validation explicitly, and review final recommendations before acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanyasheng/tech-solution-research) <br>
- [Evidence Schema](references/evidence-schema.md) <br>
- [Technical Research Report Template](references/report-template.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Source Matrix](references/source-matrix.md) <br>
- [Workflow](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, evidence matrices, scoring summaries, implementation plans, citations, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify evidence coverage, confidence, unresolved validation gaps, risks, and recommended next steps.] <br>

## Skill Version(s): <br>
0.3.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
