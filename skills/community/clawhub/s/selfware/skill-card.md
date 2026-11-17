## Description:

Defines a unified file protocol that bundles canonical data, logic, and views so agents and people can collaborate around self-contained, evolving files or .self packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozii](https://clawhub.ai/user/mozii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a protocol reference for creating Selfware runtimes, packages, views, update flows, collaboration flows, and consent boundaries around canonical data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or selected runtimes could expose local services beyond the intended boundary.

Mitigation: Bind servers to localhost or loopback unless the user explicitly configures a wider boundary.

Risk: Updates, publishing, discovery, or collaboration flows could modify files or send context externally without sufficient consent.

Mitigation: Require explicit user confirmation, minimal context sharing, rollback points, and change records before applying updates, publishing, or sending context.

Risk: Generated implementations may fail to preserve the promised canonical data write boundaries.

Mitigation: Review implementation output against the release security guidance and limit default writes to content/ or the declared canonical landing scope.

## Reference(s):

- [Artifact skill source](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/mozii/skills/selfware)
- [Selfware protocol source](https://floatboat.ai/selfware.md)
- [Release changelog](https://github.com/floatboatai/selfware.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Code]

**Output Format:** [Markdown protocol guidance with API, packaging, update, collaboration, and consent requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent outputs should preserve explicit consent, localhost exposure, canonical data write-scope, rollback, and change-record requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact protocol draft 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
