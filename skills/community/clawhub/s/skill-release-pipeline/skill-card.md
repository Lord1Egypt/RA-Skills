## Description:

Automate packaging, pushing to GitHub, and publishing OpenClaw skills to ClawHub, managing versions and sync across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerozlw](https://clawhub.ai/user/zerozlw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare OpenClaw skill folders for release, push them to GitHub, publish them to ClawHub, and manage versioned updates or forks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing commands can commit, push, and publish an entire selected skill folder.

Mitigation: Review the folder contents for secrets and unintended files before use, and run the workflow from a clean repository.

Risk: The workflow can invoke an unpinned ClawHub CLI during publishing.

Mitigation: Prefer a pinned or preinstalled ClawHub CLI and verify authentication before running publish commands.

Risk: Network publishing may have broad effects once commands are executed.

Mitigation: Use a manifest preview or manual confirmation step before pushing to GitHub or publishing to ClawHub.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may propose commands that commit, push, and publish a selected skill folder.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
