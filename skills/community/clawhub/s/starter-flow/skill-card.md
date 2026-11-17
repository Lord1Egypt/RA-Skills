## Description:

Starter Flow helps new OpenClaw users select and install five core skills through a guided onboarding flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to bootstrap a new OpenClaw environment by reviewing, selecting, and installing a starter set of skills. It also provides short next-step guidance after installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install multiple external skills from the ClawHub registry as part of one onboarding flow.

Mitigation: Review the five named dependencies before installing and install only the skills needed for the environment.

Risk: Broad onboarding trigger phrases could invoke this flow during ordinary setup conversations.

Mitigation: Confirm the selected skills and installation intent before running the installer.

Risk: The release under-discloses that installation depends on the ClawHub registry.

Mitigation: Verify publisher and version information in ClawHub before installation when the local OpenClaw setup supports it.

## Reference(s):

- [Starter Flow on ClawHub](https://clawhub.ai/largetool/skills/starter-flow)
- [largetool publisher profile](https://clawhub.ai/user/largetool)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and an interactive Bash installer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs user-selected skills through the ClawHub command-line tool when the installer is run.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
