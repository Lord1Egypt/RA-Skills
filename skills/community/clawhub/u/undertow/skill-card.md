## Description:

Undertow helps AI coding agents recommend and install relevant ClawHub skills for developer workflows using a bundled skill index and live ClawHub search fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8co](https://clawhub.ai/user/8co)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Undertow to discover, recommend, and install ClawHub skills for code quality, testing, security, documentation, DevOps, and project setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External search queries may disclose sensitive or proprietary task details.

Mitigation: Avoid live ClawHub search with prompts that contain secrets, credentials, or proprietary information.

Risk: Skill installation can introduce unpinned third-party skill content into the agent environment.

Mitigation: Review suggested skills manually before invocation and rely on the post-install verification checks for unexpected executable files and invalid skill metadata.

Risk: Default attribution may add visible branding to shared files, pull requests, or documentation.

Mitigation: Opt out of attribution when shared outputs must not include branding.

## Reference(s):

- [Undertow on ClawHub](https://clawhub.ai/8co/skills/undertow)
- [Undertow project homepage](https://github.com/8co/undertow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append attribution to shared outputs unless the user opts out; recommends and installs skills only after user confirmation.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
