## Description:

Create, validate, security-scan, and publish skills to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theashbhat](https://clawhub.ai/user/theashbhat)

### License/Terms of Use:


## Use Case:

Developers and skill publishers use this skill to scaffold skill directories, validate required metadata and naming, run an advisory security scan, and publish releases to ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing commands can run unintended local commands because the server security summary reports a command-injection risk.

Mitigation: Review generated shell commands and script arguments before execution, especially values passed to publishing options.

Risk: The publishing workflow includes unsafe escape hatches that can bypass validation or security checks.

Mitigation: Avoid --skip-checks and --force unless a reviewer has explicitly accepted the risk for the release.

Risk: The included security scan is advisory and may not catch every issue before publishing.

Mitigation: Review the full skill folder for secrets, unexpected network behavior, and unsafe scripts before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theashbhat/skills/skillpub)
- [Publisher profile](https://clawhub.ai/user/theashbhat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scaffolded skill files and publishing commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
