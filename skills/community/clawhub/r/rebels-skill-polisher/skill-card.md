## Description:

Polishes standalone skills and multi-skill bundles for ClawHub readability without sacrificing LLM effectiveness, including dependency mapping, regression checks, and reference-safe content moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill after a skill is built and tested to improve ClawHub listing readability while preserving behavior. It supports standalone skill polishing and multi-skill bundle polishing with audit and regression checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Polishing proposals can change standalone skills or multi-skill bundles in ways that affect agent behavior.

Mitigation: Review the generated audit report and approve overwrites only when the target is the ClawHub skill source intended for polishing.

## Reference(s):

- [Skill Polisher on ClawHub](https://clawhub.ai/99rebels/skills/rebels-skill-polisher)
- [Polishing Rules](references/rules.md)
- [Bundle Rules](references/bundle-rules.md)
- [Audit Guide](references/audit-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Polished Markdown skill files, reference files, and audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Waits for user approval before overwriting originals.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
