## Description:

Helps users discover and install agent skills from skills.sh, clawhub.com, and tessl.io. Use when the user asks to find a skill for a task, extend agent capabilities, or search for tools/workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdwelle](https://clawhub.ai/user/bdwelle)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to find relevant agent skills across multiple registries, compare installation options, and decide whether to install a skill for a specific task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users to search public registries and install third-party agent skills globally.

Mitigation: Check the selected skill's publisher, source, version, and instructions before installation.

Risk: The skill includes install flows that can skip confirmation prompts for skills.sh global installs.

Mitigation: Prefer pinned versions or immutable commits, avoid global installs unless needed, and do not use skipped-confirmation flags for unreviewed skills.

## Reference(s):

- [Unified Find Skills on ClawHub](https://clawhub.ai/bdwelle/skills/unified-find-skills)
- [skills.sh](https://skills.sh/)
- [ClawHub](https://clawhub.ai/)
- [Tessl Skills Registry](https://tessl.io/registry/discover?contentType=skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include registry-specific install commands and links for matching skills.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
