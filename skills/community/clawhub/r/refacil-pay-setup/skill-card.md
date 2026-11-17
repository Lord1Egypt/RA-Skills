## Description:

Refacil Pay Setup installs and configures the Refacil Pay CLI for Colombian payment workflows, then hands off operations to the installed operating skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erikole21](https://clawhub.ai/user/erikole21)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this setup skill to install refacil-pay-cli and configure its operating skill before working with Refacil Pay payment flows in Colombia.

### Deployment Geography for Use:

Colombia

## Known Risks and Mitigations:

Risk: The setup delegates persistent agent instructions to an unpinned external npm package in a payment context.

Mitigation: Install only from a trusted publisher, prefer a pinned and reviewed package version, and inspect the generated operating skill and AGENTS.md before activation.

Risk: The installed operating skill may support payment or money movement actions after setup.

Mitigation: Require explicit user confirmation before any payment or money movement command runs with automatic approval flags.

Risk: Interactive install or login commands can hang or expose sensitive credentials in an agent shell.

Mitigation: Use non-interactive install forms such as --path, --ide, or --yes, and authenticate through browser or device flows without typing or storing user passwords.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erikole21/skills/refacil-pay-setup)
- [refacil-pay-cli npm package](https://www.npmjs.com/package/refacil-pay-cli)
- [Publisher Profile](https://clawhub.ai/user/erikole21)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation and setup; does not execute payment operations itself.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
