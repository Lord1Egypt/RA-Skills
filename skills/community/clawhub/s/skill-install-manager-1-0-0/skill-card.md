## Description:

Guides agents through a skill installation workflow that requires vetting before install and rejects installs that would require configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryren2024](https://clawhub.ai/user/terryren2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to follow a conservative skill-installation workflow with pre-install vetting, user confirmation, and rejection of installs that require configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer reports a canned SAFE TO INSTALL result instead of performing real skill vetting.

Mitigation: Replace the simulated report with a fail-closed call to a real vetting process before using the skill for untrusted installs.

Risk: The configuration-change check is simulated and assumes no configuration changes are required.

Mitigation: Add explicit checks for requested file or configuration changes and stop the install whenever those checks cannot prove the install is safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryren2024/skills/skill-install-manager-1-0-0)
- [Artifact README](artifact/README.md)
- [Safe install script](artifact/scripts/safe-install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and a Bash helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI for ClawHub installs; mentions optional COMPOSIO_API_KEY for Composio search.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
