## Description:

SharpAgent Skill Contract — Schema-driven skill scaffolding tool. Generates, validates, and packages SharpAgent-compliant skills with five-factor trust verification, calibration framework hooks, and content safety integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to scaffold, validate, package, and upgrade SharpAgent-compliant skills for ClawHub publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced sharpagent CLI commands could create or package files using an untrusted local CLI installation.

Mitigation: Confirm the sharpagent CLI source before running commands.

Risk: Generated or upgraded skill files could contain incorrect contract details before publication.

Mitigation: Review and scan generated skill files before publishing them to ClawHub.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/skills/sharpagent-skill-contract)
- [Publisher Profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with YAML, JSON, directory tree, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents SharpAgent contract fields, validation checks, packaging workflow, dependencies, and edge cases.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
