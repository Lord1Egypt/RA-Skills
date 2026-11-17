## Description:

Review a public repository release across version and tag consistency, final build artifacts, archives, secrets and internal material, third-party licenses, production response headers, and GitHub Release attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wardlu](https://clawhub.ai/user/wardlu)

### License/Terms of Use:

MIT

## Use Case:

Developers and release engineers use this skill to perform a manual public-release gate before publishing tags, GitHub Releases, final archives, installers, or production launch artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may suggest adding a release-gate.config.json file when release automation is missing.

Mitigation: Treat the configuration file as a separate repository change requiring explicit user approval before writing it.

Risk: Release operations such as creating tags, publishing GitHub Releases, uploading attachments, changing production configuration, or deploying could affect public artifacts or production state.

Mitigation: Keep the review read-only by default and require explicit user authorization before performing any release, upload, configuration, or deployment action.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Structured Markdown release review record with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The review result reports PASS, BLOCKED, or FAILED with evidence and residual risks.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
