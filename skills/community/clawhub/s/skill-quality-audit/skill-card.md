## Description:

Audits and quality-reviews AI agent SKILL.md files against Nevo Systems skill-writing practices for trigger quality, structure, conciseness, progressive disclosure, common mistakes, resource bundling, and trigger testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangwei8387](https://clawhub.ai/user/zhangwei8387)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review AI agent skill definitions before release or revision. It produces a structured audit with severity-ranked findings, trigger tests, and quality scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadly phrased skill-review requests may trigger this skill when a more specific review process was intended.

Mitigation: Narrow the skill description or invocation guidance if precise skill routing is important.

Risk: Audit output is advisory and could contain incorrect or incomplete recommendations for changing a skill.

Mitigation: Have a human maintainer review findings before applying changes or releasing the reviewed skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhangwei8387/skills/skill-quality-audit)
- [Publisher profile](https://clawhub.ai/user/zhangwei8387)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review with a findings table, trigger test list, and numeric score summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity labels are critical, warning, and nit; output is intended for human review before skill changes are applied.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
