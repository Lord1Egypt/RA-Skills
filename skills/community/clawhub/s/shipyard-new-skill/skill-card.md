## Description:

Helps coding-agent users design, build, test, and prepare reusable skills or plugins for publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

Coding-agent users use this skill to turn recurring workflows into reusable skills or plugins, then test and prepare them for release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full Shipyard plugin scripts and optional third-party skills were not inspected in this release evidence, so their behavior is not assessed here.

Mitigation: Review the full plugin and any optional skills before installation, and prefer fixed installer versions.

Risk: The workflow may read a user's codebase or agent chat summaries when building a skill.

Mitigation: Approve only the code and chat access needed for the task.

## Reference(s):

- [Shipyard new-skill instructions](artifact/SKILL.md)
- [Skill anatomy guidance](artifact/references/anatomy.md)
- [Build or extend guidance](artifact/references/build-or-extend.md)
- [Publishing guidance](artifact/references/publish.md)
- [Shipyard installation instructions](https://github.com/philipposk/shipyard/blob/main/INSTALL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance and generated skill or plugin files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tests, manifests, and publishing notes for the resulting skill or plugin.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
