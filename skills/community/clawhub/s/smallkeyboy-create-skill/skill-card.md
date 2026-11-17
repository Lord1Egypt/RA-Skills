## Description:

A callable skill factory for programmatic skill creation that accepts structured parameters and generates a complete, validated skill package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to generate new agent skill packages from structured inputs, including SKILL.md plus optional scripts, references, and assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied filenames or output paths can write files outside the intended skill folder.

Mitigation: Fix filename and path handling before installation; until then, do not feed untrusted skill configs and restrict output locations.

## Reference(s):

- [AgentSkills Specification Reference](artifact/references/skill-spec.md)
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/skills/smallkeyboy-create-skill)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Configuration]

**Output Format:** [JSON result plus generated Markdown, code, and resource files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates SKILL.md and optional scripts, references, assets, and package files when requested.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
