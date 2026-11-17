## Description:

小郑女娲 is a Chinese-language cognitive distillation workflow that researches public information, extracts a person's thinking patterns, and generates a callable SKILL.md with explicit uncertainty boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boomzikazita](https://clawhub.ai/user/boomzikazita)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to research public material about a person, distill a five-layer cognitive framework, and generate an installable persona-style SKILL.md. It is intended for workflows where generated claims and boundaries are reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated persona skills may contain inaccurate or overconfident claims when public information is limited.

Mitigation: Review each generated SKILL.md, verify source support, and preserve explicit uncertainty or limited-public-data warnings before relying on it.

Risk: The workflow can persist generated SKILL.md files into an OpenClaw skills directory for later agent use.

Mitigation: Inspect generated files before enabling them for future sessions or sharing them with other users.

## Reference(s):

- [认知蒸馏方法论](references/extraction-framework.md)
- [认知框架 SKILL.md 模板](references/skill-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Guidance]

**Output Format:** [Markdown SKILL.md content with YAML frontmatter and structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills should cite public sources, include verified examples, and state what the persona skill cannot do.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
